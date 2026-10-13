import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SHOWROOM = ROOT / "showroom"


class ShowroomTests(unittest.TestCase):
    def test_service_trace_uses_installed_json_tools(self):
        trace = (SHOWROOM / 'content/modules/ROOT/pages/02-trace.adoc').read_text()
        self.assertNotIn('yq ', trace)
        self.assertIn('oc get service {adapter_service} -n {namespace} -o json', trace)
        self.assertIn("jq '{selector: .spec.selector, ports: .spec.ports}'", trace)

    def test_health_probe_runs_from_the_learner_terminal(self):
        verify = (SHOWROOM / 'content/modules/ROOT/pages/01-verify.adoc').read_text()
        self.assertNotIn('wget -qO-', verify)
        self.assertIn('curl --connect-timeout 5 --max-time 30 -fsS http://{adapter_service}:8080/healthz | jq .', verify)
        inspect = (SHOWROOM / 'content/modules/ROOT/pages/04-inspect.adoc').read_text()
        self.assertNotIn('wget -qO-', inspect)
        self.assertIn('curl --connect-timeout 5 --max-time 30 -fsS "http://{adapter_service}:8080/api/v1/evidence/$REQUEST_ID"', inspect)

    def test_vm_commands_use_a_writable_seat_key_and_supported_ssh_syntax(self):
        attrs = yaml.safe_load((SHOWROOM / "content/antora.yml").read_text())["asciidoc"]["attributes"]
        self.assertTrue(attrs["ssh_key_path"].startswith("/tmp/"))
        pages = SHOWROOM / "content/modules/ROOT/pages"
        invoke = (pages / "03-invoke.adoc").read_text()
        failure = (pages / "05-failure.adoc").read_text()
        for text in (invoke, failure):
            self.assertIn("lab@vm/{vm_name}", text)
            self.assertIn("--command=", text)
            self.assertIn("StrictHostKeyChecking=accept-new", text)
            self.assertIn("sudo env LAB_NAMESPACE={namespace} VM_NAME={vm_name}", text)
            self.assertNotIn("lab@{vm_name} --", text)

    def test_runtime_verification_stays_inside_the_seat_namespace(self):
        verify = (SHOWROOM / "content/modules/ROOT/pages/01-verify.adoc").read_text()
        self.assertNotIn("oc get hyperconverged", verify)
        self.assertNotIn("-n openshift-cnv", verify)
        self.assertIn("oc wait -n {namespace} --for=condition=Ready", verify)
        self.assertIn("vmi/{vm_name}", verify)
        self.assertIn("Launchpad verifies the cluster-wide", verify)

    def test_deployed_showroom_discovers_the_playbook_from_repository_root(self):
        playbook = ROOT / "default-site.yml"
        self.assertTrue(playbook.is_file())
        config = yaml.safe_load(playbook.read_text())
        source = config["content"]["sources"][0]
        self.assertEqual(source["url"], ".")
        self.assertEqual(source["start_path"], "showroom/content")
        self.assertTrue((ROOT / source["start_path"] / "antora.yml").is_file())

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

    def test_lab_signposts_show_learn_do_prove_and_uses_the_console(self):
        pages = SHOWROOM / "content/modules/ROOT/pages"
        text = "\n".join(path.read_text() for path in pages.glob("*.adoc"))
        for heading in ("== Show", "== Learn", "== Do", "== Prove"):
            self.assertIn(heading, text)

        verify = (pages / "01-verify.adoc").read_text()
        self.assertIn("OpenShift Console", verify)
        self.assertIn("VirtualMachines", verify)
        self.assertIn("VirtualMachineInstances", verify)
        self.assertIn("Workloads", verify)

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
