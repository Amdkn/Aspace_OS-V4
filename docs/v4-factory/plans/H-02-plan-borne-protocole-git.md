# H-02 — Plan borné : Protocole Commit/PR/Merge (fini le tout-sandbox)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) ; Discover Bill (`~/workspace/architecture-compagnons/qualif-protocole-git.md`)
**Faits structurants :** pipeline PR-only à **100 %** (20/20 commits via PR depuis le 09-10), merges owner en 1–16 min, **zéro bypass observé** (bypass conservé mais inutilisé) ; **0 artefact de la chaîne en repo** pendant que 19 PRs atterrissaient (09→16 oct.) ; « sans reçu, pas de merge » = doctrine sans enforcement (16 merges, 0 reçu).
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Le pipeline qui marche ne se casse pas.** PR-only, checks verts (ubuntu+windows requis), merge owner rapide : le protocole le **documente et le préserve**. Aucune friction ajoutée au flux agent qui fonctionne.
2. **Le R10 — analyse tranchée (pas de faux binaire).** Ni « enforcement partout » (friction sur un pipeline qui marche, contre la doctrine capacité maximale) ni « doctrine alignée sur l'absence » (enterre le contrôle par les reçus du Capitaine). **Décision : enforcement scopée** — le check `r10-receipt` s'applique aux **atterrissages de missions de la chaîne** (dispatches Nardole : designs, extractions, alignements, registres, ledger — le vrai trou : 0 artefact en repo). Le flux agent général continue sur checks + jugement owner. **Ceci affine F-02/L01** (« tout merge » → « atterrissages de la chaîne ») : la capacité maximale est préservée, la traçabilité de la chaîne devient réelle. Le texte de doctrine est aligné honnêtement : « sans reçu, pas de merge » vaut pour les missions de la chaîne ; ailleurs, les reçus = traçabilité.
3. **Attribution honnête.** L'acteur GitHub est Amdkn (son identité) — **documenté tel quel**, pas déguisé. L'auteur réel survit via : (a) convention de nommage des branches (`<agent>-*` : `jules-*`, `codex/*`, `ryan-*`…) ; (b) trailer dans le **corps de la PR** (record durable — survit au squash) ; (c) trailer de commit où le workflow le permet ; (d) émetteur du reçu R10. Un merge squashé reste attribuable (PR body + reçu).
4. **Artefacts de la chaîne dans le repo.** Registres (Nardole, Bill), plans (Clara), ledger (Graham) **vivent dans le repo** (mappings SB-01, convention H-05). La sandbox est l'espace de travail, **jamais l'archive** — un artefact de la chaîne qui n'existe qu'en sandbox est une anomalie de protocole.
5. **`CONTRIBUTING.md`** : le protocole écrit — qui commit/PR/merge (agents sur branches, PRs sous identité Amdkn, owner merge après checks + validation), reçus/checks (r10-receipt pour la chaîne), attribution (§0.3), **zéro push direct sur `main`**, `enforce_admins=false` documenté honnêtement (existe, inutilisé — pas « impossible »).
6. **V3 hors protocole** jusqu'à M7 tranché (G-01-C) : le protocole couvre V4 ; le protocole lâche de V3 (pushes directs, commits bot) est **quarantiné**, pas adopté silencieusement.

## 1. Bornes

**IN :** `CONTRIBUTING.md` + check `r10-receipt` scopé + alignement du texte de doctrine + convention d'attribution + artefacts de la chaîne en repo.
**OUT :** casser la CI qui marche ; forcer `enforce_admins` (arbitrage Capitaine) ; couvrir V3 avant M7.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — `CONTRIBUTING.md`** : protocole complet (acteurs, PR-only, checks, reçus, attribution, bypass documenté).
**Système 2 — Check `r10-receipt` scopé** : s'applique aux atterrissages de missions de la chaîne (marqueur : PR liée à un dispatch Nardole) ; le flux général n'est pas entravé.
**Système 3 — Attribution** : branches + PR body + reçus (chaîne d'attribution squash-safe).
**Système 4 — Atterrissage** : registres/plans/ledger en repo (lien SB-01/H-05).

**Flux :** P0 (CONTRIBUTING.md) → P1 (check scopé + doctrine alignée) → P2 (attribution) → P3 (atterrissage) → validation Doctors.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Protocole écrit** | `CONTRIBUTING.md` : acteurs, PR-only, checks, bypass honnête | H-H02-1 |
| **P1 — R10 scopé** | Check `r10-receipt` sur les atterrissages de la chaîne ; texte de doctrine aligné (§0.2) | H-H02-2, H-H02-3 |
| **P2 — Attribution** | Convention branches + PR body + reçus documentée et appliquée | H-H02-4 |
| **P3 — Atterrissage** | Registres, plans, ledger en repo (via SB-01/H-05) | H-H02-5 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-H02-1 | Protocole écrit | `CONTRIBUTING.md` existe : PR-only, checks requis, acteur Amdkn documenté, bypass `enforce_admins=false` honnête (existe, inutilisé) |
| H-H02-2 | Enforcement scopée | PR d'atterrissage de mission de la chaîne sans reçu → check rouge ; PR agent ordinaire sans reçu → merge normal (pas d'entrave) |
| H-H02-3 | Doctrine alignée | le texte « sans reçu, pas de merge » énonce son périmètre (chaîne) — plus d'aspiration blanket contredite par 16 merges |
| H-H02-4 | Attribution squash-safe | une PR agent mergée en squash montre l'agent dans le PR body + le reçu |
| H-H02-5 | Fini le tout-sandbox | registres, plans, ledger présents en repo (pas seulement en sandbox) |
| H-H02-6 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Doctrine vs pratique.** → Tranché §0.2 : enforcement scopée + texte aligné (ni blanket ni abandon).
- **R2 — V3 hors protocole.** → Quarantaine jusqu'à M7 (G-01-C) ; le protocole V4 ne l'absorbe pas.
- **R3 — Casser le pipeline.** → §0.1 : le flux agent n'est pas entravé (H-H02-2 le prouve).

*Fin du plan H-02. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors.*

---

## ADDENDUM H-02-A1 — SIGNÉ Clara (2026-10-18, ingestion Anthropic « Redesigning source control » via Bill/Scion)

**Source :** `~/workspace/architecture-compagnons/ingestion-scion-anthropic.md` (lu en intégralité). Le reste de l'ingestion (superfans, contrôle d'accès sémantique, bornes voler/ignorer) est noté en file pour la **Mission 2 Ryan** — pas intégré ici.

**H-02-A1-1 — Fin de la file de merge (point 5).** À l'échelle agent : **pas de verrou global, investir dans le post-merge** (pas de merge queue). Notre arbitrage `enforce_admins=false` est **renforcé par l'argument** (doctrine + échelle agent : un verrou global = un goulot). H-02 spécifie désormais la **vérification post-merge** : reçus R10 émis/vérifiés après merge + vérification continue (heartbeat) — pas seulement des checks pré-merge. **Résolution agentique des conflits** : Jules rebase/fixe (Jules = celui qui continue de toucher à Aspace) plutôt que blocage humain. La CI bloquante actuelle suffit — **aucune merge queue humaine supplémentaire**. Hygiène : CI et agents **API-first + sparse checkouts** — jamais un clone de 1,6 Go pour poser une question (les ~35 branches orphelines = « l'état global partagé » : la doctrine « branches = état coûteux » s'applique en hygiène).

**H-02-A1-2 — « Dire non à Claude » : le chaînon manquant entre Clara et le merge (point 4).** La revue d'intention existe au **design-time** (Clara = autorité design unique — déjà fait). Le trou identifié : au **review-time**, merges en 1–16 min par l'owner seul, aucune revue d'intention. **Décision : pour les atterrissages de la chaîne, le chaînon manquant = le check `r10-receipt` au merge.** Le reçu porte la chaîne dispatch Nardole → design Clara signé → exécution → reçu Graham : le check au merge-time **est** la revue d'intention au review-time — sans gate humain ajouté, sans friction. Pour les PRs agents ordinaires : jugement de l'owner au merge + vérification post-merge (§A1-1). Qui dit non à Jules aujourd'hui ? Le protocole : les PRs Jules sont des PRs agents ordinaires (owner) ; les atterrissages issus de dispatches passent par le reçu — la chaîne de responsabilité est nommée.

**Tests hold-out ajoutés :** H-H02-A1-1 (post-merge spécifié : un atterrissage de la chaîne a une vérification post-merge — reçu vérifié + check continu) ; H-H02-A1-2 (conflit seedé → chemin de résolution agentique documenté et utilisé, aucun blocage humain) ; H-H02-A1-3 (le check `r10-receipt` au merge est identifié comme la revue d'intention au review-time pour les atterrissages de la chaîne) ; H-H02-A1-4 (aucune file de merge globale introduite ; `enforce_admins` reste false).

*Fin de l'addendum H-02-A1. Signature Clara apposée — PRÊT, dispatchable par Nardole avec H-02 après validation Doctors.*

---

## ADDENDUM H-02-A2 — Nommer la porte : staging → vérification d'intention → prod (Dette 2, Cole Medin)

**Date :** 2026-10-19 — **Signé Clara** (addendum au plan H-02 signé + A1 ; le corps est intact).
**Source :** ingestion Cole Medin de Bill (`~/workspace/architecture-compagnons/ingestion-cole-medin-software-factory.md`, §4 dette D2) — **converge avec l'ingestion Scion** (même trou identifié des deux sources : revue d'intention au design-time, rien au review-time ; la station du merge est le point faible commun).

**Décisions design (autorité Clara) :**

**H-02-A2-1 — La porte est nommée : staging → vérification d'intention → prod. Jamais direct en prod.** Dans nos termes :
- **Staging** = la PR (branche) — le changement est assemblé et visible, pas mergé. Nos PRs *sont* le staging ; le protocole les nomme comme tel dans `CONTRIBUTING.md` (aucune infra nouvelle).
- **Vérification d'intention** = la station nommée à la porte : atterrissages de la chaîne → check `r10-receipt` (porte la signature de design Clara — H-02-A1-2) ; PRs agents ordinaires → jugement de l'owner **enregistré** (corps de PR / message de merge). Le vérificateur est nommé par classe.
- **Prod** = `main` après merge.
- **Traverser sans la station de vérification = violation de protocole** — le « jamais direct en prod » de Cole, écrit.

**H-02-A2-2 — H-02 porte les deux sources.** Scion : pas de verrou global, tests post-merge (H-02-A1-1) — la porte se traverse par la vérification, pas par un cadenas. Cole : staging → vérification d'intention → prod (le présent addendum). Les deux stations sont distinctes : la porte dit « l'intention est vérifiée », le post-merge dit « le vivant est vérifié ».

**Tests hold-out ajoutés :** H-H02-A2-1 (la porte est nommée dans `CONTRIBUTING.md` — staging → vérification d'intention → prod ; un chemin qui saute la station échoue au contrôle de protocole) ; H-H02-A2-2 (vérificateur nommé par classe : atterrissage de la chaîne sans check `r10-receipt` au merge = violation ; PR ordinaire sans jugement owner enregistré = violation).

*Fin de l'addendum H-02-A2. Signature Clara apposée — PRÊT, dispatchable par Nardole avec H-02 après validation Doctors.*

---

## ADDENDUM H-02-A3 — Doctrine de vérification : traces, pas pensées (ingestion références forks)

**Date :** 2026-10-19 — **Signé Clara** (addendum au plan H-02 signé + A1 + A2 ; le corps est intact).
**Source :** ingestion références V5 de Bill (`~/workspace/architecture-compagnons/ingestion-references-v5-forks.md`, §4) — Eligible Receiver (la chaîne dessinée *avant* la crise), NCM, HybridAgents (raisonnement latent ; réduction de tokens 35–55 % — candidat fork aligné L00).

**H-02-A3-1 — Formulation (à écrire dans les designs).** **« Nous n'auditons pas les pensées, nous auditons les traces. »** Si la pensée des modèles devient illisible (critique Barnett ; raisonnement latent type HybridAgents — dont la « transparence » revendiquée reste une question ouverte : inspectable par qui, à quel coût), notre doctrine **ne perd rien** :
- **R10 vérifie des actes** (reçus : diff, tests, preuves horodatées) — pas des intentions pensées.
- **Les hold-outs vérifient le comportement** — des résultats contre des scénarios, indifférents au format interne de la pensée.
- **Producer ≠ validator est structurel** (organigramme), pas cognitif.
- **La chaîne signe l'intention en amont** (Clara — lisible, humaine) ; **Graham reçut l'exécution en aval** (faits). Le milieu — la pensée du modèle — peut devenir latent **sans casser la chaîne**. La confiance vient de la structure (chaîne + traces), jamais de la surveillance du raisonnement — la leçon d'Eligible Receiver, inversée et tenue.

**H-02-A3-2 — Garde-fou 1 : les reçus sont produits par le HARNESS, jamais par le modèle.** Un modèle qui s'auto-reçute produit un reçu faux — c'est l'échec GPR de Cole (« l'agent a dit done » sans avoir touché au repo). **Décision : le check `r10-receipt` vérifie la provenance — émetteur = harness (CI/tooling), pas une sortie du modèle.** Un reçu auto-rapporté = reçu invalide.

**H-02-A3-3 — Garde-fou 2 : les critères hold-out sont ROTATIFS.** Des agents qui apprennent finissent par inférer des critères statiques. **Décision : un sous-ensemble des critères est tenu secret du builder et tourne entre les runs** (extension du protocole aveugle D-N023) ; le jeu en vigueur pour un run est journalisé **sous scellé** et ouvert à la vérification. Un jeu identique d'un run à l'autre = violation de doctrine.

**H-02-A3-4 — Champ d'application.** La formulation et les deux garde-fous sont **contraignants pour tous les designs forks et V5 à venir** (à reprendre au design-time de chaque plan fork), et s'appliquent dès maintenant au protocole H-02.

**Tests hold-out ajoutés :** H-H02-A3-1 (reçu auto-rapporté par le modèle seedé → check `r10-receipt` le **rejette** : provenance harness exigée) ; H-H02-A3-2 (deux runs consécutifs de la même classe de mission → sous-ensembles de critères **différents**, rotation journalisée sous scellé) ; H-H02-A3-3 (la formulation est présente dans le protocole — `CONTRIBUTING.md` / section vérification : doctrine écrite, pas orale).

*Fin de l'addendum H-02-A3. Signature Clara apposée — PRÊT, dispatchable par Nardole avec H-02 après validation Doctors.*
