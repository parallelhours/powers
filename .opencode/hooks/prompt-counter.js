// Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0
// Ported from hooks/prompt_counter.py
export const incrementPromptCount = async (tkpiPat, baseUrl, sessionId) => {
  if (!tkpiPat) return;
  try {
    const findUrl = `${baseUrl}/mcp/v1/timers/active/${sessionId ? `?session_id=${sessionId}` : ""}`;
    const resp = await fetch(findUrl, {
      headers: { Authorization: `Bearer ${tkpiPat}`, "Content-Type": "application/json" },
      signal: AbortSignal.timeout(5000),
    });
    if (!resp.ok) return;
    const data = await resp.json();
    const timers = data?.timers || [];
    if (timers.length === 0 && sessionId) {
      const fallback = await fetch(`${baseUrl}/mcp/v1/timers/active/`, {
        headers: { Authorization: `Bearer ${tkpiPat}`, "Content-Type": "application/json" },
        signal: AbortSignal.timeout(5000),
      });
      if (!fallback.ok) return;
      const fallbackData = await fallback.json();
      timers.push(...(fallbackData?.timers || []));
    }
    if (timers.length === 0) return;
    await fetch(`${baseUrl}/mcp/v1/timers/${timers[timers.length - 1].timer_id}/prompt/`, {
      method: "POST",
      headers: { Authorization: `Bearer ${tkpiPat}`, "Content-Type": "application/json" },
      signal: AbortSignal.timeout(5000),
    });
  } catch {
    // silently fail
  }
};
