#!/usr/bin/env python3
"""Aligne les 8 projets L1 + 8 seeds Linear avec Drive PARA et GitHub."""
import json, subprocess

GH = "https://github.com/Amdkn/Aspace_OS-V4"
PARA_IDX = "https://drive.google.com/drive/folders/1fl55pFEoySRsAAto9GF0delUbo_TpHyJ"
MARK = "ALIGNEMENT CROSS-SURFACE — 2026-10-09"
D = "https://drive.google.com/drive/folders/"

LD = [
 ("P-SOH-20","L1 - LD01 Carrière/Business — Book","1QjJbUeghwUA91Ls1U5DogiE3SEFijzmq","BOOK","1-GFocLMm24EikWvi1YGeEucTPMA80euD",
  "https://linear.app/aspace-os/project/l1-ld01-carrierebusiness-book-82ecf7419645",
  "SOH-145","https://linear.app/aspace-os/issue/SOH-145/bedrock-l1-amorcage-ld01-carrierebusiness"),
 ("P-SOH-21","L1 - LD02 Finance — Saru","1NYs1dZluu91Z4LxMT1LoxF7pMhWY2qW9","SARU","1GxxjZ5T3DcNkipe1CDPB-51TWr9eaPqJ",
  "https://linear.app/aspace-os/project/l1-ld02-finance-saru-324a1ac5fdf7",
  "SOH-146","https://linear.app/aspace-os/issue/SOH-146/bedrock-l1-amorcage-ld02-finance"),
 ("P-SOH-22","L1 - LD03 Santé — Culber","1TYqMoVjHwy5zwIx2MbDeq1EcI6AU-bKS","CULB","1MrnFBHrZI19GsuNZ0mnCnJqNud4g-ScE",
  "https://linear.app/aspace-os/project/l1-ld03-sante-culber-85603a7312c0",
  "SOH-147","https://linear.app/aspace-os/issue/SOH-147/bedrock-l1-amorcage-ld03-sante"),
 ("P-SOH-23","L1 - LD04 Cognition — Tilly","1vgvZPgZeyGruXRUOSyfgeY_9yTmn0oUa","TIL","1cRCdexwrSNIRLjlm7znXuYxp01CE4QJg",
  "https://linear.app/aspace-os/project/l1-ld04-cognition-tilly-ad46761587eb",
  "SOH-148","https://linear.app/aspace-os/issue/SOH-148/bedrock-l1-amorcage-ld04-cognition"),
 ("P-SOH-24","L1 - LD05 Social — Stamets","1hjp4EtgOfZonMHFdHuIHQn_a1x3DjZvu","STAM","1AOHLzXIjdOZD16DhY0hFCw4mlXErtRow",
  "https://linear.app/aspace-os/project/l1-ld05-social-stamets-fddffd7bc21b",
  "SOH-149","https://linear.app/aspace-os/issue/SOH-149/bedrock-l1-amorcage-ld05-social"),
 ("P-SOH-25","L1 - LD06 Famille — Burnham","1uy4AqY9-cCJ_-D3mSzvHo-Hl7ac3daBh","BURN","1uoJccmrXkVMA4VcA4JMFAdzn45LEnrmT",
  "https://linear.app/aspace-os/project/l1-ld06-famille-burnham-15558ff985e0",
  "SOH-150","https://linear.app/aspace-os/issue/SOH-150/bedrock-l1-amorcage-ld06-famille"),
 ("P-SOH-26","L1 - LD07 Créativité — Reno","1WKyaXmSAyr9rhQ1zBGH1EalveeQiySAR","RENO","1wHtFdMPIs-qIfSQGr2K5TJoNCW8GRzBD",
  "https://linear.app/aspace-os/project/l1-ld07-creativite-reno-f1a74dc48fa6",
  "SOH-151","https://linear.app/aspace-os/issue/SOH-151/bedrock-l1-amorcage-ld07-creativite"),
 ("P-SOH-27","L1 - LD08 Impact — Georgiou","1DKh7aX1THXkAmCOpI_qfWCB94Db3qOfK","GEOR","1n3s-1bOO_FSYqchPrQA8XqewFhloaVPp",
  "https://linear.app/aspace-os/project/l1-ld08-impact-georgiou-99f1a6fa9c35",
  "SOH-152","https://linear.app/aspace-os/issue/SOH-152/bedrock-l1-amorcage-ld08-impact"),
]

def call(tool, args):
    r = subprocess.run(["linear","call-tool","--name",tool,"--arguments-json",json.dumps(args)],
                       capture_output=True, text=True, timeout=120)
    return json.loads(r.stdout)

def get_project(pid):
    d = call("get_project", {"query": pid})
    t = json.loads(d["result"]["content"][0]["text"])
    return t.get("project", t)

def get_issue(iid):
    d = call("get_issue", {"id": iid})
    t = json.loads(d["result"]["content"][0]["text"])
    return t.get("issue", t)

results = {"projects": [], "issues": [], "errors": []}

for pid, pname, picard, code, b1, purl, seed, surl in LD:
    try:
        pr = get_project(pid)
        desc = pr.get("description") or ""
        if MARK in desc:
            results["projects"].append({"id": pid, "status": "déjà aligné"})
            continue
        block = f"""
---

## {MARK}

- **Drive — dossier projet PICARD** : [{pname}]({D+picard})
- **Drive — B1** : [B1 {code} — Direction]({D+b1}) (encapsule les 8 L2)
- **Drive — index PARA** : [PARA — Index]({PARA_IDX})
- **GitHub** : [Amdkn/Aspace_OS-V4]({GH}) · [PR #22]({GH}/pull/22) (review humaine en attente — vérifié 2026-10-08)
- **Seed issue** : [{seed}]({surl})

Nomenclature : le dossier Drive PICARD porte exactement le nom de ce projet Linear.
Note : les lignes « IMBRICATION L2 (proposition V1, à valider) » ci-dessus sont remplacées par la doctrine fractale 8×8 (les 8 fonctions Business sont transverses aux 8 domaines Life) — voir « Matrice fractale 8x8 » dans A3 SPOCK — Areas."""
        r = call("save_project", {"id": pid, "description": desc.rstrip() + "\n" + block})
        ok = r.get("ok") and not r.get("result", {}).get("isError")
        results["projects"].append({"id": pid, "status": "aligné" if ok else "ÉCHEC"})
        if not ok: results["errors"].append({"id": pid, "resp": str(r)[:300]})
    except Exception as e:
        results["projects"].append({"id": pid, "status": f"ERREUR {e}"})

for pid, pname, picard, code, b1, purl, seed, surl in LD:
    try:
        iss = get_issue(seed)
        desc = iss.get("description") or ""
        if MARK in desc:
            results["issues"].append({"id": seed, "status": "déjà alignée"})
            continue
        block = f"""
---

## {MARK}

- **Drive — dossier projet PICARD** : [{pname}]({D+picard})
- **Drive — B1** : [B1 {code} — Direction]({D+b1})
- **Projet Linear** : [{pname}]({purl})"""
        r = call("save_issue", {"id": seed, "description": desc.rstrip() + "\n" + block})
        ok = r.get("ok") and not r.get("result", {}).get("isError")
        results["issues"].append({"id": seed, "status": "alignée" if ok else "ÉCHEC"})
        if not ok: results["errors"].append({"id": seed, "resp": str(r)[:300]})
    except Exception as e:
        results["issues"].append({"id": seed, "status": f"ERREUR {e}"})

print(json.dumps(results, ensure_ascii=False, indent=1))
