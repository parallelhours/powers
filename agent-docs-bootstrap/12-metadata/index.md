---
created: 2026-04-03
updated: 2026-04-03
labels: [metadata, conventions]
description: Machine-readable metadata and conventions for documentation files.
tags: [metadata, conventions, frontmatter, yaml]
audience: [agents, humans]
status: active
version: 1.0.0
---

# Machine-Readable Metadata

This directory contains machine-readable metadata for tooling, IDEs, and AI agents.

## Files

| File | Purpose |
|------|---------|
| `file-structure.md` | YAML frontmatter schema and file conventions |
| `diagrams.md` | Guidelines for ASCII and Mermaid diagrams |
| `project.yml` | Project-specific metadata (created by installer) |

## Quick Start

For AI agents initializing this docs kit for a new project:

1. Read `../installer.md` — follows the bootstrap process
2. Read `file-structure.md` — understand frontmatter schema
3. Read `diagrams.md` — understand diagram conventions

## Standards

- [Package Metadata](https://package.npmjs.com/) for npm
- [.editorconfig](https://editorconfig.org/) for editor settings
- [JSON Schema](https://json-schema.org/) for config validation
