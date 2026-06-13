---
name: session-end
description: End the current tracked development session. Stops the active timer, logs AI usage, pushes the branch, and transitions the task to the appropriate status.
disable-model-invocation: true
license: "PolyForm Noncommercial 1.0.0"
compatibility: claude, opencode
metadata:
  plugin: parallel-powers
  type: command
copyright: "Copyright (c) 2026 Parallel Hours LLC"

---

End the current tracked development session. Stops the active timer, logs AI usage, pushes the branch, waits for CI, and transitions the task to the appropriate status.

## Arguments

`$ARGUMENTS` may contain any combination of:
- `done` or `in_review` — final task status (default: `in_review`)
- `not autonomous` — override autonomous mode and prompt for manual session details

Examples:
- `/parallel-powers:session-end` → autonomous, in_review
- `/parallel-powers:session-end done` → autonomous, done
- `/parallel-powers:session-end not autonomous` → manual input, in_review
- `/parallel-powers:session-end done not autonomous` → manual input, done

## Mode detection

Parse `$ARGUMENTS`:
- `autonomous_mode = True` unless `$ARGUMENTS` contains `not autonomous`
- `target_status = "done"` if `$ARGUMENTS` contains `done`, else `"in_review"`

---

## Steps

### 1 — Find the active timer

#### 1a — Check session state file first
Read `.session.json` from the repo root.

**If the file exists:** extract `timer_id`, `task_id`, `issue_number`, `issue_title`, `branch`, `session_id`. Use these values directly — skip `get_active_timers()` and any disambiguation prompt. Confirm the values to the user:
```
Resuming session from .session.json
  Task:   <task_id> — <issue_title>
  Timer:  <timer_id>
  Branch: <branch>
```

**If the file does not exist:** fall through to step 1b.

#### 1b — Fallback: discover via API
Call `get_active_timers()`.

**If no timers are running:** report "No active timers found. (No .session.json either.)" and stop.

**If exactly one timer:** use it automatically. Note `timer_id`, `task_id`, `task_title`, and `elapsed_minutes`.

**If multiple timers are running:** list them and ask the user which one to stop. Show: task_id, task_title, elapsed_minutes for each.

---

### 2 — Gather session details

#### Autonomous mode (default)
Skip all prompts. All AI usage data is captured by hooks:
- **prompt_count**: already auto-incremented on the timer by the `UserPromptSubmit` hook — pass `0` to `stop_timer` (backend uses accumulated count)
- **estimated_ai_min**: full `elapsed_minutes` (session was fully AI-driven)
- **model_id**: `claude-sonnet-4-6` (current model, known at invocation time)
- **mode**: `delegated`
- **notes**: `"auto-logged by session-end"`

#### Manual mode (`not autonomous`)
Ask the user in a single prompt:
- **Prompt count**: "How many AI prompts were used this session?" (integer, required)
- **Estimated AI minutes**: "Roughly how many minutes did AI work autonomously?" (integer, optional — press enter to skip)
- **Notes**: "Any session notes to record?" (free text, optional — press enter to skip)

Determine mode: `"delegated"` if `estimated_ai_min` was provided and > half of `elapsed_minutes`, otherwise `"assisted"`.

---

### 3 — Stop the timer (with LOC capture)

**Autonomous:** 
`stop_timer(timer_id=<timer_id>, prompt_count=0, notes="auto-logged by session-end", loc_added=<lines_or_null>, loc_deleted=<lines_or_null>)`

**Manual:** 
`stop_timer(timer_id=<timer_id>, prompt_count=<count>, notes=<notes or "">, loc_added=<lines_or_null>, loc_deleted=<lines_or_null>)`

**LOC Parameters (new):**
- `loc_added` — Lines of code added in this session (optional, integer, or null)
- `loc_deleted` — Lines of code deleted/refactored in this session (optional, integer, or null)
- When MCP is used in a git repository, LOC is auto-captured via `git diff --numstat` if not provided
- In the web UI, LOC fields are optional manual inputs
- Human and AI LOC are tracked separately by `driver` field; AI Productivity metrics only count AI agent LOC

Note the returned `duration_minutes` and `loc_added`/`loc_deleted` confirmation.

**If LOC is null/missing:** auto-capture requires the MCP process to have been running since timer start (in-memory SHA state). If the process restarted mid-session, LOC won't be captured automatically. In that case, get the diff from the PR or `git diff --numstat` and call `patch_time_entry(timer_id=<timer_id>, loc_added=<n>, loc_deleted=<n>)` after stopping.

After a successful stop, delete `.session.json` if it exists (`rm -f .session.json`).

---

### 3b — Recompute focus score

Call `get_focus_score()` (no arguments, defaults to today).

This triggers a recompute of today's focus score from all TimeEntry data logged during the session, so the coaching dashboard reflects the session that just ended. Note the returned `score` and `qualifying_focus_minutes` for the report in step 7.

---

### 3c — Log AI event

**Autonomous:**
Call `log_ai_event` with:
- `timer_id`: the stopped timer
- `prompt_count`: `0` (hooks tracked it)
- `estimated_ai_min`: `duration_minutes` (full session was autonomous)
- `ai_tool`: `"claude"`
- `mode`: `"delegated"`
- `model_id`: `"claude-sonnet-4-6"`
- `notes`: `"auto-logged by session-end"`

**Manual (if prompt_count > 0):**
Call `log_ai_event` with:
- `timer_id`: the stopped timer
- `prompt_count`: count from step 2
- `estimated_ai_min`: value from step 2 (omit if not provided)
- `ai_tool`: `"claude"`
- `mode`: determined in step 2
- `notes`: same notes as step 3

---

### 4 — Transition task status
Call `update_task(task_id=<task_id>, status=<target_status>)`.
If this returns a 409 (invalid transition), report the error and ask the user what status to use instead.

---

### 5 — Push branch and open PR
Run `git push -u origin <current-branch>` to push the branch.

Then create a PR with `gh pr create` using:
- `--title`: the task title (without the TIMEKPI-XXX prefix)
- `--body`: include Summary (bullet points of what changed), Test plan checklist, and a "Closes #N" line for the GitHub issue
- Do NOT merge — leave it open for review

Note the returned PR URL.

---

### 6 — Wait for CI

Tell the user how to check the CI (do NOT wait for the CI yourself): \
 User, run: `gh run list --branch <current-branch> --limit 1` to get the latest CI run ID. \
 Once a run ID is found, call `gh run watch <run-id> --exit-status` to stream CI progress and wait for completion. \
 If the CI failed, run: `gh run view <run-id> --web` \
 Let me know the errors or fix them on your own.

---

### 7 — Report (with AI productivity metrics)
Print a clear summary:
```
Session ended
  Task:       TIMEKPI-XXX — <title>
  Duration:   <duration_minutes> min
  Prompts:    auto-tracked  (or <count> if manual)
  AI min:     <duration_minutes> min delegated  (or manual values)
  Model:      claude-sonnet-4-6  (autonomous) / not logged  (manual, if skipped)
  Code:       +<loc_added> -<loc_deleted> LOC (or "not tracked" if unavailable)
  Speedup:    <ai_speedup_ratio>x  (or "no estimate" if task not estimated)
  Focus:      <score>/10 (<qualifying_focus_minutes> qualifying min today)
  Status:     <new_status>
  Branch:     pushed
  PR:         <pr-url>
  CI:         ✓ passed  (or ✗ failed — <run-url>)
```

**New fields (AI Productivity Metrics):**
- **Code** — Lines of code added and deleted during this session (auto-captured if MCP in git repo, or manual input). Only AI agent LOC is attributed to AI Productivity.
- **Speedup** — Sequential AI productivity ratio (estimate ÷ wall-clock minutes). Null if task has no estimate. Shows how much faster the task completed versus the human estimate.

If `status` is `done`, also show: "Task complete. Remember to merge the PR and close GitHub issue #N."
