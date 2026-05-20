---
created: 2026-05-08
updated: 2026-05-08
labels: [reference, issues, agile, labels]
description: Issue label schema for agile metadata — types, priority, story points, and hour estimates.
tags: [issues, labels, agile, github, story-points, estimates]
audience: [developers, agents, project-managers]
status: draft
version: 0.1.0
applies-to: [projects using issue tracking]
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# Issue Label Schema

This document defines the label schema used to attach agile metadata to issues.

> **Conditional**: This schema applies only when the project uses an issue tracker. See `agent-docs/12-metadata/project.yml`.

## Label Categories

### 1. Issue Type

| Label | Meaning |
|-------|---------|
| `feature` | New capability or user-facing functionality |
| `bug` | Defect or incorrect behavior |
| `design` | UX/UI design work, wireframes, prototypes |
| `documentation` | Docs creation or updates |
| `spike` | Time-boxed investigation or research |
| `chore` | Maintenance, dependency updates, non-functional work |
| `refactor` | Code restructuring without behavior change |
| `test` | Test coverage additions or test infrastructure |
| `security` | Security vulnerability or hardening |

**Required**: Yes — every issue should have exactly one type label.

### 2. Priority

| Label | Meaning |
|-------|---------|
| `priority-high` | Blocking, time-sensitive, or high customer impact |
| `priority-medium` | Important but not blocking |
| `priority-low` | Nice-to-have, deferred, or low impact |

**Required**: Yes — every issue should have exactly one priority label.

### 3. Status

| Label | Meaning |
|-------|---------|
| `status-not-started` | Issue identified but work hasn't begun |
| `status-in-progress` | Work is actively underway |
| `status-blocked` | Work paused due to external dependency or blocker |
| `status-review` | Work complete, awaiting code/design review |
| `status-done` | Work merged or released |

**Required**: Optional — useful for sprint boards and burndown tracking.

**Note**: GitHub's native open/closed state is the source of truth for completion. This label is for within-sprint workflow visibility.

### 4. Scope

| Label | Meaning |
|-------|---------|
| `scope-original` | Included in sprint planning |
| `scope-added-sprint` | Added to sprint after planning; indicates scope creep |

**Required**: Optional — useful for understanding sprint dynamics.

### 5. Story Points (Fibonacci)

| Label | Points | Typical Meaning |
|-------|--------|-----------------|
| `story-points-1` | 1 | Trivial change, well-understood |
| `story-points-2` | 2 | Small, straightforward |
| `story-points-3` | 3 | Small-to-medium, some unknowns |
| `story-points-5` | 5 | Medium, meaningful complexity |
| `story-points-8` | 8 | Large, significant unknowns |
| `story-points-13` | 13 | Very large — split before starting |

### 6. Human Hour Estimate

| Label | Hours |
|-------|-------|
| `human-estimate-hours-0.5` | 30 minutes |
| `human-estimate-hours-1` | 1 hour |
| `human-estimate-hours-2` | 2 hours |
| `human-estimate-hours-4` | Half day |
| `human-estimate-hours-8` | Full day |
| `human-estimate-hours-16` | 2 days |
| `human-estimate-hours-24` | 3 days |
| `human-estimate-hours-40` | Full week |

### 7. AI Hour Estimate

| Label | Hours |
|-------|-------|
| `ai-estimate-hours-0.25` | 15 minutes |
| `ai-estimate-hours-0.5` | 30 minutes |
| `ai-estimate-hours-1` | 1 hour |
| `ai-estimate-hours-2` | 2 hours |
| `ai-estimate-hours-4` | Half day |
| `ai-estimate-hours-8` | Full day |
| `ai-estimate-hours-16` | 2 days |

## Label Color Conventions (GitHub)

| Category | Hex |
|----------|-----|
| Issue type | `#0075ca` |
| Priority — high | `#d73a4a` |
| Priority — medium | `#e4e669` |
| Priority — low | `#0e8a16` |
| Status | `#a371f7` |
| Scope | `#f0883e` |
| Story points | `#7057ff` |
| Human estimate | `#0052cc` |
| AI estimate | `#5319e7` |

## Validation Rules

- **Exactly one** issue type per issue
- **Exactly one** priority per issue
- **At most one** status label per issue
- **At most one** scope label per issue
- **At most one** story point label per issue
- **At most one** human estimate label per issue
- **At most one** AI estimate label per issue

## See Also

- [Setup issue labels guide](../03-howto/setup-issue-labels.md) — How to create labels
- [Project metadata](../12-metadata/project.yml) — Active issue tracker config
