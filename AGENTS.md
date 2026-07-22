# parallel-powers

Human-in-the-loop framework for agentic-assisted product development.

## Essentials

- **All documentation lives in `agent-docs/`** (Diátaxis framework) — read relevant docs before deep-diving code
- **`agent-docs-bootstrap/`** is the template/installer — do not remove it
- **`mcps/`** is the MCP Framework — optionally installable MCP servers managed by `mcps/installer.py`
- Documentation must include valid YAML frontmatter per `agent-docs/12-metadata/file-structure.md`

## Plugin structure

This repository is a **Claude Code plugin**, **Codex plugin**, and **OpenCode plugin** that provides session management powers. The plugin ships skills, hooks, and scripts:

### Layout

```
.claude-plugin/plugin.json      # Claude Code plugin manifest
.codex-plugin/plugin.json       # Codex plugin manifest
skills/                          # Skills (shared — Claude Code, Codex, OpenCode)
  session-start/SKILL.md         #   Start a tracked dev session
  session-end/SKILL.md           #   End a tracked dev session
  editorial-reviewer/SKILL.md    #   Review content for inclusive language and clarity
  github-burndown/SKILL.md       #   Burndown chart from GitHub issues
  github-sprint-board/SKILL.md   #   Sprint board from GitHub issues
hooks/                           # Hook scripts and configuration (shared — Claude Code, Codex)
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

### Skill vs hook model

- **Skills** (`skills/`) define multi-step workflows the agent executes — checking git state, calling MCP tools, creating branches, starting timers. Invoked explicitly by the user.
- **Hooks** (`hooks/`) fire automatically on session events — warn on missing timer at startup, count prompts on each message, log tokens on stop. Run as background scripts, invisible to the agent.
- Both can use **MCP tools** (skills call parallelhours MCP tools directly; hooks use the REST API).

### Installation

**Claude Code:**
```bash
# From release zip (no clone needed):
claude --plugin-url https://github.com/parallelhours/powers/releases/download/v1.4.6/parallel-powers.zip

# Or from a local clone:
claude --plugin-dir /path/to/parallel-powers
```

Skills are namespaced: `/parallel-powers:session-start`, `/parallel-powers:session-end`, `/parallel-powers:editorial-reviewer`

**Codex:**
```bash
codex plugin marketplace add parallelhours/powers
```
Then inside a session: `/plugin install parallel-powers`

Skills are invoked via `$` mention or `/skills` picker.

**OpenCode:**
```json
{ "plugin": ["powers@git+https://github.com/parallelhours/powers.git"] }
```

### Requirements

- `$TKPI_PAT` — parallelhours API token
- `$TKPI_BASE_URL` — parallelhours base URL (default: https://parallelhours.io)
- Python 3 + httpx (`pip install httpx`) for hook scripts
- GitHub CLI (`gh`) for issue/PR operations
- jq for pre-commit-lint hook

> For anything beyond these essentials, consult the relevant `agent-docs/` section.

## Common Agent Tasks

| Task | Guide |
|------|-------|
| Create a GitHub release | [`agent-docs/03-howto/create-a-release.md`](agent-docs/03-howto/create-a-release.md) |
| Add a new MCP server | [`agent-docs/03-howto/add-new-mcp.md`](agent-docs/03-howto/add-new-mcp.md) |
| Install docs kit | [`agent-docs/03-howto/installation.md`](agent-docs/03-howto/installation.md) |
