# D-01 — Plan borné : Lot D — Registre honnête (correction du registre des éléments enregistrés)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne lore : Bill → Clara → Nardole → validation S2 → exécution) — 2026-10-17
**Source :** dispatch Rick (S1) ; découverte Bill typée ; PRD-D (Conseil S2) ; BEFORE-YOU-BUILD.md §2 Lot D
**Arbitrages Rick intégrés (tranchés, non négociables) :**
1. **Effectifs paramétrés, jamais codés en dur.** L'état FINAL réel (bilan `items-recuperes.md`) : **82** « texte dans la transcription » / **10** « récupéré via Sources » (54, 56, 57, 60, 61, 62, 63, 66, 68, 69) / **0** « localisé » / **6** « non récupéré » (55, 64, 65, 67, 70, 71). Somme 98 ✓. Les chiffres 82/1/3/12 du brief S1 et de PRD-D §2/§4.4 sont **supersédés** — ne jamais les utiliser.
2. **Première étape obligatoire de l'exécution : relire le bilan FINAL `items-recuperes.md`.** Jamais le brief, jamais PRD-D §2/§4.4.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara — tranchées ici, ne remontent pas)

1. **Vocabulaire fermé à 4 valeurs exactes** (PRD-D §3) pour la colonne « État du texte » : `texte dans la transcription` / `récupéré via Sources` / `localisé, extraction à reprendre` / `non récupéré`. Aucune 5e valeur, aucune variante orthographique — le script les parse en littéral.
2. **Les 3 affirmations fausses (D1) sont remplacées, pas commentées :**
   - `elements-enregistres.md` § « Vérification individuelle » (« 98/98 = doublons… 0 exception » + implicite de couverture intégrale) ;
   - `elements-enregistres.md` § « Texte intégral » (fin) (« présent dans les transcriptions des conversations sources ») ;
   - `MANIFESTE.md` L40 (« Le texte intégral de chaque élément est présent dans la transcription de sa conversation source »).
   
   Remplacement : description exacte de la couverture réelle **avec les numéros d'items concernés** (les 10 récupérés via Sources avec renvoi, les 6 non récupérés avec renvoi lot B). La fausse version ne subsiste nulle part (ni en commentaire).
3. **Le décompte est un calcul, pas une estimation** : `n1+n2+n3+n4 == 98`, vérifié par script, figurant en tête du registre. Toute incohérence **bloque la livraison** (PRD-D §8).
4. **Règle anti-faux-positif** : en cas de doute sur un item → `non récupéré` avec renvoi, jamais `texte dans la transcription` par défaut. Si la transcription source est elle-même « partiel » sur le passage : `non récupéré` avec renvoi croisé.
5. **Miroir Drive EN DERNIER, après vert local** : aucune écriture Drive avant le script au vert ; vérification post-écriture (contenu identique). Écriture uniquement dans le dossier d'extraction.
6. **Ré-ouverture prévue** : si un relais A0/B2 arrive après livraison, le registre est rouvert et le décompte re-réconcilié (PRD-D §8) — D n'est pas figé contre B2. Le paramétrage (§0 arbitrages) rend cette réouverture mécanique.

## 1. Bornes (scope strict)

**IN :**
- Correction des 3 affirmations fausses (D1) aux 3 emplacements.
- Colonne « État du texte » (4 valeurs exactes) pour les items 1–98, renvois valides (C1).
- Script `somme-98` selon spéc D5 : parse la colonne, assertion `n1+n2+n3+n4==98` (échec bruyant, bloque livraison), contrôles croisés (récupéré→section `items-recuperes.md` non vide ; non récupéré→doc échec lot B ; localisé→détails lot B), anti-faux-positif, re-jouable.
- Décompte réconcilié en tête du registre.
- Miroir Drive en dernier, après vert local (C5).

**OUT :**
- Aucune nouvelle tentative de récupération (lot B).
- Aucune modification des transcriptions elles-mêmes.
- Aucune écriture Drive hors dossier d'extraction.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — `tools/somme-98.py` (script de vérification, re-jouable)**
- Input : `elements-enregistres.md`. Parse la table items 2–98 (+ item 1) et la colonne « État du texte ».
- Vocabulaire fermé : les 4 valeurs exactes en littéral ; toute autre valeur → échec bruyant.
- Assertions : `n1+n2+n3+n4 == 98` (échec → exit 1 + message explicite, **bloque la livraison**).
- Contrôles croisés : chaque `récupéré via Sources` → ancre de section existante et non vide dans `items-recuperes.md` ; chaque `non récupéré` → renvoi vers la doc d'échec lot B ; chaque `localisé` → renvoi vers détails lot B.
- Anti-faux-positif : aucun `texte dans la transcription` sur un item dont la transcription source est marquée « partiel » sur le passage (liste des partiels en entrée du script).
- Aucun effectif codé en dur : le script compte le réel ; les 82/10/0/6 ne figurent que comme référence commentée.
- Sortie : rapport (n1, n2, n3, n4, renvois vérifiés) + exit code.

**Système 2 — `elements-enregistres.md` corrigé (le registre)**
- En-tête : décompte réconcilié **calculé** (n1/n2/n3/n4 + somme 98), date de calcul, référence au bilan FINAL lu.
- Table items 2–98 : colonne « État du texte » (4 valeurs) + colonne/notes de renvoi (ancre `items-recuperes.md` | doc lot B).
- Item 1 : texte intégral inline (inchangé) + état `texte dans la transcription`.
- Affirmations fausses remplacées (§0.2).

**Système 3 — `MANIFESTE.md` corrigé (L40)**
- Passage remplacé par la description exacte de la couverture réelle (avec numéros d'items).

**Flux de données :** `items-recuperes.md` FINAL (source de vérité, **étape 0 obligatoire**) → correction registre (P1–P2) → `somme-98.py` au vert (P3) → décompte en tête (P4) → miroir Drive (P5, en dernier).

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Bilan FINAL (OBLIGATOIRE, première étape)** | Relire `items-recuperes.md` FINAL ; établir les effectifs réels (référence : 82/10/0/6). Interdit : brief S1, PRD-D §2/§4.4 | Effectifs établis et notés |
| **P1 — D1** | Remplacer les 3 affirmations fausses (description exacte + numéros d'items) | H-D1 |
| **P2 — Colonne d'état** | Renseigner « État du texte » items 1–98 (4 valeurs exactes) + renvois valides | H-D2, H-D4 |
| **P3 — Script** | Écrire `tools/somme-98.py` (spéc D5), le faire passer au vert ; test négatif (corruption seedée → échec bruyant) | H-D3, H-D5, H-D6 |
| **P4 — Décompte** | Écrire le décompte réconcilié calculé en tête du registre | H-D3 |
| **P5 — Miroir Drive** | **En dernier**, après vert local ; vérification post-écriture ; dossier d'extraction uniquement | H-D8 |
| **P6 — Validation** | Revue S2 (Doctors) → Nardole dispatche la validation | Tous verts |

**Règle d'exécution :** phases séquentielles, un seul exécutant. `OWNER_STAND_DOWN=1` arrête tout.

## 4. Tests hold-out (définis AVANT exécution — validation aveugle)

| ID | Vérifie | Seuil |
|---|---|---|
| **H-D1** | Les 3 affirmations fausses sont corrigées | grep des formulations fausses → vide ; nouvelles formulations décrivent la couverture réelle avec numéros d'items |
| **H-D2** | Colonne « État du texte » complète, vocabulaire fermé | 98/98 items renseignés ; 0 valeur hors des 4 exactes |
| **H-D3** | Somme-98 vert | `n1+n2+n3+n4 == 98`, exit 0 ; corruption seedée → exit 1 bruyant (bloque livraison) |
| **H-D4** | Contrôles croisés valides | chaque `récupéré via Sources` → section non vide de `items-recuperes.md` ; chaque `non récupéré` → doc échec lot B ; chaque `localisé` → détails lot B |
| **H-D5** | Anti-faux-positif | aucun `texte dans la transcription` sur passage « partiel » ; doute → `non récupéré` |
| **H-D6** | Paramétrage (arbitrage Rick 1) | 0 effectif codé en dur (script + registre) ; le script lit le réel |
| **H-D7** | Étape 0 respectée (arbitrage Rick 1) | la première action tracée de l'exécution est la relecture du bilan FINAL (ni brief, ni PRD-D §2/§4.4) |
| **H-D8** | Miroir Drive en dernier (C5) | écriture Drive postérieure au vert local ; contenu post-miroir identique au local ; dossier d'extraction uniquement |

## 5. Critères C1–C5 (Bill)

- **C1** : colonne « État du texte » à 4 valeurs exactes (PRD-D §3) pour items 1–98, renvois valides.
- **C2** : les 3 affirmations fausses (D1) corrigées — couverture réelle décrite avec numéros d'items.
- **C3** : décompte réconcilié `n1+n2+n3+n4 == 98`, vérifié par script, en tête du registre.
- **C4** : contrôles croisés valides (cf. H-D4).
- **C5** : miroir Drive EN DERNIER, après vert local, vérifié post-écriture.

## 6. Risques R1–R4

- **R1 — Dérive des effectifs** (relais A0/B2 rouvre le registre, PRD-D §8). → Paramétrage + procédure de re-réconciliation (P0→P4 rejoués).
- **R2 — Faux positif** « texte dans la transcription ». → Règle doute→`non récupéré` + contrôle script (H-D5).
- **R3 — Renvois cassés** (ancres `items-recuperes.md`). → Vérification d'ancres par le script (H-D4).
- **R4 — Miroir Drive divergent ou prématuré**. → Miroir en dernier + vérification post-écriture (H-D8).

## 7. Séquence d'exécution (pas un swarm)

```
P0 (bilan FINAL — OBLIGATOIRE) → P1 (D1) → H-D1 → P2 (colonne) → H-D2/H-D4
  → P3 (script) → H-D3/H-D5/H-D6 → P4 (décompte) → P5 (miroir Drive, en dernier) → H-D8
  → P6 (revue S2 → validation Nardole)
```

Tout écart → **BLOQUÉ** avec raison + qui débloque. Pas de contournement silencieux.

*Fin du plan D-01. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation S2.*
