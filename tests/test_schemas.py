"""Schema validation tests for series.csv and brief_signals.csv."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

import validate_data as vd


def test_committed_tables_pass_validation():
    errors = vd.validate_all()
    assert errors == []


def test_invalid_obs_id_is_rejected(tmp_path: Path, repo_root: Path):
    src = repo_root / "index" / "series.csv"
    dest = tmp_path / "series.csv"
    with src.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    rows[0]["obs_id"] = "BAD-ID"
    with dest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    errors = vd.validate_all(series_path=dest, brief_path=repo_root / "index" / "brief_signals.csv")
    assert errors, "invalid obs_id must fail validation"


def test_unknown_pillar_is_rejected(tmp_path: Path, repo_root: Path):
    src = repo_root / "index" / "brief_signals.csv"
    dest = tmp_path / "brief_signals.csv"
    with src.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    rows[0]["pillar"] = "not_a_pillar"
    with dest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    errors = vd.validate_all(series_path=repo_root / "index" / "series.csv", brief_path=dest)
    assert errors, "unknown pillar must fail validation"
