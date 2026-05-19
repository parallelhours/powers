---
created: 2026-04-03
updated: 2026-04-06
labels: [setup, installer, agents]
description: Bootstrap script and instructions for initializing the docs kit for a new project.
tags: [setup, bootstrap, installer, initialization]
audience: [agents]
status: active
version: 1.0.0
---

# Docs Kit Installer

This document guides AI agents through initializing the docs kit for a specific project.

## Prerequisites

The agent should have read access to the codebase and understand the project structure.

## Before Starting

Review these files first:

1. `agent-docs/00-readme/` — Understand the docs kit structure
2. `agent-docs/12-metadata/file-structure.md` — Frontmatter schema
3. `agent-docs/12-metadata/diagrams.md` — Diagram conventions

> **Note**: Much of the standard documentation structure (index files, skeleton content, metadata conventions) was already copied in **Phase 0**. For steps below that reference existing files, you should customize the bootstrap copies rather than recreating them from scratch.

Also check for existing project files that may contain agent conventions:
- `CLAUDE.md` — Existing agent instructions
- `.mcp.json` — MCP server configuration (for time tracking like parallelhours)
- `.claude/commands/` — Custom slash commands (e.g., `/vault-start`, `/vault-end`)
- `.claude/hooks/` — Session hooks for automation

## Phase 0: Bootstrap Initialization

### Step 0.1: Copy Bootstrap Skeleton Files

Copy **all** template skeleton files from `agent-docs-bootstrap/` into the target project's `agent-docs/` directory. These provide the standard index pages, skeleton content files, and conventions that every docs kit project needs.

Run:

```bash
# Create the target agent-docs directory if it doesn't exist
mkdir -p agent-docs

# Copy all numbered directories and their contents (excluding installer.md)
for dir in agent-docs-bootstrap/0[0-9]-*/ agent-docs-bootstrap/1[0-3]-*/; do
  cp -r "$dir" agent-docs/
done
```

This copies every bootstrap file into the project, including:
- **Index files** for all 14 directories (`00-readme/index.md`, ..., `13-personas/index.md`)
- **Skeleton content files**: `01-explanation/architecture.md`, `01-explanation/decisions.md`, `02-tutorial/getting-started.md`, `03-howto/installation.md`, `04-reference/cli.md`, `04-reference/config-schema.md`, `07-runbooks/deployment.md`, `08-troubleshooting/common-errors.md`, `05-plans/roadmap.md`, `06-environment/setup.md`
- **Metadata standards**: `12-metadata/index.md`, `12-metadata/diagrams.md`, `12-metadata/file-structure.md`

**Important**: Do NOT copy `installer.md` itself into the target project. It stays in `agent-docs-bootstrap/`.

> **Why this step?** The bootstrap templates contain standardized frontmatter, diagram conventions, file structure guidelines, and skeleton content. Previously, agents had to recreate these from inline templates — which was error-prone and led to missing files. Copying from the bootstrap ensures consistency across all docs kit projects.

### Step 0.2: Add Frontmatter to Copied Files

Each copied bootstrap file needs frontmatter added. For every `.md` file in the target `agent-docs/` directory, add standard YAML frontmatter:

```yaml
---
created: [current date YYYY-MM-DD]
updated: [current date YYYY-MM-DD]
labels: [category, subcategory]
description: [One-line description of the file]
tags: [tag1, tag2]
audience: [agents, humans]
status: draft
version: 0.1.0
---
```

Use the existing frontmatter in parallel-powers' own `agent-docs/` files as a reference. Each directory's files should have appropriate labels and tags (e.g., `labels: [readme, overview]` for 00-readme, `labels: [explanation, architecture]` for 01-explanation).

## Phase 1: Project Grounding

### Step 1.1: Identify the Project

Determine the project name and primary purpose from existing code, README, or context.

### Step 1.2: Architect Deep Dive

Do a deep dive on the project architecture, then create the architect persona:

Create `agent-docs/13-personas/architect.md`:

```yaml
---
created: [date]
updated: [date]
labels: [persona, architect]
description: The architect persona for this specific project.
tags: [persona, architect, architecture]
audience: [agents]
status: draft
version: 0.1.0
---

# Persona: The Architect

**Name**: Riley  
**Role**: Solutions architect for [PROJECT NAME]  
**Experience**: [Years] years

### Project Context

[What makes architecting THIS project unique? What are the key constraints, scale, domain?]

### Goals
- [Project-specific goals]

### Pain Points
- [Project-specific pain points]

### How We Help
- [Project-specific documentation that helps Riley]
```

Riley's content should come from the deep dive into this specific project.

### Step 1.3: Create Project Metadata

The `12-metadata/` directory and its conventions (`index.md`, `diagrams.md`, `file-structure.md`) were already copied in Phase 0. Now create the project-specific metadata file:

Create `agent-docs/12-metadata/project.yml`:

```yaml
project:
  name: "[Project Name]"
  description: "[One-line description]"
  repository: "[Repo URL]"
  language: "[Primary language]"
  framework: "[Primary framework]"
  created: "[YYYY-MM-DD]"
```

### Step 1.4: Create AGENTS.md

Create or update `AGENTS.md` in the project root (or `agent-docs/AGENTS.md` if that's the convention) to inform agents about the documentation framework:

```yaml
Refer to [CLAUDE.md](./CLAUDE.md) for instructions
```

If `AGENTS.md` already exists, update it to include diataxis information. If not, create it.

### Step 1.5: Create CLAUDE.md

`CLAUDE.md` is Claude Code's primary instructions file — it is loaded automatically at the start of every Claude Code session and every time Claude is spawned as a subagent. It is the single most important file for shaping how Claude behaves in this project.

Create `CLAUDE.md` in the project root:

```markdown
# [Project Name]

[One-paragraph description of the project — what it does, who it's for, the core problem it solves.]

## Project Context

- **Language / Runtime**: [e.g., TypeScript / Node 20]
- **Framework**: [e.g., Next.js 14, FastAPI]
- **Primary Datastores**: [e.g., PostgreSQL, Redis]
- **Key External Services**: [e.g., Stripe, SendGrid]

## Documentation

This project uses the [Diátaxis documentation framework](https://diataxis.fr/). All docs live in `agent-docs/`.

## Key Conventions

- [List project-specific coding conventions, naming rules, or architectural constraints]
- [e.g., "All API routes must be versioned under /api/v1/"]
- [e.g., "Database migrations must be reversible"]

## Development Commands

    # Install dependencies
    [command]

    # Run tests
    [command]

    # Start local dev server
    [command]

    # Lint / format
    [command]

## Testing

[Describe the testing strategy — unit, integration, e2e. Note any important constraints like "never mock the database".]

```

**CLAUDE.md vs AGENTS.md:**
- `CLAUDE.md` is Claude Code-specific. It is loaded automatically and should include Claude-specific tooling notes (commands, MCP servers, hooks). It is the richer, more authoritative file for Claude.
- `AGENTS.md` is a cross-agent convention (OpenAI, etc.). Keep it for interoperability but it should point to CLAUDE.md
- Keep CLAUDE.md sparse, but knowledgeably about the diataxis. Tokens cost a lot of money unfortunately and I don't want context to be eaten up by the diataxis.

If `CLAUDE.md` already exists, extend it with the documentation structure and agent workflow sections above rather than replacing it.

### Step 1.6: Configure Issue Tracking

The issue label reference (`04-reference/issue-labels.md`) and setup guide (`03-howto/setup-issue-labels.md`) were already copied in Phase 0. Customize them as needed.

Determine which issue tracking system the project uses and record it in `agent-docs/12-metadata/project.yml`:

```yaml
issue-tracking:
  provider: github           # github | jira | parallelhours | none
  repository: "owner/repo"   # GitHub only
  project-key: "PROJ"        # Jira or parallelhours project key
  issue-labels:
    story-points-prefix: "story-points-"
    status-prefix: "status-"
    scope-prefix: "scope-"
    human-estimate-prefix: "human-estimate-hours-"
    ai-estimate-prefix: "ai-estimate-hours-"
```

**Default is GitHub.** If the project uses a different system, update `provider` accordingly.

For GitHub projects, create the standard label set now using the GitHub CLI script in `agent-docs/03-howto/setup-issue-labels.md`. Labels must be created before issues can be filed with agile metadata.

The label schema (types, priority, story points, hour estimates, status, scope) is defined in `agent-docs/04-reference/issue-labels.md`. Labels provide the following agile metadata on each issue:

- **Issue type** — `feature`, `bug`, `design`, `documentation`, `spike`, `chore`, `refactor`, `test`, `security`
- **Priority** — `priority-high`, `priority-medium`, `priority-low`
- **Status** — `status-not-started`, `status-in-progress`, `status-blocked`, `status-review`, `status-done`
- **Scope** — `scope-original` (included in sprint planning), `scope-added-sprint` (added after sprint start)
- **Story points** — `story-points-1` through `story-points-13` (Fibonacci)
- **Human estimate** — `human-estimate-hours-N` (time without AI assistance)
- **AI estimate** — `ai-estimate-hours-N` (time with AI assistance — often significantly lower)

If the project integrates with parallelhours.io, GitHub labels sync automatically into structured fields (`story_points`, `priority`, `task_type`, `estimate_human_min`).

If the project has no issue tracker (`provider: none`), skip this step.

## Phase 2: Architecture Deep Dive

The architect (Riley) performs a deep dive and creates three architecture views:

### Step 2.1: Subsystem View

Create `agent-docs/01-explanation/architecture-subsystems.md`:

```yaml
---
created: [date]
updated: [date]
labels: [architecture, subsystems]
description: High-level subsystem decomposition of the system.
tags: [architecture, subsystems, decomposition]
audience: [architects, evaluators, agents]
status: draft
version: 0.1.0
applies-to: [system]
---
```

Content:
- What are the major subsystems?
- What is each subsystem's responsibility?
- How do subsystems interact?
- What are the boundaries and interfaces?

Use Mermaid `graph TB` for subsystem diagrams.

### Step 2.2: Component View

Create `agent-docs/01-explanation/architecture-components.md`:

```yaml
---
created: [date]
updated: [date]
labels: [architecture, components]
description: Component-level architecture including databases, services, and packages.
tags: [architecture, components, database, services, packages]
audience: [architects, developers, agents]
status: draft
version: 0.1.0
applies-to: [system]
---
```

Content:
- **Databases**: What data stores exist? What data lives where?
- **Services/Packages**: What are the main packages/modules?
- **External Dependencies**: What external services/APIs are used?
- **Configuration**: How is the system configured?

Use ASCII tree for file/package structures, Mermaid ER diagrams for data models.

### Step 2.3: Runtime View

Create `agent-docs/01-explanation/architecture-runtime.md`:

```yaml
---
created: [date]
updated: [date]
labels: [architecture, runtime, sequences]
description: Runtime behavior including critical sequence flows and processes.
tags: [architecture, runtime, sequences, flows]
audience: [architects, developers, agents]
status: draft
version: 0.1.0
applies-to: [system]
---
```

Content:
- **Critical Sequences**: What are the key user/system flows?
- **Authentication Flow**: How does auth work?
- **Request Lifecycle**: How does a typical request flow through the system?
- **Event Flows**: How do async events propagate?
- **Error Handling**: How are errors handled at runtime?

Use Mermaid sequence diagrams for all runtime flows.

## Phase 3: Documentation Population

After Phase 2 architecture deep dives are complete, use the remaining personas to populate documentation:

### Step 3.1: Create Remaining Personas

> **Note**: The `13-personas/index.md` directory index was already copied in Phase 0. Remove its generic bootstrap content and replace with a proper table of contents linking to each persona.

The architect has completed the deep dive. Now create remaining personas as separate files in `agent-docs/13-personas/`:

Create each of these files with proper frontmatter:

- `agent-docs/13-personas/developer.md` — Alex, adapted for this project
- `agent-docs/13-personas/operator.md` — Jordan, adapted for this project
- `agent-docs/13-personas/evaluator.md` — Sam, adapted for this project
- `agent-docs/13-personas/project-manager.md` — Morgan, adapted for this project
- `agent-docs/13-personas/docs-author.md` — Casey, adapted for this project
- `agent-docs/13-personas/product-marketing.md` — Taylor, adapted for this project

If based on the architecture deep dives, additional personas are needed, create them.

### Step 3.2: Docs Author Creates Glossary

> **Note**: The `10-glossary/index.md` skeleton was already copied in Phase 0. Replace its generic terms with project-specific ones.

Using the **Docs Author (Casey)** persona:

Add project-specific terms to `agent-docs/10-glossary/index.md` based on the architecture. Each term should have frontmatter:

```yaml
---
created: [date]
updated: [date]
labels: [glossary]
description: [One-line definition]
tags: [term, domain]
---
```

### Step 3.3: Developer Identifies Key Decisions

> **Note**: The `01-explanation/decisions.md` skeleton was already copied in Phase 0. You may either keep it as a flat file or convert to a `decisions/` directory with individual ADR files (as was done in the parallel-powers project itself).

Using the **Developer (Alex)** persona:

Create initial ADRs in `agent-docs/01-explanation/decisions/` based on the architecture deep dive. If there is existing code, do additional deep dives if necessary to understand the rationale.

### Step 3.4: Docs Author Outlines Tutorials and How-Tos

Using the **Docs Author (Casey)** persona:

> **Note**: Skeleton files (`02-tutorial/getting-started.md`, `03-howto/installation.md`, `03-howto/setup-issue-labels.md`) were already copied in Phase 0. Customize these rather than recreating them.

**Tutorials** — Based on the codebase, identify 2-3 learning paths:
- Getting started tutorial (already has a bootstrap skeleton)
- One intermediate tutorial
- One advanced tutorial

Create any additional skeleton files in `agent-docs/02-tutorial/` with proper frontmatter.

**How-To Guides** — Based on common tasks:
- Installation/setup (already has a bootstrap skeleton)
- Configuration
- Common workflows

Create any additional skeleton files in `agent-docs/03-howto/` with proper frontmatter.

## Phase 4: Validation

Using the **Project Manager (Morgan)** persona:

Review and verify:

- [ ] All new files have valid frontmatter
- [ ] Diagrams render correctly
- [ ] Links between docs work
- [ ] Personas reference actual docs
- [ ] Architecture views are consistent
- [ ] Glossary terms are complete
- [ ] ADRs capture key decisions

## Checklist Summary

```
=== Phase 0: Bootstrap Initialization =========================================

All files below are copied from agent-docs-bootstrap/ in Step 0.1.
After copying, customize each file for the project in subsequent phases.

agent-docs/00-readme/index.md                       → Skeleton readme
agent-docs/01-explanation/index.md                  → Directory index
agent-docs/01-explanation/architecture.md           → Architecture skeleton
agent-docs/01-explanation/decisions.md              → Design decisions skeleton
agent-docs/02-tutorial/index.md                     → Directory index
agent-docs/02-tutorial/getting-started.md            → Tutorial skeleton
agent-docs/03-howto/index.md                        → Directory index
agent-docs/03-howto/installation.md                 → Installation guide skeleton
agent-docs/03-howto/setup-issue-labels.md           → Issue label setup guide
agent-docs/04-reference/index.md                    → Directory index
agent-docs/04-reference/cli.md                      → CLI reference skeleton
agent-docs/04-reference/config-schema.md            → Config schema skeleton
agent-docs/04-reference/issue-labels.md             → Issue label schema
agent-docs/05-plans/index.md                        → Directory index
agent-docs/05-plans/roadmap.md                      → Roadmap skeleton
agent-docs/06-environment/index.md                  → Directory index
agent-docs/06-environment/setup.md                  → Setup guide skeleton
agent-docs/07-runbooks/index.md                     → Directory index
agent-docs/07-runbooks/deployment.md                → Deployment runbook skeleton
agent-docs/08-troubleshooting/index.md              → Directory index
agent-docs/08-troubleshooting/common-errors.md      → Common errors skeleton
agent-docs/09-changelog/index.md                    → Changelog skeleton
agent-docs/10-glossary/index.md                     → Glossary skeleton
agent-docs/11-agents/index.md                       → Agents guide skeleton
agent-docs/12-metadata/index.md                     → Metadata directory index
agent-docs/12-metadata/diagrams.md                  → Diagram conventions
agent-docs/12-metadata/file-structure.md            → File structure conventions
agent-docs/13-personas/index.md                     → Personas directory index

=== Phase 1-5: Project-Specific Files (created from scratch) =================

agent-docs/13-personas/architect.md             → Step 1.2: Architect persona
agent-docs/12-metadata/project.yml              → Step 1.3: Project metadata
AGENTS.md (or agent-docs/AGENTS.md)              → Step 1.4: Agent guide with diataxis
CLAUDE.md                                       → Step 1.5: Claude Code instructions
agent-docs/13-personas/developer.md             → Step 3.1: Developer persona
agent-docs/13-personas/operator.md              → Step 3.1: Operator persona
agent-docs/13-personas/evaluator.md             → Step 3.1: Evaluator persona
agent-docs/13-personas/project-manager.md       → Step 3.1: PM persona
agent-docs/13-personas/docs-author.md           → Step 3.1: Docs author persona
agent-docs/13-personas/product-marketing.md     → Step 3.1: Product marketing persona

agent-docs/01-explanation/
  ├── architecture-subsystems.md   → Step 2.1
  ├── architecture-components.md   → Step 2.2
  └── architecture-runtime.md      → Step 2.3

agent-docs/10-glossary/index.md     → Step 3.2: Glossary terms (extend copied skeleton)
agent-docs/01-explanation/decisions/ → Step 3.3: ADRs
agent-docs/02-tutorial/             → Step 3.4: Tutorial outlines (extend copied skeleton)
agent-docs/03-howto/                → Step 3.4: How-to outlines (extend copied skeleton)

agent-docs/11-agents/time-tracking.md → Step 5.2: Time tracking guide (optional)
agent-docs/11-agents/superpowers.md   → Step 5.3: Superpowers guide (optional)
```

## Running the Installer

As an agent, execute this installer by:

1. Reading `agent-docs/00-readme/` to understand the kit structure
2. Reading `agent-docs/12-metadata/file-structure.md` for conventions
3. Reading `agent-docs/12-metadata/diagrams.md` for diagram styles
4. Starting with **Phase 0: Bootstrap Initialization** — copy all skeleton files
5. Following the remaining phases in order
6. Progressively customizing copied files as you go
7. Marking docs as `status: review` when draft is complete

## Phase 5: Optional Integrations

These steps are conditional — only apply what is relevant to the project.

### Time Tracking Integration

If the project uses parallelhours.io for time tracking, add time tracking integration:

### Step 5.1: Add Time Tracking Metadata

In `agent-docs/12-metadata/project.yml`, add time tracking configuration:

```yaml
time-tracking:
  provider: parallelhours.io
  project-key: "[PROJECT_KEY]"  # e.g., ZEROTRST
  mcp-server: parallelhours
```

### Step 5.2: Create Time Tracking Guidelines

Create `agent-docs/11-agents/time-tracking.md` with instructions for agents:

```yaml
---
created: [date]
updated: [date]
labels: [agents, time-tracking]
description: Time tracking instructions for AI agents.
tags: [time-tracking, parallelhours, sessions]
audience: [agents]
status: draft
version: 0.1.0
---

# Time Tracking

This project uses parallelhours.io for time tracking.

## Session Commands

- **`/vault-start [issue#]`** — Start a tracked session (creates task, starts timer)
- **`/vault-end`** — End session (stops timer, logs AI usage, pushes branch)

## How It Works

1. Agent runs `/vault-start 123` → creates/finds ZEROTRST task, starts timer
2. Agent works on the issue
3. Agent runs `/vault-end` → stops timer, logs AI usage, pushes branch

## MCP Configuration

If the project has `.mcp.json`, agents should check for parallelhours configuration:

```json
{
  "mcpServers": {
    "parallelhours": {
      "command": "uv",
      "args": ["run", "python", "/path/to/parallelhours/mcp_server.py"],
      "env": {
        "TKPI_PROJECT": "[PROJECT_KEY]"
      }
    }
  }
}
```

## What Gets Tracked

- Task creation/finding in parallelhours.io
- Timer start/stop
- AI prompt count (autonomous sessions)
- Branch push and PR creation
- CI status

## Notes for Agents

- Always run `/vault-start` before beginning work on an issue
- Always run `/vault-end` when completing a session
- The MCP must be configured in `.mcp.json` for time tracking to work
- Check existing commands in `.claude/commands/` for project-specific commands

## Superpowers Integration (Optional)

If the project uses the superpowers workflow:

### Step 5.3: Add Superpowers Reference

Create or update `agent-docs/11-agents/superpowers.md`:

```yaml
---
created: [date]
updated: [date]
labels: [agents, superpowers]
description: Superpowers workflow integration for planning and execution.
tags: [superpowers, planning, workflow]
audience: [agents]
status: draft
version: 0.1.0
---

# Superpowers Workflow

This project uses [superpowers](https://superpowers.app) for planning and execution.

## How It Works

1. **Planning**: Use superpowers to create implementation plans
2. **Plans Location**: `agent-docs/superpowers/plans/` — treat as authoritative once execution begins
3. **Specs Location**: `agent-docs/superpowers/specs/` — architecture and design documents

## Agent Integration

- Read `agent-docs/superpowers/plans/` for active implementation plans
- Read `agent-docs/superpowers/specs/` for design documents
- Plans created by superpowers are the source of truth for feature implementation

## Session Flow with Superpowers

1. `/vault-start` — Start session
2. Read relevant superpowers plan/spec
3. Execute according to plan
4. `/vault-end` — End session
```