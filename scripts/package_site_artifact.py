#!/usr/bin/env python3
"""Pack the public site into dist/site and write dist/SHA256SUMS.

The file set follows firebase.json hosting ignore rules so Firebase and a
future Pages deploy can serve the same artifact. This script never deploys.
"""

from __future__ import annotations

import fnmatch
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SITE = DIST / "site"
FIREBASE_JSON = ROOT / "firebase.json"

# Extra paths to omit from the packed site even if firebase.json does not list them.
# Tests, docs, and Python tooling are not part of the published page.
ALWAYS_IGNORE = (
    "dist/**",
    "tests/**",
    "docs/**",
    "schemas/**",
    "data/**",
    "requirements.txt",
    "CHANGELOG.md",
    "VERSION",
    "placeholders.md",
    "**/__pycache__/**",
    "**/*.pyc",
)


def load_ignore_patterns() -> list[str]:
    patterns = list(ALWAYS_IGNORE)
    if FIREBASE_JSON.is_file():
        config = json.loads(FIREBASE_JSON.read_text(encoding="utf-8"))
        patterns.extend(config.get("hosting", {}).get("ignore", []))
    return patterns


def ignored(rel: str, patterns: list[str]) -> bool:
    posix = rel.as_posix() if isinstance(rel, Path) else rel
    name = Path(posix).name
    for raw in patterns:
        pat = raw
        if pat.startswith("/"):
            pat = pat[1:]
        if fnmatch.fnmatch(posix, pat) or fnmatch.fnmatch(name, pat):
            return True
        # firebase.json uses globstar paths such as .github/**
        if pat.endswith("/**") and (posix.startswith(pat[:-3]) or posix == pat[:-3].rstrip("/")):
            return True
    return False


def package() -> Path:
    if DIST.exists():
        shutil.rmtree(DIST)
    SITE.mkdir(parents=True)
    patterns = load_ignore_patterns()
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if ignored(rel, patterns):
            continue
        dest = SITE / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    # Reuse the checksum writer
    sys.path.insert(0, str(ROOT / "scripts"))
    from make_checksums import write_sums

    # Checksums at dist/SHA256SUMS with paths relative to dist/ (site/...)
    sums = write_sums(DIST)
    n_files = sum(1 for p in SITE.rglob("*") if p.is_file())
    print(f"[OK] Packed {n_files} site files into {SITE.relative_to(ROOT)}; checksums at {sums.relative_to(ROOT)}")
    return DIST


def main() -> int:
    package()
    return 0


if __name__ == "__main__":
    sys.exit(main())
