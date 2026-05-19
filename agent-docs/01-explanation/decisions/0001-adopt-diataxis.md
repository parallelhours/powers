---
created: 2026-05-08
updated: 2026-05-08
labels: [decision, architecture, diataxis]
description: ADR-0001: Adopt the Diátaxis documentation framework for all project documentation.
tags: [adr, decision, diataxis, documentation]
audience: [architects, developers, agents]
status: draft
version: 0.1.0
concepts: [diataxis, documentation-framework]
---

# ADR-0001: Adopt the Diátaxis Documentation Framework

**Status**: Accepted

## Context

The parallel-powers framework needs a consistent, scalable approach to documentation that serves both human readers and AI agents. The documentation must cover multiple use cases: tutorials for beginners, how-to guides for common tasks, technical reference, and deep explanation of architecture and rationale.

Without a structured framework, documentation tends to become inconsistent, duplicative, and hard to navigate — especially as the project grows.

## Decision

Adopt the [Diátaxis documentation framework](https://diataxis.fr/) as the organizing principle for all project documentation.

The framework divides documentation into four quadrants:

| Quadrant | Orientation | Purpose |
|----------|-------------|---------|
| Tutorials | Learning-oriented | Step-by-step guides for beginners |
| How-to Guides | Task-oriented | Practical guides for specific goals |
| Explanation | Understanding-oriented | Background, architecture, rationale |
| Reference | Information-oriented | Technical descriptions, APIs, configs |

The `agent-docs/` directory extends these four quadrants with additional directories for project-specific needs (plans, environment, runbooks, troubleshooting, changelog, glossary, agent guides, metadata, personas).

## Consequences

**Positive**:
- Clear, predictable structure for all documentation
- AI agents can quickly locate the right type of documentation
- Humans can navigate by quadrant based on their need (learning, doing, understanding, looking up)
- The framework is well-established and documented at diataxis.fr

**Negative**:
- Requires discipline to maintain the quadrant boundaries
- Some documents may straddle multiple quadrants, requiring judgment calls
- The extended directory structure (beyond the four quadrants) adds complexity not present in pure Diátaxis

## See Also

- [Diátaxis Guide](https://diataxis.fr/)
- [File structure conventions](../../12-metadata/file-structure.md)
- [00-readme index](../../00-readme/index.md)
