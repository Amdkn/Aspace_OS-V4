# E-01 — Plan borné : Lot E — Extraction IPBD (Intentions, Promesses, Besoins, Décisions)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne lore : Bill → Clara → Nardole → validation S2 → exécution) — 2026-10-17
**Source :** dispatch Rick (S1) ; découverte Bill typée ; PRD-E (Conseil S2) ; rapport matière `ipbd-qualification-matiere.md` (159 lignes, 33 transcriptions exploitables)
**Arbitrage Rick intégré (tranché, non négociable) :** **design MAINTENANT sur le corpus disponible, exécution APRÈS lot C partie 1/2.** La vague-4 n'a que 2/11 exploitables (08, 09) ; 6 conversations (01–06) en cours chez S3. Le design porte sur les 33 transcriptions disponibles ; l'exécution (dispatch Nardole) attend le corpus complet. **Pas d'extraction partielle avec réouverture — un seul passage, sur corpus complet.**
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara — tranchées ici, ne remontent pas)

1. **Le corpus est un paramètre d'exécution, pas du design.** Le design définit la méthode sur les 33 transcriptions disponibles ; l'exécution commence par l'établissement du **manifeste de corpus complet** (après lot C 1/2, incluant les 6 conversations S3 01–06). **Aucune extraction avant manifeste complet et vérifié** (H-E1).
2. **Un seul passage.** L'extraction s'exécute une fois, sur corpus complet. Si le relais B2 arrive après : rattrapage documenté (PRD-E §9), jamais de ré-extraction silencieuse ni de réouverture.
3. **Ordre de balayage : les 9 fortes en priorité** (v1/01, 02, 18, 19, 20, 21, 22 + v3/01 + v4/09 — marqueurs explicites d'abord), **puis balayage complet des 17 faibles/nulles sans omission silencieuse** (C4) : chaque fichier du manifeste a un statut (`0 entrée` ou `N entrées`), aucun fichier ignoré sans mention.
4. **Découpage des directives impératives longues (E5)** : mode dominant du corpus — chaque message-mission embarque 5–15 intentions/décisions implicites. Règle : **1 énoncé = 1 entrée** ; découpage documenté dans l'entrée (référence au message source).
5. **P (promesses) non forcé (E4)** : quasi absent en formulation explicite — le livrable **constate** la rareté (ou les formulations indirectes trouvées), il ne l'invente pas.
6. **Thèmes émergents (E6)** : pas de grille imposée. Les 9 thèmes du rapport matière sont le **point de départ documenté**, pas une grille fermée — le livrable justifie tout thème ajouté ou retiré.
7. **Cas limites E7** (protocole) :
   - v4/08 : attribution quasi nulle — **seules les 1–2 phrases de cadrage** du Capitaine sont exploitables ;
   - citations de traces d'autres sessions (v1/02, v1/18) : **vérification une par une**, jamais d'attribution par défaut ;
   - troncation v1 : intentions antérieures au 28 sept. = hors corpus = hors extraction (mentionné, pas deviné) ;
   - « go » bruité (ex. « GO Listener ») → **« attribution incertaine »**, jamais deviné.
8. **Attribution à 3 statuts** : `citation vérifiée` / `attribution incertaine` / `non établi`. En cas de doute sur un champ : `non établi` plutôt qu'une valeur devinée (PRD-E §8).
9. **Traçabilité bidirectionnelle des corrections (C2)** : tout énoncé postérieur qui corrige/précise/annule pointe vers l'origine **et réciproquement** (index des corrections).
10. **Énoncés des IA = contexte seulement** (OUT Rick) : `items-recuperes.md` est marginal pour IPBD (réponses IA, pas paroles du Capitaine — rapport matière §1) — balayé pour relations/contexte, jamais comme source d'énoncés.

## 1. Bornes (scope strict)

**IN :**
- Rapport matière `ipbd-qualification-matiere.md` comme base de design (159 lignes).
- Corpus de design : 33 transcriptions exploitables ; corpus d'exécution : complet après lot C 1/2 (manifeste vérifié).
- 9 fortes en priorité, 17 faibles/nulles balayées sans omission silencieuse (C4).
- Volume cible : 150–220 candidats bruts → **80–140 entrées finales** (fourchette Bill) ; I domine, D second, B diffus, P quasi absent (E4).
- Entrées à 5 champs (PRD-E §3) : citation exacte entre guillemets / conversation+URL / emplacement+date / corrections / relations. Reformulations marquées « reformulation », jamais sous guillemets.
- Corrections bidirectionnelles (C2), thèmes émergents E6, cas limites E7.
- Dépôt `ipbd/` (README méthode+décompte + 1 fichier/thème) + miroir Drive (dossier d'extraction uniquement) + note vocale MP3 FR.

**OUT :**
- Énoncés des IA (contexte/relations seulement).
- Interprétation stratégique (travail de Bill–Tilly).
- Paraphrases non marquées (toute reformulation porte « reformulation »).

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Manifeste de corpus (établi à l'exécution, après lot C 1/2)**
- Fichier : `~/workspace/chatgpt-extraction/ipbd/corpus-manifest.md` (ou `.json`).
- Contenu : liste exhaustive des fichiers du corpus complet (vagues 1–4 + items-récupérés), chacun avec statut : `exploitable` / `fiche` (non transcrit) / `réserve` (attribution douteuse, ex. v4/08).
- Vérification : les 6 conversations S3 (01–06) présentes ; les 3 fiches vague-4 (07, 10, 11) marquées `fiche` ; total rapproché du lot C.
- **Gate : aucune extraction avant manifeste complet et vérifié (H-E1).**

**Système 2 — Grille d'extraction (méthode)**
- Les 5 champs PRD-E §3 + statut d'attribution (`citation vérifiée` / `attribution incertaine` / `non établi`).
- Marqueurs : explicites (I/P/B/D) + doux (« je vais », « je reprends », « il faut »…) + directives impératives (mode dominant).
- Règle de découpage E5 : 1 énoncé = 1 entrée, référence au message source.
- Protocole E7 (§0.7).

**Système 3 — Dépôt `~/workspace/chatgpt-extraction/ipbd/`**
- `README.md` : méthode + décompte (total entrées, par thème, par type I/P/B/D, distinction `citation vérifiée` / `attribution incertaine`) + statut du corpus (manifeste) + limites connues (troncation, fiches).
- `<theme>.md` : un fichier par thème émergent (E6) — les 9 du rapport comme point de départ.
- Index des corrections (C2) : bidirectionnel.

**Système 4 — Livraison**
- Miroir Drive : dossier `ipbd/` **dans le dossier d'extraction uniquement**, après contrôles verts.
- Note vocale MP3 FR de synthèse : panorama des thèmes + décisions majeures, sans paraphrase abusive (standing request).

**Flux de données :** lot C 1/2 livré → manifeste de corpus complet (P0) → extraction un seul passage : 9 fortes (P1) puis balayage complet (P2) → découpage/corrections/thèmes (P3) → cas limites (P4) → dépôt + contrôles (P5) → miroir + MP3 (P6) → validation S2 (P7).

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Manifeste (OBLIGATOIRE, première étape d'exécution)** | Après lot C 1/2 : établir le manifeste de corpus complet ; vérifier les 6 conversations S3 (01–06) intégrées ; marquer fiches et réserves | H-E1 (aucune extraction avant) |
| **P1 — 9 fortes** | Extraction prioritaire : marqueurs explicites d'abord, puis découpage E5 | H-E2, H-E3 |
| **P2 — Balayage complet** | Les 17 faibles/nulles + reste du corpus, sans omission silencieuse (C4) : chaque fichier a un statut | H-E4 |
| **P3 — Structuration** | Découpage E5 finalisé, corrections bidirectionnelles (C2), thèmes émergents (E6) | H-E5, H-E9 |
| **P4 — Cas limites** | Protocole E7 : v4/08, citations d'autres sessions, troncation, « go » bruité | H-E6 |
| **P5 — Dépôt + contrôles** | `ipbd/` (README + thèmes), contrôles hold-out H-E2..H-E10 | Tous verts |
| **P6 — Livraison** | Miroir Drive (dossier d'extraction uniquement) + note vocale MP3 FR | H-E11 |
| **P7 — Validation** | Revue S2 (Doctors) → Nardole dispatche la validation | Tous verts |

**Règle d'exécution :** phases séquentielles, un seul exécutant. Un seul passage sur corpus complet. `OWNER_STAND_DOWN=1` arrête tout.

## 4. Tests hold-out (définis AVANT exécution — validation aveugle)

| ID | Vérifie | Seuil |
|---|---|---|
| **H-E1** | Manifeste de corpus complet avant extraction | manifeste vérifié (6 conversations S3 incluses, fiches marquées) ; 0 extraction avant |
| **H-E2** | 5 champs par entrée | chaque entrée : citation exacte + conversation/URL + emplacement/date + corrections + relations ; `non établi` si doute, jamais deviné |
| **H-E3** | Guillemets = mots exacts | échantillon de citations revérifié contre transcriptions : 0 paraphrase sous guillemets ; reformulations marquées « reformulation » |
| **H-E4** | Aucune omission silencieuse (C4) | chaque fichier du manifeste a un statut (`0` ou `N` entrées) ; les 17 faibles/nulles toutes couvertes |
| **H-E5** | Traçabilité bidirectionnelle (C2) | chaque correction pointe vers l'origine et réciproquement (index vérifié) |
| **H-E6** | Cas limites E7 traités | v4/08 : seules phrases de cadrage ; citations d'autres sessions vérifiées une par une ; « go » bruité → `attribution incertaine` |
| **H-E7** | P non forcé (E4) | si P quasi absent : constat écrit, 0 promesse inventée |
| **H-E8** | Volume plausible | 80–140 entrées finales ; hors fourchette → justification écrite (pas d'échec automatique) |
| **H-E9** | Thèmes émergents (E6) | pas de grille imposée ; ajouts/retraits vs les 9 du rapport justifiés |
| **H-E10** | Un seul passage | aucune extraction partielle avant corpus complet ; relais B2 ultérieur → rattrapage documenté (PRD-E §9), pas de ré-extraction silencieuse |
| **H-E11** | Livraison complète | `ipbd/` + miroir Drive (dossier d'extraction uniquement) + note vocale MP3 FR |

## 5. Risques

- **R1 — Corpus incomplet au lancement** (6 conversations S3 manquantes). → H-E1 : manifeste vérifié avant tout ; l'exécution attend lot C 1/2 (arbitrage Rick).
- **R2 — Attribution erronée** (v4/08, citations d'autres sessions, « go » bruité). → Protocole E7 + statuts d'attribution (H-E6) ; jamais deviné.
- **R3 — Paraphrase sous guillemets** (le risque qualité n°1 du lot). → H-E3 : échantillon revérifié ; règle « recopié, pas reconstruit de mémoire » (PRD-E §8).
- **R4 — Extraction partielle avec réouverture** (l'anti-pattern à éviter). → H-E10 : un seul passage ; conception sur 33, exécution sur complet.
- **R5 — Grille de thèmes imposée** (tuer l'émergence). → H-E9 : les 9 thèmes sont un point de départ, pas une grille fermée.

## 6. Séquence d'exécution (pas un swarm)

```
[lot C 1/2 livré] → P0 (manifeste — OBLIGATOIRE) → H-E1 → P1 (9 fortes) → P2 (balayage complet, C4) → H-E4
  → P3 (découpage E5, C2, E6) → H-E5/H-E9 → P4 (E7) → H-E6 → P5 (dépôt) → H-E2/H-E3/H-E7/H-E8/H-E10
  → P6 (miroir + MP3) → H-E11 → P7 (revue S2 → validation Nardole)
```

Tout écart → **BLOQUÉ** avec raison + qui débloque. Pas de contournement silencieux. Pas d'extraction partielle.

*Fin du plan E-01. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation S2 (exécution après lot C 1/2).*
