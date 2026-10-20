#!/usr/bin/env python3
"""Importe un export JSON de clés FreeLLMAPI vers la config déclarative.

Usage :
    python3 import-freellmapi-keys.py [export.json] [freellmapi.config.json]

Défauts (dans le Codespace V4) :
    export : $ASPACE_INSTANCE_ROOT/state/freellmapi/freellmapi-keys.json
    sortie : $ASPACE_INSTANCE_ROOT/state/freellmapi/freellmapi.config.json

L'export vient de : app desktop → Keys → Export → JSON
    {"version": 1, "exportedAt": "...", "source": "freellmapi",
     "keys": [{"platform": "...", "key": "...", "label": "..."}]}

La sortie est la config déclarative FreeLLMAPI (FREEAPI_CONFIG_PATH) :
    {"keys": [{"platform": "...", "key": "...", "label": "...", "enabled": true}]}

Idempotent côté serveur : les clés existantes sont mises à jour, pas dupliquées.
Relançable sans risque quand on fabrique des centaines de clés.

Sécurité : ce script ne journalise JAMAIS les valeurs de clés (comptes seulement).
La sortie vit sous state/ (hors git).
"""
import json
import os
import sys
from collections import Counter

ASPACE = os.environ.get("ASPACE_INSTANCE_ROOT", "/workspaces/aspace")
STATE = os.path.join(ASPACE, "state", "freellmapi")


def main() -> int:
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(STATE, "freellmapi-keys.json")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(STATE, "freellmapi.config.json")

    if not os.path.isfile(src):
        print(f"✗ export introuvable : {src}", file=sys.stderr)
        print("  Exporter depuis l'app desktop : Keys → Export → JSON, puis placer le fichier ici.",
              file=sys.stderr)
        return 1

    with open(src, encoding="utf-8") as fh:
        data = json.load(fh)

    raw_keys = data.get("keys") if isinstance(data, dict) else None
    if not isinstance(raw_keys, list) or not raw_keys:
        print("✗ format inattendu : 'keys' absent ou vide", file=sys.stderr)
        return 1

    seen = set()
    out_keys = []
    skipped = 0
    for k in raw_keys:
        platform = (k.get("platform") or "").strip()
        key = (k.get("key") or "").strip()
        label = (k.get("label") or "").strip()
        if not platform or not key:
            skipped += 1
            continue
        if (platform, key) in seen:
            skipped += 1
            continue
        seen.add((platform, key))
        out_keys.append({
            "platform": platform,
            "key": key,
            "label": label,
            "enabled": True,
        })

    if not out_keys:
        print("✗ aucune clé valide dans l'export", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    with open(dst, "w", encoding="utf-8") as fh:
        json.dump({"keys": out_keys}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.chmod(dst, 0o600)

    per_platform = Counter(k["platform"] for k in out_keys)
    print(f"✓ {len(out_keys)} clés → {dst} (600)")
    for plat, n in sorted(per_platform.items()):
        print(f"  {plat}: {n}")
    if skipped:
        print(f"  ({skipped} entrée(s) ignorée(s) : vide ou doublon)")
    print("Relancer setup-freellmapi.sh pour appliquer (FREEAPI_CONFIG_PATH).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
