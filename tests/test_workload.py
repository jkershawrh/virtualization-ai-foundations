import json
import os
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WorkloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["ADAPTER_MODE"] = "rehearsal"
        os.environ["ADAPTER_PORT"] = "0"
        from workload.app import create_server

        cls.server = create_server("127.0.0.1", 0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def request(self, path, payload=None):
        body = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}",
            data=body,
            headers={"Content-Type": "application/json"} if body else {},
            method="POST" if body else "GET",
        )
        with urllib.request.urlopen(request, timeout=2) as response:
            return response.status, json.load(response)

    def test_health_discloses_mode_without_secret(self):
        _, data = self.request("/healthz")
        self.assertEqual(data["mode"], "rehearsal")
        self.assertNotIn("api_key", json.dumps(data).lower())

    def test_healthy_rehearsal_response_is_labeled(self):
        payload = json.loads((ROOT / "contracts/examples/healthy-request.json").read_text())
        _, data = self.request("/api/v1/analyze", payload)
        self.assertEqual(data["source_state"], "REHEARSAL")
        self.assertTrue(data["ai_participated"])
        self.assertEqual(data["authority"]["actions_permitted"], [])

    def test_unavailable_condition_fails_closed(self):
        payload = json.loads((ROOT / "contracts/examples/healthy-request.json").read_text())
        payload["request_id"] = "22222222-2222-4222-8222-222222222222"
        payload["condition"] = "model-unavailable"
        _, data = self.request("/api/v1/analyze", payload)
        self.assertFalse(data["ai_participated"])
        self.assertIsNone(data["model"])
        self.assertIsNone(data["result"])

    def test_evidence_record_redacts_note(self):
        payload = json.loads((ROOT / "contracts/examples/healthy-request.json").read_text())
        self.request("/api/v1/analyze", payload)
        _, evidence = self.request(f"/api/v1/evidence/{payload['request_id']}")
        rendered = json.dumps(evidence)
        self.assertNotIn(payload["note"], rendered)
        self.assertRegex(evidence["request_sha256"], r"^[a-f0-9]{64}$")

    def test_invalid_request_returns_400(self):
        with self.assertRaises(urllib.error.HTTPError) as captured:
            self.request("/api/v1/analyze", {"schema_version": "analysis-request/v1"})
        self.assertEqual(captured.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
