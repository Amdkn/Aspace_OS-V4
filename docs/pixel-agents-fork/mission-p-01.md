# MISSION P-01 — « Pixel Agents harness-agnostic » (pour Clara)

**Chaîne :** Bill (Discover, qualifié 2026-10-17) → Clara (Design + Architecture des Design Systems) → Nardole (Dispatch) → validation **11e Doctor** (périmètre Amy = Interfaces) → exécution par Compagnons nommés.
**Cadre :** `~/workspace/pixel-agents-fork/BEFORE-YOU-BUILD.md` · **Qualification :** `qualification-pixel-agents.md` (~15 Ko, lecture seule, aucun fork effectué).

## Objet

Designer la **couche d'adapteurs harness-agnostique** du fork Pixel Agents + **registre de harnesses à découverte dynamique**.
**Livrable :** VSIX installable dans Antigravity (première surface d'Amy dans l'IDE).
**Critère d'acceptation :** brancher un deuxième harness (non-Claude Code) **sans toucher à l'UI**.

## Découvertes (qualification)

- **Licence : MIT claire** — 4 sources concordantes (LICENSE texte intégral « Copyright (c) 2026 Pablo De Lucca », `package.json` `"license": "MIT"`, API GitHub `spdx_id: MIT`, README § License). Fork autorisé sous condition MIT (conserver copyright + notice) ; attribution personnages « based on » JIK-A-4 Metro City (itch.io). Le badge marketplace « license: invalid » = artefact d'affichage, pas une ambiguïté juridique. **Gate licence : PASS — aucun arbitrage vision requis.** Re-vérifier le VSIX publié au moment du fork (non bloquant).
- **Détection (lue dans le code, `server/src/`) : deux voies.**
  - **Hooks (défaut, push temps réel)** : `claudeHookInstaller.ts` installe (consent-gated, backup) `~/.pixel-agents/hooks/claude-hook.js` dans `~/.claude/settings.json` → POST des événements vers `POST /api/hooks/:providerId` (Fastify, bearer token `~/.pixel-agents/server.json`) → `claude.ts::normalizeHookEvent()` (**la** frontière Claude-spécifique : 11 événements → `AgentEvent` commun) → `HookEventHandler` → `SessionRouter` → `AgentRuntime`/`agentStateStore` → transport typé (AsyncAPI 3.0) → webview React.
  - **Heuristique (fallback)** : `fileWatcher.ts` (fs.watch + polling 500 ms) scanne `~/.claude/projects/*.jsonl` → `transcriptParser.ts` → `AgentEvent` ; `subagentWatch.ts` pour les sub-agents.
  - **Point clé :** `server/manual-hook-events.http` prouve que **n'importe quel harness peut POSTer des événements** sur `/api/hooks/{provider}` avec le token — porte d'entrée pour les harnesses sans hooks natifs (Compagnons, Jules).
- **Couplage dur Claude** (à répliquer par provider) : binaire `claude` (`buildLaunchCommand`), `~/.claude/settings.json`, `~/.claude/projects/`, `~/.claude/teams/`, payloads snake_case, noms d'outils (Read/Edit/Write/Bash/Task/Agent/…), `terminalNamePrefix` (adoption heuristique terminal→agent).
- **Abstraction déjà en place :** `HookProvider` (`core/src/provider.ts` : `normalizeHookEvent`, install/uninstall/consent, `formatToolStatus`, sets d'outils, `terminalNamePrefix`, `contextWindowForModel`, fallback fichier optionnel, `buildLaunchCommand`, `team?`) ; **registre `hookProviders`** (ajouter un provider = 1 sous-répertoire + 1 ligne d'export) ; `AgentEvent` (10 variantes) ; consent gate/executor provider-agnostiques ; webview déjà clé par `providerId` ; **aucune logique Claude dans le rendu** (Canvas 2D, pathfinding, state machines, éditeur de layout, assets, sons).
- **États UI émergents** (`active`/`idle`/`waiting`/`completed`/`working`/`error`/`done`) — pas un enum fermé : **à formaliser au design**.
- **TODO explicite dans le code :** `FileProvider` et `StreamProvider` à ajouter avec le premier vrai second provider (**Jules = cas naturel du StreamProvider**).

## Périmètre

**IN :**
- Design du contrat adapteur : un adapteur = une implémentation `HookProvider` + 1 entrée registre ; détection via `normalizeHookEvent` / `parseTranscriptLine` / POST manuel ; états dérivés des `AgentEvent` ; identité = `provider.id` / `displayName` ; cycle de vie `sessionStart` → events → `sessionEnd`.
- Formalisation des états en **enum fermé** (actif/idle/erreur/terminé + waiting/working/completed).
- Registre de harnesses à **découverte dynamique**.
- 3 adapteurs de référence : `companionsProvider` (9 Compagnons, shim push → `/api/hooks/companions`), `julesProvider` (StreamProvider : polling `jules.googleapis.com/v1alpha` ou bridge push), 1 harness local (Umbrel/VPS).
- VSIX installable dans Antigravity ; critère : 2e harness branché **sans toucher à l'UI** (test hold-out : l'UI ne change pas).
- Licence MIT respectée (copyright + notice conservés, attribution personnages).

**OUT :**
- Réécrire le runtime (le layering strict le permet déjà — R8).
- Le design des interfaces Amy au-delà de cette première surface (missions suivantes).
- La publication sur les marketplaces (arbitrage vision ultérieur si requis).
- Le fork lui-même pendant le design (fork après design signé, dispatch Nardole).

## Critères

- C1 — Un adapteur = une implémentation `HookProvider` + 1 ligne de registre ; **l'UI pixel ne connaît que l'interface**.
- C2 — États formalisés (enum fermé), dérivés des `AgentEvent`.
- C3 — 2e harness (non-Claude Code) branché sans toucher à l'UI (hold-out).
- C4 — VSIX installable dans Antigravity (validé).
- C5 — Licence MIT respectée (copyright + notice + attribution).
- C6 — Token du hook server traité comme un **secret** (jamais en clair dans le repo).

## Risques

- R1 — Licence : risque résiduel faible (re-vérifier le VSIX au fork ; arbitrage vision si doute).
- R2 — Dérive amont (repo actif) → **figer la version de référence au fork**.
- R3 — Token du hook server = secret (stockage, rotation).
- R4 — Fantômes de détection heuristique → politique d'adoption par harness au design.
- R5 — Point d'enregistrement + consentement par harness (à designer).
- R6 — Compatibilité Antigravity / Open VSX (à valider au design).
- R7 — Ne pas réécrire le runtime.

## Recommandation de Bill (faisabilité)

**FAISABLE — le terrain est déjà préparé.** L'extension a été conçue agent-agnostique dès le départ : `HookProvider` = « a single subdirectory of code », registre à une ligne, UI clé par `providerId`, zéro logique Claude dans le rendu. **Aucune réarchitecture requise** : N providers + états formalisés + `FileProvider`/`StreamProvider` (TODO déjà prévu dans le code). Effort estimé : **faible-modéré** pour 2–3 providers push (Compagnons, harness local), **modéré** pour le registre à découverte dynamique et le StreamProvider Jules.
