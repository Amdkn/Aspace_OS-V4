#!/usr/bin/env python3
"""Upload séquentiel des 167 fichiers .md vers Drive, dans l'ordre du manifeste."""
import json, subprocess, sys, os

MANIFEST = "/home/hatch/workspace/life-os/b3members/uploads.json"
LOG = "/home/hatch/workspace/life-os/b3members/upload-results.jsonl"
PROGRESS = "/home/hatch/workspace/life-os/b3members/progress.txt"

entries = json.load(open(MANIFEST))
done = set()
if os.path.exists(LOG):
    for line in open(LOG):
        try:
            done.add(json.loads(line)["index"])
        except Exception:
            pass

print(f"total={len(entries)} déjà_faits={len(done)}", flush=True)

for i, e in enumerate(entries):
    if i in done:
        continue
    if i < 1:  # index 0 déjà uploadé manuellement
        with open(LOG, "a") as f:
            f.write(json.dumps({"index": i, "status": "ok", "name": e["name"], "parent": e["parent"], "id": "1pnncgIRR52x2oSahTjI7HSUF3H_xKIiw", "note": "upload manuel"}) + "\n")
        continue
    cmd = ["hatch_gws_cli", "drive", "+upload", e["local"],
           "--parent", e["parent"], "--name", e["name"]]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd="/home/hatch")
        out = (r.stdout or "") + (r.stderr or "")
        if r.returncode == 0:
            try:
                fid = json.loads(r.stdout).get("id", "?")
            except Exception:
                fid = "?"
            status, note = "ok", fid
        else:
            low = out.lower()
            if "denied" in low or "refus" in low or "approval" in low:
                status, note = "refused", out.strip()[:300]
            else:
                status, note = "error", out.strip()[:300]
    except subprocess.TimeoutExpired:
        status, note = "error", "timeout 180s"
    except Exception as ex:
        status, note = "error", str(ex)[:300]
    with open(LOG, "a") as f:
        f.write(json.dumps({"index": i, "status": status, "name": e["name"], "parent": e["parent"], "note": note}) + "\n")
    with open(PROGRESS, "w") as f:
        f.write(f"{i+1}/{len(entries)} dernier={status} {e['name']}\n")
    print(f"{i+1}/{len(entries)} {status} {e['name']}", flush=True)

print("TERMINE", flush=True)
