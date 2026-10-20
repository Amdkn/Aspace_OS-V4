

# Watch

## Purpose
Analyser une vidéo YouTube et produire un rapport d'analyse structuré en français :
thèses clés, structure narrative, chapitres, éléments réutilisables.
Pipeline : métadonnées → transcription horodatée (VTT) → frames vidéo (si besoin)
→ analyse Gemini → rapport Markdown.

## Tooling
Interpreter dédié (venv avec `yt-dlp`) + `ffmpeg` système :

```bash
~/.venvs/watch/bin/python ~/workspace/custom-skills/local-watch/bin/watch.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  [--frames 12] [--out rapport.md] [--model gemini-3.6-flash] [--lang en,fr]
```

Comportement :
- `--frames 0` (défaut) : transcription d'abord ; si aucune piste de sous-titres,
  télécharge la vidéo (plus basse qualité) et extrait des frames réparties sur la durée.
- `--frames N` : force l'extraction de N frames + transcription si disponible.
- Le rapport est écrit dans `~/workspace/watch-reports/<video_id>-<date>.md` par défaut.
- Résumé JSON sur stdout : `{"video_id","title","transcript_segments","frames","report"}`.

## Auth
- Connecteur `custom.gemini` (Secure Vault) : utilisé en priorité, sans exposer
  la clé. Ne jamais demander la clé en clair ni l'écrire dans un fichier.
- Fallback `GEMINI_API_KEY` (variable d'environnement) : pour le contexte
  GitHub Action uniquement (`assets/watch-video.yml`, secret `GEMINI_API_KEY`).
- Sans authentification : métadonnées/transcription/frames fonctionnent,
  l'analyse Gemini est sautée et le rapport contient les données brutes.

## Operating Rules
1. YouTube bloque parfois l'accès automatisé depuis ce serveur (429 / bot-check).
   En cas d'échec, le script enregistre la cause exacte et le rapport dégrade
   gracieusement (métadonnées + description + chapitres) au lieu d'inventer.
2. Ne jamais contourner un CAPTCHA ou un contrôle anti-bot.
3. Ne jamais affirmer qu'une transcription existe si aucune piste n'a été extraite.
4. Les frames sont redimensionnées (max 768px) avant envoi à Gemini — quota oblige.
5. Variante GitHub Actions : voir `assets/watch-video.yml` (secret `GEMINI_API_KEY`
   dans le repo, déclenchement manuel `workflow_dispatch`).
## Available connectors

Use `muse.connector_search` to find the current connector docs before following
recovered instructions.
