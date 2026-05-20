---
name: session-start
description: Start a tracked development session for a GitHub issue. Verifies git state, creates or finds the matching parallelhours task, transitions it to in_progress, and starts a timer.
license: "PolyForm Noncommercial 1.0.0"
compatibility: opencode
metadata:
  plugin: parallel-powers
  type: command
copyright: "Copyright (c) 2026 Parallel Hours LLC"

---

Start a tracked development session for a GitHub issue. Verifies git state, creates (or finds) the matching parallelhours task, transitions it to in_progress, and starts a timer.

## Arguments

`$ARGUMENTS` — optional GitHub issue number. If provided, skip the issue selection prompt. If omitted, prompt the user to pick an open issue or create a free-form task.

Examples:
- `/parallel-powers:session-start 49`
- `/parallel-powers:session-start`

## Steps

### 0 — Pre-flight checks

#### 0a — Branch check
Run `git rev-parse --abbrev-ref HEAD` to get the current branch.

If the current branch is **not** `main`, tell the user:
> "You are on branch `<branch>`, not `main`. How would you like to proceed?"

Present these options and wait for a choice:
1. **Switch to main now** — run `git checkout main`, then continue (only offer this if the working tree is clean — see 0b)
2. **Continue on this branch** — skip branch switching and proceed with the current branch
3. **Abort** — stop here and do nothing

#### 0b — Working tree check
Run `git status --porcelain` to check for uncommitted changes (staged or unstaged files).

If the output is **non-empty**, tell the user:
> "Your working tree has uncommitted changes. How would you like to proceed?"

Present these options and wait for a choice:
1. **Stash changes** — run `git stash push -m "stash before starting issue #N"` (use the issue number once known, or `"stash before session-start"` if not yet known), then continue
2. **Continue anyway** — leave changes in place and proceed (the feature branch will include them)
3. **Abort** — stop here and do nothing

Run both checks before any GitHub or parallelhours API calls. If either results in **Abort**, stop immediately.

---

### 1 — Resolve the issue number

**If `$ARGUMENTS` was provided**, use that as the issue number and skip to step 2.

**If no argument was provided:**
  - Run `gh issue list --state open --json number,title,labels,milestone --limit 30`
  - Display the results as a numbered list in this format:
    ```
    Open issues:
      #57  [bug, priority-high, story-points-2]       Nav bar doesn't collapse on mobile
      #46  [feature, priority-medium, story-points-3]  get_task_kpis MCP tool
      ...
    ```
    Group by milestone if present; show unlabelled/no-milestone issues last.
  - Ask: "Which issue would you like to work on or would they like to do a free-form task? (enter the issue number)"
  - Use the entered number as the issue number going forward.

**If user wants to work on a free-form task:**
- Ask the following
  * What type of task is it (`feature`, `bug`, `spike`, `chore`): `$TASK_TYPE`
  * A brief description of the task: `$TASK_DESC`
  * Human Estimate Hours: `$TASK_HUMAN`
  * Story Points: `$TASK_POINTS`
  * Priority: `$TASK_PRIORITY`
  * Will AI be used: `$TASK_USE_AI`

- Create the github issue, this will be `$ISSUE_NUMBER`
- **title** → `$TASK_DESC` (in summary form if it is long)
- **body** → `$TASK_DESC` (enhance if possible)
- **labels** → extract:
  - `story_points`: label matching `story-points-$TASK_POINTS` → integer N (null if none)
  - `task_type`:  label from `$TASK_TYPE` that is one of `feature`, `bug`, `spike`, `chore` (default `feature`)
  - `priority`: label from `$TASK_PRIORITY` matching `priority-high` → `high`, `priority-medium` → `medium`, `priority-low` → `low` (default `medium`)
- **milestone** → note it for context but do not store

**Assign the issue to me:**
- If the github issue is not already assigned to me, assign it now

---

### 2 — Fetch the GitHub issue
Run `gh issue view <number> --json number,title,body,labels,milestone,assignees` and parse:
- **title** → task title
- **body** → use as description; if the body contains a section starting with "## Acceptance Criteria" or "**Acceptance Criteria**", extract it separately into `acceptance_criteria`; put the rest into `description`
- **labels** → extract:
  - `story_points`: first label matching `story-points-N` → integer N (null if none)
  - `task_type`: first label that is one of `feature`, `bug`, `spike`, `chore` (default `feature`)
  - `priority`: first label matching `priority-high` → `high`, `priority-medium` → `medium`, `priority-low` → `low` (default `medium`)
- **milestone** → note it for context but do not store

---

### 3 — Create the feature branch

Derive the branch name from the issue:
- **type**: map `task_type` → `feat` (feature), `fix` (bug), `spike` (spike), `chore` (chore)
- **issue-id**: the issue number, e.g. `63`
- **description**: issue title lowercased, spaces replaced with hyphens, non-alphanumeric characters (except hyphens) removed, truncated to 40 characters

Branch format: `<type>/<issue-id>-<description>`

Examples:
- bug #64 "Project KEY uniqueness should be per-user" → `fix/64-project-key-uniqueness-per-user`
- feature #49 "Task linking — link task to GitHub Issue" → `feat/49-task-linking-link-task-to-github-issue`
- chore #12 "Update dependencies" → `chore/12-update-dependencies`

Run `git checkout -b <branch-name>`.
If the branch already exists, check it out with `git checkout <branch-name>` and note this to the user.

---

### 4 — Find or create the parallelhours task
Call `list_tasks(project_key="TIMEKPI")` and search results for a task whose title closely matches the issue title OR whose description references the issue number.

**If a matching task is found:**
- Note its `task_id` and current `status`
- If status is already `in_progress` or `in_review`, confirm with the user before proceeding
- Skip to step 5

**If no matching task exists:**
- Call `create_task` with:
  - `project_key`: `"TIMEKPI"`
  - `title`: issue title (prefix with `#N: ` where N is the issue number, e.g. `#49: Task linking — link task to GitHub Issue`)
  - `description`: extracted description + a line at the top: `GitHub Issue: https://github.com/parallelhours/powers/issues/N`
  - `acceptance_criteria`: extracted acceptance criteria (empty string if none found)
  - `story_points`: parsed value or omit if null
  - `task_type`: parsed value
  - `priority`: parsed value
- Note the returned `task_id`

---

### 5 — Transition to in_progress
Call `update_task(task_id=<task_id>, status="in_progress")`.
If this returns a 409 (invalid transition), the task may already be in a later state — report this to the user and ask how to proceed.

---

### 6 — Start the timer
Call `start_timer(task_id=<task_id>, notes="Starting #N: <issue title>")`.
Note the returned `timer_id` and `session_id`.

---

### 6b — Persist session state
Write the following JSON to `.session.json` at the repo root:

```json
{
  "task_id": "<task_id>",
  "timer_id": "<timer_id>",
  "session_id": "<session_id>",
  "issue_number": <N>,
  "issue_title": "<issue title>",
  "branch": "<branch-name>",
  "started_at": "<ISO-8601 timestamp>"
}
```

This file lets `session-end` stop the correct timer without disambiguation, and lets subagents link their timers to this session. It is gitignored.

---

### 7 — Report
Print a clear summary:
```
Session started
  Task:    TIMEKPI-XXX — <title>
  Issue:   #N (https://github.com/parallelhours/powers/issues/N)
  Branch:  <branch-name>
  Timer:   <timer_id>
  Session: <session_id>
  Status:  in_progress

Stop with: /parallel-powers:session-end
```

---

## Subagent timer pattern

When the main agent dispatches parallel subagents (via `superpowers:dispatching-parallel-agents`), each subagent should track its own time so overlapping AI work is captured correctly.

**Main agent responsibility — include in every subagent prompt:**
```
Time tracking context:
  task_id:    <task_id>
  session_id: <session_id>

At the START of your work, call:
  start_timer(task_id="<task_id>", session_id="<session_id>", notes="Subagent: <what you're doing>")
  → capture the returned timer_id

At the END of your work, call:
  stop_timer(timer_id=<your_timer_id>, prompt_count=<prompts you used>)
  log_ai_event(timer_id=<your_timer_id>, prompt_count=<prompts>, mode="delegated",
               model_id="claude-sonnet-4-6", estimated_ai_min=<your elapsed minutes>,
               notes="Subagent: <what you did>")
```

The backend supports concurrent timers — subagent timers can overlap with each other and with the main timer. The KPI engine uses interval union for wall time and treats concurrent AI work as a concurrency bonus, not double-counting.
