#!/usr/bin/env python3
# Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0
import json
import os
import sys
from pathlib import Path

import httpx

PAT = os.environ.get("TKPI_PAT", "")
BASE_URL = os.environ.get("TKPI_BASE_URL", "https://parallelhours.io").rstrip("/")


def _mcp_configured() -> bool:
    """Return True if a parallelhours MCP server entry exists in any known config file."""
    candidates = [
        Path.cwd() / ".mcp.json",
        Path.home() / ".claude" / ".mcp.json",
    ]
    for path in candidates:
        if path.exists():
            try:
                data = json.loads(path.read_text())
                servers = data.get("mcpServers", {})
                if "parallelhours" in servers:
                    return True
            except Exception:
                pass
    return False


if not PAT:
    if not _mcp_configured():
        print(json.dumps({
            "systemMessage": (
                "parallelhours MCP not configured. "
                "Run the installer once to set up time tracking tools: "
                "python -m mcps.installer --mcp parallelhours --agent claude --location project "
                "(from your parallel-powers directory, or see README for global install). "
                "Then restart Claude Code."
            )
        }))
    sys.exit(0)

if not _mcp_configured():
    print(json.dumps({
        "systemMessage": (
            "parallelhours: TKPI_PAT is set but no MCP server is configured — "
            "time tracking tools are unavailable. "
            "Run: python -m mcps.installer --mcp parallelhours --agent claude --location project "
            "then restart Claude Code."
        )
    }))
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
