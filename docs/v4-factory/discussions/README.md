# Discussions Missions — mode d'emploi

6 missions typées (S1 → S2/S3), prêtes à poster dans les GitHub Discussions du repo `Amdkn/Aspace_OS-V4`.

| Fichier | Mission | Source audit |
|---|---|---|
| D1-crlf-gitattributes.md | [MISSION-S2] Racine CRLF : `.gitattributes` + renormalisation | §1, §3.3 |
| D2-journal-append-only.md | [MISSION-S2] Journal append-only réel | §2.1 |
| D3-validation-temporelle.md | [MISSION-S2] Validation temporelle honnête | §2.2–§2.7 |
| D4-ci-windows.md | [MISSION-S3] CI portable Windows | §3.2, §3.4, §3.5 |
| D5-aspace-memory.md | [MISSION-S2] Implémenter `aspace/memory.py` | §3.1 |
| D6-capabilities-supabase.md | [MISSION-S2] Qualifier capabilities.json + statuer Supabase | §3.8, §3.9 |

Chaque fichier contient : titre de discussion + mission typée (objectif, périmètre, critères de reçu R10, gate humain) + bloc « Prise en charge » pour les Workers/Doctors.

## Blocage : création impossible depuis ma connexion GitHub actuelle

- Le connecteur GitHub de cette session n'expose aucune API Discussions (catalogue vérifié le 2026-10-09 : issues et PR oui, discussions non).
- Le CLI `gh` n'est pas authentifié sur cette machine.

## Options pour poster

1. **Manuelle (recommandé) :** copier titre + corps de chaque fichier dans une nouvelle Discussion du repo (catégorie au choix, ex. « Missions »).
2. **Via une session authentifiée :** n'importe quelle session disposant de `gh auth` (ex. Codespace V4 control-plane) peut les créer avec `gh api graphql` (mutation `createDiscussion`).
3. **Repli Issues :** je peux les créer comme Issues via `issue_write` — mais ça change le design (le Capitaine veut les missions en Discussions).
