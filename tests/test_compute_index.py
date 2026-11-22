"""Tests for the v1.0 compiler: formulas, [K] block, golden file, and sensitivity."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import pytest

import compute_index as ci

VOLATILE_KEYS = {"generated_at"}
GOLDEN_PATH = Path(__file__).resolve().parent.parent / "index" / "computed.v1.0.json"
ALLOWED_STATUSES = {"scored", "experimental", "not measured", "stale", "incomplete"}


def strip_volatile(value):
    if isinstance(value, dict):
        return {k: strip_volatile(v) for k, v in value.items() if k not in VOLATILE_KEYS}
    if isinstance(value, list):
        return [strip_volatile(item) for item in value]
    return value


def _collect_statuses(value, found: list[str]) -> None:
    if isinstance(value, dict):
        if "status" in value and isinstance(value["status"], str):
            found.append(value["status"])
        for item in value.values():
            _collect_statuses(item, found)
    elif isinstance(value, list):
        for item in value:
            _collect_statuses(item, found)


@pytest.fixture(scope="session")
def computed() -> dict:
    return ci.compute()


def test_round_half_up_and_display_integer():
    assert ci.round_half_up(21.67, 1) == 21.7
    assert ci.round_half_up(21.65, 1) == 21.7
    assert ci.round_half_up(16.71, 1) == 16.7
    assert ci.round_half_up(26.98, 1) == 27.0
    assert ci.round_int(21.67) == 22
    assert ci.round_int(28.33) == 28


def test_normalise_linear_log_reverse_and_clip():
    linear = {"id": "demo_lin", "scale": "linear", "floor": 0.0, "ceiling": 100.0}
    score, clipped = ci.normalise(19.95, linear, 1)
    assert score == pytest.approx(19.95)
    assert clipped is False

    # K1 is linear 0–15 % of GDP: 5.1 → 34 in the worked example
    k1 = {"id": "K1_gfcf_ict_ipp_gdp", "scale": "linear", "floor": 0.0, "ceiling": 15.0}
    score, clipped = ci.normalise(5.1, k1, 1)
    assert score == pytest.approx(34.0, abs=0.005)
    assert clipped is False

    log_ind = {"id": "demo_log", "scale": "log", "floor": 1.0, "ceiling": 100.0}
    score, clipped = ci.normalise(10.0, log_ind, 1)
    assert score == pytest.approx(50.0)
    assert clipped is False

    downward = {"id": "demo_down", "scale": "linear", "floor": 0.0, "ceiling": 100.0}
    score, clipped = ci.normalise(20.0, downward, -1)
    assert score == pytest.approx(80.0)
    assert clipped is False

    score, clipped = ci.normalise(150.0, linear, 1)
    assert score == 100.0
    assert clipped is True

    with pytest.raises(RuntimeError, match="Log-scale"):
        ci.normalise(0.0, log_ind, 1)


def test_unverified_source_is_blocked(tmp_path: Path, repo_root: Path):
    index_dir = repo_root / "index"
    series_src = index_dir / "series.csv"
    dest_series = tmp_path / "series.csv"
    with series_src.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    registry = json.loads((index_dir / "registry.v1.0.json").read_text(encoding="utf-8"))
    unverified = [s["id"] for s in registry["sources"] if not s.get("verified")]
    assert unverified, "registry must contain at least one [K] source for this test"
    rows[0]["source_id"] = unverified[0]
    with dest_series.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(RuntimeError, match=r"Unverified source"):
        ci.compute(series_path=dest_series)


def test_golden_computed_json_matches_except_generated_at(computed: dict):
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert computed["pipeline_version"] == ci.read_pipeline_version()
    assert computed["method_version"] == "1.0"
    assert strip_volatile(computed) == strip_volatile(golden)


def test_headline_figures_and_statuses(computed: dict):
    eu = computed["populations"]["EU27"]["headline"]
    fi = computed["populations"]["FI"]["headline"]
    assert eu["score"] == 21.7
    assert eu["display"] == 22
    assert eu["geometric_mean"] == 17.8
    assert eu["status"] == "scored"
    assert eu["median"] == 21.6
    assert eu["p2_5"] == 16.7
    assert eu["p97_5"] == 27.0
    assert eu["variance_decomposition"]["share_data_pct"] == 5
    assert eu["variance_decomposition"]["share_weights_pct"] == 61
    assert eu["variance_decomposition"]["share_aggregation_pct"] == 34
    assert fi["score"] == 28.3
    assert fi["display"] == 28
    assert fi["geometric_mean"] == 26.1
    assert fi["status"] == "scored"
    # FI interval after the TP1 review: pace draws use their own stream (method monte_carlo.pace_stream_offset).
    assert fi["p2_5"] == 23.8
    assert fi["p97_5"] == 33.3
    assert fi["variance_decomposition"]["share_data_pct"] == 11
    assert fi["variance_decomposition"]["share_weights_pct"] == 72
    assert fi["variance_decomposition"]["share_aggregation_pct"] == 17
    # Channel weights are a single JSON parameter (default 50/50).
    assert computed["channel_weights"]["digital"] == 0.5
    assert computed["channel_weights"]["physical"] == 0.5
    assert computed["range_level"] == "95%"
    assert computed["quarter_label"] == "2026-Q4"
    statuses: list[str] = []
    _collect_statuses(computed, statuses)
    assert statuses, "computed JSON must carry status fields"
    unexpected = sorted({s for s in statuses if s not in ALLOWED_STATUSES})
    assert not unexpected, f"unexpected status values: {unexpected}"
    for pop in computed["populations"].values():
        cost = next(p for p in pop["pillars"] if p["id"] == "cost_to_serve")
        assert cost["status"] == "experimental"


def test_sensitivity_changing_an_input_changes_the_headline(tmp_path: Path, repo_root: Path, computed: dict):
    src = repo_root / "index" / "series.csv"
    dest = tmp_path / "series.csv"
    with src.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    touched = False
    for row in rows:
        if (
            row["indicator_id"] == "D1_ent_any_ai"
            and row["geo"] in {"EU27", "EU27_2020"}
            and row["period"] == "2025"
            and row["sector"] == "ALL"
        ):
            row["value"] = "40.0"
            touched = True
    assert touched, "expected the EU27 2025 D1 row in series.csv"
    with dest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    bumped = ci.compute(series_path=dest)
    assert bumped["populations"]["EU27"]["headline"]["score"] != computed["populations"]["EU27"]["headline"]["score"]
    # Finland's D1 is unchanged, so its headline stays put.
    assert bumped["populations"]["FI"]["headline"]["score"] == computed["populations"]["FI"]["headline"]["score"]


def test_obs_026_has_no_bridge_and_obs_027_is_corrected(repo_root: Path):
    with (repo_root / "index" / "series.csv").open(encoding="utf-8") as handle:
        rows = {row["obs_id"]: row for row in csv.DictReader(handle)}
    for obs_id in ("OBS-025", "OBS-026"):
        row = rows[obs_id]
        assert row["bridge_source"] == ""
        assert row["bridge_period"] == ""
        assert row["bridge_factor"] == ""
        assert row["indicator_id"] == ""
        assert row["geo"] == "US"
    assert rows["OBS-027"]["value"] == "8.28"
    assert rows["OBS-027"]["indicator_id"] == "D3_ent_depth_ge3"


def test_pace_history_ignores_staleness_but_respects_segments(computed: dict):
    """Method pace.history: staleness limits levels only; segments are never crossed."""
    for pop in ("EU27", "FI"):
        paces = {(p["indicator_id"], p["segment_id"]): p for p in computed["populations"][pop]["paces"]}
        k1 = paces[("K1_gfcf_ict_ipp_gdp", "S1")]
        assert k1["n_points"] == 7 and k1["periods"][0] == "2019" and k1["periods"][-1] == "2025"
        d1 = paces[("D1_ent_any_ai", "S1")]
        assert d1["periods"] == ["2021", "2023", "2024"]
        # n = 3: the OLS t-interval (df = 1) is wide, so no direction is claimed.
        assert d1["wording"] == "not distinguishable from zero"
        assert ("D1_ent_any_ai", "S2") not in paces


def test_proxy_flags_follow_channel_inputs(computed: dict):
    """method block_a.dai_pai: DAI is a proxy mix (K1); PAI uses only AI-specific D4."""
    for pop in ("EU27", "FI"):
        block = computed["populations"][pop]
        assert block["dai"]["proxy"] is True
        assert block["pai"]["proxy"] is False
