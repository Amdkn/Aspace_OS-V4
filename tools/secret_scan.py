#!/usr/bin/env python3
"""Secret scan — P-003 (L05, D-N027).

Grep de patterns de secrets sur le repo. Tier D : pur code, zéro modèle.
Pattern trouvé → exit 1 (check rouge). Aucune écriture.

Patterns : JWT (eyJ…), Supabase sb_secret_/sbp_, clés AWS AKIA…,
tokens GitHub (préfixes ghp_ / github_pat_), clés privées PEM, service_role assigné,
clés sk-*. Les fichiers binaires et les répertoires .git/node_modules
sont exclus ; les exemples de docs marqués placeholder/REPLACE_WITH sont
ignorés.

Usage : python3 tools/secret_scan.py [--root .]
"""

import argparse
import os
import re
import sys

PATTERNS = [
    (r"eyJ[A-Za-z0-9_-]{20,}", "JWT"),
    (r"sb_secret_[A-Za-z0-9_-]{10,}", "supabase-secret"),
    (r"sbp_[A-Za-z0-9]{20,}", "supabase-personal-token"),
    (r"AKIA[0-9A-Z]{16}", "aws-access-key"),
    (r"ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}", "github-token"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "private-key"),
    (r"service_role['\"]?\s*[:=]\s*['\"][^'\"]{10,}", "service-role-assigned"),
    (r"sk-[A-Za-z0-9]{24,}", "api-key-sk"),
]

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
SKIP_FILES = ("package-lock.json", "pnpm-lock.yaml", "yarn.lock")  # lockfiles générés : blobs base64, jamais des secrets
PLACEHOLDER_HINTS = ("placeholder", "replace_with", "<REPLACE", "abcd1234",
                     "test.supabase", "example", "EXAMPLE")


def iter_text_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in SKIP_FILES:
                continue
            p = os.path.join(dirpath, fn)
            try:
                with open(p, "rb") as f:
                    head = f.read(4096)
                if b"\x00" in head:
                    continue  # binaire
                yield p
            except OSError:
                continue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    hits = 0
    for path in iter_text_files(args.root):
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        lowered = text.lower()
        if any(h in lowered for h in PLACEHOLDER_HINTS) and "eyJ" not in text:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            if any(h in low for h in PLACEHOLDER_HINTS):
                continue
            for pat, label in PATTERNS:
                if re.search(pat, line):
                    print(f"SECRET-SCAN FAIL [{label}]: {path}:{lineno}")
                    hits += 1
                    break
    if hits:
        print(f"\n{hits} secret(s) détecté(s) — P-003 violée.")
        return 1
    print("SECRET-SCAN OK: aucun secret détecté.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
