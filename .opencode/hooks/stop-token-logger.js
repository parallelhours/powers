// Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0
// Ported from hooks/stop_token_logger.py
export const logTokenUsage = async (tkpiPat, baseUrl, usage, sessionId) => {
  if (!tkpiPat) return;
  try {
    const timer = await findActiveTimer(tkpiPat, baseUrl, sessionId);
    if (!timer) return;

    const body = {
      ai_tool: "opencode",
      mode: "delegated",
      prompt_count: 0,
      input_tokens: usage?.inputTokens || 0,
      output_tokens: usage?.outputTokens || 0,
      notes: "auto-logged by stop-token-logger hook",
    };

    const cacheRead = usage?.cacheReadInputTokens || usage?.cache_read_input_tokens || 0;
    const cacheWrite = usage?.cacheWriteInputTokens || usage?.cache_creation_input_tokens || 0;
    const toolCalls = usage?.toolCallCount || usage?.tool_call_count || 0;

    if (cacheRead > 0) body.cache_read_tokens = cacheRead;
    if (cacheWrite > 0) body.cache_write_tokens = cacheWrite;
    if (toolCalls > 0) body.tool_call_count = toolCalls;
    if (usage?.modelId || usage?.model_id) body.model_id = usage?.modelId || usage?.model_id || "";

    await fetch(`${baseUrl}/mcp/v1/timers/${timer.timer_id}/ai-event/`, {
      method: "POST",
      headers: { Authorization: `Bearer ${tkpiPat}`, "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(5000),
    });
  } catch {
    // silently fail
  }
};

async function findActiveTimer(tkpiPat, baseUrl, sessionId) {
  try {
    const params = sessionId ? `?session_id=${sessionId}` : "";
    const resp = await fetch(`${baseUrl}/mcp/v1/timers/active/${params}`, {
      headers: { Authorization: `Bearer ${tkpiPat}`, "Content-Type": "application/json" },
      signal: AbortSignal.timeout(5000),
    });
    if (resp.ok) {
      const data = await resp.json();
      const timers = data?.timers || [];
      if (timers.length > 0) return timers[timers.length - 1];
    }
    if (sessionId) {
      const fallback = await fetch(`${baseUrl}/mcp/v1/timers/active/`, {
        headers: { Authorization: `Bearer ${tkpiPat}`, "Content-Type": "application/json" },
        signal: AbortSignal.timeout(5000),
      });
      if (fallback.ok) {
        const data = await fallback.json();
        const timers = data?.timers || [];
        if (timers.length > 0) return timers[timers.length - 1];
      }
    }
  } catch {
    // silently fail
  }
  return null;
}
