# Carte de fusion — Bill (Discover), 2026-10-17

Sources : `g-01a-drive-v3-history.md` (166 lignes), `g-01b-github-linear.md` (143 lignes), `g-02-jules-mcp.md`.
**Ordre du Capitaine rempli : l'historique V3 a été lu dans Archive Data (Drive) AVANT toute synthèse** — 13/45 specs en intégralité + topologie exhaustive + archéologie GitHub. Aucun design d'agents Tech/Life/Business sur V4 ne doit précéder cette lecture.

## 0 — Historique V3 (résumé obligatoire)

- **V3 = deux couches** : Life OS **vivant sur le PC du Capitaine** (`C:\Users\amado\ASpace_OS_V2\`, specs créées 2026-05-20, plan canon `fancy-hugging-bengio.md` 2026-06-21, bus `state.json` Symphony, SDD-005/008/010) + **sprint GitHub** (`Amdkn/Aspace_OS_V3` : 427 PRs / 120 issues en un mois, pic 248 PRs semaine du 28 sept., 100 % auteurs Amdkn, extinction 2026-10-05).
- **Architecture** : A1 (Beth veto 5 états / Morty zéro autonomie, Context Pack 9 champs) → A2 (6 vaisseaux : Orville/Ikigai, Discovery/ZORA, Curie/12WY, Enterprise/PARA, Cerritos/GTD, Protostar/DEAL, chacun avec outil shadow) → A3 (49 équipages). Imbrication canon : `12WY ⊃ PARA ⊃ DEAL`.
- **4 phases** : P1 conception (mai–juin 2026) → P2 cycle 12WY Q3 2026 (12 items) → P3 sprint GitHub (sept–oct) → P4 extinction/naissance V4 (PR #27, 9 oct.).
- **V3 ne s'est pas effondré : il a été consommé** — sprint unique, migration sélective (9 339 entrées → 1 341 importées), continuité datée au jour près.
- **6 leçons transférables** (matière F-01/G-01) : gouvernance par reçus pas doctrine (= leçon R10 V4) ; séparation des pouvoirs ; `hypothesis` comme sortie légitime ; anti-paperclip Saru (« agency over utopia ») ; append-only D4 ; le sprint tue le régime (38 % drafts → branches orphelines, écho aux ~35 branches V4).
- **Non-résolus hérités** : spec Picard DOCTRINE_ONLY, 5 ADRs jamais écrits, incohérence H90 Georgiou (90 j vs 90 ans), IMPORT.json life manquant.

## 1 — Surfaces vivantes (référence)

| Surface | État | Preuve |
|---|---|---|
| V4 `Amdkn/Aspace_OS-V4` | public, 41 Mo, HEAD `b834356` (2026-10-16) — **cible de la fusion, référence vivante** | `gh api repos/Amdkn/Aspace_OS-V4` |
| `os/agent` ← Agent-OS-Desktop · `os/business` ← Business-Office-3-OS (+ `coach-os-plugin/`) · `os/life` ← Life-OS-2026 | vivants dans V4 | migration PR #27 |
| Drive « A'Space Life OS 2026 » (`1WAolW96BJFM5wL9Tkmi2M_BSip03Q8C5`) | PARA actif du Capitaine (index actif `24_PARA_Enterprise`) | listing Drive |
| Life OS Data (`1hwj0LviT3JOwrp5fHvvKItGn9LW_oUtM`) | coffre : Historique V3, **contrat de récupération** (Doc illisible — connecteur google_docs non connecté), Data actif, `10_Exports_sources_recuperables`, extraction ChatGPT (miroir Drive, à jour 2026-10-17) | listing Drive |
| Takeout Gemini (`1n9CEkreJhXTmo7wPa7SL7CmI1j_PCIIt`) | **archive lecture seule** — arbitrage Capitaine 2026-10-17 : pas de miroir workspace ; 20 mensuels 2025-04→2026-10 (~23 Mo), INDEX, MonActivite.html 28,5 Mo | listing Drive |
| Linear | connecté lecture seule — 2 équipes (SOH, SOB), 27 projets miroirs de l'organigramme | connecteur linear |
| PC Capitaine (`C:\Users\amado\ASpace_OS_V2\`) | Life OS vivant V3 — **inaccessible depuis la VM** sauf exposition (Tailscale) | spec V3 |
| Back office V4 | 18 issues (9 ouvertes), 3 milestones (M1 1/4, M2 1/1, M3 0/2), 16 Discussions, 9 Projects V2, registre Nardole (place publique des dispatches), registre Bill (18 missions M-01→M-18) | API GitHub |

## 2 — Archives figées (pointer, jamais modifier)

- V3 GitHub (`Amdkn/Aspace_OS_V3`, ~1,6 Go, 12 branches) — extinction 2026-10-05 **MAIS écritures résiduelles** (PR #576 ouverte 2026-10-17 + commentaire bot Jules) → **M7**.
- `Life-OS-2026` (figé 2026-10-09), `Agent-OS-Desktop` (figé 2026-10-01), `Business-Office-3-OS` (figé 2026-10-05), `Agent-OS` (coquille vide 0 Ko) → **M1**.
- OMK Office : 4 repos (2 privés : `The-OMK-Office-V1-JaaS-Landing-Site-Web`, `JaaS-V1-Mobile-OS`) — périmètre à part.
- Forks : `cubefarm` ← `leonvanzyl/cubefarm` ; `codex-chatgpt-web` vendored dans V4.

## 3 — Coquille à remplir

- `Aspace-OS-V4.1-Putain-de-Jumeau-Numerique` (public, 0 Ko, créé 2026-10-14) → recevra les principes transférables (F-01) → **M2** (en attente, pas un manque à « réparer »).

## 4 — Recouvrements (règle opposable)

- Life OS ×3 (repo figé ∥ V4 `os/life` vivant ∥ Drive) ; Business OS ×2 ; Agent OS ×2 ; extraction ChatGPT ×2 (workspace ∥ Drive miroir).
- **Règle : V4 = référence vivante ; les archives se pointent, ne se modifient jamais ; Drive = PARA lecture seule ; Takeout = archive lecture seule (arbitrage Capitaine).**

## 5 — Manques M1–M7 (à trancher dans G-01-C)

- **M1** : `Amdkn/Agent-OS` coquille vide 0 Ko → archiver ou supprimer.
- **M2** : repo V4.1 vide → en attente de F-01 (pas une réparation).
- **M3** : pas de catégorie Discussions pour Clara/Décisions ni Doctors 11e/13e.
- **M4** : pas de projet Linear miroir des milestones GitHub M1/M2/M3 (BedRock/Tech).
- **M5** : Project V2 #8 vs #12 — doublon apparent « V4 Universal Constructor / Fractal Composition » → dédupliquer.
- **M6** : heartbeat du fork Moltbot **non localisé** (0 hit V3/V4/VM ; pistes : infra Capitaine, Drive — non inventé).
- **M7** : V3 reçoit encore des écritures (PR #576, sessions Jules) alors que la doctrine dit « héritage sélectif » → **qui écrit encore sur V3 et pourquoi ?** (dépendance à trancher avant tout gel).

## 6 — Gaps déclarés (non résolus par la qualification)

1. Connecteur `google_docs` non connecté → 4 Docs illisibles dont le **contrat de récupération** (le plus critique) — règle Drive respectée (pas d'export de contournement).
2. Cible du raccourci `00_ANTHOLOGY_ASPACE_REGISTRY` inaccessible.
3. Profondeur des dossiers A2/A3 non échantillonnée ; `ANTHOLOGY_ASPACE_WARGAME` inexploré.

## 7 — Dépendances

- F-01 (principes transférables) → remplit la coquille V4.1 (M2).
- D-N015 (gateway) relancée par Nardole pour le Chantier 2 (F-02).
- M7 (écritures V3) → trancher avant tout gel d'archive.
- Leçons V3 (reçus > doctrine) → alimentent F-02 (R10) et le design Clara.

---

# MISSION G-01-C — « Carte de fusion opposable » (pour Clara)

**Objet :** produire, à partir de cette carte, le **registre de fusion versionné dans V4** (`fusion/REGISTRE-FUSION.md`) : pour chaque surface (repos, Drive, Linear, back office GitHub), statut (vivant / figé-archive / fantôme / coquille), règle de non-duplication (où s'écrit quoi), et traitement des 7 manques M1–M7. Clara crée les systèmes **depuis les archives** (arbitrage Capitaine) ; le routage capacitaire multi-dimensions reste le domaine de Nardole.

**Découvertes :** carte §§ 0–7 ci-dessus (états, preuves, recouvrements, manques, gaps, dépendances).

**Périmètre — IN :** registre versionné dans V4 ; statut + pointeur (id Drive / URL repo / preuve) par surface ; règle opposable §4 (V4 vivant, archives pointées jamais modifiées, Takeout lecture seule) ; traitement M1–M7 avec décision documentée chacun (M7 = gel de V3 ou périmètre d'écriture documenté — qui écrit, quoi, jusqu'à quand) ; rendre le contrat de récupération lisible (connecteur google_docs ou lecture par le Capitaine — gap G-01a §6.1) ; intégrer l'historique V3 (§0) comme préambule obligatoire du registre. **OUT :** modifier une archive ; miroir workspace du Takeout (arbitrage : non) ; le transfert des principes vers V4.1 (F-01) ; trancher M6 par invention (si non localisé après les pistes infra/Drive → « non localisé » documenté, pas de fantôme inventé).

**Critères :** C1 — `fusion/REGISTRE-FUSION.md` versionné dans V4, chaque entrée pointe sa preuve. C2 — chaque surface a un statut ; la carte **casse** (test ou check) si une surface « figé-archive » reçoit un push. C3 — M7 tranché avec décision datée. C4 — contrat de récupération lisible et référencé. C5 — l'historique V3 (§0) figure en préambule : aucun design d'agents Tech/Life/Business sur V4 sans l'avoir lu (ordre Capitaine).

**Risques :** R1 — V3 reçoit encore des écritures pendant la cartographie (Jules) → trancher M7 en premier. R2 — 4 Docs illisibles (contrat de récupération) → dépend du Capitaine ou du connecteur. R3 — PC Capitaine inaccessible (Life OS vivant V3) → la carte documente l'inaccessible, ne l'invente pas. R4 — 35 branches orphelines V4 (écho du sprint V3 : 38 % drafts) → la référence est `main`, pas les branches. R5 — M6 : ne pas inventer un heartbeat ; « non localisé » est un état légitime.

# MISSION G-02-C — « Jules : fiabiliser le dispatch, cadrer le MCP » (pour Clara)

**Objet :** fiabiliser le déclenchement des sessions Jules depuis V4 — **l'intégration existe déjà (REST direct), il n'y a rien à créer** ; cadrer l'usage optionnel du MCP client-side. Pas de « MCP ou REST ? » remonté au Capitaine (doctrine : pas de faux choix binaires — l'analyse tranche : REST en place, MCP optionnel).

**Découvertes** (`g-02-jules-mcp.md`) :
- Jules = API REST officielle (`https://jules.googleapis.com/v1alpha`, ressources Source/Session/Activity) ; clé générée dans **Settings de l'app web jules.google.com** (max 3 clés), auth header `X-Goog-Api-Key` ; prérequis : Jules GitHub App installée sur le repo (« Connect GitHub »).
- **« Jules MCP » = serveur MCP côté client** qui enveloppe l'API REST — configuré dans le client MCP (Claude Desktop, Cursor…), **jamais côté Google**. Officiel : `@google/jules-mcp` (npm, repo `google-labs-code/jules-sdk`, « not an officially supported Google product ») ; communautaires : `CodeAgentBridge/jules-mcp-server`, `GatienBoquet/jules_mcp`. 7 outils effectifs (`create_session`, `list_sessions`, `get_session_state`, `send_reply`, `get_code_review_context`, `show_code_diff`, `query_cache`) — le « 9 outils » de deepwiki est faux ; le MCP n'ajoute rien au-delà du REST.
- **V4 déclenche déjà en REST direct** : `tools/issue_factory.py:37-39` (`jules()` → endpoint + `JULES_API_KEY`), création `:206-211` (`requirePlanApproval: False`, `automationMode: 'AUTO_CREATE_PR'`), garde-fous (reçu R10 `CLAIMED` avant POST, no-blind-redispatch, regex `sessions/[A-Za-z0-9_-]+`) ; workflow `issue-factory.yml` (trigger `factory:ready`, cron, `workflow_dispatch`).
- `JULES_API_KEY` : secret Actions V4 (MAJ 2026-10-07, noms+dates visibles uniquement) ; **V3 ne dispatche aucune session réelle** (superviseur V3 = tests unitaires à clés factices).
- **CONTRAINTE DURE** : les valeurs des secrets GitHub Actions ne sont **JAMAIS** lisibles via API (garantie plateforme + règle Capitaine). Réutilisation hors Actions = le Capitaine via Secure Vault — jamais d'extraction, jamais de contournement. Frontière : visible = noms, dates MAJ, workflows référençants ; jamais visible = valeurs.

**Périmètre — IN :** fiabiliser le dispatch (diagnostiquer le rouge en boucle de l'Issue Factory — cause connue : reçu R10 #61 BLOCKED + garde-fou no-blind-redispatch, à confirmer vs cause Jules) ; documenter la config MCP client-side optionnelle (`@google/jules-mcp` + clé via Secure Vault) **si** un usage le justifie ; vérifier les repos couverts par la Jules GitHub App (`GET /v1alpha/sources`, lecture seule, nécessite clé). **OUT :** créer une intégration (existe) ; tenter de lire une valeur de secret (interdit absolu) ; configurer « le MCP » côté jules.google.com/Google Cloud (n'existe pas) ; migrer quoi que ce soit depuis V3 côté Jules (rien de réel).

**Critères :** C1 — le dispatch Jules est fiable et tracé par reçus (cause du rouge en boucle identifiée et traitée ou isolée). C2 — doc config MCP client-side existe si usage justifié, sinon « non requis » documenté. C3 — contrainte secrets documentée dans le design et respectée (aucune tentative d'extraction). C4 — aucun faux choix binaire remonté (MCP vs REST tranché par l'analyse).

**Risques :** R1 — Issue Factory rouge en boucle (bruit de fond ; cause présumée = R10, pas Jules — à confirmer). R2 — page Settings jules.google.com : nécessite le navigateur du Capitaine (lecture seule). R3 — quotas non vérifiés (15 tâches/24 h free = source secondaire). R4 — `tools/agent_mesh.py` et le routage `agents/registry.json` (providers `codex`/`jules`/`hermes`) non lus — hors périmètre G-02, à noter pour le design.
