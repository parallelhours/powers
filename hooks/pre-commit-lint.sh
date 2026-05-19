#!/bin/bash

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
