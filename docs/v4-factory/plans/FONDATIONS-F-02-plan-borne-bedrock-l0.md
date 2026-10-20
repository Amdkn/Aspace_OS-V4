# F-02 — Plan borné : Chantier 2 — Autonomisation du BedRock L0

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne lore : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** dispatch Rick (S1) « Finalisation des Fondations Aspace » ; découverte Bill L01–L06 (`chantier-2-qualification-bedrock-l0.md`, repo `main` @ `b834356`, lecture seule stricte) ; cadre `BEFORE-YOU-BUILD.md`
**Arbitrages Rick intégrés (tranchés) :**
- **A2 — enforce_admins : RESTE À FALSE (arbitrage Capitaine 2026-10-17 ~04:35 EDT).** Bypass owner conservé — doctrine **capacité MAXIMALE** dans orchestration déterministe (inverse du moindre privilège) ; le contrôle = l'organigramme + les reçus, pas le verrouillage. Le design L04 **ne verrouille pas** : il prouve l'intégrité par les reçus (un merge sans reçu = bloqué par le check R10, pas par GitHub). La branche « verrouiller enforce_admins » est **supprimée**.
- **A3 — D-N015 : fausse alerte, pas de doublon.** Le dispatch existe au registre (créé 2026-10-09, ASSIGNÉ, design Clara, cible 12e) — 8 jours sans design livré. **Le présent design L03 EST le design D-N015 attendu** : il le clôt, Nardole le dispatche tel quel. Héritage design : mon plan D-N015 du 2026-10-09 (`~/workspace/v4-factory/plans/D-N015-plan-borne-gateway-v4.md`) comme input philosophique (Zero Trust), pas comme réutilisation aveugle — l'état actuel a zéro code serveur.
- **A4 — Secrets Supabase : design d'abord.** Inventaire existant (design, pas d'extraction) : `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY` (env, jamais en repo), client fail-fast `os/life/src/lib/supabase.ts` (erreur si absents sauf `VITE_LIFE_LOCAL_ONLY=true` + bannière), `.env.example` = placeholders, business `supabaseConfigured=false` → seed. La sonde P0 inventorie (Vault métadonnées → secrets Codespace → projet documenté) ; si absent → **escalade via A0** (capacité/vision), jamais d'exigence directe au Capitaine.
**Séquencement : le Chantier 2 ne dépend pas du salvage — exécution dès design validé.**
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant à la fois, ordre L06 → L04 → L02 → L01 → L05 → L03.

---

## 0. Décisions design transverses (autorité Clara)

0. **Nomenclature (correction Capitaine 2026-10-19).** L0 = la couche BedRock (Tech OS) — **à ne pas confondre avec L1 (Life OS), L2 (Business OS), L2+ (LD101-08, univers des domaines)**. Les composants de F-02 sont numérotés **L01–L06** : L01 ledger R10 vivant, L02 sonde Supabase, L03 gateway (= D-N015), L04 CI (intégrité par les reçus), L05 policy store, L06 réactivation des 9 Compagnons. L'addendum A1 (résilience aux quotas) est nommé **L00**, socle transversal sous les L01–L06.

1. **Ordre d'exécution : L06 → L04 → L02 → L01 → L05 → L03.** Réactiver les acteurs d'abord (L06), prouver l'intégrité des gates (L04), prouver la connexion (L02), puis construire le vivant dessus : ledger (L01, dont l'enforcement rejoint les checks L04), policy store (L05, qui codifie entre autres L01/L04), gateway (L03, le plus gros build, dispatch D-N015 existant).
2. **Chaque fondation a une preuve qui casse si c'est faux** (contrainte inviolable) : test, reçu, ou check CI qui échoue visiblement sur violation seedée. Aucune fondation déclarée « finalisée » sans elle.
3. **Ne pas refaire ce qui existe** : DDL Supabase (L02), protection CI (L04) — on prouve et on verrouille, on ne reconstruit pas.
4. **Pas d'écriture Linear sans instruction explicite du Capitaine** (contrainte inviolable).
5. **Rapports en français + note vocale MP3 FR par livraison** (contrainte inviolable).

---

## L01 — Ledger R10 : réactiver comme mécanisme vivant 🔴

**État (Bill) :** ledger existant hors repo (`~/workspace/kernel/holons/ledger-graham.md`, 22 reçus G-20261009-001→022, dernier 2026-10-09), doctrine « sans reçu, pas de merge » en texte seul (`.github/agents/s3-companions.agent.md:27-29`), **aucune enforcement codée**, aucun reçu depuis 8 jours, rédacteur dormant.

### Décisions design
1. **Double réactivation :** (a) **émission ritualisée** — Graham (ou Compagnon désigné) émet : reçu par mission terminée + reçu hebdo au rituel M'Benga/Graham ; (b) **enforcement codée** — « sans reçu, pas de merge » devient un check CI requis, pas une phrase de doc.
2. **Le ledger vivant vit DANS le repo** (versionné) : `ledger/` à la racine (ou emplacement tranché à l'exécution, documenté). Les 22 reçus historiques sont importés comme **bloc genesis** (marqués comme tels, intacts).
3. **Schéma de reçu (versionné)** : `mission_id` + `SHA` + `observed_at`/`recorded_at` (vérité temporelle) + liens de preuve + émetteur. Pas de reçu sans les cinq.
4. **Enforcement** : check CI `r10-receipt` — tout merge vers `main` exige un reçu référençant le head SHA (ou la PR). C'est ce check qui porte l'intégrité (arbitrage A2 : pas de verrouillage GitHub, contrôle par les reçus).

### Bornes
**IN :** `ledger/` repo + import genesis + schéma + check CI `r10-receipt` + rituel d'émission. **OUT :** réécriture de l'historique (genesis intact) ; enforcement hors CI (pas de hook local obligatoire).

### Hold-out (avant exécution)
| ID | Vérifie | Seuil |
|---|---|---|
| H-L01-1 | Émission ritualisée | 1 reçu par mission terminée + 1 reçu hebdo (2 cycles observés) |
| H-L01-2 | Merge sans reçu BLOQUÉ | PR seedée sans reçu → check `r10-receipt` rouge → merge impossible |
| H-L01-3 | Ledger versionné, vérité temporelle | `ledger/` dans le repo ; chaque reçu a les 5 champs dont observed_at/recorded_at |
| H-L01-4 | Genesis intact | les 22 reçus historiques présents, marqués genesis, non modifiés |

---

## L02 — Supabase : prouver la connexion live 🟢/⚪

**État (Bill) :** DDL versionné PRÉSENT (`os/business/supabase/migrations/` ~20 fichiers, `os/life/supabase/migrations/` + `config.toml`) — contredit l'audit. Clients présents (fail-fast life, thin client business + tests). **Écart : connexion live non prouvable sans secrets ; aucune sonde automatisée.**

### Décisions design
1. **Ne pas refaire le DDL.** La fondation « Supabase » = DDL versionné (acquis) + **sonde live** (manquant).
2. **Sonde automatisée, lecture seule** : `tools/supabase-probe` (ou job CI) — connexion avec clé anon, check read-only (table connue / health), **zéro écriture**. Log horodaté.
3. **Secrets (A4) :** P0 = inventaire (métadonnées Vault → secrets Codespace → projet documenté). La sonde lit l'env, **jamais de secret en repo, jamais de secret codé en dur**. Si introuvable → escalade via A0 (capacité/vision), pas d'exigence au Capitaine.
4. **Non-régression** : le fail-fast et le mode `VITE_LIFE_LOCAL_ONLY` restent intacts (la sonde ne les contourne pas).

### Bornes
**IN :** sonde read-only + log horodaté + protocole d'inventaire secrets (A4). **OUT :** nouvelle migration DDL ; écriture en base par la sonde ; secrets en repo.

### Hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-L02-1 | Sonde existe, read-only | script présent ; audit : 0 écriture dans le code de la sonde |
| H-L02-2 | Sonde verte sur instance live | exit 0 + log horodaté (connexion réelle, pas mock) |
| H-L02-3 | Aucun secret en repo | grep patterns secrets → vide |
| H-L02-4 | Fail-fast intact | client life : sans env → erreur explicite (sauf local-only + bannière) |

---

## L03 — Gateway + auth : design puis construction 🔴 — **CECI EST LE DESIGN D-N015**

**État (Bill) :** aucun code serveur gateway dans V4 (specs `...FleetGateway.md`, watchdog ps1, evidence `NEEDS_LIVE_CHECK` seuls) ; inchangé depuis le 2026-10-09. D-N015 existe au registre (ASSIGNÉ, 8 jours sans design) — **ce design le clôt**.

### Décisions design
1. **Héritage, pas réutilisation aveugle** : mon plan D-N015 du 2026-10-09 fournit la philosophie (Zero Trust : bearer token via env uniquement, `crypto.timingSafeEqual`, bind `127.0.0.1` par défaut, CORS origines explicites jamais `*`, module `gateway/` à la racine = capacité V4 native, pas greffée sur l'héritage). L'état actuel (zéro code serveur) impose un design frais, informé par cet héritage.
2. **Périmètre minimal viable** : middleware d'auth + protection des routes + `/health` (sans données métier) + registre de routes (les backends s'y enregistrent — aucun backend n'existe encore, le gateway EST le premier composant serveur).
3. **Contrat d'auth** : token requis sur toutes les routes `/api/*` ; `/health` ouvert ; 401 indiscernable (token absent vs invalide : même réponse) ; comparaison temps constant (grep `timingSafeEqual`).
4. **Secrets** : `GATEWAY_TOKEN` via env uniquement ; `.env.example` à valeurs vides ; aucun secret en repo (H-L03-5).
5. **Le pont Life→Business (127.0.0.1:3001, 🛡) reste hors gateway** — déjà `127.0.0.1`, aucun changement.

### Bornes
**IN :** `gateway/` (auth + routes + /health + registre), `.env.example`, `README` (modèle d'auth, rotation), tests d'auth. **OUT :** gestion comptes/utilisateurs (module identité V4 ultérieur) ; TLS (responsabilité déploiement) ; fédération inter-machines ; modification du pont 🛡.

### Hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-L03-1 | Module gateway à la racine, middleware d'auth présent | existe, V4-native |
| H-L03-2 | Sans token → 401 sur toutes les `/api/*` | 401 partout |
| H-L03-3 | Token valide → 200 | 200 |
| H-L03-4 | Temps constant | `timingSafeEqual` présent ; 0 comparaison naïve du token |
| H-L03-5 | Aucun secret en repo | grep → vide |
| H-L03-6 | Bind local strict | `0.0.0.0` absent ; écoute vérifiée `127.0.0.1` |
| H-L03-7 | R10 | reçu au ledger |

---

## L04 — CI : intégrité prouvée par les reçus 🟢

**État (Bill) :** protection configurée (`verify (ubuntu-latest)` + `verify (windows-latest)` requis), effective sur 4/4 PRs échantillonnées. **Réserve : `enforce_admins=false`** — l'owner peut bypasser, non journalisé comme tel. (Nuance mémoire 2026-10-09 : ne pas prétendre « aucun merge rouge possible » sans cette réserve.)

### Décisions design
1. **Ne pas reconstruire, ne pas verrouiller.** La fondation = la protection existante + **preuve d'intégrité par les reçus** (arbitrage Capitaine A2 : capacité maximale, contrôle par organigramme + reçus).
2. **Le bypass owner est une capacité délibérée, pas une vulnérabilité** (doctrine) : documenté explicitement comme tel — jamais présenté comme « aucun bypass possible ».
3. **Job d'audit non-bypass** : vérifie pour chaque merge sur `main` (fenêtre glissante) que les checks requis étaient verts **avant** le merge (timestamps check-runs vs merge). Rôle : **transparence du trail** (qui a bypassé, quand) — pas une marche vers le verrouillage. Bypass détecté → alerte visible et tracée.
4. **Le check `r10-receipt` (L01) rejoint les checks requis** : c'est lui qui bloque un merge sans reçu — l'intégrité vient des reçus, pas de GitHub.

### Bornes
**IN :** job d'audit non-bypass (transparence du trail) + bypass documenté comme capacité délibérée + intégrité prouvée par les reçus (L01). **OUT :** reconstruction de la CI ; verrouillage `enforce_admins` (écarté par arbitrage Capitaine A2).

### Hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-L04-1 | Protection intacte | `verify (ubuntu-latest)` + `verify (windows-latest)` requis sur `main` |
| H-L04-2 | Audit non-bypass vert | job présent ; échantillon de merges récents : 100 % checks verts pré-merge (ou bypass tracés avec qui/quand) |
| H-L04-3 | Bypass documenté comme doctrine | la doc dit explicitement : `enforce_admins=false`, bypass owner = capacité délibérée (capacité maximale), jamais « aucun bypass possible » |
| H-L04-4 | Intégrité par les reçus | un merge sans reçu R10 est bloqué par le check `r10-receipt` (L01) — la preuve d'intégrité ne dépend pas du verrouillage GitHub |

---

## L05 — Policy store versionné : créer, opposable 🔴

**État (Bill) :** inexistant en tant que composant (policies RLS SQL et retry-policy ne sont pas un store de gouvernance ; aucune doc ne fait office de store opposable).

### Décisions design
1. **Emplacement : `policy/` à la racine du repo** (versionné par git) : `REGISTRY.md` (index) + `POLICY-XXX.md` (une par politique) + `CHANGELOG.md`.
2. **Schéma de politique** : id, énoncé, périmètre, **mécanisme d'enforcement**, version, date d'effet, remplace.
3. **Opposable = effet observable.** Chaque politique déclare son enforcement (check CI / middleware / gate dispatch). Une politique sans enforcement est marquée **`DÉCLARATIVE`** — jamais présentée comme opposable (honnêteté).
4. **Seed initial (4 politiques, toutes opposables car checkées)** :
   - P-001 « sans reçu R10, pas de merge » → enforcement : check `r10-receipt` (L01) ;
   - P-002 « jamais de swarm sans design Clara signé » → enforcement : gate dispatch Nardole (registre) ;
   - P-003 « aucun secret en repo » → enforcement : check CI grep ;
   - P-004 « un service = un port, documenté avant d'écouter » → enforcement : check `PORTS.md`.
5. **Protocole de changement** : politique = PR + revue + entrée changelog ; **aucune édition silencieuse**.

### Bornes
**IN :** `policy/` + registre + changelog + 4 politiques seed + protocole. **OUT :** politiques déclaratives présentées comme opposables ; édition silencieuse.

### Hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-L05-1 | Store existe, versionné | `policy/` + REGISTRY.md + CHANGELOG.md dans le repo |
| H-L05-2 | Chaque politique opposable a un check qui mord | 4 violations seedées → 4 échecs visibles |
| H-L05-3 | Honnêteté déclarative | toute politique sans enforcement est marquée `DÉCLARATIVE` |
| H-L05-4 | Protocole tenu | aucun changement hors PR+revue+changelog (échantillon) |

---

## L06 — Compagnons : réactiver, pas recréer 🟡

**État (Bill) :** 9/9 chats existent (structure OK). Réel : 1/9 actif (Bill), 3 dormants depuis le 2026-10-09, 1 dormant-via-registre (silence depuis le 2026-10-11), 4 sans trace locale (« sans trace locale » ≠ preuve d'inexistence — à confirmer via `chat.list`).

### Décisions design
1. **P0 = inventaire via `chat.list`** (autorité), pas via le filesystem. Chaque Compagnon : actif / dormant / manquant — avec preuve.
2. **Yaz en premier** (interrupted) : diagnostiquer l'interruption puis consigner le statut avec son motif (cause établie → repris ; blocage persistant → parqué avec motif et suivi ; incertain → en suivi actif). Le statut est tracé, jamais deviné.
3. **Ping 9/9** : chaque Compagnon accuse réception + énonce son mandat lore-corrigé (les 9 nommés + canaux). Non-réponse = documentée avec suivi, pas ignorée.
4. **Rituel d'activité tracé** : battement périodique léger (adossé au heartbeat existant) — chaque Compagnon loggue activité / non-activité. **Dormant-mais-tracé est un état valide** (les 9 n'ont pas besoin de churner).
5. **Aucune recréation** : si `chat.list` confirme un chat manquant → recréation documentée (escalade opérationnelle, pas vision).

### Bornes
**IN :** inventaire `chat.list` + diagnostic Yaz + ping 9/9 + rituel tracé. **OUT :** recréation de chats existants ; ping sans mandat.

### Hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-L06-1 | Inventaire faisant foi | 9/9 statués via `chat.list` (actif/dormant/manquant + preuve) |
| H-L06-2 | Yaz diagnostiqué | cause de l'interruption documentée ; repris ou parqué (décision tracée) |
| H-L06-3 | Ping 9/9 | accusés de réception + mandats énoncés (ou non-réponse documentée + suivi) |
| H-L06-4 | Rituel établi | premier battement tracé pour les 9 |

---

## 2. Architecture des Design Systems (pour dispatch Nardole)

| Comp. | Systèmes livrés | Preuve |
|---|---|---|
| L01 | `ledger/` repo + schéma reçu (5 champs) + import genesis (22) + check CI `r10-receipt` + rituel d'émission | merge sans reçu BLOQUÉ (seed) |
| L02 | `tools/supabase-probe` (read-only, log horodaté) + protocole inventaire secrets A4 | sonde verte |
| L03 | `gateway/` (auth + routes + /health + registre) + `.env.example` + README — **= design D-N015, dispatch existant au registre** | auth vérifiée par test (401/200) |
| L04 | job d'audit non-bypass (transparence) + bypass documenté comme doctrine + intégrité par les reçus | audit vert sur échantillon |
| L05 | `policy/` (REGISTRY + POLICY-XXX + CHANGELOG) + 4 politiques seed + protocole de changement | 4 violations seedées → 4 échecs |
| L06 | inventaire `chat.list` + diagnostic Yaz + ping 9/9 + rituel d'activité tracé | 9/9 statués + premier battement |

**Dépendances d'exécution :** L06 → L04 → L02 → L01 → L05 → L03 (séquentiel, un exécutant). L01-enforcement rejoint les checks L04 ; L05 codifie L01/L04 ; L03 ferme D-N015.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — L06** | Inventaire `chat.list`, diagnostic Yaz, ping 9/9, rituel | H-L06-1..4 |
| **P1 — L04** | Job d'audit non-bypass (transparence du trail) ; bypass documenté comme capacité délibérée | H-L04-1..4 |
| **P2 — L02** | Inventaire secrets (A4) → sonde read-only → sonde verte | H-L02-1..4 |
| **P3 — L01** | `ledger/` + genesis + schéma + check `r10-receipt` (rejoint les requis) + rituel | H-L01-1..4 |
| **P4 — L05** | `policy/` + 4 seeds + protocole ; violations seedées | H-L05-1..4 |
| **P5 — L03** | `gateway/` + auth + tests (design D-N015 — dispatch existant au registre) | H-L03-1..7 |
| **P6 — Validation** | Revue Doctors (13e Kernel, 11e Life, 12e Buzz) → Nardole dispatche la validation | Tous verts |

**Règle d'exécution :** séquentiel, un seul exécutant. Le Chantier 2 ne dépend pas du salvage. `OWNER_STAND_DOWN=1` arrête tout.

## 4. Risques transverses

- **R1 — Secrets Supabase introuvables (A4).** → Escalade via A0 (capacité/vision) ; la sonde reste en attente documentée, pas en échec silencieux.
- **R2 — Tentation de verrouiller quand même.** → Écartée par arbitrage Capitaine A2 : capacité maximale, contrôle par organigramme + reçus. Le design ne contient aucune marche vers le verrouillage.
- **R3 — Arbitrage A1 (Takeout) sans effet ici.** → F-02 indépendant du Takeout ; aucun couplage.
- **R4 — Chat manquant confirmé (L06).** → Recréation documentée, escalade opérationnelle (pas vision).
- **R5 — Bypass owner et intégrité.** → Tranché par arbitrage Capitaine A2 : le bypass est une capacité délibérée (capacité maximale), pas une faille à fermer. L'intégrité est prouvée par les reçus (check R10 bloque le merge sans reçu) ; l'audit L04 assure la transparence du trail. Aucune marche vers le verrouillage.

## 5. Séquence d'exécution (pas un swarm)

```
P0 (L06 : acteurs) → H-L06 → P1 (L04 : gates) → H-L04 → P2 (L02 : sonde) → H-L02
  → P3 (L01 : ledger vivant) → H-L01 → P4 (L05 : policy store) → H-L05
  → P5 (L03 : gateway = D-N015) → H-L03 → P6 (revue Doctors → validation Nardole)
```

Tout écart → **BLOQUÉ** avec raison + qui débloque. Pas de contournement silencieux.

*Fin du plan F-02. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors (exécution dès validé, indépendant du salvage). Le design L03 clôt le D-N015 resté 8 jours sans design.*

---

# ADDENDUM A1 (L00) — Résilience aux quotas : la vivacité fait partie du L0

**Date :** 2026-10-17 ~11:15 EDT — **Signé Clara** (addendum au plan F-02 signé ; le corps du plan est intact).
**Root cause validée par le Capitaine :** le ledger mort depuis 8 jours = épuisement des quotas frontier + départ sur ChatGPT, pendant que tout le travail restait dans la sandbox. **Le ledger est une preuve de vivacité** : 8 jours de silence = l'organisme ne vivait pas. (Le volet « travail coincé en sandbox » est traité par SB-01/02/03 ; le présent addendum traite le volet « quotas ».)
**Exigence transverse (6 composants) : la résilience aux quotas fait partie du L0 — elle est nommée L00, socle transversal sous les L01–L06.**

## A1.1 — Principe : deux tiers de modèles, un seul tier de vivacité

- **Tier F (frugal, local)** — piste System 1 déjà validée par le Capitaine (Needle, GLiNER) : **tier de vivacité**, toujours disponible, sans quota frontier.
- **Tier X (frontier)** — **rehaussement uniquement**, jamais requis pour la vivacité.
- **Échelle de dégradation** (chaque boucle la documente) : `Normal` (X disponible) → `Dégradé` (X épuisé : templates déterministes + Tier F, **mode marqué**) → `Survie` (code déterministe seul). **Une boucle ne se tait jamais** — le silence est la panne, pas un mode.
- **Honnêteté du mode** : toute sortie émise en mode dégradé le porte (ex. reçu : « émis en mode dégradé (frugal) ») — jamais de sortie qui prétend le Tier X.

## A1.2 — Invariant de vivacité : le silence est une anomalie

Chaque boucle perpétuelle a un **silence maximal** ; le dépasser = anomalie visible + alerte (pas un état acceptable) :

| Boucle | Silence maximal | Surveillé par |
|---|---|---|
| Heartbeat | 1 intervalle manqué | timestamp du dernier run (déterministe, sans modèle) |
| Émetteur R10 (L01) | 1 mission sans reçu, ou 1 semaine (rituel hebdo) | check `r10-receipt` + log d'émission |
| Sonde Supabase (L02) | 1 run planifié manqué | log horodaté de la sonde |
| Audit non-bypass (L04) | 1 run planifié manqué | log du job |
| Rituel Compagnons (L06) | 1 battement manqué par Compagnon | registre du rituel |
| Watch fusion (G-01-C) | 1 run planifié manqué | log du watch |

Le contrôle de vivacité lui-même est **déterministe et sans quota** (comparaison de timestamps) — les surveillants ne meurent pas de la panne qu'ils surveillent.

## A1.3 — Intégration par composant

- **L01 (ledger)** : l'émission suit l'échelle §A1.1 — Normal : jugement complet ; Dégradé : reçu assemblé par template + contrôle de complétude Tier F, marqué « dégradé » ; le check CI `r10-receipt` est **pur code** (zéro modèle, toujours vivant). L'invariant §A1.2 s'applique à l'émetteur.
- **L02 (sonde)** : pur code, zéro modèle — classée **Tier D (déterministe)** ; l'exigence est déjà satisfaite par construction, le design le constate (pas de dépendance frontier à « ajouter »).
- **L03 (gateway)** : composant runtime, pas une boucle — son health check est sans quota par construction (HTTP). Rien à dégrader.
- **L04 (audit)** : pur code (comparaison de timestamps) — Tier D ; invariant §A1.2 sur ses runs.
- **L05 (policy store)** : les checks d'enforcement sont pur code (Tier D) ; l'assistance à la revue d'une politique dégrade vers Tier F + template (jamais de blocage silencieux d'une revue).
- **L06 (rituel Compagnons)** : l'agrégation du rituel = script déterministe ; le reporting de chaque Compagnon dégrade vers des pings structurés par template quand le Tier X est épuisé (un Compagnon qui ne peut plus « parler » continue de **signaler**).
- **Heartbeat (transverse)** : checks déterministes (git, gh api, fichiers — zéro modèle) + synthèse Tier F ; le Tier X n'est qu'un rehaussement du rapport.

## A1.4 — Tests hold-out (ajoutés AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-F02-Q1 | **Les boucles L0 survivent à une panne de quotas frontier** | simulation `FRONTIER_OFFLINE=1` (ou mock) : heartbeat, émission R10, sonde L02, audit L04, rituel L06 effectuent chacun un cycle complet en Tier F/déterministe — 0 appel frontier (journal d'appels vérifié), 0 boucle silencieuse |
| H-F02-Q2 | Le silence est une anomalie | silence seedé au-delà du maximum §A1.2 → alerte visible et tracée |
| H-F02-Q3 | Honnêteté du mode dégradé | toute sortie émise en dégradé porte son mode ; aucune ne prétend le Tier X |

## A1.5 — Ce que l'addendum ne fait pas

- Il ne sert pas les modèles frugaux (piste System 1 du Capitaine — son infrastructure) : il spécifie les tiers, l'échelle et les invariants que les boucles doivent respecter.
- Il n'ajoute aucune dépendance réseau : le contrôle de vivacité est local et déterministe.
- Il ne rouvre pas le corps signé du plan : en cas de conflit, l'addendum (postérieur, daté) fait foi sur son périmètre.

*Fin de l'addendum A1 (L00). Signature Clara apposée — le 13e Doctor est informé (via Rick) : l'addendum est revu avec la validation F-02.*
