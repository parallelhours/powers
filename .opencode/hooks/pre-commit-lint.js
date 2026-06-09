// Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0
// Ported from hooks/pre-commit-lint.sh
import { spawnSync } from "child_process";

export const runPreCommitLint = (projectDir) => {
  const proc = spawnSync(".venv/bin/ruff", ["check", "src/", "tests/"], { cwd: projectDir });
  if (proc.status !== 0) {
    throw new Error(`ruff lint check failed (pre-commit):\n${proc.stderr.toString()}`);
  }
};
