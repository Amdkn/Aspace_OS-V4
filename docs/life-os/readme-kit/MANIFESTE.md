# Kit README — Chaîne A3 Spock → Projections fractales → B1 de Coacher

Source : analyse profonde de `Amdkn/Aspace_OS_V3`, arborescence `20_Life_OS`
(2026-10-08). En attente de correction via le brainstorming Gemini de Capitaine.

## La chaîne

```
02_Areas_Spock (PARA A3 — responsabilités continues, jamais terminées)
  └─ 8 A3 Domaines (A2 Discovery / ZORA — Life Wheel)
       ├─ LD01 Book · LD02 Saru · LD03 Culber · LD04 Tilly
       ├─ LD05 Stamets · LD06 Burnham · LD07 Reno · LD08 Georgiou
       └─ 8 projections fractales par A3 (sous-domaines business)
            └─ 8 B1 de Coacher par A3 (cockpits de direction — ÉTAPE SUIVANTE)
```

## Ce que V3 contient vraiment

- **Doctrine B1/B2/B3** (`Computer_B1_B2_B3_Business_Pulse_Doctrine.md`) : B1 = cockpit
  de direction (North Star 1y/3y/10y, 12WY, charte de décision) ; B2 = 8 managers
  de domaine avec **ordre des gates** (1.Product → 2.Ops → 3.IT → 4.Finance →
  5.Legal → 6.Sales → 7.Growth → 8.People) ; B3 = squads Marvel d'exécution.
  Règle dure : *« A Project folder without the 8 Business domains is structurally
  incomplete. »*
- **A3 Spock** (`A3_Spock_Areas_Spec.md`) : les Areas sont des responsabilités
  continues — entretenues, jamais terminées, cadencées 12WY.
- **8 specs A3** (`A3_<Nom>_LD0X_Spec.md`) : Identité, Question centrale, Inputs,
  Outputs (finding green/yellow/red), Boundaries, Horizon canon.
- **LD01 seul distillé** : `01_Guides_Business/` (8 guides, ~15 500 fichiers sources
  Geordi distillés par MiniMax-M3, vérifiés par A0 — 2 citations à ne pas réutiliser).
  LD02–LD08 n'ont AUCUNE distillation : le prototype franchise est LD01, le reste
  est à répliquer.
- **Coaching loop** (ADR-LD01-008) : triangle Picard (H10 projets) × Jerry (B1 macro)
  × Summers (B1 micro), orchestré par Book (H1). C'est le pattern des « B1 de Coacher ».
- **E-Myth** (`01_E_MYTH_FRANCHISE_PROTOTYPE.md` dans la doctrine SOB) : le prototype
  franchise comme test de répétabilité SOP-grade.

## Correspondance guides V3 → 8 domaines business

| Guide V3 (LD01) | Domaine | VP (DC) | Squad (Marvel) | Lead |
|---|---|---|---|---|
| 01_RH_Meta_Gouvernance | People | Green Lantern | X-Men | Professor X |
| 02_Operations_en_Loops | Ops | Batman | Fantastic Four | Reed Richards |
| 03_Productization_des_Besoins | Product | Flash | Avengers | Captain America |
| 04_Sales_et_Cognition | Sales | Martian Manhunter | Illuminati | Black Bolt |
| 05_People_et_Brand | Growth | Superman | Guardians | Star-Lord |
| 06_Finance_et_ROI | Finance | Wonder Woman | Thunderbolts | Bucky Barnes |
| 07_RD_et_IT | IT | Cyborg | Kang Dynasty | Kang Prime |
| 08_Legal_et_Compliance | Legal | Aquaman | Eternals | Ikaris |

## Ordre des gates B2 (canon)

Product → Ops → IT → Finance → Legal → Sales → Growth → People.
*Empêche Product de devenir tout le business par accident.*

## Contenu du kit

- `A3_LD0X_<Nom>.md` (8) : README de chaque Area — Identité, Question centrale,
  Horizon canon, Règle dure, les 8 projections fractales (table), rattachements.
- `LD01/<CELLULE>.md` (8) : les 8 cellules prototype remplies depuis les guides V3
  (Mission, Frameworks, Actifs, Reçu).
- `TEMPLATE_CELLULE.md` : le moule de réplication pour LD02–LD08.
- Chaque README porte une section **B1 de Coacher — À DÉFINIR** (prochaine étape).

## Déploiement Drive (prévu)

- `A3_LD0X_<Nom>.md` → doc Google dans chaque dossier LD de `02_Areas_Spock`.
- `<CELLULE>.md` → doc Google dans chaque sous-dossier fractal.
- Codes Drive déjà en place : `[CODE_RESP] [CODE_BIZ] [nom adapté]`.
