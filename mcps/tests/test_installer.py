"""Tests for mcps.installer."""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from mcps.installer import (
    McpMetadata,
    Replacement,
    collect_values,
    generate_config,
    install_mcp,
    load_registry,
    merge_config,
    resolve_config_path,
    substitute,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_install_json():
    return {
        "id": "parallelhours",
        "name": "Parallel Hours",
        "description": "Time tracking via parallelhours.io",
        "mcp_server_relative": "server.py",
        "replacements": [
            {
                "placeholder": "TKPI_PAT",
                "prompt": "Personal Access Token",
                "secret": True,
                "default": "",
            },
            {
                "placeholder": "TKPI_PROJECT",
                "prompt": "Default project key",
                "secret": False,
                "default": "MYPROJ",
            },
        ],
        "default_env": {
            "TKPI_BASE_URL": "https://parallelhours.io",
        },
        "agents": {
            "claude": {
                "config_file": ".mcp.json",
                "entry": {
                    "mcpServers": {
                        "parallelhours": {
                            "command": "uvx",
                            "args": ["parallelhours-mcp"],
                            "env": {
                                "TKPI_PAT": "${TKPI_PAT}",
                                "TKPI_BASE_URL": "${TKPI_BASE_URL}",
                                "TKPI_PROJECT": "${TKPI_PROJECT}",
                            },
                        }
                    }
                },
            },
            "opencode": {
                "config_file": "opencode.jsonc",
                "entry": {
                    "mcp": {
                        "parallelhours": {
                            "type": "local",
                            "command": [
                                "uv",
                                "run",
                                "--with",
                                "mcp",
                                "--with",
                                "httpx",
                                "python",
                                "{MCP_SERVER_PATH}",
                            ],
                            "enabled": True,
                            "environment": {
                                "TKPI_PAT": "${TKPI_PAT}",
                                "TKPI_BASE_URL": "${TKPI_BASE_URL}",
                                "TKPI_PROJECT": "${TKPI_PROJECT}",
                            },
                        }
                    }
                },
            },
        },
        "global_paths": {
            "claude": "~/.claude/.mcp.json",
            "opencode": "~/.config/opencode/opencode.jsonc",
        },
    }


@pytest.fixture
def mcps_dir(tmp_path, sample_install_json):
    """Create a temporary mcps directory with a parallelhours MCP."""
    mcp_path = tmp_path / "parallelhours"
    mcp_path.mkdir(parents=True)
    (mcp_path / "install.json").write_text(json.dumps(sample_install_json))
    (mcp_path / "server.py").write_text("# fake server")
    return tmp_path


@pytest.fixture
def sample_meta():
    return McpMetadata(
        id="parallelhours",
        name="Parallel Hours",
        description="Time tracking via parallelhours.io",
        mcp_server_relative="server.py",
        replacements=[
            Replacement(placeholder="TKPI_PAT", prompt="Token", secret=True, default=""),
            Replacement(placeholder="TKPI_PROJECT", prompt="Project", secret=False, default="MYPROJ"),
        ],
        default_env={"TKPI_BASE_URL": "https://parallelhours.io"},
        agents={
            "claude": {
                "config_file": ".mcp.json",
                "entry": {
                    "mcpServers": {
                        "parallelhours": {
                            "command": "uvx",
                            "args": ["parallelhours-mcp"],
                            "env": {
                                "TKPI_PAT": "${TKPI_PAT}",
                                "TKPI_PROJECT": "${TKPI_PROJECT}",
                            },
                        }
                    }
                },
            },
        },
        global_paths={"claude": "~/.claude/.mcp.json"},
    )


# ---------------------------------------------------------------------------
# load_registry
# ---------------------------------------------------------------------------


class TestLoadRegistry:
    def test_loads_install_json(self, mcps_dir, monkeypatch):
        monkeypatch.setattr("mcps.installer.MCP_DIR", mcps_dir)
        registry = load_registry()
        assert "parallelhours" in registry
        meta = registry["parallelhours"]
        assert meta.name == "Parallel Hours"
        assert len(meta.replacements) == 2
        assert meta.replacements[0].placeholder == "TKPI_PAT"

    def test_empty_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr("mcps.installer.MCP_DIR", tmp_path)
        registry = load_registry()
        assert "parallelhours" not in registry

    def test_skips_dirs_without_install_json(self, tmp_path, monkeypatch):
        (tmp_path / "foo").mkdir()
        monkeypatch.setattr("mcps.installer.MCP_DIR", tmp_path)
        registry = load_registry()
        assert "foo" not in registry


# ---------------------------------------------------------------------------
# substitute
# ---------------------------------------------------------------------------


class TestSubstitute:
    def test_replaces_placeholders(self):
        result = substitute("hello ${NAME}", {"NAME": "world"})
        assert result == "hello world"

    def test_replaces_multiple(self):
        result = substitute("${A} and ${B}", {"A": "x", "B": "y"})
        assert result == "x and y"

    def test_nested_dict(self):
        obj = {"env": {"KEY": "${VALUE}"}}
        result = substitute(obj, {"VALUE": "secret"})
        assert result == {"env": {"KEY": "secret"}}

    def test_nested_list(self):
        obj = {"args": ["--name", "${NAME}"]}
        result = substitute(obj, {"NAME": "foo"})
        assert result == {"args": ["--name", "foo"]}

    def test_unmatched_placeholder_unchanged(self):
        result = substitute("hello ${UNKNOWN}", {"NAME": "world"})
        assert result == "hello ${UNKNOWN}"

    def test_non_string_unchanged(self):
        assert substitute(42, {}) == 42
        assert substitute(True, {}) is True
        assert substitute(None, {}) is None


# ---------------------------------------------------------------------------
# generate_config
# ---------------------------------------------------------------------------


class TestGenerateConfig:
    def test_generates_claude_config(self, sample_meta):
        values = {
            "TKPI_PAT": "pat_123",
            "TKPI_PROJECT": "MYPROJ",
            "TKPI_BASE_URL": "https://parallelhours.io",
        }
        config = generate_config(sample_meta, "claude", values)
        assert config["mcpServers"]["parallelhours"]["command"] == "uvx"
        assert config["mcpServers"]["parallelhours"]["env"]["TKPI_PAT"] == "pat_123"
        assert config["mcpServers"]["parallelhours"]["env"]["TKPI_PROJECT"] == "MYPROJ"

    def test_unsupported_agent(self, sample_meta):
        with pytest.raises(ValueError, match="not supported"):
            generate_config(sample_meta, "codex", {})


# ---------------------------------------------------------------------------
# merge_config
# ---------------------------------------------------------------------------


class TestMergeConfig:
    def test_merges_claude(self):
        existing = {"other_key": True, "mcpServers": {"existing": {}}}
        new = {"mcpServers": {"parallelhours": {"command": "uvx"}}}
        merged = merge_config(existing, new, "claude")
        assert "existing" in merged["mcpServers"]
        assert "parallelhours" in merged["mcpServers"]

    def test_merges_opencode(self):
        existing = {"$schema": "https://opencode.ai/config.json"}
        new = {"mcp": {"parallelhours": {}}}
        merged = merge_config(existing, new, "opencode")
        assert merged["$schema"] is not None
        assert "parallelhours" in merged["mcp"]

    def test_creates_new_key_when_missing(self):
        existing = {}
        new = {"mcpServers": {"ph": {}}}
        merged = merge_config(existing, new, "claude")
        assert merged == {"mcpServers": {"ph": {}}}

    def test_preserves_existing_keys(self):
        existing = {"mcpServers": {"a": 1}}
        new = {"mcpServers": {"b": 2}}
        merged = merge_config(existing, new, "claude")
        assert merged["mcpServers"] == {"a": 1, "b": 2}


# ---------------------------------------------------------------------------
# resolve_config_path
# ---------------------------------------------------------------------------


class TestResolveConfigPath:
    def test_project_local(self, sample_meta):
        path = resolve_config_path("claude", "project", sample_meta)
        assert path.name == ".mcp.json"
        assert path.is_absolute()

    def test_global(self, sample_meta):
        path = resolve_config_path("claude", "global", sample_meta)
        assert str(path).endswith(".claude/.mcp.json")

    def test_global_expands_user(self, sample_meta):
        path = resolve_config_path("claude", "global", sample_meta)
        assert "~" not in str(path)


# ---------------------------------------------------------------------------
# collect_values
# ---------------------------------------------------------------------------


class TestCollectValues:
    def test_reads_from_env(self, sample_meta):
        env = {"TKPI_PAT": "from_env", "TKPI_PROJECT": "ENVPROJ"}
        values = collect_values(sample_meta, env=env, non_interactive=True)
        assert values["TKPI_PAT"] == "from_env"
        assert values["TKPI_PROJECT"] == "ENVPROJ"

    def test_default_env_included(self, sample_meta):
        values = collect_values(sample_meta, env={}, non_interactive=True)
        assert values["TKPI_BASE_URL"] == "https://parallelhours.io"

    def test_non_interactive_uses_default(self, sample_meta):
        values = collect_values(sample_meta, env={}, non_interactive=True)
        assert values["TKPI_PAT"] == ""
        assert values["TKPI_PROJECT"] == "MYPROJ"

    def test_env_overrides_default(self, sample_meta):
        env = {"TKPI_PROJECT": "OVERRIDE"}
        values = collect_values(sample_meta, env=env, non_interactive=True)
        assert values["TKPI_PROJECT"] == "OVERRIDE"

    @patch("mcps.installer.getpass.getpass", return_value="interactive_pat")
    @patch("mcps.installer.input", return_value="INTERACTIVE_PROJ")
    def test_interactive_prompt(self, mock_input, mock_getpass, sample_meta):
        values = collect_values(sample_meta, env={}, non_interactive=False)
        assert values["TKPI_PAT"] == "interactive_pat"
        assert values["TKPI_PROJECT"] == "INTERACTIVE_PROJ"


# ---------------------------------------------------------------------------
# install_mcp
# ---------------------------------------------------------------------------


class TestInstallMCP:
    def test_creates_new_config(self, tmp_path, sample_meta):
        config_path = tmp_path / ".mcp.json"
        values = {
            "TKPI_PAT": "pat_123",
            "TKPI_PROJECT": "MYPROJ",
            "TKPI_BASE_URL": "https://parallelhours.io",
        }

        with patch.object(type(sample_meta), "server_path", tmp_path / "server.py"):
            with patch("mcps.installer.resolve_config_path", return_value=config_path):
                result = install_mcp(sample_meta, "claude", "project", values)

        assert result == config_path
        assert config_path.exists()
        data = json.loads(config_path.read_text())
        assert data["mcpServers"]["parallelhours"]["env"]["TKPI_PAT"] == "pat_123"

    def test_merges_existing_config(self, tmp_path, sample_meta):
        config_path = tmp_path / ".mcp.json"
        config_path.write_text(json.dumps({"existing_key": True}))

        values = {
            "TKPI_PAT": "pat_456",
            "TKPI_PROJECT": "TEST",
            "TKPI_BASE_URL": "https://parallelhours.io",
        }

        with patch.object(type(sample_meta), "server_path", tmp_path / "server.py"):
            with patch("mcps.installer.resolve_config_path", return_value=config_path):
                result = install_mcp(sample_meta, "claude", "project", values)

        assert result == config_path
        data = json.loads(config_path.read_text())
        assert data["existing_key"] is True
        assert "parallelhours" in data["mcpServers"]


# ---------------------------------------------------------------------------
# main() / CLI
# ---------------------------------------------------------------------------


class TestMain:
    def test_list_flag(self, mcps_dir):
        from mcps.installer import main

        exit_code = main(["--list", "--mcps-dir", str(mcps_dir)])
        assert exit_code == 0

    def test_install_all(self, tmp_path, mcps_dir):
        from mcps.installer import main

        config_path = tmp_path / ".mcp.json"
        env = {"TKPI_PAT": "pat_cli", "TKPI_PROJECT": "CLIPROJ"}

        with patch.dict(os.environ, env, clear=True):
            with patch("mcps.installer.resolve_config_path", return_value=config_path):
                exit_code = main(
                    [
                        "--mcp",
                        "parallelhours",
                        "--agent",
                        "claude",
                        "--location",
                        "project",
                        "--non-interactive",
                        "--mcps-dir",
                        str(mcps_dir),
                    ]
                )

        assert exit_code == 0
        assert config_path.exists()
        data = json.loads(config_path.read_text())
        env_block = data["mcpServers"]["parallelhours"]["env"]
        assert env_block["TKPI_PAT"] == "pat_cli"
        assert env_block["TKPI_PROJECT"] == "CLIPROJ"

    def test_unknown_mcp_returns_error(self, mcps_dir):
        from mcps.installer import main

        exit_code = main(
            [
                "--mcp",
                "nonexistent",
                "--non-interactive",
                "--mcps-dir",
                str(mcps_dir),
            ]
        )
        assert exit_code == 1
