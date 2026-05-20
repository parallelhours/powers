#!/bin/bash
# Copyright (c) 2026 Parallel Hours LLC — PolyForm Noncommercial 1.0.0

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -q '^git commit'; then
  PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
  cd "$PROJECT_DIR" || exit 0
  echo "--- ruff lint check (pre-commit) ---"
  .venv/bin/ruff check src/ tests/
  exit $?
fi

exit 0
