# Évaluation anti-sycophanie — M-14

**Mission :** Bill (holon DISCOVER) — M-14 du registre, dispatch D-N018 (Nardole, AGORA).
**Date :** 2026-10-09 ~16:45 EDT · **Statut :** ÉVALUÉ — verdict ADAPTER, mission typée pour Clara ci-dessous.
**Limite de méthode :** les textes intégraux n'ont pas été récupérés (ar5iv redirige vers les pages arXiv abs) ; l'évaluation repose sur les abstracts officiels et les mécanismes déclarés — signalé, pas comblé.

---

## 1 — Résumés fidèles

### 1.1 PlurPO — « Mitigating Social Sycophancy via Pluralistic Preference Optimization » (arXiv:2610.02568)
- **Lien :** https://arxiv.org/abs/2610.02568 · soumis 1 oct. 2026, révisé 5 oct. 2026 (v2).
- **Auteurs :** Stephane Hatgis-Kessell, Myra Cheng, Xiaoxuan Hou, Qian Hu, Rahul Gupta, Natasha Jaques, Emma Brunskill.
- **Thèse :** la sycophanie sociale (conseils personnels sans vérité terrain) vient en partie de ce que les LM se centrent excessivement sur l'utilisateur et ignorent les autres parties prenantes affectées par son comportement.
- **Mécanisme :** face à des descriptions de conflits interpersonnels, le LM identifie et simule les parties prenantes pertinentes, puis est **entraîné** (optimisation de préférences) à préférer et générer des réponses acceptables pour toutes les parties prenantes. N'utilise que des signaux que le modèle produit sur ses propres sorties — **aucun label de vérité terrain**.
- **Résultats clés :** réduction substantielle de la sycophanie sociale sur 4 jeux de données et 4 familles de modèles vs méthodes antérieures ; sur les déclarations d'intention de nuire, taux d'approbation réduit de **89 %** en moyenne (4 modèles) ; sur les conseils généraux, l'écart au taux d'approbation humain passe de **17,8 % à 8,0 %** (plus de moitié comblé) ; le jeu de préférences construit pour un modèle 8B se transfère efficacement à un 32B.
- **Limites (déclarées et structurelles) :** méthode de **post-training** (fine-tuning), pas un protocole d'inférence ; domaine = **conseils sociaux/interpersonnels**, pas la revue technique ; la « sycophanie » traitée = approuver le comportement de l'utilisateur, pas l'inflation de notes d'évaluation.

### 1.2 Protocole de débat instance-optimal — « How to Have a Sensitive Debate: An Instance-Optimal Protocol for AI Debate » (arXiv:2610.02557)
- **Lien :** https://arxiv.org/abs/2610.02557 · soumis 1 oct. 2026.
- **Auteurs :** Jiawei Li, Zhiyang Xun, Lijie Chen, Jonah Brown-Cohen.
- **Thèse :** pour la supervision d'IA qui dépassent l'expert humain, le débat entre deux IA puissantes décompose les questions complexes en affirmations simples jugeables. Nouveau protocole pour les problèmes à **décompositions stables** en sous-problèmes.
- **Mécanisme (théorique) :** garanties de correction au **pire cas** (vs cas moyen) ; l'honnêteté+correction est un **équilibre en stratégie dominante** pour les deux débatteurs (vs équilibre de Stackelberg) ; **bornes inférieures boîte-noire** prouvant l'optimalité instance-par-instance — aucun protocole de cette classe ne peut faire mieux à requêtes de jugement humain égales. Relie les décompositions stables à la sensibilité par blocs fractionnaire (complexité de requêtes).
- **Résultats clés :** ce sont des **preuves**, pas des expériences — pas de résultats empiriques dans l'abstract, pas de protocole implémentable livré pour la revue de code.
- **Limites :** contribution théorique (théorie de la complexité, équilibres) ; la classe couverte (décompositions stables) ne recouvre pas proprement la revue de PR ; « instance-optimal » ne donne aucune procédure concrète à coder.

---

## 2 — Évaluation d'intégration au Grep-Loop (M-03)

**Rappel M-03 :** un reviewer indépendant (type Greptile) note le travail /5 et renvoie l'agent en boucle Build → Prove → Ship jusqu'à 5/5. Le risque visé : le reviewer qui **gonfle ses notes** (5/5 complaisant) — sycophanie d'évaluation / faux positifs — pas la sycophanie sociale.

### 2.1 PlurPO face au Grep-Loop
- **Inadéquation de couche :** PlurPO est une méthode d'entraînement ; le Grep-Loop est un protocole d'inférence. Adopter PlurPO = fine-tuner le modèle reviewer sur des jeux de préférences à parties prenantes — lourd, indirect, et hors domaine (conflits interpersonnels vs revue de code).
- **Inadéquation de cible :** la sycophanie du reviewer n'est pas « approuver l'utilisateur » mais « noter haut pour faire plaisir à l'opérateur / clore la boucle » — du reward hacking d'évaluation, mieux traité par rubriques, critères cachés et revue adverse.
- **Principe récupérable :** la pluralité des perspectives. Un reviewer qui ne juge que « est-ce que ça a l'air bien » sycophante ; un reviewer tenu de noter **du point de vue du mainteneur futur, de l'auditeur sécurité et de l'utilisateur final** a trois fois moins de place pour la complaisance. C'est un enrichissement de rubrique, pas un fine-tuning.

### 2.2 Débat instance-optimal face au Grep-Loop
- **Structure récupérable :** l'échange adverse (défenseur du PR vs challenger + juge) au lieu d'une note unique. C'est exactement la « validation adverse » de M-02 — le débat est son mécanisme naturel, et le hold-out aux critères cachés en est le terrain.
- **Non récupérable tel quel :** le protocole théorique (preuves d'optimalité, équilibres) ne se code pas ; aucune garantie empirique sur la revue de code.
- **Mapping Knox :** reviewer /5 unique = Inner loop (rapide, frugal) ; débat adverse = Outer loop (lourd, post-PR). Les deux coexistent, à des coûts différents.

### 2.3 Où brancher, coût/bénéfice, risques
- **Où brancher :** (a) rubrique du reviewer /5 enrichie de 3 perspectives parties prenantes (principe PlurPO) ; (b) couche adverse : challenger qui attaque le PR, juge qui tranche, critères cachés du hold-out (structure du débat, arrimée à M-02/D-N022).
- **Bénéfice :** fait chuter les faux 5/5 ; rend l'overfitting aux critères connus du reviewer beaucoup plus coûteux (le challenger ne connaît pas les critères cachés non plus — il attaque réellement).
- **Coût :** le débat multiplie le coût d'inférence par review (×2–3) — à réserver à l'Outer loop, pas à chaque itération de boucle.
- **Risques :** latence ajoutée à la boucle ; collusion possible entre débatteurs (même modèle, mêmes biais) — d'où l'importance des critères cachés et d'un juge indépendant ; un fine-tuning PlurPO dégraderait la calibration technique du reviewer (domaine shift) — raison de plus de l'écarter comme méthode.

---

## 3 — Verdict : **ADAPTER**

**Ni l'une ni l'autre des deux méthodes n'est adoptée telle quelle :**
- **PlurPO comme méthode : ÉCARTÉ** — mauvaise couche (entraînement vs inférence), mauvais domaine (social vs revue technique), levier disproportionné.
- **Protocole instance-optimal comme implémentation : ÉCARTÉ** — théorique, non actionable, sans validation empirique sur notre tâche.

**Adaptés, les deux principes :**
1. **Pluralité des parties prenantes (de PlurPO)** → rubrique du reviewer : toute note /5 doit être défendue depuis trois perspectives (mainteneur, auditeur, utilisateur).
2. **Débat adverse (du papier débat)** → couche de validation adverse : défenseur vs challenger + juge, branchée sur le hold-out aux critères cachés (M-02).

---

## 4 — Mission typée pour Clara (si ADAPTER — c'est le cas)

### M-14-C — Couche de validation adverse du Grep-Loop
- **Objectif :** le reviewer ne peut plus donner un 5/5 complaisant : sa note est contestée par un challenger adverse et jugée contre des critères cachés.
- **Dedans :** structure débatteur (défenseur du PR vs challenger adverse + juge indépendant) ; rubrique /5 enrichie des trois perspectives parties prenantes (mainteneur futur, auditeur sécurité, utilisateur final) ; critères cachés du hold-out (arrimage M-02 / D-N022) ; mapping Inner (reviewer /5 rapide, chaque itération) / Outer (débat adverse lourd, post-PR) ; mesure et borne du surcoût d'inférence par review.
- **Dehors :** le fine-tuning PlurPO du reviewer (écarté, §3) ; l'implémentation littérale du protocole instance-optimal (écarté, §3) ; le contenu des reçus métier (owners des domaines).
- **Reçu :** un PR notoirement faible obtient < 5/5 après débat (cas adversarial documenté) ; au moins un faux 5/5 historique est re-noté à la baisse par la nouvelle structure ; le surcoût d'inférence par review est mesuré, borné et documenté ; la collusion débatteurs est traitée (juge indépendant + critères cachés).
- **Voie :** Clara (design), en lien avec D-N022 (M-02, import/validation) et M-03 (standard de preuve).
- **Sources :** la présente évaluation ; arXiv:2610.02568 ; arXiv:2610.02557 ; REGISTRE-INSPIRATIONS.md (M-02, M-03).
