---
name: github-sprint-board
description: >
  Display a real-time sprint board from GitHub issues organized by status (not-started,
  in-progress, blocked, review, done). Shows story points, assignees, priorities, and
  scope indicators. Updates instantly from current issue state.
license: "PolyForm Noncommercial 1.0.0"
compatibility: claude, opencode
metadata:
  plugin: parallel-powers
  type: command
  requires:
    - github-cli
    - jq
copyright: "Copyright (c) 2026 Parallel Hours LLC"

---

The Sprint Board skill displays a Kanban-style board of sprint issues grouped by workflow status. Given a sprint (milestone) or time window, it provides real-time visibility into what's being worked on, blocked items, and completion status.

## Arguments

`$ARGUMENTS` — the sprint to display. One of:

| Format | Example | What happens |
|--------|---------|-------------|
| **Milestone name** | `Sprint-5` or `v1.2` | Shows all issues in that milestone, grouped by status |
| **Date range** | `2026-05-07..2026-05-21` | Shows issues created within that range |
| **"now"** | `now` | Shows current/active sprint (most recent milestone with target_date in future) |
| **Repository** | `owner/repo Sprint-1` | Scopes to specific repo |

Optional flags:
- `--group-by assignee|priority|type` — Group columns by assignee, priority, or issue type instead of status
- `--hide-blocked` — Hide blocked status column (for cleaner view when no blockers)
- `--show-points` — Show total story points per column (default: yes)
- `--refresh N` — Auto-refresh every N seconds (e.g., `--refresh 30`)

Full syntax:
- `/parallel-powers:github-sprint-board <milestone>`
- `/parallel-powers:github-sprint-board <date-range> --group-by priority`
- `/parallel-powers:github-sprint-board now --refresh 60`

If no argument given, show the current/active sprint.

---

## Steps

### 0 — Validate Environment & Determine Sprint

1. Check `gh` CLI is installed and authenticated
2. Determine target repository (from `--project` flag or git remote)
3. If `$ARGUMENTS` is empty or "now":
   - Find the milestone with:
     - `target_date` in the future (active sprint)
     - Most recently created
   - Use that as the sprint
4. Otherwise, resolve `$ARGUMENTS` to a specific milestone or date range (same as burndown skill, Step 1)

---

### 1 — Fetch Issues & Parse Labels

Query GitHub for all issues in the sprint:

```bash
gh issue list \
  --repo $REPO \
  --milestone "$MILESTONE" \
  --state all \
  --json "number,title,labels,assignees,state,createdAt,closedAt" \
  --limit 1000 > issues.json
```

For each issue, extract:
- **number, title, state** (open/closed)
- **assignees** — list of usernames
- **labels** — parse:
  - `status-*` → determine column (not-started, in-progress, blocked, review, done)
  - `priority-*` → priority level (high, medium, low)
  - `type-*` or other categorization labels
  - `story-points-*` → numeric points
  - `scope-*` → scope indicator

**Default status logic:**
- If `state == "closed"` → status = "done"
- If `state == "open"` and no status label → status = "in-progress"
- If `status-blocked` label present → status = "blocked"
- Otherwise use label value

---

### 2 — Organize by Grouping

Determine grouping strategy:
- **Default: by status** → columns are: Not Started | In Progress | Blocked | Review | Done
- **--group-by assignee** → columns are assignee names (or "Unassigned")
- **--group-by priority** → columns are: High | Medium | Low | Unset
- **--group-by type** → columns are: feature | bug | design | documentation | etc.

Within each column/group, sort by:
1. Priority (high → low)
2. Story points (largest first)
3. Issue number (ascending for tiebreak)

---

### 3 — Calculate Column Statistics

For each column:
- **Issue count** — number of issues
- **Story points total** — sum of all story points in column
- **Assignee coverage** — who's working in this column (if grouping by status)
- **Blocked count** — issues with blockers (if column contains open issues)

---

### 4 — Generate Board Layout

Create a text-based Kanban board:

```
╔════════════════════════════════════════════════════════════════════════════════╗
║ Sprint Board: {Milestone Name} ({Sprint Dates})                                ║
╚════════════════════════════════════════════════════════════════════════════════╝

 ┌─ Not Started ─────┬─ In Progress ──────┬─ Blocked ──────┬─ Review ───────┬─ Done ────────┐
 │ (2 issues, 8 pts) │ (3 issues, 13 pts) │ (1 issue, 5pt) │ (1 issue, 3pt) │ (8 issues)    │
 ├───────────────────┼────────────────────┼────────────────┼────────────────┼───────────────┤
 │ #142 [HIGH] (3)   │ #156 [HIGH] (5)    │ #161 [HIGH]    │ #170 (3)       │ #101 ✓        │
 │ Build auth        │ Add S3 upload      │ Waiting DB     │ PR review      │ Setup CLI     │
 │ @unassigned       │ @alice             │ @charlie       │ @bob           │ @alice        │
 │ 🟠 scope-added    │ 🟢 scope-original  │ ⛔ blocked     │ 🔵 review      │              │
 │                   │                    │                │                │              │
 │ #151 [MED] (5)    │ #165 [MED] (8)     │                │                │ #105 ✓       │
 │ Update tests      │ Refactor parser    │                │                │ Write docs   │
 │ @unassigned       │ @alice             │                │                │ @yuki        │
 │ 🟢 scope-original │ 🟢 scope-original  │                │                │              │
 │                   │                    │                │                │              │
 │                   │ #172 [LOW] (0)     │                │                │ #109 ✓       │
 │                   │ Code review fix    │                │                │ Fix typos    │
 │                   │ @david             │                │                │ @david       │
 │                   │ 🟢 scope-original  │                │                │              │
 │                   │                    │                │                │              │
 └───────────────────┴────────────────────┴────────────────┴────────────────┴───────────────┘

Legend:
  [HIGH/MED/LOW]       Priority
  (N)                  Story points
  @username            Assigned to
  🟢 scope-original    Part of sprint plan
  🟠 scope-added       Added mid-sprint (scope creep)
  ⛔ blocked           Blocked on external work
  ✓                    Done/Closed
```

---

### 5 — Add Summary Stats

Below the board, add a summary table:

```
╔════════════════════════════════════════════════════════════════════════════════╗
║ Sprint Summary                                                                  ║
╠═══════════════════════════════════════════════════════════════════╪═════╪══════╣
║ Status                   │ Issues │ Points │ % of Total │ Avg Size           ║
╠══════════════════════════╪════════╪════════╪════════════╪════════════════════╣
║ ✓ Done                   │   8    │  15    │   34%      │ 2 points/issue     ║
║ ⧗ Review                 │   1    │   3    │    7%      │ 3 points/issue     ║
║ ➜ In Progress            │   3    │  13    │   30%      │ 4 points/issue     ║
║ ⊘ Blocked                │   1    │   5    │   11%      │ 5 points/issue     ║
║ ○ Not Started            │   2    │   8    │   18%      │ 4 points/issue     ║
╠══════════════════════════╪════════╪════════╪════════════╪════════════════════╣
║ TOTAL (Original Scope)   │  15    │  44    │  100%      │ 3 points/issue     ║
║ ADDED (Scope Creep)      │   1    │   3    │   +7%      │ 3 points/issue     ║
╚════════════════════════════════════════════════════════════════════╧═════╧══════╝

Staffing Summary:
  @alice:    3 issues (13 pts) — In Progress, highest utilization
  @bob:      1 issue  (3 pts)  — In Review
  @charlie:  1 issue  (5 pts)  — Blocked
  @david:    2 issues (8 pts)  — In Progress + 1 Done
  Unassigned: 2 issues (8 pts) — Not Started, needs assignment
```

---

### 6 — Highlight Risks & Bottlenecks

Add a brief risk section:

```
⚠ Risks & Bottlenecks
─────────────────────
🔴 1 Blocker      — #161 "Waiting on DB migration" (assigned to @charlie)
                    Unblocks #163 and #164. Expected resolution: {date}

🟡 2 Unassigned   — #142 "Build auth", #151 "Update tests"
                    8 story points sitting idle. Needs assignment.

🟢 Scope Creep OK — +1 issue, +3 points. Manageable with current velocity.
```

---

### 7 — Interactive Options

After displaying the board, offer quick actions:

```
What's next?
  [1] Show details for a specific issue
  [2] Show issues by assignee
  [3] Show only high-priority items
  [4] Show only blockers
  [5] Auto-refresh (live updates every 30s)
  [6] Assign unassigned issues
  [7] Help
```

Examples:
- "Show #142" → expand issue details
- "Assign #142 to alice" → update via GitHub
- "Blockers" → filter to only blocked items
- "Refresh" → auto-update board every 30 seconds

---

## Grouping Variations

### By Status (Default)
```
Not Started | In Progress | Blocked | Review | Done
```

### By Assignee
```
@alice | @bob | @charlie | @david | Unassigned
```

### By Priority
```
High | Medium | Low | Unset
```

### By Type
```
Feature | Bug | Design | Documentation | Other
```

---

## Real-Time Updates (--refresh flag)

If `--refresh N` is specified:
1. Re-fetch issue data every N seconds
2. Update board in place (terminal clear + redraw)
3. Highlight changes in green (new items) or red (status changes)
4. Show timestamp of last update
5. Press Ctrl+C to stop auto-refresh

---

## Examples

```bash
# Show board for current sprint
/parallel-powers:github-sprint-board now

# Show board grouped by assignee
/parallel-powers:github-sprint-board Sprint-5 --group-by assignee

# Show board with auto-refresh every 30 seconds
/parallel-powers:github-sprint-board "Sprint 5" --refresh 30

# Show only high-priority items
/parallel-powers:github-sprint-board Sprint-5 --show-priority high

# Show different repo
/parallel-powers:github-sprint-board v2.0 --project anthropic/anthropic-sdk-python
```

---

## Limitations & Notes

- **Status label required** — If an issue has no `status-*` label, logic infers from `state` (see Step 1)
- **Live updates** are best-effort; GitHub API has rate limits (5000 requests/hour for authenticated users)
- **Assignee display** — Shows first assignee if multiple; use `--show-all-assignees` to see full list
- **Point size** — Cards scale vertically by points (more points = taller card) for visual scanning
- **Scope indicator** — `🟢 scope-original` vs `🟠 scope-added` helps spot creep quickly

---

## Color Scheme (if terminal supports)

- 🟢 Green: scope-original, healthy progress, no blockers
- 🟡 Yellow: medium priority, partially done, unassigned
- 🔴 Red: high priority, blocked, at risk
- ⛔ Red X: blocked, requires action
- ✓ Checkmark: done/closed
