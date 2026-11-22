# AI Diffusion Index 1.0.0-rc.1 — draft release notes

Status: draft for branch `release/1.0.0`. This file is documentation only. It is **not** a GitHub Release, and it must not be turned into a git tag until Harri gives a separate publication approval.

Date: 22 November 2026 (Europe/Helsinki).

## What this candidate is

The first assembled 1.0.0 release candidate of the Machine Learning Societies AI Diffusion Index. Scores come from `index/series.csv` through the frozen method in `index/method.v1.0.json`. The public English dashboard is `diffusion-index.html`. The full method is `diffusion-method.html`.

Pipeline version: `1.0.0-rc.1`. Method edition: 1.0. Data cut-off: 2026-12-31 (2026-Q4), as proposed in the method.

## Headline figures

EU27 and Finland are published separately and are never averaged.

| Population | Headline (display) | Geometric sensitivity | 95% range | Status |
|---|---|---|---|---|
| EU27 | 22 / 100 (21.7 unrounded 21.67) | 17.8 | 17–27 | scored |
| Finland | 28 / 100 (28.3 unrounded 28.33) | 26.1 | 24–33 | scored |

For the EU27, capital commitments score 34.0 and company adoption scores 9.3. For Finland the figures are 39.3 and 17.3. Reliable task completion (`cost_to_serve`) is experimental in 1.0.0 and is not in the headline, until a Task Price Index exists.

## Still open before a 1.0.0 publication

- Harri's decision on the digital/physical 50/50 channel weights.
- Harri's publisher credit line (`{{PUBLISHER_LINE}}`).
- Harri's next-update date (`{{NEXT_UPDATE_DATE}}` / `next_update`).
- Press chart images and the Open Graph image (not yet created).
- Binary favicons (`favicon.ico`, `favicon-32.png`); the SVG favicon is already on the branch.
- Massi's check of remaining method discrepancies (staleness vs the worked-example paces, OBS-012 mapping, the channel-weights JSON parameter).
- Licence audit (TP3) and final publication approval (no deploy, no tag from this branch until then).

## How to check the numbers

```
python3 -m pip install -r requirements.txt
python3 scripts/compute_index.py
python3 -m pytest -q
```

The golden file is `index/computed.v1.0.json`. A rerun must match it except for `generated_at`.
