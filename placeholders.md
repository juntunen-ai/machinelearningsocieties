# AI Diffusion Index 1.0.0 – main page placeholders

Status: draft copy in branch `release/1.0.0` (Wedgwood, 22.11.2026). Not published.
Page: `diffusion-index.html`. Methodology page: `diffusion-method.html` (content by Massi, not changed here).

Every `{{NAME}}` below must be filled from the 1.0.0 recalculation (plan TP1/TP2) before release.
Nothing may be published while any `{{...}}` remains (`rg -n '\{\{' diffusion-index.html` must return nothing).
Kernelio decides how they are filled: build step, or JS from `computed` JSON.

| Placeholder | Meaning | Format | v0.6 value (for reference only, do not reuse) |
|---|---|---|---|
| `{{HEADLINE_SCORE}}` | Headline score, rounded to a whole number (plan TP4) | integer, e.g. `43` | 42.7 |
| `{{RANGE_LEVEL}}` | Uncertainty range level | `95%` (plan TP1/TP4) – see note | 90% |
| `{{RANGE_LOW}}` | Lower end of the range | integer | 32.0 |
| `{{RANGE_HIGH}}` | Upper end of the range | integer | 53.4 |
| `{{CAPITAL_SCORE}}` | Capital commitments pillar (P3 Capital intensity) | integer 0–100 | 58.6 |
| `{{ADOPTION_SCORE}}` | Company adoption pillar (P1 Deployment) | integer 0–100 | 28.4 |
| `{{TASK_SCORE}}` | Reliable task completion (P2 Cost to serve) | integer 0–100 | 41.2 |
| `{{BOTTLENECK_SCORE}}` | "Weakest-link score" = geometric mean (sensitivity check, floor 1.0) | integer | 40.5 |
| `{{ANNUAL_SPEED}}` | Annual speed, points per year, with sign | e.g. `+3` | +8.9 |
| `{{QUARTER_LABEL}}` | Reference quarter | e.g. `2026-Q4` | 2026-Q4 |
| `{{SCOPE_LABEL}}` | Population covered (plan §2.4: EU27 and Finland separately) | e.g. `EU27 and Finland` | – |
| `{{NEXT_UPDATE_DATE}}` | Next fixed quarterly update | e.g. `13 April 2027` (second Tuesday of the month after quarter end, proposal) | – |

Used in: `<head>` og tags (`HEADLINE_SCORE`, `QUARTER_LABEL`), the ruler pin and bar widths (`style="left:{{HEADLINE_SCORE}}%"`, `width:{{CAPITAL_SCORE}}%` etc.), opening, gap chart, scale section, journalist section, credit.

## Conditional blocks (see HTML comments)
- **Gap headline** ("The money has arrived. The use hasn't."): keep only if `CAPITAL_SCORE` is clearly above `ADOPTION_SCORE` and `TASK_SCORE` after recalculation. Otherwise Wedgwood rewrites it.
- **Third bar** (`TASK_SCORE`): plan TP1 moves cost_to_serve to grade C until a Task Price Index exists. If P2 is not published, use two bars.
- **Annual speed card**: show only if the frozen method allows it (≥ 3 comparable time points). Otherwise delete the card.

## Notes
- `RANGE_LEVEL`: Wedgwood's brief used "90% range"; the plan (TP1, TP4) says a 95% range. It is a placeholder so Massi's frozen method decides.
- Image files referenced but not yet created: `assets/adi/adi-og-1200x675.png`, `adi-headline-1200x675.png`, `adi-gap-1200x675.png`, `adi-industries-1200x675.png`.
- Sections below the new copy (KPI grid, blocks, pace layers, matrix, pillars, briefs ledger, planetary boundaries, observations, sources) are unchanged apart from removing the Finnish text. Their headings still carry v0.6 numbers (e.g. "56", "49 sources"), and their JS still renders v0.6 data.
