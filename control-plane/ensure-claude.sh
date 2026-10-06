#!/usr/bin/env bash
set -euo pipefail

CLAUDE_CODE_VERSION="${CLAUDE_CODE_VERSION:-2.1.291}"

current=""
if command -v claude >/dev/null 2>&1; then
  current="$(claude --version 2>/dev/null | awk '{print $1}' || true)"
fi

if [[ "$current" != "$CLAUDE_CODE_VERSION" ]]; then
  npm install --global "@anthropic-ai/claude-code@$CLAUDE_CODE_VERSION"
fi

claude --version
