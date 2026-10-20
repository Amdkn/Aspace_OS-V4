# D-N004 — Plan borné : migration 3 OS → mono-repo `Aspace_OS-V4`

**Auteur :** 12e Doctor (cœur Buzz, plans) — 2026-10-09 ~06:45 EDT
**Source :** décision vision Capitaine 2026-10-09 (mono-repo, 3 OS réunis)
**Base :** `~/workspace/your_files/plan-migration-mono-repo.md` (5 phases, R1–R9)
**Réduction :** `~/workspace/life-os-audit/PONYTAIL-REDUCTION-PLAN.md` (audit lecture seule, 38 706 → ~13 000 lignes)
**Statut :** plan livré — **en attente signature design Clara** (D-N004 reste EN DESIGN). Aucune exécution avant sa signature. Pas un swarm : séquence stricte, un exécutant à la fois.

---

## 0. Corrections de routage (règle d'or)

Le plan d'origine adressait au Capitaine des décisions techniques. Corrigé :

**Les 6 questions du plan de réduction — tranchées par S2 (12e), 2026-10-09 ~06:45 EDT. Ne remontent JAMAIS au Capitaine.** Le 11e garde un droit de révision sur l'implémentation Life ; en cas de désaccord, S2 tranche.

| # | Question | Décision S2 | Justification |
|---|---|---|---|
| Q1 | `supabase.ts` : mock silencieux `http://mock.supabase.co` — fail-fast ou local-only assumé ? | **Mode local-only EXPLICITE + erreur visible, jamais de mock silencieux.** Au boot sans env vars : bannière d'état persistante, sync désactivée avec raison affichée. | Un mock silencieux à la frontière de confiance viole la doctrine. Le local-first (IndexedDB) continue de fonctionner ; c'est la sync qui doit échouer bruyamment. |
| Q2 | `settings/` (1 309 lignes, UI connecteurs) : couper ou garder réduit ? | **CUT. Configuration Supabase uniquement par variables d'environnement.** | Hors minimum (a)-(d). Le pattern V4 est Zero Trust : pas de secrets manipulés via UI. |
| Q3 | `mcp/` + `cli/` : couper maintenant ou garder ? | **CUT maintenant, réécrire dans V4 sous design Clara.** | 302 lignes hors minimum. Le futur serveur MCP V4 sera designé, pas hérité organiquement. |
| Q4 | `auth/` (boot path) : auth Supabase requise pour le minimum ? | **KEEP les fichiers (400 lignes, boot path intact), compte NON requis.** Le shell démarre sans compte ; l'identité est un module V4 ultérieur (Master Profile / OMK-OS-ID). | Éviter une chirurgie risquée de `App.tsx` pendant la réduction. L'auth obligatoire est une décision produit V4, pas un prérequis de migration. |
| Q5 | `cron-registry/` : les crons font-ils partie du minimum ? | **CUT du noyau migré.** La planification vit dans V4 (cœur Buzz / Ryan), pas dans l'héritage Life. | Le minimum (a)-(d) ne contient ni notifications ni rappels. Pas de double autorité de scheduling. |
| Q6 | `server/auth/` : Blackboard local strict ou exposé un jour ? | **CUT. Blackboard strictement local.** L'auth API est une responsabilité V4 (Gateway — risque résiduel déjà identifié au diagnostic), pas un héritage. | Ne pas importer un middleware d'auth pour un serveur local better-sqlite3. |

**Ordre des merges Life** — déjà tranché par S2 et **validé par le 11e Doctor le 2026-10-09 ~11:55 EDT** (revérifié via API : 6 PRs ouvertes, `mergeable_state: clean` sur les 6) : #118 → #113 → rebase #115/#117 → #111 (un-draft + CI) → #114 fermée (doublon de #113, fix B3Matrix re-filé en issue fraîche). D-N002, 11e. **Gate humain supprimé (doctrine 2026-10-09) : exécution par le 11e, plus de clics Capitaine.**

**Layout validé (12e) :** `os/life/`, `os/agent/`, `os/business/` à la racine du mono-repo.

---

## 1. Bornes (scope strict)

**IN :**
- Import fidèle des 3 OS via le gate V4 (`tools/import_v3.py` + `source-lock.json`, une entrée par OS : repo d'origine, SHA, date).
- Réduction Life selon les verdicts Ponytail corrigés (§2 du plan de réduction + §5 points d'ancrage).
- Les 3 modifications d'ancrage obligatoires : `app-registry.ts` (retirer `AgentPortalApp` statique, `para` en dockSlot 1), `Desktop.tsx` (retirer `AssistantOverlay`), `App.tsx` (retirer `bridge-worker` dynamique).
- CI scopée par sous-arbre ; ports documentés ; README par OS ; registre des capabilities au niveau mono-repo.
- Reçu R10 par OS importé (mission_id + SHA).

**OUT (explicitement hors scope) :**
- Aucune réécriture fonctionnelle pendant l'import (fidélité d'abord, traçabilité).
- Aucune résolution des conflits des PRs dans le plan de migration — c'est D-N002 (11e), prérequis.
- Pas de nouveau serveur MCP, pas de nouvelle auth, pas de scheduler hérité (voir Q3/Q4/Q5).
- Pas de `node_modules` commité, pas de workspace npm unique (décision ultérieure, pas bloquante).

**🛡 PROTÉGÉ (jamais coupé, jamais « réduit », hash vérifié) :**
- `capabilities` (définition canonique issue de #113),
- `river-adapter` (canonique issu de #113 ; le fix B3Matrix de #114 devient une issue fraîche),
- pont Life→Business (`src/lib/api/client.ts`, `127.0.0.1:3001/api/bridge`, zod).

---

## 2. Phases et gates

| Phase | Objectif | Exécutant | Gate de sortie |
|---|---|---|---|
| **P0 — Gel** | Merges #118 + #113 (D-N002) OU pin `3f11cff` ; figer le SHA canonique Life par OS | 11e (exécution, gate supprimé) | **Gate technique (12e) :** SHA canonique enregistré ; les 6 questions tranchées (fait, §0) |
| **P1 — Réduction** | Appliquer les verdicts sur clone local, branche dédiée ; 3 ancrages ; `npm run build` + `npm run gate` verts | Agent sous design Clara signé | **Gates :** H1, H2, H6 (hold-out) ; signature Clara du diff de réduction |
| **P2 — Import gate** | Branche `mission/a0/mono-3os` ; 1 commit par OS + entrée `source-lock.json` ; import fidèle, zéro réduction | A0 (prépare) + factory (push via route d'écriture : grant Contents write ou credential) | **Gate technique :** H4 ; le push n'attend plus le terminal du Capitaine (doctrine 2026-10-09) |
| **P3 — Réduction dans le mono-repo** | Remplacer `os/life` par l'arbre réduit de P1 ; boot des 3 OS vérifié | Agent sous design Clara signé | **Gates :** H1, H3, H6 |
| **P4 — Câblage** | CI scopée par sous-arbre ; ports documentés ; README ×3 ; registre capabilities mono-repo ; reçus R10 | Agent sous design Clara signé | **Gates :** H5, H7, H8 |
| **P5 — Merge** | PR `mission/a0/mono-3os` → review → merge | 12e (review + merge, autorité pleine) | **Gate technique :** H1–H8 tous verts. Pas de merge aveugle. |

**Règle d'exécution :** une phase à la fois, un seul exécutant actif par phase. `OWNER_STAND_DOWN=1` arrête tout.

---

## 3. Tests hold-out (définis AVANT exécution — validation aveugle)

L'exécutant ne redéfinit pas le succès. Chaque test est binaire (pass/fail), exécuté à la phase indiquée.

| ID | Vérifie | Comment | Seuil | Phase |
|---|---|---|---|---|
| **H1** | Le Life réduit build et le shell boot | `cd os/life && npm run build` puis `npm run gate` (validation-gate + tsc --noEmit) | exit 0 aux deux | P1, P3 |
| **H2** | Plus de mock Supabase silencieux | `grep -rn "mock.supabase.co" os/life/src` → vide ; `grep -q "local-only\|CONFIG_REQUIRED" os/life/src/lib/supabase.ts` → trouvé | les deux conditions vraies | P1, P3 |
| **H3** | Protégés 🛡 intacts après réduction | SHA256 de `capabilities.ts` (canonique #113), `river-adapter`, `src/lib/api/client.ts` identiques avant/après P1 et P3 | 3 hashs inchangés | P1, P3 |
| **H4** | Import gate V4 respecté | `source-lock.json` contient 3 entrées (life, agent, business) avec `origin_repo` + `commit_sha` + `date` | 3 entrées complètes | P2 |
| **H5** | CI V4 non régressée, checks scopés | `v4-checks.yml` verte sur la branche ; aucun check existant (`control-plane/`, `architecture/`) cassé par l'import | verte + zéro régression | P4 |
| **H6** | Ancrages appliqués | `! grep -q "AgentPortalApp" os/life/src/lib/app-registry.ts` ; `! grep -q "AssistantOverlay" os/life/src/components/Desktop.tsx` ; `! grep -q "bridge-worker" os/life/src/App.tsx` | les trois greps vides | P1, P3 |
| **H7** | Traçabilité R10 | Un reçu par OS importé (mission_id + SHA) présent dans le ledger | 3 reçus | P4 |
| **H8** | Aucun secret commité | `grep -rEi "sk-[a-z0-9]{20,}\|-----BEGIN.*PRIVATE KEY" os/*/src os/*/server` → vide (patterns existants uniquement) | vide | P2, P4 |

**Note d'honnêteté :** les verdicts Ponytail reposent sur une analyse statique sans `node_modules` (pas de build/typecheck possible dans le clone d'audit). H1 est donc aussi un test de *découverte* : s'il échoue sur un import manqué, le CUT fautif est réintégré (KEEP) au lieu d'être contourné.

---

## 4. Portes d'exécution — autorité factory (gate humain SUPPRIMÉ le 2026-10-09)

1. **Merges #118 + #113** — exécutés par le 11e (D-N002). #118 : re-run checks d'abord.
2. **Push** — via la route d'écriture établie par la factory (grant Contents write via browser, ou credential disponible). N'attend plus le terminal du Capitaine.
3. **Review + merge** de la PR `mission/a0/mono-3os` — 12e, autorité pleine.

**Arbitrage vision → Rick (S1)** (protocole codes d'exception, Capitaine 2026-10-09). Rien ne remonte directement au Capitaine. Les actions liées à ses comptes personnels (ex. grant GitHub App si le browser échoue, création du lien Stripe) sont des *capacités*, pas des décisions : la factory tente d'abord ses propres routes.

---

## 5. Risques (repris du plan d'origine, avec propriétaire)

- **R1 — Push bloqué (maître).** GitHub App sans Contents write (403). Propriétaire : Capitaine (grant humain). Tout le reste est préparable sans lui.
- **R2 — Life main en vol.** → P0 : merger #118+#113 (D-N002) ou pinner `3f11cff`. Propriétaire : 11e.
- **R3 — Mock Supabase silencieux.** → Tranché Q1 (§0) : local-only explicite. Propriétaire : 12e (décidé).
- **R4 — 3 fichiers d'ancrage.** → H6. Propriétaire : exécutant P1 sous design Clara.
- **R5 — Poids (~135k lignes, 3×node_modules, 2-core/8GB).** → Ports : Life 4444 (connu) ; Agent et Business à documenter en P4. Workspace npm unique : décision ultérieure, hors scope.
- **R6 — CI.** → H5, scoping par sous-arbre en P4.
- **R7 — Import gate.** → H4, `source-lock.json` obligatoire.
- **R8 — Secrets.** → H8.
- **R9 — Branche.** → `mission/a0/mono-3os` (nouvelle). Le Codespace reste sur sa branche mission actuelle ; la migration ne part pas de `mission/doctor12/codex-supabase-foundation` sans décision explicite.

---

## 6. Séquence d'exécution (pas un swarm)

```
P0 (11e + clics) → gate 12e → design Clara signé → P1 → H1/H2/H6
  → P2 (push humain) → H4 → P3 → H1/H3/H6 → P4 → H5/H7/H8 → P5 (review + clic)
```

Tout écart (CUT qui casse H1, conflit d'import, R1 non débloqué) → **BLOQUÉ** avec raison + qui débloque, enregistré par Nardole. Pas de contournement silencieux.

*Fin du plan. Prochaine étape : signature design Clara → Nardole passe D-N004 à PRÊT.*

---

## 7. Signature design — Clara (2026-10-09 ~09:10 EDT)

**Je signe ce plan.** Vérification règle d'or :

- ✅ Scope borné IN/OUT explicite (§1) ; aucune réécriture fonctionnelle pendant l'import.
- ✅ 🛡 Protégés identifiés avec vérification par hash (H3) — capabilities, river-adapter, pont Life→Business.
- ✅ 8 tests hold-out H1–H8 écrits AVANT toute exécution, binaires, mappés aux phases (§3). L'exécutant ne redéfinit pas le succès.
- ✅ Séquence stricte P0→P5, un seul exécutant par phase, pas un swarm (§6). `OWNER_STAND_DOWN=1` = frein d'urgence.
- ✅ Reçus R10 par OS importé (H7).

**Adaptation doctrine no-human-gate (2026-10-09) :** les 3 gates de la §4 sont réassignés — les merges relèvent des Doctors (11e pour D-N002 / #118+#113, 12e pour la PR `mission/a0/mono-3os`), plus du Capitaine. Le push terminal (R1) reste une action credential du Capitaine jusqu'au grant Contents write — c'est un déblocage, pas une décision.

**Condition de maintien :** tout CUT qui casse H1 → réintégration KEEP (note d'honnêteté §3), pas de contournement silencieux. Tout écart → BLOQUÉ enregistré par Nardole.

→ Nardole : passer D-N004 à **PRÊT**. P0 démarre au 11e (D-N002).

---

## 8. OBSOLÈTE — ne pas exécuter (2026-10-09 ~15:45 EDT)

Décision S1 (routage) : la migration décrite par ce plan a déjà été exécutée par un autre canal — **PR #27 mergée**, `os/{life,agent,business}` présents sur main (vérifié dans le repo par S1). La signature Clara (§7) portait sur un plan devenu sans objet ; le registre Nardole D-N004 passe à REJETÉ (motif : exécution déjà réalisée). **Ne pas ré-exécuter ce plan.** Le besoin résiduel éventuel (vérification post-migration) fera l'objet d'une issue distincte.
