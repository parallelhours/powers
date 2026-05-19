---
created: 2026-05-08
updated: 2026-05-08
labels: [glossary]
description: Terminology and definitions for the parallel-powers framework.
tags: [glossary, terminology, definitions]
audience: [agents, humans]
status: draft
version: 0.1.0
---

# Glossary

Key terms used in the parallel-powers framework.

## Terms

### Diátaxis
A documentation framework that divides documentation into four categories: tutorials, how-to guides, explanation, and reference. Pronounced "dee-ah-TAX-iss."

### Gantt Chart
A bar chart that illustrates a project schedule, showing tasks against time. Named after Henry Gantt (early 1900s). Common in Western project management; some teams use equivalent terms like "timeline view" or "schedule bar chart."

### Sprint
A time-boxed development cycle, typically 1-2 weeks, following Scrum/agile methodology. Also called an iteration or cycle in some frameworks.

### Bootstrap Kit
The `agent-docs-bootstrap/` directory — a template/installer for initializing the docs kit in new projects.

### Agent Documentation
The `agent-docs/` directory — live documentation following the Diátaxis framework, structured for both human and AI agent consumption.

### Persona
A fictional user archetype used to guide documentation and design decisions. Each persona has specific goals, pain points, and needs.

### Architecture Decision Record (ADR)
A document that captures an important architectural decision, including context, options considered, and rationale.

### parallelhours.io
An optional time-tracking service that integrates with MCP to track agent session time, AI usage, and project metrics.

### MCP (Model Context Protocol)
A protocol for providing tools and context to AI models. Used here for time tracking integration.

### MCP Framework
The `mcps/` directory and `installer.py` — a system for optionally installing MCP servers for various AI agents (Claude Code, OpenCode, Codex). Each MCP has its own directory with an `install.json` metadata file and optionally a local `server.py` implementation (MCPs published to PyPI may omit the local server, relying on `uvx` instead).

### MCP Installer
`mcps/installer.py` — a CLI tool that discovers MCPs, collects replacement values (tokens, project keys), and generates agent-specific config files (`.mcp.json`, `opencode.jsonc`).
