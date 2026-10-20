# Cube Farm — draft de preuve (M-16/D-N019, batch 2/3)

- **verdict** : NEEDS_LIVE_CHECK
- **proof_level** : installed
- **date d'enquête** : 2026-10-09 · **clone** : `~/workspace/v4-capabilities` @ `2554e0f`

## Checks

| Check | Résultat | Preuve |
|---|---|---|
| Scripts control-plane présents | ✅ PASS | `control-plane/` : `README.md` (4 Ko), `setup.sh`, `office.sh`, `directory.py`, `codex.sh`, `ensure-claude.sh` |
| Fork épinglé (lock) | ✅ PASS | `control-plane/runtime.lock.json` : `Amdkn/cubefarm` @ `31e7ce01a1dcc1da2b576d1da36718c16b05b8ca` |
| Fork + commit existent sur GitHub | ✅ PASS | `gh api repos/Amdkn/cubefarm/commits/31e7ce0…` → sha `31e7ce01a1dc` ; repo poussé le 2026-10-05 |
| Devcontainer câblé (port 4417) | ✅ PASS | `.devcontainer/devcontainer.json` : `forwardPorts: [4417]`, label « CubeFarm · A'Space V4 », `postCreateCommand: bash control-plane/setup.sh`, `postStartCommand: … office.sh start` |
| setup.sh hydrate + build l'app | ✅ PASS (code) | `portable/instance.py hydrate --manifest …`, `npm ci`, `npm run build`, `playwright install --with-deps chrome` dans `apps/cubefarm` |
| Bureau live sur 4417 | ❌ NON VÉRIFIABLE | Hydratation uniquement dans le Codespace (`/workspaces/aspace/apps/cubefarm`) — injoignable depuis cette VM |
| Auth + mission avec résultat | ❌ NON VÉRIFIÉ | Le README lui-même l'avoue : « L'authentification et une mission avec résultat restent à vérifier. » |

## Artefacts
- `control-plane/` (scripts + lock), `.devcontainer/devcontainer.json`, fork GitHub vérifié live.

## not_verified
- Bureau 3D répondant sur le port 4417 (privé, Codespace)
- `cubefarm.js login` / `cubefarm.js doctor`
- Une mission bornée avec résultat observable

## live_checks_needed (Codespace uniquement)
1. `bash control-plane/office.sh status` → bureau sur le port privé 4417 répondant (HTTP 200)
2. `(cd /workspaces/aspace/apps/cubefarm && node bin/cubefarm.js doctor)` → output sans erreur
3. Une mission bornée exécutée avec résultat observable (reçu conservé)

## Note de périmètre (honnête)
Capacité prouvée comme **control-plane installé et câblé** (scripts réels, fork épinglé vérifié, devcontainer opérationnel). L'exécution runtime vit dans le Codespace et n'est pas prouvable depuis cette VM. Recommandation : NEEDS_LIVE_CHECK — les 3 checks ci-dessus, exécutés dans le Codespace, suffiraient à passer en QUALIFIED.
