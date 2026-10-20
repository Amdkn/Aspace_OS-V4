# D-N021 / M-07 — Supervision Jules end-to-end

**Mission :** M-07 (`REGISTRE-INSPIRATIONS.md`) — dispatch D-N021 (Nardole). **Plan :** 12e Doctor.
**Objectif :** aucune session Jules ne meurt en draft ; toute mission exige « PR Ready for review + Fixes #N ».
**Contexte :** parallélisme assumé (100 sessions daily, 15 simultanées) ; circuit `factory:ready` vérifié (#30 → Jules) ; leçon : sessions bloquées à la publication de la PR après travail terminé ; exemple #37 (session en attente d'input).

## Bornes
**IN :** inventaire des sessions/PRs/issues Jules ouvertes ; protocole de reprise (bloqué >24h → reprise avec input, ou clôture motivée) ; gate « Ready for review + Fixes #N » inscrit dans le cycle de dispatch (schéma registre Nardole) ; boucle de supervision périodique (qui/quand/quoi).
**OUT :** le contenu des PR elles-mêmes (revue = Doctors) ; la mécanique interne de Jules.

## Phases (séquentielles)
| Phase | Action | Gate |
|---|---|---|
| **P0 — Inventaire** | Lister : sessions Jules ouvertes, PRs en draft, issues liées (dont #37). Livrable : tableau d'état | Inventaire complet et daté |
| **P1 — Reprise** | Pour chaque item bloqué >24h : reprise (input fourni) ou clôture motivée | H-M07-4 |
| **P2 — Gate installé** | Le cycle de dispatch exige « PR Ready for review + Fixes #N » avant TERMINÉ (mise à jour du schéma registre par Nardole) ; boucle de supervision quotidienne (S3/Nardole) : inventaire → détection >24h → action | H-M07-3 |
| **P3 — Vérification** | Audit hold-out | H-M07-1/2 |

## Tests hold-out (définis avant exécution)
| ID | Vérifie | Seuil |
|---|---|---|
| **H-M07-1** | Aucune session abandonnée | audit : toute PR d'origine Jules ouverte depuis >24h est soit « Ready for review » avec `Fixes #N`, soit a une entrée reprise/clôture au registre |
| **H-M07-2** | Aucun draft orphelin | zéro issue avec PR Jules en draft >24h sans entrée dispatch |
| **H-M07-3** | Gate gravé | « Ready for review + Fixes #N » figure dans le cycle de dispatch comme condition de TERMINÉ (registre) |
| **H-M07-4** | Backlog vidé | backlog P0 vide — dont #37 : reprise ou clôturée motivée |

**Reçu (mission) :** zéro session bloquée >24h sans reprise ; toute PR Jules sort du draft avec `Fixes #N`.
**Note :** la supervision est un processus permanent — le reçu porte sur l'installation du processus + backlog initial vidé. La détection peut être portée par le heartbeat unique (ne remonte que le rouge).
**Exécutants pressentis :** P0/P1 : S3 (inventaire + reprise) ; P2 : Nardole (schéma registre). Aucun swarm — si parallélisation nécessaire : signature Clara d'abord (D-10).
