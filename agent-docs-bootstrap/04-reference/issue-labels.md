---
created: 2026-04-06
updated: 2026-04-06
labels: [reference, issues, agile, labels]
description: Issue label schema for agile metadata — types, priority, story points, and hour estimates across issue tracking systems.
tags: [issues, labels, agile, github, jira, story-points, estimates]
audience: [developers, agents, project-managers]
status: active
version: 1.0.0
applies-to: [projects using issue tracking]
---

# Issue Label Schema

This document defines the label schema used to attach agile metadata to issues. It is system-aware: GitHub labels are the default, but equivalent mappings are provided for Jira and parallelhours.io.

> **Conditional**: This schema applies only when the project uses an issue tracker. See `agent-docs/12-metadata/project.yml` for the configured `issue-tracker` value.

---

## Label Categories

### 1. Issue Type

Describes the nature of the work.

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

**GitHub label name**: the value itself (e.g., `feature`, `bug`)

**Required**: Yes — every issue should have exactly one type label.

---

### 2. Priority

Signals urgency and scheduling order.

| Label | Meaning |
|-------|---------|
| `priority-high` | Blocking, time-sensitive, or high customer impact |
| `priority-medium` | Important but not blocking |
| `priority-low` | Nice-to-have, deferred, or low impact |

**Required**: Yes — every issue should have exactly one priority label.

---

### 3. Story Points

Complexity estimate using the Fibonacci sequence. Story points measure relative effort, not time.

| Label | Points | Typical Meaning |
|-------|--------|-----------------|
| `story-points-1` | 1 | Trivial change, well-understood |
| `story-points-2` | 2 | Small, straightforward |
| `story-points-3` | 3 | Small-to-medium, some unknowns |
| `story-points-5` | 5 | Medium, meaningful complexity |
| `story-points-8` | 8 | Large, significant unknowns — consider splitting |
| `story-points-13` | 13 | Very large — split before starting |

**Label prefix**: `story-points-` (configurable per repository via `agent-docs/12-metadata/project.yml`)

**Required**: Recommended — assign before sprint planning.

**Note**: If your issue tracker is parallelhours.io or parallelhours, story points are stored as the `story_points` field (integer). The label prefix is configurable in `GitHubRepository.label_prefix`.

---

### 4. Human Hour Estimate

The estimated time for a human to complete the work without AI assistance. Use discrete values.

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

**Label prefix**: `human-estimate-hours-`

**Required**: Optional — populate during sprint planning or estimation sessions.

**Note**: In parallelhours this maps to `estimate_human_min` (stored in minutes). Multiply hours × 60 when syncing to the API.

---

### 5. AI Hour Estimate

The estimated time for a human working *with AI assistance* to complete the work. AI significantly reduces calendar time for many tasks.

| Label | Hours |
|-------|-------|
| `ai-estimate-hours-0.25` | 15 minutes |
| `ai-estimate-hours-0.5` | 30 minutes |
| `ai-estimate-hours-1` | 1 hour |
| `ai-estimate-hours-2` | 2 hours |
| `ai-estimate-hours-4` | Half day |
| `ai-estimate-hours-8` | Full day |
| `ai-estimate-hours-16` | 2 days |

**Label prefix**: `ai-estimate-hours-`

**Required**: Optional — populated by AI estimation tools or manually during planning.

**Note**: In parallelhours this maps to `ai_estimate_human_ai_min`. A separate `ai_estimate_human_min` field tracks what a human would take *without* AI — that corresponds to the human estimate label above.

---

## Label Color Conventions (GitHub)

Consistent colors make label categories visually scannable in the GitHub UI.

| Category | Suggested Color | Hex |
|----------|----------------|-----|
| Issue type | Blue-grey | `#0075ca` |
| Priority — high | Red | `#d73a4a` |
| Priority — medium | Yellow | `#e4e669` |
| Priority — low | Light green | `#0e8a16` |
| Story points | Purple | `#7057ff` |
| Human estimate | Teal | `#0052cc` |
| AI estimate | Indigo | `#5319e7` |

---

## System Mappings

### GitHub (default)

Labels are free-text strings attached to issues. Each label above maps directly to its name string.

### Jira

Jira uses structured fields rather than free-text labels.

| Label Category | Jira Field |
|---------------|-----------|
| Issue type | Issue Type (system field) |
| Priority | Priority (system field) |
| Story points | Story Points custom field (or `story_points` in next-gen) |
| Human estimate | Original Estimate (time tracking) or custom field |
| AI estimate | Custom field: `AI Estimate (h)` |

Configure custom fields in Jira project settings. Story points must be enabled in board configuration.

### parallelhours.io / parallelhours

| Label Category | Field |
|---------------|-------|
| Issue type | `task_type` — choices: `feature`, `bug`, `spike`, `chore` |
| Priority | `priority` — choices: `high`, `medium`, `low` |
| Story points | `story_points` — integer, Fibonacci values |
| Human estimate | `estimate_human_min` — integer minutes |
| AI estimate | `ai_estimate_human_ai_min` — integer minutes (AI-generated) |

GitHub labels are synced to these fields automatically when GitHub integration is enabled.

---

## Validation Rules

- **Exactly one** issue type per issue
- **Exactly one** priority per issue
- **At most one** story point label per issue
- **At most one** human estimate label per issue
- **At most one** AI estimate label per issue
- Do not combine `story-points-8` or `story-points-13` without a plan to split — large issues reduce sprint predictability

---

## Related

- `agent-docs/03-howto/setup-issue-labels.md` — How to create these labels in each system
- `agent-docs/12-metadata/project.yml` — Where the active issue tracker and label prefix are configured
- `agent-docs/11-agents/time-tracking.md` — How agents interact with time tracking during sessions
