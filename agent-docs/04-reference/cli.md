---
created: 2026-05-13
updated: 2026-05-13
labels: [reference, cli]
description: CLI reference for the parallel-powers framework tools.
tags: [cli, commands, reference]
audience: [developers, operators, agents]
status: draft
version: 0.1.0
applies-to: [mcp-framework]
---

# CLI Reference

Complete reference for command-line interfaces in the parallel-powers framework.

## MCP Installer

The MCP framework includes `installer.py` for managing optionally installable MCP servers.

**Usage**:
```bash
python mcps/installer.py [command] [options]
```

**Commands**:

| Command | Description |
|---------|-------------|
| `install <server>` | Install an MCP server from the framework |
| `uninstall <server>` | Remove an MCP server |
| `list` | List available and installed servers |
| `status` | Show installation status of all servers |

See [mcp-installer.md](mcp-installer.md) for full reference.
