---
created: 2026-05-13
updated: 2026-05-13
labels: [reference, mcp, installer, cli]
description: CLI reference for mcps/installer.py and install.json schema.
tags: [reference, mcp, installer, cli, schema]
audience: [developers, operators, agents]
status: draft
version: 0.1.0
applies-to: [mcp-framework]
---

# MCP Installer Reference

## CLI Usage

```bash
python -m mcps.installer [options]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--mcp <id>` | — | MCP to install (repeatable, or `all`). If omitted, lists available MCPs. |
| `--agent <name>` | `claude` | Target agent: `claude`, `opencode`, or `codex` |
| `--location <loc>` | `project` | Install location: `project` (repo root) or `global` (agent config dir) |
| `--list` | — | List available MCPs and exit |
| `--non-interactive` | — | Skip prompts; use env vars or defaults for replacement values |
| `--mcps-dir <path>` | auto | Path to the `mcps/` directory (auto-detected by default) |

### Value precedence

Replacement values are resolved in this order:

1. Environment variable matching the placeholder name (e.g. `TKPI_PAT`)
2. Interactive prompt (skipped in `--non-interactive` mode)
3. Default value from `install.json`

### Examples

```bash
# List available MCPs
python -m mcps.installer --list

# Install parallelhours for Claude Code (project-local), prompted for values
python -m mcps.installer --mcp parallelhours --agent claude --location project

# Install all MCPs for OpenCode globally, using env vars
TKPI_PAT=abc123 TKPI_PROJECT=MYPROJ \
  python -m mcps.installer --mcp all --agent opencode --location global --non-interactive

# Install specific MCPs
python -m mcps.installer --mcp parallelhours --mcp code-review --agent claude
```

## install.json Schema

Each MCP directory must contain an `install.json` with the following structure:

```json
{
  "id": "string (required) — MCP identifier, must match directory name",
  "name": "string (required) — human-readable display name",
  "description": "string (required) — one-line description",
  "mcp_server_relative": "string (optional) — filename of the server script, relative to MCP dir. Omit for MCPs published to PyPI (resolved via `uvx`).",

  "replacements": [
    {
      "placeholder": "string (required) — env var name, e.g. TKPI_PAT",
      "prompt": "string (required) — prompt text for interactive mode",
      "secret": false,
      "default": ""
    }
  ],

  "default_env": {
    "KEY": "value — static env vars that don't need user input"
  },

  "agents": {
    "<agent-id>": {
      "config_file": "string — config filename (e.g. .mcp.json)",
      "entry": { }
    }
  },

  "global_paths": {
    "<agent-id>": "string — global config path (supports ~ expansion)"
  }
}
```

### Placeholder substitution

- `${PLACEHOLDER}` in config templates is replaced with the user-provided value for that placeholder
- Unmatched `${...}` tokens are left as-is

### Agent config template structure

**Claude Code** (`.mcp.json`):
```json
{
  "mcpServers": {
    "<mcp-id>": {
      "command": "uvx",
      "args": ["<package-name>"],
      "env": { }
    }
  }
}
```

**OpenCode** (`opencode.jsonc`):
```json
{
  "mcp": {
    "<mcp-id>": {
      "type": "local",
      "command": ["uvx", "<package-name>"],
      "enabled": true,
      "environment": { }
    }
  }
}
```

For MCPs that are not published to PyPI, use `uv run` with the local path:
```json
{
  "mcp": {
    "<mcp-id>": {
      "type": "local",
      "command": ["uv", "run", "python", "path/to/server.py"],
      "enabled": true,
      "environment": { }
    }
  }
}
```

## See also

- [MCP Framework explanation](../01-explanation/mcp-framework.md)
- [How to add a new MCP](../03-howto/add-new-mcp.md)
- [Parallel Hours MCP reference](mcp-parallelhours.md)
