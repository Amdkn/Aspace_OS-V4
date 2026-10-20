# SB-01 — Plan borné : Lot 1 — docs/designs → GitHub (~11 Mo)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) ; inventaire Bill (`~/workspace/sandbox-extraction/inventaire-sandbox.md`, lecture seule, 6,6 Go)
**Contraintes inviolables :** extraction = **copie vérifiée SHA, jamais de déplacement** — sandbox intacte ; manifeste par lot (pattern extraction GPT) ; **aucun push sans validation Doctors** ; aucun repo créé sans arbitrage vision ; secrets jamais dans le lot.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Contenu du lot (copie de fichiers, pas push git)** : `fondations-aspace/`, `frameworks/`, `kernel/`, `pixel-agents-fork/`, `custom-skills/`, `custom-connectors/`, `life-os/`, `systems/`, `v4-factory/` (docs : plans/, dispatch/REGISTRE-NARDOLE.md, specs/, discussions/, control-plane/, evidence-drafts/, phase4/, templates/, agents-profiles/, rebases-life/README.md), `life-115-117.bundle`, `skills/`. **Exclu du lot** : `life-os-audit` (→ SB-03, mécanisme git push, pas copie), `user/` (fichiers personnels — `freellmapi-keys.json` **jamais** dans le lot), `memory/`, runtime (`feed/`, `proactivity/`, `email/`, `cron.d/`, `self_improvement/`, `system/`, `objectives/`).
2. **Mapping de nommage (`Amdkn/Aspace_OS-V4` — cible arbitrée)** : racine `docs/` — `docs/fondations-aspace/`, `docs/frameworks/`, `docs/pixel-agents-fork/`, `docs/systems/`, `docs/life-os/`, `docs/v4-factory/` (structure interne préservée), `skills/` + `custom-skills/` fusionnés sous `skills/` (code versionné réutilisable — un seul arbre, pas de doublon), `custom-connectors/` tel quel. **Exception** : `kernel/holons/ledger-graham.md` → **`ledger/` à la racine** (import genesis, selon F-02/L1 — pas de duplication sous `docs/`). `life-115-117.bundle` → `docs/v4-factory/rebases-life/` (artefact d'historique git, 1,8 Mo — c'est du code/historique, pas une archive média).
3. **Cible verrouillée (arbitrage Capitaine 2026-10-17) : `Amdkn/Aspace_OS-V4`.** Le mapping §0.2 s'applique. Aucune branche alternative — le design ne prépare plus qu'une cible.
4. **Gate avant push** : validation Doctors obtenue (arbitrage repo enregistré — la cible est tranchée, la validation reste requise).
5. **`skills/` → GitHub avec `custom-skills/`** (décision documentée) : ce sont du code versionné réutilisable (doctrine : GitHub = code/designs) — pas de l'état runtime.
6. **Défense secrets (transverse, arbitrage Capitaine)** : `freellmapi-keys.json` n'entre dans **aucun** manifeste d'extraction (SB-01/02/03) — **jamais Drive, jamais GitHub** (non négociable). Stockage → Secure Vault via le flow sécurisé, **hors design** (à l'exécution, pas pendant). Grep patterns de secrets sur le lot avant préparation (H-SB01-6).
7. **Gate sécurité FreeLLMAPI LEVÉ (vérification Bill 2026-10-17 ~10:50 EDT, négative)** : `setup-freellmapi.sh`, `import-freellmapi-keys.py`, `README-freellmapi.md` ne contiennent aucune valeur de clé en dur (env vars, génération runtime, placeholders) — `v4-factory/control-plane/` confirmé incluable dans le push, aucune purge requise. Rapport : `~/workspace/sandbox-extraction/gate-securite-freellmapi.md`.

## 1. Bornes

**IN :** copie vérifiée SHA + manifeste par lot + mapping §0.2/§0.3 + staging (branche locale, sans push) + gates arbitrage/validation.
**OUT :** push sans validation Doctors ; création de repo sans arbitrage ; `life-os-audit` (SB-03) ; `user/`, `memory/`, runtime ; blobs > seuils (→ SB-02, Drive).

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Table de mapping** : source → destination (branches A/B), exceptions documentées (`ledger/`, bundle, fusion `skills/`).
**Système 2 — Manifeste SHA par lot** (pattern extraction GPT) : par fichier — chemin relatif, SHA-256, octets, destination. Fichier sans entrée manifeste = non extrait.
**Système 3 — Staging + gates** : branche locale préparée (copie + manifeste) → gate arbitrage 1 → gate validation Doctors → push.

**Flux :** P0 (manifeste + copie en staging) → gates (arbitrage, validation) → push → vérification post-push.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Staging** | Copie vers l'arborescence cible (mapping §0.2) en branche locale ; manifeste SHA par fichier ; grep secrets | H-SB01-1, H-SB01-2, H-SB01-5, H-SB01-6 |
| **P1 — Gate** | Validation Doctors obtenue (cible V4 arbitrée et enregistrée) | H-SB01-3, H-SB01-4 |
| **P2 — Push** | Push vers la cible arbitrée ; vérification post-push (SHAs distants) | Tous verts |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-SB01-1 | Manifeste SHA | chaque fichier du lot a une entrée (chemin, SHA-256, octets, destination) ; re-calcul conforme |
| H-SB01-2 | Sandbox intacte | re-hash des sources après copie : 0 fichier modifié/déplacé |
| H-SB01-3 | Aucun push sans validation | avant validation Doctors : `git ls-remote` sans nouvelle ref du lot |
| H-SB01-4 | Cible verrouillée | arbitrage enregistré 2026-10-17 : `Amdkn/Aspace_OS-V4` ; push uniquement vers cette cible |
| H-SB01-5 | Mapping appliqué | contrôle par échantillon : chaque fichier à sa destination §0.2 ; `ledger-graham.md` uniquement sous `ledger/` (0 doublon) |
| H-SB01-6 | Aucun secret | grep patterns secrets sur le lot = vide ; `freellmapi-keys.json` absent du lot |
| H-SB01-7 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Repo cible non tranché.** → Gate P1 : le push attend l'arbitrage ; la préparation n'attend pas.
- **R2 — `skills/` : périmètre flou.** → Tranché §0.5 : GitHub avec `custom-skills/`, arbre unique.
- **R3 — Divergence avec F-02/L1 sur le ledger.** → Aligné §0.2 : `ledger/` racine, import genesis — le design F-02 fait foi.

*Fin du plan SB-01. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors (push après gates).*
