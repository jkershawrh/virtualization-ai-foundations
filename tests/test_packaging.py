import subprocess
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHART = ROOT / "charts/virtualization-ai-foundations"


class PackagingTests(unittest.TestCase):
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

    def test_release_images_require_digests(self):
        values = yaml.safe_load((CHART / "values.candidate.yaml").read_text())
        for image in (
            values["adapter"]["image"],
            values["presentation"]["image"],
            values["vm"]["containerDisk"],
        ):
            self.assertRegex(image["digest"], r"^sha256:[0-9a-f]{64}$")
            self.assertTrue(image["repository"])


if __name__ == "__main__":
    unittest.main()
