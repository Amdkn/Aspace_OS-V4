#!/usr/bin/env python3
"""Ports check — P-004 (L05, D-N027).

Croise les ports bindés dans le code avec les ports documentés dans
os/PORTS.md. Tier D : pur code, zéro modèle. Un service = un port,
documenté avant d'écouter. Port non documenté → exit 1 (check rouge).

Patterns (code source .ts/.js/.mjs/.py, périmètre os/ + tools/) :
  .listen(PORT) · process.env.PORT ?? DEFAULT · ternaire env PORT · --port=N · port: N (vite.config uniquement)
Ports documentés : tous les nombres à 4-5 chiffres dans os/PORTS.md.
Hors périmètre : node_modules, tests (*.test.*), docs (*.md),
configs d'outillage (*.toml — ports gérés par la CLI).

Usage : python3 tools/check_ports.py [--root .]
"""

import argparse
import os
import re
import sys

SCOPE_DIRS = ("os", "tools")
SRC_EXT = (".ts", ".js", ".mjs", ".py")
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}

LISTEN_PATTERNS = [
    re.compile(r"\.listen\(\s*(\d{2,5})"),                      # listen direct avec défaut numérique
    re.compile(r"process\.env\.PORT\s*\?\?\s*(\d{2,5})"),        # env ?? 4600
    re.compile(r"process\.env\.PORT\s*\?[^:]{0,80}:\s*(\d{2,5})"),  # env ? ... : 4445 (ternaire)
    re.compile(r"--port[= ](\d{2,5})"),                         # scripts npm : vite --port=4444
]


def _is_vite_config(rel):
    return os.path.basename(rel).startswith("vite.config")


VITE_PORT_PATTERN = re.compile(r"\bport:\s*(\d{2,5})")  # vite dev server (fichier vite.config.* uniquement)


def iter_source_files(root):
    for scope in SCOPE_DIRS:
        base = os.path.join(root, scope)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if fn.endswith(SRC_EXT) and ".test." not in fn:
                    yield os.path.join(dirpath, fn)


def documented_ports(root):
    pmd = os.path.join(root, "os", "PORTS.md")
    text = open(pmd, encoding="utf-8").read()
    return set(int(n) for n in re.findall(r"\b(\d{4,5})\b", text))


def bound_ports(root):
    found = {}
    for path in iter_source_files(root):
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        rel = os.path.relpath(path, root)
        lines = text.splitlines()
        for lineno, line in enumerate(lines, 1):
            for pat in LISTEN_PATTERNS:
                m = pat.search(line)
                if m:
                    num = int(next(g for g in m.groups() if g))
                    found.setdefault(num, []).append(f"{rel}:{lineno}")
            if _is_vite_config(rel):
                m = VITE_PORT_PATTERN.search(line)
                if m:
                    num = int(m.group(1))
                    found.setdefault(num, []).append(f"{rel}:{lineno}")
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    documented = documented_ports(args.root)
    bound = bound_ports(args.root)
    violations = {p: locs for p, locs in bound.items() if p not in documented}
    if violations:
        for p, locs in sorted(violations.items()):
            for loc in locs:
                print(f"PORTS-CHECK FAIL: port {p} non documenté ({loc})")
        print("\nPort(s) non documenté(s) — documenter dans os/PORTS.md avant d'écouter (P-004).")
        return 1
    print(f"PORTS-CHECK OK: {len(bound)} port(s) bindé(s), tous documentés "
          f"({sorted(documented)}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
