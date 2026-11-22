"""Version consistency and series seed synchronisation."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import check_version


def _csv_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_version_file_is_single_line(repo_root: Path):
    version = (repo_root / "VERSION").read_text(encoding="utf-8").strip()
    assert version == "1.0.0-dev"
    assert "\n" not in (repo_root / "VERSION").read_text(encoding="utf-8").strip()


def test_check_version_script_passes(repo_root: Path):
    result = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "check_version.py")],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_check_version_helper_matches_file(repo_root: Path):
    assert check_version.read_version() == (repo_root / "VERSION").read_text(encoding="utf-8").strip()


def test_series_and_seed_are_identical(repo_root: Path):
    series = _csv_rows(repo_root / "index" / "series.csv")
    seed = _csv_rows(repo_root / "index" / "series.seed.csv")
    assert series == seed
    assert len(series) >= 57
