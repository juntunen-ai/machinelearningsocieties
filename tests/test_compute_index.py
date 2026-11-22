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
    """1.0.0-rc.3: the headline is the deployment pillar alone (Harri's decision, option (a)+(c));
    the interval includes digital channel weight ~ U[0.25, 0.75] (method monte_carlo.channel_weights)."""
    eu = computed["populations"]["EU27"]["headline"]
    fi = computed["populations"]["FI"]["headline"]
    for h in (eu, fi):
        assert h["status"] == "scored"
        assert h["eligible_pillars"] == ["deployment"]
        assert h["weights"] == {"deployment": 1.0}
        # One eligible pillar: H = G, so the aggregation spread is zero.
        assert h["geometric_mean"] == h["score"]
        assert h["variance_decomposition"]["share_aggregation_pct"] == 0
    assert eu["score"] == 9.3
    assert eu["display"] == 9
    assert eu["geometric_mean"] == 9.3
    assert eu["median"] == 9.4
    assert eu["p2_5"] == 5.6
    assert eu["p97_5"] == 13.2
    assert eu["variance_decomposition"]["share_data_pct"] == 1
    assert eu["variance_decomposition"]["share_weights_pct"] == 99
    assert fi["score"] == 17.3
    assert fi["display"] == 17
    assert fi["geometric_mean"] == 17.3
    assert fi["median"] == 17.3
    assert fi["p2_5"] == 10.4
    assert fi["p97_5"] == 24.4
    assert fi["variance_decomposition"]["share_data_pct"] == 1
    assert fi["variance_decomposition"]["share_weights_pct"] == 99
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
    """method block_a.dai_pai: since rc.3 Block A has only AI-specific inputs, so neither flag is set."""
    for pop in ("EU27", "FI"):
        block = computed["populations"][pop]
        assert block["dai"]["proxy"] is False
        assert block["pai"]["proxy"] is False


def test_evidence_is_counted_per_population(computed: dict):
    """method evidence_rules counting: only the population's own geo rows count.

    capital_intensity passes the two-source test in EU27 and FI through the
    OECD cross-check (K1x), not through US/GLOBAL K2 context rows.
    """
    for pop in ("EU27", "FI"):
        pillars = {p["id"]: p for p in computed["populations"][pop]["pillars"]}
        cap = pillars["capital_intensity"]
        assert cap["source_ids"] == ["eurostat_nama_10_an6", "oecd_sna_table1"]
        assert cap["n_official_sources"] == 2 and cap["n"] >= 5
        assert cap["eligible"] is True
        assert "sec_edgar" not in cap["source_ids"] and "epoch_ai_data" not in cap["source_ids"]
        assert pillars["deployment"]["eligible"] is True


def test_cross_check_indicator_is_never_scored(computed: dict):
    for pop in ("EU27", "FI"):
        for p in computed["populations"][pop]["pillars"]:
            assert all(m["indicator_id"] != "K1x_gfcf_ict_ipp_gdp_oecd" for m in p.get("observations", []))
        assert all(x["indicator_id"] != "K1x_gfcf_ict_ipp_gdp_oecd" for x in computed["populations"][pop]["paces"])


def _compute_with_method(tmp_path: Path, repo_root: Path, mutate, *, n_draws: int = 400) -> dict:
    method = json.loads((repo_root / "index" / "method.v1.0.json").read_text(encoding="utf-8"))
    method["monte_carlo"]["n_draws"] = n_draws
    mutate(method)
    dest = tmp_path / "method.v1.0.json"
    dest.write_text(json.dumps(method), encoding="utf-8")
    return ci.compute(method_path=dest)


def test_staleness_limit_is_read_from_method(tmp_path: Path, repo_root: Path, computed: dict):
    """Changing target.reference_period.staleness_limit_months changes which levels are kept."""

    def mutate(method: dict) -> None:
        method["target"]["reference_period"]["staleness_limit_months"] = 1

    bumped = _compute_with_method(tmp_path, repo_root, mutate)
    # A 1-month window makes the 2025 annual levels stale relative to 2026-12-31.
    assert bumped["populations"]["EU27"]["headline"]["score"] != computed["populations"]["EU27"]["headline"]["score"]
    assert len(bumped["stale_observations"]) > len(computed["stale_observations"])


def test_population_geo_is_read_from_method(tmp_path: Path, repo_root: Path, computed: dict):
    """Changing series_geo_codes changes which rows attach to a population."""

    def mutate(method: dict) -> None:
        for pop in method["target"]["populations"]:
            if pop["id"] == "EU27":
                # Official Eurostat code only — series.csv uses the shorthand EU27.
                pop["series_geo_codes"] = ["EU27_2020"]

    bumped = _compute_with_method(tmp_path, repo_root, mutate)
    assert bumped["populations"]["EU27"]["headline"]["score"] != computed["populations"]["EU27"]["headline"]["score"]
    # Finland is untouched.
    assert bumped["populations"]["FI"]["headline"]["score"] == computed["populations"]["FI"]["headline"]["score"]


def test_fallback_sigma_is_read_from_method(tmp_path: Path, repo_root: Path):
    """When a row has no sigma, the grade fallback table in the method file is used."""
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
            row["sigma"] = ""
            row["sigma_basis"] = ""
            touched = True
    assert touched, "expected the EU27 2025 D1 row"
    with dest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    method = json.loads((repo_root / "index" / "method.v1.0.json").read_text(encoding="utf-8"))
    method["monte_carlo"]["n_draws"] = 400
    default_path = tmp_path / "method-default.json"
    default_path.write_text(json.dumps(method), encoding="utf-8")
    baseline = ci.compute(method_path=default_path, series_path=dest)

    method["monte_carlo"]["data_noise"]["fallback_sigma_by_grade"]["A"] = 0.80
    wide_path = tmp_path / "method-wide.json"
    wide_path.write_text(json.dumps(method), encoding="utf-8")
    wide = ci.compute(method_path=wide_path, series_path=dest)

    base_h = baseline["populations"]["EU27"]["headline"]
    wide_h = wide["populations"]["EU27"]["headline"]
    assert wide_h["p97_5"] - wide_h["p2_5"] > base_h["p97_5"] - base_h["p2_5"]


def test_geometric_floor_is_read_from_method(tmp_path: Path, repo_root: Path, computed: dict):
    """The Monte Carlo and point-estimate geometric means use block_a.sensitivity_aggregation.floor."""

    def mutate(method: dict) -> None:
        method["block_a"]["sensitivity_aggregation"]["floor"] = 50.0

    bumped = _compute_with_method(tmp_path, repo_root, mutate)
    assert bumped["populations"]["EU27"]["headline"]["geometric_mean"] != computed["populations"]["EU27"]["headline"]["geometric_mean"]
    assert bumped["populations"]["FI"]["headline"]["geometric_mean"] != computed["populations"]["FI"]["headline"]["geometric_mean"]


def test_pillar_n_is_per_population(computed: dict):
    """Pillar cards expose per-population n and source counts, not a pooled n."""
    eu_dep = next(p for p in computed["populations"]["EU27"]["pillars"] if p["id"] == "deployment")
    fi_dep = next(p for p in computed["populations"]["FI"]["pillars"] if p["id"] == "deployment")
    assert eu_dep["n"] != fi_dep["n"]
    assert eu_dep["n_sources"] >= 1
    assert fi_dep["n_sources"] >= 1
    for card in (eu_dep, fi_dep):
        assert "sec_edgar" not in card["source_ids"]
        assert "epoch_ai_data" not in card["source_ids"]


def test_planetary_scores_are_null_when_not_measured(computed: dict):
    eco = next(p for p in computed["populations"]["EU27"]["pillars"] if p["id"] == "ecological_balance")
    assert eco["status"] == "not measured"
    pb = computed["planetary_boundaries"]
    meter = pb["summary_meter"]
    assert meter["burden_increase_score"] is None
    assert meter["burden_reduction_score"] is None
    assert meter["rebound_discount_factor"] is None
    assert meter["status"] == "not measured"
    for token in ("52.4", "26.8", "42.7", "0.35", "35%"):
        assert token not in (meter.get("headline_rule_en") or "")
        assert token not in (meter.get("headline_rule_fi") or "")
    for boundary in pb["boundaries"]:
        assert boundary["burden_score"] is None
        assert boundary["abatement_score"] is None
        assert boundary["ai_measured"] is False



def test_context_only_registry_sources_never_feed_a_score(repo_root: Path):
    """Registry use=context_only (TP3 licence audit): no row from such a source carries an indicator_id."""
    index_dir = repo_root / "index"
    registry = json.loads((index_dir / "registry.v1.0.json").read_text(encoding="utf-8"))
    context_only = {s["id"] for s in registry["sources"] if s.get("use") == "context_only"}
    assert {"gdpval", "ramp_ai_index", "iea_energy_ai_observatory"} <= context_only
    with (index_dir / "series.csv").open(encoding="utf-8") as handle:
        bad = [r["obs_id"] for r in csv.DictReader(handle) if r["source_id"] in context_only and r["indicator_id"]]
    assert bad == []


def test_capital_intensity_is_block_b_and_still_scored(computed: dict):
    """K1 moved to Block B (rc.3): computed and shown with an interval, never in the headline."""
    expected = {"EU27": (34.0, 31.0, 37.0), "FI": (39.3, 35.8, 42.8)}
    for pop, (score, lo, hi) in expected.items():
        block = computed["populations"][pop]
        cap = {p["id"]: p for p in block["pillars"]}["capital_intensity"]
        assert cap["block"] == "B_conditions"
        assert cap["status"] == "scored"
        assert cap["score"] == score
        assert cap["interval"] == {"p2_5": lo, "median": score, "p97_5": hi}
        assert "capital_intensity" not in block["headline"]["eligible_pillars"]
