---
created: 2026-05-13
updated: 2026-05-13
labels: [reference, mcp, parallelhours, time-tracking]
description: Reference for the Parallel Hours MCP server in the MCP framework.
tags: [reference, mcp, parallelhours, time-tracking, installer]
audience: [developers, operators, agents]
status: draft
version: 0.1.0
applies-to: [mcp-framework, parallelhours]
---

# Parallel Hours MCP

## Overview

The Parallel Hours MCP server (`mcps/parallelhours/`) provides time tracking and KPI management tools via the [parallelhours.io](https://parallelhours.io) API.

## Installation

```bash
# Interactive
python -m mcps.installer --mcp parallelhours --agent claude --location project

# Non-interactive (with env vars)
TKPI_PAT=your_token TKPI_PROJECT=MYPROJ \
  python -m mcps.installer --mcp parallelhours --agent claude --location project --non-interactive
```

## Replacement entries

| Placeholder | Prompt | Secret | Default |
|-------------|--------|--------|---------|
| `TKPI_PAT` | Personal Access Token for parallelhours.io | Yes | — |
| `TKPI_PROJECT` | Default project key (e.g. MYPROJ) | No | — |

## Default environment

| Variable | Value |
|----------|-------|
| `TKPI_BASE_URL` | `https://parallelhours.io` |

## MCP tools

| Tool | Description |
|------|-------------|
| `list_projects` | List all projects for the authenticated user |
| `get_active_timers` | List all running timers |
| `start_timer` | Start a timer on a task (supports delegation mode, agent identity, session grouping) |
| `stop_timer` | Stop a running timer |
| `increment_prompt_count` | Increment prompt count on a timer |
| `log_ai_event` | Log AI usage event (tokens, model, tool calls) |
| `list_tasks` | List tasks in a project (filterable by status) |
| `get_task_context` | Get task details with active timers |
| `get_task_kpis` | Get task KPI metrics (time, concurrency, estimates) |
| `create_task` | Create a new task (with estimates, external issue links) |
| `update_task` | Update an existing task |
| `get_project_billing` | Get billing period summary |
| `get_project_billing_tasks` | Get itemized task-level billing |
| `get_project_hours` | Get hour totals for a project period |
| `request_ai_estimate` | Queue an AI time estimate |
| `get_ai_estimate` | Poll AI estimate status |
| `set_ai_estimate` | Directly write an agent-computed estimate |
| `get_autonomous_kpis` | Get productivity summary for autonomous AI sessions |

## See also

- [MCP Framework explanation](../01-explanation/mcp-framework.md)
- [Installer reference](mcp-installer.md)
- [How to add a new MCP](../03-howto/add-new-mcp.md)
