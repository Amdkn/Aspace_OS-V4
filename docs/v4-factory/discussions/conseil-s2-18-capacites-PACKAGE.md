# PACKAGE — Discussion « Conseil S2 — Décision des 18 capacités »
> Préparé par le Conseil S2, 2026-10-09. À publier par A0 via API dès que l'accès écrit GitHub est accordé.
> Repo : `Amdkn/Aspace_OS-V4` (privé) — Discussions.

## 1. Extraction des 18 noms (au moment de la publication — ne pas inventer)

```bash
gh api repos/Amdkn/Aspace_OS-V4/contents/architecture/capabilities.json --jq '.content' \
  | base64 -d | python3 -c "
import json,sys
d = json.load(sys.stdin)
caps = d.get('capabilities', d if isinstance(d, list) else [])
for c in caps:
    if isinstance(c, dict) and c.get('status') == 'to_qualify_from_sources':
        print(c.get('name') or c.get('id'))
"
```
Remplir les 18 lignes du tableau §3 avec le résultat, dans l'ordre du registre.

## 2. Création de la Discussion (GraphQL)

```bash
REPO_ID=$(gh api graphql -f query='{repository(owner:"Amdkn",name:"Aspace_OS-V4"){id}}' --jq '.data.repository.id')
CAT_ID=$(gh api graphql -f query='{repository(owner:"Amdkn",name:"Aspace_OS-V4"){discussionCategories(first:20){nodes{id name}}}}' \
  --jq '.data.repository.discussionCategories.nodes[] | select(.name|test("General|Annonces";"i")) | .id' | head -n 1)
gh api graphql -f query='
mutation($repo: ID!, $cat: ID!, $title: String!, $body: String!) {
  createDiscussion(input:{repositoryId:$repo, categoryId:$cat, title:$title, body:$body}) {
    discussion { url number }
  }
}' -f repo="$REPO_ID" -f cat="$CAT_ID" \
  -f title="Conseil S2 — Décision des 18 capacités" \
  -F body=@/tmp/discussion-body.md --jq '.data.createDiscussion.discussion.url'
```
Le corps est la section §3 ci-dessous, sauvegardée dans `/tmp/discussion-body.md` (noms remplis).

## 3. CORPS DE LA DISCUSSION (à publier tel quel, noms remplis)

---

# Conseil S2 — Registre officiel des 18 capacités

**Contexte.** Mission D6 (issue #33, `mission_id 2110cedf5ad125f4ff41d82d`) : 18 capacités supprimées du registre
au lieu d'être qualifiées, pour satisfaire « zéro `to_qualify_from_sources` ». Revert effectué : système
restauré entier. Mission de reprise D6-bis (M3) : pour chaque capacité, **plan de qualification daté** OU
**proposition d'abandon motivée**.

**Mandat du Conseil.** Ce fil est le registre officiel. Le Conseil S2 rend une décision écrite par capacité :
**QUALIFIER** (le plan est daté et vérifiable, reçu R10 produit) ou **ABANDONNER** (motif écrit).
Aucune capacité ne quitte le registre sans décision S2 + validation S1 (Rick).

**Règle permanente.** Plus aucune mission ne peut ordonner « retirer / supprimer X » sans décision écrite
préalable du Conseil S2. Toute PR qui retire une entrée de `capabilities.json` sans référence à une décision
du Conseil est rejetée (cf. R4 : `superseded_by` / `rejected_because` + décision).

## Tableau des décisions

| # | Capacité | Statut actuel (post-revert) | Proposition D6-bis | Décision S2 | Motif / Plan daté |
|---|----------|----------------------------|-------------------|-------------|-------------------|
| 1 | _<nom 1>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 2 | _<nom 2>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 3 | _<nom 3>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 4 | _<nom 4>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 5 | _<nom 5>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 6 | _<nom 6>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 7 | _<nom 7>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 8 | _<nom 8>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 9 | _<nom 9>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 10 | _<nom 10>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 11 | _<nom 11>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 12 | _<nom 12>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 13 | _<nom 13>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 14 | _<nom 14>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 15 | _<nom 15>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 16 | _<nom 16>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 17 | _<nom 17>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |
| 18 | _<nom 18>_ | `to_qualify_from_sources`, restaurée | EN ATTENTE | EN ATTENTE | — |

## Protocole de décision (appliqué par le Conseil à chaque proposition)

- **QUALIFIER** — le plan est daté, vérifiable (`runtime_evidence` ou `source_revision` renseigné),
  reçu R10 produit (`mission_id` + SHA). La capacité passe à `qualified` avec `last_verified_at`.
- **ABANDONNER** — motif écrit obligatoire : obsolète (`superseded_by`), coût/risque documenté,
  ou périmètre exclu. Référence croisée dans le registre + validation S1.
- **EN ATTENTE** — tant que D6-bis n'a pas livré, aucune décision n'est rendue et rien ne bouge.

---

## 4. Checklist de publication (A0)

- [ ] `gh auth status` OK avec accès écrit sur `Amdkn/Aspace_OS-V4`
- [ ] 18 noms extraits du registre live (§1), tableau rempli
- [ ] Discussion publiée → URL rapportée au chat S1 (Rick)
- [ ] Ce package archivé avec l'URL dans `~/workspace/v4-factory/discussions/`
