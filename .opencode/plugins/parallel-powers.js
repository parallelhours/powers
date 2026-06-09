// Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";
import { runPreCommitLint } from "../hooks/pre-commit-lint.js";
import { incrementPromptCount } from "../hooks/prompt-counter.js";
import { logTokenUsage } from "../hooks/stop-token-logger.js";

export const ParallelPowersPlugin = async ({ project, client, $, directory, worktree }) => {
  const TKPI_PAT = process.env.TKPI_PAT || "";
  const BASE_URL = (process.env.TKPI_BASE_URL || "https://parallelhours.io").replace(/\/+$/, "");

  const apiGet = async (path, params = {}) => {
    if (!TKPI_PAT) return null;
    try {
      const url = new URL(`${BASE_URL}${path}`);
      Object.entries(params).forEach(([k, v]) => { if (v) url.searchParams.set(k, v); });
      const resp = await fetch(url.toString(), {
        headers: { Authorization: `Bearer ${TKPI_PAT}`, "Content-Type": "application/json" },
        signal: AbortSignal.timeout(5000),
      });
      return resp.ok ? await resp.json() : null;
    } catch { return null; }
  };

  const apiPost = async (path, body = {}) => {
    if (!TKPI_PAT) return null;
    try {
      const resp = await fetch(`${BASE_URL}${path}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${TKPI_PAT}`, "Content-Type": "application/json" },
        body: JSON.stringify(body), signal: AbortSignal.timeout(5000),
      });
      return resp.ok ? await resp.json().catch(() => null) : null;
    } catch { return null; }
  };

  const findActiveTimer = async (sessionId = "") => {
    const data = await apiGet("/mcp/v1/timers/active/", { session_id: sessionId });
    const timers = data?.timers || [];
    if (timers.length > 0) return timers[timers.length - 1];
    if (sessionId) return findActiveTimer();
    return null;
  };

  return {
    config: async (config) => {
      const skillsDir = resolve(dirname(fileURLToPath(import.meta.url)), "../skills");
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(skillsDir)) {
        config.skills.paths.push(skillsDir);
      }

      config.mcp = config.mcp || {};
      config.mcp.parallelhours = {
        type: "local",
        command: ["uvx", "parallelhours-mcp"],
        enabled: true,
        environment: {
          TKPI_PAT,
          TKPI_BASE_URL: BASE_URL,
          TKPI_PROJECT: process.env.TKPI_PROJECT || "",
        },
      };
    },

    "session.created": async () => {
      if (!TKPI_PAT) return;
      const timers = await apiGet("/mcp/v1/timers/active/");
      if (timers && (timers.timers || []).length === 0) {
        await client.app.log({
          body: { service: "parallel-powers", level: "warn",
            message: "No timer running. Start one with /session-start or the parallelhours MCP tools." },
        });
      }
    },

    "tool.execute.before": async (input, output) => {
      if (input.tool === "bash" && output.args.command?.startsWith("git commit")) {
        runPreCommitLint(directory);
      }
    },

    "session.status": async () => {
      await incrementPromptCount(TKPI_PAT, BASE_URL);
    },

    "session.idle": async (input) => {
      await logTokenUsage(TKPI_PAT, BASE_URL, input?.usage, input?.session?.id);
    },

    "session.error": async (input) => {
      await logTokenUsage(TKPI_PAT, BASE_URL, input?.usage, input?.session?.id);
    },

    "session.deleted": async (input) => {
      await logTokenUsage(TKPI_PAT, BASE_URL, input?.usage, input?.session?.id);
    },
  };
};
