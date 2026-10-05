# Bill : WATCH, première compétence perceptive V4

Code amont MIT présent dans `.agents/skills/watch`, version 0.3.2, commit
`03ceb42f7fa2c4439aca01752118044baabffb8f`. Copie suivie, licence conservée.
Le lock `watch.lock.json` permet de vérifier l'intégrité des fichiers distribués.
Ne pas installer une mise à jour flottante qui change silencieusement les preuves.

## Exécution sur le compute cloud

```sh
python .agents/skills/watch/scripts/setup.py --json
python .agents/skills/watch/scripts/watch.py /path/in/cloud/video.mp4 --engine local --detail efficient --no-whisper --out-dir /durable/watch --question "Question de la mission"
```

FFmpeg et ffprobe sont requis pour la voie frames. yt-dlp est requis pour les URL
de cette voie. WhisperX est une option séparée pour les vidéos sans sous-titres.
« local » désigne le compute du harness, jamais une obligation d'utiliser le PC.

Avec une clé `GEMINI_API_KEY` injectée dans le runtime :

```sh
python .agents/skills/watch/scripts/watch.py 'https://www.youtube.com/watch?v=VIDEO_ID' --engine gemini --question "Question de la mission" --out-dir /durable/watch
```

Le choix du moteur est explicite. Pour Gemini, l'observation est attribuée à
Gemini ; pour les frames, Bill doit effectivement consulter les images. Une
transcription seule ne prouve pas ce qui est visible. Les fichiers privés ne sont
pas envoyés à un provider par simple auto-détection d'une clé. Pas de promesse
de gratuité, de couverture totale ni de latence tirée d'une vidéo promotionnelle.

Le rapport conserve URL/origine, question, moteur/version, timestamps, modalités
présentes et manquantes. Capturer rapport et références durables via `memory.py`.
Une sortie sans audio reste une observation visuelle partielle. Aucun résultat
de modèle n'est promu en canon uniquement parce que le processus retourne zéro.

## Réception

Un canary synthétique sans clé valide le décodage, la sélection de frames et le
rapport. Il ne valide ni YouTube, ni Gemini, ni la transcription WhisperX. Une
vidéo réelle et les credentials du runtime seront nécessaires pour ces preuves.

L'installation dans le dépôt rend le skill disponible aux harness compatibles
qui ouvrent ce dépôt. Elle ne crée pas une session Bill active ni un Codespace.
