# H-05 — Plan borné : Designs de Clara accessibles (synchro extraction sandbox → V4)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) « Mission 1 : Architecture des 9 Compagnons » ; lien SB-01 (lot GitHub)
**Fait :** 18+ plans signés en `~/workspace/v4-factory/plans/`, **0 en repo** — le tout-sandbox quantifié (H-02 §4). Le chaînon manquant n'est pas la production, c'est l'atterrissage.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Convention d'emplacement** : les designs signés vivent dans `docs/` selon le mapping SB-01 (`docs/fondations-aspace/`, `docs/frameworks/`, `docs/v4-factory/plans/`, …) + **index `docs/REGISTRE-DESIGNS.md`** (id, titre, date de signature, chemin, statut de validation, date de validation). Un design sans entrée d'index = non compté.
2. **Convention de nommage** : `<MISSION>-plan-borne-<slug>.md` (convention existante conservée — déjà cohérente sur les 18 plans).
3. **Règle des 24 h** : signature → **PR ouverte sous 24 h** (le design entre dans le protocole H-02) ; merge après validation Doctors. Les 24 h portent sur **l'entrée dans le flux**, pas sur le merge — la validation garde son temps.
4. **Invariant opposable** : **aucun design signé n'existe qu'en sandbox** — vérifiable mécaniquement (index vs repo). Un signé sandbox-only = anomalie de protocole (cf. H-H05-3).
5. **Lien SB-01** : le stock existant (18+ plans) part avec le lot GitHub SB-01 ; la règle des 24 h couvre tous les futurs signés.
6. **Dépendance d'exécution** : la règle des 24 h s'exécute **via le protocole H-02** (CONTRIBUTING.md) — H-02 conçu, H-05 l'utilise. Pas de duplication normative.
7. **Non signé = non publié** : seuls les designs signés entrent dans le flux (les brouillons restent en sandbox, marqués comme tels).

## 1. Bornes

**IN :** convention (emplacement + nommage + index) + règle des 24 h + invariant + lien SB-01.
**OUT :** publier des designs non signés ; dupliquer le protocole H-02.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Convention** : mapping SB-01 + `docs/REGISTRE-DESIGNS.md` + nommage `<MISSION>-plan-borne-<slug>.md`.
**Système 2 — Règle des 24 h** : signature → PR sous 24 h (protocole H-02) → merge après validation.
**Système 3 — Invariant** : index vs repo — aucun signé sandbox-only.

**Flux :** P0 (convention + index) → P1 (stock SB-01) → P2 (règle des 24 h en régime) → validation Doctors.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Convention** | Mapping + `docs/REGISTRE-DESIGNS.md` + nommage documentés | H-H05-1 |
| **P1 — Stock** | Les 18+ plans existants dans le lot SB-01 (index rempli) | H-H05-3 |
| **P2 — Régime** | Règle des 24 h appliquée aux nouveaux signés (via H-02) | H-H05-2 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-H05-1 | Convention suivie | chaque design signé est sous `docs/` selon le mapping + entrée d'index (id, titre, date, chemin, validation) |
| H-H05-2 | Règle des 24 h | tout design signé depuis > 24 h a une PR ouverte (ou un motif enregistré) |
| H-H05-3 | Aucun signé sandbox-only | comparaison index vs repo : 0 design signé absent du repo (hors PR en cours < 24 h) |
| H-H05-4 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Stock initial volumineux (18+ plans).** → P1 : le lot SB-01 l'emporte en une fois, index rempli.
- **R2 — 24 h vs validation.** → §0.3 : les 24 h = entrée dans le flux, pas merge — pas de conflit avec la validation.
- **R3 — Dérive future.** → Invariant §0.4, vérifiable mécaniquement.

*Fin du plan H-05. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors.*
