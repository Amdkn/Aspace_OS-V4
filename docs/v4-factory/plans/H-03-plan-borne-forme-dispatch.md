# H-03 — Plan borné : Forme du Dispatch de Nardole (le Capitaine doit VOIR)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) ; Discover Bill (`~/workspace/architecture-compagnons/qualif-router-dispatch.md` — le vieux router `dispatch_routing.py`, 712 lignes, jamais porté en V4)
**Fait structurant :** hier, le dispatch était **une machine qui décidait** (radar : présence, capacité, santé, `quota_ok`) ; aujourd'hui, **une personne qui décide** (registre tenu à la main, jugement). 4 pertes : déterministe→jugement, retour durable→chat, **backpressure→rien**, claims→doctrine. **Le chaînon manquant de la root cause** : le router modélisait l'épuisement des quotas en backpressure explicite — le mécanisme qui aurait fait remonter la panne du ledger au lieu de 8 jours de silence.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Ni moteur qui remplace Nardole, ni statu quo.** Le registre est un **organe** (mission → Compagnon, chaîne lore, place publique lisible) — le router était une **machine** (capacité → runtime). Deux niveaux différents. **Décision : les propriétés de sûreté sont codées SOUS le registre ; Nardole garde la décision.** Concrètement : (a) backpressure première classe ; (b) claims/baux ; (c) routes de retour durables ; (d) `select_runtime` en **conseiller visible** — sa proposition (exécutants sûrs classés + motifs) est attachée à chaque dispatch ; Nardole tranche (jugement + lore) ; tout override est enregistré avec motif (responsabilité, pas blocage).
2. **Backpressure première classe (réponse directe à la root cause).** Chaque exécutant a un état `quota_ok` (sondé, Tier F/déterministe) ; `false` → décision **`BACKPRESSURE`** — explicite, durable, visible. Jamais d'échec silencieux, jamais de retry aveugle. C'est le `quota_backpressure` du vieux router + l'addendum A1 (L00) de F-02 (résilience quotas = L0) qui se rejoignent dans le dispatch.
3. **Le Capitaine VOIT (livrables accessibles, pas juste du code).**
   - **`docs/DISPATCH.md`** — narratif : ce qu'est le dispatch (contrôleur aérien : radar + bandes de vol), les 3 commandes en langage plain (choisir l'exécutant sûr / réserver la mission / garantir le retour).
   - **Le tableau de bord** — missions en vol × claims (détenteur, bail) × feux de backpressure × routes de retour, généré depuis le registre + le WorkGraph (`tools/dispatch-board`). Le Capitaine voit : ce qui vole, qui tient quoi, ce qui est bloqué, ce qui est en retard.
   - **Par dispatch** : la proposition de la machine visible à côté de la décision de Nardole.
4. **WorkGraph tranché : Supabase (L0).** Tables `dispatch_work`, `dispatch_event`, `dispatch_claim` — miroir du schéma de l'ancien `uc.db` (work/event/claim). Le `uc.db` du PC du Capitaine devient **archive**, pas autorité. Rationnel : L0 acte déjà Supabase ; l'état machine exige requêtes + écritures runtime ; le repo porte le registre humain (markdown), Supabase l'état machine — exactement l'ancien split (`uc.db` + rapport kanban).
5. **Boucles du dispatch sur Tier F** : sondage backpressure, réconciliation des retours — Tier F/déterministe par addendum A1 (L00) F-02 (référencé, pas dupliqué).
6. **La chaîne lore a un ancêtre machine** : `VERDICT_ROUTES` routait déjà `REOPEN_BUILD`→RYAN, `REOPEN_DESIGN`→CLARA — le design s'en réclame, sans rupture. Le reçu avant complétion (`COMPLETE` exige reçu `SUCCEEDED` postérieur au dispatch) = ancêtre direct de la doctrine R10.

## 1. Bornes

**IN :** propriétés de sûreté codées (backpressure, claims, retours durables) + conseiller `select_runtime` visible + représentation accessible (narratif + tableau de bord) + WorkGraph Supabase + boucles Tier F.
**OUT :** remplacer le jugement de Nardole par un moteur ; casser la place publique (le registre marche) ; inventer un dispatch sans ancrage dans le router.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Sûreté** : `quota_ok` par exécutant → BACKPRESSURE ; claim/bail 900 s par `work_id` (un seul writer) ; `return_route` explicite + événement `continuation_routed` idempotent (aucune mission perdue sans détection mécanique).
**Système 2 — Conseiller** : `select_runtime` (présence, capacité, santé, quota → classement déterministe) attaché visiblement à chaque dispatch ; overrides motivés.
**Système 3 — Représentation** : `docs/DISPATCH.md` + tableau de bord généré (`tools/dispatch-board`) depuis registre + WorkGraph.
**Système 4 — WorkGraph** : Supabase `dispatch_work/event/claim` ; `uc.db` PC = archive.

**Flux :** P0 (sûreté) → P1 (conseiller) → P2 (représentation) → P3 (WorkGraph) → validation Doctors.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Sûreté codée** | Backpressure, claims/baux, retours durables (schémas d'événements) | H-H03-2, H-H03-3, H-H03-4 |
| **P1 — Conseiller** | `select_runtime` visible par dispatch ; overrides motivés | H-H03-5 |
| **P2 — Représentation** | `docs/DISPATCH.md` + tableau de bord généré | H-H03-1 |
| **P3 — WorkGraph** | Tables Supabase + `uc.db` archivé (plus autorité) | H-H03-6 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-H03-1 | Le Capitaine voit | `docs/DISPATCH.md` + tableau de bord existants, à jour, régénérables depuis registre + WorkGraph |
| H-H03-2 | Backpressure première classe | épuisement seedé → décision BACKPRESSURE durable et visible (pas de silence, pas de retry aveugle) |
| H-H03-3 | Claims | double dispatch sur un même `work_id` → échec fermé (un seul writer) |
| H-H03-4 | Retour durable | mission sans retour après expiration du bail → anomalie détectée mécaniquement |
| H-H03-5 | Conseiller visible | chaque dispatch montre la proposition machine + la décision Nardole (+ motif si override) |
| H-H03-6 | WorkGraph tranché | tables Supabase existantes selon le schéma ; `uc.db` PC documenté comme archive |
| H-H03-7 | R10 | reçu au ledger |

## 5. Risques

- **R1 — `uc.db` sur PC Capitaine.** → Tranché §0.4 : Supabase = autorité, PC = archive (plus besoin d'exposition pour l'autorité).
- **R2 — Scope moteur vs propriétés.** → Tranché §0.1 : propriétés codées + conseiller visible, décision à Nardole (ni moteur complet ni rien).
- **R3 — Casser la place publique.** → §0.1 : le registre reste l'organe lisible ; la machine est dessous, pas à la place.

*Fin du plan H-03. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors.*

---

## ADDENDUM H-03-A1 — Rescue explicite : recovery vs rescue (Dette 3, Cole Medin)

**Date :** 2026-10-19 — **Signé Clara** (addendum au plan H-03 signé ; le corps est intact).
**Source :** ingestion Cole Medin de Bill (`~/workspace/architecture-compagnons/ingestion-cole-medin-software-factory.md`, §4 dette D3). Le manager de Cole *secourt* (réachemine) **et** alerte l'humain ; Nardole aujourd'hui ne fait que de la reprise de claims au crash. Sans le sauvetage : D-N015 encalminée 8 jours, à nouveau.

**Décisions design (autorité Clara) :**

**H-03-A1-1 — Recovery ≠ rescue.**
- **Recovery** (technique, automatique — Nardole, machine) : crash / expiration de bail → libération du claim, BACKPRESSURE, retry, réacheminement vers un autre exécutant **dans la même mission** (liste classée du conseiller). Journalisé, **sans décision, sans alerte**. C'est le Système 1 de H-03.
- **Rescue** (décision, nommée) : déclenchée quand la recovery est épuisée ou inapplicable —
  - **R1** : 3 recoveries en échec sur le même `work_id`, ou
  - **R2** : **cale sans crash** — mission en vol au-delà de 2× son bail, sans crash ni progression (le cas D-N015 : 8 jours ASSIGNÉE, aucun mouvement, aucun crash — la recovery ne se déclenche jamais car rien n'a crashé ; **c'est le silence qui est la panne**).

**H-03-A1-2 — Qui décide du réacheminement : Nardole.** Réacheminer = réassigner à une autre lane/exécutant, re-scoper, ou parquer — **avec motif enregistré au registre public** (place publique). **Validation du Doctor S2** de la lane quand le réacheminement change la nature de la mission ou traverse les lanes. L'autorité remplace le gate : la décision est nommée et tracée, pas bloquée.

**H-03-A1-3 — Quand l'humain est alerté (réconciliation avec la doctrine no-human-gate).** Deux niveaux :
- Le **Doctor S2** — l'autorité humaine dans la boucle (autorité pleine : valide et exécute) — est **alerté à chaque déclenchement de rescue**. C'est « l'humain » de la station de Cole.
- Le **Capitaine** est alerté uniquement si (a) le blocage touche **l'une de ses 6 portes explicites** (35 clés, écriture Drive, pushes d'extraction, médias F-01, miroir Linear M4, OAuth GWS), ou (b) l'escalade S2 → S1 est épuisée → code d'exception via Rick. **Jamais « en attente Capitaine »** pour un rescue de routine — ni spam d'alertes, ni goulot.
- Sous ce design, le cas D-N015 : cale à 2× bail → rescue → Nardole réachemine ou escalade → **jamais 8 jours de silence**. Le silence au-delà du bail est une anomalie visible par construction (cohérent avec l'invariant de vivacité F-02/L00).

**Tests hold-out ajoutés :** H-H03-A1-1 (cale seedée — sans crash, sans progression, 2× bail → rescue déclenché : réacheminement décidé par Nardole avec motif enregistré, Doctor S2 alerté) ; H-H03-A1-2 (recovery vs rescue distingués au registre : un crash montre le chemin recovery — automatique, journalisé, sans alerte ; une cale montre le chemin rescue — décision + alerte) ; H-H03-A1-3 (discipline d'alerte Capitaine : rescue de routine hors ses portes et sans escalade épuisée → **aucune** alerte Capitaine ; rescue sur l'une de ses 6 portes → alerte).

*Fin de l'addendum H-03-A1. Signature Clara apposée — PRÊT, dispatchable par Nardole avec H-03 après validation Doctors.*
