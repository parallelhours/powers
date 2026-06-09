// Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0
// Ported from hooks/session_start_timer_check.py
export const checkActiveTimer = async (tkpiPat, baseUrl) => {
  if (!tkpiPat) return null;
  try {
    const resp = await fetch(`${baseUrl}/mcp/v1/timers/active/`, {
      headers: { Authorization: `Bearer ${tkpiPat}`, "Content-Type": "application/json" },
      signal: AbortSignal.timeout(5000),
    });
    if (!resp.ok) return null;
    const data = await resp.json();
    const timers = data?.timers || [];
    if (timers.length === 0) {
      return "parallelhours: No timer running. Start one with /session-start so this session is tracked.";
    }
  } catch {
    return null;
  }
  return null;
};
