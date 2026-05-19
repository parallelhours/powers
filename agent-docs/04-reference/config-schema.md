---
created: 2026-05-13
updated: 2026-05-13
labels: [reference, configuration]
description: Configuration schema reference for MCP server install.json files and project configuration.
tags: [configuration, schema, json, reference]
audience: [developers, agents]
status: draft
version: 0.1.0
applies-to: [mcp-framework]
---

# Configuration Schema

Complete reference for configuration options in the parallel-powers framework.

## MCP Install Schema

Each optionally installable MCP server in `mcps/` has an `install.json` that defines its metadata and requirements.

### Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Display name of the MCP server"
    },
    "id": {
      "type": "string",
      "description": "Unique identifier (kebab-case)"
    },
    "description": {
      "type": "string",
      "description": "Short description of what the server does"
    },
    "command": {
      "type": "string",
      "description": "Command to run the server (e.g., uv, python, node)"
    },
    "args": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Arguments for the command"
    },
    "env": {
      "type": "object",
      "description": "Environment variables required by the server"
    }
  },
  "required": ["name", "id", "description", "command", "args"]
}
```

## Project Configuration

Project-level configuration is stored in `agent-docs/12-metadata/project.yml`.
