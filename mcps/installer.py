#!/usr/bin/env python3
"""MCP Installer for parallel-powers.

Installs MCP servers for various AI agents (Claude Code, OpenCode, Codex).
MCPs live under mcps/<mcp_id>/ with an install.json describing how to configure
them for each agent.

Usage:
    python -m mcps.installer --mcp parallelhours --agent claude --location project
    python -m mcps.installer --mcp all --agent claude --location project
    python -m mcps.installer --list
"""

import argparse
import getpass
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

MCP_DIR = Path(__file__).resolve().parent


@dataclass
class Replacement:
    placeholder: str
    prompt: str
    secret: bool = False
    default: str = ""


@dataclass
class McpMetadata:
    id: str
    name: str
    description: str
    mcp_server_relative: str
    replacements: list[Replacement] = field(default_factory=list)
    default_env: dict[str, str] = field(default_factory=dict)
    agents: dict[str, Any] = field(default_factory=dict)
    global_paths: dict[str, str] = field(default_factory=dict)

    @property
    def server_path(self) -> Path:
        return MCP_DIR / self.id / self.mcp_server_relative


def load_registry() -> dict[str, McpMetadata]:
    """Load all MCP metadata from mcps/*/install.json files."""
    registry: dict[str, McpMetadata] = {}
    for item in sorted(MCP_DIR.iterdir()):
        if not item.is_dir():
            continue
        install_json = item / "install.json"
        if not install_json.exists():
            continue
        data = json.loads(install_json.read_text())
        replacements = [Replacement(**r) for r in data.get("replacements", [])]
        registry[data["id"]] = McpMetadata(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            mcp_server_relative=data.get("mcp_server_relative", ""),
            replacements=replacements,
            default_env=data.get("default_env", {}),
            agents=data.get("agents", {}),
            global_paths=data.get("global_paths", {}),
        )
    return registry


def resolve_config_path(agent: str, location: str, meta: McpMetadata) -> Path:
    if location == "global":
        raw = meta.global_paths.get(agent, f"~/.{agent}/{meta.agents.get(agent, {}).get('config_file', '.mcp.json')}")
        return Path(raw).expanduser().resolve()
    return Path.cwd() / meta.agents.get(agent, {}).get("config_file", ".mcp.json")


def substitute(obj: Any, values: dict[str, str]) -> Any:
    """Walk a JSON-like structure and replace ${KEY} placeholders."""
    if isinstance(obj, dict):
        return {k: substitute(v, values) for k, v in obj.items()}
    if isinstance(obj, list):
        return [substitute(v, values) for v in obj]
    if isinstance(obj, str):
        for key, val in values.items():
            obj = obj.replace("${" + key + "}", val)
        return obj
    return obj


def generate_config(meta: McpMetadata, agent: str, values: dict[str, str]) -> dict:
    """Generate the agent-specific config block with values substituted."""
    agent_config = meta.agents.get(agent)
    if agent_config is None:
        raise ValueError(f"Agent {agent!r} not supported for MCP {meta.id!r}")
    entry = agent_config["entry"]
    resolved = substitute(entry, values)
    return resolved


def merge_config(existing: dict, new: dict, agent: str) -> dict:
    """Merge a new MCP config block into an existing agent config file."""
    if agent == "claude":
        servers = existing.setdefault("mcpServers", {})
        servers.update(new.get("mcpServers", {}))
    elif agent == "opencode":
        mcp_block = existing.setdefault("mcp", {})
        mcp_block.update(new.get("mcp", {}))
    else:
        existing.update(new)
    return existing


def collect_values(
    meta: McpMetadata,
    env: Optional[dict[str, str]] = None,
    non_interactive: bool = False,
) -> dict[str, str]:
    """Collect values for each replacement, from env vars or interactive prompts."""
    if env is None:
        env = os.environ

    values: dict[str, str] = dict(meta.default_env)

    for rep in meta.replacements:
        if rep.placeholder in env and env[rep.placeholder]:
            values[rep.placeholder] = env[rep.placeholder]
            continue

        if non_interactive:
            values[rep.placeholder] = rep.default
            continue

        default_str = f" [{rep.default}]" if rep.default else ""
        secret_str = " (input hidden)" if rep.secret else ""
        prompt_text = f"  {rep.prompt}{secret_str}{default_str}: "

        if rep.secret:
            try:
                val = getpass.getpass(prompt_text)
            except (EOFError, KeyboardInterrupt):
                val = ""
        else:
            try:
                val = input(prompt_text)
            except (EOFError, KeyboardInterrupt):
                val = ""

        if not val:
            val = rep.default
        values[rep.placeholder] = val

    return values


def install_mcp(
    meta: McpMetadata,
    agent: str,
    location: str,
    values: dict[str, str],
) -> Path:
    """Install a single MCP: generate config and write/merge into the config file."""
    config = generate_config(meta, agent, values)
    config_path = resolve_config_path(agent, location, meta)

    if config_path.exists():
        existing = json.loads(config_path.read_text())
        merged = merge_config(existing, config, agent)
    else:
        merged = config

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(merged, indent=2) + "\n")
    return config_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install MCP servers for AI agents in parallel-powers.",
    )
    parser.add_argument(
        "--mcp",
        action="append",
        default=[],
        help="MCP to install (repeatable, or 'all' for all). If omitted, lists available MCPs.",
    )
    parser.add_argument(
        "--agent",
        default="claude",
        choices=["claude", "opencode", "codex"],
        help="Target AI agent (default: claude)",
    )
    parser.add_argument(
        "--location",
        default="project",
        choices=["global", "project"],
        help="Install location (default: project)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available MCPs and exit",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Skip interactive prompts; use defaults for missing values",
    )
    parser.add_argument(
        "--mcps-dir",
        default=None,
        help="Path to mcps directory (default: auto-detected)",
    )

    args = parser.parse_args(argv)

    if args.mcps_dir:
        mcps_dir = Path(args.mcps_dir)
    else:
        mcps_dir = MCP_DIR

    registry = load_registry()

    if args.list or not args.mcp:
        print("Available MCPs:")
        for mcp_id, meta in sorted(registry.items()):
            print(f"  {mcp_id:<20s} {meta.name:<20s} {meta.description}")
        if not registry:
            print("  (no MCPs found)")
        return 0

    mcps_to_install: set[str] = set()
    for m in args.mcp:
        if m == "all":
            mcps_to_install.update(registry.keys())
        else:
            mcps_to_install.add(m)

    invalid = mcps_to_install - set(registry.keys())
    if invalid:
        print(f"Unknown MCP(s): {', '.join(sorted(invalid))}", file=sys.stderr)
        print(f"Available: {', '.join(sorted(registry.keys()))}", file=sys.stderr)
        return 1

    results: list[tuple[str, Path]] = []

    for mcp_id in sorted(mcps_to_install):
        meta = registry[mcp_id]
        values = collect_values(meta, non_interactive=args.non_interactive)
        config_path = install_mcp(meta, args.agent, args.location, values)
        results.append((meta.name, config_path))

    for name, path in results:
        print(f"  ✓ {name} installed to {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
