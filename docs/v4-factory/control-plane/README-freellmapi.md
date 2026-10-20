# FreeLLMAPI sur le Codespace V4 — au côté de CubeFarm

Le routeur unifié tourne **dans** le Codespace, à côté de CubeFarm (:4417).
Claude Code et Codex (déjà installés par `control-plane/setup.sh`) s'y branchent
en `localhost:3001` — zéro clé Anthropic/OpenAI à payer.

## Fichiers

| Fichier | Rôle |
|---|---|
| `control-plane/setup-freellmapi.sh` | Installe + démarre FreeLLMAPI (idempotent) |
| `control-plane/devcontainer-3001.patch` | Ajoute le port 3001 au devcontainer |

## Mise en place (3 gestes, dans le terminal du Codespace)

```bash
# 1. Placer le script (une fois le push débloqué, il sera dans le repo ;
#    en attendant, copier le fichier vers control-plane/setup-freellmapi.sh)
# 2. Appliquer le patch devcontainer (port 3001) puis rebuild si besoin
# 3. Lancer :
bash control-plane/setup-freellmapi.sh
```

## Migration des clés (une fois)

1. App desktop → Keys → **Export → JSON** → placer le fichier à
   `/workspaces/aspace/state/freellmapi/freellmapi-keys.json` (hors git).
2. Lancer `bash control-plane/setup-freellmapi.sh` : l'import est
   **automatique** (`import-freellmapi-keys.py` transforme l'export vers la
   config déclarative `freellmapi.config.json`, mode 600, déduplique les
   doublons). Idempotent : relançable quand on fabrique des centaines de clés —
   les existantes sont mises à jour, pas dupliquées.
   Alternative manuelle : ouvrir `http://localhost:3001` → page Keys → import.
3. Récupérer la **clé unifiée** (`freellmapi-…`, header de la page Keys), puis :
   ```bash
   npx freellmapi setup-claude --url http://localhost:3001 --api-key <clé-unifiée>
   npx freellmapi setup-codex  --url http://localhost:3001 --api-key <clé-unifiée>
   ```
   (Les générateurs sauvegardent la config existante et ne l'écrasent jamais.
   Ou relancer le setup avec `FREELLMAPI_UNIFIED_KEY` settée pour automatiser.)
4. Lanceurs sans persistance (clé injectée au seul process fils) :
   `npx freellmapi launch` (Claude Code), `npx freellmapi launch-codex` (Codex).

## Relier la factory à son monde 3D

- **En local (Codespace)** : `ANTHROPIC_BASE_URL=http://localhost:3001`
  (origine, sans `/v1`) + `ANTHROPIC_AUTH_TOKEN=<clé-unifiée>`.
  Ne jamais setter `ANTHROPIC_API_KEY` à côté (Claude Code refuse de démarrer).
- **Depuis les workers Actions** : passer le port 3001 en **Public**
  (onglet Ports du Codespace) → `ANTHROPIC_BASE_URL=https://<codespace>-3001.app.github.dev`.
  Fragile par design : meurt avec le Codespace (stop / 30 min d'inactivité) —
  réservé aux tests, pas à la prod. Pour du permanent : VPS/Coolify.

## Notes d'ops

- Données : `/workspaces/aspace/state/freellmapi/` (`.env` 0600, `freeapi.db`,
  `server.log`, `server.pid`). Survit au stop/rebuild, pas à la suppression.
- Redémarrage : relancer le script (idempotent) ou
  `kill $(cat /workspaces/aspace/state/freellmapi/server.pid)` puis relancer.
- Le routeur met à jour son catalogue de modèles seul (flux signé, 2×/jour).
