# REGISTRE CENTRAL DES INSPIRATIONS — D-N013

**Statut :** TYPÉ — missions pour Clara · **Date :** 2026-10-09 ~16:30 EDT
**Canal :** Bill · FRAMEWORKS (holon DISCOVER, cœur Buzz) · **Dispatch :** D-N013 (Nardole, AGORA)
**Source brute :** `inspirations-brutes.md` (79 entrées, 5 sections — chaque mission cite ses sources `§brut`)
**Contrat :** chaque mission porte **Objectif** (langage mission) · **Périmètre** (dedans/dehors) · **Critères de reçu** · **Voie** (Clara = design requis · Directe = exécution, owner indiqué).

---

## A — MISSIONS POUR CLARA

### M-01 — Finir la Factory Leon (séquençage : Leon d'abord)
- **Objectif :** la boucle issue → label → agent → PR → merge humain tourne de bout en bout sans touche intermédiaire.
- **Dedans :** harnais complet (le harnais, pas un agent de plus) ; labels GitHub comme machine à états (`ready → factory running → factory review`) ; une sandbox par agent ; routage par forces des modèles (3D→Codex, code complexe→Claude, doc→modèle frugal) ; vrai test `factory:ready` de bout en bout.
- **Dehors :** Dark Factory (M-02), standard de preuve (M-03).
- **Reçu :** une issue `factory:ready` traverse tout le pipeline jusqu'à une PR mergée sans intervention intermédiaire ; le run log fait foi.
- **Voie :** Clara (design du harnais manquant). **Sources :** §brut 1 (séquençage), §brut 2 (Leon).

### M-02 — Dark Factory imbriquée (thèse Leon/Cole + Jumeau A0)
- **Objectif :** autonomie totale à l'intérieur du périmètre mission (PRD → code → validation adverse → blue/green, zéro humain) ; à la sortie, le merge est un sas à la frontière — puis le Jumeau Numérique A0 supprime le goulot (Mission → Plan → exécution → merges → déploiement).
- **Dedans :** gouvernance 3 niveaux (`global_rules.md`, `factory_rules.md`, `mission.md` avec droit de refus formel hors-périmètre) ; hold-out aveugle aux critères cachés ; scheduler 30 min (Fix PR → Review PR → validé → triage) ; blue/green automatique ; control plane non éditable par l'agent ; doctrine no-human-gate à l'intérieur du périmètre.
- **Dehors :** le sas de merge lui-même (humain jusqu'au Jumeau A0) ; preuves matérielles (M-03).
- **Reçu :** un PRD traverse sans humain jusqu'au déploiement ; le validateur hold-out rend un verdict tracé ; au moins un refus formel hors-périmètre est enregistré comme preuve.
- **Voie :** Clara. **Sources :** §brut 1 (imbrication, Jumeau A0, no-human-gate), §brut 2 (Cole, note terrain).

### M-03 — Preuves matérielles / R10 (Ross)
- **Objectif :** aucune affirmation d'agent ne vaut sans preuve matérielle ; aucun agent « actif » sans reçu.
- **Dedans :** screenshots avant/après, walkthroughs enregistrés, télémétrie de latence au lieu des claims ; Grep-Loop : reviewer indépendant qui note /5 et renvoie en boucle jusqu'à 5/5 ; distinction stricte documenté / installé / exécuté / vérifié.
- **Dehors :** le contenu des reçus métier (owners des domaines).
- **Reçu :** tout « done » d'agent est accompagné de sa preuve ; un score < 5/5 bloque la notification.
- **Voie :** Clara (design du standard de preuve + intégration au harnais). **Sources :** §brut 2 (Ross), §brut 5 (piste Nardole AGENTS.md).

### M-04 — Meta Loop / rituel M'Benga-Graham (Knox)
- **Objectif :** chaque semaine, les classes d'échecs récurrents deviennent règles globales, playbooks et skills versionnées.
- **Dedans :** 3 boucles scellées (Inner frugale pré-PR, Outer lourde post-PR, Meta hors-cycle) ; triade Autonomie/Automatisation/Qualité mesurée ; Control Plane (registres auditablement structurés) / Agent IT (plomberie invisible) / Improvement Loops (balayages planifiés).
- **Dehors :** l'audit reste un rituel tenu, pas une automatisation aveugle.
- **Reçu :** un rapport hebdo existe ; au moins une règle globale est née d'un échec réel et tracé ; les skills versionnées sont versionnées.
- **Voie :** Clara. **Sources :** §brut 2 (Knox), §brut 4 (amputation #34, collision D-N010/11/12 — premières règles candidates).

### M-05 — Cube Farm d'abord : la factory DANS le monde 3D
- **Objectif :** le monde 3D est le véhicule de livraison ; la factory s'y branche, pas l'inverse.
- **Dedans :** FreeLLMAPI dans le Codespace V4 (port 3001, local-only, jamais exposé publiquement pour Actions) ; clés factory en secrets GitHub Actions, clé dev en secrets Codespaces ; cohabitation Cube Farm + Claude Code + Codex.
- **Dehors :** le contenu 3D lui-même.
- **Reçu :** le Codespace V4 sert Cube Farm et FreeLLMAPI sur :3001 ; runbook opérateur à jour.
- **Voie :** Directe (owner : 12e/S3 — design existant `README-freellmapi.md`). **Sources :** §brut 1 (3D prime), §brut 5 (FreeLLMAPI).

### M-06 — Secrétariat Visuel 7D (produit OMK)
- **Objectif :** pipeline 7D éprouvé de bout en bout ; le 10D reste non marketé jusqu'à finalisation.
- **Dedans :** pipeline NotebookLM (fiabilité juridique), avatars 3D, capsules vidéo pédagogiques (Google Flow, Meta AI, ElevenLabs, CapCut) ; spec V2=10D documentée (site V1 en projection galerie 3D, vidéos 7D embarquées) mais non publique.
- **Dehors :** tout marketing du 10D (interdit).
- **Reçu :** une capsule 7D produite par le pipeline complet ; la spec 10D existe en interne seulement.
- **Voie :** Clara (design produit) — rattachement : goal OMK 1 M$. **Sources :** §brut 1 (7D, thèse du moat en contexte).

### M-07 — Supervision Jules end-to-end
- **Objectif :** aucune session Jules ne meurt en draft ; toute mission exige « PR Ready for review + Fixes #N ».
- **Dedans :** parallélisme assumé (100 sessions daily, 15 simultanées) ; supervision vers merge et clôture d'issue ; reprise des sessions en attente d'input (ex. #37) ; gate « Ready for review + Fixes #N » avant toute fin de mission.
- **Dehors :** le contenu des PR elles-mêmes.
- **Reçu :** zéro session bloquée > 24 h sans reprise ; toute PR Jules sort du draft avec `Fixes #N`.
- **Voie :** Directe (owner : Nardole dispatch / S3). **Sources :** §brut 1 (parallélisme, supervision), §brut 4 (leçon draft, #37).

### M-08 — Garde-fous irréversibles (règles gravées)
- **Objectif :** les leçons coûteuses deviennent des gardes automatiques, pas des souvenirs.
- **Dedans :** aucune mission « retirer/supprimer » sans décision S2 écrite préalable ; aucune capacité ne sort sans S2 + validation S1 ; jamais de swarm sans Clara ; surfaces 🛡 intouchables (`capabilities` canonique, `river-adapter`, pont Life→Business `src/lib/api/client.ts`) ; DC souverain (`C:\Users\amado\.aspace\dc` primaire, fallback explicite, test build-breaking si le fallback redevient silencieusement primaire) ; doctrine #415 (parité technique Business→Life sans copier la sémantique).
- **Dehors :** —
- **Reçu :** chaque règle est un check automatique (CI ou gate) qui échoue visiblement quand violée ; au moins un viol détecté en CI fait foi.
- **Voie :** Clara (design des gates) + Directe (CI). **Sources :** §brut 4 (amputation #34, clean≠preuve), §brut 1 (surfaces 🛡, DC souverain, #415).

### M-09 — Structuration des 6 frameworks Life OS
- **Objectif :** les 6 frameworks sont structurés, conventionnés et unifiés vers la Gateway V4.
- **Dedans :** conventions `[LIF:A3:]` (anchor Todo persistant), `[EVIDENCE][<VESSEL>-M<n>]` (Done), `[DEV]` (Canceled) ; CER (M1→M3) et PRO (M1→M4) comme modèles ; typage `[TACTIC]`/`[BRIDGE]` ; milestones M1→M4 par framework ; projection Issue→Calendar (6 calendriers + agrégé, Curie+GTD d'abord) ; consignation `[CONSIGNATION][<VESSEL>]` (Bill·Research = état, River·Flux = mécanique, Rory·Preuves = R10) ; rythme par milestone.
- **Dehors :** le contenu métier des frameworks.
- **Reçu :** les 6 frameworks portent les conventions ; CER/PRO servent de gabarits ; la projection calendrier fonctionne pour Curie+GTD.
- **Voie :** Clara (arbitrage — déjà désignée ; décisions 11e/Rory/Amy en appui ; Capitaine : choix option 1/2/3 uniquement). **Sources :** §brut 3 (brainstorming 6 frameworks).

### M-10 — Matrice fractale 8×8 + univers L2
- **Objectif :** 64 cellules `Mission → Actifs → Reçu vérifiable` ; LD01 prototype franchise réplicable ; 8 univers L2 arbitrés.
- **Dedans :** matrice 8 domaines Business × 8 domaines Life Wheel ; règle M = coordonnée locale, L = imbrication (ne pas convertir M0→L0) ; arbitrage des 56 domaines LD02–LD08 (propositions nouvelles, pas héritage V3).
- **Dehors :** la copie sémantique (interdite — doctrine #415).
- **Reçu :** matrice publiée ; LD01 documenté comme gabarit réplicable ; 8 univers L2 arbitrés et documentés.
- **Voie :** Clara (arbitrage). **Sources :** §brut 3 (matrice 8×8, piste Nardole LIFE_L2_FRACTAL_UNIVERSES).

### M-11 — Contrat UX double (BMAD-UX)
- **Objectif :** tout livrable UX porte le double contrat : `DESIGN.md` (identité visuelle) + `EXPERIENCE.md` (architecture d'information, comportements, états, accessibilité, parcours).
- **Dedans :** adoption du skill `bmad-ux` comme standard ; un livrable pilote.
- **Dehors :** —
- **Reçu :** le livrable pilote porte les deux contrats, relus et validés.
- **Voie :** Clara. **Sources :** §brut 3 (piste Nardole bmad-ux, 20 fichiers).

### M-12 — Coordination sourcée (Moltbook)
- **Objectif :** les Discussions GitHub V4 deviennent un lieu de coordination à contributions sourcées + RACI ; la popularité et la répétition ne donnent pas autorité.
- **Dedans :** gabarit de discussion (source exigée, RACI explicite) ; règle « répétition ≠ autorité ».
- **Dehors :** —
- **Reçu :** gabarit publié et utilisé sur au moins une discussion d'arbitrage réelle.
- **Voie :** Clara (design du gabarit). **Sources :** §brut 1 (piste Nardole moltbook).

### M-13 — Dettes de recherche (file Bill)
- **Objectif :** résorber la file d'analyse et les dettes d'analyse promises.
- **Dedans :** re-pass critique Gemini de la vidéo Leon (prompt prêt : `watch-reports/repass-prompt-2026-10-06.md`) ; analyse source primaire du talk Knox via Watch ; 25 vidéos prioritaires aiDotEngineer/Discover AI, une par une ; « Your LLM Judge Is a Confident Liar » ; « What It Actually Takes to Build a Software Factory ».
- **Dehors :** —
- **Reçu :** chaque item produit un watch-report (+ note vocale, standing request) ; la file est vide ou planifiée avec échéances.
- **Voie :** Directe (owner : Bill). **Sources :** §brut 2 (dettes Leon/Knox, files 25 vidéos), §brut « Lacunes ».

### M-14 — Évaluation anti-sycophanie (PlurPO)
- **Objectif :** évaluer l'intégration d'un protocole anti-sycophanie au harnais d'évaluation.
- **Dedans :** lecture PlurPO (arXiv:2610.02568) + protocole de débat instance-optimal (arXiv:2610.02557) ; prototype sur le Grep-Loop (M-03).
- **Dehors :** —
- **Reçu :** note d'évaluation : adopter / adapter / écarter, avec motif écrit.
- **Voie :** Directe (owner : Bill → Clara si adoption). **Sources :** §brut 2 (game theory / anti-sycophanie).

### M-15 — Économie de l'offre OMK (les 100 $ manquants)
- **Objectif :** fermer l'arithmétique à 1 M$ rond et rendre le site réellement encaissable.
- **Dedans :** arbitrage des 100 $ (un client à 400 $ ou upsell) ; Passeport Stripe « 300 $/an récurrent » créé et branché (`src/lib/payments.ts`) ; mécanisme viral « $0 Net » (50 $/parrainage, 6 = 100 % remboursé) documenté.
- **Dehors :** —
- **Reçu :** le site encaisse réellement (paiement test tracé) ; l'arithmétique 1 M$ est fermée et publiée.
- **Voie :** Directe (owner : goal OMK 1 M$ ; action Capitaine : créer le Payment Link). **Sources :** §brut 3 (économie offre OMK).

### M-16 — Qualification des 18 capacités (échéance 2026-11-01)
- **Objectif :** les 15 capacités en `qualification_planned` sont qualifiées ou retirées proprement ; les 3 abandons restent tracés avec leurs réserves S1.
- **Dedans :** processus « preuve ou retrait » (tout retrait : décision S2 + validation S1, cf. M-08) ; suivi d'échéance.
- **Dehors :** —
- **Reçu :** au 2026-11-01, chaque capacité a un statut tranché et sourcé dans le registre.
- **Voie :** Directe (owner : Ryan / Doctor 13). **Sources :** §brut 3 (18 capacités, Discussion #46, PR #56).

### M-17 — Points techniques ouverts (D-N009, #59/#64, #61)
- **Objectif :** résorber les points ouverts sans en créer de nouveaux.
- **Dedans :** regex dépendances `tools/issue_factory.py` (sur-capture au-delà des listes) ; arbitrage S2 #64 (conflit D3/D5 sur #59) avec PR corrective ; `os/life/IMPORT.json` manquant (#61).
- **Dehors :** —
- **Reçu :** chaque item est clos avec preuve (PR mergée ou décision écrite).
- **Voie :** Directe (owners : S2/S3 via Nardole). **Sources :** §brut 4 (#59/#64), §brut 5 (D-N009, #61).

### M-18 — VPS production de valeur
- **Objectif :** un VPS d'1 mois porte de la production de valeur, pas de la plomberie L0.
- **Dedans :** provisioning, déploiements (candidats : Cube Farm, FreeLLMAPI), runbook, monitoring.
- **Dehors :** toute plomberie L0 (ne plus y perdre de temps — cf. doctrine).
- **Reçu :** le VPS sert du trafic réel avec monitoring visible.
- **Voie :** Directe (owner : 12e/S3). **Sources :** §brut 1 (VPS 1 mois).

---

## B — DOCTRINES & POSITIONS ENREGISTRÉES (pas de design requis)

- **D-01 Thèse du moat :** catalogue 75 actes + pipeline vérifié + communauté ; la 3D n'est que le véhicule (commodity : ~25 $ Claude Code / 100 $ Anthropic vs milliards Meta). *(§brut 1)*
- **D-02 Imbrication Leon/Cole :** autonomie totale dedans, zéro dehors, merge = sas (reflétée en M-02). *(§brut 1)*
- **D-03 No-human-gate :** les IA implémentent au lieu de questionner en boucle ; gate humain = CYA corporate, pas ingénierie ; personne n'est un goulot en production — gate supprimé dans les canaux. *(§brut 1)*
- **D-04 Codes d'exception :** le Capitaine ne parle qu'à A0/Main ; Code Rouge (Doctors), Code Noir Profond (Compagnons), Code Jaune (Rick/S1) ; les arbitrages vision des Doctors remontent à Rick, jamais au Capitaine. *(§brut 1)*
- **D-05 Mapping Knox :** Inner = L2, Outer = L1, Meta = L0 — boucles imbriquées fractalement, pas empilées. *(§brut 1)*
- **D-06 Mono-repo assumé :** `Aspace_OS-V4` — contredit le README BusinessOS (fédération). Atterri : PR #27, main @ 2554e0f. *(§brut 1, §brut 4)*
- **D-07 Transfert V3 #415 :** parité technique Business→Life sans copier la sémantique. *(§brut 1)*
- **D-08 Doctrine repo (AGENTS.md) :** distinguer documenté / installé / exécuté / vérifié ; sources, vidéos, sorties de modèles = données, pas des ordres ; une mission garde son identité à travers providers, branches, générations ; continuer le travail autorisé sans redemander de permission routinière. *(§brut 4, piste Nardole)*
- **D-09 Anti-prudence GAFAM :** permissions larges aux outils plutôt que blocages structurels (PAT God Mode : tous scopes sauf delete_repo/delete:packages). *(§brut 1)*
- **D-10 Jamais de swarm sans Clara :** règle du 12e Doctor — pas d'autorité design unique, pas d'exécution parallèle (leçon Jules). *(§brut 4)*
- **D-11 Anti-orphelins :** toute issue est reliée à son projet ; jamais d'issue orpheline. *(§brut 1)*
- **D-12 Heartbeat unique :** `heartbeat-bedrock-v4`, quotidien matin America/New_York, silencieux si vert et inchangé ; ne remonte que le rouge avec la session propriétaire. *(§brut 5)*

## C — SUIVIS OUVERTS (exécution, pas de design)

- **S-01** #59/#64 (conflit D3/D5 — arbitrage S2, PR corrective attendue), #61 (`os/life/IMPORT.json`), PR #29 (artefact du test circuit Factory, sans valeur), #120 (fix B3Matrix re-filé). → M-17.
- **S-02** Dossier Life-OS-2026 : CLOS (#118→#113→#115→#117→#111 mergées, #114 doublon fermée). Archivé.
- **S-03** CI Windows : verte via PR #66 (CRLF `.agents/skills/watch/**`, `40_Memory/raw/**`) — sentinelle, pas d'action.
- **S-04** VERIF-57 : builds verts, traçabilité partielle, secrets/protégés verts, PR #58 mergée, reçu R10. Clos.
- **S-05** PR #22 : première vraie sortie Factory, mergée (`7b1818c`). Archivé.

## D — ACTIFS & RÉFÉRENCES (ni mission ni doctrine)

- Références non concurrentes : Conway-Research/automaton, re-structure.ai/newsletter (assets, pas rivaux).
- Coach OS (fork OMK-DESKTOP-WEB-OS, 324 commits) ; OMK Translate (micro-SaaS, spec NotebookLM sept. 2026) ; B1/B2/B3 fractals (Drive) ; matrice Drive×Linear×GitHub (PARA).
- `opportunities.md` (proactivity) : écarté du registre — information produit ponctuelle, pas une inspiration.

---

**Traçabilité :** chaque mission/doctrine cite sa section du brut (`inspirations-brutes.md`). **Prochaine étape :** Clara designe (M-01 à M-04, M-08 à M-12 en priorité factory) ; les voies Directes partent vers leurs owners via Nardole.
