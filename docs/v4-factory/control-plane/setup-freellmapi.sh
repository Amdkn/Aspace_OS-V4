#!/usr/bin/env bash
# setup-freellmapi.sh — Installe FreeLLMAPI sur le Codespace V4, au côté de CubeFarm.
#
# Ce que fait ce script (idempotent, relançable sans risque) :
#   1. Clone FreeLLMAPI (défaut : upstream tashfeenahmed/freellmapi)
#   2. Installe les dépendances (Node 20+ requis — le devcontainer a Node 24)
#   3. Build production (dashboard + serveur sur :3001)
#   4. Génère ENCRYPTION_KEY (persistée sous state/, jamais dans git)
#   5. Applique la config déclarative si présente (clés provider, idempotent)
#   6. Démarre le serveur en tâche de fond (logs sous state/)
#
# Usage :
#   bash control-plane/setup-freellmapi.sh
#
# Variables d'environnement :
#   FREELLMAPI_REPO         — dépôt git (défaut : https://github.com/tashfeenahmed/freellmapi.git)
#   FREELLMAPI_DIR          — cible (défaut : $ASPACE_INSTANCE_ROOT/services/freellmapi)
#   FREELLMAPI_PORT         — port (défaut : 3001)
#   FREEAPI_CONFIG_PATH     — freellmapi.config.json déclaratif (défaut : $STATE/freellmapi.config.json si présent)
#   FREELLMAPI_UNIFIED_KEY  — si settée, lance setup-claude + setup-codex automatiquement
#
# Migration des clés (à faire UNE fois, dans le terminal du Codespace, pas dans git) :
#   a) Exporter depuis l'app desktop : Keys → Export → JSON (35 clés)
#   b) Transformer en {"keys": [{"platform": "...", "key": "...", "label": "..."}]}
#      et placer le fichier à $ASPACE_INSTANCE_ROOT/state/freellmapi/freellmapi.config.json
#      (ou importer via la page Keys du dashboard http://localhost:3001)
#   c) Relancer ce script, récupérer la clé unifiée (header de la page Keys),
#      puis : npx freellmapi setup-claude --url http://localhost:3001 --api-key <clé>
#              npx freellmapi setup-codex  --url http://localhost:3001 --api-key <clé>
set -euo pipefail

ASPACE_INSTANCE_ROOT="${ASPACE_INSTANCE_ROOT:-/workspaces/aspace}"
FREELLMAPI_REPO="${FREELLMAPI_REPO:-https://github.com/tashfeenahmed/freellmapi.git}"
FREELLMAPI_DIR="${FREELLMAPI_DIR:-$ASPACE_INSTANCE_ROOT/services/freellmapi}"
FREELLMAPI_PORT="${FREELLMAPI_PORT:-3001}"
STATE_DIR="$ASPACE_INSTANCE_ROOT/state/freellmapi"

mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR"

# 1. Clone (sauté si déjà présent)
if [ ! -d "$FREELLMAPI_DIR/.git" ]; then
  echo "→ clone $FREELLMAPI_REPO"
  git clone --depth 1 "$FREELLMAPI_REPO" "$FREELLMAPI_DIR"
else
  echo "→ dépôt déjà présent ($FREELLMAPI_DIR), pas de re-clone"
fi

cd "$FREELLMAPI_DIR"

# 2. Dépendances + build
echo "→ npm install"
npm install --no-audit --no-fund 2>&1 | tail -2
echo "→ npm run build"
npm run build 2>&1 | tail -2

# 3. Clé de chiffrement (persistée sous state/, jamais dans git)
ENV_FILE="$STATE_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "→ génération ENCRYPTION_KEY"
  if command -v openssl >/dev/null 2>&1; then
    KEY="$(openssl rand -hex 32)"
  else
    KEY="$(node -e 'console.log(require("crypto").randomBytes(32).toString("hex"))')"
  fi
  printf "ENCRYPTION_KEY=%s\n" "$KEY" > "$ENV_FILE"
  chmod 600 "$ENV_FILE"
else
  echo "→ ENCRYPTION_KEY existante réutilisée"
fi
set -a; . "$ENV_FILE"; set +a

# 4. Config déclarative (clés provider) : import auto depuis l'export si besoin
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$STATE_DIR/freellmapi-keys.json" ] && [ ! -f "$STATE_DIR/freellmapi.config.json" ]; then
  echo "→ import de l'export vers la config déclarative"
  python3 "$SCRIPT_DIR/import-freellmapi-keys.py" \
    "$STATE_DIR/freellmapi-keys.json" "$STATE_DIR/freellmapi.config.json"
fi
if [ -z "${FREEAPI_CONFIG_PATH:-}" ] && [ -f "$STATE_DIR/freellmapi.config.json" ]; then
  export FREEAPI_CONFIG_PATH="$STATE_DIR/freellmapi.config.json"
fi
if [ -n "${FREEAPI_CONFIG_PATH:-}" ]; then
  echo "→ config déclarative : $FREEAPI_CONFIG_PATH"
else
  echo "→ pas de config déclarative (importer les clés via http://localhost:$FREELLMAPI_PORT → Keys)"
fi

# 5. Démarrage (sauté si déjà en écoute)
if curl -sf "http://localhost:$FREELLMAPI_PORT/v1/models" >/dev/null 2>&1; then
  echo "→ serveur déjà en écoute sur :$FREELLMAPI_PORT"
else
  echo "→ démarrage du serveur sur :$FREELLMAPI_PORT"
  export PORT="$FREELLMAPI_PORT"
  export FREEAPI_DB_PATH="$STATE_DIR/freeapi.db"
  nohup node server/dist/index.js >>"$STATE_DIR/server.log" 2>&1 &
  echo $! > "$STATE_DIR/server.pid"
  for _ in $(seq 1 30); do
    if curl -sf "http://localhost:$FREELLMAPI_PORT/v1/models" >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done
  curl -sf "http://localhost:$FREELLMAPI_PORT/v1/models" >/dev/null \
    && echo "→ serveur OK (pid $(cat "$STATE_DIR/server.pid"), logs : $STATE_DIR/server.log)" \
    || { echo "✗ le serveur ne répond pas — voir $STATE_DIR/server.log"; exit 1; }
fi

# 6. Générateurs de setup (seulement si la clé unifiée est fournie)
if [ -n "${FREELLMAPI_UNIFIED_KEY:-}" ]; then
  echo "→ setup-claude"
  npx -y freellmapi setup-claude --url "http://localhost:$FREELLMAPI_PORT" --api-key "$FREELLMAPI_UNIFIED_KEY"
  echo "→ setup-codex"
  npx -y freellmapi setup-codex --url "http://localhost:$FREELLMAPI_PORT" --api-key "$FREELLMAPI_UNIFIED_KEY"
else
  echo ""
  echo "Prochaines étapes (une fois les clés provider importées) :"
  echo "  1. Ouvrir http://localhost:$FREELLMAPI_PORT → Keys → récupérer la clé unifiée (header)"
  echo "  2. npx freellmapi setup-claude --url http://localhost:$FREELLMAPI_PORT --api-key <clé>"
  echo "     npx freellmapi setup-codex  --url http://localhost:$FREELLMAPI_PORT --api-key <clé>"
  echo "  (ou relancer ce script avec FREELLMAPI_UNIFIED_KEY settée)"
fi

echo ""
echo "FreeLLMAPI prêt : dashboard http://localhost:$FREELLMAPI_PORT — au côté de CubeFarm (:4417)."
