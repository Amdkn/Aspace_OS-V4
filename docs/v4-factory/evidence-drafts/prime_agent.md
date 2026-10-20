# Dossier de preuve — Prime Agent
**Mission :** M-16 / D-N019 · **Échéance :** 2026-11-01 · **Clone :** `~/workspace/v4-capabilities` (main @ 2554e0f)
**Verdict : NOT_PROVEN** · **proof_level : documented** (registre + scripts de déploiement, jamais exécuté)

## Checks

| # | Check | Résultat | Preuve |
|---|---|---|---|
| 1 | Entrée registre harnais | ✅ PASS (déclarée) | `os/business/_runtime/bridge/harnesses.json` → id `prime-agent`, `statut: "suppose"`, `mesure_le: null` |
| 2 | Sonde de joignabilité | ❌ FAIL (non mesuré) | même fichier : `sonde.joignable: null`, note : « PISTE NON VERIFIEE (apercu IA Google, 2026-08-24, pas la doc primaire) : Prime Agent aurait un mode `--mode acp`… A confirmer contre la doc officielle Prime Intellect avant d'agir » |
| 3 | Scripts de déploiement | ✅ PASS (existent) | `os/business/_runtime/bridge/deploy/vps/03-install-prime-agent.sh` + `deploy/vps/systemd/prime-agent.service` |
| 4 | Exécution vérifiée du déploiement | ❌ FAIL | le fichier `.service` lui-même porte : « A CONFIRMER : la sous-commande de lancement persistant n'est pas verifiee dans cette session — l'URL d'install l'est (Prime Intellect, 2026-08-24), pas le mode d'execution en service » |
| 5 | Binaire présent / exécuté | ❌ FAIL | `command -v prime-agent` : absent sur cette VM ; aucune exécution tracée nulle part dans le repo |
| 6 | Tests | ❌ FAIL | aucun test ne référence prime-agent (`tests/` : 0 hit) |
| 7 | Issues/PRs GitHub | — | 0 issue, 0 PR mentionnant « prime agent » sur Amdkn/Aspace_OS-V4 |

## Artefacts
- `os/business/_runtime/bridge/harnesses.json` (entrée `prime-agent`, statut `suppose`)
- `os/business/_runtime/bridge/deploy/vps/03-install-prime-agent.sh`
- `os/business/_runtime/bridge/deploy/vps/systemd/prime-agent.service`

## not_verified
- Installation réelle (`curl …/install.sh | sh` puis `prime-agent --version`) — jamais exécutée ni tracée
- Mode `--mode acp` / Agent Client Protocol — piste non vérifiée contre la doc Prime Intellect
- Service systemd actif sur la VPS — aucun `systemctl status` produit
- Routage effectif par le bridge (`ori` → `prime-agent`) — aucune trace d'exécution

## live_checks_needed
1. Sur la VPS : exécuter `03-install-prime-agent.sh`, capturer `prime-agent --version` et `prime-agent --help` (vérifier la sous-commande de lancement persistant)
2. Confirmer le mode ACP contre la documentation officielle Prime Intellect (pas l'aperçu IA)
3. `systemctl status prime-agent` sur la VPS + un appel routé via le bridge avec reçu

## Note de périmètre (honnête)
Prime Agent est **déclaré** au registre des harnais et **préparé** au déploiement (scripts + unit systemd), mais le registre lui-même le marque `suppose` et sa propre sonde n'a jamais été concluante. Aucune exécution n'est prouvée. Conformément à la condition S2, sans preuve au 2026-11-01 la capacité revient devant le Conseil ; tout retrait exige décision S2 + validation S1 (M-08) — ce dossier ne prononce aucun retrait.
