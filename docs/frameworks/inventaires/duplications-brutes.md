# D-N016 phase 1 — Inventaire brut des duplications inter-OS

**Mission :** Bill (holon DISCOVER) — D-N016 phase 1, ordre direct Capitaine via Nardole · Agora.
**Date :** 2026-10-09 ~16:10 EDT.
**Règle de phase :** inventaire seul — pas de design, pas de code, pas de proposition de solution (phase 2 = Clara).

## Source primaire

**`main` @ `2554e0f`** (« Merge pull request #66 from Amdkn/jules-2709487073187738769-eaa8859e »,
Amdkn/Aspace_OS-V4) — vérifié au niveau git le 2026-10-09 ~16:25 EDT sur clone frais
(`/tmp/v4check`, éphémère) : `os/` à la racine avec `PORTS.md`, `agent/`, `business/`,
`capabilities.registry.json`, `life/`.

La lecture a été conduite sur la copie locale `~/workspace/v4-factory/s3/rory/verify-57-repo/os/`.
**Comparaison d'arborescences** (`git ls-tree -r HEAD os/` vs `git hash-object` local,
1870 fichiers) : **96 chemins diffèrent** — la copie locale est antérieure à `main`
(commits post-VERIF-57 : PR #33, #58, #66). Écarts substantiels : `os/agent/src/shell/`
(`Dock.tsx`, `store.ts`, `dockSkins.ts` — voir §1), `os/agent/src/apps/{TechOSWorkflows,
TechOSDocs}`, `os/life/src/apps/para/` (ParaApp V0.4.1), `os/life/src/stores/`
(`fw-gtd.store.ts` V0.7.1, `os-settings.store.ts`). Le reste = artefacts d'encodage
(BOM/fins de ligne). **Toutes les conclusions structurelles ci-dessous ont été
re-vérifiées contre `main@2554e0f`** (existence des fichiers + en-têtes via `git show`) ;
les chemins cités sont ceux de `main`.

**Erratum :** une première vérification (~16:05 EDT) avait conclu à l'absence de `os/`
sur `main` sur la base de 404 API — ces appels utilisaient des URLs malformées
(préfixe `/repos/` manquant). Leçon consignée : **un 404 API n'est pas une preuve
d'absence** — toujours valider l'endpoint avant de conclure.

**Référence croisée :** 3 échantillons comparés byte-identiques (`diff -q`) entre `os/` et
les sources standalone (`agent-os-size`, `business-os-size`, `life-os-audit`) :
`agent/src/apps/CoachOS/index.tsx`, `business/src/agent/scenarios.ts`, `life/src/apps/auth/FirstLaunch.tsx`.
Provenance : `os/agent/IMPORT.json` et `os/business/IMPORT.json` présents (source-lock) ;
`os/life/IMPORT.json` absent (D-N011 ouvert).

## DUPLICATIONS FORTES

### 1. Desktop shell complet — business ∥ agent
- **business :** `os/business/src/components/` — `Desktop.tsx` (189 l.), `DesktopIcons.tsx`, `Dock.tsx`, `TopBar.tsx`, `TopBarMenu.tsx`, `Wallpaper.tsx`, `WindowFrame.tsx`, `AppDrawer.tsx`, `Breadcrumbs.tsx`, `NotificationsDropdown.tsx`, `ContextMenu.tsx`, `Toast.tsx`, `ErrorBoundary.tsx`
- **agent :** `os/agent/src/shell/` — `Desk.tsx`, `DeskIcons.tsx`, `Dock.tsx`, `MenuBar.tsx`, `NotificationsDropdown.tsx`, `CommandPalette.tsx`, `AppDrawer.tsx`, `Breadcrumbs.tsx`, `AppLayout.tsx`, `store.ts`, `wallpaper.ts`, `dockSkins.ts`
- **Overlap :** deux kits de composants shell desktop parallèles (bureau, dock, barre, fenêtres, notifications, tiroir d'apps). Business OS embarque son propre shell alors qu'Agent OS est le shell canonique. **Sur `main@2554e0f`, la convergence est active et documentée dans le code :** l'en-tête de `os/agent/src/shell/Dock.tsx` dit *« Upgraded to BusinessOS standard : 20 UI/UX Pro Max skins from dockSkins.ts… »* et `dockSkins.ts` précise *« Les mêmes vingt styles que la vitrine de l'app Design »* — le shell Agent importe les standards BusinessOS au lieu d'un socle canonique unique.
- **Confiance : FORT**

### 2. Système de thèmes — business → agent (porté) ∥ life (parallèle)
- **business (source) :** `os/business/src/apps/settings/theme-details.tsx`, `ThemeDetailPage.tsx`
- **agent :** `os/agent/src/themes/{store.ts, tokens.ts, ThemeApplier.tsx}` — l'en-tête de `tokens.ts` dit littéralement : *« 12 thèmes canoniques portés depuis BusinessOS »*
- **life :** `os/life/src/themes/theme-tokens.ts` (`THEME_TOKENS` : solarpunk/cyberpunk/…) + `os/life/src/stores/os-settings.store.ts`
- **Overlap :** trois systèmes de thèmes, deux lignées (port BusinessOS→Agent, implémentation Life indépendante).
- **Confiance : FORT**

### 3. Explorateur d'ontologie — business ∥ agent
- **business :** `os/business/src/apps/ontology/OntologyApp.tsx` (621 l. — Entities/Relations/Contracts/Versions), adossé à `os/business/src/lib/ontology/{entities.ts, relations.ts, contracts.ts, index.ts, scope-store.ts}` + tests (`architecture.test.ts` verrouille les boundaries)
- **agent :** `os/agent/src/apps/Onthology/index.tsx` (2236 l. — style Palantir : lineage, framework, mining, explorer, contour, vertex, workshop, quiver)
- **Overlap :** même capacité (graphe de connaissances / ontologie explorable), deux implémentations sans dépendance commune.
- **Confiance : FORT**

### 4. Paramètres système — business ∥ agent
- **business :** `os/business/src/apps/settings/{SettingsApp.tsx, AssistantSettings.tsx, SettingsItemDetail.tsx, ThemeDetailPage.tsx, theme-details.tsx, seed.ts}`
- **agent :** `os/agent/src/apps/Settings/index.tsx` (« Paramètres Système » : thèmes, wallpapers, environnement, `dockSlot: 99`)
- **Overlap :** deux apps Paramètres couvrant les mêmes réglages (thèmes, apparence, préférences).
- **Confiance : FORT**

### 5. Hébergement Coach OS (embed vs canonique) — business (source) ∥ agent (embed)
- **business :** le code Coach OS — `os/business/coach-os-plugin/skills/` (app.list/open, collection.*, scenario.approve/list/read/reject, section.goto), `os/business/src/agent/`, `os/business/api/v1/`, `coach-os.bat`
- **agent :** `os/agent/src/apps/{CoachOS, CoachOSOnline}/index.tsx` — simples `Cadre` pointant vers `localhost:5174` et Vercel (`omk-desktop-web-os.vercel.app`)
- **Overlap :** Agent OS ré-héberge Coach OS par encapsulation au lieu d'une intégration canonique unique. Duplication architecturale (pas de code dupliqué, deux chemins d'accès).
- **Confiance : FORT**

### 6. Hébergement Life OS Engagement dans Agent OS — life (source) ∥ agent (embed)
- **life :** surface d'engagement complète — `os/life/src/App.tsx`, `os/life/src/apps/{auth, para}/`, shell store, thèmes
- **agent :** `os/agent/src/apps/{LifeOS, LifeOSOnline}/index.tsx` — `Cadre` vers `127.0.0.1:4444` / Vercel (`life-os-2026-amd-lab.vercel.app`), avec le commentaire *« L'app n'est qu'une encapsulation : Life OS existe, on ne le refait pas »* ; `os/agent/src/apps/Doctor11Life/index.tsx` — cockpit 11e/Amy/Rory/River parallèle au cœur Life
- **Overlap :** la surface d'engagement Life (shell, PARA, auth) est re-hébergée dans Agent OS ; Doctor11Life duplique la structure d'autorité du cœur Life (11e/Amy/Rory/River).
- **Confiance : FORT**

## DUPLICATIONS MOYENNES

### 7. Auth UX — business ∥ life
- **business :** `os/business/src/apps/auth/{AuthPage.tsx (270 l.), OAuthCallback.tsx, FOURNISSEURS.md}`
- **life :** `os/life/src/apps/auth/{FirstLaunch.tsx (107 l.), LandingPage.tsx, MigrationScreen.tsx}`
- **Overlap :** deux parcours d'authentification / first-launch parallèles.
- **Confiance : MOYEN**

### 8. Roster d'agents — business ∥ agent
- **business :** `os/business/src/agent/{characters.ts, roster.test.ts}`
- **agent :** `os/agent/src/apps/SubagentsRoster/{index.tsx, AgentCard.tsx}` (cockpit 14 subagents : Rick, 3 Docteurs, 10 Compagnons)
- **Overlap :** deux modélisations du roster d'agents (personnages vs cockpit d'orchestration).
- **Confiance : MOYEN**

### 9. Dashboard / building blocks — business ∥ agent
- **business :** `os/business/src/apps/dashboard/{dashboard, platform}/` (AgentDetail, Chat, CapabilitiesPanel, ContextPanel, seeds)
- **agent :** `os/agent/src/blueprints/{DataGrid.tsx, KanbanBoard.tsx, MetricCard.tsx, BlueprintAppFactory.tsx, templateManager.ts, types.ts}`
- **Overlap :** deux kits de construction de tableaux de bord (cartes métriques, grilles, kanban).
- **Confiance : MOYEN**

### 10. Harness — business ∥ agent
- **business :** `os/business/harness/adws/` (+ `adws/adw_modules`, `adw_data`, `adw_sssf_config`)
- **agent :** `os/agent/src/apps/{CanaryHarness, DeepSeekHarness}/` (E2E canary, fixtures, `useRuntimePresence`, `contracts/truth`)
- **Overlap :** deux infrastructures de harness (exécution déterministe + fixtures), sans socle commun.
- **Confiance : MOYEN**

### 11. Tâches / GTD — business ∥ life
- **business :** `os/business/src/apps/tasks/{TasksApp.tsx, TasksDetailPage.tsx, TasksItemDetail.tsx, seed.ts}`
- **life :** `os/life/src/stores/fw-gtd.store.ts` (framework GTD)
- **Overlap :** gestion des tâches implémentée des deux côtés (app métier vs store framework).
- **Confiance : MOYEN**

### 12. Voix / TTS — business ∥ agent (réserve)
- **business :** `os/business/src/agent/{voice.ts, voice.test.ts, VoiceWave.tsx}`
- **agent :** mentions voix/TTS dans `os/agent/src/apps/AgenticOS/` (`WarRoomDrawer.tsx`, bascule « flux audio TTS Daemon » dans `src/cms/hierarchy.ts`)
- **Overlap :** capacité vocale présente des deux côtés, intégrations différentes ; pas de module voix unifié côté agent vérifié.
- **Confiance : MOYEN (réserve — échantillon partiel)**

## FAIBLES / ADJACENTS (pas de duplication fonctionnelle établie)

- **Landing / welcome :** `os/business/src/{landing, site}` + `src/apps/welcome` vs `os/life/src/apps/auth/LandingPage.tsx` — surfaces marketing parallèles. FAIBLE.
- **Observers :** `os/agent/src/apps/{Observers, PostHogObservatory}` + `src/observers.json` vs `os/business/src/apps/dashboard/platform` — observabilité éclatée, pas de recouvrement fonctionnel direct. FAIBLE.
- **Contrats :** `os/agent/src/contracts/truth.ts` (zod : SystemStatus, WritePathAuthority, fingerprint) vs `os/life/src/contracts/crossCategoryEvents.ts` + `src/types/capabilities.ts` — couches « contrats » adjacentes, périmètres différents. FAIBLE (adjacent).
- **API layers :** `os/business/api/v1/` (manifest d'outils REST coach-os) vs `os/agent/src/api/projection.ts` (projection tech-os) vs `os/life/src/lib/api/client.ts` (bridge 127.0.0.1:3001) — finalités différentes. FAIBLE (adjacent).
- **Mémoires :** `os/agent/src/apps/Memories` (durable layer locale, `storage/contract`) vs `os/life/src/lib/blackboard/client.ts` + `os/life/server/blackboard/` (:4445, bus temps réel partagé) — sémantiques différentes (durable local vs bus partagé). Adjacent, pas duplication.

## INNOVATIONS NON DUPLIQUÉES (à préserver telles quelles — input D-N014/Clara phase 2)

- **Life-only (11 capabilities 🛡, `capabilities.registry.json`) :** `capability-contract` (`services/clara/`), `capability-factory` (`services/ryan/`), `flow-engine` (`services/river/`), `evidence-store` (`services/rory/`), `workgraph-adapter`, `river-adapter` (×2), `life-business-bridge`, `canary-holon`, `wargame-runner` — **zéro occurrence dans business/agent (grep vide).**
- **Business-only :** `src/agent/scenarios.ts` (exécution atomique tout-ou-rien avec revert, testée), `src/agent/AssistantOverlay.tsx`, `src/apps/onboarding/tours/{threeTours.ts, helpers.ts}`, skills `scenario.approve/reject` (coach-os-plugin).
- **Agent-only :** `src/shell/store.ts` + `CommandPalette.tsx`, `src/cms/hierarchy.ts` (generateCmsHierarchy), `src/storage/contract.ts`.

## COLLISION DE NOMMAGE (pas une duplication — point de gouvernance pour D-N014)

- **« Workspace » :** `os/agent/src/apps/Workspace/` = mini-SaaS multi-tenant conversationnel (gateway Hermes, `mapping.json` des compagnons) ; `os/business/src/apps/workspace/` = gestion branches/PRs/merges (`lib/workspace/`, `branches.store.ts`). Même nom, responsabilités disjointes → à renommer ou typer dans l'architecture cible.
