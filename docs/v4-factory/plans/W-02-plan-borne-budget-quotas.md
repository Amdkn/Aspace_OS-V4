# W-02 — Plan borné : Budget quotas & garde-fou tokens

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-19
**Source :** mission Rick (S1) W-01/02/03 ; Discover Bill (`~/workspace/architecture-compagnons/discover-ingestion-youtube-autonome.md`, §4) — V1 consomme ~258 tok/s sur free-tier (503 intermittents déjà observés = rate-limit, pas panne)
**Principe :** sans budget, V1 = babysitting de quotas. Le garde-fou tourne en **code déterministe, zéro quota pour décider si on peut dépenser du quota** (doctrine L00).
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant. **Précondition des runs non supervisés de W-01.**

---

## 0. Décisions design (autorité Clara)

1. **Modèle de budget : plafond par vidéo + plafond journalier.** Défaut : ~400 k tokens par vidéo V1 (une vidéo de 19 min ≈ 300 k tok — ordre de grandeur) ; plafond journalier paramétrable. **Vérification déterministe AVANT l'appel V1** (jamais un appel modèle pour décider du budget).
2. **Rate-limit ≠ quota épuisé — deux états, deux comportements.**
   - **503 / rate-limit** → retry avec backoff borné (l'appel n'est pas perdu, le quota n'est pas épuisé).
   - **Quota épuisé** → dégradation vers V2/V3 avec label `dégradé — budget`, **sans brûler en silence**.
   - Confondre les deux = soit brûler du quota en retries infinis, soit dégrader alors qu'un retry suffisait.
3. **Budget épuisé = état explicite** (écho H-03 backpressure + doctrine L00) : la cascade dégrade, le rapport dit pourquoi — jamais d'échec silencieux, jamais de dépense invisible.
4. **Journal de tokens par vidéo** : consultable (vidéo → voie → tokens → timestamp). Comptabilité = ce que l'API expose, **jamais de chiffre inventé** (même honnêteté que P-01).
5. **Lien L00** : le garde-fou lui-même est pur code (Tier D) — il ne meurt pas de la panne qu'il surveille.
6. **Précondition W-01** : aucun run non supervisé de la cascade sans le garde-fou actif et câblé.

## 1. Bornes

**IN :** plafonds par vidéo/journalier + check déterministe pré-appel + distinction rate-limit/quota + journal tokens + état explicite.
**OUT :** contourner un quota (retry infini) ; décider du budget par appel modèle ; comptabilité inventée.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Plafonds** : par vidéo + journalier, check déterministe pré-appel.
**Système 2 — Distinction** : rate-limit (backoff borné) vs quota épuisé (dégradation étiquetée).
**Système 3 — Comptabilité** : journal par vidéo, consultable.

**Flux :** P0 (plafonds + check) → P1 (distinction + journal) → validation Doctors → **câblé à W-01 avant runs non supervisés**.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Plafonds** | Plafonds + check déterministe pré-appel V1 | H-W02-1 |
| **P1 — États** | Distinction rate-limit/quota + journal tokens | H-W02-2, H-W02-3, H-W02-4 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-W02-1 | Plafond opposable | budget à 0 (seedé) → **appel V1 bloqué**, cascade dégrade vers V2/V3 |
| H-W02-2 | Distinction d'états | 503 seedé → retry backoff borné (pas de dégradation) ; quota épuisé seedé → dégradation (pas de retry infini) |
| H-W02-3 | Comptabilité | journal consultable : vidéo → voie → tokens → timestamp ; 0 chiffre inventé |
| H-W02-4 | État explicite | rapport dégradé porte `dégradé — budget` ; jamais silencieux |
| H-W02-5 | R10 | reçu au ledger |

## 5. Risques

- **R1 — 503 free-tier fréquents.** → Backoff borné ; le retry n'est pas une dépense aveugle.
- **R2 — Plafonds mal calibrés.** → Paramétrables ; le défaut est un ordre de grandeur documenté, pas une vérité.
- **R3 — W-01 sans W-02.** → §0.6 : précondition — pas de run non supervisé sans garde-fou.

*Fin du plan W-02. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors.*
