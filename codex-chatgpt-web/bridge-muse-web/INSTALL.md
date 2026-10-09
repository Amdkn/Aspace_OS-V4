# INSTALL — bridge muse_web sur ta machine

## Prérequis

- Bun 1.4+ (voir bun.sh/docs/installation)
- Playwright + Chromium : `bunx playwright install chromium`
- Un compte muse.ai (le tien)

## Installation

```sh
# 1. Cloner TON fork (déjà existant — blocker #410 levé le 2026-10-09)
git clone https://github.com/Amdkn/codex-chatgpt-web.git bridge && cd bridge
# Fork vérifié : public, "forked from miuuyy/codex-chatgpt-web".
# Le scaffold de l'adapter muse_web vit aussi ici :
# ~/workspace/v4-factory/bridge-muse-web/ (à pousser dans le fork quand tu veux).

# 2. Dépendances
bun install
bunx playwright install chromium

# 3. Renseigner les sélecteurs
#    Éditer src/surfaces/muse-web/selectors.json
#    à partir de SELECTORS.md (inspection DOM réelle).
```

## Premier lancement (login une fois)

```sh
BRIDGE_PROFILE_DIR=./.bridge-profile bun src/server.ts
```

Le navigateur s'ouvre **visible** : connecte-toi à muse.ai à la main, une fois.
Le profil est persisté dans `.bridge-profile/` — les lancements suivants
sont silencieux.

## Utilisation avec Claude Code

```sh
ANTHROPIC_BASE_URL=http://127.0.0.1:8741 \
ANTHROPIC_AUTH_TOKEN=bridge-local \
claude "dis bonjour"
```

Chaque session Claude Code utilise le side chat **« Claude Code Bridge »**
(dédié, créé automatiquement) — ton Main chat n'est jamais pollué.

## Dépannage

- `pas de session muse.ai détectée` → relance avec le navigateur visible et logge-toi.
- `aucune réponse assistant détectée` → un sélecteur a dérivé : mets à jour
  `selectors.json` depuis SELECTORS.md (jamais de contournement silencieux).
- Réponse lente : normal en v1 — A0 utilise ses propres outils avant de répondre.
