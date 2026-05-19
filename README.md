# parallel-powers

Human-in-the-loop framework for agentic-assisted product development. Adds session management skills, automated hooks, and MCP servers that give coding agents time tracking and workflow powers — useful for anyone whose agentic workflow needs structured session start/end, prompt counting, and token logging against a time-tracking backend.

## Components

### agent-docs-bootstrap — Documentation Kit Template

The `agent-docs-bootstrap/` directory is a template for initializing the [Diátaxis](https://diataxis.fr/) documentation framework in any project. It provides skeleton files for all 14 doc categories (readme, explanation, tutorials, how-tos, reference, plans, etc.), frontmatter conventions, and persona templates.

→ [Installer guide](agent-docs-bootstrap/installer.md) — instructions for agents to bootstrap a new project's docs

### Plugin — Session Management Powers

The repo is a **Claude Code plugin** (and **OpenCode plugin**) that adds session-tracking skills and automated hooks.

| Component | What it does |
|-----------|-------------|
| **Skills** (`skills/`) | `/parallel-powers:session-start` and `/parallel-powers:session-end` — multi-step workflows for creating tasks, starting/stopping timers, pushing branches, and opening PRs. `/parallel-powers:editorial-reviewer` — inclusive language, clarity, and sentiment review of any target (files, URLs, or freeform text) |
| **Hooks** (`hooks/`) | Trigger automatically on events: warn on missing timer at startup, count prompts on each message, log tokens on stop, lint before git commit |
| **OpenCode plugin** (`.opencode/`) | JS plugin with equivalent hook behavior, plus skills for OpenCode's `skill` tool — including `editorial-reviewer` for content review |

**Claude Code:**

Clone and load locally:
```bash
git clone git@github.com:parallelhours/powers.git
claude --plugin-dir /path/to/powers
```

Or load directly from a GitHub archive URL (no clone needed):
```bash
claude --plugin-url https://github.com/parallelhours/powers/archive/main.zip
```

Skills are namespaced: `/parallel-powers:session-start`, `/parallel-powers:session-end`, `/parallel-powers:editorial-reviewer`

Run `/reload-plugins` after adding new skills to the `skills/` directory.

**OpenCode:**

Add to `opencode.json` — local path or remote git URL:
```json
{ "plugin": ["/path/to/powers"] }
```
```json
{ "plugin": ["powers@git+https://github.com/parallelhours/powers.git"] }
```

Requires a parallelhours API token (`TKPI_PAT`), the parallelhours base URL (`TKPI_BASE_URL`, defaults to `https://parallelhours.io`), Python 3 with httpx, the GitHub CLI (`gh`), and `jq`.

### MCP Servers — Optional Tool Integration

The `mcps/` directory provides installable MCP servers managed by `mcps/installer.py`:

| MCP | Description |
|-----|-------------|
| **parallelhours** | Time tracking and KPI management via [parallelhours.io](https://parallelhours.io) — exposes tools for tasks, timers, and AI event logging |

**Install an MCP:**
```bash
python -m mcps.installer --mcp parallelhours --agent claude --location project
python -m mcps.installer --mcp parallelhours --agent opencode --location project
python -m mcps.installer --list              # list available MCPs
python -m mcps.installer --mcp all --agent claude --location global  # install all globally
```

Each MCP server lives in `mcps/<name>/` with an `install.json` describing agent-specific config, environment variables, and placeholder prompts (e.g., `TKPI_PAT`). The installer walks you through each credential or token and writes the resulting config to `.mcp.json` (project) or `~/.claude/.mcp.json` (global).

### agent-docs — Project Documentation

All project docs follow the Diátaxis framework in `agent-docs/`. See the [docs readme](agent-docs/00-readme/) for the full structure.
