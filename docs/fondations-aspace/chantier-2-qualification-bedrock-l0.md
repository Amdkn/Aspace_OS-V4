# Chantier 2 — Qualification BedRock L0 (état réel vs attendu)

**Mission :** Bill (holon DISCOVER) — « Finalisation des Fondations Aspace », dispatch S1 Rick, go Capitaine via A0.
**Date :** 2026-10-17 ~02:30 EDT · **Référence d'écart :** audit GitHub du 2026-10-17.
**Méthode :** lecture du code (clone frais `/tmp/v4-l0-check`, HEAD `b834356`), `gh` authentifié (URLs API avec préfixe `/repos/`), protocole git comme référence des arbres. Lecture seule stricte — aucun commit, push, merge, commentaire.
**Repo :** Amdkn/Aspace_OS-V4 (public), branche `main`.

**Contexte vérifié :** Issue Factory rouge en boucle (6 échecs consécutifs le 2026-10-17 : 03:24 → 05:44 UTC, 14–17 s chacun — `gh run list --workflow issue-factory.yml`) ; 35 branches distantes (`git ls-remote --heads | wc -l`).

---

## 1. Ledger R10 — 🔴 ROUGE (mécanisme à l'arrêt)

**Attendu :** un ledger de reçus R10 vivant — « aucun agent 'active' sans reçu », chaque mission se termine par un reçu, le mécanisme tourne et bloque sans reçu.

**Réel vérifié :**
- Le ledger EXISTE : `~/workspace/kernel/holons/ledger-graham.md` (652 lignes, hors repo) — 22 reçus `G-20261009-001` → `G-20261009-022`, discipline de vérité temporelle (`observed_at` / `recorded_at`), dernier reçu = merge PR #27 le 2026-10-09 11:16 EDT.
- La règle « sans reçu, pas de merge » n'existe que comme doctrine dans `.github/agents/s3-companions.agent.md:27-29` (« une mission se termine au reçu R10 final — sans reçu, pas de merge ») — **aucune enforcement codée** (ni CI, ni hook, ni script d'émission trouvé dans `tools/` ou `control-plane/`).
- **Aucun reçu émis depuis 8 jours** (dernier : 2026-10-09). Graham dormant depuis le 2026-10-09 (side-chat `059b0c23`, aucun fichier modifié depuis).
- Aucun artefact de reçu dans le repo (`grep -r "G-2026"` : rien ; seuls `os/business/src/lib/saas-builder/ledger.store.ts` — ledger SaaS sans rapport — et `os/business/_audit/PHASE0_RECEIPT.md`).

**Écart :** le ledger a fonctionné le 2026-10-09 (22 reçus) mais ne fonctionne plus comme mécanisme vivant : processus manuel, mono-rédacteur, hors repo, sans enforcement codée, rédacteur dormant.

**Preuves :**
- `grep -n "^## G-" ~/workspace/kernel/holons/ledger-graham.md` → 22 reçus, dernier `G-20261009-022` (merge PR #27, recorded_at 2026-10-09).
- `grep -rli "emit.*receipt\|R10.*receipt" tools/ control-plane/` (clone) → aucun résultat.
- `.github/agents/s3-companions.agent.md:27` → doctrine seule.

---

## 2. Supabase connecté — 🟢 VERT (DDL) / ⚪ NON VÉRIFIÉ (connexion live)

**Attendu :** Supabase connecté — DDL versionné dans le code + connexion vérifiée.

**Réel vérifié :**
- **DDL versionné PRÉSENT** (contredit l'audit « DDL absent du code » sur ce point) : `os/business/supabase/migrations/` (~20 fichiers : `2026-08-15_*`, `2026-08-17_*`, `20260811*` — audit events, memberships, RLS, jwt hooks, cognition, seeds) ; `os/life/supabase/migrations/20261001021212_bootstrap_local_first_persistence.sql` + `config.toml` ; `os/business/supabase/` contient aussi `EVOLUTION.md`, `VERIFICATION_RLS.md`, `tools/`.
- **Clients présents :** `os/life/src/lib/supabase.ts` — fail-fast explicite D13-01 (erreur si `VITE_SUPABASE_URL`/`VITE_SUPABASE_ANON_KEY` absents, sauf `VITE_LIFE_LOCAL_ONLY=true` avec bannière visible) ; `os/business/src/lib/supabase.ts` — thin client singleton (+ tests `supabase.test.ts`, `supabase.inlining.test.ts`, `backend.supabase.test.ts`).
- Doc : `architecture/SUPABASE_RUNTIME.md` présent.

**Écart :** la partie « connecté » (connexion live vérifiée contre une instance) **n'est pas prouvable depuis le code seul** — elle exige des secrets d'environnement. Aucune sonde de connexion automatisée trouvée dans le repo.

**Preuves :**
- `ls os/business/supabase/migrations/ | wc -l` → ~20 fichiers (clone `/tmp/v4-l0-check`, HEAD `b834356`).
- `head -30 os/life/src/lib/supabase.ts` → fail-fast D13-01 cité verbatim.

---

## 3. Gateway avec auth — 🔴 ROUGE (confirmé, inchangé)

**Attendu :** un gateway avec authentification, en code, dans V4.

**Réel vérifié :**
- **Aucun code serveur gateway dans V4.** Seuls : specs `os/life/openspec/changes/TOTAL_Spec/{PRD,DDD,ADR}/…FleetGateway.md`, `os/business/tools/watchdog-agentgateway.ps1`, et `evidence/gateway_openclaw._qualification.json`.
- Le fichier d'évidence M-16/D-N019 (2026-10-09, Ryan/Doctor 13) concluait déjà : `"Code de service Gateway dans V4": "fail"` — « Aucun : seuls …FleetGateway.md (specs) et …watchdog-agentgateway.ps1 », verdict global `NEEDS_LIVE_CHECK`.
- `find . -path "*gateway*" (*.ts|*.js|*.py)` hors specs/watchdog/evidence → **aucun résultat** ; `find` auth middleware → aucun ; `grep -rli "gws.*oauth"` → aucun (GWS OAuth absent confirmé).
- Aucun commit gateway/auth depuis le 2026-10-09 dans les messages (`gh api repos/Amdkn/Aspace_OS-V4/commits?since=2026-10-09` filtré).
- D-N015 : aucune issue trouvée (`gh issue list --search "D-N015"` → vide) — le dispatch reste sans trace GitHub.

**Écart :** le gateway avec auth n'existe pas en code ; l'état rouge du 2026-10-12 est inchangé.

**Preuves :**
- `evidence/gateway_openclaw._qualification.json` : `"result": "fail"`, `"Code de service Gateway dans V4"`.
- Commandes `find`/`grep` ci-dessus → vides (clone HEAD `b834356`).

---

## 4. CI réellement bloquante — 🟢 VERT (avec réserve documentée)

**Attendu :** la protection de branche bloque réellement les merges sans checks verts.

**Réel vérifié :**
- **Protection configurée** (`gh api repos/Amdkn/Aspace_OS-V4/branches/main/protection`) : `required_status_checks` = [`verify (ubuntu-latest)`, `verify (windows-latest)`] (app_id 15368) ; `enforce_admins: false` ; `allow_force_pushes: false` ; `allow_deletions: false`.
- **Effective en pratique (échantillon) :** 4/4 dernières PRs mergées vérifiées avec les deux checks verts AVANT merge :
  - #84 (merge 2026-10-16T21:42Z) : `verify (ubuntu-latest)` + `verify (windows-latest)` = completed/success à 21:30Z sur le head `292d92d8`.
  - #83, #81, #78 : idem (success sur les heads).
- **Réserve :** `enforce_admins=false` — l'owner (Amdkn, auteur des 8 dernières PRs mergées) **peut** bypasser la protection. Aucun bypass observé dans l'échantillon, mais la porte existe et n'est pas journalisée comme telle.

**Écart :** aucun écart observé sur l'échantillon ; la réserve `enforce_admins=false` est le seul point dur.

**Preuves :**
- `gh api repos/Amdkn/Aspace_OS-V4/branches/main/protection --jq .required_status_checks.contexts` → les deux contextes.
- `gh api repos/Amdkn/Aspace_OS-V4/commits/<head>/check-runs` → success (4 PRs).

---

## 5. Policy store versionné — 🔴 ROUGE (inexistant en tant que composant)

**Attendu :** un policy store versionné (répertoire/fichier dédié, historique git des changements de politiques).

**Réel vérifié :**
- **Aucun composant dédié trouvé** : `find -iname "*polic*"` → seulement des policies RLS SQL (`os/business/supabase/migrations/2026-08-17_*_policies.sql`), `retry-policy.ts` et `limits-policy.json` (codex-chatgpt-web) — ce sont des politiques de données / retry, pas un policy store de gouvernance.
- `grep -rli "policy.store\|policy store" --include="*.md"` → **aucun résultat**.
- Les docs de gouvernance existent (`architecture/Conseil_S2_Decision_18_capacites.md`, etc.) mais ce ne sont pas un store versionné de politiques opposable au runtime.

**Écart :** le composant n'existe pas ; rien n'en tient lieu de façon versionnée et opposable.

**Preuves :** commandes `find`/`grep` ci-dessus → vides ou non pertinentes (clone HEAD `b834356`).

---

## 6. S3 Compagnons opérationnels — 🔴 ROUGE (1/9 actif)

**Attendu :** les 9 Compagnons nommés (correction lore 2026-10-17) opérationnels : Yaz—Observatoire, Ryan·Factory, Bill—Frameworks, Clara—Décisions, Nardole—Agora, Rory—Preuves, Amy—Interfaces, River—Flux, Graham—Mémoire.

**Réel vérifié** (traces locales `~/side-chats/<id>/`, dernier fichier modifié) :

| Compagnon | Chat ID | État | Preuve |
|---|---|---|---|
| Bill—Frameworks | `500abaec` | 🟢 ACTIF | fichiers modifiés le 2026-10-17 (mission en cours) |
| Graham—Mémoire | `059b0c23` | 🟠 DORMANT | dernier fichier : 2026-10-09 ~11:20 EDT |
| Amy—Interfaces | `337fb65c` | 🟠 DORMANT | dernier fichier : 2026-10-09 ~06:20 EDT |
| Ryan·Factory | `a152c901` | 🟠 DORMANT | dernier fichier : 2026-10-09 ~19:02 EDT |
| Nardole—Agora | `ae7d36d1` | 🟠 DORMANT (registre) | pas de répertoire local ; `REGISTRE-NARDOLE.md` actif jusqu'au 2026-10-11 (D-N019 MERGÉ), 6 jours de silence depuis |
| Yaz—Observatoire | `e1ac3b2d` | ⚪ SANS TRACE LOCALE | aucun répertoire `~/side-chats/e1ac3b2d` |
| Clara—Décisions | `ef2544e6` | ⚪ SANS TRACE LOCALE | aucun répertoire `~/side-chats/ef2544e6` |
| Rory—Preuves | `5dba06d6` | ⚪ SANS TRACE LOCALE | aucun répertoire `~/side-chats/5dba06d6` |
| River—Flux | `dfd97c8e` | ⚪ SANS TRACE LOCALE | aucun répertoire `~/side-chats/dfd97c8e` |

(À titre de contexte : S1 Rick `2428b187` actif le 2026-10-17, 12e Doctor `7489b6f0` dormant depuis le 2026-10-09 ; 11e `6f410ddd` et 13e `a517ae1d` sans trace locale.)

**Écart :** 1/9 actif (Bill), 3 dormants depuis le 2026-10-09, 1 dormant-via-registre (silence depuis le 2026-10-11), 4 sans aucune trace locale. « Sans trace locale » ≠ preuve d'inexistence du chat — à confirmer via `chat.list`, indisponible à cet agent.

**Preuves :** `ls ~/side-chats/` (6 répertoires) ; `find <dir> -type f -printf '%T@'` → derniers mtimes ci-dessus ; `ls -la ~/workspace/v4-factory/dispatch/REGISTRE-NARDOLE.md` → 11 oct. 12:46.

---

## Synthèse des verdicts

| # | Composant | Verdict | En une phrase |
|---|---|---|---|
| 1 | Ledger R10 | 🔴 ROUGE | Ledger existant (22 reçus) mais à l'arrêt depuis le 2026-10-09, manuel, sans enforcement codée |
| 2 | Supabase connecté | 🟢/⚪ VERT (DDL) / NON VÉRIFIÉ (live) | DDL versionné présent (contredit l'audit) ; connexion live non prouvable sans secrets |
| 3 | Gateway avec auth | 🔴 ROUGE | Aucun code serveur ; specs seules ; inchangé depuis le 2026-10-09 |
| 4 | CI réellement bloquante | 🟢 VERT | Configurée + effective sur 4/4 PRs ; réserve : `enforce_admins=false` |
| 5 | Policy store versionné | 🔴 ROUGE | Inexistant en tant que composant |
| 6 | S3 Compagnons | 🔴 ROUGE | 1/9 actif, 4 dormants, 4 sans trace locale |

**Contexte confirmé :** Issue Factory rouge en boucle (6 échecs le 2026-10-17) ; 35 branches distantes.

**Contraintes respectées :** lecture seule stricte — aucune écriture hors ce livrable, aucun commit/push/merge/commentaire, pas d'écriture Linear.
