# Transfert intelligent V3 → V4

V4 est autonome. L'import conserve les sources sans importer leur autorité ni
réactiver leurs processus. Le PC personnel n'est pas utilisé.

## Contenu effectivement repris

- Snapshot V3 `ad5e68e2867854ad952495cf1fcd37d76acbd33e`.
- Inventaire des 9 339 blobs/gitlinks et leur disposition.
- 1 341 sources textuelles exactes : les 100 fichiers OKF, Life OS hors archives,
  distillation, méthodes et ontologies. Les 7 binaires sélectionnés restent des
  références V3. Les 3 249 fichiers des archives Life sont indexés par chemin et
  objet Git ; 4 736 autres entrées attendent qualification, ainsi que 6 gitlinks.
- Corpus compressé déterministe, non exécutable, consultable sans checkout V3.
- Huit LD, six frameworks et références de sources résolubles.
- Graphe temporel, compilateur, paquets et réconciliation extraits de V3 ; tests
  d'origine repris avec adaptation des imports et chemins.
- Journal SQLite append-only par API, sauvegarde cohérente, contrôle d'intégrité,
  idempotence, immuabilité des identifiants, scopes et provenance explicite.
- Revue Life sans inférence de score : les historiques ne deviennent pas des
  observations actuelles. Contradictions, dates et return_to sont conservés.

## Utilisation dans le compute

Depuis la racine du dépôt :

```bash
python -m pip install -r requirements.txt
python tools/heritage.py verify
python tools/heritage.py search --text 'Graham'
python tools/heritage.py read --path '40_Memory_Wiki_OKF/index.md'
python -m aspace.life list
python -m aspace.life review --domain LD03 --at 2026-10-05T18:00:00Z
python -m unittest discover -s tests -v
(cd portable && python -m unittest -v)
```

Une observation réelle est admise par `python -m aspace.life record --db
runtime-state/life.sqlite --claim observation.json --authority <autorité-source>`.
L'observation doit satisfaire TemporalClaim et porter une preuve, un domaine
LD01–LD08, scope life, observed_at/recorded_at et classification. Une valeur
historique reste HISTORICAL. Le moteur ne vérifie pas la réalité physique affirmée.

`python -m aspace.memory` propose claim, transition, context, replay et backup.
`context --input capsule-request.json` reçoit les arguments du compiler :
holon_id, mission_id, correlation_id, scope, authority_envelope,
workgraph_neighborhood, evidence_head, return_to et cutoff explicite t.
`backup --destination` crée une copie SQLite cohérente sans écraser de cible.

L'autorité passée au CLI est un contrat entre appelants locaux de confiance,
pas une authentification réseau. Un Gateway devra authentifier et autoriser
l'appelant avant d'exposer ces opérations. Le corpus n'autorise aucune mutation.
Les bases runtime sont exclues de Git.

## Reproduction et limites

`tools/import_v3.py` prend un checkout sparse V3 au SHA fixé, vérifie les blobs
contre Git et produit corpus, inventaire, compte rendu et registre Life. Il ne
lance aucun script de V3. Une source modifiée ou un LD manquant fait échouer
l'import. Les sources UTF-8 sont récupérables octet pour octet. Lancer sur une
branche de transfert pour examiner le diff avant intégration.

Les anciens CORE interdisant toute contribution transversale, routeurs retirés,
états GREEN datés et politiques de providers restent historiques. Les classes
V3 en mémoire sont utilisées via Journal pour le chemin durable V4. Le moteur
alternatif core.py n'est pas adopté par accident.

Les liens Windows dans le corpus sont des coordonnées historiques, pas des liens
résolus sur Linux. heritage read/search retrouve les sources incluses ;
l'inventaire retrouve les autres références. La résolution des junctions et des
dépôts externes reste à compléter, notamment l'origin pocketbase-vec.

## Portée restante conservée

Gateway, WorkGraph/Supabase, GWS, incarnations des Doctors, données réelles des
huit LD, Business B1/B2/B3, franchises et 75 services OMK déclarés, Factory Ryan,
Automaton M0/M1/M2, Prime Agent/DeepSeek, BMAD/gstack/CEO Bench, OpenShell/Octop,
surfaces Desktop/Mobile/3D restent dans architecture/capabilities.json.

La copie/reprise du journal sur deux chemins isolés du compute ne vaut pas une
migration certifiée entre deux VPS. Aucun daemon ni reset programmé n'est activé.

## Attribution

Code V3 sous MIT, SHA ci-dessus :
`10_Tech_OS/kernel/temporal_truth/{temporal_truth,compiler,packets,reconciliation}.py`
et `10_Tech_OS/kernel/contracts/TEMPORAL_TRUTH_CONTEXT_V1.schema.json`.
Les imports de réconciliation sont adaptés au package V4 ; les corrections de
persistance et de requête sont dans aspace/journal.py. Les tests adaptés gardent
leurs assertions. source-lock.json porte les empreintes avant/après.
