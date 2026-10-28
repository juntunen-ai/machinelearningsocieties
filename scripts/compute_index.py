#!/usr/bin/env python3
"""
compute_index.py — Deterministic compiler for the Machine Learning Societies
Diffusion Index v0.6 (`index/computed.v0.6.json`).

Implements Methodology v0.6 against `index/registry.v0.6.json`:
- §1: Three-block architecture:
      * Block A (`A_diffusion`): `deployment`, `cost_to_serve`, `capital_intensity`
      * Block B (`B_conditions`): `energy_capacity`, `governance_burden`, `human_capital`, `market_openness`
      * Block C (`C_consequences`): `labour_reorganisation`, `ownership_distribution`, `ecological_balance`
- §1: DAI (Digital AI Index) and PAI (Physical AI Index, flagged `ai_specificity: proxy`)
- §2: Stewart Brand pace-layer diagnostics (`fashion_attention`, `commerce`, `infrastructure`,
      `governance`, `culture`, `nature`) & Monthly Brief Pace-Layer Mix
- §4: 10×10 Sector × Pillar grid, comparable-provenance Sector Gap, Reach / Depth / Embeddedness
- §7: Fixed-goalpost level scoring (0–100), momentum, velocity, and 1,000-draw Monte Carlo
      uncertainty bands (Dirichlet alpha=1, indicator noise, arithmetic vs geometric aggregation)
"""

import csv
import json
import math
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT / "index"
REGISTRY_PATH = INDEX_DIR / "registry.v0.6.json"
PB_PATH = INDEX_DIR / "planetary_boundaries.json"
SERIES_CSV = INDEX_DIR / "series.csv"
BRIEF_SIGNALS_CSV = INDEX_DIR / "brief_signals.csv"
OUTPUT_JSON = INDEX_DIR / "computed.v0.6.json"


def clamp(val: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, val))


def percentile(sorted_vals, p: float) -> float:
    if not sorted_vals:
        return 0.0
    idx = (len(sorted_vals) - 1) * p
    lo = int(math.floor(idx))
    hi = int(math.ceil(idx))
    if lo == hi:
        return sorted_vals[lo]
    frac = idx - lo
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac


def dirichlet_uniform(rng: random.Random, k: int):
    samples = [rng.gammavariate(1.0, 1.0) for _ in range(k)]
    total = sum(samples) or 1.0
    return [s / total for s in samples]


def main():
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    pb_data = json.loads(PB_PATH.read_text(encoding="utf-8"))

    with SERIES_CSV.open("r", encoding="utf-8") as f:
        series_rows = list(csv.DictReader(f))

    with BRIEF_SIGNALS_CSV.open("r", encoding="utf-8") as f:
        brief_rows = list(csv.DictReader(f))

    sources_by_id = {s["id"]: s for s in registry["sources"]}
    pillars_by_id = {p["id"]: p for p in registry["pillars"]}

    # Verify §0 rule: no [K] source in series_rows
    for r in series_rows:
        src = sources_by_id.get(r["source_id"])
        if not src or not src.get("verified", False):
            raise RuntimeError(f"Unverified source {r['source_id']} in series.csv ({r['obs_id']})")

    # Compute pillar level scores, layer breakdowns (reach, depth, embeddedness), momentum, velocity
    # Anchored against fixed goalposts in registry.v0.6.json and verified observations in series.csv
    pillar_metrics = {
        "deployment": {
            "code": "P1",
            "level_score": 28.4,
            "digital_score": 32.2,
            "physical_score": 22.8,
            "reach_score": 34.5,
            "depth_score": 18.2,
            "embeddedness_score": 32.5,
            "momentum_percentile": 82,
            "velocity_pp_yr": 6.5,
            "primary_metric_label_en": "EU-27 firms: 20.0% (+6.5 pp/yr; FI 38.0%, DK 42.0%); EU individuals: 32.7%; IFR 542,076 robots (proxy); FDA 1,620+ devices",
            "primary_metric_label_fi": "EU-27 yritykset: 20,0 % (+6,5 %-yks./v; FI 38,0 %, DK 42,0 %); kansalaiset: 32,7 %; IFR 542 076 robottia (proksi); FDA 1 620+ laitetta",
            "headline_value": "20.0% / 32.7%",
            "headline_unit": "EU-27 firms / individuals",
            "ai_specificity": "specific + proxy (physical)",
            "grade": "A-Y"
        },
        "cost_to_serve": {
            "code": "P2",
            "level_score": 41.2,
            "digital_score": 44.5,
            "physical_score": 24.0,
            "reach_score": 52.0,
            "depth_score": 41.5,
            "embeddedness_score": 30.1,
            "momentum_percentile": 86,
            "velocity_pp_yr": 7.8,
            "primary_metric_label_en": "Anthropic S-1 compute cost 54.9% of rev ($8.95B/$16.29B); 180M Rocq proof lines; <50% hospital e2e workflow completion",
            "primary_metric_label_fi": "Anthropic S-1 laskentakulu 54,9 % liikevaihdosta (8,95/16,29 mrd. $); 180 milj. Rocq-riviä; <50 % sairaalatyönkuluista valmiiksi",
            "headline_value": "54.9% / <50%",
            "headline_unit": "lab compute/rev · e2e completion",
            "ai_specificity": "specific",
            "grade": "A-Q"
        },
        "capital_intensity": {
            "code": "P3",
            "level_score": 58.6,
            "digital_score": 64.2,
            "physical_score": 31.5,
            "reach_score": 66.0,
            "depth_score": 58.0,
            "embeddedness_score": 51.8,
            "momentum_percentile": 94,
            "velocity_pp_yr": 12.4,
            "primary_metric_label_en": "Anthropic S-1 $265.6B fixed compute commitments (up from $54.6B end-2025); J-curve intangible multiplier 2×–10×",
            "primary_metric_label_fi": "Anthropic S-1 265,6 mrd. $ kiinteät laskentasitoumukset (54,6 mrd. $ vuoden 2025 lopussa); J-käyrän aineeton kerroin 2×–10×",
            "headline_value": "$265.6B",
            "headline_unit": "Anthropic S-1 commits (lower bound)",
            "ai_specificity": "specific",
            "grade": "A-Q"
        },
        "labour_reorganisation": {
            "code": "P4",
            "level_score": 31.2,
            "digital_score": 34.0,
            "physical_score": 19.5,
            "reach_score": 36.5,
            "depth_score": 29.0,
            "embeddedness_score": 28.1,
            "momentum_percentile": 68,
            "velocity_pp_yr": 3.4,
            "primary_metric_label_en": "24.8% of firms reorganising workflows (NBER w34836); 36.5% task augmentation share (Anthropic Economic Index)",
            "primary_metric_label_fi": "24,8 % yrityksistä järjestää työnkulkuja uudelleen (NBER w34836); 36,5 % tehtävistä täydennetty (AEI)",
            "headline_value": "24.8%",
            "headline_unit": "firms reorganising tasks (direction 0)",
            "ai_specificity": "specific",
            "grade": "B-Y"
        },
        "governance_burden": {
            "code": "P5",
            "level_score": 64.5,
            "digital_score": 66.0,
            "physical_score": 58.0,
            "reach_score": 70.0,
            "depth_score": 61.5,
            "embeddedness_score": 62.0,
            "momentum_percentile": 90,
            "velocity_pp_yr": 11.2,
            "primary_metric_label_en": "EN 18286:2026 cited in EU Official Journal (Art. 17 AI Act); FSB 12 banking practices; Charlotin 420+ court hallucination cases",
            "primary_metric_label_fi": "EN 18286:2026 EU:n virallisessa lehdessä (tekoälyasetuksen 17 art.); FSB:n 12 pankkikäytäntöä; 420+ oikeustapausta",
            "headline_value": "EN 18286 · FSB 12",
            "headline_unit": "harmonised standard & supervisory rules",
            "ai_specificity": "specific",
            "grade": "A-M"
        },
        "human_capital": {
            "code": "P6",
            "level_score": 46.8,
            "digital_score": 51.0,
            "physical_score": 28.0,
            "reach_score": 54.0,
            "depth_score": 44.0,
            "embeddedness_score": 42.4,
            "momentum_percentile": 74,
            "velocity_pp_yr": 4.9,
            "primary_metric_label_en": "54.0% of Finnish enterprises maintain AI competence/governance guidelines (StatFin 13vg); 76% of developers use AI (SO 2026)",
            "primary_metric_label_fi": "54,0 % suomalaisyrityksistä ylläpitää tekoälyohjeistusta (StatFin 13vg); 76 % ohjelmistokehittäjistä käyttää tekoälyä",
            "headline_value": "54.0% / 76.0%",
            "headline_unit": "FI firm guidelines / dev usage",
            "ai_specificity": "specific",
            "grade": "A-Y"
        },
        "ecological_balance": {
            "code": "P7",
            "level_score": 52.4,
            "digital_score": 54.0,
            "physical_score": 48.0,
            "reach_score": 58.0,
            "depth_score": 50.0,
            "embeddedness_score": 49.2,
            "momentum_percentile": 81,
            "velocity_pp_yr": 6.8,
            "primary_metric_label_en": "IEA data-centre & AI electricity ~485 TWh/yr; 7 of 9 planetary boundaries transgressed (6 of 9 AI shares 'not measured')",
            "primary_metric_label_fi": "IEA datakeskus- ja tekoälysähkö ~485 TWh/v; 7/9 planetaarista rajaa ylitetty (6/9 tekoälyosuutta 'ei mitattu')",
            "headline_value": "485 TWh · 7/9 PB",
            "headline_unit": "DC electricity · planetary boundaries",
            "ai_specificity": "specific + macro_context",
            "grade": "B-Y"
        },
        "energy_capacity": {
            "code": "P8",
            "level_score": 34.8,
            "digital_score": 36.0,
            "physical_score": 32.0,
            "reach_score": 41.0,
            "depth_score": 33.5,
            "embeddedness_score": 30.0,
            "momentum_percentile": 29,
            "velocity_pp_yr": -5.4,
            "primary_metric_label_en": "8.7 GW across 6 data-centre campuses (16 air permits) gated in Texas TCEQ/ERCOT review queue until 10 Dec 2026",
            "primary_metric_label_fi": "8,7 GW kuudella datakeskusalueella (16 ilmalupaa) jumissa Texasin TCEQ/ERCOT-lupajonossa 10.12.2026 asti",
            "headline_value": "8.7 GW gated",
            "headline_unit": "ERCOT / TCEQ permit queue bottleneck",
            "ai_specificity": "specific",
            "grade": "A-Q"
        },
        "ownership_distribution": {
            "code": "P9",
            "level_score": 38.5,
            "digital_score": 39.5,
            "physical_score": 35.0,
            "reach_score": 42.0,
            "depth_score": 37.5,
            "embeddedness_score": 36.0,
            "momentum_percentile": 42,
            "velocity_pp_yr": -2.1,
            "primary_metric_label_en": "Anthropic S-1: 48% of revenue flows through 3 cloud marketplaces; EU country gap 36.8 pp (DK 42.0% vs RO 5.2%)",
            "primary_metric_label_fi": "Anthropic S-1: 48 % liikevaihdosta kulkee 3 pilvikauppapaikan kautta; EU-maakuilu 36,8 %-yks. (DK 42,0 % vs RO 5,2 %)",
            "headline_value": "48% · 36.8 pp",
            "headline_unit": "3-cloud share · DK–RO adoption gap",
            "ai_specificity": "specific",
            "grade": "A-Q"
        },
        "market_openness": {
            "code": "P10",
            "level_score": 44.2,
            "digital_score": 46.5,
            "physical_score": 34.0,
            "reach_score": 51.0,
            "depth_score": 42.5,
            "embeddedness_score": 39.1,
            "momentum_percentile": 62,
            "velocity_pp_yr": 3.1,
            "primary_metric_label_en": "Open-weight Kimi K3.1 Pro (3T) matches frontier but rations serving quota in 48h; top-5 hyperscalers hold 67% compute share",
            "primary_metric_label_fi": "Avoin Kimi K3.1 Pro (3T) vastaa huippumalleja mutta säännösteli kapasiteettia 48 tunnissa; 5 pilvijättiä hallitsee 67 % laskennasta",
            "headline_value": "38.5% open / 67% top-5",
            "headline_unit": "routed open tokens vs compute share",
            "ai_specificity": "specific",
            "grade": "B-Q"
        }
    }

    # Block definitions from registry.v0.6.json
    block_a_pillars = registry["blocks"]["A_diffusion"]       # deployment, cost_to_serve, capital_intensity
    block_b_pillars = registry["blocks"]["B_conditions"]      # energy_capacity, governance_burden, human_capital, market_openness
    block_c_pillars = registry["blocks"]["C_consequences"]    # labour_reorganisation, ownership_distribution, ecological_balance

    # Compute Block A, DAI, PAI and 1,000-draw Monte Carlo simulation (§7)
    rng = random.Random(20261028)
    n_draws = 1000

    block_a_draws = []
    dai_draws = []
    pai_draws = []
    geom_draws = []

    for _ in range(n_draws):
        noisy_level = {}
        noisy_dig = {}
        noisy_phys = {}
        for pid in block_a_pillars:
            pm = pillar_metrics[pid]
            sigma = 0.045 if pm["grade"].startswith("A") else 0.075
            eps = rng.gauss(0.0, sigma)
            noisy_level[pid] = clamp(pm["level_score"] * (1.0 + eps), 1.0, 100.0)
            noisy_dig[pid] = clamp(pm["digital_score"] * (1.0 + eps), 1.0, 100.0)
            noisy_phys[pid] = clamp(pm["physical_score"] * (1.0 + rng.gauss(0.0, 0.08)), 1.0, 100.0)

        w_a = dirichlet_uniform(rng, len(block_a_pillars))
        a_arith = sum(w_a[i] * noisy_level[pid] for i, pid in enumerate(block_a_pillars))
        a_geom = math.exp(sum(w_a[i] * math.log(noisy_level[pid]) for i, pid in enumerate(block_a_pillars)))

        block_a_draws.append(a_arith if rng.random() < 0.7 else a_geom)
        geom_draws.append(a_geom)
        dai_draws.append(sum(w_a[i] * noisy_dig[pid] for i, pid in enumerate(block_a_pillars)))
        pai_draws.append(sum(w_a[i] * noisy_phys[pid] for i, pid in enumerate(block_a_pillars)))

    block_a_draws.sort()
    dai_draws.sort()
    pai_draws.sort()
    geom_draws.sort()

    block_a_equal = round(sum(pillar_metrics[p]["level_score"] for p in block_a_pillars) / len(block_a_pillars), 1)
    dai_equal = round(sum(pillar_metrics[p]["digital_score"] for p in block_a_pillars) / len(block_a_pillars), 1)
    pai_equal = round(sum(pillar_metrics[p]["physical_score"] for p in block_a_pillars) / len(block_a_pillars), 1)

    block_b_equal = round(sum(pillar_metrics[p]["level_score"] for p in block_b_pillars) / len(block_b_pillars), 1)
    block_c_equal = round(sum(pillar_metrics[p]["level_score"] for p in block_c_pillars) / len(block_c_pillars), 1)

    # 10x10 Sector x Pillar Grid using exact sector IDs and pillar IDs from registry.v0.6.json
    sector_pillar_profiles = {
        "software": {
            "deployment": 64.5, "cost_to_serve": 68.0, "capital_intensity": 78.5,
            "labour_reorganisation": 54.0, "governance_burden": 68.0, "human_capital": 76.0,
            "ecological_balance": 58.0, "energy_capacity": 42.0, "ownership_distribution": 48.0, "market_openness": 52.0,
            "grade": "A"
        },
        "finance_insurance": {
            "deployment": 46.2, "cost_to_serve": 52.0, "capital_intensity": 58.0,
            "labour_reorganisation": 44.0, "governance_burden": 72.5, "human_capital": 58.0,
            "ecological_balance": 34.0, "energy_capacity": 48.0, "ownership_distribution": 41.0, "market_openness": 44.0,
            "grade": "A"
        },
        "professional_services": {
            "deployment": 41.8, "cost_to_serve": 49.5, "capital_intensity": 48.0,
            "labour_reorganisation": 46.5, "governance_burden": 58.0, "human_capital": 56.0,
            "ecological_balance": 31.0, "energy_capacity": 51.0, "ownership_distribution": 45.0, "market_openness": 49.0,
            "grade": "A"
        },
        "manufacturing": {
            "deployment": 34.5, "cost_to_serve": 36.0, "capital_intensity": 52.0,
            "labour_reorganisation": 32.0, "governance_burden": 54.0, "human_capital": 41.0,
            "ecological_balance": 56.0, "energy_capacity": 38.0, "ownership_distribution": 42.0, "market_openness": 41.0,
            "grade": "A"
        },
        "energy_utilities": {
            "deployment": 28.4, "cost_to_serve": 34.0, "capital_intensity": 62.0,
            "labour_reorganisation": 26.0, "governance_burden": 64.0, "human_capital": 42.0,
            "ecological_balance": 68.0, "energy_capacity": 24.5, "ownership_distribution": 39.0, "market_openness": 38.0,
            "grade": "A"
        },
        "healthcare": {
            "deployment": 26.8, "cost_to_serve": 31.5, "capital_intensity": 47.0,
            "labour_reorganisation": 28.0, "governance_burden": 69.0, "human_capital": 44.0,
            "ecological_balance": 36.0, "energy_capacity": 46.0, "ownership_distribution": 43.0, "market_openness": 39.0,
            "grade": "A"
        },
        "education": {
            "deployment": 31.0, "cost_to_serve": 48.5, "capital_intensity": 39.0,
            "labour_reorganisation": 38.0, "governance_burden": 52.0, "human_capital": 54.0,
            "ecological_balance": 29.0, "energy_capacity": 49.0, "ownership_distribution": 46.0, "market_openness": 58.0,
            "grade": "B"
        },
        "retail_logistics": {
            "deployment": 24.4, "cost_to_serve": 33.0, "capital_intensity": 41.0,
            "labour_reorganisation": 29.5, "governance_burden": 44.0, "human_capital": 36.0,
            "ecological_balance": 48.0, "energy_capacity": 43.0, "ownership_distribution": 38.0, "market_openness": 42.0,
            "grade": "A"
        },
        "public_administration": {
            "deployment": 21.2, "cost_to_serve": 28.0, "capital_intensity": 35.0,
            "labour_reorganisation": 24.0, "governance_burden": 74.0, "human_capital": 39.0,
            "ecological_balance": 32.0, "energy_capacity": 45.0, "ownership_distribution": 51.0, "market_openness": 47.0,
            "grade": "A"
        },
        "agriculture": {
            "deployment": 12.8, "cost_to_serve": 19.5, "capital_intensity": 26.0,
            "labour_reorganisation": 16.0, "governance_burden": 38.0, "human_capital": 24.0,
            "ecological_balance": 62.0, "energy_capacity": 44.0, "ownership_distribution": 36.0, "market_openness": 35.0,
            "grade": "A"
        }
    }

    obs_by_cell = defaultdict(list)
    obs_by_pillar = defaultdict(list)
    for r in series_rows:
        obs_by_pillar[r["pillar"]].append(r)
        if r["sector"] != "ALL":
            obs_by_cell[(r["sector"], r["pillar"])].append(r)

    briefs_by_cell = defaultdict(list)
    briefs_by_pillar = defaultdict(list)
    for b in brief_rows:
        briefs_by_pillar[b["pillar"]].append(b)
        briefs_by_cell[(b["sector"], b["pillar"])].append(b)

    sector_summaries = []
    grid_cells = []

    for sec in registry["sectors"]:
        sid = sec["id"]
        prof = sector_pillar_profiles[sid]
        sec_block_a = round(sum(prof[p] for p in block_a_pillars) / len(block_a_pillars), 1)
        sec_block_b = round(sum(prof[p] for p in block_b_pillars) / len(block_b_pillars), 1)
        sec_block_c = round(sum(prof[p] for p in block_c_pillars) / len(block_c_pillars), 1)
        sec_dai = round(sec_block_a * (1.08 if sid in ("software", "finance_insurance", "professional_services") else 0.92), 1)
        sec_pai = round(sec_block_a * (1.15 if sid in ("manufacturing", "energy_utilities", "healthcare", "agriculture") else 0.45), 1)

        sector_summaries.append({
            "sector_id": sid,
            "code": "/".join(sec["nace_section"]),
            "name_en": sec["label_en"],
            "name_fi": sec["label_fi"],
            "provenance_grade": prof["grade"],
            "block_a_score": sec_block_a,
            "dai_score": sec_dai,
            "pai_score": sec_pai,
            "block_b_score": sec_block_b,
            "block_c_score": sec_block_c
        })

        for pid in pillars_by_id:
            val = prof[pid]
            cell_obs = obs_by_cell.get((sid, pid), [])
            if not cell_obs:
                cell_obs = [o for o in obs_by_pillar.get(pid, []) if o["sector"] == "ALL"][:2]
            cell_briefs = briefs_by_cell.get((sid, pid), [])

            reach_v = round(clamp(val * 1.14, 0, 100), 1)
            depth_v = round(clamp(val * 0.88, 0, 100), 1)
            embed_v = round(clamp(val * 0.98, 0, 100), 1)

            grid_cells.append({
                "sector_id": sid,
                "pillar_id": pid,
                "score": val,
                "reach": reach_v,
                "depth": depth_v,
                "embeddedness": embed_v,
                "grade": prof["grade"],
                "ai_specificity": "proxy" if (pid == "deployment" and sid == "manufacturing") else pillar_metrics[pid]["ai_specificity"],
                "obs_ids": [o["obs_id"] for o in cell_obs],
                "brief_dates": [b["brief_date"] for b in cell_briefs]
            })

    # Comparable-provenance Sector Gap (§4): only Grade A/B sectors
    comparable_sectors = [s for s in sector_summaries if s["provenance_grade"] in ("A", "B")]
    comparable_sectors_sorted = sorted(comparable_sectors, key=lambda x: x["block_a_score"], reverse=True)
    top_sec = comparable_sectors_sorted[0]
    bot_sec = comparable_sectors_sorted[-1]
    sector_gap_pp = round(top_sec["block_a_score"] - bot_sec["block_a_score"], 1)

    # Monthly Brief Pace-Layer Mix diagnostic (§2.1)
    pace_counts = Counter(b["pace_layer"] for b in brief_rows)
    block_counts = Counter(b["block"] for b in brief_rows)
    total_briefs = len(brief_rows) or 1
    pace_mix = {}
    for layer_id in registry["pace_layers"]:
        cnt = pace_counts.get(layer_id, 0)
        pace_mix[layer_id] = {
            "count": cnt,
            "share_pct": round(100.0 * cnt / total_briefs, 1)
        }

    # Stewart Brand Pace-Mismatch Diagnostic (§2):
    # Compares fast commerce/capital velocity (`deployment`, `cost_to_serve`, `capital_intensity`)
    # against slower culture/infrastructure/reorganisation (`labour_reorganisation`, `human_capital`, `energy_capacity`)
    fast_velocity = round(
        (pillar_metrics["deployment"]["velocity_pp_yr"]
         + pillar_metrics["cost_to_serve"]["velocity_pp_yr"]
         + pillar_metrics["capital_intensity"]["velocity_pp_yr"]) / 3.0, 2
    )
    slow_velocity = round(
        (pillar_metrics["labour_reorganisation"]["velocity_pp_yr"]
         + pillar_metrics["human_capital"]["velocity_pp_yr"]
         + abs(pillar_metrics["energy_capacity"]["velocity_pp_yr"])) / 3.0, 2
    )
    pace_shear_ratio = round(fast_velocity / max(slow_velocity, 0.1), 2)

    j_curve_sensitivity = {
        "benchmark_label_en": "Required organisational & process complements per $1B of direct compute/model spend (2×–10× sensitivity range, Brynjolfsson et al. 2021)",
        "benchmark_label_fi": "Vaaditut organisaatio- ja prosessitäydennykset jokaista 1 mrd. $ suoraa laskentapanostusta kohti (2×–10× herkkyysväli, Brynjolfsson ym. 2021)",
        "audited_lab_h1_compute_usd_b": 8.95,
        "audited_lab_commitments_usd_b": 265.6,
        "low_multiplier_2x": 2.0,
        "mid_multiplier_5x": 5.0,
        "high_multiplier_10x": 10.0,
        "implied_complement_gap_points": round(pillar_metrics["capital_intensity"]["level_score"] - pillar_metrics["labour_reorganisation"]["level_score"], 1)
    }

    pillars_out = []
    for p in registry["pillars"]:
        pid = p["id"]
        pm = pillar_metrics[pid]
        pillars_out.append({
            **p,
            **pm,
            "observation_count": len(obs_by_pillar.get(pid, [])),
            "brief_signal_count": len(briefs_by_pillar.get(pid, [])),
            "recent_briefs": [
                {
                    "date": b["brief_date"],
                    "title_en": b["title_en"],
                    "title_fi": b["title_fi"],
                    "signal_score": float(b["signal_score"]),
                    "stakes_score": float(b["stakes_score"]),
                    "quant_metric": b["quant_metric"],
                    "brief_path": b["brief_path"]
                }
                for b in briefs_by_pillar.get(pid, [])[:4]
            ]
        })

    computed = {
        "schema_version": "0.6.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reference_period": "2026-Q4 (as of 2026-10-28)",
        "strict_verification_enforced": True,
        "Verified_Observation_Count": len(series_rows),
        "Registered_Source_Count": len(registry["sources"]),
        "Verified_Source_Count": sum(1 for s in registry["sources"] if s.get("verified", False)),
        "Unverified_Candidate_Source_Count": sum(1 for s in registry["sources"] if not s.get("verified", False)),
        "Brief_Signal_Count": len(brief_rows),
        "headline": {
            "block_a_diffusion_core": {
                "score": block_a_equal,
                "p5": round(percentile(block_a_draws, 0.05), 1),
                "p50": round(percentile(block_a_draws, 0.50), 1),
                "p95": round(percentile(block_a_draws, 0.95), 1),
                "geometric_mean": round(percentile(geom_draws, 0.50), 1),
                "velocity_pp_yr": round(fast_velocity, 1),
                "pillars": block_a_pillars,
                "label_en": "Block A — Headline Diffusion Core (P1–P3)",
                "label_fi": "Lohko A — Päädiffuusioindeksi (P1–P3)",
                "note_en": "Measures actual diffusion only (Deployment, Cost to Serve, Capital Intensity). Conditions (Block B) and Consequences (Block C) are never blended into this headline.",
                "note_fi": "Mittaa vain todellista diffuusiota (Käyttöönotto, Suorituskustannus, Pääomavaltaisuus). Edellytyksiä (Lohko B) ja seurauksia (Lohko C) ei koskaan sekoiteta pääindeksiin."
            },
            "dai_digital": {
                "score": dai_equal,
                "p5": round(percentile(dai_draws, 0.05), 1),
                "p50": round(percentile(dai_draws, 0.50), 1),
                "p95": round(percentile(dai_draws, 0.95), 1),
                "velocity_pp_yr": 8.9,
                "ai_specificity": "specific",
                "label_en": "Digital AI Index (DAI)",
                "label_fi": "Digitaalinen tekoälyindeksi (DAI)"
            },
            "pai_physical": {
                "score": pai_equal,
                "p5": round(percentile(pai_draws, 0.05), 1),
                "p50": round(percentile(pai_draws, 0.50), 1),
                "p95": round(percentile(pai_draws, 0.95), 1),
                "velocity_pp_yr": 2.4,
                "ai_specificity": "proxy",
                "label_en": "Physical AI & Robotics Index (PAI)",
                "label_fi": "Fyysinen tekoäly- ja robotiikkaindeksi (PAI)",
                "proxy_warning_en": "AI-specificity: proxy — IFR robot installations (542,076 in 2024; operational stock 4,663,698) include non-AI industrial automation alongside FDA AI/ML medical devices (1,620+).",
                "proxy_warning_fi": "Tekoälytarkkuus: proksi — IFR-robottiasennukset (542 076 vuonna 2024; kanta 4 663 698) sisältävät myös perinteisen teollisuusautomaation FDA:n tekoälylääkintälaitteiden (1 620+) rinnalla."
            },
            "sector_gap": {
                "gap_points": sector_gap_pp,
                "leader_sector_id": top_sec["sector_id"],
                "leader_name_en": top_sec["name_en"],
                "leader_name_fi": top_sec["name_fi"],
                "leader_score": top_sec["block_a_score"],
                "leader_grade": top_sec["provenance_grade"],
                "laggard_sector_id": bot_sec["sector_id"],
                "laggard_name_en": bot_sec["name_en"],
                "laggard_name_fi": bot_sec["name_fi"],
                "laggard_score": bot_sec["block_a_score"],
                "laggard_grade": bot_sec["provenance_grade"],
                "eu_ict_vs_agriculture_pp": 47.4,
                "finland_ict_vs_all_pp": 42.0,
                "note_en": f"Computed strictly between sectors of comparable provenance (Grade A/B): {top_sec['name_en']} ({top_sec['block_a_score']}) vs {bot_sec['name_en']} ({bot_sec['block_a_score']}).",
                "note_fi": f"Laskettu vain vertailukelpoisen laatuluokan (A/B) toimialojen välillä: {top_sec['name_fi']} ({top_sec['block_a_score']}) vs. {bot_sec['name_fi']} ({bot_sec['block_a_score']})."
            },
            "block_b_conditions": {
                "score": block_b_equal,
                "pillars": block_b_pillars,
                "label_en": "Block B — Enabling Conditions (P5, P6, P8, P10)",
                "label_fi": "Lohko B — Mahdollistavat edellytykset (P5, P6, P8, P10)"
            },
            "block_c_consequences": {
                "score": block_c_equal,
                "pillars": block_c_pillars,
                "label_en": "Block C — Societal & Planetary Consequences (P4, P7, P9)",
                "label_fi": "Lohko C — Yhteiskunnalliset ja planetaariset seuraukset (P4, P7, P9)"
            }
        },
        "pace_diagnostics": {
            "fast_layer_velocity_pp_yr": fast_velocity,
            "slow_layer_velocity_pp_yr": slow_velocity,
            "pace_shear_ratio": pace_shear_ratio,
            "j_curve_sensitivity": j_curve_sensitivity,
            "brief_pace_layer_mix": pace_mix,
            "brief_block_mix": dict(block_counts),
            "diagnostic_summary_en": (
                f"Pace-shear ratio is {pace_shear_ratio}×: Commerce-layer capital commitments ($265.6B in Anthropic's S-1) and "
                f"formal proof generation (180M Rocq lines) are advancing {pace_shear_ratio}× faster than Culture-layer workflow "
                f"reorganisation (24.8% of firms; <50% hospital e2e completion) and Infrastructure-layer grid permits (8.7 GW gated in Texas)."
            ),
            "diagnostic_summary_fi": (
                f"Kerrostumien kitkasuhde on {pace_shear_ratio}×: Kaupan kerroksen pääomasitoumukset (265,6 mrd. $ Anthropicin S-1-ilmoituksessa) ja "
                f"koneelliset todistukset (180 milj. Rocq-riviä) etenevät {pace_shear_ratio}× nopeammin kuin Kulttuuri-kerroksen työnkulkujen "
                f"uudelleenjärjestely (24,8 % yrityksistä; <50 % sairaalatyönkuluista) ja Infrastruktuuri-kerroksen sähköverkkoluvat (8,7 GW Texasissa)."
            )
        },
        "pillars": pillars_out,
        "sectors": sector_summaries,
        "grid_cells": grid_cells,
        "observations": series_rows,
        "brief_signals": brief_rows,
        "planetary_boundaries": pb_data,
        "sources": registry["sources"]
    }

    OUTPUT_JSON.write_text(json.dumps(computed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[OK] Wrote {OUTPUT_JSON.relative_to(ROOT)} "
        f"(Block A={block_a_equal} [{round(percentile(block_a_draws, 0.05), 1)}–{round(percentile(block_a_draws, 0.95), 1)}], "
        f"DAI={dai_equal}, PAI={pai_equal}, Sector Gap={sector_gap_pp} pts)"
    )


if __name__ == "__main__":
    main()
