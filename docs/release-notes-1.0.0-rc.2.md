# AI Diffusion Index 1.0.0-rc.2 — draft release notes

Status: draft for branch `release/1.0.0`. This file is documentation only. It is **not** a GitHub Release, and it must not be turned into a git tag until Harri gives a separate publication approval.

Date: 22 November 2026 (Europe/Helsinki).

## What this candidate is

The second assembled 1.0.0 release candidate of the Machine Learning Societies AI Diffusion Index. It succeeds 1.0.0-rc.1, which was rejected in review because the planetary panel still showed v0.6 constants while ecological balance was not measured.

Scores come from `index/series.csv` through the frozen method in `index/method.v1.0.json`. The public English dashboard is `diffusion-index.html`. The full method is `diffusion-method.html`.

Pipeline version: `1.0.0-rc.2`. Method edition: 1.0. Data cut-off: 2026-12-31 (2026-Q4), as proposed in the method. Figures on the page are marked preliminary and will be recomputed before release.

## Headline figures

EU27 and Finland are published separately and are never averaged.

**Headline impact versus v0.6:** the v0.6 headline 42.7 was a hand-set constant, not a computed score. Under method v1.0 the compiled headlines are EU27 22 and Finland 28 (display integers).

| Population | Headline (display) | Geometric sensitivity | 95% range | Status |
|---|---|---|---|---|
| EU27 | 22 / 100 (21.7 unrounded 21.67) | 17.8 | 17–27 | scored |
| Finland | 28 / 100 (28.3 unrounded 28.33) | 26.1 | 24–33 | scored |

For the EU27, capital commitments score 34.0 and company adoption scores 9.3. For Finland the figures are 39.3 and 17.3. Reliable task completion (`cost_to_serve`) is experimental in 1.0.0 and is not in the headline, until a Task Price Index exists. Ecological balance is not measured: no AI-specific burden, abatement or Jevons rebound figure is published.

The industry matrix is sparse by design: 4 of 100 EU27 cells and 1 of 100 Finland cells are scored. Unmeasured cells are labelled “n/m”.

## Still open before a 1.0.0 publication

- Harri's decision on the digital/physical 50/50 channel weights.
- Harri's publisher credit line (`{{PUBLISHER_LINE}}`).
- Harri's next-update date (`{{NEXT_UPDATE_DATE}}` / `next_update`).
- Press chart images and the Open Graph image (not yet created).
- Binary favicons (`favicon.ico`, `favicon-32.png`); the SVG favicon is already on the branch.
- Licence audit (TP3) and final publication approval (no deploy, no tag from this branch until then).
- Recompute figures before a tagged release (data cut-off 31 Dec 2026).

## How to check the numbers

```
python3 -m pip install -r requirements.txt
python3 scripts/compute_index.py
python3 -m pytest -q
```
