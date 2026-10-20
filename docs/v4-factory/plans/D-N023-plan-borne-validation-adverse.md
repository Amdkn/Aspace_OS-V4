# D-N023 — Plan borné : couche de validation adverse du Grep-Loop (M-14-C)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE — 2026-10-09
**Source :** dispatch D-N023 (Nardole, AGORA) ; mission typée Bill M-14-C (`~/workspace/frameworks/registre/evaluation-anti-sycophanie.md` §4, verdict ADAPTER vérifié)
**Arrimage :** M-02 (le validateur hold-out aux critères cachés — H-M02-2), M-03 (le Grep-Loop et son standard de preuve), D-N022 (les PRs de canonisation, à fort enjeu, y passent aussi)
**Séquençage Clara :** D-N017 lot 1 → **D-N023** → D-N017 lot 2 → D-N022 — la couche adverse complète le stack de validation factory (M-01/M-02/M-03/M-04) avant la gouvernance
**Décision Bill respectée (écarté) :** fine-tuning PlurPO du reviewer ; implémentation littérale du protocole instance-optimal (preuves d'optimalité/équilibres non codées)
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant à la fois.

---

## 0. Décisions design (autorité Clara — tranchées ici, ne remontent pas)

1. **Deux paliers (mapping Knox, §2.2 de l'évaluation) :**
   - **Inner** (rapide, frugal, chaque itération) : reviewer /5 **indépendant** (M-03, H-M03-3) avec la **rubrique enrichie** (§0.2). Un 5/5 Inner = PR ouvrable, pas mergée.
   - **Outer** (lourd, post-PR, pré-merge) : **débat adverse** défenseur vs challenger + **juge**. Le débat est le sas de merge (M-02) : aucun merge sans verdict du juge.
2. **Rubrique /5 enrichie (principe PlurPO adapté) :** toute note se défend depuis **trois perspectives** — *mainteneur futur* (pourriture ? lisible ? testé ?), *auditeur sécurité* (secrets, boundaries, 🛡), *utilisateur final* (la mission promise est-elle tenue ?). **Note finale = minimum des trois sous-notes** — un PR n'est fort que par son maillon faible ; la complaisance sur une dimension ne compense plus.
3. **Protocole du débat :**
   - **Challenger** : reçoit PR + périmètre mission — **ni les critères cachés, ni la note du reviewer** (anti-ancrage). Mission : construire le dossier le plus fort que le PR vaut < 5/5.
   - **Défenseur** : répond point par point (peut être l'exécutant d'origine ou un défenseur désigné).
   - **Juge** : agent **indépendant** (id différent du reviewer, du challenger et du défenseur — vérifiable aux logs), seul à voir les **critères cachés**. Rend : note /5 + verdict (merge / renvoi en boucle avec les findings du challenger) + trace.
4. **Critères cachés scellés** : écrits au design (par mission ou classe de mission), stockés hors d'atteinte des débatteurs, **révélés uniquement dans le reçu post-verdict**. C'est le mécanisme H-M02-2 de M-02, ici concrétisé.
5. **Anti-collusion :** indépendance des ids (§0.3) + critères cachés + le challenger ignore la note du reviewer + le juge ne rejuge jamais deux fois de suite le même PR. Modèles différents pour le juge vs les débatteurs **quand disponibles** (table de routage M-01) — sans en faire un prérequis bloquant.
6. **Coût borné :** le débat est **Outer uniquement** (jamais par itération Inner). **Cap = 3× le coût du reviewer Inner** par débat, mesuré (tokens/temps) et loggé. Débat qui dépasse le cap → le juge tranche sur pièces (pas de boucle infinie).
7. **Verdict < 5/5 = renvoi en boucle** avec les findings du challenger comme entrée — jamais un merge silencieux.

## 1. Bornes (scope strict)

**IN :**
- Rubrique /5 enrichie (3 perspectives, règle du minimum) + protocole de scellement des critères cachés.
- Contrats de prompts des trois rôles (ce que chacun voit / ne voit pas — §0.3).
- Câblage Outer : débat post-PR pré-merge, cap de coût + mesure, verdict du juge comme gate de merge.
- Preuve adverse : **un PR notoirement faible → < 5/5 après débat** (cas seedé/provoqué, tracé) + **un faux 5/5 historique re-noté à la baisse**.
- Documentation du surcoût (mesuré, borné).

**OUT (explicitement hors scope) :**
- Fine-tuning PlurPO du reviewer (écarté par Bill — mauvaise couche, mauvais domaine).
- Implémentation littérale du protocole instance-optimal (écarté — théorique, non actionable).
- Le contenu des reçus métier (owners des domaines).

## 2. Phases et gates

| Phase | Objectif | Exécutant | Gate de sortie |
|---|---|---|---|
| **P0 — Rubrique** | Grille /5 enrichie (3 perspectives, règle du minimum) + protocole de scellement des critères cachés | Agent | **Gates :** V5 |
| **P1 — Rôles** | Contrats de prompts défenseur/challenger/juge (visibilité §0.3) + règles d'indépendance et d'anti-collusion | Agent | **Gates :** V3, V4 |
| **P2 — Câblage Outer** | Débat post-PR pré-merge comme gate ; cap 3× + mesure du coût ; verdict < 5/5 = renvoi en boucle | Agent | **Gates :** V6, V7, V8 |
| **P3 — Preuve adverse** | Cas seedé (PR faible → < 5/5 tracé) + re-notation à la baisse d'un faux 5/5 historique | Agent | **Gates :** V1, V2 |
| **P4 — Revue + merge** | Revue technique 12e, merge par le 12e (doctrine AGORA) | 12e Doctor | **Gates :** V1–V9 tous verts ; V9 (R10) |

**Règle d'exécution :** une phase à la fois, un seul exécutant actif. `OWNER_STAND_DOWN=1` arrête tout.

## 3. Tests hold-out (définis AVANT exécution — validation aveugle)

| ID | Vérifie | Comment | Seuil |
|---|---|---|---|
| **V1** | Un PR notoirement faible obtient < 5/5 après débat | cas seedé : PR faible documenté → débat complet → note finale | **< 5/5**, avec trace défenseur/challenger/juge |
| **V2** | Un faux 5/5 historique est re-noté à la baisse | avant (5/5 reviewer seul) vs après (débat) | delta **< 0**, documenté |
| **V3** | Indépendance des rôles | reviewer, challenger, juge, défenseur : ids agents dans les logs | **4 ids distincts** (défenseur peut = exécutant, mais ≠ les 3 autres) |
| **V4** | Critères cachés scellés | audit des contextes : les critères n'apparaissent dans aucun prompt du challenger/défenseur avant verdict | **0 occurrence** avant verdict ; révélés dans le reçu |
| **V5** | Rubrique à 3 perspectives appliquée | chaque note /5 cite les 3 sous-notes ; finale = min | **100 %** des notes conformes |
| **V6** | Surcoût borné et mesuré | coût du débat loggé (tokens/temps) par débat | **≤ 3×** le coût reviewer Inner |
| **V7** | Débat Outer uniquement | aucun débat déclenché par itération Inner | débats **post-PR** seulement |
| **V8** | Verdict < 5/5 bloque le merge | PR dégradé par le juge | **non mergé**, renvoyé en boucle avec findings |
| **V9** | Traçabilité R10 | reçu (mission_id D-N023 + SHA + les 3 artefacts : cas seedé, re-notation, mesure de coût) | présent |

## 4. Risques

- **R1 — Collusion des débatteurs** (même modèle, mêmes biais). → Traité par §0.5 (indépendance + critères cachés + aveuglement du challenger) ; V3/V4 le vérifient.
- **R2 — Latence ajoutée à la boucle.** → Outer uniquement (§0.6) ; cap 3× ; le juge tranche sur pièces au-delà.
- **R3 — Juge qui devient le nouveau point de complaisance.** → La Meta Loop (M-04) en fera une classe d'échec surveillée ; les verdicts sont tracés et re-vérifiables.
- **R4 — Critères cachés qui fuient par les reçus précédents.** → Rotation des critères par classe de mission ; un critère révélé n'est plus utilisé tel quel.

## 5. Séquence d'exécution (pas un swarm)

```
[D-N017 lot1] → D-N023 P0 (rubrique+scellement) → V5 → P1 (rôles) → V3/V4
  → P2 (câblage Outer) → V6/V7/V8 → P3 (preuve adverse) → V1/V2
  → V9 → revue 12e → merge 12e → [D-N017 lot2 → D-N022]
```

Tout écart → **BLOQUÉ** avec raison + qui débloque, enregistré par Nardole. Pas de contournement silencieux.

*Fin du plan. Signature Clara apposée — D-N023 PRÊT, dispatchable après D-N017 lot 1.*
