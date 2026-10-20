# B2 DC — VPs de Domaines

Projection B2 à la racine de **LD01 Career & Business**, à côté de
`B1 BOOK — Direction`.

## Doctrine (source : `Amdkn/BusinessOS` — `04_Business_Domains/`)

| Niveau | Rôle E-Myth | Fonction | Figure |
|---|---|---|---|
| B1 | Entrepreneur (Summers) | Direction : Rocks, North Star, charte de décision | — |
| **B2** | **Manager (VP/capitaine)** | **Découpe les rocks en sprints, tient le veto** | **Héros DC** |
| B3 | Technicians (squad) | Exécution : scrums + preuves vérifiables | Équipe Marvel |

- Chaque domaine L2 a un **VP/capitaine** (le champion DC). Le B2 manage, il n'exécute pas :
  le jour où le manager fait le geste d'un technicien, le domaine perd son manager.
- Amont : `B2_DC_DIRECTION_COUNCIL_DECISIONS.md` — journal append-only des décisions
  (dormant/actif). Sans ligne `signé:`, une entrée ne compte pas.
- Aval : `SPRINTS.md` par domaine → `SCRUMS.md` par technicien B3.
- Dormance : B1 peut la *demander*, seul le capitaine peut la *déclarer*
  (3 conditions cumulatives).
- Règle dure : un domaine sans les 8 fonctions est structurellement incomplet.

## Les 8 VPs

| B2 | Domaine L2 | Champion DC | Devise |
|---|---|---|---|
| B2 PPL | People | Green Lantern | Recruter lentement, trancher vite |
| B2 OPS | Opérations | Batman | Le processus est l'arme |
| B2 PRD | Product | Flash | Vitesse de boucle, pas de sortie |
| B2 SAL | Sales | Martian Manhunter | Lire l'acheteur avant le prix |
| B2 GRO | Growth | Superman | La marque survit au silence |
| B2 FIN | Finance | Wonder Woman | Le chiffre avant son histoire |
| B2 IT | IT | Cyborg | Veille > infra lourde |
| B2 LEG | Legal | Aquaman | Le contrat est le fond |

Chaque dossier B2 contient son README : mandat VP, veto, roster du squad B3
(équipe Marvel, à structurer), lien source GitHub.

## Squads B3 (à structurer)

Les équipes Marvel sont les squads d'exécution de chaque VP :
X-Men (8), Fantastic Four (4), Avengers (7), Illuminati (6),
Guardians (6), Thunderbolts (6), Kang Dynasty (6), Eternals (10).

## OMK

Ces VPs pilotent l'exécution du catalogue **OMK 75 actes**
(Pôle 1 Légal · Pôle 2 Vault privé · Pôle 3 JaaS/Carrière). Chaque acte
s'assigne au domaine de son VP ; le reçu d'exécution remonte en B1.

## Sources

- Business OS : https://github.com/Amdkn/BusinessOS/tree/HEAD/04_Business_Domains
- OMK Office : catalogue 75 actes (3 pôles × 5 cadres × 5 actes), 300 $/an
