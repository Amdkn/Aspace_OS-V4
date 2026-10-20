# D-N028 — Dossier Conseil S2 : les 13 capacités non-qualifiées

| Champ | Valeur |
|---|---|
| **Mission** | D-N028 — suite de M-16 / D-N019 (qualification des 18 capacités, processus « preuve ou retrait ») |
| **Échéance** | **2026-11-01** |
| **Périmètre** | Les 13 capacités restées en `qualification_planned` après M-16 : 2 `NEEDS_LIVE_CHECK` (Cube Farm, Gateway OpenClaw) + 11 `NOT_PROVEN` |
| **Hors périmètre** | Les 2 capacités qualifiées par M-16 (Business OS — verified ; BMAD — executed) et les 2 déjà qualifiées avant M-16 (Life OS, Graham memory continuity) |
| **Rédacteur** | Ryan / Factory (13e Doctor, cœur Kernel) — **dossier de recommandation, pas de décision** |
| **Décideur** | Conseil S2 (décision écrite par capacité) + validation S1 (Rick) pour tout retrait — règle M-08 |
| **Sources** | Discussion #46 « Conseil S2 — Décision des 18 capacités » · PR #56 (plans de qualification) · PR #67 (mergée le 2026-10-10) — 15 preuves · `architecture/capabilities.json` (état live vérifié : 2 `qualified`, 13 `qualification_planned`, 3 `abandonment_proposed`) · `architecture/Conseil_S2_Decision_18_capacites.md` |
| **Condition S2 (Discussion #46)** | Toute capacité sans preuve à l'échéance 2026-11-01 revient devant le Conseil, qui tranche : QUALIFIER (plan daté + reçu R10) ou ABANDONNER (motif écrit, validation S1). |

**Règle de décision — M-08 (gravée).** Aucune mission ne peut ordonner « retirer / supprimer X » sans décision écrite préalable du Conseil S2 ; aucune capacité ne quitte le registre sans décision S2 + validation S1. **La Factory recommande seulement** : chaque recommandation ci-dessous est marquée « recommandation Factory, décision S2 » et ne tranche rien.

**Échelle de preuve (M-16).** `documented` (docs seules) → `installed` (code/déploiement présents) → `authenticated` (connexion live) → `executed` (a tourné, output observable) → `verified` (output vérifié, reçu conservé). Verdict QUALIFIED exige ≥ `executed` avec artefacts.

---

## 1. Tableau de synthèse des 13

| # | Capacité | Verdict | Niveau | Preuve clé | Check live manquant |
|---|---|---|---|---|---|
| 1 | Cube Farm | NEEDS_LIVE_CHECK | installed | control-plane réel + fork `Amdkn/cubefarm@31e7ce0` épinglé et vérifié sur GitHub ; devcontainer câblé (port 4417) | 3 checks Codespace : `office.sh status` (HTTP 200 sur :4417), `cubefarm.js doctor`, une mission bornée avec résultat |
| 2 | Gateway OpenClaw | NEEDS_LIVE_CHECK | executed | harnais mesuré le 2026-08-24 (`harnesses.json` : statut `mesure`, sonde `joignable: true`, OpenClaw 2026.5.18) + audit indépendant « Honnête » | clarification de périmètre S2 (harnais vs service gateway) ; si gateway : URL du service + statut de l'auth |
| 3 | Automaton M0/M1/M2 | NOT_PROVEN | documented | héritage V3 seulement (`AUTOMATON_GATEWAY_M0_M1_M2_PROPOSAL.md`, disposition `REFERENCE_PENDING_QUALIFICATION`) | aucun check identifiable : rien à sonder (pas de code, pas d'endpoint) |
| 4 | CEO Bench | NOT_PROVEN | documented | benchmark externe réel (arXiv 2606.18543) cité comme doctrine dans `os/business/_prd/` et `os/business/_runtime/GATES.md` | clarification S2 : référence doctrinale (re-typage) ou exécution du bench (runner + résultats) |
| 5 | Constructeur Universel | NOT_PROVEN | documented | nom au registre + décision S2 QUALIFIER ; aucune spec fonctionnelle trouvée | définir la capacité (spec minimale) — à défaut, rien à prouver |
| 6 | DeepSeek Harness | NOT_PROVEN | installed | wrapper UI en code (`os/agent/src/apps/DeepSeekHarness/index.tsx` → iframe `:3080`) + routeur + lanceur | installer `dsh` (source officielle à identifier), `dsh web --port 3080`, curl → 200, exercer une capacité avec reçu |
| 7 | gstack | NOT_PROVEN | documented | nom de méthodologie (`00_L1_gstack_ship_stack.md`, ADR-LD01-014) référencé par `life/registry.json` ; classé « exploration » par le repo | contenu des docs méthodologie (arbre Drive Life OS, hors repo) — non lu |
| 8 | Hermes surfaces et harness | NOT_PROVEN | documented | slot provider nommé dans `agents/registry.json` (`providers: […, "hermes"]`) + doctrine `agents/CONTRACT.md` | si un runner Hermes existe hors repo : URL + credential pour tester une connexion |
| 9 | Octop | NOT_PROVEN | documented | cible de déploiement Octopus identifiée ; seule « preuve » = déclaration du Capitaine dans `REPRO.md`, qui exige elle-même une re-confirmation | re-confirmation (Capitaine ou accès console) : déploiement Octopus toujours actif ? URL ? |
| 10 | OpenShell | NOT_PROVEN | documented | nom au registre + décision S2 QUALIFIER ; 3 mentions docs au total | définir la capacité (spec minimale) — à défaut, rien à prouver |
| 11 | Prime Agent | NOT_PROVEN | documented | scripts de déploiement VPS + unit systemd présents ; registre : statut `suppose`, sonde jamais concluante | sur la VPS : `03-install-prime-agent.sh`, `prime-agent --version`, `systemctl status prime-agent`, un appel routé avec reçu |
| 12 | Starnet | NOT_PROVEN | documented | « interface du périmètre de composition » dans le PRD-Fork-CubeFarm ; zéro trace runtime | aucun endpoint connu : le Conseil doit d'abord clarifier ce que serait le runtime Starnet |
| 13 | WorkAdventure | NOT_PROVEN | documented | même statut que Starnet (périmètre de composition, PRD) ; aucune instance connue | aucune instance connue : le Conseil doit clarifier le runtime attendu |

**Total : 0 des 13 atteint le seuil QUALIFIED (≥ executed avec artefacts) à ce jour.** 2 sont à un pas (Cube Farm : checks bornés ; Gateway OpenClaw : décision de périmètre). 11 n'ont aucune exécution prouvée.

---

## 2. Briefs par capacité

### 2.1 Cube Farm — NEEDS_LIVE_CHECK · `installed`

**État actuel.** Control-plane installé et câblé, vérifié : scripts `control-plane/` (`setup.sh`, `office.sh`, `directory.py`, `codex.sh`, `ensure-claude.sh`, README 4 Ko) ; fork épinglé dans `control-plane/runtime.lock.json` (`Amdkn/cubefarm` @ `31e7ce01a1dcc1da2b576d1da36718c16b05b8ca`, existence du commit confirmée via API GitHub, repo poussé le 2026-10-05) ; `.devcontainer/devcontainer.json` câble le port privé 4417 + `postCreateCommand`/`postStartCommand` ; `setup.sh` hydrate et build l'app (`portable/instance.py hydrate`, `npm ci`, `npm run build`). **Non vérifié** : le bureau 3D répondant sur :4417 (l'app n'hydrate que dans le Codespace `/workspaces/aspace/apps/cubefarm`, injoignable depuis la VM d'enquête) ; l'auth et une mission avec résultat — le README du control-plane l'avoue lui-même : « L'authentification et une mission avec résultat restent à vérifier. »

**Ce qui manque (live_checks_needed, Codespace uniquement).**
1. `bash control-plane/office.sh status` → bureau sur le port privé 4417 répondant (HTTP 200).
2. `(cd /workspaces/aspace/apps/cubefarm && node bin/cubefarm.js doctor)` → output sans erreur.
3. Une mission bornée exécutée avec résultat observable (reçu conservé).

**Options.**
- **a. Qualifier** — conditions : les 3 checks ci-dessus passent dans le Codespace ; le reçu de la mission bornée devient l'artefact de qualification (`executed`, voire `verified`).
- **b. Abandonner** — motif possible : le monde 3D n'a jamais été démontré en exécution malgré un control-plane complet ; la revendication au registre serait prématurée.
- **c. Re-typer** — en `installed_control_plane` (statut intermédiaire honnête) en attendant les checks live.
- **d. Prolonger l'enquête** — quoi : les 3 checks, bornés et nommés ; par qui : la Factory via la route Codespace (13e Doctor) ; délai : court, avant l'échéance.

> **Recommandation Factory, décision S2 : (d) prolonger l'enquête, puis (a) qualifier.** C'est la seule des 13 dont la preuve est à portée de 3 commandes nommées ; le control-plane est réel, épinglé et vérifié. Abandonner avant d'avoir tenté les checks serait décider sans la preuve disponible.

### 2.2 Gateway OpenClaw — NEEDS_LIVE_CHECK · `executed` (périmètre harnais)

**État actuel.** Le **harnais** OpenClaw est réellement mesuré : `os/business/_runtime/bridge/harnesses.json` → entrée `openclaw`, statut `mesure`, `mesure_le: 2026-08-24`, sonde `joignable: true` (chemin Windows `…\npm\openclaw`) ; `os/business/_audit/AUDIT_BRIDGE.md` confirme indépendamment : OpenClaw `2026.5.18 (50a2481)`, mention « Honnête ». **Non prouvé** : aucun code de service « Gateway » dans V4 (seules des specs `FleetGateway.md` dans `os/life/openspec/…` et un watchdog) ; `VITE_OPENCLAW_URL` = placeholder dans `os/life/.env.example` ; auth du gateway non vérifiée (diagnostic V4 du 2026-10-06 : « Gateway without auth », risque résiduel connu).

**Ce qui manque (live_checks_needed).**
1. Clarification de périmètre par le Conseil : la capacité vise-t-elle le **harnais** (mesuré → qualifiable sur artefacts existants) ou un **service gateway** V4 (non prouvé) ?
2. Si gateway : URL du service en cours d'exécution + statut de l'authentification.

**Options.**
- **a. Qualifier** — conditions : le Conseil tranche « périmètre = harnais » ; la mesure du 2026-08-24 + l'audit font foi (`executed`).
- **b. Abandonner** — motif possible : si le Conseil tranche « périmètre = service gateway », aucun service n'existe ; la revendication tombe.
- **c. Re-typer** — renommer la capacité en « OpenClaw harness » (ce qui est prouvé) et sortir la prétention « Gateway » du registre.
- **d. Prolonger l'enquête** — quoi : démontrer un service gateway en exécution + son auth ; par qui : la Factory ; délai : plus long, aucun point de départ dans le repo.

> **Recommandation Factory, décision S2 : (c) re-typer en « OpenClaw harness », puis (a) qualifier sur la mesure existante.** La preuve d'exécution existe déjà pour le harnais ; c'est le nom « Gateway » qui sur-vend. Le re-typage aligne le registre sur la preuve sans rien retirer de réel.

---

### 2.3 Automaton M0/M1/M2 — NOT_PROVEN · `documented`

**État actuel.** Héritage V3 uniquement : `migration/v3-inventory.json` référence `HANDOVER-2026-10-05-AUDIT-GATEWAY-AUTOMATON.md` et `docs/architecture/AUTOMATON_GATEWAY_M0_M1_M2_PROPOSAL.md` (V3 @ `ad5e68e`), disposition `REFERENCE_PENDING_QUALIFICATION` ; mentions dans `architecture/ASpace-V4-PRD-Fork-CubeFarm.md:111`, `architecture/REFONDATION.md:134-137`. Aucun module, service, test ou config `automaton` dans le repo V4 (hors docs et inventaire) ; aucune trace d'exécution des échelles M0/M1/M2. Référence externe https://github.com/Conway-Research/automaton = ressource de recherche du triptyque (Leon van Zyl), pas une capacité runtime V4.

**Ce qui manque.** Rien d'identifiable à sonder — pas de code, pas d'endpoint, pas de spec d'exécution. La voie de qualification serait : implémenter ou démontrer M0/M1/M2 contre des usages Life/Business observables (cf. `REFONDATION.md:134-137`).

**Options.**
- **a. Qualifier** — conditions : implémentation ou démonstration exécutée des échelles M0→M1→M2 avec artefacts (effort de construction, pas d'enquête).
- **b. Abandonner** — motif : proposition d'architecture V3 jamais implémentée ; revendication sans substance.
- **c. Re-typer** — en `référence de recherche` (triptyque), hors registre des capacités runtime.
- **d. Prolonger l'enquête** — sans objet en l'état : il n'y a rien à sonder tant qu'aucune spec d'exécution n'est définie.

> **Recommandation Factory, décision S2 : (b) abandonner** (motif : héritage non implémenté) **ou (c) re-typer en référence de recherche.** Le (a) est un chantier de construction, pas une qualification ; le (d) est vide. Le re-typage préserve la valeur du triptyque sans sur-vendre.

### 2.4 CEO Bench — NOT_PROVEN · `documented` (comme capacité runtime)

**État actuel.** CEO Bench **existe** : benchmark externe réel (arXiv 2606.18543) et **sert** — cité comme doctrine dans `os/business/_prd/PRD_DARK_FACTORY_RUNTIME_AMBIANT.md:17-24` (« le harnais doit être mesuré, pas supposé ») et `os/business/_runtime/GATES.md:53` (« Non franchie à ce jour, et c'est declaré ») ; `portable/README.md:35` le classe en « exploration BMAD/Gstack/CEO Bench ». Mais ce n'est pas une capacité *runtime* de V4 : V4 ne l'exécute pas, V4 le cite. Aucun runner, aucun harness de bench, aucun résultat de bench produit dans le repo ; 0 test bench dans `tests/`.

**Ce qui manque.** Clarification de périmètre par le Conseil : (a) la « capacité » = la référence doctrinale (la preuve = les citations ci-dessus) ; ou (b) une exécution du bench (runner + résultats requis, hors de portée sans cadrage).

**Options.**
- **a. Qualifier** — conditions : uniquement si (b) — runner exécuté, résultats conservés ; effort important, hors périmètre naturel de V4.
- **b. Abandonner** — motif possible : pas une capacité V4 ; mais perdrait la trace doctrinale.
- **c. Re-typer** — en `doctrinal_reference` (référence externe citée par les gates) : aligne le statut sur la réalité d'usage.
- **d. Prolonger l'enquête** — sans objet en (b) sans cadrage préalable du Conseil.

> **Recommandation Factory, décision S2 : (c) re-typer en référence doctrinale.** C'est le seul des 13 dont l'existence est incontestable hors V4 et dont l'usage est réel ; le NOT_PROVEN porte uniquement sur la qualification *comme runtime*. Le re-typage évite un faux retrait.

### 2.5 Constructeur Universel — NOT_PROVEN · `documented`

**État actuel.** Nom au registre (décision S2 QUALIFIER, échéance 2026-11-01) + mention en liste dans `architecture/REFONDATION.md:134-137`. Aucune définition fonctionnelle : 0 fichier hors docs (les 2 hits « constructeur » en code sont des faux positifs), 0 test, rien d'exécutable, aucun port/binaire/config. Le PRD-Fork-CubeFarm l'interdit explicitement : « Aucun nom de framework n'est assimilé à une capacité prouvée. »

**Ce qui manque.** Définir la capacité : spec minimale (entrées/sorties, interface) — à défaut, il n'y a rien à prouver. Si une implémentation existe hors repo : la localiser, l'exécuter, capturer un output observable.

**Options.**
- **a. Qualifier** — conditions : une spec puis une implémentation exécutée (chantier de construction).
- **b. Abandonner** — motif : aucune définition fonctionnelle, aucune substance exécutable ; nom sans objet au registre.
- **c. Re-typer** — sans objet : il n'y a pas d'autre nature à typer (pas de référence externe, pas d'usage doctrinal attesté).
- **d. Prolonger l'enquête** — sans objet sans spec préalable.

> **Recommandation Factory, décision S2 : (b) abandonner** (motif : capacité indéfinissable en l'état). Si un jour une spec émerge, la capacité pourra être re-proposée au Conseil avec un plan — le retrait n'est pas une interdiction de retour.

### 2.6 DeepSeek Harness — NOT_PROVEN · `installed` (wrapper seulement)

**État actuel.** Le **périphérique** existe en code : `os/agent/src/apps/DeepSeekHarness/index.tsx` (23 lignes : app `Cadre` en iframe vers `http://127.0.0.1:3080`, remède « `dsh web --port 3080` ou cliquer sur Lancer »), entrée routeur `os/agent/tools/routeurs-api.ts:105-111` (clé `deepseek`, port 3080, lanceur `C:/Users/amado/agent-os/desktop/lancer_dsh.cmd` — chemin Windows), lanceur `os/agent/lancer_dsh.cmd` présent. Mais le **harnais** n'a jamais été mesuré : le registre `harnesses.json` le marque `suppose`, et sa propre sonde du 2026-08-24 a constaté son absence (`joignable: false`, « absent du PATH et des repertoires connus (68 repertoires sondes) »). Binaire absent de la VM d'enquête, port 3080 fermé (curl → 000), aucune mention `dsh`/`deepseek` dans les `package.json`, 0 test.

**Ce qui manque.**
1. Installer `dsh` depuis sa source officielle (à identifier — absente du repo), `dsh --version`.
2. `dsh web --port 3080`, `curl -s http://127.0.0.1:3080/` → 200 (+ capture du rendu).
3. Exercer une capacité (ex. `tool_call`) et conserver le reçu.

**Options.**
- **a. Qualifier** — conditions : les 3 checks ci-dessus, bornés et nommés.
- **b. Abandonner** — motif : harnais jamais installé ni exécuté ; wrapper ≠ capacité.
- **c. Re-typer** — sans objet pertinent : le wrapper existe mais ne vaut pas une capacité.
- **d. Prolonger l'enquête** — quoi : identifier la source officielle puis les 3 checks ; par qui : la Factory ; risque : si la source officielle n'existe pas ou n'est pas identifiable, l'enquête meurt là.

> **Recommandation Factory, décision S2 : (d) prolonger l'enquête, bornée** — identifier la source officielle d'abord (si introuvable : **(b) abandonner**). Le périphérique en code justifie une dernière tentative bornée, pas une qualification.

### 2.7 gstack — NOT_PROVEN · `documented`

**État actuel.** Nom de méthodologie dans des documents : `life/registry.json` référence `00_L1_gstack_ship_stack.md`, `ADR-LD01-014_gstack_sober_install_lighting_l1_book_lune.md`, `l1_gstack_e_myth_mapping.md` (registre de fichiers pointant vers l'arbre Drive Life OS, non lus dans cette passe) ; mentions doctrine (`PRD-Fork-CubeFarm`, `REFONDATION.md`, `migration/README.md`, `presentations/…`, `portable/README.md:35` : « exploration BMAD/Gstack/CEO Bench »). Recherche `*gstack*` dans le repo : zéro fichier. Aucune installation, aucun code, aucune exécution, aucune trace de log ou reçu.

**Ce qui manque.** Le contenu des docs méthodologie (arbre Drive, hors repo) — non lu ; toute installation ou usage réel de gstack comme stack technique (aucun trouvé).

**Options.**
- **a. Qualifier** — sans objet : ce n'est pas une stack technique installable en l'état des preuves.
- **b. Abandonner** — motif : nom de méthodologie sans installation ni exécution ; le repo lui-même le classe en « exploration ».
- **c. Re-typer** — en `référence méthodologique` (comme CEO Bench) : la méthode vit dans les docs Life OS, pas dans le runtime V4.
- **d. Prolonger l'enquête** — quoi : lire les docs Drive ; par qui : avec accès Drive en lecture (décision Capitaine : Drive = PARA, lecture seule pour A0) ; apport incertain pour le registre runtime.

> **Recommandation Factory, décision S2 : (c) re-typer en référence méthodologique.** Même logique que CEO Bench : l'objet existe (docs Life OS), son usage n'est pas un runtime V4. Le re-typage préserve la trace sans sur-vendre.

### 2.8 Hermes surfaces et harness — NOT_PROVEN · `documented`

**État actuel.** Nom de provider dans la doctrine du plan de contrôle : `agents/registry.json` → `providers: ["codex", "jules", "hermes"]` — **noms seuls, aucun objet de configuration** (pas d'endpoint, pas de credentials, pas de paramètres) ; `agents/CONTRACT.md:19-20` (« Codex et Hermes produisent le même résultat typé ») et `:41` (« connexion Hermes sur runner cloud éphémère ») ; 15 occurrences dans le repo, toutes nominatives/doctrinales. Aucun fichier d'implémentation : pas de client, pas d'adaptateur, pas de skill, pas de config sous `harness/`, `agents/`, `control-plane/`, `tools/`. Aucune « surface » (UI/API) attribuable à Hermes. Aucune connexion établissable : rien à quoi se connecter.

**Ce qui manque.** Si un runner Hermes existe hors repo : URL + credential pour tester une connexion ; à défaut, la capacité reste indémontrable depuis la factory (noté `live_checks_needed` dans la fiche).

**Options.**
- **a. Qualifier** — conditions : un runner identifié + connexion testée + exécution tracée (aucun connu à ce jour).
- **b. Abandonner** — motif : slot doctrinal sans implémentation, sans endpoint, sans exécution ; le PRD-Fork-CubeFarm interdit d'assimiler le nom à une capacité prouvée.
- **c. Re-typer** — en `slot de provider doctrinal` (plan de contrôle) : honnête sur la nature réelle de l'objet.
- **d. Prolonger l'enquête** — sans objet sans piste de runner.

> **Recommandation Factory, décision S2 : (b) abandonner** la revendication de capacité, **ou (c) re-typer** en slot doctrinal si le Conseil veut garder la trace du plan de contrôle. Le (a) exige un runner dont personne n'a produit l'existence.

### 2.9 Octop — NOT_PROVEN · `documented` (déclaration)

**État actuel.** Nature identifiée : Octop = cible de déploiement **Octopus** (ligne REPRO : « Vercel / Render / Octopus », dans `os/business/04_Business_Domains/06_Finance_et_ROI_WonderWoman_Thunderbolts/dossiers/2026-08/`). Aucune config de déploiement, aucun pipeline, aucun artefact dans le repo. Seule « preuve » : déclaration directe du Capitaine dans `REPRO.md` — qui stipule elle-même : « pas une commande — à reconfirmer par un nouvel échange si le statut a changé » (« Gratuit »). Aucune URL, aucun accès vérifiable depuis la VM.

**Ce qui manque.** Re-confirmation par le Capitaine (ou accès console) : le déploiement Octopus est-il toujours actif ? URL ? — c'est exactement ce que le REPRO prescrit.

**Options.**
- **a. Qualifier** — conditions : re-confirmation + URL joignable + preuve de déploiement (pipeline ou console).
- **b. Abandonner** — motif : déclaration non re-confirmée, aucun artefact de déploiement.
- **c. Re-typer** — sans objet : une cible de déploiement ne se re-type pas utilement.
- **d. Prolonger l'enquête** — quoi : la re-confirmation prescrite par le REPRO lui-même ; par qui : le Capitaine (arbitrage vision, pas technique) ou accès console ; délai : court.

> **Recommandation Factory, décision S2 : (d) prolonger l'enquête** — la re-confirmation est prescrite par la source elle-même et c'est un arbitrage vision du Capitaine, pas une décision technique. Si non re-confirmé à l'échéance : **(b) abandonner**.

### 2.10 OpenShell — NOT_PROVEN · `documented`

**État actuel.** Nom au registre (décision S2 QUALIFIER, échéance 2026-11-01). 3 mentions documentaires au total (`capabilities.json`, `Conseil_S2_Decision_18_capacites.md`, `migration/README.md:77` en énumération « OpenShell/Octop »). Zéro référence dans tout le code (`*.mjs`/`*.ts`/`*.tsx`/`*.py`/`*.sh` : 0 hit hors `.git`), aucun fichier `*openshell*`, 0 test, rien d'exécutable, aucun port/binaire/config. 0 issue/PR sur le repo.

**Ce qui manque.** Définir la capacité : spec minimale (entrées/sorties, interface) — à défaut, il n'y a rien à prouver. Si une implémentation existe hors repo : la localiser, l'exécuter, capturer un output observable.

**Options.**
- **a. Qualifier** — conditions : une spec puis une implémentation exécutée (chantier de construction).
- **b. Abandonner** — motif : nom sans définition fonctionnelle ni substance exécutable.
- **c. Re-typer** — sans objet : aucune autre nature attestée.
- **d. Prolonger l'enquête** — sans objet sans spec préalable.

> **Recommandation Factory, décision S2 : (b) abandonner** (motif : capacité indéfinissable en l'état). Même logique que Constructeur Universel : un retrait n'interdit pas un retour avec une spec et un plan.

### 2.11 Prime Agent — NOT_PROVEN · `documented`

**État actuel.** Déclaré au registre des harnais (`os/business/_runtime/bridge/harnesses.json` → id `prime-agent`, statut **`suppose`**, `mesure_le: null`) ; sonde `joignable: null`, note : « PISTE NON VERIFIEE (apercu IA Google, 2026-08-24, pas la doc primaire) : Prime Agent aurait un mode `--mode acp`… A confirmer contre la doc officielle Prime Intellect avant d'agir ». **Préparé** au déploiement : `os/business/_runtime/bridge/deploy/vps/03-install-prime-agent.sh` + `deploy/vps/systemd/prime-agent.service` — mais le `.service` lui-même porte : « A CONFIRMER : la sous-commande de lancement persistant n'est pas verifiee dans cette session — l'URL d'install l'est (Prime Intellect, 2026-08-24), pas le mode d'execution en service ». Binaire absent de la VM (`command -v prime-agent` : rien), aucune exécution tracée nulle part, 0 test, 0 issue/PR.

**Ce qui manque.**
1. Sur la VPS : exécuter `03-install-prime-agent.sh`, capturer `prime-agent --version` et `prime-agent --help` (vérifier la sous-commande de lancement persistant).
2. Confirmer le mode ACP contre la documentation officielle Prime Intellect (pas l'aperçu IA).
3. `systemctl status prime-agent` sur la VPS + un appel routé via le bridge avec reçu.

**Options.**
- **a. Qualifier** — conditions : les 3 checks ci-dessus (chemin de preuve le plus court des 13 : scripts déjà écrits).
- **b. Abandonner** — motif : jamais installé, jamais exécuté ; statut `suppose` assumé par le registre lui-même.
- **c. Re-typer** — sans objet pertinent.
- **d. Prolonger l'enquête** — quoi : les 3 checks, bornés ; par qui : la Factory avec accès VPS (hors de portée de la VM d'enquête — noté, rien n'a été téléchargé/exécuté depuis l'URL d'install dans cette passe).

> **Recommandation Factory, décision S2 : (d) prolonger l'enquête, bornée** — les scripts existent, le chemin est le plus court des 13, et l'URL d'install est vérifiée (Prime Intellect). Si les checks échouent ou restent inaccessibles à l'échéance : **(b) abandonner**.

### 2.12 Starnet — NOT_PROVEN · `documented`

**État actuel.** « Interface du périmètre de composition » dans le PRD-Fork-CubeFarm (« Les interfaces Agent OS, Life OS, Business OS, Mobile OS, Starnet et WorkAdventure appartiennent au même périmètre de composition ») ; mentions dans `REFONDATION.md`, `Conseil_S2_Decision_18_capacites.md`, `capabilities.json`, `presentations/v3-v4/*`. Zéro trace hors docs : aucun fichier non-doc ne mentionne starnet (grep : seuls `.md`/`.html`/`.ts` de présentation). Aucune URL, aucun port, aucun docker-compose/service.

**Ce qui manque.** Aucun check identifiable : aucun endpoint connu à sonder. Le Conseil doit d'abord clarifier ce que serait le runtime Starnet (service ? URL ? périmètre ?) avant tout check live.

**Options.**
- **a. Qualifier** — sans objet en l'état : aucun runtime à exécuter.
- **b. Abandonner** — motif : ambition documentée sans aucun runtime identifiable ; revendication sans objet.
- **c. Re-typer** — en `interface du périmètre de composition` (ambition documentée) : honnête sur la nature, hors registre runtime.
- **d. Prolonger l'enquête** — sans objet sans clarification préalable du Conseil.

> **Recommandation Factory, décision S2 : (b) abandonner** la revendication runtime, **ou (c) re-typer** en ambition documentée si le Conseil veut garder la trace du périmètre de composition. Le (a) et le (d) sont vides sans clarification.

### 2.13 WorkAdventure — NOT_PROVEN · `documented`

**État actuel.** Même statut que Starnet : interface du périmètre de composition (PRD), ambition documentée, mentions dans `REFONDATION.md`, `Conseil_S2_Decision_18_capacites.md`, `presentations/v3-v4/*`. Zéro trace hors docs ; aucune URL d'instance, aucun port, aucune config de déploiement ; aucun client, aucun embed dans le repo.

**Ce qui manque.** Aucune instance connue à sonder. Le Conseil doit clarifier le runtime attendu (instance auto-hébergée ? URL publique ?) avant tout check live.

**Options.**
- **a. Qualifier** — sans objet en l'état.
- **b. Abandonner** — motif : aucune instance identifiable, zéro intégration.
- **c. Re-typer** — en `interface du périmètre de composition` (ambition documentée).
- **d. Prolonger l'enquête** — sans objet sans clarification préalable.

> **Recommandation Factory, décision S2 : (b) abandonner** la revendication runtime, **ou (c) re-typer** en ambition documentée. Même logique que Starnet.

---

## 3. Retraits — procédure et état des propositions existantes

**Règle M-08 (gravée, Discussion #46).** Aucune capacité ne quitte le registre sans **décision écrite du Conseil S2** (motif par capacité) **+ validation S1 (Rick)**. Toute PR qui retire une entrée de `capabilities.json` sans référence à une décision du Conseil est rejetée. Ce dossier ne retire rien : il recommande, le Conseil décide, S1 valide.

**Les 3 `abandonment_proposed` existants (PR #56) restent des PROPOSITIONS en attente de validation S1** — ils ne sont pas des retraits exécutés :

| Capacité | Motif S2 (2026-10-09) | Réserve expresse |
|---|---|---|
| Agent OS | « Redondant avec le substrat agent du BedRock L0 ; périmètre propre non vérifiable » | Porte sur la revendication au registre V4, **pas** sur la migration d'Agent-OS-Desktop dans le mono-repo (décision mono-repo du 2026-10-09, inchangée) |
| Mobile OS | « Hors périmètre du V4 minimal viable ; surface mobile réelle = portable cloud (Codespace) » | — |
| The OMK Office JaaS — 75 services déclarés | « Non pertinent comme capacité runtime V4 ; les 75 services vivent dans le site OMK Office / Master Profile » | Porte sur la revendication au registre, **pas** sur l'activité OMK Office (objectif 1 M$ inchangé) |

**Demande au Conseil (procédure).** Pour chaque capacité de ce dossier, rendre une décision écrite : QUALIFIER (avec le plan daté associé) / ABANDONNER (avec motif) / RE-TYPER (avec le statut cible) / PROLONGER (avec l'objet et le délai). Les décisions d'abandon partent ensuite en validation S1 (Rick). La Factory exécutera ensuite les transitions de registre dans une PR dédiée, avec reçu R10.

**Synthèse des recommandations Factory (décision S2 pour chacune) :**
- **Prolonger puis qualifier** : Cube Farm (3 checks Codespace), Prime Agent (3 checks VPS, bornés), DeepSeek Harness (source officielle puis 3 checks, sinon abandonner).
- **Re-typer puis qualifier** : Gateway OpenClaw (→ « OpenClaw harness », qualifier sur la mesure du 2026-08-24).
- **Re-typer** : CEO Bench (→ `doctrinal_reference`), gstack (→ `référence méthodologique`).
- **Prolonger (arbitrage vision)** : Octop (re-confirmation prescrite par sa propre source ; sinon abandonner).
- **Abandonner ou re-typer** : Automaton M0/M1/M2, Hermes, Starnet, WorkAdventure.
- **Abandonner** : Constructeur Universel, OpenShell.

---

## 4. Annexe — preuves et fiches

**Fichiers de preuve (repo `Amdkn/Aspace_OS-V4`, `evidence/`, livrés par PR #67 mergée le 2026-10-10) :**
- `~/workspace/v4-capabilities/evidence/cube_farm._qualification.json` · `gateway_openclaw._qualification.json` · `automaton_m0_m1_m2._qualification.json` · `ceo_bench._qualification.json` · `constructeur_universel._qualification.json` · `deepseek_harness._qualification.json` · `gstack._qualification.json` · `hermes_surfaces_et_harness._qualification.json` · `octop._qualification.json` · `openshell._qualification.json` · `prime_agent._qualification.json` · `starnet._qualification.json` · `workadventure._qualification.json`
- Hors périmètre mais liés : `business_os._qualification.json` (QUALIFIED, verified), `bmad._qualification.json` (QUALIFIED, executed)

**Fiches d'investigation détaillées (factory, lecture seule) :** `~/workspace/v4-factory/evidence-drafts/<slug>.md` — mêmes 15 slugs que ci-dessus (checks pass/fail, artefacts, `not_verified`, `live_checks_needed`, notes de périmètre).

**Décisions et sources :** `~/workspace/v4-capabilities/architecture/Conseil_S2_Decision_18_capacites.md` · Discussion #46 https://github.com/Amdkn/Aspace_OS-V4/discussions/46 · PR #56 (plans) · PR #67 https://github.com/Amdkn/Aspace_OS-V4/pull/67 (preuves, mergée) · registre `~/workspace/v4-capabilities/architecture/capabilities.json`.

---

*Dossier D-N028 rédigé par Ryan / Factory — recommandations seulement. Aucune décision n'est prise ici : le Conseil S2 décide, S1 valide (M-08). Tout fait non vérifié est marqué tel quel dans les preuves sources.*
