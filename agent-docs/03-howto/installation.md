---
created: 2026-05-13
updated: 2026-05-13
labels: [howto, installation, setup]
description: How to install and initialize the docs kit for a new project.
tags: [installation, bootstrap, setup, new-project]
audience: [agents, developers]
status: draft
version: 0.1.0
---

# How-To: Install the Docs Kit

This guide walks through initializing the agent-docs documentation kit for a new project.

## Prerequisites

- Read access to the `parallel-powers/agent-docs-bootstrap/` directory
- Understanding of the project structure and conventions

## Installation Methods

### Method 1: Agent-Assisted (Recommended)

Run the [installer](../agent-docs-bootstrap/installer.md) as an AI agent. The installer will:

1. Guide you through project grounding and architecture discovery
2. Copy bootstrap template files into the new project's `agent-docs/` directory
3. Customize content for the specific project
4. Create project-specific metadata and persona files

### Method 2: Manual Copy

```bash
# Copy the bootstrap template into your project
cp -r agent-docs-bootstrap/ /path/to/your-project/agent-docs/

# Remove the installer script (not needed in the target project)
rm /path/to/your-project/agent-docs/installer.md
```

## Verify Installation

After installation, verify the structure:

```bash
ls -la agent-docs/
```

Expected output should show 14 numbered directories (00-13):

```
00-readme/  03-howto/    06-environment/  09-changelog/  12-metadata/
01-explanation/  04-reference/  07-runbooks/    10-glossary/   13-personas/
02-tutorial/  05-plans/    08-troubleshooting/  11-agents/
```

## Next Steps

- Read the [tutorials](../02-tutorial/getting-started.md) to get started
- Review the [file structure conventions](../12-metadata/file-structure.md) for documentation standards
