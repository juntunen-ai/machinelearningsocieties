#!/usr/bin/env python3
"""Write SHA256SUMS for every regular file in a directory (relative paths)."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

SUMS_NAME = "SHA256SUMS"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def files_to_hash(root: Path) -> list[Path]:
    out = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name == SUMS_NAME:
            continue
        out.append(path)
    return out


def write_sums(root: Path) -> Path:
    root = root.resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")
    lines = []
    for path in files_to_hash(root):
        rel = path.relative_to(root).as_posix()
        lines.append(f"{sha256_file(path)}  {rel}\n")
    dest = root / SUMS_NAME
    dest.write_text("".join(lines), encoding="utf-8")
    return dest


def verify_sums(root: Path) -> int:
    dest = root / SUMS_NAME
    if not dest.is_file():
        print(f"missing {dest}")
        return 1
    errors = 0
    for line in dest.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        expected, _, rel = line.partition("  ")
        if not rel:
            expected, _, rel = line.partition(" *")
        path = root / rel
        if not path.is_file():
            print(f"MISSING {rel}")
            errors += 1
            continue
        actual = sha256_file(path)
        if actual != expected:
            print(f"MISMATCH {rel}")
            errors += 1
    if errors:
        print(f"[FAIL] {errors} checksum problem(s) in {dest}")
        return 1
    print(f"[OK] Verified {dest}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Write or verify SHA256SUMS in a directory.")
    parser.add_argument("directory")
    parser.add_argument("--verify", action="store_true", help="Verify an existing SHA256SUMS file")
    args = parser.parse_args()
    root = Path(args.directory)
    if args.verify:
        return verify_sums(root)
    dest = write_sums(root)
    count = len(dest.read_text(encoding="utf-8").splitlines())
    print(f"[OK] Wrote {count} checksums to {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
