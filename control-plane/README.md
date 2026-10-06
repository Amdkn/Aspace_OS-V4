# Un seul Codespace : V4

Décision du 6 octobre 2026 : V4 porte le poste de contrôle du Directory GitHub.
Créer/reprendre le Codespace **depuis Amdkn/Aspace_OS-V4**. L'instance CubeFarm
`ominous palm-tree` reste arrêtée ; aucun script ne la redémarre ou la supprime.

Le devcontainer installe Node 24, Python 3.12, gh, OpenWiki, Codex et Chrome,
hydrate uniquement CubeFarm au SHA du lock, puis construit son client et son
serveur. Le démarrage du Codespace démarre le bureau réel sur **4417 privé**.
Les anciens locks/hydrateurs portables restent disponibles, jamais auto-exécutés.

## Utilisation

Ouvrir `/workspaces/aspace/aspace.code-workspace` avec File → Open Workspace from File.
V4 est la racine de contrôle ; CubeFarm est une application sœur hors du dépôt.
Ouvrir le port 4417 depuis Ports en conservant Private : il expose des terminaux.

```bash
bash control-plane/office.sh status
python3 control-plane/directory.py refresh
python3 control-plane/directory.py workspace
```

L'inventaire paginé conserve les repos visibles de Amdkn, omk-services et
outsourc-e avec branche, URL, visibilité et permission observée. Un propriétaire
inaccessible fait échouer le rafraîchissement sans remplacer l'inventaire précédent.
`--owners Amdkn` permet un périmètre explicitement réduit. Pas de prétention à voir
les repos privés absents des autorisations. Pas de clone massif.

Les projets clonés sous `/workspaces/aspace/projects/<owner>/<repo>` rejoignent
le workspace à sa régénération. CubeFarm gère séparément ses propres worktrees.
Les nouvelles configurations et intégrations se développent dans V4, sous branches
de mission Doctors. Le fork CubeFarm reste une source épinglée ; aucun push amont.

## Connexions des agents

Dans le terminal du compute, pas dans le chat :

```bash
(cd /workspaces/aspace/apps/cubefarm && node bin/cubefarm.js login)
codex login --device-auth
(cd /workspaces/aspace/apps/cubefarm && node bin/cubefarm.js doctor)
```

Le CEO actuel de CubeFarm utilise Claude ; ses développeurs peuvent utiliser
Codex. Les adaptateurs Jules/Hermes de V4 restent distincts : aucune compatibilité
CubeFarm n'est inventée. Créer le bureau dans l'interface puis connecter V4 comme
premier projet. L'authentification et une mission avec résultat restent à vérifier.

Le token Codespaces appartient à V4. Les cinq Apps conservent leurs autorités :
ce bootstrap ne les remplace pas et ne modifie pas leurs permissions. L'inventaire
ne donne pas de droits supplémentaires. Les accès aux autres dépôts doivent être
accordés à l'identité qui y exécute réellement une mission.

## État, arrêt et reprise

État CubeFarm : `/workspaces/aspace/state/cubefarm` ; inventaire :
`/workspaces/aspace/state/directory.json`. Le volume survit au stop/rebuild de
l'instance, pas à sa suppression. Aucun secret/état privé dans Git.
Arrêter les sessions actives dans l'interface avant `bash control-plane/office.sh stop`.
Le gestionnaire de terminaux amont peut conserver des sessions après arrêt du bureau.

Pour un VPS compatible : même devcontainer et volume `/workspaces` restauré de
façon privée après arrêt des sessions, puis réauthentification. Le bootstrap ne
fournit pas encore la sauvegarde externe automatique ou le fencing inter-machines.
Un Codespace arrêté ne fait pas tourner les agents. Un seul Codespace de contrôle
n'impose pas un seul processus ni un seul provider.

## Codex et Supabase
Codex est installe par setup.sh. Verifier : bash control-plane/codex.sh status. Connecter : bash control-plane/codex.sh login. Completer la connexion dans le navigateur sans copier de secret dans Git ou le chat. Apres connexion, choisir Codex pour les developpeurs/QA dans les reglages CubeFarm et verifier une mission bornee. Le CEO reste Claude dans cette version.
Lire [Supabase dans V4](../architecture/SUPABASE_RUNTIME.md). La commande bash control-plane/codex.sh supabase-login configure le MCP Life OS de decouverte puis lance OAuth. Connexion distincte du connecteur ChatGPT ; credentials hors depot, reconnexion sur un nouveau compute.
