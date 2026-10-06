#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-status}" in
 status) command -v codex; codex --version; codex login status ;;
 login) exec codex login --device-auth ;;
 supabase-login)
 codex mcp add supabase_life --url "https://mcp.supabase.com/mcp?project_ref=hjweyhpmrxqsxfbibsnc&read_only=true"
 exec codex mcp login supabase_life ;;
 *) echo "Usage: bash control-plane/codex.sh [status|login|supabase-login]" >&2; exit 2 ;;
esac
