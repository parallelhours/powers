---
created: 2026-05-08
updated: 2026-05-08
labels: [readme, overview]
description: Entry point and repository overview for the parallel-powers project.
tags: [readme, overview, entry-point]
audience: [agents, humans]
status: published
version: 0.1.0
---

# parallel-powers

Human-in-the-loop framework for agentic-assisted product definition through product delivery.

This repository defines the documentation structure, agent conventions, issue tracking metadata, and workflows that enable **controlled, agentic-assisted product development** — from initial product definition all the way through delivery.

## Structure

| Directory | Purpose |
|-----------|---------|
| [00-readme/](00-readme/) | Entry point and repository overview |
| [01-explanation/](01-explanation/) | Understanding-oriented docs (architecture, design rationale) |
| [02-tutorial/](02-tutorial/) | Learning-oriented step-by-step guides |
| [03-howto/](03-howto/) | Task-oriented guides for specific goals |
| [04-reference/](04-reference/) | Technical reference (APIs, configs, CLI) |
| [05-plans/](05-plans/) | Project plans and roadmaps |
| [06-environment/](06-environment/) | Development environment setup |
| [07-runbooks/](07-runbooks/) | Operational procedures and checklists |
| [08-troubleshooting/](08-troubleshooting/) | Common errors, FAQs, debugging |
| [09-changelog/](09-changelog/) | Version history and release notes |
| [10-glossary/](10-glossary/) | Terminology and definitions |
| [11-agents/](11-agents/) | AI agent context and conventions |
| [12-metadata/](12-metadata/) | Machine-readable project metadata |
| [13-personas/](13-personas/) | User personas and use cases |

## Inclusive & Accessible Documentation

We strive for documentation that respects diverse backgrounds and works for a broad audience. This includes using gender-neutral language, culturally diverse examples, and accessible formatting. If you find language or design choices that exclude or stereotype, please open an issue or PR.

> **Note:** This framework integrates with optional paid services (Claude Code, parallelhours.io). Core documentation conventions work independently of any paid tool. See the [environment setup](../06-environment/setup.md) for free alternatives where available.

## Key Directories

- **`agent-docs/`** — Live documentation for this project following the Diátaxis framework
- **`agent-docs-bootstrap/`** — Template/installer for initializing the docs kit in new projects
- **`mcps/`** — MCP Framework: optionally installable MCP servers managed by `installer.py`
