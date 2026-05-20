---
created: 2026-05-08
updated: 2026-05-08
labels: [architecture, runtime, sequences]
description: Runtime behavior including critical sequence flows and processes.
tags: [architecture, runtime, sequences, flows]
audience: [architects, developers, agents]
status: draft
version: 0.1.0
applies-to: [system]
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# Runtime Architecture

parallel-powers is primarily a documentation and conventions framework, not a running system. Its "runtime" is the workflow patterns agents and humans follow.

## Critical Sequence: Project Initialization

When a new project is initialized with the bootstrap kit:

```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant Bootstrap as agent-docs-bootstrap/
    participant Docs as agent-docs/
    participant Root as Root Files

    Agent->>Bootstrap: Read installer.md
    Agent->>Bootstrap: Read 00-readme/, 12-metadata/
    Agent->>Docs: Create agent-docs/ structure
    Agent->>Root: Create/update CLAUDE.md + AGENTS.md
    Agent->>Docs: Create project.yml, personas
    Agent->>Docs: Populate architecture views
    Agent->>Docs: Create remaining docs (glossary, ADRs, tutorials)
    Agent->>Docs: Validate frontmatter, diagrams, links
```

## Critical Sequence: Agent Onboarding

When an agent starts a new session:

```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant Root as Root
    participant Docs as agent-docs/
    participant Metadata as 12-metadata/

    Agent->>Root: Load CLAUDE.md (automatic)
    Agent->>Root: Read project context + conventions
    Agent->>Docs: Read 00-readme/index.md
    Agent->>Metadata: Read project.yml
    Agent->>Metadata: Read file-structure.md
    Note over Agent: Agent now has sufficient<br/>context to work productively
```

## Critical Sequence: Issue-Driven Workflow

A typical day-in-the-life:

```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant GitHub as GitHub Issues
    participant Tkpi as parallelhours.io
    participant Branch as Git Branch

    Agent->>GitHub: Review assigned issue
    Agent->>Tkpi: /vault-start [issue#]
    Tkpi-->>Agent: Timer started
    Agent->>Docs: Read relevant docs
    Agent->>Branch: Create feature branch
    Agent->>Agent: Implement changes
    Agent->>Branch: Commit + push
    Agent->>GitHub: Create PR
    Agent->>Tkpi: /vault-end
    Tkpi-->>Agent: Timer stopped, AI usage logged
```

## Error Handling

Since this is a documentation framework, "errors" are primarily:

- **Missing frontmatter**: Documents won't be indexable by agents
- **Broken links**: Navigational failures within agent-docs/
- **Stale docs**: Outdated metadata (status, version, dates)
- **Inconsistent personas**: Personas that don't reference actual docs

Agents should validate these as part of any documentation workflow.
