// Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0
export const ParallelPowersPlugin = async ({ project, client, $, directory, worktree }) => {
  const TKPI_PAT = process.env.TKPI_PAT || "";
  const BASE_URL = (process.env.TKPI_BASE_URL || "https://parallelhours.io").replace(/\/+$/, "");

  const headers = () => ({
    "Authorization": `Bearer ${TKPI_PAT}`,
    "Content-Type": "application/json",
  });

  const apiGet = async (path, params = {}) => {
    if (!TKPI_PAT) return null;
    try {
      const url = new URL(`${BASE_URL}${path}`);
      Object.entries(params).forEach(([k, v]) => { if (v) url.searchParams.set(k, v); });
      const resp = await fetch(url.toString(), { headers: headers(), signal: AbortSignal.timeout(5000) });
      return resp.ok ? await resp.json() : null;
    } catch { return null; }
  };

  const apiPost = async (path, body = {}) => {
    if (!TKPI_PAT) return null;
    try {
      const resp = await fetch(`${BASE_URL}${path}`, {
        method: "POST", headers: headers(),
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
        const ruffArgs = { cwd: directory };
        const proc = Bun.spawnSync([".venv/bin/ruff", "check", "src/", "tests/"], ruffArgs);
        if (proc.exitCode !== 0) {
          throw new Error(`ruff lint check failed (pre-commit):\n${proc.stderr.toString()}`);
        }
      }
    },

    "session.status": async () => {
      if (!TKPI_PAT) return;
      const timer = await findActiveTimer();
      if (timer) {
        await apiPost(`/mcp/v1/timers/${timer.timer_id}/prompt/`);
      }
    },

    "session.idle": async (input) => {
      if (!TKPI_PAT) return;
      const timer = await findActiveTimer(input?.session?.id);
      if (!timer) return;
      const body = {
        ai_tool: "opencode",
        model_id: input?.session?.model || "unknown",
        mode: "delegated",
        prompt_count: 0,
        input_tokens: input?.usage?.inputTokens || 0,
        output_tokens: input?.usage?.outputTokens || 0,
        notes: "auto-logged by session.idle hook",
      };
      await apiPost(`/mcp/v1/timers/${timer.timer_id}/ai-event/`, body);
    },

    "session.error": async (input) => {
      if (!TKPI_PAT) return;
      const timer = await findActiveTimer(input?.session?.id);
      if (!timer) return;
      const body = {
        ai_tool: "opencode",
        model_id: input?.session?.model || "unknown",
        mode: "delegated",
        prompt_count: 0,
        input_tokens: input?.usage?.inputTokens || 0,
        output_tokens: input?.usage?.outputTokens || 0,
        notes: `auto-logged by session.error: ${input?.error?.message || "unknown error"}`,
      };
      await apiPost(`/mcp/v1/timers/${timer.timer_id}/ai-event/`, body);
    },
  };
};
