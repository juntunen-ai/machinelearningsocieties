"""Tests for compute_index helpers, the [K] block, Monte Carlo, and the golden file."""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path

import pytest

import compute_index as ci

VOLATILE_KEYS = {"generated_at"}
GOLDEN_PATH = Path(__file__).resolve().parent.parent / "index" / "computed.v0.6.json"


def strip_volatile(value):
    if isinstance(value, dict):
        return {k: strip_volatile(v) for k, v in value.items() if k not in VOLATILE_KEYS}
    if isinstance(value, list):
        return [strip_volatile(item) for item in value]
    return value


def test_clamp_bounds():
    assert ci.clamp(-5) == 0.0
    assert ci.clamp(150) == 100.0
    assert ci.clamp(42.7) == 42.7
    assert ci.clamp(5, lo=10, hi=20) == 10
    assert ci.clamp(25, lo=10, hi=20) == 20


def test_percentile_edges_and_interpolation():
    assert ci.percentile([], 0.5) == 0.0
    assert ci.percentile([7.0], 0.5) == 7.0
    assert ci.percentile([0.0, 10.0], 0.5) == 5.0
    assert ci.percentile([0.0, 10.0, 20.0], 0.0) == 0.0
    assert ci.percentile([0.0, 10.0, 20.0], 1.0) == 20.0
    # 0.25 of [0, 10, 20] sits a quarter of the way from 0 to 10
    assert ci.percentile([0.0, 10.0, 20.0], 0.25) == pytest.approx(5.0)


def test_dirichlet_uniform_is_a_probability_vector():
    rng = random.Random(ci.MC_SEED)
    weights = ci.dirichlet_uniform(rng, 3)
    assert len(weights) == 3
    assert all(w > 0 for w in weights)
    assert math.isclose(sum(weights), 1.0, rel_tol=1e-12)


def test_unverified_source_is_blocked(tmp_path: Path, repo_root: Path):
    index_dir = repo_root / "index"
    series_src = index_dir / "series.csv"
    dest_series = tmp_path / "series.csv"
    with series_src.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    # Point the first row at a known unverified [K] source in the registry.
    registry = json.loads((index_dir / "registry.v0.6.json").read_text(encoding="utf-8"))
    unverified = [s["id"] for s in registry["sources"] if not s.get("verified")]
    assert unverified, "registry must contain at least one [K] source for this test"
    rows[0]["source_id"] = unverified[0]
    with dest_series.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(RuntimeError, match=r"Unverified source"):
        ci.compute(series_path=dest_series)


def test_seeded_monte_carlo_is_deterministic():
    first = ci.compute()
    second = ci.compute()
    a = first["headline"]["block_a_diffusion_core"]
    b = second["headline"]["block_a_diffusion_core"]
    assert a["p5"] == b["p5"]
    assert a["p50"] == b["p50"]
    assert a["p95"] == b["p95"]
    assert a["score"] == b["score"]
    # Same seed must also match the committed golden uncertainty band.
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    g = golden["headline"]["block_a_diffusion_core"]
    assert a["p5"] == g["p5"]
    assert a["p95"] == g["p95"]


def test_different_seed_changes_uncertainty_band(monkeypatch):
    original_seed = ci.MC_SEED
    first = ci.compute()["headline"]["block_a_diffusion_core"]
    monkeypatch.setattr(ci, "MC_SEED", original_seed + 1)
    second = ci.compute()["headline"]["block_a_diffusion_core"]
    assert (second["p5"], second["p95"]) != (first["p5"], first["p95"])


def test_golden_computed_json_matches_except_generated_at():
    produced = ci.compute()
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert produced["pipeline_version"] == ci.read_pipeline_version()
    assert strip_volatile(produced) == strip_volatile(golden)
