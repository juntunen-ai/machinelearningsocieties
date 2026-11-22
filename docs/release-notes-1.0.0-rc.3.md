# Machine Learning Societies – Diffusion Index 1.0.0-rc.3 — draft release notes

Status: draft for branch `release/1.0.0`. This file is documentation only. It is **not** a GitHub Release, and it must not be turned into a git tag until Harri gives a separate publication approval.

Date: 22 November 2026 (Europe/Helsinki).

## What this candidate is

The third assembled 1.0.0 release candidate of the Machine Learning Societies – Diffusion Index. It succeeds 1.0.0-rc.2 after Harri Juntunen’s method decision of 22 November 2026, 18:15 (Europe/Helsinki): the headline is the deployment pillar (company adoption) alone; capital intensity (K1) moves to Block B as context; the Monte Carlo draws the digital channel weight from U[0.25, 0.75] instead of holding it fixed at 0.5.

Scores come from `index/series.csv` through the frozen method in `index/method.v1.0.json`. The public English dashboard is `diffusion-index.html`. The full method is `diffusion-method.html` (a page mirror of `index/method.v1.0.md`; the Markdown and JSON method files are Massi’s and were not edited in this page pass).

Pipeline version: `1.0.0-rc.3`. Method edition: 1.0. Data cut-off: 2026-12-31 (2026-Q4), as proposed in the method. Figures on the page are marked preliminary and will be recomputed before release.

## Headline figures

EU27 and Finland are published separately and are never averaged. The headline is company adoption only. Capital intensity is a context indicator and is not in the headline.

**Headline impact versus rc.2:** moving K1 out of Block A, and drawing the digital weight in the Monte Carlo, changes the published headlines from EU27 22 and Finland 28 to EU27 9 and Finland 17 (display integers).

| Population | Headline (display) | Geometric sensitivity | 95% range | Status |
|---|---|---|---|---|
| EU27 | 9 / 100 (9.3 unrounded 9.34) | 9.3 (equals the headline) | 6–13 (5.6–13.2) | scored |
| Finland | 17 / 100 (17.3 unrounded 17.33) | 17.3 (equals the headline) | 10–24 (10.4–24.4) | scored |

For the EU27, capital commitments (context, not in the headline) score 34.0 (31.0–37.0) and company adoption, the headline, is 9.3 (5.6–13.2). For Finland the figures are 39.3 (35.8–42.8) and 17.3 (10.4–24.4). Reliable task completion (`cost_to_serve`) remains experimental and is not in the headline, until a Task Price Index exists. Ecological balance is not measured: no AI-specific burden, abatement or Jevons rebound figure is published.

The width of the headline range comes almost entirely from the digital-versus-physical channel weighting (the digital share is drawn from U[0.25, 0.75]), not from the data. Variance shares are 1 % data, 99 % channel weights and 0 % aggregation in both populations.

The industry matrix is sparse by design: 4 of 100 EU27 cells and 1 of 100 Finland cells are scored. Unmeasured cells are labelled “n/m”.

## Lead line (placeholder)

The previous hero lead, “The money has arrived. The use hasn't.”, no longer fits as the headline message, because the headline no longer mixes capital with use. It is kept only as context framing on the Block B capital-versus-use card, where it remains factually true (capital 34 / 39 versus use 9 / 17).

The live lead on the public page is a placeholder pending Wedgwood:

1. **Live placeholder:** “Company adoption of AI remains limited: 9 out of 100 in the EU27 and 17 in Finland.”
2. “The headline measures company adoption only. It stands at 9 out of 100 in the EU27 and 17 in Finland.”
3. “Most companies have not yet put AI into everyday work. The headline is 9 in the EU27 and 17 in Finland, on a 0–100 scale.”
4. “On a 0–100 scale of company adoption, the EU27 scores 9 and Finland 17.”

Option 1 is on the page because it states both published scores, stays factual, and does not claim more than the deployment pillar supports.

## Still open before a 1.0.0 publication

- Wedgwood’s final wording of the headline lead (the live text is the placeholder in option 1).
- Harri's publisher credit line (`{{PUBLISHER_LINE}}`).
- Harri's next-update date (`{{NEXT_UPDATE_DATE}}` / `next_update`).
- Press chart images and the Open Graph image (not yet created).
- Binary favicons (`favicon.ico`, `favicon-32.png`); the SVG favicon is already on the branch.
- Final publication approval (no deploy, no tag from this branch until then).
- Recompute figures before a tagged release (data cut-off 31 Dec 2026).

The digital/physical channel weights are decided for 1.0.0: the point estimate stays 0.5 / 0.5, and the Monte Carlo draws the digital weight from U[0.25, 0.75]. The TP3 licence audit is on the branch.

## How to check the numbers

```
python3 -m pip install -r requirements.txt
python3 scripts/compute_index.py
python3 -m pytest -q
```
