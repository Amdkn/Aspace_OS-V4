# Schéma de reçu R10 — `aspace.r10-receipt.v1`

**Statut :** version 1, ratifié dans le cadre L01 (D-N027), 2026-10-19.
**Émetteur :** Graham — Mémoire du Kernel (13e Doctor).
**Doctrine :** sans reçu, pas de merge. Un reçu incomplet est refusé et renvoyé.

## Les 5 champs obligatoires

| Champ | Type | Règle |
|---|---|---|
| `mission_id` | string | Identifiant de la mission (ex. `D-N027-L04`, `RYAN-FAB-DN029-001`). Non vide. |
| `sha` | string | SHA complet (40 hex) du commit livré, OU référence de PR (`#87`) quand le head bouge encore. Jamais abrégé seul : un SHA tronqué n'est pas un reçu. |
| `observed_at` | string | ISO-8601 avec fuseau — **quand c'est arrivé** (la livraison). Posé par l'exécutant. |
| `recorded_at` | string | ISO-8601 avec fuseau — **quand c'est consigné**. Posé par Graham seul à la consignation. L'exécutant ne le pose jamais. |
| `proof` | array[string] | Liens de preuve non vides : URL de PR, run CI, artefact, chemin de fichier. Au moins 1 élément. |
| `issuer` | string | Émetteur du reçu (ex. `Graham (Kernel, 13e Doctor)`). Non vide. |

## Champs d'enveloppe (requis par le check, non négociables)

| Champ | Type | Règle |
|---|---|---|
| `schema` | string | Doit valoir exactement `aspace.r10-receipt.v1`. |
| `entry_id` | string | Identifiant d'entrée ledger (ex. `G-20261019-007`). Unique. |

## Champs libres

`summary` (string) — résumé humain d'une ligne. Tout autre champ est ignoré par le check,
jamais rejeté : le schéma est extensible, pas cassant.

## Règles de vérité temporelle

1. `observed_at` ≠ `recorded_at` par construction : l'un dit quand c'est arrivé,
   l'autre quand c'est consigné. Les confondre, c'est corrompre le ledger.
2. Un reçu antidaté (`recorded_at` < `observed_at`) est refusé.
3. Le bloc genesis (`ledger/genesis/`) est **hors schéma** : c'est l'historique pré-L01,
   importé verbatim, vérifié par hash (H-L01-4), jamais réécrit. Le schéma v1 s'applique
   à tout reçu émis à partir de L01.

## Évolution

Toute v2 du schéma : nouveau fichier `SCHEMA-v2.md`, les reçus v1 restent valides
(compatibilité ascendante des lecteurs). On ne réécrit jamais un reçu émis.
