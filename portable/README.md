# Instance A'Space portable — cloud-first

Directive du Fondateur, 2026-10-05 : PC = terminal d'accès ; aucune nouvelle donnée de travail ni harness sur le PC. Codespaces héberge les workspaces et harnesses ; un VPS/compute compatible peut reprendre l'instance. V3 reste source de provenance pendant la construction de V4, sans destruction ni réécriture de V3.

## Livré et vérifié

- Lock de dix dépôts du registre V3 avec SHA complets observés via GitHub le 2026-10-05 ; V3 épinglé à ad5e68e2867854ad952495cf1fcd37d76acbd33e, incluant les permissions des cinq Apps activées sur V3/V4.
- Hydratation explicite, idempotente, checkout détaché à SHA exact, vérification origine/révision/propreté ; refus d'écraser un checkout divergent ; verrou de provisioning ; reçu sur disque distant.
- Six tests exécutés dans l'environnement cloud de construction : Git réel, révision ancienne malgré une branche avancée, deuxième exécution, travail non commité conservé, mauvaise origine, chemins et liens sortants refusés.
- Devcontainer Codespaces / Dev Containers. Les images/features ont des tags versionnés mais pas de digest : reproductibilité des dépôts prouvée par SHA, reproductibilité binaire complète restant à verrouiller.

## Utilisation sur le compute distant

Python 3.12 et Git requis. Ouvrir cette branche V4 dans Codespaces, puis :

```sh
python3 portable/instance.py plan
python3 portable/instance.py hydrate --root /workspaces/aspace
python3 portable/instance.py verify --root /workspaces/aspace
```

Sur un VPS Linux, même checkout V4 et mêmes commandes avec `--root /srv/aspace` dans un répertoire possédé par l'opérateur. Authentification GitHub configurée sur le compute cible ; ne jamais mettre un jeton dans le lock. Les dix repos peuvent nécessiter plusieurs autorisations distinctes : les cinq Apps A'Space ne sont installées que sur V3/V4.

`hydrate` n'exécute aucun code cloné, n'initialise pas les sous-modules, n'installe pas les dépendances applicatives et ne démarre aucun agent. Une erreur d'un dépôt produit FAILED et un code non nul ; les autres résultats restent dans le reçu. Exit 0 signifie seulement que les dix checkouts correspondent au lock. Il ne certifie pas une migration runtime.

Pour mettre à jour : publier un nouveau lock avec les SHA acceptés et hydrater dans une nouvelle racine ; conserver l'ancienne pour rollback. Ne jamais employer reset --hard sur un workspace actif. Les changements de mission se font en branches/worktrees séparés du socle détaché.

## Fusion fonctionnelle recherchée

| Primitive | Rôle dans la boucle Life / Business / Tech |
|---|---|
| GitHub Agents | incarnations natives avec contrat de capacité et retour de preuve ; aucun fichier persona n'est une session active |
| Project | portefeuille et compositions de capacités ; B1/B2/B3, frameworks Life et échelles M0/M1/M2 restent distincts des fournisseurs |
| Milestone | résultat de convergence, dont cutover distant vérifié |
| Discussion | exploration BMAD/Gstack/CEO Bench, alternatives et besoins ambigus |
| Wiki/docs | doctrine et mémoire versionnées ; miroir vers Wiki, aucune seconde constitution |
| Issue | effet exécutable et acceptation ; réutiliser #542/#545/#546 dans V3 |
| PR | mutation exacte et preuve, y compris adaptateurs Business et harnesses |
| Actions/Checks | vérification déterministe et pont d'événements ; pas le scheduler universel |
| Release | code accepté + lock + références d'état/rollback ; aucune donnée privée dans une release publique |

Business OS conserve ses huit domaines et ses agents cognitifs complets. Le Gateway transporte leurs requêtes vers les capacités existantes (API/MCP/CLI/skills/harnesses) ; il ne remplace ni leur cognition, ni leurs opérations GWS, ni leur mémoire. Les providers restent orthogonaux aux identités. Hermes Workspace cloné != Hermes Agent installé et connecté. L'interface Agents de la capture ne montre aucune session correspondant au filtre ; elle ne prouve pas l'absence de runtimes externes.

## Une migration complète : code + état + autorité + reprise

Le lock de code est le premier composant exécutable, pas une réduction de cette cible :

1. Code : dix dépôts épinglés ; gitlinks tiers et dépendances/harnesses à inventorier et verrouiller, sans copier aveuglément des installations Windows.
2. État : transférer WorkGraph/SQLite par sauvegarde cohérente, mémoire mutable, sessions Hermes, evidence, travail non commité et curseurs Gateway vers stockage durable privé distant. GitHub porte le versionné ; les données de domaine restent dans leur plan autoritaire. Un volume Codespaces n'est pas un backup externe.
3. Autorité : injecter les secrets sur le compute cible, conserver installation/token scopes et les baux. Ne pas exporter les clés dans un bundle de code.
4. Reprise : arrêter/admettre les effets source par fencing, reprendre mission/work/correlation/operation/session/return_to identiques sur cible. Une seule autorité pour chaque effet conflictuel ; poly-incarnations permises pour effets distincts.
5. Preuve : exécuter une mission Business/Life réversible entre GitHub + surface Hermes/Agent OS et deux runtimes ; coupure/reconnexion, absence de double effet et rollback observés (#546).

Codespaces est soumis à arrêt/inactivité : aucune promesse 24/7. Le même paquet vise Linux sur VPS pour les services permanents ; CPU/architecture, ressources, réseau et dépendances doivent être compatibles. La commande unique de cutover complet n'est pas implémentée tant que restauration d'état et fencing n'ont pas d'adaptateurs vérifiés.

## Manques précis, sans effacement de portée

- Agent-OS parent et Observatoire sont local_only dans le registre historique. Agent-OS comporte un ancien rejet secret-scanning ; préparer un export assaini, jamais contourner le blocage ni pousser l'historique brut.
- Gateway/OpenClaw, Hermes et autres harnesses : installation, auth, session federation et démarrage réel restent non certifiés. Retour : https://github.com/Amdkn/Aspace_OS_V3/issues/545 et #546.
- GitHub PR #569 fournit le setup complémentaire ; elle n'est pas incorporée dans le SHA V3 épinglé. La réponse API consultée indique OPEN, mergeable=false : ne pas reprendre l'ancien « mergeable » comme preuve actuelle.
- Source locale intacte ; aucune suppression, extinction ou lecture DC effectuée dans cette livraison. Le retrait des anciennes exécutions attend un cutover réel et vérifié.
- Aucun Codespace créé/démarré, aucun compute facturé, aucune session native GitHub déclenchée par cette PR. Le transport réseau GitHub des dix clones reste à tester sur la cible authentifiée.

Références : V3 ASPACE_WORKSPACE_REGISTRY.json ; ASPACE_GATEWAY_NATIVE_GITHUB_V0.md ; ASPACE_GITHUB_APP_CAPACITY_AND_PROMOTION_V1.md ; PR #569 ; https://docs.github.com/en/codespaces/about-codespaces/understanding-the-codespace-lifecycle
