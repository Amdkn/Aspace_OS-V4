# P-01 — Plan borné : Pixel Agents harness-agnostic

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation **11e Doctor** [périmètre Amy = Interfaces]) — 2026-10-17
**Source :** mission Rick (S1) ; Discover Bill (`~/workspace/pixel-agents-fork/qualification-pixel-agents.md`, `mission-p-01.md` ; note vocale transcrite — confirme le dossier écrit, sans instruction nouvelle)
**Gate licence : PASS (MIT, 4 sources concordantes) — aucun arbitrage vision requis.** Fork autorisé : conserver copyright « Copyright (c) 2026 Pablo De Lucca » + notice + attribution « based on » JIK-A-4 Metro City.
**Terrain : aucune réarchitecture requise** — `HookProvider`, registre à 1 ligne, UI clé par `providerId`, zéro logique Claude dans le rendu.
**Scope Capitaine (2026-10-17) : 9 harnesses cibles** — Antigravity CLI, Hermes, OpenClaw, Spacebot, Prime Agents, Pi coding agent, Codex CLI, Claude, DeepSeek harness (remplacent les 3 adapteurs de référence). **Fait d'architecture :** le Capitaine alimente ces harnesses avec son agrégateur de tokens gratuits multi-providers — l'adapteur s'inscrit dans cet écosystème : il porte l'**identité** et la **comptabilité** par harness (qui consomme quoi, traçabilité), **sans facturation** (l'allocation/monétisation reste son domaine).
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Contrat adapteur (figé) — identité + comptabilité, sans facturation.** Un adapteur = **une implémentation `HookProvider`** (ou `FileProvider`/`StreamProvider` une fois introduits) + **une entrée au registre**. L'UI pixel ne connaît que `AgentEvent` + `HookProvider` + l'enum d'états fermé. **Identité** : `provider.id` / `displayName` / **`accountingId`** (identifiant stable de comptabilité — traçabilité de qui consomme quoi) + `terminalNamePrefix` pour l'adoption terminal. **Comptabilité** : l'adapteur émet des **faits de consommation** (harness X, session Y, N tokens, horodatage) via `usage?` en métadonnée d'`AgentEvent` — **uniquement ce que le harness expose** ; aucune donnée = aucun événement émis, **jamais de chiffre inventé**. **Ce n'est pas un système de facturation** : pas de prix, pas de quotas, pas d'allocation — l'agrégateur de tokens et la monétisation restent l'infrastructure et le domaine du Capitaine ; l'adapteur ne route pas de tokens, ne choisit pas de providers. L'UI pixel ignore ces métadonnées (une future surface comptable, domaine Capitaine, les consommera). Détection : `normalizeHookEvent()` (push) et/ou `parseTranscriptLine()` + `getSessionDirs()` (fichier) et/ou POST manuel sur `/api/hooks/{providerId}`. Cycle de vie : `sessionStart` → événements → `sessionEnd`.
2. **États en enum fermé (5 valeurs, dérivées des `AgentEvent`)** — formalise les 7 états émergents :
   - `actif` — `toolStart` sans `toolEnd` (couvre `active` + `working`)
   - `inactif` — `turnEnd` sans `awaitingInput` (couvre `idle`)
   - `en_attente` — `turnEnd` avec `awaitingInput` OU `permissionRequest` en suspens (couvre `waiting`)
   - `erreur` — événement `error` ou `sessionEnd` avec motif d'échec (couvre `error`)
   - `terminé` — `sessionEnd` propre (couvre `completed` + `done`)
   Aucun état en littéral string hors enum dans le code UI.
3. **Passe de généralisation UI (une fois, P1)** : les 15 fichiers webview mentionnant « claude » → labels = `displayName` du provider. **Après cette passe**, brancher un harness = zéro diff UI (c'est ce que le hold-out C3 vérifie — le critère porte sur l'ajout, pas sur la passe initiale).
4. **Registre à découverte dynamique** : remplace le tableau statique `hookProviders` par `discoverProviders()` — scan de `server/src/providers/hook/*/` (chaque sous-répertoire exporte un `HookProvider`) + manifeste pour les providers push-only (shim Compagnons). Validation au chargement : `id` unique, `protocolVersion` conforme, `consentDisclosure()` présent ; invalide → erreur claire, **jamais chargé silencieusement**. Consent gate par provider conservé (un ask par provider).
5. **9 adapteurs cibles (scope Capitaine)** : `antigravityCli` (Antigravity CLI), `hermes` (Hermes), `openclaw` (OpenClaw), `spacebot` (Spacebot), `primeAgents` (Prime Agents), `piCoding` (Pi coding agent), `codexCli` (Codex CLI), `claude` (Claude — provider existant = implémentation de référence), `deepseek` (DeepSeek harness). **Voie d'intégration par harness à qualifier à l'exécution** (P0) selon le catalogue : hooks natifs → `HookProvider` ; pas de hooks → push via `/api/hooks/{id}` (mécanisme documenté) ou `FileProvider` sur logs/états ; API distante → `StreamProvider` polling. Aucune capacité inventée : voie inconnue = « à qualifier », pas devinée. Les patterns des 3 adapteurs de référence initiaux (push Compagnons, polling Jules) restent valides comme gabarits.
6. **Token = secret (C6)** : lu depuis `~/.pixel-agents/server.json` par le serveur uniquement ; transmis aux adapteurs via env/canal sécurisé — **jamais en dur, jamais en repo, jamais en clair dans les logs** (redaction). Rotation documentée.
7. **Politique anti-fantômes (R4)** : un personnage n'est créé que sur `sessionStart` **+ un événement de confirmation** ; les détections heuristiques seules restent en attente, ne créent jamais ; adoption terminal uniquement sur `terminalNamePrefix` correspondant.
8. **Consentement par harness (R5)** : `consentDisclosure()` requis par adapteur + point d'enregistrement documenté par harness (où l'adapteur s'enregistre, avec quel consentement explicite).
9. **MIT (C5/R1)** : LICENSE + notice conservées dans toutes les copies ; attribution JIK-A-4 conservée ; **re-vérifier le champ `license` du VSIX publié au moment du fork** — si doute subsiste → arbitrage vision via A0 **AVANT** tout fork (gate).
10. **Gel de la référence amont (R2)** : tag/commit figé au fork ; politique de rebase documentée (pas de dérive silencieuse).
11. **Pas de réécriture du runtime (R7)** : ajouts uniquement (providers, enum, découverte) — runtime, store, transport, rendu webview intouchés.
12. **Antigravity (C4/R6)** : VSIX ciblant VS Code `^1.105.0` ; validé par installation + activation + smoke test dans Antigravity. Publication marketplaces = OUT (arbitrage vision ultérieur).

## 1. Bornes

**IN :** contrat adapteur (identité + comptabilité, sans facturation) + enum fermé + passe de généralisation UI + registre dynamique + **9 adapteurs cibles** (Antigravity CLI, Hermes, OpenClaw, Spacebot, Prime Agents, Pi coding agent, Codex CLI, Claude, DeepSeek) + VSIX validé Antigravity + checklist MIT + gel référence + politique token/consentement/fantômes.
**OUT :** réécrire le runtime ; design Amy au-delà de cette surface ; publication marketplaces ; fork pendant le design (fork après design signé, dispatch Nardole).

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Contrat (`core/`)**
- `HookProvider` + `StreamProvider`/`FileProvider` (réalise le TODO du code) ; `AgentEvent` = seul modèle connu de l'UI ; enum fermé 5 états (§0.2).

**Système 2 — Registre dynamique (`server/src/providers/`)**
- `discoverProviders()` (scan + manifeste push-only) ; validation au chargement (id unique, protocolVersion, consentDisclosure) ; consent gate par provider.

**Système 3 — 9 adapteurs cibles**
- `antigravityCli`, `hermes`, `openclaw`, `spacebot`, `primeAgents`, `piCoding`, `codexCli`, `claude` (existant = référence), `deepseek` — voie d'intégration qualifiée à l'exécution P0 (catalogue : hooks natifs / push `/api/hooks/{id}` / `FileProvider` / `StreamProvider` polling) ; chaque adapteur porte `accountingId` et émet les faits de consommation que son harness expose.

**Système 4 — Packaging & conformité**
- Build VSIX, validation Antigravity, checklist MIT (copyright + notice + attribution + champ `license` du VSIX), gel référence amont, gestion du token comme secret.

**Flux :** P0 (fork : licence re-vérifiée + ref gelée + qualification des 9 voies) → P1 (contrat identité/comptabilité + généralisation UI) → P2 (registre) → P3 (9 adapteurs) → P4 (VSIX + Antigravity) → P5 (validation 11e Doctor → dispatch Nardole).

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Fork + qualification (exécution, après validation)** | Re-vérifier le champ `license` du VSIX publié (doute → arbitrage vision via A0 AVANT fork) ; figer tag/commit amont ; fork (dispatch Nardole) ; **qualifier la voie d'intégration de chacun des 9 harnesses** (hooks natifs ? push ? fichier ? API ?) — voie inconnue = « à qualifier », jamais devinée | H-P01-7 |
| **P1 — Contrat** | Enum fermé 5 états ; `StreamProvider`/`FileProvider` ; identité + comptabilité (`accountingId`, `usage?` — sans facturation) ; passe de généralisation UI (labels → `displayName`) | H-P01-1, H-P01-2, H-P01-12, H-P01-13 |
| **P2 — Registre** | `discoverProviders()` + manifeste push-only + validation au chargement + consent par provider | H-P01-4 |
| **P3 — Adapteurs** | Les 9 adapteurs (vagues selon la qualification P0 — `claude` existant = référence) ; `accountingId` + faits de consommation par adapteur ; politique anti-fantômes ; consentement par harness ; token comme secret | H-P01-5, H-P01-6, H-P01-8, H-P01-9, H-P01-12 |
| **P4 — VSIX** | Build + installation/activation/smoke test dans Antigravity | H-P01-10 |
| **P5 — Validation** | Revue 11e Doctor (périmètre Amy = Interfaces) → Nardole dispatche la validation | Tous verts |

**Règle d'exécution :** séquentiel, un seul exécutant. `OWNER_STAND_DOWN=1` arrête tout.

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-P01-1 | Contrat adapteur | chaque adapteur = 1 implémentation `HookProvider` + 1 entrée registre ; l'UI n'importe que `AgentEvent` + `HookProvider` + enum (grep : 0 import provider-spécifique dans webview/) |
| H-P01-2 | Enum fermé | tous les états personnages de l'UI viennent des 5 valeurs ; 0 littéral d'état hors enum |
| H-P01-3 | **C3 — 2e harness sans toucher l'UI** | cycle complet (sessionStart → toolStart/toolEnd → sessionEnd) d'un harness non-Claude Code rendu correctement avec **git diff vide sur webview/** (après la passe P1) |
| H-P01-4 | Découverte dynamique | nouveau sous-répertoire/manifeste découvert au démarrage sans toucher au code du registre ; provider invalide (protocolVersion, id dupliqué) rejeté avec erreur claire |
| H-P01-5 | Push Compagnons | POST avec token sur `/api/hooks/companions` → personnage ; token faux → 401 |
| H-P01-6 | StreamProvider Jules | le polling traduit un cycle de vie de session Jules en `AgentEvent` (données fixture, 0 quota live brûlé) |
| H-P01-7 | MIT | LICENSE + copyright + notice + attribution JIK-A-4 présents ; champ `license` du VSIX vérifié |
| H-P01-8 | Token = secret | grep : token jamais en repo, jamais en clair dans les logs (test de redaction) |
| H-P01-9 | Anti-fantômes | détection heuristique seule (sans sessionStart + confirmation) → aucun personnage créé |
| H-P01-10 | Antigravity | VSIX installé, activé, smoke test vert dans Antigravity |
| H-P01-11 | R10 | reçu au ledger |
| H-P01-12 | Comptabilité par harness | chaque adapteur expose `accountingId` ; les faits de consommation émis correspondent à ce que le harness expose (adapteur sans données d'usage = 0 événement `usage` émis — jamais de chiffre inventé) |
| H-P01-13 | Pas de facturation | le code des adapteurs ne contient ni prix, ni quotas, ni allocation (grep : 0 occurrence) — la monétisation reste hors design |

## 5. Risques (Bill R1–R8 → réponses design)

- **R1 — Licence résiduelle.** → Gate P0 : re-vérification VSIX ; doute → arbitrage vision via A0 avant fork.
- **R2 — Dérive amont.** → Référence figée au fork + politique de rebase documentée.
- **R3 — Token exposé.** → Secret de bout en bout (H-P01-8) ; `--host 0.0.0.0` jamais activé sans décision.
- **R4 — Fantômes heuristiques.** → Politique §0.7 + H-P01-9.
- **R5 — États non formalisés.** → Enum fermé §0.2 + H-P01-2.
- **R6 — Enregistrement/consentement par harness.** → §0.8 : point d'enregistrement + consentement explicite documentés par adapteur.
- **R7 — Antigravity/Open VSX.** → Validation au design/exécution P4 (H-P01-10) ; publication = OUT.
- **R8 — Portée (réécriture runtime).** → Ajouts uniquement ; H-P01-3 prouve l'UI intouchée.
- **R9 — Couplage à l'agrégateur de tokens.** → L'adapteur ne dépend pas de l'agrégateur : il émet des faits de consommation en fire-and-forget, ne route pas de tokens, ne choisit pas de providers. L'agrégateur reste l'infrastructure du Capitaine, hors design.
- **R10 — Comptabilité dévoyée en facturation.** → Tranché par le scope Capitaine : le contrat porte l'identité et les faits, pas la monétisation (H-P01-13).

## 6. Séquencement vs les 6 missions Fondations

P-01 est **sans dépendance** (fork d'un repo externe, lane Amy/11e Doctor) : dispatchable dès validation du 11e Doctor, **sans perturber** la séquence F-02 → G-01-C → G-02-C → D-01 → E-01 → F-01. L'agrégateur de tokens du Capitaine est son infrastructure : les adapteurs émettent des faits de consommation, ils n'en dépendent pas.

*Fin du plan P-01. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation du 11e Doctor.*
