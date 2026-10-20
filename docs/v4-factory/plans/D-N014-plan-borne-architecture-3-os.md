# D-N014 — Plan borné : architecture des 3 OS dans le mono-repo V4

**Auteur :** Clara — compagnon du 12e Doctor, cœur Buzz, AUTORITÉ DE DESIGN UNIQUE — 2026-10-09
**Source :** ordre direct Capitaine, canal AGORA, 2026-10-09 ~16:10 EDT (registre Nardole : D-N014 ASSIGNÉ)
**Point de départ (vérifié) :** `main` @ `2554e0f` (PR #66) — `os/agent` fidèle (142 fichiers, Agent OS Desktop), `os/business` fidèle (1 345 fichiers, Business OS / Coach OS), `os/life` réduit (tsc 0 erreur, vite build OK). PR #27 = migration d'origine.
**Alimentation :** D-N013 (Bill, Inspirations centralisées) quand livré — le plan ne l'attend pas ; §5 prévoit l'amendement.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : séquence stricte, un exécutant à la fois.

---

## 0. Décisions design (autorité Clara — tranchées ici, ne remontent pas)

1. **Les 3 OS coexistent** dans le mono-repo (ordre AGORA). La proposition d'abandon d'Agent OS dans `architecture/capabilities.json` (statut `abandonment_proposed`, « S1 Validation Required ») est notée **SUPERSEDÉE** par l'ordre AGORA. Réouverture possible uniquement via S1/Rick (escalade vision) — jamais par un exécutant.
2. **Aucune traversée de sous-arbre sans contrat documenté.** `os/agent`, `os/business`, `os/life` sont des propriétés fermées ; tout couplage inter-OS passe par un contrat nommé dans `os/ARCHITECTURE.md`.
3. **Zones sous inventaire D-N016 — intouchables dans D-N014 :** `os/agent/src/apps/{CoachOS, CoachOSOnline, Doctor11Life, Doctor12Bus, Doctor13Kernel, LifeOS, LifeOSOnline}`. Constatées comme chevauchement potentiel avec `os/life` et `os/business` — **aucun déplacement, aucune suppression, aucun renommage** dans D-N014. La déduplication est D-N016 phase 2 (Bill phase 1 → Clara phase 2).
4. **Le pont Life→Business (`127.0.0.1:3001/api/bridge`, zod) reste le seul couplage runtime inter-OS autorisé** — 🛡 protégé (registre `os/capabilities.registry.json`), hash vérifié avant/après (A7).
5. **Les registres sont la source de vérité :** `os/PORTS.md`, `os/capabilities.registry.json`, `IMPORT.json` par OS.

## 1. Bornes (scope strict)

**IN :**
- Rédaction de `os/ARCHITECTURE.md` : contrat d'architecture — les 3 OS, leurs racines, règle de propriété, règle de traversée (§0.2), interfaces autorisées (pont 🛡, registres), zones D-N016 marquées intouchables.
- Compléter `os/PORTS.md` : documenter les ports réels d'`os/agent` et `os/business` (aujourd'hui TBD) — règle « un service = un port, documenté avant d'écouter ».
- Mettre à jour `os/capabilities.registry.json` : refléter l'état post-migration (11 capabilities 🛡 actives, chemins existants).
- Exiger `IMPORT.json` présent et valide pour les 3 OS (dépend de D-N011 pour `os/life` — voir R2).
- Reçu R10 (mission_id + SHA) au ledger.

**OUT (explicitement hors scope) :**
- Aucune suppression, déplacement ou renommage de code (c'est D-N016 phase 2).
- Aucune résolution des duplications (inventaire Bill D-N016 phase 1 d'abord).
- Aucun nouveau code runtime, aucun refactor.
- Aucune décision d'abandon d'un OS (vision → S1/Rick si rouvert).
- Pas de `node_modules` commité.

## 2. Phases et gates

| Phase | Objectif | Exécutant | Gate de sortie |
|---|---|---|---|
| **P0 — Inventaire** | Lecture seule : cartographier ports en écoute (grep), imports inter-OS (grep), chemins du registre capabilities | Agent | Inventaire versé au plan, zéro écriture |
| **P1 — Contrat** | Rédiger `os/ARCHITECTURE.md` selon §0 | Agent | **Gates :** A1, A5, A6 |
| **P2 — Registres** | Compléter `os/PORTS.md`, mettre à jour `os/capabilities.registry.json` | Agent | **Gates :** A2, A3, A4 |
| **P3 — Revue + merge** | Revue technique 12e, merge par le 12e (doctrine AGORA : pas de gate Capitaine — « l'autorité remplace le gate », clarification 12e) | 12e Doctor | **Gates :** A1–A8 tous verts ; A8 (R10) |

**Règle d'exécution :** une phase à la fois, un seul exécutant actif. `OWNER_STAND_DOWN=1` arrête tout.

## 3. Tests hold-out (définis AVANT exécution — validation aveugle)

| ID | Vérifie | Comment | Seuil |
|---|---|---|---|
| **A1** | Le contrat d'architecture existe et est complet | `os/ARCHITECTURE.md` nomme les 3 OS + leurs racines + la règle de traversée + les interfaces autorisées | tous les éléments présents |
| **A2** | Aucun port non documenté | grep `listen(` / `--port=` / `process.env.PORT` sous `os/` → chaque occurrence couverte par `os/PORTS.md` | zéro « TBD » sans justification écrite |
| **A3** | Registre capabilities sans chemin mort | chaque entrée `protected` de `os/capabilities.registry.json` → chemin existant sur la branche | 11/11 chemins existants |
| **A4** | Traçabilité d'import par OS | `IMPORT.json` présent et JSON-valide sous `os/agent`, `os/business`, `os/life` | 3/3 valides |
| **A5** | Aucun couplage inter-OS hors contrat | grep des imports relatifs traversant `os/agent` ↔ `os/business` ↔ `os/life` hors contrats listés en §0 | vide, ou liste blanche explicite dans `os/ARCHITECTURE.md` |
| **A6** | Zones D-N016 intactes | diff avant/après sur `os/agent/src/apps/{CoachOS,CoachOSOnline,Doctor11Life,Doctor12Bus,Doctor13Kernel,LifeOS,LifeOSOnline}` | zéro suppression/déplacement/renommage |
| **A7** | 🛡 Pont Life→Business intact | SHA256 de `os/life/src/lib/api/client.ts` identique avant/après | hash inchangé |
| **A8** | Traçabilité R10 | reçu (mission_id D-N014 + SHA) au ledger | présent |

## 4. Risques

- **R1 — D-N013 non livré.** → Le plan n'attend pas Bill ; `os/ARCHITECTURE.md` prévoit une section d'amendement alimentée par D-N013/D-N016.
- **R2 — D-N011 (`os/life/IMPORT.json`) non mergé.** → A4 bloque P3. Pas de contournement : le blocage est enregistré par Nardole avec « en attente D-N011 ».
- **R3 — Tentation de « ranger » les duplications pendant l'inventaire.** → Interdit (§0.3). Tout déplacement constaté = A6 rouge = phase rejetée.
- **R4 — Proposition d'abandon d'Agent OS.** → Supersedée (§0.1). Un exécutant qui la rouvre = hors bornes.

## 5. Séquence d'exécution (pas un swarm)

```
P0 (inventaire RO) → P1 (contrat) → A1/A5/A6 → P2 (registres) → A2/A3/A4
  → A7/A8 → revue 12e → merge 12e
```

Tout écart → **BLOQUÉ** avec raison + qui débloque, enregistré par Nardole. Pas de contournement silencieux.

*Fin du plan. Signature Clara apposée — D-N014 PRÊT, dispatchable.*
