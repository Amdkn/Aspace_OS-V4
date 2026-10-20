#!/usr/bin/env python3
"""Test preuve-de-capacité : ingérer une vidéo YouTube via l'API Gemini (fileData.fileUri).
La vidéo est récupérée par l'infrastructure Google — l'IP de la VM ne touche jamais YouTube.
Usage: youtube-via-gemini.py <video_id_ou_url> [--model gemini-3.6-flash]
"""
import json
import sys
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
import dynamic_credentials as dc

HOST = "generativelanguage.googleapis.com"
URL = f"https://{HOST}/v1beta/models/{{model}}:generateContent"

PROMPT = (
    "Analyse cette vidéo YouTube en français. Réponds en français avec :\n"
    "1. Titre et thèse centrale (2-3 phrases).\n"
    "2. Les 5 points clés développés (puces).\n"
    "3. Trois citations marquantes (en anglais d'origine + traduction française).\n"
    "4. Durée approximative et structure (chapitres si identifiables).\n"
    "Ne résume pas à partir de tes connaissances : base-toi uniquement sur le contenu de la vidéo."
)


def call(video_url, model="gemini-3.6-flash"):
    body = json.dumps({
        "contents": [{
            "parts": [
                {"file_data": {"file_uri": video_url}},
                {"text": PROMPT},
            ]
        }],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 8192},
    }).encode()
    req = urllib.request.Request(
        URL.format(model=model), data=body, method="POST",
        headers={"Content-Type": "application/json"})
    dc.add_surrogate_to_request(req, "custom.gemini", allowed_hosts=[HOST])
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = dc.read_json_response(resp)
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise SystemExit(f"réponse inattendue : {json.dumps(data)[:800]}")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: youtube-via-gemini.py <video_id_ou_url> [--model X]")
    vid = sys.argv[1]
    model = "gemini-3.6-flash"
    if "--model" in sys.argv:
        model = sys.argv[sys.argv.index("--model") + 1]
    url = vid if vid.startswith("http") else f"https://www.youtube.com/watch?v={vid}"
    print(call(url, model=model))


if __name__ == "__main__":
    main()
