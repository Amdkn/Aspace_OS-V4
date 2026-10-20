# Structuration des Discussions GitHub — S1/S2/S3 × canaux holons

> Analyse demandée par le Capitaine, 2026-10-09.
> Repo : `Amdkn/Aspace_OS-V4` → `/discussions`.
> État actuel : 16 catégories, **1 seule discussion** (épinglée, Life Core).
> Le terrain est vierge : on structure avant l'arrivée des holons, pas après.

## Principe

- **3 sections = les 3 étages de la chaîne** : S1 (Rick) → S2 (Doctors) → S3 (Compagnons).
- **13 canaux de responsabilité** : 1 (Rick) + 3 (Doctors) + 9 (Compagnons).
- **« Réservé » = RACI, pas permissions** : le holon est *Accountable* de son canal,
  mais tout le monde peut y écrire — c'est le mécanisme de **délégation coopérative**.
  On ne sait pas où déléguer ? → canal de Nardole (Dispatch), qui route.
- **Règle d'or** : le Capitaine n'est sollicité que dans `S1 · Missions` (gate vision)
  et notifié des `Preuves` (R10). Jamais pour la technique.

## Architecture cible (corrigée par le Capitaine, 2026-10-09 ~09:20 EDT)

> Correction du Capitaine : les holons **absorbent les catégories existantes**
> plutôt que d'en créer des neuves — 7 renommages + 2 créations seulement.
> Doctrine : implémenter même imparfait (les erreurs se corrigent), jamais de
> boucle de questions-babysitting.

### Section « S1 · Gatekeeper » (à créer)

| Catégorie | Responsable (A) | Usage |
|---|---|---|
| Missions | Rick | Mission.md publiée par Rick ; le Capitaine valide = gate vision. Chaque mission lie ses Issues. |

### Section « S2 · Doctors » (renommer la section existante « Doctors — trois Cores »)

| Catégorie | Responsable (A) | Usage |
|---|---|---|
| Life Core | 11e Doctor | PRD/ADR du cœur Life (existe déjà, garder) |
| Kernel Core | 13e Doctor | PRD/ADR du Kernel (existe, garder) |
| Buzz Core | 12e Doctor | PRD/ADR du Buzz (existe, garder) |

### Section « S3 · Compagnons » (à créer — 9 canaux par absorption)

| Catégorie (nouveau nom) | Ancien nom | Responsable (A) | Usage |
|---|---|---|---|
| Nardole · Dispatch | Agora | Nardole | Place publique + **entrée du dispatch** : intentions, demandes de délégation coopérative, exploration. Nardole route vers le bon canal |
| Clara · Design | Decisions | Clara | Autorité design + arbitrages : alternatives, raisons, supersession. Un seul A par décision, RACI explicite |
| Bill · Research | Frameworks | Bill | Recherche et compositions : Ikigai, Wheel, Curie/12WY, PARA, GTD, DEAL ; découvertes et signaux sourcés |
| Ryan · Factory | Atelier | Ryan | Fabrication : demandes de build, sorties factory, capacités |
| Graham · Mémoire | Memoire | Graham | Synthèses : connaissances liées, contradictions, leçons. Sources et provenance |
| Yaz · Observatoire | Observatoire | Yaz | Signaux, observations, infrastructure, WATCH et veille |
| Rory · Preuves | Preuves | Rory | R10, démos, résultats, incidents et réparations. Distinguer observé / testé / hypothétique |
| Amy · Interfaces | *(nouvelle)* | Amy | Squad Life : shell, PARA, matrice 8×8, thèmes |
| River · Flux | *(nouvelle)* | River | Squad Life : intégrations, ponts, river-adapters |

### Catégories transverses (garder telle quelle)

| Catégorie | Usage |
|---|---|
| Announcements | Réservée aux mainteneurs (restreinte, garder) |

### À supprimer (redondantes avec la taxonomie française)

General, Ideas, Polls, Q&A, Show and tell — les 5 catégories par défaut de GitHub,
recouvertes par Nardole · Agora (idées, discussions libres) et Clara · Decisions.

## Règles de délégation coopérative

1. **N'importe qui ouvre une discussion dans n'importe quel canal holon** :
   titre `[DEMANDE] …`, RACI proposé dans le corps, `return_to` indiqué.
2. **Le holon Accountable trie sous 48 h** : accepte (→ Atelier ou son backlog),
   redirige (→ bon canal, via Nardole si hésitation), ou refuse (motif sourcé).
3. **Traçabilité** : S1 Mission ↔ Issues ↔ PRs ↔ Preuves (R10). Une mission sans
   Issue liée = pas de tracking ; une PR sans R10 = pas de merge.
4. **Silence = vert** : pas de réponse d'un holon sous 48 h → Nardole escalade
   au Doctor du cœur (même rituel que M'Benga/Graham).
5. **Le Capitaine** n'écrit que dans Missions (gate) et lit les Preuves. Tout le
   reste est délégué.

## Règles et protocoles d'échanges inter-holons — ✅ LOI RATIFIÉE par le Capitaine, 2026-10-09 (« go »)

### Typage des discussions (préfixe de titre obligatoire)

| Préfixe | Sens | Canal typique |
|---|---|---|
| `[DEMANDE]` | Délégation coopérative : qui demande quoi à qui | canal du holon sollicité |
| `[PROPOSITION]` | PRD / ADR / TDD / plan soumis à revue | S2 ou S3 selon l'étage |
| `[ARBITRAGE]` | Décision à trancher, alternatives + recommandation | Clara · Design |
| `[PREUVE]` | R10, démo, résultat vérifié | Rory · Preuves |
| `[ESCALADE]` | Blocage remonté d'un étage à l'autre | Nardole · Dispatch |
| `[RETOUR]` | Post-mortem, leçon apprise | Graham · Mémoire |

### Règles d'échange

1. **Corps structuré** : tout fil porte un RACI explicite + `return_to`
   (où la réponse doit atterrir). Sans `return_to`, Nardole le demande.
2. **Un seul fil par sujet** : pas de cross-posting entre canaux.
   Mauvais canal → Nardole redirige, ne duplique pas.
3. **SLA 48 h** : le holon responsable accuse réception avec un statut —
   accepté / redirigé / refusé (motif sourcé).
4. **Silence = vert, mais silence ≠ accord** : passé 48 h sans réponse,
   Nardole escalade au Doctor du cœur (rituel M'Benga/Graham).
5. **Niveaux de preuve obligatoires** : chaque affirmation est étiquetée
   OBSERVÉ (fait vérifié) / TESTÉ (check vert) / HYPOTHÉTIQUE (à valider).
   Jamais mélangés sans étiquette.
6. **Aucune technique ne remonte au Capitaine** : seule la vision va en
   S1 · Missions. Règle d'or non négociable.
7. **Décision finale sauf preuve contraire** : un arbitrage de Clara · Design
   est définitif ; on ne le rouvre que par supersession explicite
   (lien vers la décision remplacée + nouvelle preuve).
8. **Pas de fil orphelin** : toute `[DEMANDE]` lie une Issue ou une Mission ;
   toute `[PREUVE]` lie sa PR. Sinon le fil est redirigé vers Nardole.
9. **Conflit entre holons → arbitrage Clara**, jamais de guerre de threads.
10. **Français par défaut** ; termes techniques anglais si consacrés.

### Protocole de routage (Nardole · Dispatch)

Entrée → tri sous 48 h → canal compétent → suivi jusqu'à `[PREUVE]` →
clôture + inscription au REGISTRE-NARDOLE. Nardole est le seul à pouvoir
déplacer un fil d'un canal à l'autre (traçabilité unique).

### Protocole d'escalade

Holon → Doctor du cœur → (si vision uniquement) S1 · Missions → Capitaine.
Jamais de saut d'étage, sauf urgence bloquante documentée dans le fil.

## Plan de migration — ✅ RÉALISÉ le 2026-10-09 (7/7, via navigateur)

1. ✅ Section « S1 · Gatekeeper » + catégorie « Missions » créées.
2. ✅ Section « Doctors — trois Cores » → « S2 · Doctors ».
3. ✅ Section « S3 · Compagnons » créée.
4. ✅ 7 renommages + déplacements : Nardole · Agora, Clara · Decisions,
   Bill · Frameworks, Ryan · Factory, Graham · Mémoire, Yaz · Observatoire,
   Rory · Preuves.
5. ✅ « Amy · Interfaces » et « River · Flux » créées.
6. ✅ 5 catégories par défaut supprimées (General, Ideas, Polls, Q&A, Show and tell).
7. ✅ Discussion « Mode d'emploi des canaux holons » créée dans Nardole · Agora
   (discussion #23, https://github.com/Amdkn/Aspace_OS-V4/discussions/23) et épinglée.
   La discussion d'origine de Life Core est intacte.
- 2026-10-09 ~09:35 EDT : **3 renommages appliqués** (noms seuls, descriptions
  inchangées) : « Nardole · Agora » → « Nardole · Dispatch »,
  « Clara · Decisions » → « Clara · Design »,
  « Bill · Frameworks » → « Bill · Research ».
