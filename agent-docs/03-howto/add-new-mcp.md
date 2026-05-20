---
created: 2026-05-13
updated: 2026-05-13
labels: [howto, mcp, framework]
description: Step-by-step guide for adding a new MCP server to the MCP framework.
tags: [howto, mcp, framework, installer]
audience: [architects, developers, agents]
status: draft
version: 0.1.0
applies-to: [mcp-framework]
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# Add a New MCP to the Framework

This guide walks through adding a new MCP server to the `mcps/` directory so it becomes available via `python -m mcps.installer`.

> **Prerequisites**: Read the [MCP Framework explanation](../01-explanation/mcp-framework.md) first.

## Step 1: Create the MCP directory

```bash
mkdir mcps/<mcp-id>
```

Replace `<mcp-id>` with a short kebab-case identifier (e.g. `code-review`, `deploy-agent`).

## Step 2: Write the MCP server

If your MCP is published to PyPI, skip this step — the installer will configure agents to use `uvx <package>`. Otherwise, create `mcps/<mcp-id>/server.py` with your MCP implementation:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp>=1.0", "httpx>=0.27"]
# ///
```

Include PEP 723 inline script metadata so the server can run via `uv run python mcps/<mcp-id>/server.py` without a pre-installed environment.

## Step 3: Create `install.json`

This is the metadata file the installer reads. Full schema in the [Installer reference](../04-reference/mcp-installer.md#installjson-schema).

```json
{
  "id": "<mcp-id>",
  "name": "Human-Readable Name",
  "description": "One-line description of what this MCP does.",
  "mcp_server_relative": "server.py",
  "replacements": [
    {
      "placeholder": "MY_VAR",
      "prompt": "Description of what the user needs to provide",
      "secret": false,
      "default": ""
    }
  ],
  "default_env": {
    "MY_BASE_URL": "https://example.com"
  },
  "agents": {
    "claude": {
      "config_file": ".mcp.json",
      "entry": {
        "mcpServers": {
          "<mcp-id>": {
            "command": "uvx",
            "args": ["<pypi-package>"],
            "env": {
              "MY_VAR": "${MY_VAR}",
              "MY_BASE_URL": "${MY_BASE_URL}"
            }
          }
        }
      }
    },
    "opencode": {
      "config_file": "opencode.jsonc",
      "entry": {
        "mcp": {
          "<mcp-id>": {
            "type": "local",
            "command": ["uv", "run", "--with", "mcp", "--with", "httpx", "python", "{MCP_SERVER_PATH}"],
            "enabled": true,
            "environment": {
              "MY_VAR": "${MY_VAR}",
              "MY_BASE_URL": "${MY_BASE_URL}"
            }
          }
        }
      }
    }
  },
  "global_paths": {
    "claude": "~/.claude/.mcp.json",
    "opencode": "~/.config/opencode/opencode.jsonc"
  }
}
```

Key fields:

| Field | Purpose |
|-------|---------|
| `replacements` | Env vars the user needs to supply install-time; supports `secret` for masking |
| `default_env` | Static env vars that don't need user input (e.g. default URLs) |
| `agents` | Per-agent config templates; `${PLACEHOLDER}` values are substituted at install time |
| `mcp_server_relative` | Path to `server.py` relative to MCP dir; only needed for local-only MCPs |
| `global_paths` | Where to write the config file for global installations |

## Step 4: Verify the MCP is discovered

```bash
python -m mcps.installer --list
```

Your MCP should appear in the list.

## Step 5: Test installation

```bash
# Non-interactive test (uses env vars or defaults)
MY_VAR=test123 python -m mcps.installer \
  --mcp <mcp-id> \
  --agent claude \
  --location project \
  --non-interactive
```

Check the generated config file (`.mcp.json` in the project root) for correct values and structure.

## Conventions

- MCP server files should be self-contained Python scripts with inline script metadata (omit if published to PyPI)
- Use `TKPI_*` prefix for parallelhours-related env vars; use your own prefix for new MCPs
- Include `__init__.py` and `__main__.py` only if the server lives locally (PyPI-published MCPs don't need them)
- Pin critical dependencies but prefer broad version ranges (`>=1.0`)
- Keep MCP tools focused on a single domain

## See also

- [MCP Framework explanation](../01-explanation/mcp-framework.md)
- [Installer reference](../04-reference/mcp-installer.md)
- [Parallel Hours MCP reference](../04-reference/mcp-parallelhours.md)
