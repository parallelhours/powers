---
name: diataxis-refresh
description: >
  Refresh stale Diátaxis agent-docs after code changes, architectural decisions, or sprint completion.
  Use when agent-docs/ exists but may be out of date, when the user asks to "update docs",
  "refresh the diataxis", or "sync docs with code". Also use after resolving TBD design decisions
  or adding new services/components. Requires existing agent-docs/ created by diataxis-install.
license: "PolyForm Noncommercial 1.0.0"
compatibility: opencode
metadata:
  plugin: parallel-powers
  type: command
  requires:
    - agent-docs/ (from diataxis-install)
copyright: "Copyright (c) 2026 Parallel Hours LLC"
---

Refresh and synchronize the project's Diátaxis `agent-docs/` with the current state of the codebase. Identifies stale docs, resolves TBD markers where design has settled, updates architecture views, adds new ADRs for significant decisions, and extends the glossary.

## Arguments

`$ARGUMENTS` — optional scope limiter. Defaults to full refresh.

| Argument | Effect |
|----------|--------|
| _(none)_ | Full refresh — all stale areas |
| `architecture` | Only architecture views (subsystems, components, runtime) |
| `adr` | Only scan for new architectural decisions needing ADRs |
| `glossary` | Only extend the glossary from new code |
| `personas` | Only refresh persona pain points / how-we-help |
| `--since <date>` | Override staleness check — treat everything since date as changed |

## Pre-flight: Is This the Right Command?

```
agent-docs/ exists?  → YES → continue
                      NO  → suggest /parallel-powers:diataxis-install
```

## Phase 0: Bootstrap Template Drift Check

Before assessing code staleness, check whether the **bootstrap templates themselves** have been updated since this project was installed. Newer plugin versions may have improved skeleton files, new diagram conventions, or additional personas.

### 0.1 Read Install Provenance

```bash
# Get the installed version and date from project.yml
grep -A4 "diataxis-bootstrap:" agent-docs/12-metadata/project.yml
```

Expected output:
```yaml
diataxis-bootstrap:
  installed: "2026-05-21"
  plugin-version: "1.0.0"
  bootstrap-path: "/Users/you/.claude/plugins/cache/parallel-powers/parallel-powers/1.0.0/agent-docs-bootstrap"
```

If `diataxis-bootstrap:` is missing from `project.yml`, the project was bootstrapped before provenance tracking was introduced. Note this in the report — template drift cannot be assessed.

### 0.2 Find the Current Bootstrap

```bash
# Current installed bootstrap (highest version)
CURRENT=$(ls -d ~/.claude/plugins/cache/parallel-powers/parallel-powers/*/agent-docs-bootstrap 2>/dev/null | sort -V | tail -1)
CURRENT_VERSION=$(echo "$CURRENT" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
echo "Installed at bootstrap: $INSTALLED_VERSION  |  Current: $CURRENT_VERSION"
```

### 0.3 Compare Template Files

If versions differ, or if `installed` date is older than the most recent `updated:` date in any bootstrap template file:

```bash
# Find bootstrap template files newer than the install date
INSTALLED_DATE=$(grep "installed:" agent-docs/12-metadata/project.yml | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
find "$CURRENT" -name "*.md" -newer <(date -d "$INSTALLED_DATE" +%Y%m%d 2>/dev/null || date -j -f "%Y-%m-%d" "$INSTALLED_DATE" +%Y%m%d) 2>/dev/null
```

### 0.4 Template Drift Report

Include in the Phase 2 staleness report:

```
### Bootstrap Template Status
Installed version:  1.0.0  (2026-05-21)
Current version:    1.2.0  (plugin updated)
Status: DRIFT DETECTED

Changed templates since install:
  - 12-metadata/diagrams.md       → updated diagram conventions
  - 13-personas/index.md          → new persona structure
  - 03-howto/setup-issue-labels.md → new label types added

Recommendation: Review changed templates and decide whether to
pull updates into this project's agent-docs/ manually.
Template updates are NEVER applied automatically — they require
human review because your project has customized these files.
```

If no drift:
```
### Bootstrap Template Status
Installed version:  1.0.0  (2026-05-21)
Current version:    1.0.0
Status: UP TO DATE — no template changes since install
```

> **Template updates are never applied automatically.** The project's `agent-docs/` files have been customized — a blind overwrite would destroy that work. Present the diff, let the human decide.

## Phase 1: Staleness Assessment

### 1.1 Find the Last Update Baseline

```bash
# Find the most recent updated: date across all doc files
grep -r "^updated:" agent-docs/ | sort -t: -k2 -r | head -5

# Compare against recent git commits
git log --oneline --since="$(grep -r '^updated:' agent-docs/ | \
  sort -t: -k2 -r | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')" \
  --name-only | head -60
```

### 1.2 Identify Changed Areas

Build a staleness map from the git log. Categorize changes:

| Changed Area | Docs Likely Stale |
|-------------|-------------------|
| New service directory or Dockerfile | architecture-subsystems, architecture-components |
| New database table or migration | architecture-components (ER diagram), glossary |
| New REST endpoint | architecture-runtime (sequence diagrams), CLI reference |
| Changed service-to-service call | architecture-runtime |
| New config key / env var | config-schema reference |
| Significant refactor | ADR candidate |
| TBD comment removed from code | TBD tracker (see Phase 2) |

### 1.3 Scan for Resolved TBDs

```bash
# Find all TBD markers in agent-docs
grep -rn "TBD" agent-docs/ --include="*.md" -l

# Check if those items now have answers in code
# (e.g., lifecycle_state values defined, sweep interval in config)
```

For each TBD found: check if the codebase or recent commits have resolved it. If yes, flag for update.

### 1.4 Scan for New Terms

```bash
# Find domain terms in code not yet in glossary
grep -r "^updated:" agent-docs/10-glossary/index.md | \
  grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}'
# Then scan for new domain concepts introduced since that date
```

## Phase 2: Staleness Report

Before making changes, present a summary to the user:

```
## Staleness Assessment

Last doc update: YYYY-MM-DD
Commits since then: N

### Stale Areas
- architecture-components.md — new service `X` added (commit abc1234)
- architecture-runtime.md — new sequence for `Y` endpoint
- glossary — 3 new domain terms found: foo, bar, baz

### Resolved TBDs
- lifecycle_state field values — values found in models/usage.py
- Sweep interval — found SWEEP_INTERVAL_SECONDS in config.py

### ADR Candidates
- Decision to use Alembic for migrations (commit def5678)
- Switch from REST to gRPC for internal service calls

### No Change Needed
- architecture-subsystems.md — subsystem boundaries unchanged
- personas — no structural changes to roles
```

Ask: **"Proceed with full refresh, or select specific areas?"**

## Phase 3: Execute Refresh

Run only for stale areas confirmed in Phase 2.

### Architecture Views

**Subsystems** (`architecture-subsystems.md`):
- Add new subsystem blocks if new services added
- Update interface table if service boundaries changed
- Regenerate Mermaid `graph TB` to reflect current topology

**Components** (`architecture-components.md`):
- Update `erDiagram` with new tables, columns, or relationships
- Update ASCII service tree if new packages added
- Add new external dependencies if introduced

**Runtime** (`architecture-runtime.md`):
- Add `sequenceDiagram` blocks for new critical flows
- Update existing sequences if call patterns changed
- Flag deprecated flows for removal

### Resolve TBD Markers

For each resolved TBD found in Phase 1:

1. Find the `> **TBD:**` block in the relevant doc
2. Replace with the settled answer
3. Update the `updated:` frontmatter date
4. Create an ADR if the resolution was a non-obvious decision

### New ADRs

For each ADR candidate identified:

Create `agent-docs/01-explanation/decisions/ADR-NNN-<slug>.md`:

```yaml
---
created: [today]
updated: [today]
labels: [architecture, decisions]
description: [One-line decision statement]
tags: [adr, architecture]
audience: [architects, developers, agents]
status: draft
version: 0.1.0
---

# ADR-NNN: [Title]

## Status
Accepted

## Context
[What situation made this decision necessary?]

## Decision
[What was decided?]

## Consequences
[What are the trade-offs? What becomes easier or harder?]
```

### Glossary Extension

For each new domain term found:

```markdown
## <Term>

<One-sentence definition.>

**Used in:** `<service-or-file>` | **Related:** [[existing-term]]
```

Update the `updated:` date in `agent-docs/10-glossary/index.md`.

### CLAUDE.md

Refresh only if:
- A new service was added (update Services list)
- A key convention changed (update Key Conventions)
- Dev commands changed (update commands block)

Keep CLAUDE.md **sparse** — every line costs tokens in every session.

## Phase 4: Frontmatter Audit

After all edits, update `updated:` dates on every modified file to today:

```bash
# Verify all modified files have updated frontmatter
grep -rL "^updated:" agent-docs/ --include="*.md"
```

Any file missing `updated:` gets it added.

## Phase 5: Refresh Summary

```
## Refresh Complete

### Bootstrap Template Status
Installed: 1.0.0 (2026-05-21) | Current: 1.2.0 | Status: DRIFT DETECTED
Changed templates: diagrams.md, 13-personas/index.md
→ Review changes manually before pulling into agent-docs/

### Updated
- architecture-components.md — added `usage_events` table to ER diagram
- architecture-runtime.md — added sequence for audit replay flow
- ADR-005-alembic-migrations.md — created
- glossary — added: lifecycle_state, sweep_cycle, audit_replay

### Resolved TBDs
- lifecycle_state values: now documented (pending, active, paused, deleted)
- Sweep interval: SWEEP_INTERVAL_SECONDS=300 (5 minutes)

### Still TBD (no resolution found in code)
- Certificate Authority choice for mTLS (ADR-002)
- Report output format

### No Change Needed
- architecture-subsystems.md (boundaries stable)
- Personas (role structure unchanged)

### Recommended Next Actions
- Review ADR-005 for accuracy
- File an issue for CA choice (ADR-002 still open)
- Review 2 changed bootstrap templates for relevant improvements
```

## When to Refresh

| Trigger | Scope |
|---------|-------|
| After each sprint | Full refresh |
| After adding a new service | `architecture` |
| After schema migration | `architecture`, `glossary` |
| After resolving a TBD design decision | Targeted update + ADR if needed |
| Before creating a PR for a major feature | `adr` + `architecture` |
| After onboarding a new team member who asks "where is X documented?" | Full refresh — it's stale |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Refreshing without checking git log first | Always run Phase 1 staleness assessment before writing |
| Updating every file even when nothing changed | Only update files with actual changes; stale `updated:` dates are misleading |
| Inventing resolutions for still-open TBDs | Only mark TBD resolved when evidence is in the code |
| Bloating CLAUDE.md during refresh | CLAUDE.md is load-on-every-session; keep additions minimal |
| Creating redundant ADRs for trivial decisions | ADRs are for non-obvious decisions with lasting consequences |
| Skipping the staleness report | User deserves to know what changed before you write 15 files |
