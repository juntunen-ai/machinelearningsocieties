"""Statistical coherence check across the 27 EU member states (JRC COIN audit step).

Appendix only: reads the Eurostat 2025 member-state files in
docs/analysis/data/eurostat_ms_2025/ and the goalposts in index/method.v1.0.json,
scores every member state with the v1.0 Block A rules (channel weights and
the rc.2 equal deployment/capital weighting, cost_to_serve absent) and prints the
correlation matrix, indicator->pillar and pillar->headline correlations and the
K1 share of the headline. It never writes index/computed.v1.0.json.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs" / "analysis" / "data" / "eurostat_ms_2025"
MS = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
CODES = {"E_AI_TANY": "D1", "E_AI_TGE3": "D3", "E_AI_TAR": "D4", "E_AI_TPVSG": "PVSG"}


def jsonstat(path: Path) -> list[tuple[dict, float]]:
    d = json.loads(path.read_text(encoding="utf-8"))
    ids, size = d["id"], d["size"]
    cats = [sorted(d["dimension"][k]["category"]["index"].items(), key=lambda x: x[1]) for k in ids]
    out = []
    for key, value in d["value"].items():
        k, idx = int(key), []
        for s in reversed(size):
            idx.append(k % s)
            k //= s
        idx.reverse()
        out.append(({ids[i]: cats[i][idx[i]][0] for i in range(len(ids))}, value))
    return out


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = a.argsort().argsort(), b.argsort().argsort()
    return float(np.corrcoef(ra, rb)[0, 1])


def main() -> None:
    method = json.loads((ROOT / "index" / "method.v1.0.json").read_text(encoding="utf-8"))
    inds = {i["id"][:2]: i for p in method["pillars"] for i in p["indicators"] if i["id"][:2] in {"D1", "D2", "D3", "D4", "K1"} and not i["id"].startswith("K1x")}
    cw = method["scoring"]["within_pillar_aggregation"]["channel_weights"]
    # The coherence check evaluates the rc.2 structure that motivated the rc.3 decision:
    # deployment and capital_intensity at equal effective weight. In rc.3 the headline
    # is deployment alone, so its pillar->headline correlation is 1 by construction.
    w_dep = 0.5

    data = {c: {} for c in MS}
    for k, v in jsonstat(DATA / "eb.json"):
        data[k["geo"]][CODES[k["indic_is"]]] = v
    for k, v in jsonstat(DATA / "iaiu.json"):
        data[k["geo"]]["D2"] = v
    k1: dict = {}
    for k, v in jsonstat(DATA / "an6.json"):
        k1.setdefault((k["geo"], k["time"]), {})[k["asset10"]] = v
    for c in MS:
        for y in ("2025", "2024"):
            x = k1.get((c, y), {})
            if "N1132G" in x and "N117G" in x:
                data[c]["K1"] = round(x["N1132G"] + x["N117G"], 1)
                break
    names = ["D1", "D2", "D3", "D4", "K1"]
    rows = [c for c in MS if all(n in data[c] for n in names)]
    X = {n: np.array([data[c][n] for c in rows], dtype=float) for n in names}
    S = {n: np.clip((X[n] - inds[n]["floor"]) / (inds[n]["ceiling"] - inds[n]["floor"]) * 100, 0, 100) for n in names}
    digital = ((S["D1"] + S["D2"]) / 2 + S["D3"]) / 2  # reach layer (D1, D2), depth layer (D3)
    dep = float(cw["digital"]) * digital + float(cw["physical"]) * S["D4"]
    H = w_dep * dep + (1 - w_dep) * S["K1"]
    share = (1 - w_dep) * S["K1"] / H

    print(f"Member states with all five indicators: {len(rows)}")
    M = np.corrcoef([X[n] for n in names])
    print("\nPearson r, raw values, 2025\n      " + " ".join(f"{n:>6}" for n in names))
    for i, n in enumerate(names):
        print(f"{n:>5} " + " ".join(f"{M[i, j]:6.2f}" for j in range(len(names))))
    print("\nindicator -> deployment pillar r:", {n: round(float(np.corrcoef(X[n], dep)[0, 1]), 2) for n in names[:4]})
    print("indicator -> headline r:", {n: round(float(np.corrcoef(X[n], H)[0, 1]), 2) for n in names})
    print("pillar -> headline r: deployment %.2f, capital_intensity %.2f" % (np.corrcoef(dep, H)[0, 1], np.corrcoef(S["K1"], H)[0, 1]))
    print("Spearman: deployment vs K1 %.2f, headline vs K1 %.2f, headline vs deployment %.2f" % (spearman(dep, S["K1"]), spearman(H, S["K1"]), spearman(H, dep)))
    print("K1 share of the headline across member states: min %.0f %%, median %.0f %%, max %.0f %%" % (100 * share.min(), 100 * np.median(share), 100 * share.max()))
    print("Highest D4: %s %.2f; highest K1: %s %.1f" % (max(rows, key=lambda c: data[c]["D4"]), max(X["D4"]), max(rows, key=lambda c: data[c]["K1"]), max(X["K1"])))


if __name__ == "__main__":
    main()
