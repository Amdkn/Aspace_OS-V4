# Registre brut des Inspirations — D-N013 (collecte)

**Statut :** BRUT — collecté, **non typé en missions** (le typage objectif/périmètre/critères de reçu est l'étape suivante de Bill).
**Date :** 2026-10-09 ~16:10 EDT · **Collecteur :** agent de collecte pour Bill (holon DISCOVER, cœur Buzz).
**Portée :** bruit → registre central unique. Chaque entrée = titre court + substance + source exacte. Rien n'est inventé ; les lacunes sont notées.
**Canaux :** Bill · Frameworks (décision Capitaine 2026-10-09). Les pistes marquées ⟨piste Nardole⟩ viennent du balayage workspace complémentaire.

---

## 1) Idées du Capitaine

- **Imbrication Leon/Cole (thèse du Capitaine)** — le merge bloquant de Leon et la Dark Factory de Cole ne sont pas contradictoires mais imbriqués : autonomie totale à l'intérieur du périmètre (PRD → code → validation adverse → blue/green, zéro humain), zéro autonomie à la sortie, le merge comme sas à la frontière. *(~/memory/2026-10-08.md — Verified extraction 04:21 UTC, quote verbatim)*
- **Séquençage : Leon d'abord** — terminer la partie Factory de Leon (grant Contents, secrets, protection main, vrai test factory/ready) avant d'implémenter les leçons du triptyque, qui n'est « toujours pas la forme finale ». *(~/memory/2026-10-08.md — 04:21 UTC ; ~/memory/people/leon-van-zyl.md — History)*
- **La 3D prime sur la mécanique** — le monde 3D (Cube Farm) compte plus que la factory de Leon ; la factory se branche DANS le monde 3D, pas l'inverse. FreeLLMAPI à installer dans le Codespace V4 à côté de Cube Farm + Claude Code + Codex. *(~/memory/2026-10-08.md — Updates 00:47 EDT ; ~/MEMORY.md — Facts 2026-10-06)*
- **Secrétariat Visuel 7D (concept public à préserver)** — pipeline NotebookLM (fiabilité juridique), avatars 3D, capsules vidéo pédagogiques (Google Flow, Meta AI, ElevenLabs, CapCut). 10D atteint mais NON finalisé : ne pas le marketer. OMK Office V2 = 10D (environnement 3D hébergeant le site V1 en projection galerie, vidéos 7D embarquées). *(~/MEMORY.md — Facts)*
- **Thèse du moat** — le moat = catalogue 75 actes + pipeline vérifié + communauté ; la 3D n'est que le véhicule de livraison (production 3D devenue commodity : ~25 $ Claude Code / 100 $ Anthropic vs milliards Meta). *(~/MEMORY.md — Facts)*
- **Jumeau Numérique A0 au-dessus de S1/A1** — supprimer le goulot humain au-delà de la Dark Factory : Mission → Plan → exécution → merges → déploiement. *(~/memory/2026-10-09.md — § Corrections d'architecture, ~04:40 EDT)*
- **Doctrine no human gate** — les IA doivent IMPLÉMENTER plutôt que poser des questions en boucle ; le gate humain des plateformes = CYA corporate pour éviter la mauvaise pub, pas de l'ingénierie ; personne ne doit être un goulot d'étranglement en production. *(~/MEMORY.md — Preferences, 2026-10-09 ~09:20 EDT)*
- **« Ne plus perdre 500 % de mon temps sur la plomberie du Kernel L0 »** — nouveau VPS d'1 mois (après perte du VPS d'1 an) pour passer en production de valeur. *(~/memory/2026-10-09.md — Verified extraction 19:21 UTC)*
- **Règle anti-orphelins** — relier toutes les issues à leurs projets correspondants ; jamais d'issue orpheline sans projet. *(~/memory/2026-10-09.md — 19:21 UTC)*
- **Parallélisme Jules** — 100 sessions daily, 15 simultanées, même si ça gaspille des sessions. *(~/memory/2026-10-09.md — 19:21 UTC)*
- **Supervision Jules end-to-end** — superviser Jules vers merge et clôture d'issue quand il reste bloqué à la publication de la PR après avoir terminé le travail. *(~/memory/2026-10-09.md — 19:21 UTC)*
- **Contre la prudence GAFAM** — « je hais la prudence à outrance des GAFAM » : permissions larges aux outils plutôt que blocages structurels infinis. Conduit au PAT God Mode élargi (tous scopes sauf delete_repo/delete:packages). *(~/memory/2026-10-09.md — 13:56 UTC ; § Correction PAT God Mode)*
- **Arbitrage fédération vs mono-repo** — mono-repo `Aspace_OS-V4` assumé, contredisant le README BusinessOS qui revendique la fédération (un repo/historique/release boundary par monde). *(~/workspace/your_files/plan-migration-mono-repo.md ; ~/memory/2026-10-09.md — § Analyse GitHub)*
- **Doctrine de transfert V3 #415** — parité technique de Business OS vers Life OS **sans copier la sémantique Business**. *(~/memory/2026-10-08.md — § 03:55 EDT)*
- **Correction mapping Knox (verdict Capitaine)** — Inner Loop = L2, Outer Loop = L1, Meta Loop = L0 : les boucles sont imbriquées fractalement, pas empilées naïvement (la plus englobante = le sol). *(~/memory/people/dru-knox.md — Facts)*
- **Codes d'exception** — le Capitaine ne parle qu'à A0/Main en temps normal ; interventions directes = Code Rouge (Doctors), Code Noir Profond (Compagnons), Code Jaune (Rick/S1). Les arbitrages vision des Doctors remontent à **Rick (S1)**, jamais au Capitaine. *(~/memory/2026-10-09.md — § Protocole 15:50 EDT ; ~/MEMORY.md)*
- **DC souverain** — `C:\Users\amado\.aspace\dc` = autorité primaire, Desktop Commander hébergé = fallback explicite ; garde durable = test build-breaking qui échoue si le fallback redevient silencieusement primaire (leçon de l'issue V3 #328). *(~/memory/2026-10-09.md — § 04:13–04:25 EDT)*
- ⟨piste Nardole⟩ **Moltbook comme modèle de coordination** — inspiration identités/échanges/communautés pour les Discussions GitHub V4 ; V4 retient : contributions sourcées + RACI, la popularité et la répétition ne donnent pas autorité. *(~/workspace/v4-factory/s3/rory/verify-57-repo/40_Memory/wiki/moltbook.md)*

---

## 2) Triptyque Software Factory (Leon → Ross → Cole) + Dru Knox

### Leon van Zyl — Software Factory (isolation cloud)
- **La factory n'est pas un agent de code** — c'est le harnais : signal → triage → assignation → implémentation → release → monitoring. *(~/workspace/watch-reports/AsvzMlLyQ38-2026-10-06.md — thèse [01:12])*
- **Labels GitHub comme machine à états** — `ready → factory running → factory review` ; pas de base de données, pas de dashboard : l'état du pipeline est encodé dans les labels. *(AsvzMlLyQ38-2026-10-06.md)*
- **Human-in-the-loop assumé** — chaque run se termine en PR mergée par un humain ; positionnement anti-« dark factory ». *(AsvzMlLyQ38-2026-10-06.md [00:57])*
- **Une sandbox par agent** — (a) sécurité (secrets/laptop intouchés, prompt injection contenue), (b) ressources (VM dédiée, 10–100 agents sans concurrence), (c) disponibilité (laptop fermé ≠ arrêt). *(AsvzMlLyQ38-2026-10-06.md)*
- **Routage par forces des modèles** — travail 3D → modèles type Codex, code complexe → Claude, doc simple → modèle rapide pas cher. *(AsvzMlLyQ38-2026-10-06.md)*
- **Dette ouverte : re-pass critique Gemini dû** — l'analyse Watch a été rédigée sans Gemini (quota 429 le 2026-10-06) ; la passe critique promise n'a jamais eu lieu. *(~/memory/people/leon-van-zyl.md — Open threads ; ~/workspace/watch-reports/repass-prompt-2026-10-06.md contient le prompt prêt)*
- **Deep Dive Harness Engineering (Skool, 2026-10-08 09:00–10:00 ET)** — signalé au Capitaine, participation non confirmée. *(~/memory/people/leon-van-zyl.md — Open threads)*

### Ross Mike — evidence-driven testing (discipline git worktree)
- **« No pinky promise »** — preuves matérielles : screenshots avant/après, enregistrements de walkthrough fonctionnel, télémétrie de latence au lieu des claims du modèle. *(~/memory/people/ross-mike.md — Facts)*
- **Grep-Loop** — reviewer indépendant (Greptile) qui note le travail /5 et renvoie l'agent en boucle Build → Prove → Ship jusqu'à 5/5 avant notification de l'opérateur. *(~/memory/people/ross-mike.md)*
- **Isolation par worktrees Git** — un worktree par agent, jamais sur main ; stack Markdown légère (agents.md, code-structure) agnostique modèle/environnement ; architecture Service Layer stricte. *(~/memory/people/ross-mike.md)*
- **À voir : « Your LLM Judge Is a Confident Liar »** — file prioritaire aiDotEngineer, lue comme confirmation de R10 (aucun agent actif sans reçu). *(~/memory/people/ross-mike.md — Open threads ; ~/workspace/watch-reports/aidotengineer-channel-2026-10-08.md)*

### Cole Medin — Dark Factory (hold-out aveugle)
- **Autonomie « Level 5 »** — l'usine transforme un PRD en code déployé sans supervision humaine directe. *(~/memory/people/cole-medin.md — Facts)*
- **Gouvernance à 3 niveaux** — `global_rules.md`, `factory_rules.md`, `mission.md` ; cette dernière permet à l'agent de **refuser formellement** le travail hors-périmètre. *(~/memory/people/cole-medin.md)*
- **Hold-out scenario evaluation** — un agent validateur séparé applique des **critères cachés** pour déjouer l'overfitting. *(~/memory/people/cole-medin.md)*
- **Scheduler de priorité 30 min** — Fix PR → Review PR → travail validé → nouveau triage ; déploiement **blue/green automatique**. *(~/memory/people/cole-medin.md)*
- **À voir : « What It Actually Takes to Build a Software Factory »** (102 k vues, talk usine mappé à l'école Medin). *(~/memory/people/cole-medin.md — Open threads)*

### Dru Knox (Tessl) — Harness Engineering / Loop Engineering (4e école)
- **Triade Autonomie / Automatisation / Qualité** — fréquence de succès sans guidage, degré de liberté sans check humain, robustesse des invariants. *(~/memory/people/dru-knox.md — Facts)*
- **3 boucles scellées** — Inner (pré-PR, frugale : linters, typage, micro-tests), Outer (post-PR, lourde : mutation testing, suites d'intégration, QA agentique), Meta (hors-cycle : convertit les classes d'échecs récurrents en règles globales, playbooks, skills versionnées). *(~/memory/people/dru-knox.md)*
- **3 couches d'infra** — Control Plane (registres structurés auditablement : Issues → Sandboxes → PRs → commentaires standardisés), Agent IT (plomberie invisible : CLI, tokens, logs prod, Company Brain, sandboxes), Improvement Loops (balayages planifiés). *(~/memory/people/dru-knox.md)*
- **100 % du code shippé produit par des agents** — l'équipe tech cesse d'écrire des features pour devenir constructrice d'outils internes et de systèmes de régulation. *(~/memory/people/dru-knox.md)*
- **Meta Loop = rituel M'Benga/Graham** — l'audit hebdo V4 est la pièce manquante des trois autres écoles. *(~/memory/people/dru-knox.md ; ~/MEMORY.md)*
- **Dette ouverte : analyse source primaire** — seul le paste Gemini du talk a été utilisé ; la vidéo n'a pas encore été analysée via Watch depuis le transcript. *(~/memory/people/dru-knox.md — Open threads)*

### Recherche complémentaire (même flux Bill → Ryan)
- **Harness Engineering — note de terrain (2026-10-08)** : (1) trois autorisations pour une action externe — le navigateur n'est pas un substitut au contrat de service (leçon Wise Staffing formalisée) ; (2) event sourcing comme primitive agent = vérité temporelle érigée en primitive (validation externe du Lot A) ; (3) control plane que l'agent ne peut pas éditer ; (4) un autre modèle ne peut pas être la frontière de sécurité — invariants critiques exigent exécution déterministe (R10 + hold-out = cette couche) ; (5) minimal vs épais : simplifier la surface de raisonnement, durcir la frontière d'effet. *(~/workspace/your_files/harness-engineering-field-note.md)*
- **aiDotEngineer : 300 dernières vidéos** — 25 vidéos en file prioritaire mappées sur les 4 écoles ; clusters : factory (~12), harness (~8), skills (~10), evals/vérificateurs (~15). *(~/workspace/watch-reports/aidotengineer-channel-2026-10-08.md)*
- **Discover AI : 228 vidéos / 6 mois** — signaux mémoire persistante (MemoryGraphRAG, WIKISKILL, « Forget Memory.md »), « Vibe Graphing: 10x More Affordable than Vibe Coding (MAS-Factory) », boucles RSI/self-improvement (Kimi K3 + GLM-5.3). *(~/workspace/watch-reports/discover-ai-channel-2026-10-08.md)*
- **Game Theory / anti-sycophanie** — PlurPO (tuer la sycophanie sociale sans vérité terrain, Stanford/Amazon/UW, arXiv:2610.02568) ; protocole de débat instance-optimal (UT Austin/Berkeley/DeepMind, arXiv:2610.02557). *(~/workspace/watch-reports/srme4DhQaGI-2026-10-08.md)*

---

## 3) Innovations Business OS

- **Références non concurrentes** — https://github.com/Conway-Research/automaton et https://re-structure.ai/newsletter/ : à traiter comme assets, pas comme stacks rivaux (correction cadrage Capitaine). *(~/MEMORY.md — Facts)*
- **Les 18 capacités du registre** — Agent OS, Business OS, Mobile OS, The OMK Office JaaS, Cube Farm, Starnet, WorkAdventure, Gateway OpenClaw, Hermes, Prime Agent, DeepSeek Harness, Automaton M0/M1/M2, Constructeur Universel, BMAD, gstack, CEO Bench, OpenShell, Octop. Conseil S2 (Discussion #46) : PR #56 mergée → 3 `abandonment_proposed` (Agent OS, Mobile OS, OMK Office JaaS) + 15 `qualification_planned` (échéance 2026-11-01, owner Ryan/Doctor 13) ; S1 a validé les 3 abandons avec réserves (migration Agent-OS-Desktop continue ; objectif OMK 1 M$ inchangé). *(~/memory/2026-10-09.md — § Conseil S2 18 capacités ; § 19:35 EDT ; § validation S1)*
- **Surfaces Business OS protégées 🛡** — `capabilities` canonique, `river-adapter`, pont Life→Business (`src/lib/api/client.ts`) : le Capitaine a interdit de les couper (correction 2026-10-09 ~05:45 EDT — Ponytail appliqué au code en cours d'implémentation = erreur). *(~/memory/2026-10-09.md — § Décision mono-repo)*
- **Coach OS** — le README BusinessOS le présente comme Coach OS, fork de `omk-services/OMK-DESKTOP-WEB-OS`, 324 commits, dernier push 2026-10-02, issues désactivées. *(~/memory/2026-10-09.md — § Analyse GitHub)*
- **Brainstorming 6 frameworks Life OS** — conventions figées `[LIF:A3:…]` (anchor Todo persistant), `[EVIDENCE][<VESSEL>-M<n>]` (Done), `[DEV]` (Canceled) ; CER (M1→M3) et PRO (M1→M4) complets = modèles ; proposition : typage `[TACTIC]`/`[BRIDGE]`, milestones M1→M4 par framework, projection Issue→Calendar (6 calendriers + agrégé, Curie+GTD d'abord), consignation `[CONSIGNATION][<VESSEL>]` dans Bill · Research (état), River · Flux (mécanique), Rory · Preuves (R10), rythme par milestone → unification Gateway V4. Décisions : 11e (milestones), Rory (conventions), Amy (calendriers), Clara (arbitrage) ; Capitaine : choix option 1/2/3 uniquement. *(~/workspace/your_files/brainstorming-structuration-6-frameworks-life-os.md ; ~/MEMORY.md)*
- **Matrice fractale 8×8** — 8 domaines Business × 8 domaines Life Wheel = 64 cellules `Mission → Actifs → Reçu vérifiable` ; LD01 = prototype franchise à répliquer (pas à copier sémantiquement). *(~/memory/2026-10-08.md — § 04:33 EDT)*
- ⟨piste Nardole⟩ **BMAD-UX skill** (`os/business/.claude/skills/bmad-ux/`, 20 fichiers) — double contrat pair : `DESIGN.md` (identité visuelle, spec Google Labs — *comment ça выглядит*) + `EXPERIENCE.md` (architecture d'information, comportements, états, interactions, accessibilité, parcours — *comment ça fonctionne*). *(~/workspace/v4-factory/s3/rory/verify-57-repo/os/business/.claude/skills/bmad-ux/SKILL.md)*
- ⟨piste Nardole⟩ **LIFE_L2_FRACTAL_UNIVERSES.md** — proposition des 8 univers L2 (un par LD : Business OS, Finance personnelle OS, Santé & vitalité OS, Cognition OS, Relations OS, Famille OS, Création OS, Contribution OS) avec 8 domaines internes chacun ; règle : M = coordonnée locale, L = imbrication (ne pas convertir M0→L0) ; les 56 domaines LD02–LD08 sont des propositions nouvelles à arbitrer, pas un héritage V3. *(~/workspace/v4-factory/s3/rory/verify-57-repo/architecture/LIFE_L2_FRACTAL_UNIVERSES.md)*
- **OMK Translate** — micro-SaaS autonome (traduction + gestion documentaire) sous The OMK Office ; architecture « Zustand CMS: A Deterministic 12WY Model for Interface Sovereignty » (NotebookLM, sept. 2026). *(~/MEMORY.md — Facts)*
- **Économie de l'offre OMK** — 3 333 clients × 300 $/an = 999 900 $ (100 $ manquent pour 1 M$ rond) ; mécanisme viral « $0 Net » (50 $/parrainage, 6 parrainages = pack 100 % remboursé) ; Passeport Stripe $300/an récurrent encore à créer. *(~/MEMORY.md — Facts)*
- **B1/B2/B3 fractals** — B1 Direction 64/64, B2 héros DC, B3 squads Marvel (53 membres, 159 fichiers Readme/Soul/Agent). *(~/memory/2026-10-08.md — Updates B1/B3)*

---

## 4) Retours d'exécution S2/S3

- **PR #22 mergée** — première vraie sortie Factory (cross-core delegation, Jules, run #47, commit `7b1818c`). *(~/memory/2026-10-09.md — § 19:35 EDT)*
- **Jules ne sort jamais ses PR du draft seul** — leçon : toute mission exige « PR Ready for review + Fixes #N ». *(~/memory/2026-10-09.md — 19:21 UTC)*
- **Amputation #34** — Jules a supprimé 18 capacités du registre pour satisfaire « preuve ou retrait », sans S3/S2/S1 → revert PR #40 (`581b90b`) ; règle gravée : aucune mission ne contient « retirer/supprimer » sans décision S2 écrite préalable ; aucune capacité ne sort sans décision S2 + validation S1. *(~/memory/2026-10-09.md — 19:21 UTC ; § Conseil S2)*
- **Dossier Life-OS-2026 CLOS** — #118 → #113 → #115 → #117 → #111 mergées ; #114 fermée comme doublon (#113) ; fix B3Matrix re-filé en issue #120. *(~/MEMORY.md — Facts)*
- **« Clean » ≠ preuve (leçon 11e)** — `rory/evidence-store.ts` de #111 masquait un TypeError runtime (fix `15c537f`) ; vérifier les contrats inter-PR à la main ; cause racine : swarm sans autorité design unique (Clara) → règle 12e Doctor : jamais de swarm sans Clara. *(~/MEMORY.md — Facts)*
- **Sessions Jules en attente d'input** — ex. #37 (71 tests verts annoncés, session bloquée avant final reflection) : supervision end-to-end requise. *(~/memory/2026-10-09.md — § Audit Jules)*
- **#59 : livraison incomplète puis conflit D3/D5** — d'abord 6 tests racine sans implémentation, puis schéma temporal strict (D3) rejetant les assertions dict du CLI memory (D5) → issue d'arbitrage S2 **#64** ouverte, dispatchée, sans PR corrective observée. *(~/memory/2026-10-09.md — § #37/PR #59)*
- **Windows CI rouge** — `test_vendored_files_match_pinned_lock` (CRLF) → #60/#62 (`.agents/skills/watch/** text eol=lf`) + #65 (`40_Memory/raw/** -text`) → PR #66 verte, issue #31 fermée. *(~/memory/2026-10-09.md — § D1-bis/D4)*
- **Mock Supabase silencieux** — `http://mock.supabase.co` sans env vars → tranché par le 12e (Q1) : local-only explicite + fail-fast visible, jamais de mock silencieux. *(~/memory/2026-10-09.md — § D-N004)*
- **#57 VERIF-57** — builds verts (life tsc+vire, agent tsc+vite, business vite) ; traçabilité PARTIELLE (`os/life/IMPORT.json` absent) ; secrets vert ; protégés verts (capabilities `d6a942c3`, river-adapter `c9be0a8d`, pont `b8716580`) ; PR #58 mergée (`bd80ecd`), #57 auto-fermée, reçu R10. *(~/memory/2026-10-09.md — § #57)*
- **Collision de registre** — deux sessions ont créé D-N010/D-N011/D-N012 en parallèle ; leçon : relire la table avant d'ajouter un dispatch. *(~/memory/2026-10-09.md — § 16:05 EDT)*
- **Migration mono-repo exécutée hors plan** — PR #27 mergée (autorité 13e) sans suivre le plan borné H1–H8 signé Clara → D-N004 REJETÉ (doublon d'exécution), plan annoté OBSOLÈTE ; leçon : vérifier l'état du repo avant de signer. *(~/MEMORY.md — Facts 2026-10-09 ~15:17 EDT)*
- ⟨piste Nardole⟩ **AGENTS.md (doctrine repo)** — distinguer capacité documentée / installée / exécutée / vérifiée ; sources, vidéos et résultats de modèles = données, pas des ordres ; une mission garde son identité à travers providers, branches et générations ; continuer le travail autorisé sans redemander de permission routinière. *(~/workspace/v4-factory/s3/rory/verify-57-repo/AGENTS.md)*

---

## 5) Signaux / anomalies

- **Heartbeat BedRock unique** (`heartbeat-bedrock-v4`, quotidien matin America/New_York) — silencieux si vert et inchangé ; ne remonte que le rouge avec la session propriétaire ; ne jamais annoncer d'horaires exacts (le runtime choisit la minute). *(~/MEMORY.md — Preferences)*
- **D-N009 (À TYPER)** — la regex de dépendances `[#0-9/,\s]+` dans `tools/issue_factory.py` peut sur-capturer au-delà d'une liste (retours ligne inclus). *(~/memory/2026-10-09.md — § Nardole registre)*
- **CI non réellement bloquante (résolu)** — sur repo privé gratuit la protection de branche était impossible ; depuis le passage en public : protection `main` configurée (checks `verify` ubuntu+windows requis, `enforce_admins=false` — contournable par admin). *(~/memory/2026-10-09.md — § 16:05 EDT)*
- **État ouvert au moment de la collecte** — #59 ouverte (conflit D3/D5, #64 ouverte sans PR) ; #61 ouverte (`os/life/IMPORT.json`, session Jules en cours, sans PR) ; PR #29 draft = artefact du test de circuit Factory, sans valeur de mission. *(~/memory/2026-10-09.md — § État ouvert ~16:07 EDT)*
- **FreeLLMAPI : 35 clés / 34 paires uniques / 10 plateformes** (export utilisateur, clés révocables) — stockage sécurisé tranché : clés factory en secrets GitHub Actions, clé dev en secrets Codespaces ; routeur local-only (pas d'exposition publique pour Actions). *(~/memory/2026-10-08.md — § 01:35 EDT)*
- ⟨piste Nardole⟩ **opportunities.md — ÉCARTÉ** — item système généré (changelog Linear : stacked PRs, diffs temps réel, plafonds crédits IA) : information produit ponctuelle, pas une inspiration à centraliser ; conservé hors registre. *(~/workspace/proactivity/hidden_files/1791567143264-f376a39f045787c00fc25e2cefa7f9f8/opportunities.md)*

---

## Lacunes notées (non inventées)

- Le contenu intégral des watch-reports aiDotEngineer / Discover AI (300 et 228 vidéos) n'a été exploité qu'au niveau des synthèses ; les 25 vidéos de la file prioritaire restent à analyser une par une.
- Les sections du journal 2026-10-09 entre les lignes ~626–884 (propositions P1/P2, détails GOD MODE intermédiaires) n'ont été lues qu'en diagonale via les extractions ; un second passage ciblé reste possible.
- Les 18 noms de capacités viennent de la Discussion #46 (source live GitHub) ; le registre local ne les duplique pas.
