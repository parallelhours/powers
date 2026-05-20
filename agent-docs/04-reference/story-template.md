---
created: 2026-05-12
updated: 2026-05-12
labels: [reference, template, story, agile]
description: Story template with human and AI-assisted estimates — tool-agnostic, for sprint planning and task tracking.
tags: [story, template, agile, estimates, sprint, planning]
audience: [developers, project-managers, agents]
status: draft
version: 0.1.0
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# Story Template

A story (also called issue, task, or ticket) is the atomic unit of work in
the human-in-the-loop cadence. This template defines the standard format.

It is **tool-agnostic** — the structure works in any tracker (GitHub Issues,
Jira, Linear, Trello, a Markdown file, or a spreadsheet). The field mappings
section shows how to adapt it.

---

```markdown
## Story: [Short title — what needs to be done]

**Type**: feature | bug | design | documentation | spike | chore | refactor | test | security
**Priority**: high | medium | low
**Story Points**: 1 | 2 | 3 | 5 | 8 | 13

---

### Description

*What needs to be done and why. One to three paragraphs. Link to the PRD or
parent epic if applicable.*

---

### Acceptance Criteria

*Specific, testable conditions that must be met.*

- [ ] [Condition 1]
- [ ] [Condition 2]
- [ ] [Condition 3]

---

### Technical Notes

*Implementation hints, architecture decisions, files to modify, patterns to
follow.*

---

### Estimates

| Estimate Type | Time | Notes |
|---------------|------|-------|
| Human (unassisted) | [e.g. 4 hours] | Time without AI assistance |
| AI-assisted | [e.g. 1 hour] | Time with AI agent working alongside |

*Estimates are bounds, not guarantees. Update actuals after completion.*

---

### Definition of Done

- [ ] Code written and follows project conventions
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Documentation updated (if applicable)
- [ ] PR created and reviewed
- [ ] Branch merged to `main`
- [ ] Human estimate and AI-assisted actuals recorded

---

### Dependencies

*List any blockers or prerequisites:*

- Blocked by: #[issue or story ID]
- Blocks: #[issue or story ID]

---

### Labels

`[type]` `priority-[level]` `story-points-[n]` `human-estimate-hours-[n]` `ai-estimate-hours-[n]`
```

## Usage Notes

### During PM Sprint Breakdown (Phase 3)

The Developer and Project Manager personas decompose requirements into
stories. Each story gets:
- A clear description and acceptance criteria
- Both a human estimate and an AI-assisted estimate
- Story points for relative sizing

The dual estimate is the key innovation: it lets you compare how long a task
would take a human working alone vs. a human working with an AI agent. This
informs sprint planning — tasks where the AI-assisted estimate is much lower
than the human estimate are candidates for early sprint slots.

### During Sprint Planning (Phase 4)

Stories are assigned to sprints. The agent:
1. Creates the story in your project tracker (or as a Markdown file)
2. Applies the appropriate [labels](issue-labels.md) for type, priority,
   story points, and estimates
3. Moves it into the sprint backlog

### After Completion

Record the actual human and AI-assisted time so estimates improve over time.
See the [issue labels reference](issue-labels.md) for the label schema and
[time tracking](../11-agents/time-tracking.md) for recording actuals.

### Story Size Guidelines

| Story Points | Human Estimate | AI-Assisted Estimate | Best For |
|--------------|---------------|---------------------|----------|
| 1 | ≤ 1 hour | ≤ 15 min | Typos, simple config changes |
| 2 | 1-2 hours | 15-30 min | Small features, straightforward fixes |
| 3 | 2-4 hours | 30 min - 1 hr | Moderate features with some unknowns |
| 5 | 4-8 hours | 1-2 hours | Complex features, new endpoints |
| 8 | 1-2 days | 2-4 hours | Large features, multiple files |
| 13 | 2+ days | 4+ hours | Very large — split before starting |

### Tool Mapping

| This Template | GitHub Issues | Jira | Linear | Markdown File |
|--------------|---------------|------|--------|---------------|
| Type | Labels (`type:`) | Issue Type | Label | Metadata field |
| Priority | Labels (`priority-*`) | Priority field | Priority | Metadata field |
| Story Points | Labels (`story-points-*`) | Story Points field | Estimate | Metadata field |
| Human Estimate | Labels (`human-estimate-hours-*`) | Custom field | Label | Metadata field |
| AI-Assisted Estimate | Labels (`ai-estimate-hours-*`) | Custom field | Label | Metadata field |
| Acceptance Criteria | Issue body checklist | Description | Description | Markdown checklist |
| Technical Notes | Issue body | Description | Description | Markdown section |

## See Also

- [PRD Template](prd-template.md) — Upstream: stories are derived from PRD requirements
- [Issue Labels](issue-labels.md) — Label schema for estimates and metadata
- [Time Tracking](../11-agents/time-tracking.md) — Recording actual time against estimates
- [Human in the Loop Tutorial](../02-tutorial/human-in-the-loop.md) — How stories fit in the cadence
