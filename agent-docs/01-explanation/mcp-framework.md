---
created: 2026-05-13
updated: 2026-05-13
labels: [explanation, mcp, architecture]
description: The MCP framework — optionally installable MCP servers for AI agents.
tags: [mcp, framework, architecture, agents]
audience: [architects, developers, operators, agents]
status: draft
version: 0.1.0
concepts: [mcp, installer, mcp-definition]
prerequisites: [architecture-subsystems]
---

# MCP Framework

The MCP (Model Context Protocol) framework is a directory of optionally installable MCP servers under `mcps/`, managed by a Python installer. It lets you add agent-accessible tools (time tracking, code review, deployment, etc.) on a per-project or per-agent basis.

## Motivation

Different AI agents (Claude Code, OpenCode, Codex) use different config file formats and placement conventions. Each MCP server has required environment variables (tokens, project keys, URLs) that must be supplied before installation. The MCP framework abstracts over both:

- **Agent-specific config formats** — each MCP definition includes templates for every supported agent
- **Replacement text** — each MCP declares which env vars are user-supplied (e.g. `TKPI_PAT`, `TKPI_PROJECT`)
- **Installation location** — config files can be project-local (recommended) or global (`~/.claude/.mcp.json`, etc.)

## Architecture

```
mcps/
├── installer.py                   # Unified CLI installer
├── parallelhours/                 # MCP server (published to PyPI, pulled via uvx)
│   └── install.json               # Metadata: replacements, templates, paths
└── ...                            # Future MCPs follow the same pattern
```

Each MCP lives in its own directory under `mcps/`. The installer discovers MCPs by scanning for `install.json` files.

### How it works

1. **Discovery** — `installer.py` scans `mcps/*/install.json` to build a registry of available MCPs
2. **Selection** — user picks which MCPs to install via `--mcp` (or `--mcp all`)
3. **Value collection** — for each MCP, the installer collects replacement values from env vars, CLI flags, or interactive prompts
4. **Config generation** — placeholders like `${TKPI_PAT}` are substituted into the agent-specific config template
5. **Config merging** — the generated config block is merged into the existing config file (`.mcp.json`, `opencode.jsonc`, etc.)
6. **Write** — config file is created or updated at the installation location

### Replacement text entries

Each MCP defines a set of "replacement" entries — environment variables that the user must supply:

| Field | Purpose |
|-------|---------|
| `placeholder` | Env var name (e.g. `TKPI_PAT`) |
| `prompt` | Human-readable prompt for interactive mode |
| `secret` | Whether to mask input (for tokens, passwords) |
| `default` | Fallback value if not provided |

### Agent config formats

| Agent | Config file | Entry point |
|-------|-------------|-------------|
| Claude Code | `.mcp.json` (`mcpServers` key) | `uvx <package>` |
| OpenCode | `opencode.jsonc` (`mcp` key) | `uvx <package>` or local script |
| Codex | *not yet implemented* | — |

### Installation locations

- **project** (recommended) — config file written to the project root, making MCPs portable with the repo
- **global** — config file written to the agent's global config directory (e.g. `~/.claude/.mcp.json`)

## Design decisions

1. **install.json over hardcoded registry** — each MCP self-describes; adding a new MCP means adding a directory, not modifying the installer
2. **Template-based config generation** — agent config formats evolve independently; templates isolate the installer from format changes
3. **Merge over overwrite** — multiple MCPs can coexist in the same config file; the installer merges new entries into the existing structure
4. **Env var fallback chain** — CLI flag > environment variable > interactive prompt > default

## See also

- [How to add a new MCP](../03-howto/add-new-mcp.md) — step-by-step
- [Installer reference](../04-reference/mcp-installer.md) — CLI flags and install.json schema
- [Parallel Hours MCP reference](../04-reference/mcp-parallelhours.md) — the parallelhours server
- [Architecture subsystems](architecture-subsystems.md) — where MCP Framework fits in
