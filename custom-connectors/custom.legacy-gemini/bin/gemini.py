#!/usr/bin/env python3
"""CLI générique Google Gemini (clé via Secure Vault, connecteur custom.gemini).

Usage:
    gemini.py --prompt "texte" [--model gemini-3.6-flash] [--system "..."]
    echo "texte" | gemini.py
"""
import argparse
import json
import sys
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/templates/skill/bin")
import dynamic_credentials as dc

HOST = "generativelanguage.googleapis.com"
URL = f"https://{HOST}/v1beta/models/{{model}}:generateContent"


def call(prompt, model="gemini-3.6-flash", system=None, images_b64=()):
    parts = ([{"text": system + "\n\n" + prompt}] if system
             else [{"text": prompt}])
    for img in images_b64:
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": img}})
    body = json.dumps({
        "contents": [{"parts": parts}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 8192},
    }).encode()
    req = urllib.request.Request(
        URL.format(model=model), data=body, method="POST",
        headers={"Content-Type": "application/json"})
    dc.add_surrogate_to_request(req, "custom.gemini", allowed_hosts=[HOST])
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = dc.read_json_response(resp)
    except Exception as e:
        raise SystemExit(f"appel Gemini impossible : {e}")
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise SystemExit(f"réponse Gemini inattendue : {json.dumps(data)[:500]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", default="")
    ap.add_argument("--model", default="gemini-3.6-flash")
    ap.add_argument("--system", default="")
    a = ap.parse_args()
    prompt = a.prompt or sys.stdin.read().strip()
    if not prompt:
        raise SystemExit("prompt vide (argument --prompt ou stdin)")
    print(call(prompt, model=a.model, system=a.system or None))


if __name__ == "__main__":
    main()
