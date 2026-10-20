#!/usr/bin/env python3
"""Crée les 8 dossiers projet PICARD + dépose les 9 docs d'alignement PARA."""
import json, subprocess, os, sys

PICARD = "17SuVx4Ld0tpYsgL-7l1EWu_O7H81W2ce"
PARA_ROOT = "1fl55pFEoySRsAAto9GF0delUbo_TpHyJ"
BASE = "/home/hatch/workspace/life-os/para"
LOG = os.path.join(BASE, "deploy-results.jsonl")

PROJECTS = [
    ("L1 - LD01 Carrière/Business — Book", "L1 - LD01 Carrière-Business — Book.md"),
    ("L1 - LD02 Finance — Saru", "L1 - LD02 Finance — Saru.md"),
    ("L1 - LD03 Santé — Culber", "L1 - LD03 Santé — Culber.md"),
    ("L1 - LD04 Cognition — Tilly", "L1 - LD04 Cognition — Tilly.md"),
    ("L1 - LD05 Social — Stamets", "L1 - LD05 Social — Stamets.md"),
    ("L1 - LD06 Famille — Burnham", "L1 - LD06 Famille — Burnham.md"),
    ("L1 - LD07 Créativité — Reno", "L1 - LD07 Créativité — Reno.md"),
    ("L1 - LD08 Impact — Georgiou", "L1 - LD08 Impact — Georgiou.md"),
]

def gws(*args):
    r = subprocess.run(["hatch_gws_cli", "drive"] + list(args),
                       capture_output=True, text=True, timeout=300)
    return r

def log(entry):
    with open(LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

results = {"folders_created": [], "uploads": [], "errors": []}

for folder_name, local_file in PROJECTS:
    local = os.path.join(BASE, local_file)
    assert os.path.exists(local), f"manquant: {local}"
    # 1. créer le dossier
    r = gws("files", "create", "--params", '{"ignoreDefaultVisibility":true}',
            "--json", json.dumps({"name": folder_name,
                                  "mimeType": "application/vnd.google-apps.folder",
                                  "parents": [PICARD]}))
    try:
        fid = json.loads(r.stdout).get("id")
    except Exception:
        fid = None
    if not fid:
        results["errors"].append({"op": "mkdir", "folder": folder_name, "stderr": r.stderr[:300]})
        log({"op": "mkdir", "folder": folder_name, "ok": False})
        continue
    results["folders_created"].append({"name": folder_name, "id": fid})
    log({"op": "mkdir", "folder": folder_name, "id": fid, "ok": True})
    # 2. uploader l'index (nom exact du dossier + .md)
    r = gws("+upload", local, "--parent", fid, "--name", folder_name + ".md")
    ok = r.returncode == 0 and '"id"' in r.stdout
    results["uploads"].append({"file": folder_name + ".md", "ok": ok})
    log({"op": "upload", "file": folder_name + ".md", "ok": ok})
    if not ok:
        results["errors"].append({"op": "upload", "file": folder_name + ".md", "stderr": r.stderr[:300]})

# 3. index PARA à la racine de la branche
r = gws("+upload", os.path.join(BASE, "PARA — Index.md"), "--parent", PARA_ROOT,
        "--name", "PARA — Index.md")
ok = r.returncode == 0 and '"id"' in r.stdout
results["uploads"].append({"file": "PARA — Index.md", "ok": ok})
log({"op": "upload", "file": "PARA — Index.md", "ok": ok})

print(json.dumps({"folders": len(results["folders_created"]),
                  "uploads_ok": sum(1 for u in results["uploads"] if u["ok"]),
                  "errors": results["errors"]}, ensure_ascii=False, indent=1))
