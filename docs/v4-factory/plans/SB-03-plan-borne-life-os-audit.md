# SB-03 — Plan borné : Lot 3 — life-os-audit → GitHub après validation Doctors

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) ; inventaire Bill (`~/workspace/sandbox-extraction/inventaire-sandbox.md`)
**Fait :** `life-os-audit/` = 344 Mo dont **338 Mo de `node_modules`** (exclu — régénérable) ; seuls **~6 Mo nets** ont de la valeur : **4 commits locaux non poussés** (04318b2, 7a116ac, 2df8032, 4fbb5e6 — réduction Ponytail Phase 1, vérifié absents du remote via `git ls-remote`) + `VALIDATION-PHASE1-D13.md` (modifié, non indexé).
**Contrainte inviolable :** **push APRÈS validation Doctors, jamais avant.** Cible confirmée après le chantier d'analyse Life OS en cours — jamais décidée seule.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Séquencement strict** : (a) **relecture** de `VALIDATION-PHASE1-D13.md` (modifié non indexé — relire le diff avant tout) ; (b) **validation Doctors** des 4 commits + du fichier ; (c) **push** vers la cible arbitrée. Aucune étape ne saute la précédente.
2. **Cible — gate marqué (arbitrage Capitaine 2026-10-17)** : la cible des 4 commits sera confirmée **après** le nouveau chantier d'analyse Life OS en cours. Le design marque ce gate : **aucun push avant confirmation enregistrée**. Défaut proposé : `Amdkn/Life-OS-2026` (le repo d'origine du clone) — proposition, pas décision.
3. **`node_modules` exclu** : vérifier qu'il n'est pas suivi (`git ls-files` — s'il est tracké, le retirer de l'index avant push, sans le supprimer du disque) ; le push ne contient que le travail (~6 Mo nets).
4. **Vérification post-push** : SHAs locaux vs distants identiques (les 4 commits + le fichier) ; `git ls-remote` confirme la présence.
5. **Pas de rebase sauvage** : les 4 commits partent tels quels (historique local préservé) sauf consigne contraire des Doctors à la validation.

## 1. Bornes

**IN :** relecture du fichier modifié + validation Doctors + push vers cible arbitrée + vérification post-push ; `node_modules` exclu.
**OUT :** push sans validation (interdit absolu) ; décision seule de la cible ; inclusion de `node_modules`.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Revue** : diff de `VALIDATION-PHASE1-D13.md` relu + 4 commits inspectés → dossier de validation Doctors.
**Système 2 — Push gaté** : validation datée → arbitrage 4 enregistré → push → vérification SHA distant.

**Flux :** P0 (relecture) → P1 (validation Doctors + arbitrage 4) → P2 (push + vérification).

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Relecture** | Diff de `VALIDATION-PHASE1-D13.md` relu et résumé ; 4 commits inspectés (`git show` — contenu conforme à la réduction Ponytail Phase 1) ; vérifier `node_modules` non suivi | H-SB03-3 |
| **P1 — Gates** | Validation Doctors obtenue et datée ; cible confirmée après le chantier d'analyse Life OS (gate marqué — aucun push avant) | H-SB03-1, H-SB03-2 |
| **P2 — Push** | Push des 4 commits + fichier ; vérification SHAs distants | H-SB03-4 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-SB03-1 | Validation avant push | validation Doctors datée **avant** tout push (`git ls-remote` sans les commits avant la date) |
| H-SB03-2 | Cible confirmée | confirmation enregistrée **après** le chantier d'analyse Life OS ; push exactement vers la cible confirmée |
| H-SB03-3 | `node_modules` exclu | le ref poussé ne contient pas `node_modules` (vérification de l'arbre distant) |
| H-SB03-4 | Push vérifié | les 4 SHAs + le fichier présents sur le remote, identiques au local |
| H-SB03-5 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Cible non confirmée.** → Gate P1 : aucun push avant confirmation post-chantier d'analyse Life OS.
- **R2 — `VALIDATION-PHASE1-D13.md` : contenu du diff.** → P0 : relecture obligatoire ; si le diff contredit la Phase 1 → retour aux Doctors avant push.
- **R3 — `node_modules` suivi par accident.** → P0 : `git ls-files` ; retrait de l'index si besoin (disque intact).

*Fin du plan SB-03. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors.*
