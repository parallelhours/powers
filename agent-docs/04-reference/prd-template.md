---
created: 2026-05-12
updated: 2026-05-12
labels: [reference, template, prd, requirements]
description: Product Requirements Document template — context, requirements, acceptance criteria, and prioritization.
tags: [prd, requirements, template, product-marketing]
audience: [product-managers, developers, agents]
status: draft
version: 0.1.0
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# PRD Template

This document defines the standard template for Product Requirements
Documents (PRDs) produced during the requirements phase. It is tool-agnostic
— use it as-is in a doc, adapt it for a wiki, or map its fields to your
project management tool of choice.

---

```markdown
# PRD: [Feature/Project Name]

**Status**: Draft | Review | Approved
**Owner**: [Persona or person]
**Date**: YYYY-MM-DD
**Version**: 0.1.0

---

## 1. Problem Statement

What problem are we solving? For whom? Why now?

*One to three paragraphs describing the context, the user need, and the
motivation for doing this work now. Avoid prescribing solutions — focus on
the problem.*

---

## 2. Target Audience

Who will use this? Reference relevant personas.

- **[Persona Name]** — how they interact with this feature
- **[Persona Name]** — how they interact with this feature

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | [What the system must do] | P0 / P1 / P2 | [Context or constraints] |
| FR-2 | [What the system must do] | P0 / P1 / P2 | [Context or constraints] |

Priority levels:
- **P0** — Blocking; must have for launch
- **P1** — Important; should have
- **P2** — Nice-to-have; deferrable

### 3.2 Non-Functional Requirements

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-1 | [Performance, security, reliability, etc.] | [Measurable target] | [Context] |
| NFR-2 | [Performance, security, reliability, etc.] | [Measurable target] | [Context] |

---

## 4. Acceptance Criteria

*Conditions that must be met for this PRD to be considered complete.*

- [ ] [Criterion 1 — specific, testable]
- [ ] [Criterion 2 — specific, testable]
- [ ] [Criterion 3 — specific, testable]

---

## 5. Out of Scope

Explicitly call out what this PRD does **not** cover.

- [Out-of-scope item 1]
- [Out-of-scope item 2]

---

## 6. Success Metrics

How will we measure success after delivery?

| Metric | Current Baseline | Target | How Measured |
|--------|-----------------|--------|--------------|
| [Metric] | [Value] | [Value] | [Tool or method] |

---

## 7. Prioritization Rationale

Why were these requirements prioritized this way? Reference customer
feedback, strategic goals, or technical constraints.

---

## 8. Risks and Open Questions

| Risk / Question | Impact | Mitigation |
|-----------------|--------|------------|
| [Risk] | [What happens if it materializes] | [How to avoid or address] |
| [Question] | [What's blocked until answered] | [How to resolve] |

---

## 9. Appendix

- Links to research, competitive analysis, user interviews
- Related PRDs or design documents
- Glossary terms
```

## Usage Notes

### For the Product Marketing persona

The agent (acting as the Product Marketing persona) will populate this template
based on your input. You provide the problem and context; the agent structures
it into the PRD format, asks clarifying questions, and produces a draft for
review.

### For humans

Use the template as a starting point for any feature or project. Not every
section is required for every PRD:
- Small features can skip sections 5, 6, and 8
- Bug-fix PRDs only need sections 1, 3, and 4
- Full projects should fill every section

### Tool mapping

This template can be:
- Used as a standalone document in `05-plans/`
- Pasted into a wiki or Google Doc
- Converted to a GitHub issue using the [story template](story-template.md)
- Mapped to Jira fields (summary, description, acceptance criteria)

## See Also

- [Story Template](story-template.md) — Break PRD requirements into individual stories
- [Product Marketing Persona](../13-personas/product-marketing.md) — Who owns this phase
- [Issue Labels](issue-labels.md) — Metadata labels linked to stories
