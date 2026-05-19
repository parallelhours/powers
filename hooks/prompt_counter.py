#!/usr/bin/env python3
import json
import os
import sys

import httpx

PAT = os.environ.get("TKPI_PAT", "")
BASE_URL = os.environ.get("TKPI_BASE_URL", "https://parallelhours.io").rstrip("/")

if not PAT:
    sys.exit(0)

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

session_id = payload.get("session_id", "")
headers = {"Authorization": f"Bearer {PAT}", "Content-Type": "application/json"}

try:
    params = {"session_id": session_id} if session_id else {}
    resp = httpx.get(f"{BASE_URL}/mcp/v1/timers/active/", headers=headers, params=params, timeout=5)
    if resp.status_code != 200:
        sys.exit(0)
    timers = resp.json().get("timers", [])

    if not timers and session_id:
        resp2 = httpx.get(f"{BASE_URL}/mcp/v1/timers/active/", headers=headers, timeout=5)
        if resp2.status_code == 200:
            timers = resp2.json().get("timers", [])

    if not timers:
        sys.exit(0)

    timer_id = timers[-1]["timer_id"]
    httpx.post(f"{BASE_URL}/mcp/v1/timers/{timer_id}/prompt/", headers=headers, timeout=5)
except Exception:
    pass

sys.exit(0)
