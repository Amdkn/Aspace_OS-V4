# D-N017 · Lot 1 — Plans bornés factory (M-01, M-03, M-02, M-04)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE — 2026-10-09
**Source :** dispatch D-N017 (Nardole, AGORA) ; registre typé Bill D-N013 (`~/workspace/frameworks/registre/REGISTRE-INSPIRATIONS.md`, 18 missions, traçabilité au brut vérifiée)
**Séquençage Clara :** M-01 → M-03 → M-02 → M-04 (Leon d'abord ; le standard de preuve se branche sur le harnais ; la Dark Factory s'imbrique dessus ; la Meta Loop observe le tout)
**Opérationnalise :** D-N014 (contrat d'architecture 3 OS — le harnais vit dans le mono-repo) et D-N015 (toutes les surfaces d'exécution passent par le Gateway authentifié quand il existe)
**Statut :** plans livrés — **SIGNÉ Clara (lot 1)**. Pas un swarm : un exécutant à la fois, dans l'ordre du séquençage.

---

## M-01 — Finir la Factory Leon

**Objectif (Bill) :** la boucle issue → label → agent → PR → merge tourne de bout en bout sans touche intermédiaire.

### Décisions design (Clara)
1. **Machine à états par labels** (contrat) : `factory:ready` → `factory:running` → `factory:review` → `factory:done`. Transitions uniquement par le harnais (workflow), jamais à la main — un label posé manuellement hors workflow = anomalie routée au heartbeat.
2. **Une sandbox par agent** : `git worktree` isolé par mission (discipline Ross). Aucun partage de workspace entre deux agents d'une même vague.
3. **Routage par forces des modèles** (table contractuelle) : 3D → Codex, code complexe → Claude, doc → modèle frugal. Le routage est une règle du harnais, pas un choix d'exécutant. **Confiné au core Buzz** (re-pass Leon M-13a) : les 3 cores (Kernel, Life, Buzz) sont des frontières de sécurité et de responsabilité fonctionnelle, pas des paliers de performance LLM — le routage ne s'applique ni entre les cores ni à l'intérieur de Kernel/Life.
4. **Merge = Doctor compétent** (doctrine AGORA — pas de gate Capitaine). Le « merge humain » du brut = le sas Doctor, pas un clic Capitaine.
5. Le test `factory:ready` de bout en bout porte sur **une vraie issue** (pas un exercice) ; le run log fait foi.
6. **Les labels GitHub sont une machine à états VISUELLE, pas le registre de preuve** (re-pass Leon M-13a, correction R10). Un label est modifiable par tout tiers ayant accès au repo, sans preuve cryptographique ; **l'autorité de preuve reste au registre R10** (reçu immuable : mission_id + SHA + faisceau). Règle : la piste des labels doit être re-dérivable du ledger ; en cas de divergence label ≠ ledger, **le ledger gagne** et la divergence est une anomalie routée au heartbeat.

### Bornes
**IN :** harnais complet (workflows + labels + worktrees + routage) ; test e2e réel ; run log comme reçu.
**OUT :** Dark Factory (M-02), standard de preuve (M-03 — se branche ici en M-03).

### Phases
P0 — Harnais : workflows + machine à états + worktree par agent → P1 — Routage modèles (table contractuelle) → P2 — Test e2e sur vraie issue → P3 — Revue 12e → merge 12e.

### Tests hold-out (avant exécution)
| ID | Vérifie | Seuil |
|---|---|---|
| H-M01-1 | Une issue `factory:ready` traverse tout le pipeline sans intervention intermédiaire | timeline issue : tous les changements de labels par le workflow, zéro touche manuelle |
| H-M01-2 | Un worktree isolé par agent | `git worktree list` : 1 worktree par agent actif, aucun partage |
| H-M01-3 | PR mergée uniquement sur CI verte + revue | merge commit avec checks verts vérifiés |
| H-M01-4 | Routage modèles honoré | le run log indique quel modèle a traité quelle classe de tâche, conforme à la table |
| H-M01-5 | Reçu R10 | mission_id + SHA + run log au ledger |
| H-M01-6 | Les labels ne sont PAS le ledger | pour une mission terminée, la piste des labels est re-dérivée du registre R10 ; un label modifié à la main → divergence détectée, **le ledger fait foi** (re-pass Leon M-13a) | 0 divergence non détectée |

### Risques
R1 — Touche manuelle « pour débloquer » pendant le test e2e → invalide le test, on recommence. R2 — Routage contourné par un exécutant → H-M01-4 rouge = phase rejetée.

---

## M-03 — Preuves matérielles / R10 (standard de preuve)

**Objectif (Bill) :** aucune affirmation d'agent ne vaut sans preuve matérielle ; aucun agent « actif » sans reçu. *Se branche sur le harnais M-01.*

### Décisions design (Clara)
1. **Format du faisceau de preuve** (par type de claim) : code → diff + log de tests ; UI → screenshots avant/après ; perf → télémétrie (latence mesurée, jamais un claim) ; doc → walkthrough enregistré. Un « done » sans le faisceau correspondant = non-done.
2. **Grep-Loop** : reviewer **indépendant** (agent/session différent de l'exécutant — vérifiable dans les logs), note /5 sur grille fixe, renvoie en boucle jusqu'à 5/5. **Un score < 5/5 bloque la notification de complétion** (pas de « done » partiel).
3. **Vocabulaire à 4 états, strict** : `documenté` / `installé` / `exécuté` / `vérifié`. Un rapport d'agent emploie exactement un état par claim, avec la preuve correspondante. « Vérifié » sans artefact de vérification = H-M03-4 rouge.
4. **Schéma du reçu R10** : `mission_id` + `SHA` + liens vers le faisceau de preuve. Pas de reçu sans les trois.
5. **Traçabilité du routage (borne re-pass Leon M-13a)** : le faisceau de preuve enregistre le modèle exécutant **et son core** ; le routage par force de modèle est confiné au core Buzz (cf. M-01 §0.3) — tout routage entre cores, ou à l'intérieur de Kernel/Life, est un finding du reviewer (note plafonnée en conséquence).

### Bornes
**IN :** standard de preuve + Grep-Loop + schéma R10, intégrés au harnais M-01.
**OUT :** le contenu des reçus métier (owners des domaines).

### Phases
P0 — Grille /5 + format du faisceau → P1 — Grep-Loop (indépendance du reviewer) → P2 — Vocabulaire 4 états dans les rapports → P3 — Intégration harnais M-01 → revue 12e.

### Tests hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-M03-1 | Tout « done » d'agent est accompagné de son faisceau de preuve | 100 % des claims « done » liés à un artefact |
| H-M03-2 | Score < 5/5 bloque la notification | simulation : reviewer à 3/5 → aucune notification de complétion émise |
| H-M03-3 | Indépendance du reviewer | agent_id reviewer ≠ agent_id exécutant dans les logs |
| H-M03-4 | « Vérifié » toujours sourcé | grep `vérifié` sans artefact adjacent → vide |

### Risques
R1 — Reviewer complaisant (5/5 systématique) → la Meta Loop (M-04) en fera une classe d'échec candidate. R2 — Faisceau de preuve décoratif (screenshots sans rapport) → la grille /5 le sanctionne.

---

## M-02 — Dark Factory imbriquée

**Objectif (Bill) :** autonomie totale à l'intérieur du périmètre mission (PRD → code → validation adverse → blue/green, zéro humain) ; à la sortie, le merge est un sas à la frontière.

### Décisions design (Clara)
1. **Gouvernance à 3 niveaux** (contrats) : `global_rules.md` (immuable par la mission — seules la Meta Loop et S2 y touchent), `factory_rules.md` (règles de la vague), `mission.md` (périmètre). **Droit de refus formel** : tout agent refuse par écrit (motif + règle déclenchée) ce qui sort du périmètre — le refus est un reçu, pas un échec.
2. **Validateur hold-out aveugle** : rôle séparé, critères **écrits par le design (moi) et cachés à l'exécutant**. Le verdict est tracé (critères révélés après coup dans le reçu).
3. **Scheduler 30 min** : `Fix PR → Review PR → validé → triage`, en boucle. Un cycle manqué = anomalie heartbeat, pas un rattrapage silencieux.
4. **Blue/green automatique** : deux worktrees/branches (blue = stable, green = candidate) ; bascule auto si hold-out vert, **rollback auto** si rouge post-bascule.
5. **Control plane non éditable par l'agent** : les fichiers du loop (`tools/`, workflows) sont en lecture seule pour les agents de mission (worktree sans droit d'écriture sur le control plane — vérifié par H-M02-4).
6. **Doctrine no-human-gate à l'intérieur du périmètre** (D-03 du registre) ; le sas de merge reste à la frontière (Doctor).

### Bornes
**IN :** les 3 fichiers de gouvernance + validateur aveugle + scheduler + blue/green + control plane verrouillé.
**OUT :** le sas de merge lui-même ; preuves matérielles (M-03 — déjà conçu, se branche ici).

### Phases
P0 — Gouvernance 3 niveaux + droit de refus → P1 — Validateur hold-out (critères scellés) → P2 — Scheduler 30 min → P3 — Blue/green + rollback → P4 — Verrouillage control plane → P5 — Traversée complète sans humain → revue 12e.

### Tests hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-M02-1 | Un PRD traverse jusqu'au déploiement avec zéro action humaine | timeline complète sans touche manuelle |
| H-M02-2 | Le validateur rend un verdict tracé | verdict + critères (révélés après) au ledger |
| H-M02-3 | Au moins un refus formel hors-périmètre est enregistré | 1+ refus écrit (motif + règle) — on le provoque si nécessaire |
| H-M02-4 | Control plane intact après la vague | hash des fichiers `tools/` + workflows identique avant/après |
| H-M02-5 | Rollback blue/green fonctionne | simulation d'échec post-bascule → retour blue vérifié |

### Risques
R1 — Validateur et exécutant partagent les critères par fuite → les critères sont scellés hors d'atteinte de l'exécutant (fichier non monté dans son worktree). R2 — Périmètre flou → le droit de refus le révèle ; on resserre `mission.md`.

---

## M-04 — Meta Loop / rituel M'Benga-Graham

**Objectif (Bill) :** chaque semaine, les classes d'échecs récurrents deviennent règles globales, playbooks et skills versionnées.

### Décisions design (Clara)
1. **3 boucles scellées** (mapping Knox D-05) : Inner = L2 (frugale, pré-PR), Outer = L1 (lourde, post-PR), Meta = L0 (hors-cycle, hebdo). Scellées = périmètres et rythmes fixes, non négociables par les exécutants.
2. **Format du rituel hebdo** (tenu, pas automatisé aveuglément) : classes d'échecs observées (sourcées aux logs) → règles candidates → règles adoptées → versions de skills bumpées. Tenu par Graham (preuves) avec M'Benga (audit) — jugement requis pour promouvoir une classe d'échec en règle.
3. **Cycle de vie d'une règle** : `candidate` → `adoptée` (décision S2 ou Doctor) → versionnée dans `global_rules.md`. Chaque règle adoptée pointe vers l'échec réel qui l'a fait naître (lien bidirectionnel).
4. **Triade mesurée** : Autonomie (% missions sans escalade), Automatisation (% étapes sans touche), Qualité (taux de hold-out verts). Trois nombres publiés chaque semaine — pas de prose sans chiffres.
5. **Versionnage des skills** : `MAJEUR.MINEUR` + changelog ; une skill sans version = non déployée.

### Bornes
**IN :** rituel hebdo + cycle de vie des règles + triade + versionnage skills.
**OUT :** l'audit reste un rituel tenu — aucune automatisation aveugle de la promotion des règles.

### Phases
P0 — Format du rituel + triade → P1 — Cycle de vie des règles (`global_rules.md`) → P2 — Versionnage skills → P3 — Premier rituel tenu → revue 12e.

### Tests hold-out
| ID | Vérifie | Seuil |
|---|---|---|
| H-M04-1 | Un rapport hebdo existe | daté, au lieu convenu, avec les 3 nombres de la triade |
| H-M04-2 | Au moins une règle globale est née d'un échec réel et tracé | lien bidirectionnel règle ↔ log d'échec |
| H-M04-3 | Les skills sont versionnées | version + changelog par skill déployée |
| H-M04-4 | Le rituel est tenu, pas automatisé | tenu par Graham/M'Benga (jugement enregistré), pas par un cron aveugle |

### Risques
R1 — Rituel qui devient du reporting décoratif → H-M04-2 l'interdit (pas de règle sans échec source). R2 — Premières règles candidates déjà connues : amputation #34, collision D-N010/11/12 (registre §brut 4) — à verser au premier rituel.

---

## Séquence d'exécution du lot 1 (pas un swarm)

```
M-01 (P0→P3, H-M01-1..6) → M-03 (P0→P3, H-M03-1..4, branché sur M-01)
  → M-02 (P0→P5, H-M02-1..5) → M-04 (P0→P3, H-M04-1..4)
  → revue 12e par mission → merge 12e
```

Tout écart → **BLOQUÉ** avec raison + qui débloque, enregistré par Nardole.

*Fin du lot 1. Signature Clara apposée — M-01, M-02, M-03, M-04 PRÊTS, dispatchables dans l'ordre.*
