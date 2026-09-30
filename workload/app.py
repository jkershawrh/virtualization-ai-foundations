#!/usr/bin/env python3
"""Contract-first VM-to-AI evidence adapter using only the Python standard library."""

from __future__ import annotations

import hashlib
import json
import os
import re
import ssl
import sys
import threading
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


VERSION = "0.1.0"
ALLOWED_CATEGORIES = {"inspect", "schedule-maintenance", "escalate"}
ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "contracts" / "examples"
EVIDENCE: Dict[str, Dict[str, Any]] = {}
LOCK = threading.Lock()


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def mode() -> str:
    value = os.getenv("ADAPTER_MODE", "rehearsal").lower()
    return value if value in {"live", "rehearsal", "offline"} else "offline"


def source_state() -> str:
    return mode().upper()


def validate_request(payload: Any) -> Tuple[bool, str]:
    if not isinstance(payload, dict):
        return False, "request must be a JSON object"
    required = {"schema_version", "request_id", "origin", "note", "allowed_categories", "condition"}
    if set(payload) != required:
        return False, "request fields do not match analysis-request/v1"
    if payload["schema_version"] != "analysis-request/v1":
        return False, "unsupported schema_version"
    try:
        uuid.UUID(payload["request_id"])
    except (ValueError, TypeError, AttributeError):
        return False, "request_id must be a UUID"
    origin = payload["origin"]
    origin_fields = {"kind", "namespace", "vm_name", "guest_hostname"}
    if not isinstance(origin, dict) or set(origin) != origin_fields:
        return False, "origin fields do not match the contract"
    if origin["kind"] != "virtual-machine":
        return False, "origin.kind must be virtual-machine"
    dns_label = re.compile(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$")
    if not dns_label.fullmatch(str(origin["namespace"])) or not dns_label.fullmatch(str(origin["vm_name"])):
        return False, "namespace and vm_name must be DNS labels"
    if not 1 <= len(str(origin["guest_hostname"])) <= 253:
        return False, "guest_hostname length is invalid"
    if not isinstance(payload["note"], str) or not 20 <= len(payload["note"]) <= 2000:
        return False, "note length must be between 20 and 2000 characters"
    categories = payload["allowed_categories"]
    if not isinstance(categories, list) or not 2 <= len(categories) <= 6:
        return False, "allowed_categories must contain two to six values"
    if len(categories) != len(set(categories)) or not set(categories).issubset(ALLOWED_CATEGORIES):
        return False, "allowed_categories contains an invalid or duplicate value"
    if payload["condition"] not in {"healthy", "model-unavailable"}:
        return False, "condition is invalid"
    return True, ""


def validate_model_result(result: Any, allowed_categories: list[str]) -> Tuple[bool, str]:
    if not isinstance(result, dict) or set(result) != {"category", "summary", "rationale"}:
        return False, "model output fields do not match the contract"
    if result["category"] not in allowed_categories:
        return False, "model category is outside the allowed set"
    if not isinstance(result["summary"], str) or not 1 <= len(result["summary"]) <= 400:
        return False, "model summary length is invalid"
    if not isinstance(result["rationale"], str) or not 1 <= len(result["rationale"]) <= 600:
        return False, "model rationale length is invalid"
    return True, ""


def read_secret(path: str) -> str:
    if not path:
        return ""
    try:
        return Path(path).read_text().strip()
    except OSError:
        return ""


def invoke_live_model(payload: Dict[str, Any]) -> Dict[str, Any]:
    api_base = os.getenv("MODEL_API_BASE", "").rstrip("/")
    model_id = os.getenv("MODEL_NAME", "")
    provider = os.getenv("MODEL_PROVIDER", "")
    hardware = os.getenv("MODEL_HARDWARE", "")
    if not api_base or not model_id or not provider or hardware != "Intel Xeon CPU":
        raise RuntimeError("live model identity is incomplete")

    prompt = (
        "Return only a JSON object with category, summary, and rationale. "
        f"Category must be one of: {', '.join(payload['allowed_categories'])}. "
        "Treat the result as advisory and do not propose or execute an action.\n\n"
        f"Operations note:\n{payload['note']}"
    )
    request_body = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "You classify synthetic operations notes for a human operator."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    headers = {"Content-Type": "application/json", "X-Request-ID": payload["request_id"]}
    api_key = read_secret(os.getenv("MODEL_API_KEY_FILE", ""))
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(
        f"{api_base}/v1/chat/completions",
        data=json.dumps(request_body).encode(),
        headers=headers,
        method="POST",
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=float(os.getenv("MODEL_TIMEOUT_SECONDS", "20")), context=context) as response:
        raw = json.load(response)
    content = raw["choices"][0]["message"]["content"]
    result = json.loads(content)
    valid, error = validate_model_result(result, payload["allowed_categories"])
    if not valid:
        raise ValueError(error)
    return {"result": result, "id": model_id, "provider": provider, "hardware": hardware}


def rehearsal_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = json.loads((FIXTURES / "healthy-response.json").read_text())
    result["request_id"] = payload["request_id"]
    result["source_state"] = source_state()
    result["evidence"] = [
        {"id": "vm-request-receipt", "producer": payload["origin"]["guest_hostname"], "observed_at": now()},
        {"id": "rehearsal-control-receipt", "producer": "ai-analysis-adapter", "observed_at": now()},
        {"id": "contract-validation-receipt", "producer": "ai-analysis-adapter", "observed_at": now()},
    ]
    return result


def unavailable_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "analysis-response/v1",
        "request_id": payload["request_id"],
        "source_state": source_state(),
        "condition": "model-unavailable",
        "ai_participated": False,
        "model": None,
        "result": None,
        "validation": {"schema_valid": True, "category_valid": False},
        "authority": {"model": "advisory-only", "final_decision_owner": "human operator", "actions_permitted": []},
        "evidence": [
            {"id": "vm-request-receipt", "producer": payload["origin"]["guest_hostname"], "observed_at": now()},
            {"id": "model-unavailable-receipt", "producer": "ai-analysis-adapter", "observed_at": now()},
        ],
    }


def analyze(payload: Dict[str, Any]) -> Dict[str, Any]:
    if payload["condition"] == "model-unavailable":
        response = unavailable_result(payload)
    elif mode() == "live":
        live = invoke_live_model(payload)
        response = {
            "schema_version": "analysis-response/v1",
            "request_id": payload["request_id"],
            "source_state": "LIVE",
            "condition": "healthy",
            "ai_participated": True,
            "model": {"id": live["id"], "provider": live["provider"], "hardware": live["hardware"]},
            "result": live["result"],
            "validation": {"schema_valid": True, "category_valid": True},
            "authority": {"model": "advisory-only", "final_decision_owner": "human operator", "actions_permitted": []},
            "evidence": [
                {"id": "vm-request-receipt", "producer": payload["origin"]["guest_hostname"], "observed_at": now()},
                {"id": "model-invocation-receipt", "producer": "ai-analysis-adapter", "observed_at": now()},
                {"id": "output-validation-receipt", "producer": "ai-analysis-adapter", "observed_at": now()},
            ],
        }
    else:
        response = rehearsal_result(payload)

    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    record = {
        "schema_version": "evidence-record/v1",
        "request_id": payload["request_id"],
        "request_sha256": hashlib.sha256(canonical).hexdigest(),
        "origin": payload["origin"],
        "service": {"dns": os.getenv("SERVICE_DNS", "ai-analysis"), "port": int(os.getenv("SERVICE_PORT", "8080"))},
        "adapter": {"name": "ai-analysis-adapter", "version": VERSION, "mode": mode()},
        "response": response,
    }
    with LOCK:
        EVIDENCE[payload["request_id"]] = record
    return response


class Handler(BaseHTTPRequestHandler):
    server_version = "virtualization-ai-adapter/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))

    def send_json(self, status: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self.send_json(200, {"status": "ok", "adapter": "ai-analysis-adapter", "version": VERSION, "mode": mode()})
            return
        prefix = "/api/v1/evidence/"
        if self.path.startswith(prefix):
            request_id = self.path[len(prefix):]
            with LOCK:
                record = EVIDENCE.get(request_id)
            if record is None:
                self.send_json(404, {"error": "evidence not found", "request_id": request_id})
            else:
                self.send_json(200, record)
            return
        self.send_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/api/v1/analyze":
            self.send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16_384:
                raise ValueError("request body size is invalid")
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json(400, {"error": str(exc)})
            return
        valid, error = validate_request(payload)
        if not valid:
            self.send_json(400, {"error": error, "request_id": payload.get("request_id")})
            return
        try:
            response = analyze(payload)
        except RuntimeError as exc:
            self.send_json(503, {"error": str(exc), "request_id": payload["request_id"], "ai_participated": False})
            return
        except (ValueError, KeyError, IndexError, urllib.error.URLError, TimeoutError) as exc:
            self.send_json(502, {"error": type(exc).__name__, "request_id": payload["request_id"], "ai_participated": False})
            return
        self.send_json(200, response)


def create_server(host: Optional[str] = None, port: Optional[int] = None) -> ThreadingHTTPServer:
    selected_host = host if host is not None else os.getenv("ADAPTER_HOST", "0.0.0.0")
    selected_port = port if port is not None else int(os.getenv("ADAPTER_PORT", "8080"))
    return ThreadingHTTPServer((selected_host, selected_port), Handler)


def main() -> None:
    server = create_server()
    print(f"ai-analysis-adapter {VERSION} listening on {server.server_address[0]}:{server.server_address[1]} mode={mode()}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
