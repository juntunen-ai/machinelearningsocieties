#!/usr/bin/env python3
"""Fail if VERSION is not the single source of truth in listed files."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
VERSION_PATH = ROOT / "VERSION"

# Paths relative to the repo root that must contain the VERSION string.
# User-facing method labels on the live pages may still say v0.6 until TP1
# and TP2.1 land; those HTML files are intentionally not listed here.
REQUIRED_CONTAINMENT = (
    "CHANGELOG.md",
    "docs/semver.md",
    "docs/data-release.md",
)


def read_version() -> str:
    text = VERSION_PATH.read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit("VERSION is empty")
    if "\n" in text:
        raise SystemExit("VERSION must be a single line")
    return text


def main() -> int:
    version = read_version()
    errors = []
    for rel in REQUIRED_CONTAINMENT:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing {rel}")
            continue
        body = path.read_text(encoding="utf-8")
        if version not in body:
            errors.append(f"{rel} does not contain {version!r}")
    computed = ROOT / "index" / "computed.v0.6.json"
    if computed.is_file():
        if f'"pipeline_version": "{version}"' not in computed.read_text(encoding="utf-8"):
            errors.append(
                "index/computed.v0.6.json pipeline_version does not match VERSION; "
                "re-run python3 scripts/compute_index.py and commit the golden file"
            )
    if errors:
        print("Version consistency check failed:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"[OK] VERSION {version} is consistent in {len(REQUIRED_CONTAINMENT)} documentation files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
