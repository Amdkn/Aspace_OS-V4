#!/usr/bin/env python3
"""Check R10 — « sans reçu, pas de merge » (L01, D-N027).

Pur code, zéro modèle. Vérifie, pour une PR vers `main` :
  1. l'intégrité du bloc genesis (hash + 22 reçus présents) ;
  2. la validité de tous les reçus de `ledger/receipts/` (schéma v1, 5 champs) ;
  3. l'existence d'un reçu valide référençant le head SHA de la PR (ou le numéro de PR).

Usage :
  python3 tools/check_r10_receipt.py --root . --head-sha <SHA> --pr-number <N>
  python3 tools/check_r10_receipt.py --root . --selftest

Exit 0 = reçu trouvé et valide (merge autorisé par le ledger).
Exit 1 = pas de reçu valide (check rouge, merge bloqué).
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SCHEMA_ID = "aspace.r10-receipt.v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
PRREF = re.compile(r"^#\d+$")
GENESIS_COUNT = 22


def parse_iso(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def validate_receipt(path):
    """Retourne (ok, erreurs, data). Un reçu incomplet est refusé."""
    errors = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # JSON illisible = reçu invalide
        return False, [f"{path.name}: JSON illisible ({exc})"], None
    if data.get("schema") != SCHEMA_ID:
        errors.append(f"{path.name}: schema != {SCHEMA_ID}")
    if not data.get("entry_id"):
        errors.append(f"{path.name}: entry_id manquant")
    if not data.get("mission_id"):
        errors.append(f"{path.name}: mission_id manquant")
    sha = data.get("sha", "")
    if not (SHA40.match(sha) or PRREF.match(sha)):
        errors.append(f"{path.name}: sha invalide (40 hex ou #PR requis)")
    obs, rec = parse_iso(data.get("observed_at", "")), parse_iso(data.get("recorded_at", ""))
    if obs is None:
        errors.append(f"{path.name}: observed_at illisible")
    if rec is None:
        errors.append(f"{path.name}: recorded_at illisible")
    if obs is not None and rec is not None and rec < obs:
        errors.append(f"{path.name}: recorded_at < observed_at (reçu antidaté, refusé)")
    proof = data.get("proof")
    if not (isinstance(proof, list) and proof and all(isinstance(p, str) and p for p in proof)):
        errors.append(f"{path.name}: proof vide ou invalide")
    if not data.get("issuer"):
        errors.append(f"{path.name}: issuer manquant")
    return not errors, errors, data


def check_genesis(root):
    """Intégrité du bloc genesis : hash + 22 reçus présents, jamais réécrits."""
    errors = []
    gdir = root / "ledger" / "genesis"
    receipts, hashfile = gdir / "receipts.md", gdir / "genesis.sha256"
    if not receipts.exists() or not hashfile.exists():
        return ["genesis: receipts.md ou genesis.sha256 absent"]
    digest = hashlib.sha256(receipts.read_bytes()).hexdigest()
    expected = hashfile.read_text(encoding="utf-8").strip()
    if digest != expected:
        errors.append("genesis: hash mismatch — le bloc genesis a été modifié (interdit)")
    count = receipts.read_text(encoding="utf-8").count("## G-20261009-")
    if count != GENESIS_COUNT:
        errors.append(f"genesis: {count} reçus trouvés, {GENESIS_COUNT} attendus")
    return errors


def receipt_matches(data, head_sha, pr_number):
    if data.get("sha") == head_sha:
        return True
    if pr_number:
        if data.get("sha") == f"#{pr_number}":
            return True
        for p in data.get("proof", []):
            if f"/pull/{pr_number}" in p or p == f"#{pr_number}":
                return True
    return False


def run_check(root, head_sha, pr_number):
    problems = []
    problems += check_genesis(root)
    rdir = root / "ledger" / "receipts"
    matched = None
    if not rdir.exists():
        problems.append("ledger/receipts/ absent")
    else:
        for path in sorted(rdir.glob("*.json")):
            ok, errs, data = validate_receipt(path)
            problems += errs
            if ok and data and receipt_matches(data, head_sha, pr_number):
                matched = data
    if problems:
        for p in problems:
            print(f"R10-FAIL: {p}")
        return 1
    if matched is None:
        print(f"R10-FAIL: aucun reçu valide pour head {head_sha} / PR #{pr_number} — sans reçu, pas de merge.")
        return 1
    print(f"R10-OK: reçu {matched['entry_id']} (mission {matched['mission_id']}) couvre ce merge.")
    return 0


def selftest(root):
    """Teste le check lui-même : genesis + reçus présents valides, et un head inconnu refusé."""
    rc_known = run_check(root, "b80c85969a53ac958a901c6fb95f27d47df7823f", None)
    rc_unknown = run_check(root, "0" * 40, 99999)
    print(f"selftest: head connu -> {rc_known} (attendu 0) ; head inconnu -> {rc_unknown} (attendu 1)")
    return 0 if (rc_known == 0 and rc_unknown == 1) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--head-sha", default="")
    ap.add_argument("--pr-number", type=int, default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)
    if args.selftest:
        return selftest(root)
    if not args.head_sha:
        print("R10-FAIL: --head-sha requis")
        return 1
    return run_check(root, args.head_sha, args.pr_number)


if __name__ == "__main__":
    sys.exit(main())
