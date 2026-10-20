# DIRECTIVE DE MERGE S2 — Life-OS-2026 : #118 → #113, puis suite
> **OBSOLÈTE — exécutée le 2026-10-09** (vérifié via API publique : #111, #113, #115, #117, #118 mergées ; #114 fermée non mergée).
> Décision du Conseil S2, 2026-10-09. Doctrine en vigueur : gate humain SUPPRIMÉ —
> S2 décide ET merge ; A0 exécute via API dès que l'accès écrit GitHub est accordé.

## Ordre d'exécution (strict)

### Étape 1 — #118 : re-run des checks puis squash-merge
#118 = 1 fichier (`scripts/test-offline-recovery.ts`, +8/-7), risque zéro, mais `verify-state`
n'a jamais tourné dessus. Re-run d'abord :
```bash
gh api repos/Amdkn/Life-OS-2026/actions/runs --jq \
  '.workflow_runs[] | select(.head_sha=="2d5945c3be971f839b4bb7b7d21824adfa8ad342") | .id' | head -n 5
# re-run du run verify-state correspondant :
gh api -X POST repos/Amdkn/Life-OS-2026/actions/runs/<RUN_ID>/rerun
# attendre le vert, puis :
gh pr merge 118 --repo Amdkn/Life-OS-2026 --squash --delete-branch
```

### Étape 2 — #113 : merge commit (jalon des types canoniques)
```bash
gh pr merge 113 --repo Amdkn/Life-OS-2026 --merge --delete-branch
```
#113 établit `src/types/capabilities.ts` (canonique) + `src/lib/river/adapter.ts` (testé).
Ne pas squash : le merge commit marque le jalon.

### Étape 3 — #114 : fermer (couverte par #113) + rouvrir le fix B3Matrix en issue
```bash
gh pr close 114 --repo Amdkn/Life-OS-2026 --comment \
  "Fermée par décision S2 (2026-10-09) : couverte par #113 (types canoniques) et en collision frontale avec #115 sur src/lib/capabilities/river-adapter.ts. Le fix B3MatrixCockpit est rouvert en issue dédiée."
gh issue create --repo Amdkn/Life-OS-2026 --title \
  "[B3Matrix] Simplifier MatrixWorker en alias de B3WorkerDescriptor" --body \
  "Extrait de #114 (décision S2 : ne pas merger la PR, garder le fix).
Fichier : src/components/b3-matrix/B3MatrixCockpit.tsx (+1/-7).
Changement : remplacer l'interface MatrixWorker (extends B3WorkerDescriptor + status, lastLogs, measuredComputeTime?, measuredBudgetTokens?, triggers[]) par le simple alias :
\`type MatrixWorker = B3WorkerDescriptor;\`
Vérifier à la reprise que les champs supprimés ne sont plus consommés ailleurs."
```

### Étape 4 — #115 et #117 : rebase sur main (dispatch S3/Nardole → Jules)
Conflits connus (vérifiés par diff S2) :
- `src/types/capabilities.ts` : 3 définitions divergentes → adopter le canonique #113, reporter le contenu utile (#115 : union `capability`, `readback` ; #117 : `context?`, `'AUTH_REQUIRED'`).
- `src/lib/capabilities/river-adapter.ts` : #114 vs #115, même chemin → trancher : garder UNE implémentation, alignée sur `src/lib/river/adapter.ts` (#113).
Dispatch : Nardole redispatch à Jules « rebase #115 et #117 sur main, conflits résolus vers le canonique #113 ».

### Étape 5 — #111 : un-draft + CI complète (en dernier)
```bash
gh pr ready 111 --repo Amdkn/Life-OS-2026
```
6 fichiers `src/services/` — attendre `verify-state` vert avant merge.

## Vérifications finales
- [ ] `main` de Life-OS-2026 contient les types canoniques + 1 seul river-adapter de référence
- [ ] PR #22 sur `Amdkn/Aspace_OS-V4` (privé) : incluse dans le balayage A0
- [ ] Reçus R10 : chaque merge exécuté par A0 consigne `mission_id` + SHA (pas de statut « actif » sans reçu)
