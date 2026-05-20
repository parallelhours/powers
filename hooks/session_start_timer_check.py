#!/usr/bin/env python3
# Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0
import json
import os
import sys

import httpx

PAT = os.environ.get("TKPI_PAT", "")
BASE_URL = os.environ.get("TKPI_BASE_URL", "https://parallelhours.io").rstrip("/")

if not PAT:
    sys.exit(0)

try:
    resp = httpx.get(
        f"{BASE_URL}/mcp/v1/timers/active/",
        headers={"Authorization": f"Bearer {PAT}", "Content-Type": "application/json"},
        timeout=5,
    )
    if resp.status_code == 200:
        timers = resp.json().get("timers", [])
        if not timers:
            print(json.dumps({
                "systemMessage": (
                    "parallelhours: No timer running. "
                    "Run /session-start before writing code so this session is tracked. "
                    "Claude will also prompt you if you skip it."
                )
            }))
except Exception:
    pass

sys.exit(0)
