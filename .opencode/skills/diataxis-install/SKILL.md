---
name: diataxis-install
description: >
  Bootstrap a Diátaxis agent-docs structure for a new or undocumented project.
  Use when a project has no agent-docs/ directory, when starting a greenfield project,
  or when the user asks to "set up docs", "bootstrap documentation", or "initialize diataxis".
  Runs an interview to gather project context, then executes all installer phases.
license: "PolyForm Noncommercial 1.0.0"
compatibility: opencode
metadata:
  plugin: parallel-powers
  type: command
  requires:
    - agent-docs-bootstrap (parallel-powers)
copyright: "Copyright (c) 2026 Parallel Hours LLC"
---

Bootstrap the Diátaxis documentation framework for a project. Runs a structured interview to capture project context, then executes the full installer to produce architecture docs, personas, ADRs, glossary, tutorials, and `CLAUDE.md`.

## Arguments

`$ARGUMENTS` — optional path to the target project. Defaults to the current working directory.

```
/parallel-powers:diataxis-install
/parallel-powers:diataxis-install /path/to/project
```

## Locating the Bootstrap

The `agent-docs-bootstrap/` directory ships with the parallel-powers plugin. Locate it before executing any phases:

```bash
# Standard plugin cache location (Claude Code)
BOOTSTRAP=$(ls -d ~/.claude/plugins/cache/parallel-powers/parallel-powers/*/agent-docs-bootstrap 2>/dev/null | sort -V | tail -1)

# Fallback: local dev clone
[ -z "$BOOTSTRAP" ] && BOOTSTRAP=$(find ~/projects -maxdepth 3 -name "agent-docs-bootstrap" -type d 2>/dev/null | head -1)

echo "Bootstrap: $BOOTSTRAP"
```

If no bootstrap is found, stop and tell the user: the parallel-powers plugin must be installed before running this skill.

Once found, read the full installer spec before executing phases:

```
$BOOTSTRAP/installer.md
```

Record the resolved bootstrap path and the plugin version (from the path segment) — both will be stored in `project.yml` so `/parallel-powers:diataxis-refresh` can detect template drift later.

## Phase 0: Pre-flight Check

Before the interview, check what already exists:

```bash
ls agent-docs/ 2>/dev/null && echo "EXISTS" || echo "MISSING"
cat CLAUDE.md 2>/dev/null | head -20
cat .mcp.json 2>/dev/null
```

If `agent-docs/` already exists with content, warn the user and confirm they want to overwrite or extend. Offer:
- **Extend** — add missing files, skip existing ones
- **Overwrite** — fresh bootstrap (destructive)
- **Cancel** — run `/parallel-powers:diataxis-refresh` instead

## Phase 1: Interview

Ask the user for project context. Gather answers before writing any files. Cover all sections below — but adapt to what you can already infer from the codebase (skip questions you can answer from code).

### Required: Project Identity

```
1. Project name and one-sentence description
   (What problem does it solve? Who uses it?)

2. Primary language / runtime
   (e.g., Python 3.12, TypeScript / Node 22, Go 1.23)

3. Primary framework (if any)
   (e.g., FastAPI, Next.js 14, Gin, none)
```

### Required: Architecture

```
4. What are the main services or components?
   (List them — e.g., "API server", "background worker", "CLI tool")

5. What datastores does it use?
   (e.g., PostgreSQL, Redis, S3, none)

6. What external services or APIs does it call?
   (e.g., Stripe, SendGrid, GitHub API, none)
```

### Required: Constraints and Conventions

```
7. What are the 3-5 most important architectural rules or constraints?
   (Things every developer working here must know)

8. Are there any active TBD / in-progress design decisions?
   (Things that are not yet settled — so docs can flag them honestly)
```

### Optional: Integrations

```
9. Issue tracking: GitHub, Jira, parallelhours, or none?
   (If GitHub: owner/repo — if none, skip label setup)

10. Time tracking: parallelhours.io?
    (Check .mcp.json — if TKPI_PROJECT is set, infer the project key)
```

### Infer What You Can

Before asking, scan the codebase for obvious answers:
- Language → check file extensions, `package.json`, `pyproject.toml`, `go.mod`
- Framework → check imports, config files
- Datastores → check docker-compose, `.env.example`, connection strings
- Services → check `docker-compose.yml`, `Dockerfile.*`, directory names
- Time tracking → check `.mcp.json` for parallelhours config

Only ask about things you cannot confidently infer.

## Phase 2: Execute Installer

After the interview, execute the full installer from `agent-docs-bootstrap/installer.md`. Run the phases in order:

| Phase | What it does |
|-------|-------------|
| **Phase 0** | Copy all skeleton files from `agent-docs-bootstrap/` |
| **Phase 1** | Create `CLAUDE.md`, `AGENTS.md`, architect persona, `project.yml` |
| **Phase 2** | Architecture deep dive: subsystems, components, runtime views |
| **Phase 3** | Remaining personas, glossary, ADRs, tutorial/howto outlines |
| **Phase 4** | Validation — frontmatter, diagram syntax, link consistency |
| **Phase 5** | Optional: time tracking, superpowers integration |

**Spawn a subagent for Phase 2 onward.** The volume of files created (40+) will consume the main context window. Pass the full interview answers and the resolved `$BOOTSTRAP` path as project context.

### Bootstrap Provenance (required in project.yml)

Phase 1 must record bootstrap provenance in `agent-docs/12-metadata/project.yml`:

```yaml
diataxis-bootstrap:
  installed: "YYYY-MM-DD"           # today
  plugin-version: "1.0.0"           # version segment from the cache path
  bootstrap-path: "/absolute/path"  # resolved $BOOTSTRAP path
```

This is the anchor used by `/parallel-powers:diataxis-refresh` to detect when bootstrap templates have been updated since install.

### CLAUDE.md Conventions

Keep CLAUDE.md **sparse** — it is loaded into every session. Token costs compound.

- One paragraph description
- Language / datastores / services (3-5 bullets max)
- Key architectural constraints (5 lines max)
- Dev commands block (even if TBD)
- Link to `agent-docs/` for everything else

### Flagging TBD Items

Where design is in progress (per interview question 8), be honest in docs:

```markdown
> **TBD:** The `lifecycle_state` field values are still being designed.
```

Do not invent settled answers for unsettled design decisions.

## Phase 3: Post-Install Summary

After the subagent completes, report back:

```
## Bootstrap Complete

### Files Created
- agent-docs/  (N files across 14 directories)
- CLAUDE.md
- AGENTS.md

### Architecture Docs
- architecture-subsystems.md — [brief summary]
- architecture-components.md — [brief summary]
- architecture-runtime.md — [brief summary]

### ADRs Created
- ADR-001: [title]
- ADR-002: [title]

### Items Needing Human Review (TBD)
- [List any design decisions flagged as in-progress]

### Next Steps
- Review CLAUDE.md for accuracy
- Run /parallel-powers:diataxis-refresh after first sprint of code changes
- File GitHub issues for TBD design decisions
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Asking every interview question even when code makes it obvious | Infer from codebase first; only ask what you can't determine |
| Writing dense CLAUDE.md | Keep it under 50 lines; link to agent-docs/ for detail |
| Inventing settled answers for unsettled design | Use `> **TBD:**` blocks honestly |
| Creating architecture docs before gathering requirements | Interview first, write second |
| Forgetting to flag parallelhours in project.yml | Always check `.mcp.json` — if it's there, include it |
