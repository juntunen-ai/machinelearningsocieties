#!/usr/bin/env python3
"""Deterministic compiler for the Machine Learning Societies AI Diffusion Index.

Implements the compiler contract in index/method.v1.0.json §14:
every score is computed from series.csv through the documented chain;
goalposts, weights, evidence rules and Monte Carlo parameters are read
only from the method file.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
import warnings
from calendar import monthrange
from collections import defaultdict
from datetime import date, datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT / "index"
METHOD_PATH = INDEX_DIR / "method.v1.0.json"
REGISTRY_PATH = INDEX_DIR / "registry.v1.0.json"
SERIES_CSV = INDEX_DIR / "series.csv"
BRIEF_SIGNALS_CSV = INDEX_DIR / "brief_signals.csv"
PB_PATH = INDEX_DIR / "planetary_boundaries.json"
OUTPUT_JSON = INDEX_DIR / "computed.v1.0.json"
VERSION_PATH = ROOT / "VERSION"

POPULATION_GEO = {
    "EU27": {"EU27", "EU27_2020"},
    "FI": {"FI"},
}


def read_pipeline_version(version_path: Path = VERSION_PATH) -> str:
    return version_path.read_text(encoding="utf-8").strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_cut_off(method: dict) -> date:
    text = method["data_vintage"]["proposed_1_0_0_cut_off"]
    # "2026-12-31 (2026-Q4): ..."
    token = text.strip().split()[0]
    return date.fromisoformat(token)


def quarter_label(cut: date) -> str:
    q = (cut.month - 1) // 3 + 1
    return f"{cut.year}-Q{q}"


def period_end(period: str) -> date:
    if len(period) == 4 and period.isdigit():
        return date(int(period), 12, 31)
    if len(period) == 7 and period[4:6] == "-Q" and period[6] in "1234":
        year, q = int(period[:4]), int(period[6])
        month = q * 3
        return date(year, month, monthrange(year, month)[1])
    if len(period) == 7 and period[4] == "-" and period[5:].isdigit():
        year, month = int(period[:4]), int(period[5:])
        return date(year, month, monthrange(year, month)[1])
    if len(period) == 7 and period[4:6] == "-H" and period[6] in "12":
        year, half = int(period[:4]), int(period[6])
        return date(year, 6 if half == 1 else 12, 30 if half == 1 else 31)
    if len(period) >= 7 and "-W" in period:
        year = int(period.split("-W")[0])
        week = int(period.split("-W")[1])
        return date.fromisocalendar(year, week, 7)
    raise ValueError(f"Unrecognised period label: {period!r}")


def period_midpoint(period: str) -> float:
    """Return a year-fraction midpoint for OLS pace (e.g. 2025.5 for a calendar year)."""
    end = period_end(period)
    if len(period) == 4 and period.isdigit():
        return int(period) + 0.5
    if "-Q" in period:
        year, q = int(period[:4]), int(period[6])
        return year + (q - 0.5) / 4.0
    if "-H" in period:
        year, half = int(period[:4]), int(period[6])
        return year + (0.25 if half == 1 else 0.75)
    if "-W" in period:
        year, week = int(period.split("-W")[0]), int(period.split("-W")[1])
        return year + (week - 0.5) / 52.0
    # YYYY-MM
    return end.year + (end.month - 0.5) / 12.0


def months_before(end: date, cut: date) -> bool:
    """True if `end` is more than 36 months before `cut`."""
    # 36 months before cut
    year, month = cut.year, cut.month - 36
    while month <= 0:
        year -= 1
        month += 12
    threshold = date(year, month, min(cut.day, monthrange(year, month)[1]))
    return end < threshold


def round_half_up(value: float, places: int) -> float:
    quant = Decimal("1") if places == 0 else Decimal("1." + "0" * places)
    # Avoid binary float artefacts by going through a stable decimal string.
    dec = Decimal(format(value, ".15g"))
    return float(dec.quantize(quant, rounding=ROUND_HALF_UP))


def round_int(value: float) -> int:
    return int(Decimal(format(value, ".15g")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalise(x: float, indicator: dict, direction: int) -> tuple[float, bool]:
    scale = indicator["scale"]
    floor, ceiling = float(indicator["floor"]), float(indicator["ceiling"])
    if scale == "log":
        if x <= 0 or floor <= 0 or ceiling <= 0:
            raise RuntimeError(
                f"Log-scale value must be > 0 (indicator {indicator['id']}, x={x}, floor={floor})"
            )
        score = 100.0 * (math.log(x) - math.log(floor)) / (math.log(ceiling) - math.log(floor))
    elif scale == "linear":
        if ceiling == floor:
            raise RuntimeError(f"Zero-width goalpost for {indicator['id']}")
        score = 100.0 * (x - floor) / (ceiling - floor)
    else:
        raise RuntimeError(f"Unknown scale {scale!r} for {indicator['id']}")
    if direction == -1:
        score = 100.0 - score
    clipped = score < 0.0 or score > 100.0
    score = max(0.0, min(100.0, score))
    return score, clipped


def provenance_rank(letter: str) -> int:
    return {"A": 0, "B": 1, "C": 2}.get(letter, 3)


def weakest_grade(letters: list[str]) -> str | None:
    if not letters:
        return None
    return max(letters, key=provenance_rank)


def parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def apply_caps(grade: str | None, *, sector: str | None, pillar: str, indicator: dict | None, caps: list) -> str | None:
    if grade is None:
        return None
    out = grade
    for cap in caps:
        scope = cap["scope"]
        max_g = cap["max_grade"][:1]  # "C" or "C for the AI dimension"
        if scope == f"sector={sector}" and sector is not None:
            if provenance_rank(out) < provenance_rank(max_g):
                out = max_g
        if scope == f"pillar={pillar}":
            if provenance_rank(out) < provenance_rank(max_g):
                out = max_g
        if "ai_specificity=proxy (physical channel indicators)" in scope:
            if indicator and indicator.get("channel") == "physical" and indicator.get("role") != "scored":
                # D4 is AI-specific and not capped (method grade_rules.caps)
                if indicator.get("id") == "D4_ent_autonomous":
                    continue
                if indicator.get("id") == "D5_robot_density" or indicator.get("role") == "sensitivity_only":
                    if provenance_rank(out) < provenance_rank("C"):
                        out = "C"
    return out


def eligible_row(row: dict, sources: dict, cut: date, method: dict) -> str | None:
    """Return None if the row may be used, else a reason to skip/fail."""
    src = sources.get(row["source_id"])
    if src is None:
        return f"unknown source_id {row['source_id']}"
    if not src.get("verified", False):
        return "K_SOURCE"
    try:
        tier = int(row.get("trust_tier") or src.get("tier") or 5)
    except ValueError:
        tier = 5
    if tier >= 5:
        return "tier_5"
    try:
        logged = date.fromisoformat(row["date_logged"])
    except ValueError:
        return "bad date_logged"
    if logged > cut:
        return "after_cut_off"
    release = row.get("source_release_date") or ""
    if release:
        try:
            if date.fromisoformat(release) > cut:
                return "source_released_after_cut_off"
        except ValueError:
            return "bad source_release_date"
    try:
        end = period_end(row["period"])
    except ValueError:
        return "bad period"
    if months_before(end, cut):
        return "stale"
    return None


def pick_level_value(candidates: list[dict], indicator: dict) -> dict | None:
    """Latest period in the latest segment with data, period_end already <= cut-off."""
    if not candidates:
        return None
    segs = indicator.get("segments") or []
    if segs:
        # Prefer the last defined segment that has a candidate.
        for seg in reversed(segs):
            sid = seg["id"]
            matched = [r for r in candidates if r.get("segment_id") == sid]
            if matched:
                matched.sort(key=lambda r: period_end(r["period"]))
                return matched[-1]
    candidates = sorted(candidates, key=lambda r: period_end(r["period"]))
    return candidates[-1]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def compute(
    *,
    method_path: Path = METHOD_PATH,
    registry_path: Path = REGISTRY_PATH,
    series_path: Path = SERIES_CSV,
    brief_path: Path = BRIEF_SIGNALS_CSV,
    pb_path: Path = PB_PATH,
    version_path: Path = VERSION_PATH,
) -> dict:
    method = load_json(method_path)
    registry = load_json(registry_path)
    series_rows = load_csv(series_path)
    brief_rows = load_csv(brief_path) if brief_path.is_file() else []
    pb_data = load_json(pb_path) if pb_path.is_file() else {}

    cut = parse_cut_off(method)
    sources = {s["id"]: s for s in registry["sources"]}
    pillars_spec = {p["id"]: p for p in method["pillars"]}
    indicators = {ind["id"]: {**ind, "pillar_id": p["id"]} for p in method["pillars"] for ind in p["indicators"]}
    caps = method["grade_rules"]["caps"]
    ev = method["evidence_rules"]
    channel_weights = method["scoring"]["within_pillar_aggregation"]["channel_weights"]
    w_digital = float(channel_weights["digital"])
    w_physical = float(channel_weights["physical"])
    mc = method["monte_carlo"]
    block_a_ids = list(method["block_a"]["pillars"])
    nominal = {k: float(v) for k, v in method["block_a"]["nominal_weights"].items()}
    populations = method["target"]["populations"]

    # Fail if a [K] source is present in the file at all (used or not).
    for row in series_rows:
        src = sources.get(row["source_id"])
        if src is None:
            raise RuntimeError(f"Unknown source {row['source_id']} in series.csv ({row['obs_id']})")
        if not src.get("verified", False):
            raise RuntimeError(f"Unverified source {row['source_id']} in series.csv ({row['obs_id']})")
        for field in ("obs_id", "period", "pillar", "geo", "value", "source_id"):
            if not str(row.get(field, "")).strip():
                raise RuntimeError(f"Missing required field {field} on {row.get('obs_id')}")

    classified: list[dict] = []
    stale_rows: list[dict] = []
    for row in series_rows:
        reason = eligible_row(row, sources, cut, method)
        item = dict(row)
        item["_reason"] = reason
        try:
            item["_value"] = float(row["value"])
        except ValueError as exc:
            raise RuntimeError(f"Non-numeric value on {row['obs_id']}") from exc
        item["_end"] = period_end(row["period"])
        if reason == "stale":
            stale_rows.append(item)
            continue
        if reason in {"after_cut_off", "source_released_after_cut_off", "tier_5"}:
            continue
        if reason == "K_SOURCE":
            raise RuntimeError(f"Unverified source {row['source_id']} in series.csv ({row['obs_id']})")
        if reason:
            continue
        classified.append(item)

    def rows_for(pop_id: str, indicator_id: str, *, sector: str | None = "ALL") -> list[dict]:
        geos = POPULATION_GEO[pop_id]
        out = []
        for row in classified:
            if row.get("indicator_id") != indicator_id:
                continue
            if row["geo"] not in geos:
                continue
            if sector is not None and row["sector"] != sector:
                continue
            if indicators[indicator_id].get("role") in {"sensitivity_only", "context_only"}:
                continue
            if indicators[indicator_id].get("exists") is False:
                continue
            out.append(row)
        return out

    def evidence_for_pillar(pillar_id: str) -> dict:
        """Count observations and sources across all geographies (plan 2.3)."""
        obs = [
            r
            for r in classified
            if r["pillar"] == pillar_id
            and r.get("indicator_id")
            and indicators.get(r["indicator_id"], {}).get("role") not in {"sensitivity_only"}
        ]
        # context_only still counts toward evidence (they are verified observations on the pillar)
        source_ids = {r["source_id"] for r in obs}
        official = {r["source_id"] for r in obs if int(r["trust_tier"]) == 1}
        return {
            "n": len(obs),
            "source_ids": sorted(source_ids),
            "n_sources": len(source_ids),
            "n_official_sources": len(official),
        }

    def score_indicator(indicator: dict, row: dict, direction: int) -> dict:
        raw = row["_value"]
        score, clipped = normalise(raw, indicator, direction)
        grade = (row.get("grade") or "C")[0]
        grade = apply_caps(grade, sector=row.get("sector"), pillar=indicator["pillar_id"], indicator=indicator, caps=caps)
        try:
            sigma = float(row["sigma"]) if row.get("sigma") else 0.045
        except ValueError:
            sigma = 0.045
        return {
            "indicator_id": indicator["id"],
            "obs_id": row["obs_id"],
            "period": row["period"],
            "geo": row["geo"],
            "sector": row["sector"],
            "raw": raw,
            "score": score,
            "clipped": clipped,
            "grade": grade,
            "sigma": sigma,
            "sigma_basis": row.get("sigma_basis") or "",
            "channel": indicator["channel"],
            "layer": indicator["layer"],
            "segment_id": row.get("segment_id") or "",
            "source_id": row["source_id"],
        }

    def aggregate_pillar(pillar: dict, measured: list[dict]) -> dict:
        """measured: list of scored indicator records for one population (sector ALL)."""
        pid = pillar["id"]
        defined = [
            ind
            for ind in pillar["indicators"]
            if ind.get("role") not in {"sensitivity_only", "context_only"} and ind.get("exists") is not False
        ]
        measured_ids = {m["indicator_id"] for m in measured}
        unmeasured = [ind["id"] for ind in defined if ind["id"] not in measured_ids]
        by_channel_layer: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for item in measured:
            by_channel_layer[(item["channel"], item["layer"])].append(item)

        channels: dict[str, dict] = {}
        for channel in ("digital", "physical"):
            layer_scores = []
            layer_detail = {}
            for layer in ("reach", "depth", "embeddedness"):
                items = by_channel_layer.get((channel, layer), [])
                if not items:
                    continue
                lscore = mean([it["score"] for it in items])
                layer_scores.append(lscore)
                layer_detail[layer] = {
                    "score": lscore,
                    "n_indicators": len(items),
                    "indicators": [it["indicator_id"] for it in items],
                }
            if not layer_scores:
                continue
            channels[channel] = {
                "score": mean(layer_scores),
                "layers": layer_detail,
            }

        if not channels:
            status = "not measured"
            pillar_score = None
            coverage_note = "digital_none"
        elif "digital" in channels and "physical" in channels:
            pillar_score = w_digital * channels["digital"]["score"] + w_physical * channels["physical"]["score"]
            coverage_note = "both"
        elif "digital" in channels:
            pillar_score = channels["digital"]["score"]
            coverage_note = "digital_only"
        else:
            pillar_score = channels["physical"]["score"]
            coverage_note = "physical_only"

        grades = [it["grade"] for it in measured if it.get("grade")]
        grade = weakest_grade(grades)
        grade = apply_caps(grade, sector="ALL", pillar=pid, indicator=None, caps=caps)
        evd = evidence_for_pillar(pid)
        n_defined = len(defined)
        n_measured = len(measured)
        coverage = f"{n_measured}/{n_defined}"

        # Eligibility
        designed = pillar.get("headline_eligible_by_design", True)
        has_value = pillar_score is not None
        min_obs = ev["pillar_headline_eligibility"]["min_verified_observations"]
        min_src = ev["pillar_headline_eligibility"]["min_distinct_verified_sources"]
        min_off = ev["pillar_headline_eligibility"]["min_official_sources"]
        min_grade = ev["pillar_headline_eligibility"]["min_derived_grade"]
        grade_ok = grade is not None and provenance_rank(grade) <= provenance_rank(min_grade)
        eligible = (
            designed
            and has_value
            and evd["n"] >= min_obs
            and evd["n_sources"] >= min_src
            and evd["n_official_sources"] >= min_off
            and grade_ok
        )
        designed_experimental = (not designed) or str(pillar.get("status_1_0") or "").startswith("experimental")
        if not has_value and designed_experimental:
            status = "experimental"
        elif not has_value:
            status = "not measured"
        elif designed_experimental or not eligible:
            status = "experimental"
        else:
            status = "scored"

        clipped_any = any(it["clipped"] for it in measured)
        return {
            "pillar_id": pid,
            "code": pillar.get("code"),
            "block": pillar.get("block"),
            "direction": pillar.get("direction"),
            "score": pillar_score,
            "status": status,
            "grade": grade,
            "n": evd["n"],
            "n_sources": evd["n_sources"],
            "n_official_sources": evd["n_official_sources"],
            "coverage": coverage,
            "channel_coverage": coverage_note,
            "channels": channels,
            "unmeasured_indicators": unmeasured,
            "measured": measured,
            "clipped": clipped_any,
            "eligible": eligible,
            "source_ids": evd["source_ids"],
        }

    def values_from_measured(measured: list[dict]) -> dict[str, dict]:
        return {m["indicator_id"]: m for m in measured}

    def score_from_values(pillar: dict, values: dict[str, float]) -> float | None:
        """Recompute a pillar score from a dict of indicator_id -> raw x (for MC draws)."""
        measured = []
        direction = pillar["direction"]
        for ind in pillar["indicators"]:
            if ind["id"] not in values:
                continue
            if ind.get("role") in {"sensitivity_only", "context_only"} or ind.get("exists") is False:
                continue
            dummy = {
                "_value": values[ind["id"]],
                "obs_id": "",
                "period": "",
                "geo": "",
                "sector": "ALL",
                "grade": "A-Y",
                "sigma": "",
                "sigma_basis": "",
                "segment_id": "",
                "source_id": "",
            }
            measured.append(score_indicator(indicators[ind["id"]], dummy, direction))
        agg = aggregate_pillar(pillar, measured)
        return agg["score"]

    # --- Build per-population levels ---
    pop_results = {}
    rng = np.random.Generator(np.random.PCG64(int(mc["seed"])))
    r_weight = float(mc["weights"]["r"])
    n_draws = int(mc["draws"])
    warning_messages: list[str] = []

    for pop in populations:
        pop_id = pop["id"]
        pillar_aggs = {}
        for pid, pillar in pillars_spec.items():
            measured = []
            for ind in pillar["indicators"]:
                if ind.get("role") in {"sensitivity_only", "context_only"} or ind.get("exists") is False:
                    continue
                cands = rows_for(pop_id, ind["id"], sector="ALL")
                chosen = pick_level_value(cands, ind)
                if chosen is None:
                    continue
                measured.append(score_indicator(indicators[ind["id"]], chosen, pillar["direction"]))
            pillar_aggs[pid] = aggregate_pillar(pillar, measured)

        eligible_ids = [pid for pid in block_a_ids if pillar_aggs[pid]["eligible"] and pillar_aggs[pid]["score"] is not None]
        # Effective weights
        if eligible_ids:
            weight_sum = sum(nominal[pid] for pid in eligible_ids)
            weights = {pid: nominal[pid] / weight_sum for pid in eligible_ids}
        else:
            weights = {}

        headline_status = "scored"
        if len(eligible_ids) < ev["headline"]["min_eligible_block_a_pillars"]:
            headline_status = "incomplete"
            H = None
            G = None
        else:
            scores = {pid: pillar_aggs[pid]["score"] for pid in eligible_ids}
            H = sum(weights[pid] * scores[pid] for pid in eligible_ids)
            floor_g = float(method["block_a"]["sensitivity_aggregation"]["floor"])
            G = math.exp(sum(weights[pid] * math.log(max(scores[pid], floor_g)) for pid in eligible_ids))

        # DAI / PAI
        def channel_pillar_score(pid: str, channel: str) -> float | None:
            ch = pillar_aggs[pid]["channels"].get(channel)
            return ch["score"] if ch else None

        def aggregate_channel(channel: str) -> dict:
            ids = [pid for pid in eligible_ids if channel_pillar_score(pid, channel) is not None]
            if len(ids) < 1:
                return {"score": None, "status": "not measured", "pillars": [], "weights": {}}
            wsum = sum(nominal[pid] for pid in ids)
            ww = {pid: nominal[pid] / wsum for pid in ids}
            score = sum(ww[pid] * channel_pillar_score(pid, channel) for pid in ids)
            proxy = any(
                indicators[m["indicator_id"]].get("ai_specificity") == "proxy"
                or pillars_spec[pid].get("ai_specificity") == "proxy"
                for pid in ids
                for m in pillar_aggs[pid]["measured"]
                if m["channel"] == channel
            )
            # K1 is a proxy; flag if it contributes
            if any(
                m.get("indicator_id") == "K1_gfcf_ict_ipp_gdp"
                for pid in ids
                for m in pillar_aggs[pid]["measured"]
                if m["channel"] == channel
            ):
                proxy = True
            return {"score": score, "status": "scored", "pillars": ids, "weights": ww, "proxy": proxy}

        dai = aggregate_channel("digital")
        pai = aggregate_channel("physical")

        # Indicator values used in scored Block A pillars (for MC)
        used_measured = []
        for pid in eligible_ids:
            used_measured.extend(pillar_aggs[pid]["measured"])
        used_measured.sort(key=lambda m: m["indicator_id"])
        indicator_ids_sorted = [m["indicator_id"] for m in used_measured]
        base_raw = {m["indicator_id"]: m["raw"] for m in used_measured}
        base_sigma = {m["indicator_id"]: m["sigma"] for m in used_measured}

        # Monte Carlo: generate Z and U for this population (order EU27, FI)
        n_ind = max(len(indicator_ids_sorted), 1)
        n_w = max(len(eligible_ids), 1)
        Z = rng.standard_normal((n_draws, n_ind))
        U = rng.uniform(1.0 - r_weight, 1.0 + r_weight, (n_draws, n_w))

        def headline_from_raw(raws: dict[str, float], weight_vec: dict[str, float] | None = None) -> tuple[float | None, float | None, float | None, float | None]:
            # returns H, G, DAI, PAI
            local = {}
            for pid, pillar in pillars_spec.items():
                vals = {iid: raws[iid] for iid in (m["indicator_id"] for m in pillar_aggs[pid]["measured"]) if iid in raws}
                local[pid] = score_from_values(pillar, vals)
            if not eligible_ids or any(local[pid] is None for pid in eligible_ids):
                return None, None, None, None
            ww = weight_vec if weight_vec is not None else weights
            h = sum(ww[pid] * local[pid] for pid in eligible_ids)
            g = math.exp(sum(ww[pid] * math.log(max(local[pid], 1.0)) for pid in eligible_ids))
            # DAI / PAI from channel scores
            def ch_agg(channel: str) -> float | None:
                ids = [pid for pid in eligible_ids if pillar_aggs[pid]["channels"].get(channel)]
                if not ids:
                    return None
                # recompute channel score from new raws
                ch_scores = {}
                for pid in ids:
                    ch_vals = {
                        m["indicator_id"]: raws[m["indicator_id"]]
                        for m in pillar_aggs[pid]["measured"]
                        if m["channel"] == channel and m["indicator_id"] in raws
                    }
                    if not ch_vals:
                        continue
                    # score only that channel's indicators
                    pieces = []
                    pillar = pillars_spec[pid]
                    by_layer = defaultdict(list)
                    for ind in pillar["indicators"]:
                        if ind["id"] not in ch_vals:
                            continue
                        if ind.get("channel") != channel:
                            continue
                        s, _ = normalise(ch_vals[ind["id"]], ind, pillar["direction"])
                        by_layer[ind["layer"]].append(s)
                    if not by_layer:
                        continue
                    ch_scores[pid] = mean([mean(v) for v in by_layer.values()])
                if not ch_scores:
                    return None
                wsum = sum(nominal[pid] for pid in ch_scores)
                return sum((nominal[pid] / wsum) * ch_scores[pid] for pid in ch_scores)

            return h, g, ch_agg("digital"), ch_agg("physical")

        def weights_from_factors(factors: np.ndarray) -> dict[str, float]:
            raw_w = np.array([nominal[pid] * float(factors[i]) for i, pid in enumerate(eligible_ids)], dtype=float)
            raw_w = raw_w / raw_w.sum()
            return {pid: float(raw_w[i]) for i, pid in enumerate(eligible_ids)}

        def run_draws(noise: bool, random_weights: bool) -> dict[str, np.ndarray]:
            Hs = np.empty(n_draws)
            Gs = np.empty(n_draws)
            Dais = np.empty(n_draws)
            Pais = np.empty(n_draws)
            for k in range(n_draws):
                raws = dict(base_raw)
                if noise:
                    for j, iid in enumerate(indicator_ids_sorted):
                        raws[iid] = base_raw[iid] * (1.0 + base_sigma[iid] * float(Z[k, j]))
                ww = weights_from_factors(U[k]) if random_weights else weights
                h, g, d, p = headline_from_raw(raws, ww)
                Hs[k] = h if h is not None else np.nan
                Gs[k] = g if g is not None else np.nan
                Dais[k] = d if d is not None else np.nan
                Pais[k] = p if p is not None else np.nan
            return {"H": Hs, "G": Gs, "DAI": Dais, "PAI": Pais}

        mc_out = None
        if H is not None:
            joint = run_draws(True, True)
            data_only = run_draws(True, False)
            weights_only = run_draws(False, True)
            quantiles = [float(q) for q in mc["interval"]["quantiles"]]
            q_h = np.quantile(joint["H"], quantiles)
            q_dai = np.quantile(joint["DAI"], quantiles)
            q_pai = np.quantile(joint["PAI"], quantiles)
            # Variance decomposition
            V_total = float(np.var(joint["H"], ddof=0))
            V_data = float(np.var(data_only["H"], ddof=0))
            V_weights = float(np.var(weights_only["H"], ddof=0))
            V_aggregation = float(((H - G) / 2.0) ** 2)
            denom = V_data + V_weights + V_aggregation
            share_data = V_data / denom if denom else 0.0
            share_weights = V_weights / denom if denom else 0.0
            share_aggregation = V_aggregation / denom if denom else 0.0
            interaction = V_total - V_data - V_weights
            median = float(q_h[1])
            if abs(median - H) > 1.0:
                msg = f"{pop_id}: Monte Carlo median {median:.4f} differs from point {H:.4f} by more than 1.0"
                warning_messages.append(msg)
                warnings.warn(msg)
            mc_out = {
                "median": median,
                "p2_5": float(q_h[0]),
                "p97_5": float(q_h[2]),
                "dai": {"median": float(q_dai[1]), "p2_5": float(q_dai[0]), "p97_5": float(q_dai[2])},
                "pai": {"median": float(q_pai[1]), "p2_5": float(q_pai[0]), "p97_5": float(q_pai[2])},
                "variance_decomposition": {
                    "V_total": V_total,
                    "V_data": V_data,
                    "V_weights": V_weights,
                    "V_aggregation": V_aggregation,
                    "share_data_pct": round_int(100 * share_data),
                    "share_weights_pct": round_int(100 * share_weights),
                    "share_aggregation_pct": round_int(100 * share_aggregation),
                    "interaction": interaction,
                },
            }

            # Pillar data-only intervals
            for pid in pillars_spec:
                if pillar_aggs[pid]["score"] is None:
                    pillar_aggs[pid]["interval"] = None
                    continue
                samples = []
                p_measured = pillar_aggs[pid]["measured"]
                if not p_measured:
                    pillar_aggs[pid]["interval"] = None
                    continue
                ids = [m["indicator_id"] for m in p_measured]
                for k in range(n_draws):
                    raws = {}
                    for m in p_measured:
                        j = indicator_ids_sorted.index(m["indicator_id"]) if m["indicator_id"] in indicator_ids_sorted else None
                        if j is None:
                            raws[m["indicator_id"]] = m["raw"]
                        else:
                            raws[m["indicator_id"]] = m["raw"] * (1.0 + m["sigma"] * float(Z[k, j]))
                    samples.append(score_from_values(pillars_spec[pid], raws))
                arr = np.array([s for s in samples if s is not None], dtype=float)
                if arr.size:
                    pq = np.quantile(arr, quantiles)
                    pillar_aggs[pid]["interval"] = {"p2_5": float(pq[0]), "median": float(pq[1]), "p97_5": float(pq[2])}
                else:
                    pillar_aggs[pid]["interval"] = None

        # Grid cells
        sectors = registry["sectors"]
        grid_cells = []
        for sector in sectors:
            sid = sector["id"]
            for pid, pillar in pillars_spec.items():
                cell_measured = []
                for ind in pillar["indicators"]:
                    if ind.get("role") in {"sensitivity_only", "context_only"} or ind.get("exists") is False:
                        continue
                    cands = rows_for(pop_id, ind["id"], sector=sid)
                    chosen = pick_level_value(cands, ind)
                    if chosen is None:
                        continue
                    cell_measured.append(score_indicator(indicators[ind["id"]], chosen, pillar["direction"]))
                if not cell_measured:
                    grid_cells.append({
                        "population": pop_id,
                        "sector_id": sid,
                        "pillar_id": pid,
                        "score": None,
                        "status": "not measured",
                        "grade": None,
                        "n": 0,
                        "coverage": f"0/{len([i for i in pillar['indicators'] if i.get('role') not in {'sensitivity_only','context_only'} and i.get('exists') is not False])}",
                        "obs_ids": [],
                    })
                    continue
                # Cell uses only sector-specific observations (already filtered)
                grades = [m["grade"] for m in cell_measured]
                grade = apply_caps(weakest_grade(grades), sector=sid, pillar=pid, indicator=cell_measured[0], caps=caps)
                # Aggregate like a pillar but only measured cell indicators
                cell_score = mean([m["score"] for m in cell_measured])
                grid_cells.append({
                    "population": pop_id,
                    "sector_id": sid,
                    "pillar_id": pid,
                    "score": cell_score,
                    "status": "scored",
                    "grade": grade,
                    "n": len(cell_measured),
                    "coverage": f"{len(cell_measured)}/{len([i for i in pillar['indicators'] if i.get('role') not in {'sensitivity_only','context_only'} and i.get('exists') is not False])}",
                    "obs_ids": [m["obs_id"] for m in cell_measured],
                    "clipped": any(m["clipped"] for m in cell_measured),
                })

        # Sector gap on scored A/B cells, same population, per pillar and overall Block A if possible
        def cell_gap(pillar_id: str) -> dict | None:
            cells = [
                c for c in grid_cells
                if c["pillar_id"] == pillar_id and c["status"] == "scored" and c["grade"] in {"A", "B"} and c["score"] is not None
            ]
            if len(cells) < 2:
                return None
            top = max(cells, key=lambda c: c["score"])
            bot = min(cells, key=lambda c: c["score"])
            return {
                "pillar_id": pillar_id,
                "gap_points": top["score"] - bot["score"],
                "leader_sector_id": top["sector_id"],
                "leader_score": top["score"],
                "leader_grade": top["grade"],
                "laggard_sector_id": bot["sector_id"],
                "laggard_score": bot["score"],
                "laggard_grade": bot["grade"],
            }

        sector_gaps = [g for g in (cell_gap(pid) for pid in pillars_spec) if g]

        # Paces (indicator-level and pillar-level)
        paces = []
        min_pts = int(method["pace"]["min_comparable_points"])

        def ols_slope(times: list[float], scores: list[float]) -> tuple[float, float, int]:
            t = np.array(times, dtype=float)
            y = np.array(scores, dtype=float)
            n = len(t)
            coef = np.polyfit(t, y, 1)
            slope = float(coef[0])
            fitted = np.polyval(coef, t)
            resid = y - fitted
            ss_t = float(((t - t.mean()) ** 2).sum())
            if n <= 2 or ss_t == 0:
                return slope, float("nan"), n
            se = math.sqrt(float((resid @ resid) / (n - 2) / ss_t))
            return slope, se, n

        TCRIT = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365}

        for pid, pillar in pillars_spec.items():
            for ind in pillar["indicators"]:
                if ind.get("role") in {"sensitivity_only", "context_only"} or ind.get("exists") is False:
                    continue
                cands = rows_for(pop_id, ind["id"], sector="ALL")
                # Group by segment; do not cross segments
                by_seg: dict[str, list] = defaultdict(list)
                for row in cands:
                    by_seg[row.get("segment_id") or "S1"].append(row)
                for seg, group in by_seg.items():
                    group = sorted(group, key=lambda r: r["_end"])
                    if len(group) < min_pts:
                        continue
                    times = [period_midpoint(r["period"]) for r in group]
                    sc = [normalise(r["_value"], ind, pillar["direction"])[0] for r in group]
                    slope, se, n = ols_slope(times, sc)
                    # OLS t interval if n >= 4
                    lo = hi = None
                    if n >= 4 and se == se:  # not NaN
                        tc = TCRIT.get(n - 2, 1.96)
                        lo, hi = slope - tc * se, slope + tc * se
                    # MC over data noise, continuing the same generator
                    mc_slopes = []
                    for k in range(n_draws):
                        ys = []
                        for r in group:
                            try:
                                sig = float(r["sigma"]) if r.get("sigma") else 0.045
                            except ValueError:
                                sig = 0.045
                            x = r["_value"] * (1.0 + sig * float(rng.standard_normal()))
                            ys.append(normalise(x, ind, pillar["direction"])[0])
                        mc_slopes.append(ols_slope(times, ys)[0])
                    mq = np.quantile(np.array(mc_slopes), [0.025, 0.5, 0.975])
                    mc_lo, mc_hi = float(mq[0]), float(mq[2])
                    if lo is None:
                        pub_lo, pub_hi = mc_lo, mc_hi
                    else:
                        # wider of the two
                        if (mc_hi - mc_lo) >= (hi - lo):
                            pub_lo, pub_hi = mc_lo, mc_hi
                        else:
                            pub_lo, pub_hi = lo, hi
                    if pub_lo > 0:
                        wording = "rising"
                    elif pub_hi < 0:
                        wording = "falling"
                    else:
                        wording = "not distinguishable from zero"
                    paces.append({
                        "level": "indicator",
                        "population": pop_id,
                        "pillar_id": pid,
                        "indicator_id": ind["id"],
                        "segment_id": seg,
                        "n_points": n,
                        "periods": [r["period"] for r in group],
                        "slope": slope,
                        "p2_5": pub_lo,
                        "p97_5": pub_hi,
                        "wording": wording,
                    })

        pop_results[pop_id] = {
            "id": pop_id,
            "label": pop["label"],
            "headline": {
                "score": H,
                "geometric_mean": G,
                "status": headline_status,
                "weights": {k: round_half_up(v, 4) for k, v in weights.items()},
                "eligible_pillars": eligible_ids,
                **({
                    "median": mc_out["median"],
                    "p2_5": mc_out["p2_5"],
                    "p97_5": mc_out["p97_5"],
                    "variance_decomposition": mc_out["variance_decomposition"],
                } if mc_out else {}),
            },
            "dai": {
                "score": dai["score"],
                "status": dai["status"],
                "proxy": dai.get("proxy", False),
                **({
                    "median": mc_out["dai"]["median"],
                    "p2_5": mc_out["dai"]["p2_5"],
                    "p97_5": mc_out["dai"]["p97_5"],
                } if mc_out and dai["score"] is not None else {}),
            },
            "pai": {
                "score": pai["score"],
                "status": pai["status"],
                "proxy": pai.get("proxy", False),
                **({
                    "median": mc_out["pai"]["median"],
                    "p2_5": mc_out["pai"]["p2_5"],
                    "p97_5": mc_out["pai"]["p97_5"],
                } if mc_out and pai["score"] is not None else {}),
            },
            "pillars": pillar_aggs,
            "grid_cells": grid_cells,
            "sector_gaps": sector_gaps,
            "paces": paces,
        }

    def publish_number(value):
        if value is None:
            return None
        return round_half_up(float(value), 1)

    def publish_pop(block: dict) -> dict:
        out = json.loads(json.dumps(block))  # deep copy via json for simplicity
        h = out["headline"]
        for key in ("score", "geometric_mean", "median", "p2_5", "p97_5"):
            if key in h and h[key] is not None:
                if key == "score":
                    h["score_unrounded"] = h["score"]
                    h["display"] = round_int(h["score"])
                h[key] = publish_number(h[key])
        for side in ("dai", "pai"):
            for key in ("score", "median", "p2_5", "p97_5"):
                if key in out[side] and out[side][key] is not None:
                    if key == "score":
                        out[side]["score_unrounded"] = out[side][key]
                    out[side][key] = publish_number(out[side][key])
        published_pillars = []
        for pid, ag in out["pillars"].items():
            item = {
                "id": pid,
                "code": ag["code"],
                "block": ag["block"],
                "direction": ag["direction"],
                "score": publish_number(ag["score"]),
                "score_unrounded": ag["score"],
                "status": ag["status"],
                "grade": ag["grade"],
                "n": ag["n"],
                "n_sources": ag["n_sources"],
                "n_official_sources": ag["n_official_sources"],
                "coverage": ag["coverage"],
                "channel_coverage": ag["channel_coverage"],
                "unmeasured_indicators": ag["unmeasured_indicators"],
                "clipped": ag["clipped"],
                "eligible": ag["eligible"],
                "source_ids": ag["source_ids"],
                "channels": {
                    ch: {
                        "score": publish_number(info["score"]),
                        "layers": {
                            layer: {**ld, "score": publish_number(ld["score"])}
                            for layer, ld in info["layers"].items()
                        },
                    }
                    for ch, info in ag["channels"].items()
                },
                "observations": [
                    {
                        "indicator_id": m["indicator_id"],
                        "obs_id": m["obs_id"],
                        "period": m["period"],
                        "raw": m["raw"],
                        "score": publish_number(m["score"]),
                        "clipped": m["clipped"],
                        "grade": m["grade"],
                        "sigma": m["sigma"],
                        "sigma_basis": m["sigma_basis"],
                    }
                    for m in ag["measured"]
                ],
            }
            if ag.get("interval"):
                item["interval"] = {k: publish_number(v) for k, v in ag["interval"].items()}
            published_pillars.append(item)
        out["pillars"] = published_pillars
        out["grid_cells"] = [
            {**c, "score": publish_number(c["score"]) if c["score"] is not None else None}
            for c in out["grid_cells"]
        ]
        for gap in out["sector_gaps"]:
            for key in ("gap_points", "leader_score", "laggard_score"):
                gap[key] = publish_number(gap[key])
        out["paces"] = [
            {**p, "slope": publish_number(p["slope"]), "p2_5": publish_number(p["p2_5"]), "p97_5": publish_number(p["p97_5"])}
            for p in out["paces"]
        ]
        return out

    pipeline_version = read_pipeline_version(version_path)
    hashes = {
        "series.csv": sha256_file(series_path),
        "registry.v1.0.json": sha256_file(registry_path),
        "method.v1.0.json": sha256_file(method_path),
        "brief_signals.csv": sha256_file(brief_path) if brief_path.is_file() else None,
        "planetary_boundaries.json": sha256_file(pb_path) if pb_path.is_file() else None,
    }

    computed = {
        "schema_version": "1.0.0",
        "method_version": method["method_version"],
        "index_version": method["index_version_target"],
        "pipeline_version": pipeline_version,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range_level": "95%",
        "quarter_label": quarter_label(cut),
        "scope_label": "EU27 and Finland, published separately",
        "next_update": None,
        "reference_period": quarter_label(cut),
        "cut_off": cut.isoformat(),
        "channel_weights": {
            "digital": w_digital,
            "physical": w_physical,
            "decision_status": channel_weights.get("decision_status"),
        },
        "vintage": {
            "cut_off": cut.isoformat(),
            "proposed_1_0_0_cut_off": method["data_vintage"]["proposed_1_0_0_cut_off"],
            "hashes": hashes,
        },
        "warnings": warning_messages,
        "stale_observations": [r["obs_id"] for r in stale_rows],
        "populations": {pop_id: publish_pop(block) for pop_id, block in pop_results.items()},
        "brief_signals": brief_rows,
        "planetary_boundaries": pb_data,
        "sources": registry["sources"],
    }
    return computed


def write_computed(computed: dict, output_path: Path = OUTPUT_JSON) -> None:
    output_path.write_text(json.dumps(computed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    computed = compute()
    write_computed(computed)
    lines = [f"[OK] Wrote {OUTPUT_JSON.relative_to(ROOT)} (method {computed['method_version']}, cut-off {computed['cut_off']})"]
    for pop_id, block in computed["populations"].items():
        h = block["headline"]
        score = h.get("score")
        interval = ""
        if h.get("p2_5") is not None:
            interval = f" 95% [{h['p2_5']}–{h['p97_5']}] median {h.get('median')}"
        lines.append(
            f"  {pop_id}: H={score} (display {h.get('display')}) G={h.get('geometric_mean')} "
            f"status={h.get('status')}{interval}"
        )
    for warning in computed.get("warnings") or []:
        lines.append(f"  WARNING: {warning}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
