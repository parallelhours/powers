---
created: 2026-05-08
updated: 2026-05-08
labels: [howto, issues, agile, labels, setup]
description: How to set up agile issue labels in GitHub for a new project.
tags: [issues, labels, agile, github, setup, configuration]
audience: [developers, project-managers, agents]
status: draft
version: 0.1.0
applies-to: [projects using issue tracking]
copyright: "Copyright (c) 2026 Parallel Hours LLC"
license: "PolyForm Noncommercial 1.0.0"

---

# Set Up Issue Labels

This guide walks through configuring agile issue labels for a new project.

> **Prerequisites**: Record the issue tracker in `agent-docs/12-metadata/project.yml`.

For the full label schema, see `agent-docs/04-reference/issue-labels.md`.

## GitHub (Default)

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
3. Set the name, color hex, and description from the label schema

## Record the Issue Tracker in Project Metadata

After setup, update `agent-docs/12-metadata/project.yml`:

```yaml
issue-tracking:
  provider: github
  repository: "owner/repo"
  issue-labels:
    story-points-prefix: "story-points-"
    human-estimate-prefix: "human-estimate-hours-"
    ai-estimate-prefix: "ai-estimate-hours-"
```

## See Also

- [Issue labels reference](../04-reference/issue-labels.md) — Full label schema
- [Project metadata](../12-metadata/project.yml) — Project-level configuration
