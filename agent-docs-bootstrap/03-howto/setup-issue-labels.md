---
created: 2026-04-06
updated: 2026-04-06
labels: [howto, issues, agile, labels, setup]
description: How to set up agile issue labels in GitHub, Jira, or parallelhours.io for a new project.
tags: [issues, labels, agile, github, jira, setup, configuration]
audience: [developers, project-managers, agents]
status: active
version: 1.0.0
applies-to: [projects using issue tracking]
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# Set Up Issue Labels

This guide walks through configuring agile issue labels for a new project. Choose the section for your issue tracker.

> **Prerequisites**: Decide which issue tracker the project will use and record it in `agent-docs/12-metadata/project.yml` under the `issue-tracker` key before starting.

For the full label schema and valid values, see `agent-docs/04-reference/issue-labels.md`.

---

## GitHub (Default)

GitHub labels are free-text strings. You must create them once per repository.

### Option A: GitHub CLI (Recommended)

Install the [GitHub CLI](https://cli.github.com/) and authenticate, then run:

```bash
# --- Issue Types ---
gh label create feature        --color "0075ca" --description "New capability or user-facing functionality"
gh label create bug            --color "d73a4a" --description "Defect or incorrect behavior"
gh label create design         --color "0075ca" --description "UX/UI design work, wireframes, prototypes"
gh label create documentation  --color "0075ca" --description "Docs creation or updates"
gh label create spike          --color "0075ca" --description "Time-boxed investigation or research"
gh label create chore          --color "0075ca" --description "Maintenance, dependency updates"
gh label create refactor       --color "0075ca" --description "Code restructuring without behavior change"
gh label create test           --color "0075ca" --description "Test coverage or test infrastructure"
gh label create security       --color "0075ca" --description "Security vulnerability or hardening"

# --- Priority ---
gh label create priority-high   --color "d73a4a" --description "Blocking, time-sensitive, high impact"
gh label create priority-medium --color "e4e669" --description "Important but not blocking"
gh label create priority-low    --color "0e8a16" --description "Nice-to-have or deferred"

# --- Story Points (Fibonacci) ---
gh label create story-points-1  --color "7057ff" --description "Trivial change"
gh label create story-points-2  --color "7057ff" --description "Small, straightforward"
gh label create story-points-3  --color "7057ff" --description "Small-to-medium"
gh label create story-points-5  --color "7057ff" --description "Medium complexity"
gh label create story-points-8  --color "7057ff" --description "Large — consider splitting"
gh label create story-points-13 --color "7057ff" --description "Very large — split before starting"

# --- Human Hour Estimates ---
gh label create human-estimate-hours-0.5 --color "0052cc" --description "Human estimate: 30 minutes"
gh label create human-estimate-hours-1   --color "0052cc" --description "Human estimate: 1 hour"
gh label create human-estimate-hours-2   --color "0052cc" --description "Human estimate: 2 hours"
gh label create human-estimate-hours-4   --color "0052cc" --description "Human estimate: half day"
gh label create human-estimate-hours-8   --color "0052cc" --description "Human estimate: full day"
gh label create human-estimate-hours-16  --color "0052cc" --description "Human estimate: 2 days"
gh label create human-estimate-hours-24  --color "0052cc" --description "Human estimate: 3 days"
gh label create human-estimate-hours-40  --color "0052cc" --description "Human estimate: full week"

# --- AI Hour Estimates ---
gh label create ai-estimate-hours-0.25 --color "5319e7" --description "AI-assisted estimate: 15 minutes"
gh label create ai-estimate-hours-0.5  --color "5319e7" --description "AI-assisted estimate: 30 minutes"
gh label create ai-estimate-hours-1    --color "5319e7" --description "AI-assisted estimate: 1 hour"
gh label create ai-estimate-hours-2    --color "5319e7" --description "AI-assisted estimate: 2 hours"
gh label create ai-estimate-hours-4    --color "5319e7" --description "AI-assisted estimate: half day"
gh label create ai-estimate-hours-8    --color "5319e7" --description "AI-assisted estimate: full day"
gh label create ai-estimate-hours-16   --color "5319e7" --description "AI-assisted estimate: 2 days"
```

### Option B: GitHub Web UI

1. Go to your repository → **Issues** → **Labels**
2. Click **New label** for each entry in the table above
3. Set the name, color hex, and description from `agent-docs/04-reference/issue-labels.md`

### Custom Story Point Prefix

If you use a custom prefix (e.g., `pts-` instead of `story-points-`), update `agent-docs/12-metadata/project.yml`:

```yaml
issue-labels:
  story-points-prefix: "pts-"
```

And adjust the label creation commands accordingly.

### Applying Labels to Issues

- Apply exactly **one** type label, **one** priority label per issue
- Apply story point and estimate labels during sprint planning or estimation sessions
- Agents can read and apply labels automatically if GitHub integration is configured — see `agent-docs/11-agents/time-tracking.md`

---

## Jira (Atlassian)

Jira uses structured fields rather than free-text labels. Most agile fields are built in.

### Issue Type

1. Go to **Project Settings** → **Issue Types**
2. Ensure these types exist: Bug, Story (for feature), Task (for chore/refactor/test), Spike, Design, Documentation, Security
3. Or add custom issue types matching the schema in `agent-docs/04-reference/issue-labels.md`

### Priority

Jira has Priority as a built-in field. Verify these values exist:

1. Go to **Administration** → **Issue Priorities**
2. Confirm: High, Medium, Low (map to `priority-high`, `priority-medium`, `priority-low`)

### Story Points

In Jira Software (company-managed):

1. Go to **Project Settings** → **Fields**
2. Enable **Story Points** or **Story point estimate** field on your issue screens
3. Ensure board is configured to use story points for estimation

Valid values: 1, 2, 3, 5, 8, 13 (Fibonacci — no label required, entered as a number)

### Human Estimate

Jira's built-in time tracking covers this:

1. Go to **Project Settings** → **Time Tracking**
2. Enable time tracking on the project
3. Use **Original Estimate** field for human-only estimates
4. Enter values as hours: `1h`, `2h`, `4h`, `8h`, etc.

### AI Estimate

Jira has no built-in AI estimate field. Add a custom field:

1. Go to **Administration** → **Issues** → **Custom Fields**
2. Create a **Number Field**: name it `AI Estimate (h)`
3. Add it to your project's issue screens
4. Enter values in hours (decimals allowed: `0.5`, `1`, `2`, etc.)

---

## parallelhours.io

parallelhours.io stores agile metadata as structured database fields, not labels. GitHub labels sync into these fields automatically when GitHub integration is enabled.

### Field Mapping

| Agile concept | Field | Type | Valid values |
|---------------|-------|------|-------------|
| Issue type | `task_type` | choice | `feature`, `bug`, `spike`, `chore` |
| Priority | `priority` | choice | `high`, `medium`, `low` |
| Story points | `story_points` | integer | 1, 2, 3, 5, 8, 13 |
| Human estimate | `estimate_human_min` | integer (minutes) | any positive integer |
| AI estimate (with AI) | `ai_estimate_human_ai_min` | integer (minutes) | auto-generated |
| AI estimate (without AI) | `ai_estimate_human_min` | integer (minutes) | auto-generated |

### GitHub → parallelhours.io Sync

If using GitHub as the issue source with parallelhours.io for time tracking:

1. Configure GitHub integration in your parallelhours.io project settings
2. Add `label_prefix` to your repository config (default: `story-points-`)
3. Labels from GitHub are parsed on sync:
   - `story-points-5` → `story_points = 5`
   - `priority-high` → `priority = "high"`
   - `feature` → `task_type = "feature"`
   - `human-estimate-hours-4` → `estimate_human_min = 240`

4. AI estimates are generated automatically by the estimation job — no manual label required

### Manual Entry

If not using GitHub, enter fields directly via the parallelhours.io UI or MCP tool:

```
create_task --title "..." --task_type feature --priority high --story_points 3 --estimate_human_min 120
```

---

## Recording the Issue Tracker in Project Metadata

After setup, update `agent-docs/12-metadata/project.yml` to record which tracker is in use:

```yaml
issue-tracking:
  provider: github           # github | jira | parallelhours | none
  repository: "owner/repo"   # GitHub only
  project-key: "PROJ"        # Jira or parallelhours project key
  issue-labels:
    story-points-prefix: "story-points-"   # GitHub only, configurable
    human-estimate-prefix: "human-estimate-hours-"
    ai-estimate-prefix: "ai-estimate-hours-"
```

---

## Related

- `agent-docs/04-reference/issue-labels.md` — Full label schema and valid values
- `agent-docs/11-agents/time-tracking.md` — How agents log time against issues
- `agent-docs/12-metadata/project.yml` — Project-level configuration
