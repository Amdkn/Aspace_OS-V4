# Aspace_OS-V4

Stark Jarvis Industry 🏭

V4 est une refondation autonome : BedRock L0, huit domaines Life OS L1, Business
OS au service de LD01 et mémoire cumulative. V3 fournit des acquis à qualifier.

- [Architecture et responsabilités](architecture/REFONDATION.md)
- [WATCH pour Bill](architecture/WATCH.md)
- [Contrat mémoire de Graham](40_Memory/AGENTS.md)
- [Périmètre des capacités à reprendre](architecture/capabilities.json)

## Disponible dans cette proposition

WATCH amont épinglé ; capture de sources avec SHA-256 ; notes sourcées et recherche
simple ; sept formulaires de Discussions avec RACI ; tests de mémoire et canary
réel d'extraction de frames sans API. Exécuter depuis un harness cloud :

```sh
python -m unittest discover -s tests -v
python tools/memory.py check --root 40_Memory
python tools/memory.py query --root 40_Memory --text "Life Core"
python tools/watch_canary.py --output /tmp/watch-canary.json
```

Le canary requiert FFmpeg/ffprobe. Les URL du moteur local nécessitent yt-dlp ;
Gemini nécessite la clé injectée dans le compute. Lire WATCH avant le premier usage.

## État restant à réaliser

Discussions activé et sept catégories créées. Formulaires RACI à fusionner sur
main. Wiki natif privé bloqué par le forfait GitHub ; génération OpenWiki à
effectuer dans le harness ; providers à certifier ; compute durable à provisionner ;
surfaces et services existants à qualifier et intégrer. Aucun Doctor autonome,
reset journalier ou service 24/7 n'est lancé par ces fichiers.

La PR de portabilité #7 est indépendante. Ses hypothèses de migration V3 doivent
être réconciliées avec cette refondation avant combinaison ou déploiement.

## OpenWiki

OpenWiki 0.7.0 est épinglé avec son lock npm. L'intégration Codex de projet est
présente (`.agents/skills/openwiki`, `.codex/config.toml`). Sur le compute cible :

```sh
npm ci
sh tools/run-harness.sh codex
```

Le lanceur rend le binaire OpenWiki épinglé accessible au MCP ; Codex lui-même doit
être installé dans le compute. Le mode code génère `openwiki/` depuis les sources
du dépôt. La mémoire de vie reste dans `40_Memory/` ; le mode personal et sa
persistance demandent une configuration séparée. Aucun modèle n'a été appelé par
le test MCP. Ne pas confondre handshake réussi et wiki généré.
