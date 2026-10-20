#!/usr/bin/env python3
"""P-003 secret scan — policy/POLICY-003.md (L05, D-N027).

Exit 0 = aucun secret détecté ; exit 1 = au moins un motif trouvé.

Approche volontairement simple : motifs regex explicites — les secrets ne
sont jamais exclus par silence. Quand un accès est légitime, on documente
le motif ICI par exception nominative plutôt que de masquer le scan.
"""

import os
import re
import sys

FAIL_DIR = os.path.join("evidence", "failures")

PATTERNS = [
    ("sbp service_role key", r"sbp_[A-Za-z0-9_\-]{16,}"),
    ("service_role nommé", r"service_role['\"]?\s*[:=]\s*['\"][^'\"]{10,}"),
    ("JWT eyJ", r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
    ("clé privée PEM", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ("sk- (OpenAI-like)", r"sk-[A-Za-z0-9]{20,}"),
    ("AKIA (AWS)", r"AKIA[0-9A-Z]{16}"),
    ("ghp_ (GitHub token)", r"ghp_[A-Za-z0-9]{20,}"),
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}
SKIP_FILES = {
    os.path.join("tools", "secret_scan.py"),  # se contient lui-même
    os.path.join("policy", "POLICY-003.md"),  # documente les motifs
}

TEXT_EXTS = {
    ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".txt", ".yml", ".yaml",
    ".toml", ".py", ".sh", ".env", ".sql", ".html", ".css",
}


def iter_files(root="."):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = os.path.join(dirpath, name)
            if path in SKIP_FILES:
                continue
            if os.path.splitext(name)[1].lower() not in TEXT_EXTS and name != ".env":
                continue
            yield path


def log_failure_checklist(path, lineno, label, line):
    """Checklist de triage écrite à CHAQUE échec (10 checks)."""
    os.makedirs(FAIL_DIR, exist_ok=True)
    logpath = os.path.join(FAIL_DIR, "secret-scan-fail.log")
    with open(logpath, "a", encoding="utf-8") as log:
        log.write(f"SECRET-SCAN FAIL [{label}]: {path}:{lineno}\n")
        log.write(f"ligne: {line.strip()[:200]}\n")
        for item in [
            " [ ] 1. Commit le contenant identifié (sha)",
            " [ ] 2. Auteur du commit identifié",
            " [ ] 3. Date d'introduction déterminée",
            " [ ] 4. Nature du secret confirmée (vrai / faux positif)",
            " [ ] 5. Si vrai : rotation immédiate du secret",
            " [ ] 6. Invalidation de l'ancien secret vérifiée",
            " [ ] 7. Historique git : purge décidée (oui / non, qui)",
            " [ ] 8. Accès faits avec ce secret audités",
            " [ ] 9. Correctif commité (suppression / env var)",
            " [ ] 10. Re-scan vert attaché à la PR",
        ]:
            log.write(item + "\n")
        log.write("\n")


def main():
    hits = 0
    compiled = [(label, re.compile(p)) for label, p in PATTERNS]
    for path in iter_files():
        try:
            with open(path, encoding="utf-8", errors="ignore") as fh:
                for lineno, line in enumerate(fh, 1):
                    for label, rx in compiled:
                        if rx.search(line):
                            hits += 1
                            print(f"SECRET-SCAN FAIL [{label}]: {path}:{lineno}")
                            log_failure_checklist(path, lineno, label, line)
        except OSError:
            continue
    if hits:
        print(f"\n{hits} secret(s) détecté(s) — P-003 violée.")
        return 1
    print("secret-scan OK — aucun motif détecté (P-003).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
