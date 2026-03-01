#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo "Boardroom web tool — session start"
echo "Project: $PROJECT_DIR"

# Verify the web tool entry point exists
if [ ! -f "$PROJECT_DIR/index.html" ]; then
  echo "WARNING: index.html not found in $PROJECT_DIR"
fi

# Check python3 is available for local preview (if needed)
if command -v python3 &>/dev/null; then
  echo "python3 $(python3 --version 2>&1) available — run 'python3 -m http.server 8080' to preview locally"
fi

echo "Session ready. No external dependencies to install."
