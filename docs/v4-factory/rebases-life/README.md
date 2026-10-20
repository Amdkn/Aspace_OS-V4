# Rebases #115 / #117 — prêts à pousser

Préparés par le 11e Doctor (cœur Life), 2026-10-09 ~13:25 EDT.
Conflits résolus et vérifiés (tsc sur les fichiers touchés : propre).

## Contenu du bundle `life-115-117.bundle`

- `doctor11/rebase-115` (1bbf893) ← rebase de `terra-m4-flow-capabilities-17234858273267160781` (PR #115) sur `origin/main` (8c06832)
  - `src/types/capabilities.ts` : conflit add/add résolu — canonique #113 comme base + champs optionnels additifs de #115
    (`capability?` union typée, `requested_at?`, `id?`, `correlation_id?`, `readback?`, `error?`, `completed_at?` ; `type?` rendu optionnel car le canary/store ne le posent pas — l'adapter #113 le lit en safe-fallback 'UNKNOWN').
    Suivi Clara : trancher UN seul discriminateur (`type` vs `capability`).
  - `src/lib/capabilities/river-adapter.ts` (fixture de test) : `timestamp: Date.now()` ajouté (requis par le canonique).
  - `test-all.sh` : fusion auto (ligne T7 canary conservée).
- `doctor11/rebase-117` (52b96df) ← rebase de `jules-issue-105-m4-convergence-boundaries-1449804890686472815` (PR #117) sur `origin/main`
  - `src/types/capabilities.ts` : version canonique #113 conservée, divergente #117 abandonnée.
  - `src/lib/workgraph/adapter.ts` : `receipt.id` → `receipt.request_id` (le canonique n'a pas de `id`).
  - `src/services/telemetry/a3-cron-dispatcher.ts` : `requestId` → `request_id`, `timestamp` string → `Date.now()`.

## Poussée — route 13e Doctor (doctrine 2026-10-09 : le Capitaine ne clique plus)

Le 13e applique + pousse via le terminal du Codespace piloté en browser
(environnement authentifié utilisateur). Package : `life-115-117.bundle`
(historique complet vérifié) + ce README. Dans un clone de Life-OS-2026 :

```bash
git fetch /chemin/vers/life-115-117.bundle 'doctor11/rebase-115:tmp115' 'doctor11/rebase-117:tmp117'
git push origin tmp115:terra-m4-flow-capabilities-17234858273267160781 --force-with-lease
git push origin tmp117:jules-issue-105-m4-convergence-boundaries-1449804890686472815 --force-with-lease
```

Le 11e vérifie post-push via API (têtes des PR #115/#117 = `1bbf893` / `52b96df`).
Note : après le merge de #115, #117 gagnera à un second rebase trivial (champs optionnels additifs) — signalé le moment venu.

## Fallback manuel (si la route 13e indisponible)

Mêmes commandes depuis tout terminal avec accès push au repo.
