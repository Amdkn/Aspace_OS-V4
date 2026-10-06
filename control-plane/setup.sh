#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export ASPACE_INSTANCE_ROOT="${ASPACE_INSTANCE_ROOT:-/workspaces/aspace}"
mkdir -p "$ASPACE_INSTANCE_ROOT/state"
chmod 700 "$ASPACE_INSTANCE_ROOT/state"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm ci
python3 portable/instance.py hydrate --manifest control-plane/runtime.lock.json --root "$ASPACE_INSTANCE_ROOT"
(
  cd "$ASPACE_INSTANCE_ROOT/apps/cubefarm"
  npm ci
  npm run build
  npx playwright install --with-deps chrome
)
npm install --global @openai/codex@0.160.1
bash control-plane/ensure-claude.sh
python3 control-plane/directory.py workspace
if ! python3 control-plane/directory.py refresh; then
  echo 'Directory refresh failed; retained previous inventory. Retry after gh authentication.' >&2
fi
printf '\nV4 ready. Open /workspaces/aspace/aspace.code-workspace and private port 4417.\n'
