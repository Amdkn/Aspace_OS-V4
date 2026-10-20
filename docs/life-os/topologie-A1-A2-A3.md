# Topologie A1 → A2 → A3 — Life OS (source : V3 `20_Life_OS`)

Analyse exhaustive des 57 specs — 2026-10-08. Référence pour structurer la
documentation de l'arborescence Life OS (Drive : `A'Space Life OS 2026`).

## A1 — Gatekeepers (2)

| A1 | Rôle | Pouvoir |
|---|---|---|
| **Beth** | Conscience stratégique / gardienne du filesystem | 5 états : GREEN / ORANGE / RED / HALT_LD03 / HALT_LD04. Veto. Protège LD03/LD04 contre toute urgence. Morty n'exécute jamais sans clearance Beth. |
| **Morty** | Routeur / exécuteur terminal | Zéro autonomie de décision. Route vers les A2 via Context Packs complets uniquement. Matrice de routage : Orville (sens) → Discovery (ZORA) → SNW (12WY) → Enterprise (PARA) → Cerritos (GTD) → Protostar (DEAL) → Symphony. |

## A2 — Vaisseaux / Frameworks (6)

| A2 | Vaisseau | Framework | Outil shadow | Fonction |
|---|---|---|---|---|
| Orville | USS Orville | Ikigai | Obsidian/notes | Moteur du sens — 4 piliers, horizons H1→H90, trajectoire Kardashev |
| Discovery | USS Discovery | Life Wheel / ZORA | Baserow | Observation — 8 LD en télémétrie, pas en humeur |
| Curie | USS SNW | 12WY | Baserow | Exécution — Rocks, Warp Core tactics, scorecard |
| Computer | USS Enterprise | PARA | Obsidian/filesystem | Structure durable — Projects/Areas/Resources/Archives |
| HoloDeck | USS Cerritos | GTD | Plane | Chaos engine — capture → clarify → organize → review → engage |
| HoloJaneway | USS Protostar | DEAL | Affine | Libération — Define/Eliminate/Automate/Liberate |

## A3 — Équipages (49 specs)

### Orville / Ikigai — 9 A3 : 4 piliers + 5 horizons sentinelles

| A3 | Fonction | Question centrale |
|---|---|---|
| Ed Mercer | Pilier Profession | Le craft est-il payé sans drainer le Life OS ? |
| Kelly Grayson | Pilier Mission | Sert-on un vrai besoin au-delà de A0 ? |
| Gordon Malloy | Pilier Passion | Énergie et curiosité, ou friction répétée ? |
| Claire Finn | Pilier Vocation | Zone de génie honorée sans violer les non-négociables ? |
| Isaac | Horizon H1 (1 an) | Exécutable cette année sans mentir au système ? |
| John Lamarr | Horizon H3 (3 ans) | Construit-on des options utiles pour 3 ans ? |
| Bortus | Horizon H10 (10 ans) | Actif durable survivant à dix ans ? |
| Alara Kitan | Horizon H30 (30 ans) | Élargit-on la liberté future ? |
| Klyden | Horizon H90 (legacy) | Le H90 n'est-il pas trahi par le court terme ? |

### Discovery / ZORA — 8 A3 : les 8 LD

| A3 | LD | Horizon | Règle dure |
|---|---|---|---|
| Book | LD01 Career & Business | H1 (weekly P&L) | Reporte à Discovery, jamais à Morty |
| Saru | LD02 Finance & Independence | H3 (quarterly runway) | Aucun changement payant sans approbation A0 |
| Culber | LD03 Health, Sleep & Energy | H10 | **HARD SAFETY** : RED = veto Beth automatique |
| Tilly | LD04 Mind & Cognition | H30 | **HARD SAFETY** : autorité STOP |
| Stamets | LD05 Social Relations | H30 | Isolation RED = escalade 1 tour |
| Burnham | LD06 Love, Family & Presence | H10 | Fracture du lien RED = escalade 1 tour |
| Reno | LD07 Creativity, Leisure & Flow | H10 | Famine de joie = poison lent |
| Georgiou | LD08 Contribution & Impact | H90 | Negative-reach RED = escalade 1 tour |

### SNW / 12WY — 5 A3 : disciplines en séquence

Pike (Vision) → Una (Planning) → M'Benga (Focus) → Chapel (Metrics) → Ortegas (Execution).
Chaîne : la vision devient Rock (Una, DoD obligatoire) → le focus protège le cycle
(50/30/20) → les métriques gardent l'honnêteté (lead indicators, pas de vanity) →
l'exécution produit des Context Packs prêts pour Morty.

### Enterprise / PARA — 4 A3 : disciplines de structure

| A3 | Discipline | Fonction |
|---|---|---|
| Picard | Projects | Owner des projets (pas de spec A3_Picard en V3 — doctrine seule) |
| Spock | Areas | Responsabilités continues, standards durables |
| Geordi | Resources | Connaissance réutilisable (jamais une responsabilité continue) |
| Data | Archives | Mémoire protégée de la suppression ET de la pollution |

### Cerritos / GTD — 5 A3 : stages en séquence

Mariner (Capture : attrape le chaos vite) → Boimler (Clarify : next action = verbe +
owner) → Rutherford (Organize : chaque item à sa place) → Tendi (Review : >3× répété
→ Protostar) → Freeman (Engage : pas d'owner + pas de preuve = pas d'exécution).

### Protostar / DEAL — 4 A3 : stages Karpathy

Dal (Define : la vérité avant le théâtre) → Rok-Tahk (Eliminate : jamais d'automation
du gaspillage) → Zero (Automate : blueprint + risque + preuves) → Gwyn (Liberate :
**no metric = no liberation claim**).

## Patterns transverses (le moule)

1. **Moule unique** : frontmatter (`id`, `layer: L1_Life_OS`, `role`, `parent_a2`,
   `status: SHADOW_ACTIVE`) + Identity / Core Question / Inputs / Outputs (YAML) /
   Boundaries / Evidence + D1 receipt (plan fancy-hugging-bengio).
2. **L'A3 ne mute jamais rien** : il produit un *finding* typé + signaux + preuves,
   routé vers l'A2 qui compile, vers l'A1 qui décide.
3. **Anti-rôles explicites** dans chaque Boundaries (séparation des pouvoirs).
4. **`hypothesis` est un statut de sortie légitime** — le non-vérifiable reste
   hypothèse, jamais preuve inventée.
5. **Escalades canoniques** : Beth (veto, non-négociables), Morty (exécution),
   Orville/Discovery (compilation), Protostar (friction répétée → DEAL).
6. **Traçabilité totale** : SDD + archives Gemini + twin paths ; doctrine append-only.

## Moule de documentation par niveau

- **A1** : Mission, Inputs lus (table surface/outil/raison), Decision Rules
  (états → action Morty), Seuils.
- **A2** : Identity, Responsibilities, Inputs, Outputs (YAML), Crew (table A3),
  Handoff Rules, Evidence.
- **A3** : Identity, Core Question, Inputs, Outputs (YAML finding), Boundaries,
  Evidence. + pour les LD : table des 8 projections fractales.

## Notes / écarts relevés

- Picard (A3 Projects) n'a pas de spec dédiée en V3 — seulement la doctrine.
- Seul LD01 possède des distillations business (`01_Guides_Business`) — les 7
  autres LD sont à répliquer (prototype franchise).
- 00_Governance (Drive) ↔ 00_Gatekeepers_Beth_Morty (V3) : les specs A1 y ont
  leur place naturelle.
