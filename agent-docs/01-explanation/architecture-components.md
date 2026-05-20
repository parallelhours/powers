---
created: 2026-05-08
updated: 2026-05-08
labels: [architecture, components]
description: Component-level architecture including directories, services, and packages.
tags: [architecture, components, directories]
audience: [architects, developers, agents]
status: draft
version: 0.1.0
applies-to: [system]
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# Component Architecture

parallel-powers is a file-and-convention-based framework. The "components" are directories, configuration files, and external service integrations.

## Directory Structure

```
parallel-powers/
├── agent-docs/                  # Live documentation (this project)
│   ├── 00-readme/               # Entry point
│   ├── 01-explanation/          # Architecture, decisions
│   │   └── decisions/           # Architecture Decision Records
│   ├── 02-tutorial/             # Learning paths
│   ├── 03-howto/                # Task-oriented guides
│   ├── 04-reference/            # Technical reference
│   ├── 05-plans/                # Roadmaps, sprint backlogs
│   ├── 06-environment/          # Dev environment setup
│   ├── 07-runbooks/             # Operational procedures
│   ├── 08-troubleshooting/      # Common errors, FAQs
│   ├── 09-changelog/            # Version history
│   ├── 10-glossary/             # Terminology
│   ├── 11-agents/               # Agent-specific guides
│   ├── 12-metadata/             # Project metadata, conventions
│   └── 13-personas/             # User personas
├── agent-docs-bootstrap/        # Template/installer (DO NOT REMOVE)
├── mcps/                        # MCP Framework — optionally installable MCP servers
│   ├── installer.py             # Unified CLI installer
│   ├── parallelhours/           # Parallel Hours MCP (time tracking)
│   └── tests/                   # Installer unit tests
├── CLAUDE.md                    # Claude Code instructions
├── AGENTS.md                    # Cross-agent interoperability
└── .claude/                     # Claude-specific config
    └── settings.local.json      # Local permission settings
```

## External Dependencies

| Service | Purpose | Required? |
|---------|---------|-----------|
| GitHub | Repository hosting, issue tracking | Yes |
| parallelhours.io | Time tracking, session management | Optional |
| Claude Code | AI agent interface | Recommended |

## Configuration

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Agent instructions (loaded automatically by Claude Code) |
| `AGENTS.md` | Cross-agent instructions (points to CLAUDE.md) |
| `.claude/settings.local.json` | Claude Code permissions |
| `mcps/installer.py` | MCP Framework installer |
| `mcps/*/install.json` | MCP definition metadata (replacements, templates, paths) |
| `.mcp.json` | MCP server configuration (installed via MCP Framework) |
| `agent-docs/12-metadata/project.yml` | Structured project metadata |
