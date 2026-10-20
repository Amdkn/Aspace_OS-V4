# D-N017 · Lot 2 — Plans bornés gouvernance & structure (M-08, M-09, M-10, M-11, M-12)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE — 2026-10-09
**Source :** dispatch D-N017 (Nardole, AGORA) ; registre typé Bill D-N013
**Séquençage Clara :** M-08 → M-09 → M-10 → M-11 → M-12 (les garde-fous d'abord — ils protègent tout le reste ; puis structure Life OS, matrice, UX, coordination)
**Opérationnalise :** D-N014 (les gardes M-08 protègent le contrat d'architecture 3 OS et les surfaces 🛡) et D-N015 (M-09 unifie les frameworks vers la Gateway V4)
**Statut :** plans livrés — **SIGNÉ Clara (lot 2)**. Pas un swarm : un exécutant à la fois, dans l'ordre du séquençage.

---

## M-08 — Garde-fous irréversibles

**Objectif (Bill) :** les leçons coûteuses deviennent des gardes automatiques, pas des souvenirs.

### Décisions design (Clara)
Chaque règle = **un check automatique** (CI ou gate) qui échoue visiblement quand violée. Six gardes, six checks :

1. **Aucune mission « retirer/supprimer » sans décision S2 écrite préalable.** Check : tout spec de mission contenant un verbe de suppression (`supprimer`, `retirer`, `abandonner`, `delete`, `remove`) doit citer une référence de décision S2 — sinon le gate refuse le dispatch (Nardole ne dispatche pas).
2. **Aucune capacité ne sort sans S2 + validation S1.** Check : changement de statut d'une capacité dans le registre (vers `abandonné`/`retiré`) exige les champs `decision_s2` + `validation_s1` renseignés — sinon CI rouge.
3. **Jamais de swarm sans Clara.** Check procédural + registre : aucun dispatch ne passe `EN DESIGN` → `PRÊT` sans plan signé Clara (Nardole refuse ; le registre l'interdit — cf. cycle de statuts).
4. **Surfaces 🛡 intouchables** (`capabilities` canonique, `river-adapter`, pont `os/life/src/lib/api/client.ts`). Check CI : toute modification d'un chemin 🛡 sans dossier d'exception enregistré → échec visible.
5. **DC souverain** (`C:\Users\amado\.aspace\dc` primaire). Check build-breaking : un test assert que le DC primaire résout vers le chemin souverain ; si un fallback devient silencieusement primaire (sans flag explicite `DC_FALLBACK_ASSUMED=1`) → build rouge.
6. **Doctrine #415** (parité technique Business→Life sans copier la sémantique). Check : copie intégrale d'un fichier `os/business` → `os/life` sans justification de parité dans le commit → revue bloquée (gate de PR).

### Bornes
**IN :** les 6 checks (CI et/ou gates), documentés, avec leur message d'échec explicite.
**OUT :** — (le brut n'exclut rien ; le périmètre est les 6 gardes).

### Phases
P0 — Spec des 6 checks → P1 — Implémentation CI/gates → P2 — Violation seedée par garde (preuve que le check mord) → P3 — Documentation des messages d'échec → revue 12e.

### Tests hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-M08-1 | Chaque garde a un check automatique | 6/6 checks présents (workflow CI ou gate), nommés |
| H-M08-2 | Chaque check mord | 6 violations seedées → 6 échecs visibles (logs CI / refus de dispatch) |
| H-M08-3 | Surfaces 🛡 protégées | modification seedée d'un chemin 🛡 sans exception → échec |
| H-M08-4 | DC souverain | fallback silencieusement primaire (seed) → build rouge ; flag explicite → vert |

### Risques
R1 — Check décoratif (toujours vert) → H-M08-2 l'interdit. R2 — Garde 6 (#415) partiellement manuelle → assumé : gate de PR, pas CI pure ; documenté comme tel.

---

## M-09 — Structuration des 6 frameworks Life OS

**Objectif (Bill) :** les 6 frameworks sont structurés, conventionnés et unifiés vers la Gateway V4.

### Décisions design (Clara)
1. **Conventions** (syntaxe exacte, portée repo) : `[LIF:A3:]` = anchor Todo persistant (un par tâche, jamais réutilisé après Done) ; `[EVIDENCE][<VESSEL>-M<n>]` = Done avec preuve (le reçu R10 suit) ; `[DEV]` = Canceled (motif obligatoire) ; `[TACTIC]` / `[BRIDGE]` = typage des items.
2. **CER (M1→M3) et PRO (M1→M4) comme gabarits gelés** : copies canoniques intouchables ; chaque framework les instancie, ne les modifie pas.
3. **Échelle M1→M4 par framework** : M1 = cadré, M2 = structuré, M3 = éprouvé, M4 = franchisé (gabarit réplicable). Chaque framework déclare son M courant.
4. **Projection Issue→Calendar** : contrat de mapping issue → événement (6 calendriers + 1 agrégé) ; **Curie+GTD d'abord** — les autres calendriers suivent quand Curie+GTD est vert.
5. **Consignation `[CONSIGNATION][<VESSEL>]`** : Bill·Research = état des lieux, River·Flux = mécanique, Rory·Preuves = R10. Format fixe par vessel.
6. **Unification vers la Gateway V4** (D-N015) : les frameworks ne parlent aux services que via la surface authentifiée — aucun contournement local documenté.
7. Le « choix option 1/2/3 » du Capitaine : choix borné, présenté par le flux normal (S3→S2→A0→Rick) — jamais une question technique ouverte.

### Bornes
**IN :** conventions + gabarits CER/PRO + échelle M1→M4 + projection calendrier + consignation + unification Gateway.
**OUT :** le contenu métier des frameworks.

### Phases
P0 — Spec des conventions + gabarits gelés → P1 — Échelle M1→M4 + déclaration par framework → P2 — Projection Curie+GTD → P3 — Consignation + unification Gateway → revue 11e (Life) puis 12e.

### Tests hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-M09-1 | Les 6 frameworks portent les conventions | grep `[LIF:A3:]`, `[EVIDENCE]`, `[TACTIC]`/`[BRIDGE]` : présents dans les 6 |
| H-M09-2 | CER/PRO gabarits gelés et instanciés | gabarits intouchables + 6 instances |
| H-M09-3 | Projection calendrier Curie+GTD | ≥1 issue projetée en événement calendrier, vérifiable |
| H-M09-4 | Échelle M1→M4 déclarée | chaque framework déclare son M courant |
| H-M09-5 | Unification Gateway | aucun appel service hors surface authentifiée dans les docs framework |

### Risques
R1 — Conventions appliquées à moitié → H-M09-1 binaire. R2 — Projection calendrier bloquée côté Google → H-M09-3 seedée en local d'abord, puis connecteur.

---

## M-10 — Matrice fractale 8×8 + univers L2

**Objectif (Bill) :** 64 cellules `Mission → Actifs → Reçu vérifiable` ; LD01 prototype franchise réplicable ; 8 univers L2 arbitrés.

### Décisions design (Clara)
1. **Schéma de cellule** : `{ mission, actifs[], recu }` — `recu` = critère vérifiable (pas une intention). 64 cellules : 8 domaines Business × 8 domaines Life Wheel.
2. **Règle M/L** : M = coordonnée locale, L = imbrication. **Ne jamais convertir M0→L0** — la confusion d'échelles est une faute d'arbitrage.
3. **LD01 = gabarit franchise** : sections fixes (mission, actifs types, reçus types, rythme) réplicables aux 7 autres domaines.
4. **Arbitrage des 56 domaines LD02–LD08** : propositions **nouvelles**, pas d'héritage V3 — chaque proposition cite ses sources ou est marquée « nouveau ». Arbitre : Clara (désignée), appui 11e.
5. **Interdiction de copie sémantique** (doctrine #415) : attestation par domaine — « parité technique sans copie de sémantique ».

### Bornes
**IN :** matrice 64 cellules + gabarit LD01 + arbitrage 56 domaines + 8 univers L2 documentés.
**OUT :** la copie sémantique (interdite).

### Phases
P0 — Schéma de cellule + règle M/L → P1 — Matrice 64 cellules → P2 — Gabarit LD01 → P3 — Arbitrage 56 domaines → P4 — 8 univers L2 → revue 12e.

### Tests hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-M10-1 | Matrice publiée, 64 cellules complètes | chaque cellule a mission + actifs + reçu vérifiable |
| H-M10-2 | LD01 gabarit réplicable | sections fixes documentées |
| H-M10-3 | 8 univers L2 arbitrés et documentés | 8/8 avec décision d'arbitrage tracée |
| H-M10-4 | Pas de copie sémantique V3 | attestation #415 par domaine ; spot-check anti-copie |

### Risques
R1 — 56 arbitrages qui s'éternisent → timebox par domaine, arbitrage Clara tranche. R2 — Tentation d'importer les domaines V3 « tels quels » → H-M10-4.

---

## M-11 — Contrat UX double (BMAD-UX)

**Objectif (Bill) :** tout livrable UX porte le double contrat : `DESIGN.md` (identité visuelle) + `EXPERIENCE.md` (architecture d'information, comportements, états, accessibilité, parcours).

### Décisions design (Clara)
1. **Adoption du skill `bmad-ux` comme standard** : tout livrable à surface utilisateur l'exige — enregistré dans l'AGENTS.md du périmètre concerné.
2. **Sections requises** — `DESIGN.md` : identité visuelle, tokens, composants ; `EXPERIENCE.md` : architecture d'information, comportements, états (dont erreur/vide/chargement), accessibilité, parcours critiques.
3. **Livrable pilote** : la prochaine surface utilisateur livrée depuis `os/agent` (défaut : shell de l'app LifeOS si aucune autre) — désigné à l'exécution, pas avant.
4. **Validation** : relecture enregistrée des deux contrats (reviewer nommé, date) — pas de contrat auto-validé.

### Bornes
**IN :** standard adopté + gabarits des deux contrats + 1 livrable pilote.
**OUT :** —

### Phases
P0 — Adoption du standard + gabarits → P1 — Livrable pilote (les deux contrats rédigés) → P2 — Relecture validée → revue 12e.

### Tests hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-M11-1 | Standard adopté | mention dans l'AGENTS.md du périmètre + skill référençable |
| H-M11-2 | Pilote porte les deux contrats | `DESIGN.md` + `EXPERIENCE.md` présents, toutes sections requises remplies |
| H-M11-3 | Contrats relus et validés | relecture enregistrée (reviewer + date) |

### Risques
R1 — Contrats écrits après coup pour cocher la case → H-M11-3 exige la relecture avant livraison.

---

## M-12 — Coordination sourcée (Moltbook)

**Objectif (Bill) :** les Discussions GitHub V4 deviennent un lieu de coordination à contributions sourcées + RACI ; la popularité et la répétition ne donnent pas autorité.

### Décisions design (Clara)
1. **Gabarit de discussion** (sections obligatoires) : proposition · sources exigées (liens, pas des « on dit ») · RACI explicite (Responsible, Accountable, Consulted, Informed nommés) · décision (avec date et décideur).
2. **Règle « répétition ≠ autorité »** : une affirmation répétée sans source nouvelle ne gagne aucun poids — appliquée par les Doctors modérateurs (procédural, pas automatisable).
3. **Emplacement** : gabarit dans `.github/` (ou `docs/` si le repo préfère — tranché à l'exécution, documenté).
4. **Preuve d'usage** : au moins une discussion d'arbitrage réelle utilise le gabarit (sources + RACI remplis).

### Bornes
**IN :** gabarit + règle formalisée + 1 usage réel.
**OUT :** —

### Phases
P0 — Gabarit + règle → P1 — Publication → P2 — Usage sur une discussion d'arbitrage réelle → revue 12e.

### Tests hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-M12-1 | Gabarit publié | fichier présent à l'emplacement documenté |
| H-M12-2 | Utilisé sur une discussion d'arbitrage réelle | 1+ discussion avec sources + RACI remplis |
| H-M12-3 | Règle « répétition ≠ autorité » formalisée | énoncée dans le gabarit et le registre |

### Risques
R1 — Gabarit ignoré dans la pratique → H-M12-2 l'interdit (pas de « publié et jamais utilisé »).

---

## Séquence d'exécution du lot 2 (pas un swarm)

```
M-08 (P0→P3, H-M08-1..4) → M-09 (P0→P3, H-M09-1..5, revue 11e puis 12e)
  → M-10 (P0→P4, H-M10-1..4) → M-11 (P0→P2, H-M11-1..3) → M-12 (P0→P2, H-M12-1..3)
  → revue 12e par mission → merge 12e
```

M-08 en premier : les gardes protègent l'exécution de tout le reste (y compris le lot 1 si encore en cours).

Tout écart → **BLOQUÉ** avec raison + qui débloque, enregistré par Nardole.

*Fin du lot 2. Signature Clara apposée — M-08, M-09, M-10, M-11, M-12 PRÊTS, dispatchables dans l'ordre.*
