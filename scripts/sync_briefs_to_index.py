#!/usr/bin/env python3
"""
sync_briefs_to_index.py — Synchronises Machine Learning Societies daily briefs
(`briefs/YYYY-MM-DD.html` and `briefs/index.json`) into the Diffusion Index v0.6
qualitative/quantitative signal log (`index/brief_signals.csv`).

Implements Methodology v0.6 §2.1 (Monthly Brief Pace-Layer Mix diagnostic) and
links daily institutional signals to the 10 Pillars, 10 NACE Rev. 2.1 sectors,
Blocks A/B/C, and Reach / Depth / Embeddedness layers in `registry.v0.6.json`.
"""

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIEFS_DIR = ROOT / "briefs"
INDEX_DIR = ROOT / "index"
BRIEF_SIGNALS_CSV = INDEX_DIR / "brief_signals.csv"

# Curated ground-truth classifications for published briefs (using exact registry.v0.6.json IDs)
CURATED_MAP = {
    "2026-10-28": {
        "pillar": "capital_intensity",
        "secondary_pillar": "governance_burden",
        "sector": "software",
        "block": "A_diffusion",
        "pace_layer": "governance",
        "channel": "digital",
        "layer": "embeddedness",
        "level": "macro",
        "source_id": "sec_edgar",
        "quant_metric": "$16.29B H1 rev; $8.95B compute cost; $265.6B commitments; 48% cloud marketplace share",
        "summary_note": "Anthropic PBC Form S-1 makes frontier lab compute economics and cloud marketplace concentration auditable under SEC disclosure rules."
    },
    "2026-10-27": {
        "pillar": "human_capital",
        "secondary_pillar": "governance_burden",
        "sector": "education",
        "block": "B_conditions",
        "pace_layer": "culture",
        "channel": "digital",
        "layer": "embeddedness",
        "level": "meso",
        "source_id": "oecd_ai",
        "quant_metric": "3 Lean-checked proofs; independent scientific referee consortium",
        "summary_note": "OpenAI published Lean-checked proofs and convened external referee groups to verify machine-generated formal mathematics."
    },
    "2026-10-26": {
        "pillar": "market_openness",
        "secondary_pillar": "cost_to_serve",
        "sector": "software",
        "block": "B_conditions",
        "pace_layer": "infrastructure",
        "channel": "digital",
        "layer": "depth",
        "level": "meso",
        "source_id": "epoch_ai_data",
        "quant_metric": "3T parameters; 1M context; subscriber inference rationing within 48h",
        "summary_note": "Moonshot AI shipped open-weight Kimi K3.1 Pro (3T params) and rationed inference quotas within 48 hours, proving serving capacity is the binding constraint."
    },
    "2026-10-25": {
        "pillar": "energy_capacity",
        "secondary_pillar": "ecological_balance",
        "sector": "energy_utilities",
        "block": "B_conditions",
        "pace_layer": "infrastructure",
        "channel": "physical",
        "layer": "embeddedness",
        "level": "macro",
        "source_id": "ercot_large_load_queue",
        "quant_metric": "8.7 GW across 6 data-centre campuses; 16 permits gated by TCEQ/ERCOT",
        "summary_note": "Texas TCEQ paused standard air permits for behind-the-meter data-centre gas turbines, gating 8.7 GW of on-site power capacity until Dec 2026."
    },
    "2026-10-24": {
        "pillar": "governance_burden",
        "secondary_pillar": "deployment",
        "sector": "software",
        "block": "B_conditions",
        "pace_layer": "infrastructure",
        "channel": "digital",
        "layer": "depth",
        "level": "micro",
        "source_id": "oecd_ai",
        "quant_metric": "Air-gapped training clusters; critical Brotli patch in Node.js, Bun, Envoy",
        "summary_note": "OpenAI air-gapped frontier training clusters after a DNS misconfiguration and exported a critical Brotli security patch across core web infrastructure."
    },
    "2026-10-23": {
        "pillar": "cost_to_serve",
        "secondary_pillar": "labour_reorganisation",
        "sector": "software",
        "block": "A_diffusion",
        "pace_layer": "commerce",
        "channel": "digital",
        "layer": "depth",
        "level": "meso",
        "source_id": "gdpval",
        "quant_metric": "180M lines of machine-checked Rocq proofs across 123 open-source libraries",
        "summary_note": "Anthropic and Theorem generated 180M lines of formal Rocq proofs across 123 libraries, shifting scarcity from proof labour to formal specification."
    },
    "2026-10-22": {
        "pillar": "deployment",
        "secondary_pillar": "market_openness",
        "sector": "software",
        "block": "A_diffusion",
        "pace_layer": "commerce",
        "channel": "digital",
        "layer": "embeddedness",
        "level": "meso",
        "source_id": "sec_edgar",
        "quant_metric": "GPT-6 family added to Google Cloud Marketplace commitment drawdowns",
        "summary_note": "Google Cloud added OpenAI's GPT-6 family to its Marketplace so enterprise usage draws down existing cloud commits, turning model adoption into a procurement line item."
    },
    "2026-10-21": {
        "pillar": "capital_intensity",
        "secondary_pillar": "deployment",
        "sector": "healthcare",
        "block": "A_diffusion",
        "pace_layer": "commerce",
        "channel": "digital",
        "layer": "embeddedness",
        "level": "meso",
        "source_id": "sec_edgar",
        "quant_metric": "Acquisition of Orchestra Bio into Rosalind clinical workflow layer (J-curve complement)",
        "summary_note": "OpenAI acquired drug-development coordination platform Orchestra Bio to own the regulated audit trail and workflow complement in life sciences."
    },
    "2026-10-19": {
        "pillar": "cost_to_serve",
        "secondary_pillar": "deployment",
        "sector": "healthcare",
        "block": "A_diffusion",
        "pace_layer": "commerce",
        "channel": "digital",
        "layer": "embeddedness",
        "level": "micro",
        "source_id": "stanford_ai_index",
        "quant_metric": "<50% end-to-end hospital/payer workflow completion vs >90% single-step QA",
        "summary_note": "Stanford HAI benchmarks show frontier models pass 90%+ of single-step clinical questions but complete under half of multi-step administrative workflows."
    },
    "2026-10-15": {
        "pillar": "governance_burden",
        "secondary_pillar": "deployment",
        "sector": "finance_insurance",
        "block": "B_conditions",
        "pace_layer": "governance",
        "channel": "digital",
        "layer": "depth",
        "level": "macro",
        "source_id": "oecd_ai",
        "quant_metric": "12 common FSB supervisory & lifecycle practices for banks and insurers",
        "summary_note": "The Financial Stability Board published 12 common AI governance and third-party risk practices for banks, insurers, and financial supervisors."
    },
    "2026-10-14": {
        "pillar": "governance_burden",
        "secondary_pillar": "deployment",
        "sector": "public_administration",
        "block": "B_conditions",
        "pace_layer": "governance",
        "channel": "digital",
        "layer": "embeddedness",
        "level": "macro",
        "source_id": "eur_lex",
        "quant_metric": "EN 18286:2026 cited in Official Journal (Art. 17 AI Act presumption of conformity)",
        "summary_note": "European Commission cited EN 18286:2026 in the Official Journal, giving providers a harmonised quality-management standard under Article 17 of the EU AI Act."
    }
}


def fix_mojibake(text: str) -> str:
    if not text:
        return text
    if "Ã" in text or "â€" in text or "Â·" in text:
        try:
            return text.encode("latin-1").decode("utf-8")
        except Exception:
            pass
    return text


def auto_classify(title: str, text_body: str):
    """Fallback keyword classifier for new daily briefs not yet in CURATED_MAP."""
    blob = (title + " " + text_body).lower()
    pillar = "deployment"
    secondary_pillar = "governance_burden"
    sector = "software"
    block = "A_diffusion"
    pace_layer = "commerce"
    channel = "digital"
    layer = "depth"
    level = "meso"
    source_id = "oecd_ai"

    if any(k in blob for k in ["standard", "statute", "commission", "fsb", "sec ", "s-1", "act", "supervisor", "regulation"]):
        pillar, block, pace_layer, level = "governance_burden", "B_conditions", "governance", "macro"
    elif any(k in blob for k in ["gigawatt", "power", "turbine", "electricity", "ercot", "grid"]):
        pillar, block, pace_layer, level = "energy_capacity", "B_conditions", "infrastructure", "macro"
    elif any(k in blob for k in ["proof", "lean", "rocq", "theorem", "benchmark", "stanford"]):
        pillar, block, pace_layer, level = "cost_to_serve", "A_diffusion", "commerce", "meso"

    if any(k in blob for k in ["hospital", "clinical", "drug", "bio", "health"]):
        sector = "healthcare"
    elif any(k in blob for k in ["bank", "insur", "financial", "fsb"]):
        sector = "finance_insurance"
    elif any(k in blob for k in ["grid", "power", "energy", "ercot", "tceq", "electricity"]):
        sector = "energy_utilities"
        channel = "physical"
    elif any(k in blob for k in ["proof", "research", "university", "stanford"]):
        sector = "education"

    return {
        "pillar": pillar,
        "secondary_pillar": secondary_pillar,
        "sector": sector,
        "block": block,
        "pace_layer": pace_layer,
        "channel": channel,
        "layer": layer,
        "level": level,
        "source_id": source_id,
        "quant_metric": "Extracted from daily brief",
        "summary_note": title
    }


def parse_brief_html(html_path: Path):
    content = html_path.read_text(encoding="utf-8")
    sig_match = re.search(r"Signal\s+(\d+(?:\.\d+)?)/10\s*·\s*Stakes\s+(\d+(?:\.\d+)?)/10", content)
    signal_score = float(sig_match.group(1)) if sig_match else 5.0
    stakes_score = float(sig_match.group(2)) if sig_match else 5.0

    p_match = re.search(r"(?:Primary source|P)\s*[=:]\s*(\d+)", content)
    n_match = re.search(r"(?:Independent confirmation|N)\s*[=:]\s*(\d+)", content)
    l_match = re.search(r"(?:First mover|L)\s*[=:]\s*(\d+)", content)
    p_val = int(p_match.group(1)) if p_match else 2
    n_val = int(n_match.group(1)) if n_match else 2
    l_val = int(l_match.group(1)) if l_match else 0
    market_test = f"Primary={p_val};Confirmation={n_val};FirstMover={l_val}"

    urls = re.findall(r'href="(https?://[^"]+)"', content)
    seen = []
    for u in urls:
        if u not in seen:
            seen.append(u)
    primary_urls = " | ".join(seen[:4])

    return signal_score, stakes_score, market_test, primary_urls, content


def main():
    index_json_path = BRIEFS_DIR / "index.json"
    briefs_index = json.loads(index_json_path.read_text(encoding="utf-8"))

    cleaned_any = False
    for entry in briefs_index:
        for k, v in list(entry.items()):
            if isinstance(v, str):
                fixed = fix_mojibake(v)
                if fixed != v:
                    entry[k] = fixed
                    cleaned_any = True
    if cleaned_any:
        index_json_path.write_text(
            json.dumps(briefs_index, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        print("Fixed UTF-8 mojibake in briefs/index.json")

    rows = []
    for entry in sorted(briefs_index, key=lambda x: x["date"], reverse=True):
        date_str = entry["date"]
        title_en = entry.get("title", "")
        title_fi = entry.get("title_fi", "")
        html_file = BRIEFS_DIR / f"{date_str}.html"
        if not html_file.exists():
            continue

        signal_score, stakes_score, market_test, primary_urls, raw_html = parse_brief_html(html_file)
        meta = CURATED_MAP.get(date_str) or auto_classify(title_en, raw_html)

        rows.append({
            "brief_date": date_str,
            "title_en": title_en,
            "title_fi": title_fi,
            "pillar": meta["pillar"],
            "secondary_pillar": meta["secondary_pillar"],
            "sector": meta["sector"],
            "block": meta["block"],
            "pace_layer": meta["pace_layer"],
            "channel": meta["channel"],
            "layer": meta["layer"],
            "level": meta["level"],
            "signal_score": signal_score,
            "stakes_score": stakes_score,
            "market_test": market_test,
            "source_id": meta["source_id"],
            "quant_metric": meta["quant_metric"],
            "primary_urls": primary_urls,
            "brief_path": f"briefs/{date_str}.html",
            "summary_note": meta["summary_note"]
        })

    fieldnames = [
        "brief_date", "title_en", "title_fi", "pillar", "secondary_pillar",
        "sector", "block", "pace_layer", "channel", "layer", "level",
        "signal_score", "stakes_score", "market_test", "source_id",
        "quant_metric", "primary_urls", "brief_path", "summary_note"
    ]
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    with BRIEF_SIGNALS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} brief signal rows to {BRIEF_SIGNALS_CSV}")


if __name__ == "__main__":
    main()
