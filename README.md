# Aspace_OS-V4

Stark Jarvis Industry 🏭

V4 est une refondation autonome : BedRock L0, huit domaines Life OS L1, Business
OS au service de LD01 et mémoire cumulative. V3 fournit des acquis à qualifier.

- [Architecture et responsabilités](architecture/REFONDATION.md)
- [WATCH pour Bill](architecture/WATCH.md)
- [Contrat mémoire de Graham](40_Memory/AGENTS.md)
- [Périmètre des capacités à reprendre](architecture/capabilities.json)
- [Instance portable Codespaces / VPS](portable/README.md) : reconstruction
  optionnelle des dépôts de référence, PC comme terminal d'accès.

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

La PR de portabilité #7 est intégrée. Son hydrateur et son devcontainer sont
conservés : le lock V3 fournit des références à qualifier, sans imposer une
migration intégrale ni les contrats V3 à V4. La reconstruction des dépôts est
testée ; la migration des états, des harnesses et du Gateway reste à certifier.
Lire [AGENTS.md](AGENTS.md) avant reprise.

Vérifier aussi le module portable : `(cd portable && python -m unittest -v)`.

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

## Transfert intelligent V3

Voir [migration/README.md](migration/README.md) : 1 341 sources historiques
vérifiables, inventaire de 9 339 entrées, huit LD et six frameworks reliés,
journal temporel durable et compilation de contexte. Les connexions Gateway,
GWS et WorkGraph distant ainsi que l’activation des Doctors restent à effectuer.

```bash
python -m pip install -r requirements.txt
python tools/memory.py check --root 40_Memory
python tools/memory.py query --root 40_Memory --text "Life Core"
python -m aspace.life review --domain LD03 --at 2026-10-05T18:00:00Z
python -m unittest discover -s tests -v
```
