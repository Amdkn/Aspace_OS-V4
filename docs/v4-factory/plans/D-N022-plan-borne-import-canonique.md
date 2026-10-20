# D-N022 — Plan borné : import canonique sans duplication (phase 2 de D-N016)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE — 2026-10-09
**Source :** dispatch D-N022 (Nardole, AGORA) ; inventaire Bill phase 1 vérifié (`~/workspace/frameworks/inventaires/duplications-brutes.md`, source `main` @ `2554e0f`)
**Constat d'inventaire :** 6 duplications FORTES, 6 MOYENNES, non-dupliqués à préserver (11 capabilities Life-only 🛡 à zéro occurrence ailleurs, `scenarios.ts` + skills approve/reject, shell store + CommandPalette + `cms/hierarchy.ts`), 1 collision de nommage (« Workspace »)
**Séquençage Clara :** après D-N017 lot 1 puis lot 2 (les gardes M-08 protègent cette canonisation) — vague A (agent/business) immédiate, **vague B (life) BLOQUÉE jusqu'au merge D-N011** (`os/life/IMPORT.json` manquant)
**Principe :** GEL ≠ COUPER. La canonisation fige et redirige — elle ne supprime aucun fichier (règle Capitaine : jamais couper le Business OS hérité en cours d'implémentation ; garde M-08 §1).
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant à la fois, vague A puis vague B.

---

## 0. Décisions design (autorité Clara — tranchées ici, ne remontent pas)

### Duplications FORTES — canonique désigné par classe

| # | Classe | Canonique | Statut de l'autre | Justification |
|---|---|---|---|---|
| 1 | Desktop shell (business ∥ agent) | **Runtime : `os/agent/src/shell/`** (Agent OS Desktop = le shell) ; **standards visuels : Business OS** (`dockSkins.ts`, 20 skins — direction de convergence déjà documentée dans le code) | `os/business/src/components/` (Desktop.tsx…) = **GELÉ** : aucun nouveau dev shell côté business ; les apps business s'exécutent dans le shell agent | Le code converge déjà vers les standards BusinessOS ; on canonise la convergence au lieu de la subir |
| 2 | Thèmes (3 lignées) | **Business OS** (source documentée des 12 thèmes : « portés depuis BusinessOS ») | Agent = **consommateur via contrat documenté** (le port existant est formalisé, plus de copie) ; Life = aligné sur le contrat pour les thèmes communs, tokens Life-only documentés comme **extension** | La source est écrite dans les en-têtes mêmes |
| 3 | Ontologie (business 621l ∥ agent 2236l) | **Périmètres disjoints officialisés** : business = ontologie de **gouvernance** (Entities/Relations/Contracts/Versions, `architecture.test.ts` verrouille les boundaries) ; agent = ontologie d'**exploration** (lignage, mining, workshop) | Modèle d'entités canonique = business ; l'explorateur agent le consomme via contrat documenté au lieu de son propre modèle | Deux outils, pas deux doublons — la fusion serait destructive |
| 4 | Paramètres système | **Désambiguïsation par périmètre** : agent = **Paramètres Système** (thèmes, wallpapers, environnement, dock) ; business = **Paramètres Business OS** (assistant, seeds métier) — l'app business est **repérimétrée et renommée**, pas coupée | `os/agent/src/apps/Settings/` = système ; `os/business/src/apps/settings/` = métier | Le système vit dans le shell, le métier dans l'OS |
| 5 | Coach OS (business source ∥ agent embed) | **Business** (plugin, skills, `api/v1`, `cli`) — **l'embed par Cadre est officialisé comme LE pattern canonique d'hébergement** : les OS s'intègrent au shell agent par embarquement, jamais par réimplémentation | `os/agent/src/apps/{CoachOS,CoachOSOnline}` = mode d'accès documenté, pas une duplication à supprimer | L'inventaire le dit : duplication architecturale, pas de code dupliqué |
| 6 | Life Engagement (life source ∥ agent embed) | **Life** (App.tsx, auth, para, shell store) — même pattern d'embed officialisé | `os/agent/src/apps/{LifeOS,LifeOSOnline}` = accès ; **`Doctor11Life` = re-périmétré en cockpit lecture seule** — ses actions s'exécutent via le cœur Life (contrat), jamais en direct (pas d'autorité parallèle) | Protège l'autorité du 11e sur le cœur Life |

### Duplications MOYENNES — canonique désigné, migration à l'évolution (pas de réécriture forcée)

| # | Classe | Canonique | Règle |
|---|---|---|---|
| 7 | Auth UX | **Pas de fusion** — les parcours first-launch restent par OS (identité) ; besoin partagé → contrat via `FOURNISSEURS.md` (business) | Documenté comme adjacent |
| 8 | Roster d'agents | **Agent** (`SubagentsRoster` — le roster opérationnel factory) ; `characters.ts` (business) = personnages narratifs, repérimétré comme tel | Pas de fusion |
| 9 | Dashboard building blocks | **Agent** (`src/blueprints/` : DataGrid, Kanban, MetricCard, BlueprintAppFactory) ; les apps business migrent leurs cartes vers les blueprints **à leur prochaine évolution** | Migration opportuniste, pas forcée |
| 10 | Harness | **La Factory M-01/M-02** = harness canonique V4 ; `adws` (business) et canary (agent) = **gelés**, lecture seule pour fixtures existantes | Tout nouveau harness passe par la Factory |
| 11 | Tâches/GTD | **Life** (`fw-gtd.store.ts` — le GTD est un framework Life) ; `TasksApp` (business) migre vers le contrat à sa prochaine évolution | Migration opportuniste |
| 12 | Voix/TTS | **REPORTÉ** — échantillon partiel (réserve) ; Bill complète l'inventaire avant canonisation | Hors scope de ce design |

### Non-dupliqués — registre des préservés
Les 11 capabilities Life-only 🛡 (zéro occurrence ailleurs au grep), `src/agent/scenarios.ts` + skills approve/reject, `src/shell/store.ts` + `CommandPalette.tsx` + `src/cms/hierarchy.ts` + `src/storage/contract.ts` sont **inscrits au registre des préservés** — toute proposition future les touchant déclenche la garde M-08 (décision S2 écrite requise).

### POINT DUR 1 — Collision « Workspace » (décision de gouvernance, vaut aussi pour D-N014)
`os/agent/src/apps/Workspace` (mini-SaaS conversationnel multi-tenant, gateway Hermes) vs `os/business/src/apps/workspace/` (gestion branches/PRs/merges) — vérifié : les deux existent sur `main`.
**Décision : renommage typé par fonction** — `os/business/src/apps/workspace/` → **`GitWorkspace`** (le nom dit la fonction : branches/PRs/merges) ; `os/agent/src/apps/Workspace/` → **`CompanionSpace`** (le nom dit la fonction : conversationnel multi-tenant).
**Règle de nommage ajoutée au contrat D-N014** (`os/ARCHITECTURE.md`) : *un nom = une fonction ; tout nouveau doublon de nom (insensible à la casse) = arbitrage Clara avant merge.*

### POINT DUR 2 — `IMPORT.json` absent pour life (D-N011 ouvert)
**Décision : l'import canonique est conditionné à la traçabilité.** Vague A (agent/business — IMPORT.json présents, source-lock OK) : immédiate. **Vague B (life) : BLOQUÉE jusqu'au merge D-N011** — aucune opération de canonisation ne touche `os/life` sans son IMPORT.json. Si D-N011 traîne, la vague B reste BLOQUÉE avec raison (Nardole), jamais contournée.

## 1. Bornes (scope strict)

**IN :**
- `os/CANONICAL.json` (registre des canoniques : par classe → canonique, consommateurs, gelés, préservés) + section correspondante dans `os/ARCHITECTURE.md` (D-N014).
- Marqueurs de gel : en-tête `GELÉ — canonique : <chemin> — voir os/CANONICAL.json` sur chaque emplacement gelé (business components, adws, agent Settings métier…).
- Renommages Workspace → GitWorkspace / CompanionSpace (mécanique : rename + imports + tests).
- Repérimétrage documenté : business Settings → « Paramètres Business OS », Doctor11Life → cockpit lecture seule, characters.ts → narratif.
- Contrats documentés : thèmes (business→agent), entités ontologie (business→agent), embed (pattern d'hébergement).
- Reçu R10 par vague.

**OUT (explicitement hors scope) :**
- **Zéro suppression de fichier** (gel ≠ coupe).
- Aucune réécriture forcée (migrations 9/11 opportunistes).
- Aucune fusion de code des shells/ontologies (périmètres officialisés, pas fusionnés).
- Classe 12 (voix/TTS) — reportée.
- Vague B sans D-N011 mergé.

## 2. Phases et gates

| Phase | Objectif | Exécutant | Gate de sortie |
|---|---|---|---|
| **P0 — Registre** | Écrire `os/CANONICAL.json` + section `os/ARCHITECTURE.md` avec toutes les décisions du §0 | Agent | **Gates :** C1 |
| **P1 — Vague A** | Marqueurs de gel + renommages Workspace + contrats documentés (agent/business uniquement) | Agent | **Gates :** C2, C4, C7 |
| **P2 — Hold-out vague A** | C1–C8 (C5/C6 partiels : périmètre agent/business) | Agent | Tous verts |
| **P3 — Vague B (gated D-N011)** | Alignement life : thèmes, embed officialisé, GTD canonique, Doctor11Life re-périmétré — **seulement si D-N011 mergé** | Agent | **Gates :** C5, C6 (complets) |
| **P4 — Revue + merge** | Revue technique 12e, merge par le 12e (doctrine AGORA) | 12e Doctor | **Gates :** C1–C8 tous verts ; C8 (R10) |

**Règle d'exécution :** une phase à la fois, un seul exécutant actif. `OWNER_STAND_DOWN=1` arrête tout.

## 3. Tests hold-out (définis AVANT exécution — validation aveugle)

| ID | Vérifie | Comment | Seuil |
|---|---|---|---|
| **C1** | Chaque duplication FORTE a une décision canonique enregistrée | `os/CANONICAL.json` couvre les classes 1–6 + 7–11 (12 = reportée) | 11/11 décisions présentes |
| **C2** | Zéro suppression | diff avant/après : aucun fichier supprimé | 0 deletion |
| **C3** | 🛡 intacts | SHA256 des 11 capabilities Life + `os/life/src/lib/api/client.ts` identiques avant/après | hashs inchangés |
| **C4** | Collision Workspace résolue | grep insensible à la casse `apps/workspace` → un seul résultat par nouveau nom | `GitWorkspace` + `CompanionSpace`, zéro doublon |
| **C5** | Vague B conditionnée à D-N011 | si D-N011 non mergé : `git diff` sur `os/life/` | vide (aucune touche) |
| **C6** | Non-dupliqués préservés | les chemins préservés existent, non modifiés hors contrat documenté | tous présents |
| **C7** | Marqueurs de gel présents | chaque emplacement gelé porte l'en-tête `GELÉ — canonique : …` | 100 % des gelés marqués |
| **C8** | Traçabilité R10 | reçu (mission_id D-N022 + SHA) par vague au ledger | présents |

## 4. Risques

- **R1 — D-N011 traîne.** → Vague B BLOQUÉE avec raison ; la vague A ne l'attend pas.
- **R2 — Tentation de « finir le travail » en supprimant les gelés.** → C2 + garde M-08 §1 : toute suppression sans décision S2 = rejet.
- **R3 — Renommage Workspace casse des imports.** → Mécanique + tests à l'exécution ; C4 vérifie le résultat, pas la méthode.
- **R4 — Conflit avec D-N014.** → Le §0 tranche aussi pour D-N014 (règle de nommage versée à `os/ARCHITECTURE.md`) ; D-N014 reste l'autorité du contrat, D-N022 son application.

## 5. Séquence d'exécution (pas un swarm)

```
[D-N017 lot1 → lot2] → D-N022 P0 (registre) → P1 (vague A) → C1–C4/C7
  → P2 (hold-out A) → [D-N011 mergé ?] → P3 (vague B) → C5/C6 → P4 (revue+merge 12e)
```

Tout écart → **BLOQUÉ** avec raison + qui débloque, enregistré par Nardole. Pas de contournement silencieux.

*Fin du plan. Signature Clara apposée — D-N022 PRÊT, dispatchable après D-N017 (vague A immédiate, vague B gated D-N011).*
