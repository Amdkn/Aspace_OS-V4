# Contrat de mission — Agents GitHub agnostiques

Les profils `.github/agents/*.agent.md` incarnent Rick, les trois Doctors et les
neuf Compagnons. Aucun modèle/provider imposé ni tools artificiellement amputés.
`registry.json` relie les identités institutionnelles aux adaptateurs exécutables.
Un profil n’est pas un daemon ; la boucle Actions fournit les déclenchements.

Identité de mission : dépôt + PR + SHA + holon + effet. Une nouvelle version de
PR crée une nouvelle mission ; une relance du workflow ne crée pas un doublon.
Le premier effet automatique est la revue sous Rick. Ce mandat autorise
inspection, raisonnement et tests, pas push/merge. Les profils gardent leurs
capacités de build/correction lorsqu’un autre mandat autorise ces effets.

Le contrôleur publie CLAIMED avant l’appel externe. Codex et Hermes produisent
le même résultat typé ; Jules fournit une session suivie puis des activités.
Le résultat porte mission_id et head_sha exacts. Une PR modifiée rend la preuve
obsolète. ready exige des preuves et zéro finding non résolu.
Les commit statuses `aspace/agent/<holon>` conservent les receipts ; les artifacts
conservent les résultats 90 jours. Archivage Graham supplémentaire à raccorder.

Après effet ambigu : UNKNOWN, pas de retry aveugle ni fallback payant. Retrouver
la session avec son titre ASpace et mission_id avant réattachement. Une interruption
brutale peut laisser CLAIMED ; cela bloque les doublons mais demande réconciliation.
Ne pas effacer un receipt pour débloquer artificiellement une mission.

Le provider exécute, le holon garde son identité. Les jobs modèles n’ont aucun
token GitHub write. Cette boucle écrit les statuts ; les cinq Apps ne sont ni
remplacées ni réautorisées. Connexion Gateway et promotions d’autorité distinctes.
Une revue réussie n’est pas une approbation de merge ou un test exécuté.

Le contrôleur et le schéma viennent du commit de contrôle, pas du candidat.
Le candidat est une donnée non fiable. Credentials injectés uniquement dans leur
step : proxy de l’action officielle Codex, API Jules, connexion Hermes sur runner
cloud éphémère. Aucun secret dans prompts, résultats ou artifacts. Aucun nouveau
harness sur le PC personnel. Un blocage nomme la connexion manquante et return_to.
