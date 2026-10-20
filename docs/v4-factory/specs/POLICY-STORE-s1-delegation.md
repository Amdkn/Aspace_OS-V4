# Policy Store — Délégation S1 (Aspace OS V4)

- **Version :** v1.0 — 2026-10-09
- **Owner :** S1 · Rick (session de délégation)
- **Source d'autorité :** ce fichier, versionné en git. Toute règle de délégation non écrite ici n'existe pas.
- **Référence normative :** `SPEC-twin-gate-a0.md` v0.2 DRAFT (A0 = Owner E-Myth au-dessus de l'actionnaire ; merges/déploiements = S2/S3)

## P1 — Règle d'or

Le Capitaine n'est pas informaticien. **AUCUNE décision technique d'implémentation ne lui est renvoyée.**

- S1 tranche au niveau **délégation** : quoi, qui, dans quel ordre, quel reçu attendu.
- S2 (Doctors) et S3 (Compagnons) tranchent au niveau **technique d'implémentation**.
- Remonte au Capitaine : **l'arbitrage VISION** (choix de direction, jamais de technique).

### Amendement v1.1 — gate humain supprimé par décision owner (2026-10-09)

Le Capitaine a mergé lui-même la PR #24 le 2026-10-09 à 09:30 EDT (via web UI) : `agents/CONTRACT.md` sur `main` dit désormais « aucun gate humain : le Capitaine ne clique plus, l'autorité est pleine ». En conséquence : **S1 ne remonte plus de gates humains** (il n'y en a plus) ; seule l'arbitrage vision remonte. R10 (pas d'agent « actif » sans reçu) reste en vigueur. Si le Capitaine signale un misclick, S1 prépare la PR de revert.

## P2 — Typage des missions

Toute mission S1→S2 est typée avec quatre champs obligatoires :

| Champ | Exigence |
|---|---|
| `objectif` | Un seul, vérifiable, formulé en résultat observable |
| `périmètre` | Inclus **et** exclus explicites |
| `critères de reçu` | Observables, binaires — un reçu R10 par critère |
| `gate_humain` | Ce qui exige un acte du Capitaine (merge, dépense, publication), ou `aucun` |

Défauts : pas de mission sans critères de reçu. Pas de reçu = pas de statut « actif » (R10).

## P3 — Routage

Capitaine (vision) → A0 (doctrine) → **S1 (typage)** → S2 Doctors (pipelines) → S3 Compagnons (factory).

- S1 ne fait pas d'implémentation : il route.
- Escalade : un différend de périmètre entre S2/S3 est re-typé par S1 ; un différend de vision remonte au Capitaine.
- Frein d'urgence : `OWNER_STAND_DOWN=1` arrête tout (défini dans la spec Twin-Gate v0.2).

## P4 — Rôles S3 (référence v0.2)

- **Bill = Discover** (bruit → missions typées)
- **Clara = Design** (mission → plan borné + tests hold-out écrits avant exécution)
- **Nardole = Dispatch** (assignation, suivi, routage des PR vers les merges S2)

## Changelog

- **v1.1** (2026-10-09, ~11:00 EDT) — amendement owner : gate humain supprimé par merge PR #24 (Capitaine, 09:30 EDT, web UI). S1 ne remonte plus que l'arbitrage vision. R10 inchangé.
- **v1.0** (2026-10-09, ~06:05 EDT) — création initiale par S1. Règles P1–P4. Premier état : file de missions vide, flux S1→S2 vide.
