#!/usr/bin/env python3
"""Installed into the operations VM by cloud-init."""

import json
import os
import socket
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path


condition = sys.argv[1] if len(sys.argv) > 1 else "healthy"
request_id = sys.argv[2] if len(sys.argv) > 2 else str(uuid.uuid4())
payload = {
    "schema_version": "analysis-request/v1",
    "request_id": request_id,
    "origin": {
        "kind": "virtual-machine",
        "namespace": os.getenv("LAB_NAMESPACE", "virtualization-ai-101"),
        "vm_name": os.getenv("VM_NAME", "operations-vm"),
        "guest_hostname": socket.gethostname(),
    },
    "note": Path("/opt/virtualization-ai/operations-note.txt").read_text().strip(),
    "allowed_categories": ["inspect", "schedule-maintenance", "escalate"],
    "condition": condition,
}
receipt = {
    "schema_version": "vm-request-receipt/v1",
    "request_id": request_id,
    "guest_hostname": socket.gethostname(),
    "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
}
print(f"VM_REQUEST_RECEIPT {json.dumps(receipt, separators=(',', ':'))}", file=sys.stderr)
request = urllib.request.Request(
    "http://ai-analysis:8080/api/v1/analyze",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "X-Request-ID": request_id},
    method="POST",
)
try:
    with urllib.request.urlopen(request, timeout=30) as response:
        print(json.dumps(json.load(response), indent=2))
except urllib.error.HTTPError as exc:
    print(exc.read().decode(), file=sys.stderr)
    raise SystemExit(1)
