import json
import subprocess
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHART = ROOT / "charts/virtualization-ai-foundations"


class PackagingTests(unittest.TestCase):
    def test_runtime_images_are_digest_pinned_and_minimal(self):
        presentation = (ROOT / "Containerfile").read_text()
        adapter = (ROOT / "workload/Containerfile").read_text()
        self.assertRegex(presentation, r"FROM cgr\.dev/chainguard/nginx@sha256:[0-9a-f]{64}")
        self.assertRegex(adapter, r"FROM cgr\.dev/chainguard/python@sha256:[0-9a-f]{64}")
        self.assertNotIn(":latest", presentation)
        self.assertNotIn(":latest", adapter)

    def test_helm_chart_lints_and_renders(self):
        lint = subprocess.run(["helm", "lint", str(CHART)], capture_output=True, text=True)
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        render = subprocess.run(
            ["helm", "template", "virtualization-ai", str(CHART), "--namespace", "virtualization-ai-101"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(render.returncode, 0, render.stderr)
        self.assertIn("kind: VirtualMachine", render.stdout)
        self.assertIn("kind: NetworkPolicy", render.stdout)

    def test_defaults_are_fail_closed_and_secret_free(self):
        values = yaml.safe_load((CHART / "values.yaml").read_text())
        self.assertEqual(values["adapter"]["mode"], "rehearsal")
        self.assertEqual(values["adapter"]["model"]["apiKeySecret"]["name"], "")
        self.assertNotIn("password", str(values).lower())

    def test_live_maas_egress_is_namespace_scoped(self):
        render = subprocess.run(
            [
                "helm", "template", "virtualization-ai", str(CHART),
                "--set", "adapter.model.egressNamespace=launchpad-flightpath-candidate",
                "--set", "adapter.model.egressPort=4000",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(render.returncode, 0, render.stderr)
        self.assertIn(
            'kubernetes.io/metadata.name: "launchpad-flightpath-candidate"',
            render.stdout,
        )
        self.assertIn("podSelector: {}", render.stdout)
        self.assertIn("port: 5353", render.stdout)
        self.assertIn("port: 4000", render.stdout)

    def test_local_candidate_images_require_digests(self):
        candidate = CHART / "values.candidate.yaml"
        values = yaml.safe_load(candidate.read_text())
        self.assertEqual(values["adapter"]["image"]["repository"], "localhost/virtualization-ai-adapter")
        self.assertEqual(values["presentation"]["image"]["repository"], "localhost/virtualization-ai-presentation")
        for image in (
            values["adapter"]["image"],
            values["presentation"]["image"],
            values["vm"]["containerDisk"],
        ):
            self.assertRegex(image["digest"], r"^sha256:[0-9a-f]{64}$")
            self.assertTrue(image["repository"])
        render = subprocess.run(
            ["helm", "template", "virtualization-ai", str(CHART), "-f", str(candidate)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(render.returncode, 0, render.stderr)
        self.assertIn(values["adapter"]["image"]["digest"], render.stdout)
        self.assertIn(values["presentation"]["image"]["digest"], render.stdout)

    def test_published_images_are_ghcr_digest_pinned_and_render(self):
        published = CHART / "values.published.yaml"
        values = yaml.safe_load(published.read_text())
        for component in ("adapter", "presentation"):
            image = values[component]["image"]
            self.assertTrue(image["repository"].startswith("ghcr.io/jkershawrh/"))
            self.assertRegex(image["digest"], r"^sha256:[0-9a-f]{64}$")
            self.assertRegex(image["tag"], r"^git-[0-9a-f]{40}$")
        render = subprocess.run(
            ["helm", "template", "virtualization-ai", str(CHART), "-f", str(published)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(render.returncode, 0, render.stderr)
        for component in ("adapter", "presentation"):
            image = values[component]["image"]
            self.assertIn(f'{image["repository"]}@{image["digest"]}', render.stdout)

    def test_published_receipts_are_distinct_and_non_certifying(self):
        values = yaml.safe_load((CHART / "values.published.yaml").read_text())
        handoff = yaml.safe_load((ROOT / "handoff/launchpad-handoff.yaml").read_text())
        for component, artifact_key in (("adapter", "workload"), ("presentation", "presentation")):
            receipt = json.loads(
                (ROOT / f"handoff/evidence/published-{component}-release.json").read_text()
            )
            expected_image = (
                f'{values[component]["image"]["repository"]}@'
                f'{values[component]["image"]["digest"]}'
            )
            self.assertEqual(receipt["evidence_scope"], "published_immutable_candidate")
            self.assertEqual(receipt["image"], expected_image)
            self.assertEqual(receipt["scan"]["severity_counts"]["high"], 0)
            self.assertEqual(receipt["scan"]["severity_counts"]["critical"], 0)
            self.assertEqual(receipt["certification"], "NOT CLAIMED")
            self.assertEqual(receipt["live_openshift_validation"], "NOT RUN")
            self.assertEqual(handoff["factory_receipt"]["artifacts"][artifact_key]["image"], expected_image)


if __name__ == "__main__":
    unittest.main()
