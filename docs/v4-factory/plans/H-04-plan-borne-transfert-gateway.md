# H-04 — Plan borné : Transfert Gateway/MCP/CLI/API → Life OS + Agent OS Desktop

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) ; Discover Bill (`~/workspace/architecture-compagnons/qualif-gateway-mcp-cli-api.md` — Business OS = vrai runtime d'agnosticité de harnais : bridge 484 lignes, **24/24 adaptateurs, 0 stub, autotest 20/20**, API serverless authentifiée, AGP deny-by-default, MCP stdio réel, CLI réelle)
**Principe : extraire, pas partir de zéro.** Pas de serveur gateway standalone (le trou D-N015 tient sur ce point précis) — mais les briques existent et sont testées.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **D-N015 révisé : extraire et composer.** F-02/L03 concevait `gateway/` à partir de zéro (état constaté : aucun code serveur). Le Discover montre les briques : `api/_agent/garde.ts` (bearer **fail-closed**, né d'un pentest réel) + `agp.ts` (deny-by-default : « une passerelle qui laisse passer ce qui n'est pas nommé n'est pas une passerelle ») + `adapt.ts` (forme Web standard, runtime-agnostique). **Décision : le serveur `gateway/` est composé par extraction de ces briques** — méthode de construction révisée (extraire-composer), philosophie Zero Trust inchangée. Aucune réimplémentation là où la brique existe et est testée.
2. **Registre canonique : généraliser, pas copier.** Le bridge projette le registre d'outils Coach OS — le transfert **généralise le registre** (vocabulaire des 11 capacités canoniques conservé : tool_call, file_edit, shell, browser, subagents, streaming, vision, voice, cron, webhook, long_context) au-delà de Coach OS. Le pattern `harnesses.json` (1 entrée JSON par harnais, **sans recompilation**) devient le registre canonique de harnais. Copie brute interdite.
3. **W03 fermé avant toute exposition à un tiers.** Limite honnête : rien n'authentifie `__tenantId/__actorId/__role` (machine de confiance uniquement). **Fermeture : tokens tenant signés HMAC** (secret partagé par tenant, vérifié par l'adaptateur, **fail-closed**). Jusqu'à fermeture : machine de confiance uniquement — **appliqué par le déploiement**, pas seulement documenté.
4. **Veto a2p respecté et voyageur.** Le veto écrit (« intention de paiement routable et traçable, **JAMAIS exécutable par un agent** ») est enregistré comme politique permanente au policy store (F-02/L05) ; chaque transfert de surface inclut le check « veto a2p vérifié ».
5. **`buzz` = ancrage naturel.** Harnais déjà mesuré (cli, subagents, voice) — le cœur Buzz du 12e : le dispatch des 9 Compagnons s'ancre sur `buzz` en premier.
6. **Convergence P-01.** Le pattern du bridge (« un travail déclare ce dont il A BESOIN, jamais QUI doit l'exécuter ») = le pattern `HookProvider` de Pixel Agents. **Unification au design** : le vocabulaire des 11 capacités devient le langage partagé ; les deux patterns convergent (pas de fusion forcée des lanes, alignement du langage).
7. **Surfaces transférables telles quelles** (haute transférabilité) : serveur MCP stdio (JSON-RPC 2.0), CLI `coach-os` (binaire npm), routes API (forme Web standard). Sondage local : les statuts `mesuré` valent pour le poste sondé (c'est le design — mesure > déclaration, anti-gaming conservé).

## 1. Bornes

**IN :** extraction-composition du serveur gateway (D-N015) + registre canonique généralisé + fermeture W03 (HMAC) + veto a2p au policy store + ancrage `buzz` + convergence P-01 + transfert MCP/CLI/API.
**OUT :** partir de zéro là où les briques existent ; exposer à un tiers sans fermer W03 ; copie brute du registre Coach OS.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Gateway extraite** : `gateway/` = `garde.ts` (auth) + `agp.ts` (deny-by-default) + `adapt.ts` (shape) composés en serveur standalone (D-N015, méthode révisée).
**Système 2 — Registre canonique** : vocabulaire 11 capacités + pattern `harnesses.json` (1 entrée/harnais, sans recompilation), périmètre généralisé.
**Système 3 — W03** : tokens tenant HMAC, fail-closed ; machine de confiance jusqu'à fermeture (déploiement).
**Système 4 — Transfert** : MCP stdio + CLI + routes API vers Life OS et Agent OS Desktop ; veto a2p en checklist ; ancrage `buzz`.

**Flux :** P0 (gateway extraite) → P1 (registre canonique) → P2 (W03) → P3 (transfert surfaces) → validation Doctors.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Gateway** | Extraction-composition du serveur depuis `garde.ts`/`agp.ts`/`adapt.ts` | H-H04-1 |
| **P1 — Registre** | Généralisation du registre (11 capacités, pattern harnesses.json) | H-H04-2 |
| **P2 — W03** | Tokens tenant HMAC, fail-closed ; exposition tiers interdite avant | H-H04-3 |
| **P3 — Transfert** | MCP/CLI/API sur Life OS + Agent OS Desktop ; veto a2p vérifié ; ancrage `buzz` | H-H04-4, H-H04-5 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-H04-1 | Pas de from-scratch | l'auth, l'AGP et la shape du serveur tracent vers les briques extraites (0 réimplémentation) |
| H-H04-2 | Registre canonique | périmètre généralisé au-delà de Coach OS (pas de copie brute) ; vocabulaire 11 capacités intact |
| H-H04-3 | W03 fermé | identité tenant authentifiée (HMAC) avant toute exposition à un tiers ; sans fermeture : machine de confiance uniquement (vérifié au déploiement) |
| H-H04-4 | Veto a2p | politique enregistrée au policy store ; checklist de transfert la vérifie |
| H-H04-5 | Surfaces fonctionnelles | MCP/CLI/API transférés et fonctionnels sur Life OS et Agent OS Desktop |
| H-H04-6 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Pas de serveur standalone.** → Trou réel, comblé par extraction-composition (§0.1), pas par construction ex nihilo.
- **R2 — W03.** → Fermeture HMAC avant exposition (§0.3) ; jamais d'exposition sur machine non digne de confiance.
- **R3 — Sondage local.** → Les statuts `mesuré` sont relatifs au poste (design, pas bug).
- **R4 — Convergence P-01.** → Alignement du langage (§0.6), pas de fusion forcée des lanes.

*Fin du plan H-04. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors.*
