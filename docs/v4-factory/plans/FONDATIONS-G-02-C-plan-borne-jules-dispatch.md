# G-02-C — Plan borné : Jules — fiabiliser le dispatch, cadrer le MCP

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne lore : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) ; découverte Bill G-02 (`fusion/g-02-jules-mcp.md`)
**Position tranchée par l'analyse (doctrine anti-faux-binaires) :** « MCP ou REST ? » n'est pas une question — le REST direct est en place et fonctionne (`tools/issue_factory.py`), le MCP est un client-side optionnel qui n'ajoute rien au REST qu'il enveloppe. Le design documente cet état, il ne le fait pas arbitrer.
**Séquencement : exécution APRÈS F-02** (le R10 doit être vivant : le diagnostic du rouge en boucle présume une cause R10 — on ne diagnostique pas un garde-fou avec un garde-fou mort).
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Rien à créer côté intégration.** Le dispatch Jules existe et fonctionne en REST direct (`tools/issue_factory.py:37-39`, `:206-211`, garde-fous R10 `CLAIMED` avant POST, no-blind-redispatch, regex session). Le design **diagnostique et fiabilise**, il ne reconstruit pas.
2. **P0 = diagnostic du rouge en boucle avec preuves.** 6 échecs consécutifs (2026-10-17 03:24→05:44 UTC, runs 14–17 s) — cause présumée : reçu R10 #61 BLOCKED + garde-fou no-blind-redispatch (`tools/issue_factory.py:364`), **pas Jules**. Confirmation par les logs : distinguer « POST Jules en échec » de « bloqué avant POST ». **L'évidence tranche, pas l'hypothèse** : cause côté Jules → traiter côté Jules ; cause côté R10 → router vers F-02/L1 (le correctif est la levée du BLOCKED #61, pas une modification du dispatch).
3. **Fiabilité = traçabilité par reçus.** Chaque tentative de dispatch produit une trace : tentative → verdict du garde-fou → session id ou motif de blocage. Un dispatch non tracé = un dispatch non prouvé.
4. **MCP client-side : documenté si justifié, sinon « non requis ».** `@google/jules-mcp` (7 outils effectifs — le « 9 outils » de deepwiki est faux ; `google-labs-code/jules-sdk`, non supporté officiellement par Google) + clé via Secure Vault. Usage justifié = sessions interactives depuis un client MCP (Claude Desktop, Cursor…). Sinon : « non requis » documenté avec l'analyse (le MCP n'ajoute rien au-delà du REST). **« Configurer le MCP côté Google » n'existe pas** — jamais proposé, jamais tenté.
5. **CONTRAINTE DURE (inviolable) : les valeurs des secrets GitHub Actions ne sont JAMAIS lisibles via API.** Documentée dans le design ; **zéro tentative d'extraction**, zéro contournement. Visible : noms, dates de MAJ, workflows référençants. Réutilisation hors Actions = le Capitaine via Secure Vault uniquement.
6. **Vérification de la couverture Jules GitHub App** : `GET /v1alpha/sources` (lecture seule, clé via env/Secure Vault — jamais extraite, jamais en repo).
7. **Hors périmètre, noté** : `tools/agent_mesh.py` et `agents/registry.json` (providers `codex`/`jules`/`hermes`) non lus — à designer séparément, pas silencieusement absorbés.

## 1. Bornes

**IN :** diagnostic du rouge en boucle (logs, cause confirmée) + traitement ou routage vers F-02/L1 ; traces de dispatch par reçus ; vérification `GET /v1alpha/sources` (lecture seule) ; doc MCP client-side si usage justifié, sinon « non requis » documenté ; contrainte secrets documentée et respectée.
**OUT :** créer une intégration (existe) ; lire une valeur de secret (interdit absolu) ; configurer « le MCP » côté Google (n'existe pas) ; migrer quoi que ce soit depuis V3 côté Jules (rien de réel) ; absorber `agent_mesh.py`/`registry.json` sans design.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Diagnostic (P0)**
- Lecture des logs Issue Factory : classification chaque run (POST Jules tenté ? verdict garde-fou ? motif ?). Verdict documenté : cause Jules vs cause R10 — avec preuves, pas avec l'hypothèse.

**Système 2 — Traces de dispatch (fiabilité)**
- Par tentative : horodatage → verdict garde-fou → session id OU motif de blocage → reçu. Chaîne auditable.

**Système 3 — Cadre MCP (optionnel, documenté)**
- Si usage justifié : doc de config `@google/jules-mcp` (clé via Secure Vault). Sinon : « non requis » + analyse. Dans les deux cas : pas de MCP côté Google.

**Système 4 — Contrainte secrets (garde-fou)**
- Documentée dans le design ; audit : aucune tentative d'extraction (aucun appel API pouvant retourner une valeur ; grep des patterns de valeurs de secrets dans le code = vide).

**Flux :** P0 (diagnostic) → traitement ou routage F-02/L1 → traces → MCP cadré → validation Doctors.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Diagnostic (OBLIGATOIRE, en premier)** | Logs des runs en échec : POST tenté ? verdict garde-fou ? → cause confirmée (Jules vs R10) avec preuves | H-G02-1 |
| **P1 — Traitement** | Cause Jules → corriger côté Jules (clé, couverture App via `GET /v1alpha/sources`, quota). Cause R10 → router vers F-02/L1 (levée du BLOCKED #61), ne pas toucher au dispatch | H-G02-2 |
| **P2 — Traces** | N tentatives tracées bout-en-bout (tentative → verdict → session/blocage → reçu) | H-G02-2 |
| **P3 — MCP** | Usage justifié ? → doc de config. Sinon → « non requis » documenté + analyse | H-G02-4 |
| **P4 — Validation** | Revue Doctors → Nardole dispatche la validation | Tous verts |

**Règle d'exécution :** séquentiel, un seul exécutant. `OWNER_STAND_DOWN=1` arrête tout.

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-G02-1 | Diagnostic avec preuves | cause du rouge en boucle identifiée (Jules vs R10) avec extraits de logs ; si R10 → routée vers F-02/L1, le dispatch n'est pas modifié pour un problème de reçu |
| H-G02-2 | Dispatch fiable et tracé | N tentatives consécutives avec trace complète (tentative → verdict → session id ou motif de blocage → reçu) ; 0 tentative non tracée |
| H-G02-3 | Contrainte secrets respectée | 0 tentative d'extraction de valeur de secret (audit des appels + grep patterns = vide) ; clé uniquement via env/Secure Vault |
| H-G02-4 | MCP cadré | doc de config **si** usage justifié, **sinon** « non requis » documenté avec l'analyse ; 0 mention d'un « MCP côté Google » |
| H-G02-5 | Aucun faux binaire | aucun livrable ne présente « MCP ou REST ? » comme choix à arbitrer — l'analyse a tranché (REST en place, MCP optionnel) |
| H-G02-6 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Le rouge en boucle est du bruit de fond.** → P0 tranche avec les logs ; si la cause est déjà traitée (F-02/L1), le diagnostic le constate au lieu de « réparer ».
- **R2 — Page Settings jules.google.com.** → Nécessite le navigateur du Capitaine (lecture seule) ; documenté, pas contourné.
- **R3 — Quotas non vérifiés (15 tâches/24 h free = source secondaire).** → Noté comme hypothèse, pas comme fait.
- **R4 — Tentation de lire un secret « pour débugger ».** → Interdit absolu (H-G02-3) ; le design ne prévoit aucune voie d'extraction.
- **R5 — `agent_mesh.py`/`registry.json` absorbés silencieusement.** → Hors périmètre explicite (§0.7), à designer séparément.

*Fin du plan G-02-C. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors (exécution après F-02).*
