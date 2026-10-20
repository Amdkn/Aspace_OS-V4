# D-N015 — Plan borné : Gateway V4 propre (avec auth)

**Auteur :** Clara — compagnon du 12e Doctor, cœur Buzz, AUTORITÉ DE DESIGN UNIQUE — 2026-10-09
**Source :** ordre direct Capitaine, canal AGORA, 2026-10-09 ~16:10 EDT (registre Nardole : D-N015 ASSIGNÉ) ; risque résiduel du diagnostic V4 2026-10-06 (« Gateway without auth »)
**État actuel — ROUGE (vérifié sur `main` @ `2554e0f`) :** `os/life/server/blackboard/index.ts` — serveur express, `cors()` **ouvert**, **AUCUNE authentification sur aucune route** (GET/POST/DELETE — y compris écritures : workspaces, events, locks, artifacts), `app.listen(port)` sans host → bind `0.0.0.0` (toutes les interfaces). Des écritures non authentifiées sont exposées sur toutes les interfaces.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : séquence stricte, un exécutant à la fois.

---

## 0. Décisions design (autorité Clara — tranchées ici, ne remontent pas)

1. **Le Gateway est une capacité V4 native :** nouveau module `gateway/` **à la racine du repo** (pas dans `os/life`). L'auth ne se greffe pas sur l'héritage — elle est frontale et V4.
2. **Modèle d'auth Zero Trust :** bearer token via variable d'environnement `GATEWAY_TOKEN` **uniquement** (jamais en repo, jamais en UI — pattern V4). Comparaison en temps constant (`crypto.timingSafeEqual`). Token **requis sur toutes les routes `/api/*`** ; `/health` ouvert mais sans aucune donnée métier.
3. **Bind `127.0.0.1` par défaut.** `0.0.0.0` interdit sans décision design explicite et motivée.
4. **CORS restreint :** origines explicites via env ; jamais `*` en présence d'auth.
5. **Architecture : proxy frontal, pas middleware greffé.** Le Gateway proxie `/api/blackboard/*` → `127.0.0.1:4445`. Le blackboard reste le service interne : **durcissement minimal = bind `127.0.0.1` explicite, zéro changement fonctionnel.** Frontière propre héritage/V4.
6. **Pas de gestion de comptes/utilisateurs** (l'identité est un module V4 ultérieur — cf. décision Q4 du plan D-N004). Pas de TLS terminé dans le gateway (local-first ; TLS = responsabilité du déploiement, hors bornes).
7. **Port :** attribué dans `os/PORTS.md`. Proposition : **4440** (4444 = life vite, 4445 = blackboard, 3001 = bridge 🛡, 4417 = CubeFarm — 4440 libre de ces usages connus ; à confirmer à l'exécution).
8. Le bridge Life→Business (`127.0.0.1:3001`) reste **hors gateway** — 🛡 protégé, déjà `127.0.0.1`, aucun changement.

## 1. Bornes (scope strict)

**IN :**
- `gateway/` : app express (ou équivalent sobre) + middleware d'auth + proxy `/api/blackboard/*` + `/health` + log d'accès minimal (qui/quand/route — sans secrets).
- `.env.example` documentant `GATEWAY_TOKEN` et les origines CORS (valeurs vides, jamais de token réel).
- Durcissement blackboard : bind `127.0.0.1` explicite dans `os/life/server/blackboard/index.ts` (1 ligne, rien d'autre).
- `os/PORTS.md` : entrée du gateway (port + bind + auth).
- `gateway/README.md` : modèle d'auth, rotation du token, règle « pas de secret en repo ».
- Reçu R10 (mission_id + SHA) au ledger.

**OUT (explicitement hors scope) :**
- Aucune gestion d'utilisateurs, sessions, ou rôles (hors bornes — module identité V4 ultérieur).
- Pas de TLS dans le gateway.
- Pas de fédération inter-machines, pas de découverte de services.
- Aucune modification fonctionnelle du blackboard (hors bind).
- Aucun secret, token, ou valeur d'env réelle dans le repo.

## 2. Phases et gates

| Phase | Objectif | Exécutant | Gate de sortie |
|---|---|---|---|
| **P0 — Gateway** | Implémenter `gateway/` selon §0 (auth, proxy, /health, CORS, log) | Agent | **Gates :** G1–G8 |
| **P1 — Durcissement blackboard** | Bind `127.0.0.1` explicite (1 ligne) ; tests existants du blackboard verts | Agent | **Gates :** G6 (côté blackboard), G9 |
| **P2 — Registres + doc** | `os/PORTS.md`, `.env.example`, `gateway/README.md` | Agent | **Gates :** G5, G10 partiel |
| **P3 — Revue + merge** | Revue technique 12e, merge par le 12e (doctrine AGORA : pas de gate Capitaine — « l'autorité remplace le gate », clarification 12e) | 12e Doctor | **Gates :** G1–G10 tous verts ; G10 (R10) |

**Règle d'exécution :** une phase à la fois, un seul exécutant actif. `OWNER_STAND_DOWN=1` arrête tout.

## 3. Tests hold-out (définis AVANT exécution — validation aveugle)

Chaque test est binaire (pass/fail). L'exécutant ne redéfinit pas le succès.

| ID | Vérifie | Comment | Seuil |
|---|---|---|---|
| **G1** | Toute route `/api/*` sans token est refusée | `curl` sans `Authorization` sur chaque route proxée | **401** sur toutes |
| **G2** | Token valide = accès | `curl -H "Authorization: Bearer $GATEWAY_TOKEN"` | **200** sur toutes |
| **G3** | Token invalide indiscernable de l'absence | `Bearer faux` vs absence de header | même **401**, même corps (pas de fuite : « token invalide » vs « token manquant » interdits) |
| **G4** | Comparaison en temps constant | grep `timingSafeEqual` dans `gateway/` | présent ; aucune comparaison `===` sur le token |
| **G5** | Aucun secret en repo | grep `-rEi "sk-[a-z0-9]{20,}\|-----BEGIN.*PRIVATE KEY\|GATEWAY_TOKEN=.+" gateway/ os/life/server/blackboard/` | vide (`.env.example` : valeurs vides uniquement) |
| **G6** | Bind local strict | grep `0.0.0.0` dans `gateway/` → vide ; au démarrage, l'adresse d'écoute du gateway **et** du blackboard = `127.0.0.1` | les deux vérifiés |
| **G7** | CORS non ouvert | grep `cors()` sans options dans `gateway/` → vide ; aucune origine `*` avec credentials | vide |
| **G8** | `/health` sans fuite | réponse sans auth | clés limitées à `status`, `time` — aucune donnée métier |
| **G9** | Blackboard non régressé | tests existants du blackboard + diff `os/life/server/blackboard/` | verts ; diff = bind seul |
| **G10** | Traçabilité R10 | reçu (mission_id D-N015 + SHA) au ledger | présent |

## 4. Risques

- **R1 — Token en clair dans l'env du Codespace.** → Documenté dans `gateway/README.md` (rotation à chaque session sensible) ; jamais commité (G5).
- **R2 — Proxy vs middleware intégré.** → Tranché §0.5 : proxy. Rouvrir ce choix = hors bornes.
- **R3 — Collision de port 4440.** → Vérifiée à l'exécution contre `os/PORTS.md` ; si occupé, port suivant libre documenté — pas de port en dur non documenté.
- **R4 — Le gateway devient un point de passage obligé.** → C'est le but (surface unique authentifiée). Le blackboard direct reste possible en `127.0.0.1` pour le debug local — documenté, pas contourné.

## 5. Séquence d'exécution (pas un swarm)

```
P0 (gateway/) → G1–G8 → P1 (bind blackboard) → G6/G9 → P2 (registres/doc) → G5
  → G10 → revue 12e → merge 12e
```

Tout écart → **BLOQUÉ** avec raison + qui débloque, enregistré par Nardole. Pas de contournement silencieux.

*Fin du plan. Signature Clara apposée — D-N015 PRÊT, dispatchable.*
