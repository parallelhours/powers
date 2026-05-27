# HITL Phase-Aligned Skills Design

**Date:** 2026-05-27  
**Status:** Approved  
**Author:** Paul Monday (via brainstorming session)  
**Branch:** feat/5-design-phase-aligned-skills-for-human-in-the-loop

---

## Overview

This spec defines eight new `parallel-powers` skills that align with the Human-in-the-Loop (HITL) development cadence described in `agent-docs/02-tutorial/human-in-the-loop.md`. Each skill covers one phase of the cadence, adopts the appropriate persona(s) from `agent-docs/13-personas/`, produces a canonical artifact written to `agent-docs/`, and ends with an explicit human approval gate before moving on.

### Existing skills (not replaced)

| Skill | Phase |
|-------|-------|
| `diataxis-install` | Phase 0 — Project Setup |
| `diataxis-refresh` | Phase 0 — Documentation refresh |
| `session-start` | Phase 4 — Task timer start |
| `session-end` | Phase 4 — Task timer stop |
| `editorial-reviewer` | Phase 4 — Content review (Emery) |
| `github-sprint-board` | Phase 4 — Sprint status |
| `github-burndown` | Phase 4 — Sprint burndown |

---

## Phase Flow

```
Phase 0:  diataxis-install
Phase 1:  requirements          → PRD
Phase 2:  architecture          → HLD + ADRs
Phase 2b: lld [×N components]   → component design docs
Phase 2c: lld --finalize        → reconciled architecture + multi-persona review
Phase 3:  sprint-plan           → PM plan + sprint backlog
Phase 4:  session-start / session-end / debug (per task)
Phase 4↩: sprint-review [N]    → sprint review doc
Phase 5:  milestone-review [N]  → milestone review doc
```

---

## Skill Inventory

| Skill | Invocation | Persona(s) | Phase | Deliverable |
|-------|-----------|-----------|-------|-------------|
| `requirements` | `/parallel-powers:requirements` | Taylor (Product Marketing) | 1 | `agent-docs/05-plans/prd.md` |
| `architecture` | `/parallel-powers:architecture` | Amara (Architect) | 2 | `agent-docs/01-explanation/architecture.md` + ADRs |
| `lld` | `/parallel-powers:lld [component]` | Amara + Wei | 2b | `agent-docs/01-explanation/components/<component>.md` |
| `lld --finalize` | `/parallel-powers:lld --finalize` | Amara + Wei + Morgan + Taylor (opt-in) | 2c | Reconciled `architecture.md` |
| `sprint-plan` | `/parallel-powers:sprint-plan` | Morgan + Wei | 3 | `agent-docs/05-plans/pm-plan.md` + `sprint-backlog.md` |
| `sprint-review` | `/parallel-powers:sprint-review [N]` | Morgan + Wei | 4 end | `agent-docs/05-plans/sprint-N-review.md` |
| `milestone-review` | `/parallel-powers:milestone-review [N]` | Morgan | 5 | `agent-docs/05-plans/milestone-N-review.md` |
| `debug` | `/parallel-powers:debug [description]` | Wei (Developer) | 4 | GitHub issue + timer + fix |

---

## Common Skill Structure

Every skill follows this pattern, scaled to its phase. **Step 4 (the approval gate) is the invariant — it cannot be skipped.**

```
Step 0 — Load persona
  Read agent-docs/13-personas/<persona>.md
  Adopt that persona's voice, goals, and lens for the session

Step 1 — Context check
  Read prior-phase artifacts from agent-docs/ (phase-specific)
  Warn if prerequisites are missing; offer to continue or pause

Step 2 — Interactive Q&A
  Ask clarifying questions one at a time
  Phase-specific questions (see each skill below)
  Human answers guide the draft

Step 3 — Draft artifact
  Produce the phase deliverable in the persona's voice
  Present to human for review section by section

Step 4 — Human approval gate   ← THE HITL CHECKPOINT
  Explicit: "Does this look right? Any changes before I save?"
  Required before writing any file — never skipped

Step 5 — Write to agent-docs/
  Save to canonical location with valid YAML frontmatter
  Commit: git add + git commit

Step 6 — Handoff
  Print a summary of what was produced
  Suggest the next phase skill
```

---

## Per-Skill Details

### `requirements` — Phase 1

**Persona:** Taylor (Product Marketing) — `agent-docs/13-personas/product-marketing.md`

**Context check:**
- Look for existing `agent-docs/05-plans/prd.md`
- If found: ask "Continue editing the existing PRD or start fresh?"
- If missing: proceed to Q&A

**Q&A topics (one at a time):**
1. What problem are we solving, and for whom?
2. Why now — what's the trigger or opportunity?
3. What are the functional requirements? (iterate until complete)
4. Non-functional requirements (performance, security, scale, accessibility)?
5. What does success look like? (acceptance criteria per requirement)
6. Impact vs. effort — how would you prioritize these requirements?

**Artifact — `agent-docs/05-plans/prd.md`:**
```
# Product Requirements Document
## Context
## Problem Statement
## Functional Requirements
## Non-Functional Requirements
## Acceptance Criteria
## Prioritization
## Success Metrics
```

**Frontmatter:** standard YAML with `labels: [prd, requirements]`, `status: draft`, `version: 0.1.0`.

**Handoff:** `→ /parallel-powers:architecture`

---

### `architecture` — Phase 2

**Persona:** Amara (Architect) — `agent-docs/13-personas/architect.md`

**Context check:**
- Read `agent-docs/05-plans/prd.md`
- If missing: warn "No PRD found. Architecture without requirements risks drift. Continue anyway?" — wait for response
- If present: summarize the requirements scope before asking questions

**Q&A topics (one at a time):**
1. Greenfield or building on existing architecture?
2. Technology constraints or decisions already made?
3. Key integration points or external dependencies?
4. Where are the highest-risk architectural decisions?

**Artifacts:**
- `agent-docs/01-explanation/architecture.md` — system overview, component breakdown, data flow, key interfaces
- `agent-docs/01-explanation/decisions/YYYY-MM-DD-<decision>.md` — one ADR per significant decision

**ADR format:**
```
# ADR-NNN: <title>
## Status: Proposed | Accepted | Deprecated
## Context
## Decision
## Consequences
```

**Frontmatter:** `labels: [architecture, hld]` for main doc; `labels: [adr, decision]` for each ADR.

**Handoff:** `→ /parallel-powers:lld <first-component>` (if project has multiple components) or `→ /parallel-powers:sprint-plan` (if single-component / small project)

---

### `lld` — Phase 2b (per component) and 2c (finalize)

**Personas:**
- Per-component: Amara (Architect) + Wei (Developer) — dual perspective
- Finalize: Amara + Wei + Morgan (PM) + Taylor (opt-in)

**Load order:** Read `agent-docs/13-personas/architect.md` first, then `agent-docs/13-personas/developer.md`. Maintain both perspectives throughout.

#### Per-component mode: `/parallel-powers:lld [component-name]`

**Context check:**
- `agent-docs/01-explanation/architecture.md` — **required**. If missing: "No HLD found. Run `/parallel-powers:architecture` first." Stop.
- List existing component docs in `agent-docs/01-explanation/components/` — show progress

**Q&A topics (one at a time):**
1. What is this component's single responsibility?
2. What are its interfaces — what does it expose, what does it depend on?
3. Any implementation constraints Wei sees from the developer side?
4. Key data structures, state, or algorithms?
5. Error handling and edge cases?
6. Open questions or deferred decisions?

**Artifact — `agent-docs/01-explanation/components/<component-name>.md`:**
```
# Component: <name>
## Responsibility
## Interfaces
### Exposed
### Dependencies
## Data Model
## Error Handling
## Open Questions
```

**End of each component run:**
- List all completed component docs
- Show which components from the HLD still need LLD
- Suggest: `→ /parallel-powers:lld <next-component>` or `→ /parallel-powers:lld --finalize` when all done

#### Finalize mode: `/parallel-powers:lld --finalize`

**Steps:**

1. **Load all three persona files:** architect, developer, project-manager
2. **Gather artifacts:** read all files in `agent-docs/01-explanation/components/` + `agent-docs/01-explanation/architecture.md`
3. **Amara's review** — coherence across components:
   - Do LLD decisions hold together across all components?
   - Any drift from the HLD?
   - Gaps or overlaps in component responsibilities?
4. **Wei's review** — implementability:
   - Are the interfaces actually buildable?
   - Anything that will cause pain in Sprint 1?
   - Dependencies between components that affect sprint ordering?
5. **Morgan's review** — scope/timeline impact:
   - Did LLD decisions add complexity that changes sprint estimates?
   - Any components significantly larger or smaller than assumed in HLD?
6. **Taylor opt-in** — PRD compliance:
   - Prompt: "Would you like Taylor to review the component designs against the PRD for requirement compliance?"
   - If yes: read `agent-docs/05-plans/prd.md` + adopt Taylor persona; check each component against acceptance criteria
   - If no: skip
7. **Human approval gate** — present all review findings; wait for response
8. **Write reconciliation:**
   - Append "## LLD Reconciliation" section to `agent-docs/01-explanation/architecture.md`
   - Document: decisions that changed from HLD, new risks surfaced, component dependency order for sprint planning
9. **Commit** all changes

**Handoff:** `→ /parallel-powers:sprint-plan`

---

### `sprint-plan` — Phase 3

**Personas:** Morgan (PM) + Wei (Developer)  
Load: `agent-docs/13-personas/project-manager.md` + `agent-docs/13-personas/developer.md`

**Context check:**
- Read `agent-docs/05-plans/prd.md` (requirements)
- Read `agent-docs/01-explanation/architecture.md` (HLD)
- Read `agent-docs/01-explanation/components/` (LLD, if present)
- Summarize understood scope before asking any questions — human confirms or corrects

**Q&A topics (one at a time):**
1. Total scope — one sprint or multi-sprint project?
2. Any hard deadlines or milestone dates?
3. Which tasks are highest risk or most uncertain?
4. For each task: Wei gives human-hours estimate; Morgan challenges or accepts; both agree on AI-assisted estimate

**Artifacts:**

`agent-docs/05-plans/pm-plan.md`:
```
# Project Management Plan
## Project Summary
## Milestones
## Sprint Structure
## Gantt Timeline
## Risk Areas
## Human vs AI-Assisted Estimates
```

`agent-docs/05-plans/sprint-backlog.md`:
```
# Sprint Backlog
## Sprint N: <goal>
| Task | Type | Points | Human hrs | AI-assisted hrs | Priority | Notes |
...
```

**Frontmatter:** `labels: [pm-plan, sprint-backlog]`.

**Handoff:** `→ /parallel-powers:session-start <first-issue>` to begin Sprint 1

---

### `sprint-review` — Phase 4 end

**Arguments:** optional sprint number `[N]`. If omitted, infer from `sprint-backlog.md` (look for the most recent in-progress sprint).

**Personas:** Morgan (PM) + Wei (Developer)  
Load: `agent-docs/13-personas/project-manager.md` + `agent-docs/13-personas/developer.md`

**Context check:**
- Read `agent-docs/05-plans/sprint-backlog.md` — get planned tasks for sprint N
- Read `.session.json` if present — get tracked time for current session
- Run `gh issue list --milestone <sprint-N> --state all --json number,title,state,labels` — get actual completion status
- If `.session.json` is active: warn "There is an active session. End it with `/parallel-powers:session-end` before reviewing the sprint."

**Q&A topics (one at a time):**
1. Completed vs. planned — confirm the GitHub issue status is accurate
2. What wasn't completed — and why? (blockers, scope creep, underestimate)
3. Any blockers to carry forward to next sprint?
4. Given actual velocity, does the estimate for remaining sprints need updating?

**Artifact — `agent-docs/05-plans/sprint-N-review.md`:**
```
# Sprint N Review
## Summary
## Completed vs Planned
| Task | Planned | Actual | Notes |
## Time Tracked
## Blockers & Carry-Forward
## Updated Estimates
## Notes for Next Sprint
```

**Frontmatter:** `labels: [sprint-review, sprint-N]`.

**Handoff:**
- If more sprints in current milestone: `→ /parallel-powers:sprint-plan` (next sprint)
- If milestone complete: `→ /parallel-powers:milestone-review [N]`

---

### `milestone-review` — Phase 5

**Arguments:** optional milestone number `[N]`. If omitted, infer from `pm-plan.md`.

**Persona:** Morgan (PM)  
Load: `agent-docs/13-personas/project-manager.md`

**Context check:**
- Read all `agent-docs/05-plans/sprint-N-review.md` files for this milestone
- Read `agent-docs/05-plans/pm-plan.md` — get original estimates for comparison
- Run `gh milestone view <N> --json title,description,dueOn,closedIssues,openIssues` for GitHub milestone status

**Q&A topics (one at a time):**
1. Demo — what was built? Describe the working software or documentation delivered
2. What worked well in this milestone's process?
3. What didn't work — what to change for next milestone?
4. Given actual velocity, does the remaining roadmap need re-estimation?

**Artifact — `agent-docs/05-plans/milestone-N-review.md`:**
```
# Milestone N Review
## Summary
## What Was Delivered (Demo)
## Metrics
### Human vs AI-Assisted Time
### Estimate Accuracy (planned vs actual per sprint)
### Velocity Trend
## Retrospective
### What Worked
### What Didn't
### Changes for Next Milestone
## Updated Roadmap
```

**Frontmatter:** `labels: [milestone-review, milestone-N]`.

**Handoff:**
- If more milestones: `→ /parallel-powers:sprint-plan` (next milestone's first sprint)
- If final milestone: prompt for project completion retrospective

---

### `debug` — Phase 4 (integrated)

**Persona:** Wei (Developer)  
Load: `agent-docs/13-personas/developer.md`

**Arguments:** optional description `[description]`. If omitted, prompt: "Describe the bug — what happened vs. what you expected."

**Steps (diverges from common structure — action-first, not Q&A-first):**

**Step 0 — Load Wei persona**

**Step 1 — Capture bug report**
- Collect: description, steps to reproduce, expected vs. actual behavior, environment (OS, version, branch)
- If `$ARGUMENTS` provided, use as initial description and ask only for missing fields

**Step 2 — Create GitHub issue**
- `gh issue create --title "<bug summary>" --body "<formatted bug report>" --label "bug" --label "priority-<inferred>"`
- Infer priority: `high` if data loss / crash, `medium` if broken feature, `low` if cosmetic
- Print the created issue URL

**Step 3 — Start timer**
- Check `.session.json` — if active session exists, ask: "Attach debug time to active session #N, or start a new session for this bug?"
- If new session: call `start_timer(task_id=<new-task-id>, notes="Debugging: <issue title>")`
- Save `timer_id` for step 7

**Step 4 — Systematic debugging**

Loop until fix confirmed:
1. **Reproduce** — attempt to reproduce the bug; confirm reproduction steps work
2. **Isolate** — identify the smallest reproducible case; narrow to component/file
3. **Hypothesize** — surface hypothesis to human: "I believe the cause is X because Y. Shall I test this?"
   - **Wait for human approval** before testing each hypothesis
4. **Verify** — run tests or add diagnostic output to confirm/refute hypothesis
5. **Fix** — implement the fix; present diff to human before applying
6. **Test** — run relevant tests; report pass/fail

**Step 5 — Commit fix**
- `git commit -m "fix: <description> (closes #N)"`
- Link commit to GitHub issue

**Step 6 — Stop timer and log**
- `stop_timer(timer_id=<timer_id>, ...)`
- `log_ai_event(timer_id=<timer_id>, ...)`
- Print session summary

**Handoff:** `→ /parallel-powers:session-end` if a full session was started

---

## Persona Loading Convention

All skills read persona files at runtime rather than embedding them. This ensures skills always reflect the current persona definition.

**Pattern in each skill's Step 0:**
```
Read agent-docs/13-personas/<persona-file>.md
Adopt the persona: use their name in responses, apply their goals and lens,
communicate in their voice for the duration of this skill.
```

For dual-persona skills (lld, sprint-plan, sprint-review): both persona files are read. The skill alternates perspective explicitly — e.g., "Amara notes a coherence issue..." / "Wei flags an implementability concern..."

---

## Artifact Conventions

All artifacts written by these skills must include valid YAML frontmatter per `agent-docs/12-metadata/file-structure.md`:

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
labels: [<phase-label>, ...]
description: <one-line summary>
status: draft
version: 0.1.0
copyright: "Copyright (c) <year> <owner>"
license: "PolyForm Noncommercial 1.0.0"
---
```

Skills commit artifacts immediately after writing with a conventional commit message:

```
docs(<phase>): add <artifact-name>

Generated by /parallel-powers:<skill> — human approved before save.
```

---

## Constraints and Non-Goals

- **Requires diataxis:** All skills assume `agent-docs/` exists with standard structure. If missing, skills warn and suggest `diataxis-install` first.
- **Requires GitHub CLI:** `debug`, `sprint-review`, `milestone-review` use `gh`. Skills check for `gh` availability and fail gracefully.
- **Requires parallelhours MCP:** `debug` uses `start_timer`/`stop_timer`/`log_ai_event`. If MCP is unavailable, debug falls back to prompt-only workflow without time tracking.
- **No automated merging:** Skills never merge branches or close milestones automatically. Human performs all merge and close operations.
- **No cross-project scope:** Skills operate on the current repo only.

---

## Open Questions

None — all design decisions resolved during brainstorming session.
