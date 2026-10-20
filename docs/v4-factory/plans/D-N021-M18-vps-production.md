# D-N021 / M-18 — VPS production de valeur (1 mois)

**Mission :** M-18 (`REGISTRE-INSPIRATIONS.md`) — dispatch D-N021 (Nardole). **Plan :** 12e Doctor.
**Objectif :** un VPS d'1 mois porte de la production de valeur, pas de la plomberie L0.
**Contexte :** perte du VPS d'1 an ; « ne plus perdre 500 % de mon temps sur la plomberie du Kernel L0 ». Doctrine D-03 (biais action).

## Bornes
**IN :** provisioning VPS (1 mois, timebox stricte) ; déploiement via **Coolify** (stack existante du Capitaine — pas de plomberie manuelle) ; candidats : FreeLLMAPI (routeur stable), Cube Farm (monde 3D) ; runbook ; monitoring visible.
**OUT :** toute plomberie L0 (infra manuelle, serveurs snowflakes) ; exposer des secrets ; tout engagement >1 mois sans arbitrage.

## Décisions 12e (techniques, tranchées)
- **Panel :** Coolify (déjà dans le stack ; deploy git/compose, zéro plomberie).
- **Dimensionnement :** ~2–4 vCPU / 8 Go RAM (miroir du Codespace 2-core/8GB) ; région au choix de l'exécutant.
- **Budget :** cap ~25 $/mois (ordre de grandeur) — l'exécutant confirme le SKU exact au provisioning.
- **Ordre de déploiement :** 1) **FreeLLMAPI** — routeur stable, la factory n'est plus otage du Codespace (meurt après 30 min d'inactivité) ; 2) **Cube Farm** — le monde 3D servi en continu.
- **Sécurité :** FreeLLMAPI derrière auth (clé unifiée), jamais d'exposition anonyme ; secrets via Coolify env, jamais dans git.

## Phases (séquentielles)
| Phase | Action | Gate |
|---|---|---|
| **P0 — Provisioning** | VPS + Coolify installé + accès | dashboard Coolify joignable (H-M18-1) |
| **P1 — FreeLLMAPI** | Routeur déployé, clé unifiée, healthcheck | H-M18-2 (router) |
| **P2 — Cube Farm** | Monde 3D déployé et servi | H-M18-2 (cube farm) |
| **P3 — Ops** | Monitoring + runbook + vérification anti-plomberie | H-M18-3/4/5/6 |

## Tests hold-out (définis avant exécution)
| ID | Vérifie | Seuil |
|---|---|---|
| **H-M18-1** | Infra UP | VPS joignable, dashboard Coolify UP |
| **H-M18-2** | Trafic réel | chaque app déployée répond **200** sur son URL publique |
| **H-M18-3** | Monitoring visible | healthchecks Coolify verts + page/uptime consultable |
| **H-M18-4** | Runbook | présent : provision → deploy → redeploy → rollback → destroy (fin de timebox) |
| **H-M18-5** | Anti-plomberie | redeploy from scratch via Coolify <30 min, zéro SSH manuel hors bootstrap initial |
| **H-M18-6** | Secrets | aucun secret dans git (grep) ; secrets uniquement via Coolify env |
| **H-M18-7** | Fin de timebox | à 1 mois : décision reconduire / arrêter / migrer — **pas d'engagement tacite** |

**Reçu (mission) :** le VPS sert du trafic réel avec monitoring visible.
**Notes :** provider/SKU exact = exécutant (Nardole/S3) au provisioning, dans le cap. La dépense est pré-autorisée par la mission (VPS 1 mois) — le compte hosting est une **capacité-compte**, pas un gate (factory tente via browser si session disponible).
