import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SHOWROOM = ROOT / "showroom"


class ShowroomTests(unittest.TestCase):
    def test_showroom_has_independent_playbook(self):
        playbook = ROOT / "showroom/default-site.yml"
        self.assertTrue(playbook.exists())
        self.assertIn("start_page: virtualization-ai-101::index.adoc", playbook.read_text())

    def test_showroom_is_separate_and_complete(self):
        antora = yaml.safe_load((SHOWROOM / "content/antora.yml").read_text())
        self.assertEqual(antora["name"], "virtualization-ai-101")
        self.assertEqual(antora["version"], "main")
        playbook = yaml.safe_load((SHOWROOM / "default-site.yml").read_text())
        self.assertEqual(
            playbook["ui"]["bundle"]["url"],
            "https://github.com/rhpds/rhdp_showroom_theme/releases/download/v2.0.3/ui-bundle.zip",
        )
        nav = (SHOWROOM / "content/modules/ROOT/nav.adoc").read_text()
        for page in ["01-verify", "02-trace", "03-invoke", "04-inspect", "05-failure", "06-evidence", "07-cleanup"]:
            self.assertIn(page, nav)

    def test_lab_states_101_and_201_boundary(self):
        index = (SHOWROOM / "content/modules/ROOT/pages/index.adoc").read_text()
        self.assertIn("Virtualization + AI 101", index)
        self.assertIn("201", index)
        self.assertIn("author", index.lower())

    def test_lab_uses_correlation_and_source_state(self):
        text = "\n".join(path.read_text() for path in (SHOWROOM / "content/modules/ROOT/pages").glob("*.adoc"))
        self.assertIn("request_id", text)
        self.assertIn("source_state", text)
        self.assertIn("ai_participated", text)
        self.assertIn("human operator", text)

    def test_lab_never_embeds_secret_values(self):
        text = "\n".join(path.read_text() for path in SHOWROOM.rglob("*") if path.is_file())
        self.assertNotIn("MODEL_API_KEY=", text)
        self.assertNotIn("changeme", text.lower())

    def test_lab_prepares_a_per_seat_key_before_any_vm_origin_request(self):
        verify = (SHOWROOM / "content/modules/ROOT/pages/01-verify.adoc").read_text()
        invoke = (SHOWROOM / "content/modules/ROOT/pages/03-invoke.adoc").read_text()

        self.assertIn("VM_SSH_PRIVATE_KEY", verify)
        self.assertIn("chmod 600 {ssh_key_path}", verify)
        self.assertIn("different SSH keypair for every seat", verify)
        self.assertIn("virtctl ssh --identity-file={ssh_key_path}", invoke)

    def test_cleanup_removes_learner_secrets_and_preserves_platform_resources(self):
        cleanup = (SHOWROOM / "content/modules/ROOT/pages/07-cleanup.adoc").read_text()
        self.assertIn('rm -f "{ssh_key_path}"', cleanup)
        self.assertIn("oc auth can-i delete namespaces", cleanup)
        self.assertIn("must not delete", cleanup)
        self.assertIn("oc get vm,vmi", cleanup)
        self.assertIn('role="execute"', cleanup)


if __name__ == "__main__":
    unittest.main()
