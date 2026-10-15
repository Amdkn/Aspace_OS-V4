# ÉTAT COURANT DES EFFETS — constitution et runtime distincts (2026-10-14)

**Autorité institutionnelle** : dans un mandat et une portée d'accès explicitement valides, Rick et les Doctors peuvent proposer, modifier, tester, pousser et fusionner, avec trace du résultat et relecture native. L'absence de gate humain routinier N'abolit PAS les permissions GitHub, la protection des branches, la validation du besoin ni la preuve.

**Mécanisme implémenté** : [Agent Mesh](README.md) prend aujourd'hui surtout les PR pour REVUE (status/receipt typé). [Issue Factory](README.md) peut déclencher fabrication par Jules sur Issue éligible et recevoir une PR. Les findings ne sont pas automatiquement réparés, l'auto-merge n'est PAS implanté comme chaîne générale, le déploiement et le gain humain ne sont pas attestés par le statut READY. Ceci n'interdit pas un holon possédant un mandat d'utiliser un autre harness capable de push/merge avec les droits réels et preuves nécessaires.

**Résidence institutionnelle** : [13 holons Tech](../tech/holons/README.md), [liaison registry et Drive](../tech/holons/HARNESS_BINDINGS.md). Une autorité accordée ≠ un effet automatique réellement câblé ≠ une session en ligne. Cette section prime sur les formulations ambiguës datées ci-dessous, qui sont de l'historique.

---

# Contrat de mission — Agents GitHub agnostiques


Les profils `.github/agents/*.agent.md` incarnent Rick, les trois Doctors et les
neuf Compagnons. Aucun modèle/provider imposé ni tools artificiellement amputés.
`registry.json` relie les identités institutionnelles aux adaptateurs exécutables.
Un profil n’est pas un daemon ; la boucle Actions fournit les déclenchements.


Identité de mission : dépôt + PR + SHA + holon + effet. Une nouvelle version de
PR crée une nouvelle mission ; une relance du workflow ne crée pas un doublon.
Le premier effet automatique est la revue sous Rick. Ce mandat autorise
inspection, raisonnement, tests, push et merge sur décision du holon —
aucun gate humain : le Capitaine ne clique plus, l'autorité est pleine.
Les profils gardent leurs
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
