#!/usr/bin/env python3
"""Watch — pipeline d'analyse vidéo YouTube (spec V4 : frames + transcripts horodatés).

Usage:
    watch.py --url <youtube-url> [--frames N] [--out rapport.md]
             [--model gemini-3.6-flash] [--lang en,fr]

Étapes : métadonnées -> transcription VTT horodatée -> frames (fallback ou forcé)
-> analyse Gemini -> rapport Markdown. Sans GEMINI_API_KEY, l'analyse est sautée.
"""
import argparse
import base64
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import date

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.expanduser("~/workspace/watch-reports")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
YTDLP = (shutil.which("yt-dlp")
         or os.path.join(os.path.dirname(sys.executable), "yt-dlp"))

VIDEO_ID_RE = re.compile(
    r"(?:youtube\.com/(?:watch\?.*v=|shorts/|embed/|live/)|youtu\.be/)([A-Za-z0-9_-]{11})"
)
_DC = None


def _dc():
    """Helper d'authentification dynamique (Secure Vault). None si indisponible."""
    global _DC
    if _DC is None:
        sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/templates/skill/bin")
        import dynamic_credentials as _mod
        _DC = _mod
    return _DC


def gemini_available():
    if os.environ.get("GEMINI_API_KEY"):
        return True
    try:
        _dc().dynamic_credential_entry("custom.gemini")
        return True
    except Exception:
        return False


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=kw.pop("timeout", 180), **kw)


def video_id(url):
    m = VIDEO_ID_RE.search(url)
    if not m:
        raise SystemExit(f"URL YouTube non reconnue : {url}")
    return m.group(1)


def ytdlp(args, timeout=180):
    return run([YTDLP] + args, timeout=timeout)


def fetch_metadata(url):
    """Métadonnées JSON via yt-dlp (pas de téléchargement)."""
    r = ytdlp(["--dump-single-json", "--no-playlist", "--skip-download",
               "--no-warnings", url])
    if r.returncode != 0:
        return {"error": (r.stderr or r.stdout)[-500:]}
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"error": "réponse yt-dlp illisible"}
    chapters = [{"start": c.get("start_time"), "title": c.get("title")}
                for c in (data.get("chapters") or [])]
    return {
        "video_id": data.get("id"),
        "title": data.get("title"),
        "channel": data.get("channel") or data.get("uploader"),
        "upload_date": data.get("upload_date"),
        "duration_s": data.get("duration"),
        "view_count": data.get("view_count"),
        "description": (data.get("description") or "")[:4000],
        "chapters": chapters,
    }


def vtt_to_segments(vtt_text):
    """Parse un VTT en segments (start_s, text).

    Déduplique les sous-titres auto-générés qui répètent la ligne précédente
    d'un segment à l'autre (rolling captions).
    """
    segs = []
    ts = re.compile(r"(\d+):(\d+):(\d+)\.\d+ -->")
    cur_start, cur_lines, last_text = None, [], None
    for line in vtt_text.splitlines():
        m = ts.match(line)
        if m:
            if cur_start is not None and cur_lines:
                text = " ".join(cur_lines).strip()
                if text and text != last_text:
                    segs.append({"start_s": cur_start, "text": text})
                    last_text = text
            h, mi, s = map(int, m.groups())
            cur_start, cur_lines = h * 3600 + mi * 60 + s, []
        elif line.strip() and not line.strip().isdigit() and "WEBVTT" not in line:
            clean = re.sub(r"<[^>]+>", "", line).strip()
            if clean:
                cur_lines.append(clean)
    if cur_start is not None and cur_lines:
        text = " ".join(cur_lines).strip()
        if text and text != last_text:
            segs.append({"start_s": cur_start, "text": text})
    return segs


def fetch_transcript(url, tmpdir, langs):
    """Télécharge les sous-titres (manuels puis auto) et les parse."""
    sub_langs = ",".join(f"{l}.*" for l in langs) + ",en.*,fr.*"
    r = ytdlp(["--write-subs", "--write-auto-subs", "--sub-langs", sub_langs,
               "--sub-format", "vtt", "--skip-download", "--no-warnings",
               "-o", os.path.join(tmpdir, "subs.%(ext)s"), url])
    vtts = [f for f in os.listdir(tmpdir) if f.endswith(".vtt")]
    if not vtts:
        reason = (r.stderr or "")[-300:]
        blocked = "429" in reason or "bot" in reason.lower() or "sign in" in reason.lower()
        return [], ("accès automatisé bloqué par YouTube (429/bot-check)"
                    if blocked else f"aucune piste de sous-titres ({reason.strip() or 'inconnu'})")
    vtts.sort(key=lambda f: (".auto." in f, f))
    with open(os.path.join(tmpdir, vtts[0]), encoding="utf-8", errors="replace") as fh:
        return vtt_to_segments(fh.read()), ""


def extract_frames(url, tmpdir, n, duration_s):
    """Télécharge la vidéo (pire qualité) et extrait N frames JPEG."""
    if not duration_s or duration_s <= 0:
        return [], "durée inconnue, frames impossibles"
    target = os.path.join(tmpdir, "video.mp4")
    r = ytdlp(["-f", "worst[ext=mp4]/worst", "--no-warnings", "-o", target, url],
              timeout=600)
    if r.returncode != 0 or not os.path.exists(target):
        return [], f"téchargement vidéo impossible ({(r.stderr or '')[-200:].strip()})"
    step = max(1, int(duration_s / n))
    out_pat = os.path.join(tmpdir, "frame-%03d.jpg")
    r = run(["ffmpeg", "-y", "-v", "error", "-i", target,
             "-vf", f"fps=1/{step},scale=768:-1", out_pat], timeout=600)
    frames = sorted(f for f in os.listdir(tmpdir)
                    if f.startswith("frame-") and f.endswith(".jpg"))[:n]
    return [os.path.join(tmpdir, f) for f in frames], ""


def gemini_analyze(model, meta, transcript, frame_paths):
    """Envoie transcription et/ou frames à Gemini, retourne le texte d'analyse.

    Auth : connecteur Secure Vault (custom.gemini) en priorité,
    sinon GEMINI_API_KEY (contexte GitHub Action).
    """
    parts = [{"text": build_prompt(meta, transcript, bool(frame_paths))}]
    for fp in frame_paths:
        with open(fp, "rb") as fh:
            parts.append({"inline_data": {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(fh.read()).decode()}})
    body = json.dumps({"contents": [{"parts": parts}],
                       "generationConfig": {"temperature": 0.4,
                                            "maxOutputTokens": 8192}}).encode()
    req = urllib.request.Request(
        GEMINI_URL.format(model=model),
        data=body, method="POST",
        headers={"Content-Type": "application/json"})
    use_dc = False
    try:
        dc = _dc()
        dc.add_surrogate_to_request(
            req, "custom.gemini",
            allowed_hosts=["generativelanguage.googleapis.com"])
        use_dc = True
    except Exception:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            return ("[analyse Gemini impossible : connecteur Secure Vault "
                    "indisponible et GEMINI_API_KEY absente]")
        req.add_header("x-goog-api-key", api_key)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = _dc().read_json_response(resp) if use_dc else json.load(resp)
    except Exception as e:
        return f"[analyse Gemini impossible : {e}]"
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return f"[réponse Gemini inattendue : {json.dumps(data)[:500]}]"


def build_prompt(meta, transcript, has_frames):
    tlines = "\n".join(f"[{s['start_s']//60:02d}:{s['start_s']%60:02d}] {s['text']}"
                       for s in transcript[:4000])
    return f"""Tu analyses une vidéo YouTube pour un entrepreneur (systèmes, IA, automatisation).
Réponds en français, format Markdown, avec timestamps [mm:ss] quand tu cites.

VIDÉO : {meta.get('title')} — {meta.get('channel')} ({meta.get('duration_s')}s)
DESCRIPTION : {(meta.get('description') or '')[:1500]}

{'TRANSCRIPTION HORODATÉE :' if tlines else 'PAS DE TRANSCRIPTION DISPONIBLE.'}
{tlines[:120000]}

{'Des frames de la vidéo sont jointes comme images.' if has_frames else 'Aucune frame jointe.'}

PRODUIS :
1. **Résumé** (5 lignes max)
2. **Thèses clés** (avec timestamps)
3. **Structure / chapitres**
4. **Éléments réutilisables** (idées, méthodes, chiffres actionnables)
5. **Verdict** (1 phrase : vaut-elle le temps d'un visionnage complet ?)
"""


def write_report(path, meta, transcript, frame_paths, transcript_note,
                 frame_note, analysis):
    dur = meta.get("duration_s") or 0
    lines = [
        f"# Watch — {meta.get('title') or 'sans titre'}",
        "",
        f"- Chaîne : {meta.get('channel')} | Durée : {dur//60} min {dur%60:02d} s"
        f" | Vues : {meta.get('view_count')}",
        f"- URL : https://www.youtube.com/watch?v={meta.get('video_id')}",
        f"- Transcription : {len(transcript)} segments"
        + (f" ({transcript_note})" if transcript_note and not transcript else ""),
        f"- Frames : {len(frame_paths)}"
        + (f" ({frame_note})" if frame_note and not frame_paths else ""),
        "",
    ]
    if meta.get("chapters"):
        lines += ["## Chapitres",
                  *[f"- [{c['start']//60:02d}:{c['start']%60:02d}] {c['title']}"
                    for c in meta["chapters"] if c.get("start") is not None], ""]
    lines += ["## Analyse", "", analysis or "_analyse non effectuée (clé Gemini absente)_", ""]
    if transcript:
        lines += ["## Transcription (extraits)", ""]
        lines += [f"[{s['start_s']//60:02d}:{s['start_s']%60:02d}] {s['text']}"
                  for s in transcript[:200]]
        lines += [""]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return path


def main():
    ap = argparse.ArgumentParser(description="Watch — analyse vidéo YouTube (spec V4).")
    ap.add_argument("--url", required=True)
    ap.add_argument("--frames", type=int, default=0,
                    help="0 = auto (frames seulement si pas de transcription)")
    ap.add_argument("--out", default="")
    ap.add_argument("--model", default="gemini-3.6-flash")
    ap.add_argument("--lang", default="en,fr")
    a = ap.parse_args()

    vid = video_id(a.url)
    langs = [l.strip() for l in a.lang.split(",") if l.strip()]
    out = a.out or os.path.join(REPORTS_DIR, f"{vid}-{date.today():%Y-%m-%d}.md")

    meta = fetch_metadata(a.url)
    if "error" in meta:
        print(json.dumps({"video_id": vid, "error": meta["error"][:300]}))
        raise SystemExit(1)

    transcript, t_note, frames, f_note = [], "", [], ""
    with tempfile.TemporaryDirectory(prefix="watch-") as tmp:
        transcript, t_note = fetch_transcript(a.url, tmp, langs)
        want_frames = a.frames > 0 or not transcript
        if want_frames:
            n = a.frames if a.frames > 0 else 12
            frames, f_note = extract_frames(a.url, tmp, n, meta.get("duration_s"))
        api_ok = gemini_available()
        analysis = (gemini_analyze(a.model, meta, transcript, frames)
                    if api_ok else "")
        report = write_report(out, meta, transcript, frames, t_note, f_note, analysis)

    summary = {"video_id": vid, "title": meta.get("title"),
               "transcript_segments": len(transcript),
               "transcript_note": t_note, "frames": len(frames),
               "frame_note": f_note,
               "analyzed": bool(analysis) and not analysis.startswith("[analyse"),
               "report": report}
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
