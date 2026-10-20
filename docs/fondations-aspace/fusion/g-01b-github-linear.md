# G-01b — Fusion overview : volet GitHub + Linear

**Mission :** Bill (holon DISCOVER) — qualification « Fusion overview » (G-01), volet GitHub+Linear.
**Date :** 2026-10-17 ~04:50 EDT · **Méthode :** `gh` authentifié (URLs API avec `/repos/`), protocole git comme référence, connecteur Linear (statut : connecté).
**Contraintes :** lecture seule partout ; aucun commit/push/merge/commentaire ; aucune valeur de secret lue.

---

## 1 — Les repos GitHub (compte Amdkn)

### Cibles de la mission

| Repo | Existe | Visibilité | Taille | Dernier push | Objet (1 ligne) | Relation avec V4 |
|---|---|---|---|---|---|---|
| `Amdkn/Aspace_OS_V3` | ✅ | public | **1 684 070 Ko (~1,6 Go)** | 2026-10-17T00:51:24Z | Héritage V3 (source primaire — cf. § recouvrements) | **Source** : V4 en est l'héritier sélectif (migration Lot A, PR #27). 12 branches. PR #576 ouverte le 2026-10-17 (kernel, « verify runtime integrity and log linear mcp governance update ») — **des sessions (Jules) opèrent encore sur V3** |
| `Amdkn/Aspace_OS-V4` | ✅ | public | 41 098 Ko | 2026-10-16T21:42:22Z (HEAD `b834356`, main) | Vaisseau actuel — « Stark Jarvis Industry 🏭 » | **Cible de la fusion** : mono-repo `os/{agent,business,life}` |
| `Amdkn/Life-OS-2026` | ✅ | public | 1 833 Ko | 2026-10-09T14:28:45Z | « The Bridge — Life OS Client (V0.9) » : shell React 19 + Vite 6 + Zustand, port 4444, 5 apps internes (command-center, para, ikigai, life-wheel, agent-portal) | **Source migrée** : réduit via Ponytail puis importé dans V4 `os/life` (PR #27). Repo figé au 2026-10-09 = dernière version standalone |
| `Amdkn/Agent-OS-Desktop` | ✅ | public | 806 Ko | 2026-10-01T06:45:47Z | « Agent OS V3 Web Desktop — Tech OS, Life OS & Business OS (Dock V3, 20 Skins, Window Manager) » | **Source migrée** : `os/agent` dans V4 (142 fichiers, fidèles) |
| `Amdkn/Agent-OS` | ✅ (vide : 0 Ko) | public | 0 Ko | 2026-09-08 | « Agent OS V3 — Desktop Unifié Tech OS, Life OS & Business OS » — coquille vide | Aucune (repo fantôme ; **manque : à archiver ou supprimer**) |
| **Coach OS** | ⚠️ **pas de repo dédié** | — | — | — | — | **Vit dans V4** : `os/business/coach-os-plugin/` (`mcp.json`, `plugin.json`, `skills/`) + `os/business/coach-os.bat` (launcher Windows local, Vite :5173, « démarre Coach OS en local »). Coach OS = **plugin du Business OS**, pas un repo |
| `Amdkn/The-OMK-Office-V1-JaaS-Landing-Site-Web` | ✅ | **private** | 660 Ko | 2026-09-20 | Landing OMK Office V1 (75 services, « Passeport » $300/an, CTA Stripe) | Périmètre OMK Office (produit, pas kernel) |
| `Amdkn/The-OMK-Office1.0-JaaS` | ✅ | public | 3 712 Ko | 2026-09-28 | The OMK Office 1.0 JaaS | Périmètre OMK Office |
| `Amdkn/The-OMK-Mobile-Back-Office` | ✅ | public | 4 191 Ko | 2026-10-04 | « Your JaaS, BaaS, PaaS Office » | Périmètre OMK Office |
| `Amdkn/JaaS-V1-Mobile-OS` | ✅ | **private** | 4 520 Ko | 2026-09-11 | « JaaS V1 » (mobile) | Périmètre OMK Office |
| `Amdkn/Business-Office-3-OS` | ✅ | public | 16 341 Ko | 2026-10-05 | « Business Office 3 OS » — desktop exécutif trimodal FR (Web Desktop + dashboard + télécommande mobile) | **Source migrée** : `os/business` dans V4 (1 345 fichiers, fidèles) |
| `Amdkn/BusinessOS` | ✅ (fork) | public | 122 859 Ko | 2026-10-02 | Fork de `omk-services/OMK-DESKTOP-WEB-OS` | Amont OMK — pas dans V4 |
| `Amdkn/01-OMK-Business-OS` | ✅ | public | 133 Ko | 2026-10-02 | (sans description) | Périmètre OMK — statut à clarifier |

### Repos connexes relevés

| Repo | Note |
|---|---|
| `Amdkn/Aspace-OS-V4.1-Putain-de-Jumeau-Numerique` | ✅ public, **0 Ko (vide)**, créé 2026-10-14T07:24:21Z par le Capitaine — **coquille vide, contenu non audité** |
| `Amdkn/cubefarm` | Fork de `leonvanzyl/cubefarm` (242 Ko) — source du socle CubeFarm remplacé par V4 (cf. issue V4 #1 fermée) |
| `Amdkn/codex-chatgpt-web` | Fork de `miuuyy/codex-chatgpt-web` (27 Mo) — vendored dans V4 (`codex-chatgpt-web/` à la racine) |
| `Amdkn/00-omk-saas-os` | Fork de `omk-services/00-omk-saas-os` |
| `Amdkn/aspace_amiral`, `aspace_a0_amadeus`, etc. | Repos archivés (cockpits 2025) — hors périmètre fusion |

**Preuves :** `gh repo list Amdkn --limit 100 --json name,visibility,diskUsage,isArchived,isFork,pushedAt,description` (2026-10-17) ; `gh api repos/Amdkn/<repo>` ; `gh api repos/Amdkn/<repo> --jq '.parent.full_name'` pour les forks.

---

## 2 — V4 : back office GitHub

### Issues : 18 au total (9 ouvertes, 9 fermées)

**Ouvertes** (`gh issue list -R Amdkn/Aspace_OS-V4 --state open`) :
- #64 `[S2][ARBITRAGE] Conflit D3/D5 : schéma temporal strict rejette les assertions dict du CLI memory`
- #61 `[M1][MISSION] [SUIVI] Régénérer os/life/IMPORT.json manquant (traçabilité post-migration)`
- #37 `[M2][MISSION-S2] Validation temporelle honnete : schema, dates, correlation chronologique`
- #28 `[TEST] Circuit auto-label → factory → Jules`
- #6 `[TRANSVERSAL][V4] Première mission utile inter-Core et preuve de reprise`
- #5 `[KERNEL][BUZZ][V4] Factory réentrante et dispatch sans réveils parasites`
- #4 `[BUZZ][KERNEL][V4] GitHub : intégration vérifiable et résultat livré`
- #3 `[KERNEL][LIFE][V4] Continuité des missions et persistance réconciliée`
- #2 `[KERNEL][V4] Autorité inter-harness, leases et promotions de capacités`

**Fermées** : #60 (CRLF watch), #57 (vérification post-migration mono-repo), #41 (REPRISE D6 capacités), #35 (journal append-only), #33 (capabilities.json), #32 (aspace/memory.py), #31 (CI Windows), #30 (CRLF racine), #1 (socle CubeFarm → fondation V4).

### Milestones : 3 (toutes ouvertes)
- **M1 — Stabilisation** : 1 ouverte / 4 fermées
- **M2 — Coeur temporel** : 1 ouverte / 1 fermée
- **M3 — Qualification** : 0 ouverte / 2 fermées

### Discussions : 16 au total
| Catégorie | Nombre |
|---|---|
| S3 · Compagnons | 12 (dont cadrages issues #2–#6, #28, #30–#32, #35, #37 ; organigramme S1/S2/S3 #42) |
| Nardole · Dispatch | 1 (#23 — mode d'emploi des canaux holons, épinglée) |
| River · Flux | 1 (#25 — continuité Drive → Linear) |
| Life Core | 1 (#14 — huit univers L2) |
| Kernel Core | 1 (#46 — décision des 18 capacités) |

**Manque :** catégories Doctors 11e/13e actives (seuls Life Core et Kernel Core ont 1 discussion chacun) ; pas de catégorie « Décisions » Clara dédiée en Discussions (Clara travaille hors Discussions).

### Projects (V2) : 9, tous ouverts
#13 « Aspace OS V4 — Factory » · #12 « V4 Universal Constructor / Fractal Composition » · #11 « Business OS — Semantic Full Stack & Launch » · #10 « Agent OS — Capability & Harness Control Plane » · #9 « A'Space Foundation Convergence » · #8 « V4 Universal Constructor — Fractal Composition » (doublon apparent avec #12 — **à dédupliquer**) · #7 « Bill Research Atlas v1 » · #6 « DC Sovereign v1 » · #5 « Ryan Factory Builder ».

**Preuves :** `gh issue list -R Amdkn/Aspace_OS-V4 --state open/closed` ; `gh api repos/Amdkn/Aspace_OS-V4/milestones` ; `gh api "repos/Amdkn/Aspace_OS-V4/discussions?per_page=100"` ; `gh project list --owner Amdkn`.

---

## 3 — Heartbeat du fork Moltbot : NON LOCALISÉ

**Recherche (2026-10-17) :**
- `gh search repos moltbot --owner Amdkn` → **aucun repo**
- `search/code` « moltbot » dans V4 et V3 → **0 résultat**
- `search/code` « heartbeat » dans V4 → **0 résultat**
- Workspace VM : « moltbot » n'apparaît que dans **un transcript vidéo YouTube** (`v4-factory/.../40_Memory/raw/9453e91d...` — passage sur Clawbot→Moltbot→OpenClaw→Moltbook, le renommage du projet de Peter Steinberger) ; « heartbeat » n'apparaît que dans les **crons A0** (`cron.d/minutely/heartbeat__interval@30m.md`, archives S1/S2/S3) — c'est le heartbeat BedRock d'A0, pas un fork.

**Verdict : aucun fork Moltbot localisé sur GitHub (repos + code V3/V4) ni sur la VM.** Pistes restantes (hors de ce volet) : infra du Capitaine (PC, Umbrel « Amdkn7 »), dossier Drive, ou nom de code d'un autre volet G-01. **À qualifier par le volet Drive/infra — ne pas inventer.**

---

## 4 — Back office Linear

**Connecteur : `connected`** (`/opt/hatch/bin/linear status` → `auth_status: connected`, MCP `https://mcp.linear.app/mcp`). Lecture seule (pas d'écriture tentée, conformément à la contrainte).

### Équipes : 2
- **SOH** — Self Operating Hubs (créée 2026-05-21)
- **SOB** — Self Operating Business (créée 2026-05-21)

### Projets : 27
- **SOH (19)** : P-SOH-1→6 (A2 : Holo Janeway/Protostar-DEAL, Orville-Ikigai, Holo Deck/Cerritos-GTD, Computer/Enterprise-PARA, Curie-12WY, Discovery/ZORA-Life Wheel), P-SOH-7 (S2 Kernel Core), P-SOH-8 (S2 Life Core), P-SOH-9 (S2 Buzz Core), P-SOH-10 (Archive pré-S2), P-SOH-19 (Anthology Cross-Surface Wargame), P-SOH-20→27 (**L1 : LD01 Carrière/Business–Book … LD08 Impact–Georgiou**, les 8 domaines Life)
- **SOB (8)** : P-SOB-11→18 (Growth–Superman, Sales–Martian Manhunter, Product–Flash, Ops–Batman, IT–Cyborg, Finance–Wonder Woman, People–Green Lantern, Legal–Aquaman — squads Marvel/DC)

**Recouvrement constaté :** la structure Linear (SOH/SOB, A2, S2, L1-LD01…LD08) **miroite l'organigramme A'Space** (Discussion V4 #42) — c'est le back office de la même organisation, pas un doublon. **Manque :** pas de projet Linear « V4 Factory / BedRock » aligné sur les milestones GitHub M1/M2/M3 (les 27 projets sont Life/Business ; le Tech/Kernel GitHub n'a pas de miroir Linear visible).

**Preuves :** `/opt/hatch/bin/linear call-tool --name list_teams` ; `list_projects` (2026-10-17).

---

## 5 — Recouvrements, manques, dépendances

### Recouvrements (même objet, plusieurs surfaces)
1. **Life OS ×3** : repo `Life-OS-2026` (figé 2026-10-09) ∥ V4 `os/life` (réduit Ponytail, vivant) ∥ Life OS Drive (volet Drive — à cartographier). **Règle : V4 `os/life` = référence vivante ; les deux autres = archives à pointer, pas à modifier.**
2. **Business OS ×2** : repo `Business-Office-3-OS` (figé 2026-10-05) ∥ V4 `os/business` (1 345 fichiers, vivant). Même règle.
3. **Agent OS ×2** : repo `Agent-OS-Desktop` (figé 2026-10-01) ∥ V4 `os/agent` (142 fichiers, vivant). Même règle.
4. **Coach OS** : **pas un repo** — plugin dans V4 `os/business/coach-os-plugin/` + launcher. Tout design « Coach OS » (D-N014) travaille sur V4, pas sur un repo externe.
5. **OMK Office** : 4 repos (2 publics, 2 privés) — périmètre produit distinct du kernel ; dépendance : le kernel V4 doit exposer ce que l'OMK consomme (à typer).
6. **Linear × GitHub** : même organigramme (SOH/SOB, cores, LD01–LD08) sur deux back offices — pas de doublon, mais **pas de pont documenté** (Discussion #25 « Continuité Drive → Linear » est une proposition, pas un état).

### Manques
- M1 : `Amdkn/Agent-OS` = coquille vide 0 Ko (archiver ou supprimer).
- M2 : repo V4.1 vide (0 Ko, créé 2026-10-14) — coquille en attente du transfert des principes (F-01).
- M3 : pas de catégorie Discussions pour Clara/Décisions ni pour les Doctors 11e/13e.
- M4 : pas de projet Linear miroir des milestones GitHub M1/M2/M3 (BedRock/Tech).
- M5 : Project V2 #8 vs #12 — doublon apparent « V4 Universal Constructor / Fractal Composition » (à dédupliquer).
- M6 : heartbeat du fork Moltbot non localisé (cf. §3).
- M7 : V3 reste vivant (PR #576 ouverte le 2026-10-17, sessions Jules actives) alors que la doctrine dit « V3 = héritage sélectif » — **dépendance à trancher : qui écrit encore sur V3 et pourquoi ?**

### Dépendances (ordre de lecture pour la fusion)
1. V3 (`Aspace_OS_V3`) = passé/patrimoine — se lit en premier (ordre du Capitaine : historique V3 dans Archive Data AVANT tout design).
2. Les 3 repos-sources figés (Life-OS-2026, Agent-OS-Desktop, Business-Office-3-OS) = état pré-migration.
3. V4 = présent vivant, référence de fusion (`os/agent`, `os/business`, `os/life`, `capabilities.registry.json`, `PORTS.md`).
4. Linear + Discussions + Projects = back office de pilotage (pas de code).
5. Drive (Life OS, Takeout, Archive Data) = mémoire — volet séparé.

---

## 6 — Mission typée pour Clara (proposition)

**G-01-C — « Carte de fusion opposable » :** produire, à partir de cette qualification (+ volets Drive/infra), la carte de la fusion sous forme de **registre versionné dans V4** (`fusion/REGISTRE-FUSION.md`) : pour chaque surface (repos, Drive, Linear, back office GitHub), statut (vivant / figé-archive / fantôme), règle de non-duplication (où s'écrit quoi), et traitement des 7 manques M1–M7. Critères : chaque entrée pointe sa preuve ; la carte casse (test ou check) si une surface « archive » reçoit un push ; M7 tranché (gel de V3 ou périmètre d'écriture documenté).
