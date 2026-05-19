---
name: github-burndown
description: >
  Generate a burndown chart from GitHub issues for a sprint (milestone). Shows story point
  burn rate, scope changes, velocity, and completion forecast. Requires repository with
  issue labels: story-points-*, status-*, scope-*.
license: MIT
compatibility: claude, opencode
metadata:
  plugin: parallel-powers
  type: command
  requires:
    - github-cli
    - jq
---

The GitHub Burndown skill generates sprint burndown charts and velocity analysis from GitHub issues. Given a milestone (sprint) identifier, it visualizes story point burn rate, identifies scope creep, and forecasts sprint completion.

## Arguments

`$ARGUMENTS` — the sprint to analyze. One of:

| Format | Example | What happens |
|--------|---------|-------------|
| **Milestone name** | `v1.2` or `Sprint 5` | Fetches all issues in that milestone; calculates burndown based on closed dates |
| **Date range** | `2026-05-01..2026-05-14` | Filters issues created/closed within date range; treats as ad-hoc sprint |
| **Repository** | `owner/repo milestone:Sprint-1` | Analyzes specific repo; scopes to that milestone |

An optional `--project` flag specifies the GitHub repository (owner/repo). Defaults to current directory's repo.

Full syntax:
- `/parallel-powers:github-burndown <milestone>`
- `/parallel-powers:github-burndown <date-range> --project owner/repo`
- `/parallel-powers:github-burndown --list` — Show all milestones in the repo

If no argument is given, list available milestones.

**Requirements:**
- GitHub CLI (`gh`) authenticated and configured
- Target repo has issues with `story-points-*` labels
- Milestone or date range specified

---

## Steps

### 0 — Validate Environment

1. Check that `gh` CLI is installed and authenticated:
   ```bash
   gh auth status
   ```
   If not authenticated, fail with instruction to run `gh auth login`.

2. Determine the target repository:
   - If `--project owner/repo` is specified, use that
   - Otherwise, get remote from current git directory: `git config --get remote.origin.url`
   - If no repo found, fail with instruction to specify `--project`

3. If `--list` flag is provided, show available milestones and exit (see Step 2).

---

### 1 — Resolve Sprint Identifier

Parse `$ARGUMENTS` to determine the sprint:

**If it matches a milestone name** (e.g., "v1.2", "Sprint 5"):
- Query GitHub for exact milestone match
- Extract milestone title and dates (target_date if set)

**If it matches a date range** (e.g., "2026-05-01..2026-05-14"):
- Parse start and end dates (ISO 8601)
- Use date range as artificial sprint boundary

**If it's ambiguous or not found**:
- Search for similar milestone names (fuzzy match)
- Prompt: "Did you mean: [list of closest matches]?"

If still unresolved, fail with: "Milestone not found. Use `--list` to see available sprints."

---

### 2 — Fetch Sprint Issues

Query GitHub for all issues in the milestone:

```bash
gh issue list \
  --repo $REPO \
  --milestone "$MILESTONE" \
  --state all \
  --json "number,title,labels,createdAt,closedAt,state" \
  --limit 1000 > issues.json
```

Parse the JSON and extract:
- **Issue number, title, state** (open/closed)
- **createdAt, closedAt** timestamps
- **Labels** — filter for:
  - `story-points-*` — extract numeric value
  - `status-*` — current status
  - `scope-*` — scope indicator (original vs added)

For each issue:
- If `state == "closed"`, use `closedAt` as completion date
- If `state == "open"`, mark as incomplete
- Assign story points (default 0 if no label)

---

### 3 — Calculate Sprint Metrics

**Sprint boundary:**
- If milestone has `target_date`, use that as sprint end
- If date range was provided, use end date
- Otherwise, estimate from issue closed dates (use latest closedAt)

**Total story points:**
- Sum story points for all issues in scope

**By-day burn:**
- For each calendar day from sprint start to today:
  - Count issues closed by that day
  - Sum their story points
  - Record as (date, remaining_points)

**Current state:**
- Count open issues by status label
- Count by scope (original vs added)
- Identify blocked issues

**Velocity:**
- If previous sprint data available: compare burn rate
- Otherwise, calculate velocity as: (points closed) / (days elapsed)

---

### 4 — Generate Burndown Chart

Create a Mermaid XY chart (line chart) showing:

```
Title: Sprint Burndown — {Milestone Name}
X-axis: Date (sprint start to sprint end)
Y-axis: Story Points Remaining

Line 1: "Ideal" — straight line from total points to 0 (projected)
Line 2: "Actual" — jagged line showing actual daily burn
Line 3 (optional): "Forecast" — extrapolated line if sprint incomplete
```

Example output:

```
xychart-beta
  title Sprint Burndown — Sprint 5 (2026-05-07 to 2026-05-21)
  x-axis [May 7, May 8, May 9, ..., May 21]
  y-axis "Story Points" 0 --> 45
  line [45, 44, 41, 40, 38, 35, 30, 25, 20, 15, ...] name "Ideal"
  line [45, 45, 42, 40, 39, 35, 33, 32, 28, 20, ...] name "Actual"
```

---

### 5 — Generate Sprint Board

Create a table showing sprint status at a glance:

```
╔════════════════════════════════════════════════════════════════╗
║ Sprint: {Milestone}  |  Sprint Board                           ║
╠════════════════════════════════════════════════════════════════╣
║ Status                │ Issues  │  Points  │  % of Sprint      ║
╠═══════════════════════╪═════════╪══════════╪═══════════════════╣
║ ✓ Done                │   N     │   M pts  │   X%              ║
║ ⧗ In Review           │   N     │   M pts  │   X%              ║
║ ➜ In Progress         │   N     │   M pts  │   X%              ║
║ ⊘ Blocked             │   N     │   M pts  │   X%              ║
║ ○ Not Started         │   N     │   M pts  │   X%              ║
╠═══════════════════════╪═════════╪══════════╪═══════════════════╣
║ TOTAL (Original)      │   N     │   M pts  │   100%            ║
║ ADDED (Scope Creep)   │   N     │   M pts  │   +Y%             ║
║ REMAINING             │   N     │   M pts  │                   ║
╚════════════════════════════════════════════════════════════════╝

Velocity:  X points/day
Forecast:  Complete by {DATE} (on-time / at risk)
```

---

### 6 — Analyze Trends and Flags

For each condition, emit a flag:

**On Track** 🟢
- Actual burn ≥ ideal burn line, or
- Remaining points ≤ velocity × days_left

**At Risk** 🟡
- Actual burn < ideal, but still achievable with acceleration
- Scope creep detected but manageable

**Off Track** 🔴
- Current velocity insufficient to complete sprint
- Major scope creep without corresponding acceleration

**Blocked** ⛔
- Issues marked `status-blocked` without clear resolution
- Dependency on external work

**Analysis box:**
```
Burndown Analysis
─────────────────
✓ Velocity: {X} pts/day (compare to historical avg if available)
✓ Scope: {Y} original + {Z} added (+{PCT}% creep)
⚠ Blockers: {N} issues blocked, {M} waiting on review
🔴 Risk: {description} if burn rate doesn't improve
```

---

### 7 — Report Output

Print structured report:

```
═══ GitHub Burndown — {Milestone Name} ═══

Sprint: {Title}  |  {Start Date} to {End Date}
Repository: {owner/repo}
Remaining days: {N} (as of {today})

── Sprint Board ──
[Table from Step 5]

── Burndown Chart ──
[Mermaid chart from Step 4]

── Velocity & Forecast ──
Current velocity: {X} points/day
Historical velocity (if available): {Y} points/day
Forecast: {Complete by DATE or AT RISK}
Confidence: {HIGH/MEDIUM/LOW} based on velocity and remaining work

── Burndown Analysis ──
[Analysis box from Step 6]

── Issues at a Glance ──

Blocked ({N}):
  - #{issue}: {title}
  - #{issue}: {title}

In Review ({N}):
  - #{issue}: {title}

Scope Additions:
  - #{issue}: {title} (+{N} pts)

═══ End of Report ═══
```

---

### 8 — Offer Follow-up

After the report, ask:

"What would help? Show [issues by assignee / priority breakdown / velocity trend over time / risks]?"

---

## Data Format Notes

- **Dates**: ISO 8601 (YYYY-MM-DD). GitHub API returns RFC 3339, convert with `date --iso-8601 < RFC3339_timestamp`
- **Story Points**: Extract numeric value from label name (e.g., `story-points-5` → 5 points)
- **Status labels**: Recognizable values are `not-started`, `in-progress`, `blocked`, `review`, `done`
- **Scope labels**: `original` or `added-sprint`

---

## Limitations & Assumptions

- **Burndown assumes** issues closed = work done. Reality may differ (closed-but-regressed, reopened issues not re-counted)
- **Velocity assumes** consistent sprint dates and issue labeling. Unlabeled issues default to 0 points
- **Forecast assumes** linear burn. Actual sprints are lumpy (bursts of activity then plateaus)
- **No integration** with CI/CD (yet) — burndown is based on issue close events only

---

## Examples

```bash
# Show burndown for current sprint (most recent milestone)
/parallel-powers:github-burndown Sprint-5

# Show burndown for a date range
/parallel-powers:github-burndown 2026-05-07..2026-05-21

# Show burndown for a different repo
/parallel-powers:github-burndown "v2.0" --project anthropic/anthropic-sdk-python

# List all available milestones
/parallel-powers:github-burndown --list
```
