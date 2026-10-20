# Qualification — Fork Pixel Agents → harness-agnostic

**Mission :** Bill (holon DISCOVER) — « Fork Pixel Agents → harness-agnostic, première surface d'Amy dans l'IDE ». Go Capitaine 2026-10-17.
**Méthode :** lecture seule stricte — clone `--depth 1` dans `/tmp/pixel-agents` (aucune modification), API GitHub (`/repos/`), pages marketplace/Open VSX (texte seul). **Aucun fork effectué.**
**Source :** `pixel-agents-hq/pixel-agents` (« Pixel office. »), HEAD `main` au 2026-10-17. Publisher marketplace : `pablodelucca` (Pablo De Lucca).

---

## §1 — Licence : VERDICT (a) — claire et permissive (MIT), fork autorisé avec conditions

Quatre sources concordantes, textes exacts :

1. **Fichier `LICENSE` (racine du repo)** — texte MIT standard intégral :
   > « MIT License
   >
   > Copyright (c) 2026 Pablo De Lucca
   >
   > Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
   >
   > The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. […] »
2. **`package.json`** : `"license": "MIT"`, `"publisher": "pablodelucca"`, `"name": "pixel-agents"`.
3. **API GitHub** (`gh api /repos/pixel-agents-hq/pixel-agents`) : `"license": {"key": "mit", "spdx_id": "MIT", "name": "MIT License"}`.
4. **README § License** (miroité sur la page marketplace) : « Pixel Agents is available under the MIT License. »

**Verdict : (a).** Base légale claire. Le fork est autorisé sous l'unique condition MIT : **conserver le copyright « Copyright (c) 2026 Pablo De Lucca » et la notice de permission dans toutes les copies ou portions substantielles.**

**Le badge « license: invalid »** est un artefact d'affichage des métadonnées marketplace (le VSIX publié ne reflète pas le champ `license`, ou version antérieure du paquet) — **pas une ambiguïté juridique**. Les quatre sources source-de-vérité disent MIT. Point de vigilance (non bloquant) : re-vérifier le champ `license` du VSIX effectivement publié au moment du fork ; si le badge persiste, le signaler à l'éditeur.

**Note assets tiers :** les 6 personnages sont « based on the amazing work of JIK-A-4, Metro City » (pack itch.io, attribution dans le README). Aucun fichier de licence sprites trouvé dans le repo → **conserver l'attribution existante dans le fork** (exigé par MIT sur portions substantielles + bonne pratique).

**→ Gate licence : PASS. Aucun arbitrage vision requis sur ce point.**

---

## §2 — Architecture de détection (lue dans le code, pas les descriptions)

L'extension utilise **deux voies de détection**, documentées dans le README § « How It Works » et implémentées dans `server/src/` :

### Voie 1 — Hooks (défaut, temps réel, push)

1. **Installation (consent-gated)** : `server/src/providers/hook/claude/claudeHookInstaller.ts` (749 l.) écrit dans `~/.claude/settings.json` (champ `hooks.<Event>`) — avec backup `.pixel-agents.backup` (création exclusive, mode 0600), refus en cas de fichier illisible ou de format non-tableau. Le script hook est déposé en `~/.pixel-agents/hooks/claude-hook.js` (bundlé depuis `hooks/claude-hook.ts`, CJS + shebang).
2. **Émission** : à chaque événement Claude (`SessionStart`, `PreToolUse`, `PostToolUse`, `PermissionRequest`, `Notification`, `Stop`, `SessionEnd`, `SubagentStart/Stop`, …), le script hook **POSTe** vers le serveur Fastify local : `POST /api/hooks/:providerId` (`server/src/httpServer.ts`), authentifié par bearer token (`~/.pixel-agents/server.json` ; `server/src/serverToken.ts`, `wsAuth.ts`).
3. **Normalisation** : `server/src/providers/hook/claude/claude.ts` → `normalizeHookEvent()` — **c'est LA frontière Claude-spécifique** (11 événements Claude traduits vers le modèle commun). `HookEventHandler` (`server/src/hookEventHandler.ts`, 782 l.) vérifie le `protocolVersion` puis dispatche.
4. **Routage & état** : `server/src/sessionRouter.ts` (mapping `session_id` → `agent_id`, sessions externes en attente, buffer d'événements) → `agentRuntime.ts` + `agentStateStore.ts` (source unique de vérité, EventEmitter) → transport typé (`core/src/transport.ts`, contrat AsyncAPI 3.0 `core/src/asyncapi.yaml`, messages auto-générés `core/src/messages.ts`) → webview React (Canvas 2D, state machines de personnages).

### Voie 2 — Heuristique (fallback, polling)

- `server/src/fileWatcher.ts` (1 573 l. — hybride `fs.watch` + polling 500 ms, buffering des lignes JSONL, détection `/clear`) scanne `~/.claude/projects/<chemin-normalisé>/*.jsonl`.
- `server/src/transcriptParser.ts` (741 l.) parse les lignes JSONL → `AgentEvent`.
- `server/src/subagentWatch.ts` (215 l.) pour les sub-agents ; « Watch All Sessions » via `getAllSessionRoots()` (`~/.claude/projects`).
- `AgentState.hooksOnly` : agent sans transcript (état 100 % hooks) ; `hookDelivered` : supprime les timers heuristiques (permission 7 s, idle 5 s).

### Couplage dur avec Claude Code (dépendances à remplacer par adapteur)

| Dépendance | Fichier | Détail |
|---|---|---|
| Binaire `claude` | `claude.ts` → `buildLaunchCommand()` | `claude --session-id <id> [--dangerously-skip-permissions]`, env `PWD=cwd` |
| `~/.claude/settings.json` | `claudeHookInstaller.ts` | installation des hooks (mutation du fichier utilisateur) |
| `~/.claude/projects/` | `claude.ts` → `getSessionDirs()`, `getAllSessionRoots()` | transcripts JSONL, `normalizeProjectPath()` |
| `~/.claude/teams/<nom>/config.json` | `claudeTeamProvider.ts` (272 l.) | Agent Teams |
| Payloads snake_case des hooks Claude | `claude.ts` → `normalizeHookEvent()` | 11 événements |
| Noms d'outils Claude | `claude.ts` → `formatToolStatus()`, `permissionExemptTools`, `subagentToolNames` (`Task`/`Agent`), `readingTools` | statuts affichés, animations lecture/écriture |
| Fenêtre de contexte par modèle | `claude.ts` → `contextWindowForModel()` | jauge de contexte dans l'UI |
| Terminaux VS Code | `adapters/vscode/vscodeTerminalAdapter.ts` (14 l.), `agentManager.ts` (565 l.) | lancement + `terminalNamePrefix` (adoption heuristique terminal→agent) |

### Générique (ne change pas d'un harness à l'autre)

Runtime, store, router, transport, persistance `~/.pixel-agents/` (JSON), webview (rendu, layout editor, assets, sons), consent gate/executor, contrat AsyncAPI.

### Porte d'entrée pour harnesses sans hooks natifs (point clé)

`server/manual-hook-events.http` documente que **n'importe quel processus peut POSTer des événements** sur `/api/hooks/{provider}` avec le token serveur (`SessionStart` stage une session externe en attente ; `PreToolUse`/`Stop`/`Notification`/`PermissionRequest` la confirment et créent l'agent). **C'est le mécanisme d'injection pour les harnesses sans API de hooks (Compagnons, Jules)** — pas besoin d'attendre un `StreamProvider`.

---

## §3 — Inventaire abstraction : ce qui s'abstrait vs ce qui reste dans l'UI

### Déjà découplé — l'UI ne connaît que l'interface

- **`HookProvider`** (`core/src/provider.ts`) — **l'interface d'intégration officielle** : `kind`/`id`/`displayName`/`protocolVersion`, `normalizeHookEvent(raw)` → `AgentEvent`, `installHooks(serverUrl, authToken)` / `uninstallHooks()` / `areHooksInstalled()` / `consentDisclosure()` (requis, non optionnel), `formatToolStatus()`, `permissionExemptTools` / `subagentToolNames` / `readingTools` (ReadonlySet), `terminalNamePrefix?`, `contextWindowForModel?`, fallback fichier optionnel (`getSessionDirs?`, `getAllSessionRoots?`, `sessionFilePattern?`, `parseTranscriptLine?`), `buildLaunchCommand?`, `team?: TeamProvider`.
- **Registre** (`server/src/providers/index.ts`) : ajouter un provider = **un sous-répertoire + une ligne d'export** (`hookProviders: readonly HookProvider[] = [claudeProvider]`). Le consent gate boucle dessus (un ask par provider).
- **`AgentEvent`** (10 variantes, `core/src/provider.ts`) : `toolStart` / `toolEnd` / `turnEnd` (`awaitingInput?`) / `subagentStart` / `subagentEnd` / `subagentTurnEnd` (`idle|completed`) / `progress` / `permissionRequest` / `sessionStart` (`sessionId`, `transcriptPath?`, `cwd?`) / `sessionEnd` (`reason?`).
- **États UI observés** (dérivés des AgentEvent par les state machines) : `'active'` (28 occ.), `'idle'` (25), `'waiting'` (24), `'completed'` (4), `'working'` (3), `'error'` (2), `'done'` (2) — modèle émergent, **pas un enum fermé** (à formaliser dans le design : actif/idle/erreur/terminé + en-attente).
- **Consent** provider-agnostique (`consentGate.ts`, `consentExecutor.ts`) ; `TeamProvider` optionnel (`core/src/teamProvider.ts`) ; `StateAdapter` (persistance), `TerminalAdapter` (terminaux), `MessageTransport` + AsyncAPI.
- **Webview** : `useExtensionMessages.ts` déjà clé par `providerId` (le checkbox Settings « claude » est `keyed by providerId` — prévu pour le multi-provider) ; 15 fichiers webview-ui mentionnent « claude » (labels à passer en `displayName` du provider au design).
- **Ce qui reste dans l'UI (ne pas abstraire)** : rendu Canvas 2D, pathfinding, state machines de personnages, éditeur de layout, packs d'assets, sons — aucune logique métier Claude dans le rendu.

### Soudé à Claude — à répliquer par provider sous `server/src/providers/hook/<id>/`

- `claude.ts` (319 l.), `claudeHookInstaller.ts` (749 l.), `hooks/claude-hook.ts`, `claudeTeamProvider.ts` (272 l.), `consentCopy.ts`, `constants.ts`.
- `transcriptParser.ts` + `fileWatcher.ts` : formats JSONL Claude (l'interface `parseTranscriptLine` est générique, l'implémentation est Claude-spécifique).
- **TODO explicite dans le code** (`core/src/provider.ts`) : `FileProvider` (CLIs en polling seul) et `StreamProvider` (services externes push) « seront ajoutés avec le premier vrai second provider » — le design Clara peut les introduire (Jules = cas d'usage naturel du StreamProvider).

### Contrat adapteur proposé (pour le typage Clara)

Un adapteur = **une implémentation `HookProvider`** (ou futur `FileProvider`/`StreamProvider`) + **une entrée au registre** (`hookProviders`). L'UI pixel ne connaît que `AgentEvent` + `HookProvider`.
- **Détection** : `normalizeHookEvent()` (push) et/ou `parseTranscriptLine()` + `getSessionDirs()` (fichier) ; injection manuelle possible via `POST /api/hooks/{providerId}`.
- **États** : dérivés des `AgentEvent` — actif (`toolStart` sans `toolEnd`), idle (`turnEnd` sans `awaitingInput`), en-attente (`turnEnd` avec `awaitingInput` | `permissionRequest`), erreur (`sessionEnd` avec motif / `error`), terminé (`sessionEnd`).
- **Identité du harness** : `provider.id` / `displayName` (+ `terminalNamePrefix` pour l'adoption terminal).
- **Cycle de vie** : `sessionStart` → événements → `sessionEnd` / `turnEnd`.

### Mapping vers les cibles A'Space

| Cible | Voie recommandée | Notes |
|---|---|---|
| **9 Compagnons** | `companionsProvider` (HookProvider) + **shim push** : un émetteur léger POSTe les événements sur `/api/hooks/companions` avec le token serveur (mécanisme déjà documenté par `manual-hook-events.http`) | Pas de hooks natifs côté Compagnons ; le shim traduit le cycle de vie des sessions (Bill/Clara/…) en AgentEvent. Alternative : `FileProvider` sur un fichier d'état. |
| **Jules** | `julesProvider` : **StreamProvider/polling** sur `jules.googleapis.com/v1alpha` (ressources Session) — à créer (le TODO du code le prévoit) ; ou bridge push → `/api/hooks/jules` | Jules n'a pas de hooks ; le polling REST est la voie naturelle (cf. mission G-02-C : l'intégration V4 déclenche déjà Jules en REST). |
| **Harnesses locaux (Umbrel/VPS)** | un provider par harness (OpenClaw, Hermes…) : hooks si le harness en expose, sinon push via `/api/hooks/{id}` ou `FileProvider` sur ses logs/états | La découverte dynamique (registre de harnesses) est l'extension du registre statique `hookProviders`. |

---

## §4 — Risques

- **R1 — Licence (résiduel faible)** : le badge « license: invalid » ne reflète pas une ambiguïté juridique (4 sources MIT concordantes), mais **re-vérifier le champ `license` du VSIX publié au moment du fork** ; si doute subsiste → arbitrage vision via A0 AVANT tout fork (conformément à la mission). Conserver l'attribution JIK-A-4 des sprites.
- **R2 — Dérive amont** : repo actif (push 2026-10-17), roadmap « Codex, Gemini, Cursor » → le fork doit figer une version de référence (tag/commit) et prévoir la politique de rebase ; risque de convergence/divergence avec l'amont.
- **R3 — Sécurité du hook server** : bearer token dans `~/.pixel-agents/server.json` ; en standalone, `--host 0.0.0.0` expose UI+WS au LAN (documenté comme risqué par l'éditeur). Les adapteurs Compagnons/Jules manipulent ce token comme un **secret** (jamais en clair dans les logs).
- **R4 — Faux positifs de détection** : l'adoption heuristique (`terminalNamePrefix`, « Watch All Sessions ») peut créer des personnages fantômes → le design doit définir la politique d'adoption par harness (qui crée un personnage, quand).
- **R5 — États non formalisés** : 7 statuts observés, aucun enum fermé → Clara doit figer le contrat d'états (actif/idle/erreur/terminé + en-attente) dans le design.
- **R6 — Installation des hooks** : écrit dans `~/.claude/settings.json` (consent-gated + backup) → pour chaque harness A'Space, définir **où** l'adapteur s'enregistre et avec quel consentement explicite (doctrine).
- **R7 — Antigravity / Open VSX** : l'extension cible VS Code `^1.105.0` ; compatibilité Antigravity (fork VS Code) et publication Open VSX (première surface d'Amy) à valider **au design**, pas au Discover.
- **R8 — Portée** : le fork ne doit pas réécrire le runtime — l'architecture le permet déjà (layering strict : `core/` sans effets de bord, `server/` ne dépend que de `core/`).

---

## §5 — Recommandation de faisabilité : FAISABLE (terrain déjà préparé)

L'extension a été **conçue agent-agnostique dès le départ** : le README l'affirme (« a typed `HookProvider` interface defines the integration boundary so adding a new AI tool is a single subdirectory of code ») et le code le confirme (registre à une ligne, consent provider-agnostique, UI clé par `providerId`, `AgentEvent` générique). Le fork harness-agnostique ne demande **aucune réarchitecture** : implémenter N providers + formaliser les états + introduire `FileProvider`/`StreamProvider` (TODO déjà prévu dans le code).

- **Effort estimé** : faible-modéré pour 2–3 providers push (Compagnons via `POST /api/hooks/companions`, Jules via polling REST ou bridge push) ; modéré pour le registre de harnesses à découverte dynamique (extension du registre statique actuel).
- **Gate licence** : PASS (MIT) — aucun arbitrage vision requis avant fork sur ce point.
- **Condition** : figer la version amont de référence au moment du fork (R2) et traiter le token du hook server comme un secret (R3).
