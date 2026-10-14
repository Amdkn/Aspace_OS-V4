# AGENTS — contrat d'écriture et d'exploitation du Home
> Instruction locale sous le `AGENTS.md` V4 racine; toute ancienne instruction V3 ne s'hérite qu'en tant que source historique.

## Lecture avant action
`README → IDENTITY → GOVERNANCE → IPBD/register → STATE → HANDOFF`, puis `../AGENTS.md`, `../40_Memory/AGENTS.md` et contrat de mission. Chercher la dernière source applicable par date, scope et autorité, jamais le fichier le plus récent seulement.

## Agents travaillant ici
Toute identité S/A/B autorisée conserve sa cognition entière et une juridiction limitée. GitHub Copilot/Codex reconnaît surtout `AGENTS.md` au plus proche chemin. `AGENT.md`, `SOUL.md`, `MISSION.md`, etc. sont des documents **à charger explicitement** via adaptateur/context compiler; aucun support automatique multi-harness n'est attesté. `.github/agents/*.agent.md` décrit les profils GitHub. `CLAUDE.md` et fichiers équivalents seulement si un adapter contrôlé les installe, sans rôle ambigu.

## Mutation
1. Source & autorité → 2. qualification/provenance → 3. diff minimal sur branche mission → 4. preuves/tests/review → 5. PR → 6. promotion `main` → 7. mise à jour `STATE/HANDOFF` et retour au porteur.
Ne jamais écrire des données sensibles dans ce dépôt public. Dans le Drive privé, garder l'ID et le lien du document existant; écrire append-only/supersession et réviser en cas de conflit, jamais effacer une ancienne déclaration.
Une demande de changement identitaire, financière ou familiale escalade à l'humain; une suggestion d'agent n'est pas une ratification.
`UNKNOWN` est un état valide; absence de receipt = pas de résultat garanti.

## Transmissions
Toujours transporter `holon_id, ipbd_id(s), mission_id, work_id, correlation_id, authority_envelope, evidence_refs, return_to, temporal_cutoff` si ces objets existent; ne pas inventer les IDs runtime manquants. Opérer dans le scope prouvé. Les titres de personnes d'agents ne signifient pas que leurs runtimes soient lancés.
