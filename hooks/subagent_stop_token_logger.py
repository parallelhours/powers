#!/usr/bin/env python3
# Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0
"""SubagentStop hook — parse subagent transcript and log token usage to the active timer.

Fires after each Claude Code subagent finishes. The subagent has its own transcript
file (separate from the main session), so we parse it in full with no since_iso
filter. Tokens are logged with mode="subagent" to distinguish from the main session.

Payload fields used:
  - transcript_path: path to the subagent's JSONL transcript
  - session_id: shared with the main session — used to find the active timer
  - tool_calls: array of tool execution records → tool_call_count (preferred over transcript)
  - stop_reason: end_turn / max_tokens / tool_use
  - effort: current effort level
"""
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

transcript_path = payload.get("transcript_path", "")
session_id = payload.get("session_id", "")
stop_reason = payload.get("stop_reason", "") or ""
effort = str(payload.get("effort", "") or "")

tool_calls_payload = payload.get("tool_calls") or []
tool_call_count_payload = len(tool_calls_payload) if isinstance(tool_calls_payload, list) else None

headers = {"Authorization": f"Bearer {PAT}", "Content-Type": "application/json"}


def _find_timer(session_id: str) -> dict | None:
    try:
        params = {"session_id": session_id} if session_id else {}
        resp = httpx.get(f"{BASE_URL}/mcp/v1/timers/active/", headers=headers, params=params, timeout=5)
        if resp.status_code == 200:
            timers = resp.json().get("timers", [])
            if timers:
                return timers[-1]
        if session_id:
            resp2 = httpx.get(f"{BASE_URL}/mcp/v1/timers/active/", headers=headers, timeout=5)
            if resp2.status_code == 200:
                timers = resp2.json().get("timers", [])
                if timers:
                    return timers[-1]
    except Exception:
        pass
    return None


def _parse_subagent_transcript(path: str) -> dict:
    """Parse subagent JSONL transcript in full (subagent has isolated transcript)."""
    totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "tool_call_count": 0,
        "turn_count": 0,
        "model_id": "",
    }
    seen_ids: set[str] = set()

    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if msg.get("isSidechain") or msg.get("isApiErrorMessage"):
                    continue

                msg_id = msg.get("uuid") or msg.get("id") or msg.get("msg_id")
                if msg_id:
                    if msg_id in seen_ids:
                        continue
                    seen_ids.add(msg_id)

                usage = msg.get("usage") or (msg.get("message", {}) or {}).get("usage")
                if usage and isinstance(usage, dict):
                    totals["input_tokens"] += usage.get("input_tokens", 0) or 0
                    totals["output_tokens"] += usage.get("output_tokens", 0) or 0
                    totals["cache_read_tokens"] += usage.get("cache_read_input_tokens", 0) or 0
                    totals["cache_write_tokens"] += usage.get("cache_creation_input_tokens", 0) or 0
                    totals["turn_count"] += 1

                content = msg.get("content") or (msg.get("message", {}) or {}).get("content", [])
                if isinstance(content, list):
                    totals["tool_call_count"] += sum(
                        1 for block in content if isinstance(block, dict) and block.get("type") == "tool_use"
                    )

                model = msg.get("model") or (msg.get("message", {}) or {}).get("model", "")
                if model:
                    totals["model_id"] = model

    except Exception:
        pass

    return totals


try:
    timer = _find_timer(session_id)
    if not timer:
        sys.exit(0)

    timer_id = timer["timer_id"]

    stats = _parse_subagent_transcript(transcript_path) if transcript_path else {}

    if not stats or (
        stats["input_tokens"] == 0
        and stats["output_tokens"] == 0
        and stats["cache_read_tokens"] == 0
        and stats["cache_write_tokens"] == 0
    ):
        sys.exit(0)

    effective_tool_call_count = (
        tool_call_count_payload if tool_call_count_payload is not None else stats["tool_call_count"]
    )

    body: dict = {
        "ai_tool": "claude",
        "mode": "subagent",
        "prompt_count": 0,
        "input_tokens": stats["input_tokens"],
        "output_tokens": stats["output_tokens"],
        "notes": "auto-logged by SubagentStop hook",
    }
    if stats["cache_read_tokens"]:
        body["cache_read_tokens"] = stats["cache_read_tokens"]
    if stats["cache_write_tokens"]:
        body["cache_write_tokens"] = stats["cache_write_tokens"]
    if effective_tool_call_count:
        body["tool_call_count"] = effective_tool_call_count
    if stats["turn_count"] > 1:
        body["turn_count"] = stats["turn_count"]
    if stats["model_id"]:
        body["model_id"] = stats["model_id"]
    if stop_reason:
        body["stop_reason"] = stop_reason
    if effort:
        body["effort"] = effort

    httpx.post(f"{BASE_URL}/mcp/v1/timers/{timer_id}/ai-event/", headers=headers, json=body, timeout=5)

except Exception:
    pass

sys.exit(0)
