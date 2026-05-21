# parallel-powers

Human-in-the-loop framework for agentic-assisted product development.

## Essentials

- **All documentation lives in `agent-docs/`** (Diátaxis framework) — read relevant docs before deep-diving code
- **`agent-docs-bootstrap/`** is the template/installer — do not remove it
- **`mcps/`** is the MCP Framework — optionally installable MCP servers managed by `mcps/installer.py`
- Documentation must include valid YAML frontmatter per `agent-docs/12-metadata/file-structure.md`

## Plugin structure

This repository is a **Claude Code plugin** (and OpenCode plugin) that provides session management powers. The plugin ships skills, hooks, and scripts:

### Layout

```
.claude-plugin/plugin.json      # Claude Code plugin manifest
.codex-plugin/plugin.json       # Codex plugin manifest
skills/                          # Claude Code skills (namespaced, explicitly invoked)
  session-start/SKILL.md         #   Start a tracked dev session
  session-end/SKILL.md           #   End a tracked dev session
hooks/                           # Hook scripts and configuration
  hooks.json                     #   Hook registration (SessionStart, PreToolUse, UserPromptSubmit, Stop)
  session_start_timer_check.py   #   Warns if no timer is running at session start
  prompt_counter.py              #   Auto-increments prompt_count on user prompts
  stop_token_logger.py           #   Logs token usage from transcript on session stop
  pre-commit-lint.sh             #   Runs ruff lint before git commit
.opencode/                       # OpenCode plugin
  plugins/parallel-powers.js     #   JS plugin (hook equivalents)
  skills/                        #   Skills for OpenCode discovery
    session-start/SKILL.md
    session-end/SKILL.md
```

### Usage

**Claude Code** — load from release zip or local clone:
```bash
# From release zip (no clone needed):
claude --plugin-url https://github.com/parallelhours/powers/releases/download/v1.0.0/parallel-powers.zip

# Or from a local clone:
claude --plugin-dir /path/to/parallel-powers
```
Skills are namespaced: `/parallel-powers:session-start`, `/parallel-powers:session-end`, `/parallel-powers:editorial-reviewer`
Run `/reload-plugins` after changes.

**OpenCode** — add to `opencode.json`:
```json
{ "plugin": ["/path/to/parallel-powers"] }
```
Skills are available via the `skill` tool. If OpenCode doesn't discover them automatically, add to your config:
```json
{ "skills": { "paths": ["/path/to/parallel-powers/.opencode/skills"] } }
```

### Skill vs hook model

- **Skills** (`skills/`) define multi-step workflows that Claude/OpenCode executes — checking git state, calling MCP tools, creating branches, starting timers. These are invoked explicitly by the user.
- **Hooks** (`hooks/`) fire automatically on session events — warn on missing timer at startup, count prompts on each user message, log tokens on stop. These run as background scripts, invisible to the agent.
- Both can use **MCP tools** (the skills call parallelhours MCP tools directly; hooks use the REST API).

### Requirements

- `$TKPI_PAT` — parallelhours API token
- `$TKPI_BASE_URL` — parallelhours base URL (default: https://parallelhours.io)
- Python 3 + httpx (`pip install httpx`) for hook scripts
- GitHub CLI (`gh`) for issue/PR operations
- jq for pre-commit-lint hook

> For anything beyond these essentials, consult the relevant `agent-docs/` section.
