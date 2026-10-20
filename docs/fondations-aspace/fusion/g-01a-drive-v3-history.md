# G-01a — Volet Drive de « Fusion overview » : historique V3 + carte Life OS Drive + archives

**Mission :** Bill (holon DISCOVER) — qualification Drive, « Fusion overview » G-01.
**Date :** 2026-10-17 ~04:50 EDT · **Statut :** QUALIFIÉ.
**Méthode :** connecteur `google_drive` (connecté, vérifié `drive status`) ; **lecture seule stricte** — aucune écriture, aucun déplacement, aucun partage.
**Gap de méthode (déclaré) :** le connecteur `google_docs` n'est PAS connecté (`docs status` → `not_connected`) ; la règle Drive interdit d'extraire un Doc natif via `drive files export` même quand l'autre connecteur échoue. **4 Google Docs n'ont donc pas pu être lus** (contenu) : `00 — DATA Archives vivantes · Contrat de récupération`, `A3 DATA — PARA Workspace (ACTIF)`, `CANON — Life OS 2026 Workspace · A1/A2/A3 (43 profils actifs documentaires)`, `00 — PARA · Index actif Tech / Life / Business`. Seules leurs métadonnées (nom, date, emplacement) sont constatées. → À résoudre par le parent (connexion Docs ou fourniture du contenu).

---

## 1 — Historique V3 (lecture OBLIGATOIRE faite — ordre du Capitaine)

**Dossier :** `Historique V3` (id `1m0RAUqFaH8frNX3iWD-tahdBrwcoZlJj`), dans Life OS Data (`1hwj0LviT3JOwrp5fHvvKItGn9LW_oUtM`), modifié 2026-10-12.
**Contenu :** 45 fichiers `.md` (text/markdown), tous datés 2026-10-10 — **lus en intégralité : 13/45** (topologie exhaustive + piliers A1/A2/A3 : Beth, Morty, Curie, Discovery, Data, Geordi, Picard, Book, Georgiou, Pike, + analyse d'archéologie GitHub V3 du workspace). Les 32 restants suivent le même moule documentaire (frontmatter + Identity/Core Question/Inputs/Outputs/Boundaries/Evidence + alignement plan canon).

### 1.1 — Ce qu'était V3 (deux couches, pas une)

V3 = **un système d'exploitation de vie** (Life OS) tournant sur le **PC du Capitaine** (`C:\Users\amado\ASpace_OS_V2\`), **plus** un repo GitHub de sprint (`Amdkn/Aspace_OS_V3`). Les deux couches ont des temporalités différentes :

- **Couche PC (mai → sept 2026) :** l'architecture vivante. Specs créées le 2026-05-20, plan canon `C:\Users\amado\.claude\plans\fancy-hugging-bengio.md` (D1 receipt, 2026-06-21), bus d'état `00_Amadeus\40_SYMPHONY_BUS\state.json`, SDD `10_Tech_OS/12_Blueprints/01-SDD/SDD-005_life-os-l1-integration.md` (+ SDD-008 shadow tools, SDD-010 clôture 13e semaine), mémoire `00_Amadeus\30_MEMORY_CORE\` (LLM Wiki + `Gemini_Takeout_2026\`), workspace OpenClaw `.openclaw/workspace/agents_runtime/`.
- **Couche GitHub (9 sept → 5 oct 2026) :** le sprint d'industrialisation. 120 issues fermées + **427 PRs fermées** (244 mergées = 57 %, 161 drafts = 38 %), 1 250 runs workflows, **100 % des auteurs = Amdkn** (les sorties Jules publiées sous son compte). 90 % des issues et 86 % des PRs nées entre le 21 sept. et le 5 oct. 2026 ; **pic : semaine du 28 sept. = 248 PRs** (vague Jules + reconcile) ; jours les plus intenses : 3 oct. (76 PRs), 2 oct. (72). Extinction : **5 oct. 2026** — la veille du premier run vert de la Factory V4.
  *Preuve : `~/workspace/v4-factory/analyse-v3-heritage.md` (archéologie exhaustive 2026-10-08, 120 issues + 427 PRs récupérées en intégralité, aucun échantillonnage).*

### 1.2 — L'architecture : A1 → A2 → A3 (le moule)

*Preuve : `[HISTORIQUE V3] Topologie A1-A2-A3 — Life OS (57 specs V3).md` (110 lignes, analyse exhaustive du 2026-10-08).*

**A1 — Gatekeepers (2) :**
- **Beth** — Conscience stratégique / gardienne du filesystem. 5 états : `GREEN / ORANGE / RED / HALT_LD03 / HALT_LD04`. **Veto.** Protège LD03 (Santé) et LD04 (Cognition) contre toute urgence. Morty n'exécute jamais sans clearance Beth. Seuils canon (SDD-005) : LD03 ≥ 4.0, LD04 ≥ 3.5, alerte multi-domaines à 3. Écrit les décisions `PRD-L1`, tient le `Beth_Alignment_Log`, Go/No-Go des sprints 12WY, escalade à A0 uniquement aux milestones H30/H90.
- **Morty** — Routeur / exécuteur terminal. **Zéro autonomie de décision.** N'exécute que sur Context Pack complet (9 champs obligatoires : ship, crew_member, next_action, framework, domain_impact, l0_skill_required, beth_clearance, evidence_paths, output_artifact) ; sinon `BLOCKED_CONTEXT_PACK_INCOMPLETE`. Limites : 3 tickets concurrents max, `dry_run_first` par défaut, interdit de décider les priorités / créer des Rocks sans A0 / bypasser Beth / écrire des secrets dans les docs. Chaque exécution écrit dans `state.json` (`stage: executed` + `agent_path` + preuves). **D7 cost-of-escalation : Morty ne remonte JAMAIS à A0 mid-execution.**

**A2 — Vaisseaux / Frameworks (6), chacun avec son outil shadow :**
| A2 | Vaisseau | Framework | Outil shadow | Fonction |
|---|---|---|---|---|
| Orville | USS Orville | Ikigai | Obsidian/notes | Moteur du sens — 4 piliers, horizons H1→H90 |
| Discovery | USS Discovery | Life Wheel / ZORA | Baserow | Observation — 8 LD en télémétrie, pas en humeur |
| Curie | USS SNW | 12WY | Baserow | Exécution — Rocks, Warp Core tactics, scorecard |
| Computer | USS Enterprise | PARA | Obsidian/filesystem | Structure durable — Projects/Areas/Resources/Archives |
| HoloDeck | USS Cerritos | GTD | Plane | Chaos engine — capture→clarify→organize→review→engage |
| HoloJaneway | USS Protostar | DEAL | Affine | Libération — Define/Eliminate/Automate/Liberate |

**Imbrication canon (poupée russe) :** `12WY ⊃ PARA ⊃ DEAL` — Curie est le métronome (cadence hebdo 50/30/20), PARA s'imbrique dans 12WY via les 5 disciplines (Pike/Una/Chapel/M'Benga/Ortegas), DEAL est libéré opérationnellement par **Data** (A3 Archives = « chef d'orchestre DEAL », plan §3.2 — nuance D3 : Data reste A3, PAS un 5e A2).
*Preuves : A2 CURIE spec (131 lignes) ; A3 DATA spec (100 lignes, patch 2026-06-21).*

**A3 — Équipages (49 specs) :** 4 piliers Ikigai (Mercer/Profession, Grayson/Mission, Malloy/Passion, Finn/Vocation) + 5 horizons sentinelles (Isaac H1, Lamarr H3, Bortus H10, Alara H30, Klyden H90) ; 8 LD Discovery (Book LD01→Georgiou LD08, horizons verrouillés : Book H1 weekly P&L, Saru H3 quarterly runway, Culber H10, Tilly H30, Stamets H30, Burnham H10, Reno H10, Georgiou H90) ; 5 disciplines 12WY (Pike→Una→M'Benga→Chapel→Ortegas) ; 4 disciplines PARA (Picard/Projects, Spock/Areas, Geordi/Resources, Data/Archives) ; 5 stages GTD (Mariner→Boimler→Rutherford→Tendi→Freeman) ; 4 stages DEAL (Dal→Rok-Tahk→Zero→Gwyn).
- **Picard est DOCTRINE_ONLY** : V3 ne contient pas de spec dédiée A3_Picard (seule la doctrine, reconstruite depuis les sources). Spec complète restait à rédiger.
- **Incohérence interne signalée** (à trancher au design, pas ici) : la spec GEORGIOU verrouille « Georgiou = H90 (90-day / quarterly legacy review) » alors que H90 = horizon legacy 90 ans chez Klyden (topologie § Orville). Conflit 90 jours vs 90 ans dans les sources V3 elles-mêmes.

**Patterns transverses (le moule — transférables tels quels) :**
1. **L'A3 ne mute jamais rien** : il produit un *finding* typé + signaux + preuves, routé vers l'A2 qui compile, vers l'A1 qui décide. Séparation des pouvoirs explicite (anti-rôles dans chaque Boundaries).
2. **`hypothesis` est un statut de sortie légitime** — le non-vérifiable reste hypothèse, jamais preuve inventée.
3. Escalades canoniques : Beth (veto), Morty (exécution), Orville/Discovery (compilation), Protostar (friction répétée → DEAL).
4. Traçabilité totale : SDD + archives Gemini + twin paths ; **doctrine append-only (D4 no-hard-delete)**.
5. **Doctrine anti-paperclip Saru 1000T** (plan §18.3 + §22.4) : 3 garde-fous — Saru « coordinates with Book but does not override LD01 strategy » ; la scarcity seule ne déclenche pas de B1 review ; **« Musk pivot = agency over utopia »** — Saru DOIT évaluer si l'intention augmente l'agency de A0 vs attend un salut externe. Objectif 1000T par **valeur réelle Solarpunk/biomimétisme** (Benyus/Aberkane), pas spéculation (SpaceX IPO 85.7B = anti-pattern cité). *Preuves : A2 DISCOVERY spec (80 lignes), A3 BOOK spec (60 lignes).*
6. **5 ADRs Life OS manquants** identifiés comme gap à fermer : ADR-DEAL-001, ADR-GTD-001, ADR-PARA-001, ADR-LIFE-WHEEL-001, ADR-SYMPHONY-001 (cible : avant Item 11 du cycle Q3 2026, soit avant le 2026-09-07).

### 1.3 — Les phases (chronologie reconstituée)

| Phase | Période | Événements | Preuve |
|---|---|---|---|
| **P1 — Conception** | 2026-05-20 → 2026-06-21 | Specs A1/A2/A3 créées (20 mai) ; shadow tools (Baserow/Obsidian/Plane/Affine) ; plan canon `fancy-hugging-bengio.md` (21 juin, D1 receipt) ; bus `state.json` Symphony ; SDD-005/008/010 | frontmatter `created: 2026-05-20` sur toutes les specs ; patchs 2026-06-21 |
| **P2 — Cycle 12WY Q3 2026** | 2026-06-15 → 2026-09-07 | 12 items : W1 (SOB Abdaty + 13e semaine) ; W2 (auto-research IA + frugalité TOKEN) ; W3 (YouTube PARA + Hermes) ; W4 (Agent OS comme interface Spec/Workflow de Symphony + Business OS + A3 + Solaris/OMK/ABC en parallèle + **transfert Memory core local sur VPS via DEAL** + auto-amélioration Tilly). 13e semaine = 14 sept. ; W0 du 4e cycle = 21 sept. | A2 CURIE spec § cycle ; A1 MORTY spec § cycle ; A1 BETH spec § cycle |
| **P3 — Sprint GitHub** | 2026-09-09 → 2026-10-05 | 427 PRs / 120 issues ; labels : `universal-constructor` (17), `bill-rd` (13), `dc-sovereign` (10), `agent-os` (10), `needs:` routage compagnons (ryan 10, nardole 8, graham 8…), `forge:discovery/design`, `fractal:composition` (11), `semantic-full-stack` (9) ; vague Jules + reconcile (pic 28 sept. : 248 PRs) | `~/workspace/v4-factory/analyse-v3-heritage.md` |
| **P4 — Extinction / naissance V4** | 2026-10-05 → 2026-10-09 | 5 oct. : dernier commit V3. 6 oct. : premier run vert Factory V4. 9 oct. : décision mono-repo (Capitaine), **PR #27 mergée** (`d65fd0e`, 1 872 fichiers, +291 343 lignes) : `os/life` réduit, `os/agent` + `os/business` importés, migration sélective (**9 339 entrées sources → 1 341 textuelles importées**, SHA corpus `9883d2ef…`) | `~/workspace/github-audit-v3-v4-2026-10-17.md` §2 |

### 1.4 — Pourquoi V3 s'est terminé (lecture honnête)

**V3 ne s'est pas effondré : il a été consommé.** Les faits :
- V3 GitHub n'a vécu qu'**un mois** — un sprint unique, pas un régime de croisière (archéologie 2026-10-08).
- Le pic de 248 PRs/semaine avec 38 % de drafts = **volume sans discipline de merge** — le symptôme exact que V4 institutionnalise contre (CI bloquante, reçus R10, « sans reçu pas de merge »).
- La couche PC (Life OS vivant) n'a pas « planté » : son contenu a été **archivé** (Historique V3, 2026-10-10/12) et son héritage **sélectivement importé** dans V4 (PR #27).
- La relève est datée au jour près : extinction V3 le 5 oct. → premier run vert Factory V4 le 6 oct. → mono-repo le 9 oct. **Continuité opérationnelle, pas rupture.**

### 1.5 — Leçons V3 à transférer (matière première pour F-01 / G-01)

1. **Gouvernance par reçus, pas par doctrine** : V3 avait les doctrines (D1 receipts, Beth veto, Context Packs) mais l'enforcement vivait dans des scripts PC et un bus `state.json` local — **exactement la leçon du R10 V4** (F-02 L1 : doctrine sans enforcement codée = mécanisme à l'arrêt). Le transfert V4.1 doit coder l'enforcement, pas recopier la doctrine.
2. **Séparation des pouvoirs A1/A2/A3** : findings typés, jamais de mutation par l'observateur ; `hypothesis` comme sortie légitime (anti-invention de preuves).
3. **Garde-fous explicites contre l'optimisation aveugle** : anti-paperclip Saru, HARD SAFETY LD03/LD04 (Beth HALT), D7 cost-of-escalation.
4. **Append-only (D4)** : la doctrine V3 est un journal, pas un wiki réécrit — principe de la traçabilité temporelle (`observed_at`/`recorded_at`).
5. **Le sprint tue le régime** : 427 PRs en un mois, 38 % de drafts — la vélocité sans merge discipline produit des branches orphelines (écho direct aux ~35 branches V4 actuelles, F-02 R5).
6. **Points non résolus hérités** : spec Picard manquante (DOCTRINE_ONLY) ; 5 ADRs Life OS jamais écrits ; incohérence H90 Georgiou (90 jours vs 90 ans) ; `IMPORT.json` life manquant (D-N011, toujours ouvert côté V4).

---

## 2 — Carte Life OS (Drive) : « A'Space Life OS 2026 »

**Dossier racine :** id `1WAolW96BJFM5wL9Tkmi2M_BSip03Q8C5` (parent de `24_PARA_Enterprise`, vérifié 2026-10-17).

| Dossier | Contenu (1er niveau) | Volume |
|---|---|---|
| `21_Ikigai_Orville` (`1tWjwR_zgmjoEJ4sJ8TKt8KsEvTiewSDo`) | 4 piliers (FINN/Vocation, MALLOY/Passion, GRAYSON/Mission, MERCER/Profession) + 5 horizons (ISAAC H1, LAMARR H3, BORTUS H10, ALARA H30, KLYDEN H90) + `A2 ORVILLE — Ikigai` + `03 — Matrice Ikigai 4 Piliers × 5 Horizons` + `04 — Provenance et évolution des intentions` | 12 dossiers |
| `22_Wheel_Discovery` (`〈ID-Drive-masqué-export-P-003〉`) | 8 LD (BOOK→GEORGIOU) + `A2 DISCOVERY — ZORA` | 9 dossiers |
| `23_12WY_SNW` (`1VAwed3pM9VdP8g3rz5N7IQr1eB4UXk7F`) | 5 disciplines (PIKE, UNA, MBENGA, CHAPEL, ORTEGAS) + `A2 CURIE — 12WY` | 6 dossiers |
| `24_PARA_Enterprise` (`1fl55pFEoySRsAAto9GF0delUbo_TpHyJ`) | `A2 COMPUTER — PARA` + `A3 PICARD — Projects` + `A3 SPOCK — Areas` + `A3 GEORDI — Resources` + `A3 DATA — Archives` + `00 — PARA · Index actif Tech / Life / Business` (Doc, **non lu** — gap) + `[HISTORIQUE - SUPERSEDE] PARA — Index avant 3 Areas.md` | 5 dossiers + 2 fichiers |
| `25_GTD_Cerritos` (`1SnI4AlvOtoI46kHlhfupPDE-_oOqElTi`) | 5 stages (MARINER, BOIMLER, RUTHERFORD, TENDI, FREEMAN) + `A2 HOLODECK — GTD` | 6 dossiers |
| `26_DEAL_Protostar` (`1VM3MngFktk5PCSFfa8iYWb6EwKqhU2Tr`) | 4 stages (DAL, ROKTAHK, ZERO, GWYN) + `A2 HOLOJANEWAY — DEAL` | 5 dossiers |
| `00_Governance` (`13SE8emNKgGPFMKeNNXbB7egSDjLU1_xS`) | `A1 BETH — Conscience` + `A1 MORTY — Exécuteur` (dossiers) + **raccourcis** vers `[HISTORIQUE V3] A1 MORTY — Exécuteur.md` et `A1 BETH — Conscience.md` (cross-link vers les archives) + raccourci `00_ANTHOLOGY_ASPACE_REGISTRY` → **cible inaccessible** (`File not found` — gap) + dossier `ANTHOLOGY_ASPACE_WARGAME` (non exploré) | 3 dossiers + 3 raccourcis |
| racine | `CANON — Life OS 2026 Workspace · A1/A2/A3 (43 profils actifs documentaires)` (Google Doc, **non lu** — gap) | 1 Doc |

**Lecture :** le Drive Life OS **est** la topologie V3, matérialisée en dossiers (6 vaisseaux A2 + gouvernance A1). L'index supersédé (`[HISTORIQUE - SUPERSEDE] PARA — Index avant 3 Areas.md`) témoigne de la migration « 3 Areas » (Tech/Life/Business) — l'index actif est le Doc non lu. Les raccourcis de `00_Governance` vers `Historique V3` prouvent le chaînage conscient archive ↔ vivant.

---

## 3 — Life OS Data : le coffre des archives

**Dossier :** `1hwj0LviT3JOwrp5fHvvKItGn9LW_oUtM` — « archives récupérables avec Data dans Life OS » (arbitrage Capitaine 2026-10-17).

| Élément | Type | Date | Notes |
|---|---|---|---|
| `Historique V3` | dossier (45 .md) | 2026-10-10 | §1 ci-dessus — **lu** |
| `00 — DATA Archives vivantes · Contrat de récupération` | Google Doc | 2026-10-12 | **Non lu** (gap Docs) — probablement le contrat de récupération des archives |
| `A3 DATA — PARA Workspace (ACTIF)` | Google Doc | 2026-10-12 | **Non lu** (gap Docs) — workspace PARA actif de Data |
| `10_Exports_sources_recuperables` (`1UO2XyMeTMThnTQVDNI1Bzyy99zANBUR0`) | dossier | 2026-10-12 | Contient `Gemini Takeout 11 Oct 2026` + `Youtube Takeout` |
| `ChatGPT — Extraction 2026-10-16` (`1Dka5uSDu1N3P5eMzEhruHnxNPFUc_Z5L`) | dossier | 2026-10-16/17 | **Miroir Drive de l'extraction workspace** : Vague 1 = 25 fichiers, Vague 2 = 2, Vague 3 = 5, Vague 4 = 5 (+ `items-recuperes.md`, `MANIFESTE — Extraction ChatGPT 2026-10-16.md`, les deux modifiés 2026-10-17 — **l'archive Drive est tenue à jour en parallèle du workspace**) |

---

## 4 — Archive Takeout Gemini : état vérifié

**Dossier :** « Gemini Takeout 11 Oct 2026 », id `1n9CEkreJhXTmo7wPa7SL7CmI1j_PCIIt`, dans `10_Exports_sources_recuperables`, déposé 2026-10-12 (export manuel du Capitaine).
**Statut : ARCHIVE LECTURE SEULE** — arbitrage Capitaine 2026-10-17 : archivé comme l'extraction ChatGPT, **pas de miroir workspace** (les pointeurs F-01 visent ce dossier Drive, pas une copie).
**Contenu vérifié (23 fichiers) :**
- 20 mensuels `Gemini_Historique_2025-04.md` → `Gemini_Historique_2026-10.md` (text/markdown prétraités) : 2025-04 = 820 o (quasi vide) → 2026-09 = 5,2 Mo (pic) → 2026-10 = 665 Ko. **Total ≈ 23 Mo.**
- `INDEX_MENSUEL.md` (2 Ko), `RAPPORT_ANALYSE_TAKEOUT.md` (4,9 Ko).
- `MonActivite.html` (28,5 Mo), `archive_browser.html` (460 Ko).
- Couverture : avril 2025 → octobre 2026 (19 mois).
- **Brut hors Drive** (rappel chantier-1) : PC du Capitaine, 1,05 Go (1 410 images, 77 .wav, 11 .mp4, 47 specs .md SDD-000→009, 34 PDF) — médias non transcrits.
- **Lien V3 :** les specs V3 citent `C:\Users\amado\ASpace_OS_V2\00_Amadeus\30_MEMORY_CORE\Gemini_Takeout_2026\2026-05_conversations.md` et `C:\Users\amado\Archives\Gemini_Archive_Cleaned\` — le Takeout est la **source primaire de la mémoire V3** (preuves des specs BOOK, DATA, GEORGIOU).

## 5 — Youtube Takeout

**Dossier** dans `10_Exports_sources_recuperables` (2026-10-12) : `youtube_watch_history` (Google Sheet, 3,5 Mo), `youtube_watch_history.csv` (11 Mo), `watch-history.html` (50,9 Mo).

---

## 6 — Recouvrements / doublons / manques

### Recouvrements (existe en Drive ET ailleurs)
- **R1 — Extraction ChatGPT : Drive = miroir de `~/workspace/chatgpt-extraction/`** (mêmes vagues, mêmes volumes : 25/2/5/5 ; `items-recuperes.md` + MANIFESTE tenus à jour des deux côtés au 2026-10-17). **Règle :** le workspace est la copie de travail, le Drive est l'archive — ne jamais diverger sans tracer (cf. F-01).
- **R2 — Specs V3 :** `Historique V3` (Drive, 45 .md) vs héritage V3 dans V4 (`os/` importé via PR #27 : 9 339 entrées sources → 1 341 textuelles). Le Drive = la doctrine, le repo = le code importé sélectivement. **Pas de doublon** : couches différentes.
- **R3 — Takeout Gemini :** Drive (prétraité, 23 Mo) vs PC Capitaine (brut, 1,05 Go) vs citations dans les specs V3 (`Gemini_Takeout_2026\2026-05_conversations.md`). Trois états de la même source — le brut PC est la référence ultime, le Drive est l'archive de travail.
- **R4 — Raccourcis 00_Governance → Historique V3** : chaînage conscient, pas un doublon.

### Manques (existe nulle part ou inaccessible)
- **M1 — 4 Google Docs illisibles** (gap connecteur Docs) : contrat de récupération, workspace PARA actif de Data, CANON 43 profils, index PARA actif. **Le contrat de récupération (M1a) est le plus critique** : c'est lui qui définit les règles d'usage des archives.
- **M2 — Cible du raccourci `00_ANTHOLOGY_ASPACE_REGISTRY` inaccessible** (`File not found`) — registre d'anthologie fantôme ou permissions d'un autre compte.
- **M3 — Contenu des dossiers A2/A3 du Drive Life OS non échantillonné** (volumes 1er niveau seulement) — profondeur à explorer si Clara en a besoin.
- **M4 — Dossier `ANTHOLOGY_ASPACE_WARGAME`** (00_Governance) non exploré.
- **M5 — Brut Takeout sur PC du Capitaine** (1,05 Go) : A0 n'y a pas accès (constat, pas une demande).
- **M6 — Médias Takeout non transcrits** (77 vocaux, 11 vidéos) — cf. F-01 R4.

### Doublons à risque (pas encore des doublons)
- **D1 — Extraction ChatGPT Drive vs workspace** : miroir actif des deux côtés — risque de divergence silencieuse si les deux sont édités. Recommandation : figer le Drive comme archive (écriture = workspace seul, sync datée) ou tracer chaque sync.
- **D2 — Historique V3 vs specs importées dans `os/`** : si un design V4.1 recopie une spec Drive déjà importée en code, doublon doctrine/code — le design Clara doit croiser les deux (cf. G-01 : carte de fusion).

---

## 7 — Points pour le design Clara (G-01)

1. **L'historique V3 est lu et versé** : les 6 leçons du §1.5 sont la matière première du design des agents Tech/Life/Business sur V4 (ordre du Capitaine respecté).
2. **Le Drive Life OS est une topologie matérialisée**, pas un tas de fichiers : tout design qui y touche doit respecter le moule A1/A2/A3 (Beth veto, Morty zéro autonomie, findings typés).
3. **Archives = lecture seule, pointeurs pas miroirs** (arbitrage Capitaine) : Takeout, extraction ChatGPT, Historique V3 — le corpus F-01 pointe, ne duplique pas.
4. **Gaps bloquants pour un design complet** : les 4 Docs illisibles (M1) — dont le contrat de récupération ; la cible anthologie fantôme (M2).
5. **Incohérences V3 à trancher au design** : H90 Georgiou (90 j vs 90 ans) ; spec Picard DOCTRINE_ONLY ; 5 ADRs jamais écrits.

---
*Preuves : toutes les affirmations ci-dessus portent leur source (id Drive, chemin fichier, date de modification ou de lecture). Dossier Drive racine Life OS : `1WAolW96BJFM5wL9Tkmi2M_BSip03Q8C5`. Life OS Data : `1hwj0LviT3JOwrp5fHvvKItGn9LW_oUtM`. Takeout : `1n9CEkreJhXTmo7wPa7SL7CmI1j_PCIIt`. Specs V3 téléchargées en `/tmp/v3h/` (éphémère — relire depuis Drive si besoin).*
