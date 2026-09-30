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
        nav = (SHOWROOM / "content/modules/ROOT/nav.adoc").read_text()
        for page in ["01-verify", "02-trace", "03-invoke", "04-inspect", "05-failure", "06-evidence"]:
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


if __name__ == "__main__":
    unittest.main()
