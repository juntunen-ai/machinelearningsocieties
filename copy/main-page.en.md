# AI Diffusion Index 1.0.0 – main page copy (English)

Status: draft copy for `diffusion-index.html` in branch `release/1.0.0`. Written by Wedgwood, 22 Nov 2026. Not published. Release needs Harri's separate approval.

Rules for this copy (Harri, 22 Nov 2026): English only, no Finnish text on the page. Plain English for a broad audience. Short sentences. No jargon in the top sections (Blocks A–C, geometric mean and Monte Carlo belong on the methodology page). The methodology page `diffusion-method.html` is Massi's and is only linked from here. No transparency or open-data section on the main page. No analytics.

All numbers are `{{placeholders}}`. The page JS fills them from `index/computed.*.json`. Names use the JSON key path. The full list is at the end of this file. Nothing goes live while any `{{...}}` remains.

Notes for Kernelio are in *italics, prefixed "Build note"*. They are not page text.

---

## 0. Page metadata (head)

- **title:** AI Diffusion Index 1.0.0 — Machine Learning Societies
- **meta description:** The AI Diffusion Index measures how far AI has moved from the lab into everyday work, machines and society. Updated every quarter.
- **og:title:** AI Diffusion Index: {{headline.block_a_diffusion_core.score}}/100 ({{reference_period}})
- **og:description:** The money has arrived. The use hasn't. How far AI has moved from the lab into everyday work, machines and society.
- **og:image:** `assets/adi/adi-og-1200x675.png` (not yet created; see image plan)
- **og:image:alt:** AI Diffusion Index {{headline.block_a_diffusion_core.score}} out of 100, {{reference_period}}
- **twitter:card:** summary_large_image

*Build note: language toggle and Finnish RSS link removed from this page. Force English on this page without writing to localStorage, so the bilingual daily briefs keep the reader's own choice.*

---

## 1. Opening (anchor `#summary`)

**Kicker:** AI Diffusion Index 1.0.0 · {{reference_period}} · {{SCOPE_LABEL}}

**H1:** AI Diffusion Index

**What we measure:** how far AI has moved from the lab into everyday work, machines and society.

**The result:** {{headline.block_a_diffusion_core.score}}/100 in {{reference_period}} ({{RANGE_LEVEL}} range {{headline.block_a_diffusion_core.p5}}–{{headline.block_a_diffusion_core.p95}}).

**What it means:** AI is not yet everyday infrastructure. The money is far ahead of real use.

Buttons: [See the gap](#gap) · [How we calculate it →](diffusion-method.html)

*Build note: headline score is shown rounded to a whole number (plan TP4). Range ends rounded the same way.*

---

## 2. The gap (anchor `#gap`)

**H2:** The money has arrived. The use hasn't.

Companies and investors are committing large sums to AI. Far fewer companies use AI in their daily work. And AI still cannot be trusted to finish multi-step tasks on its own.

**Chart slot: one simple bar chart, three bars, same 0–100 scale.**

| Bar label | Value | One-line explanation |
|---|---|---|
| Money committed | {{pillars.capital_intensity.level_score}}/100 | Capital commitments: money locked into data centres, AI chips and long-term cloud contracts. |
| Companies using AI | {{pillars.deployment.level_score}}/100 | Company adoption: how many companies, public agencies and people use AI in daily work. |
| Tasks done reliably | {{pillars.cost_to_serve.level_score}}/100 | Reliable task completion: what it costs to finish a real job with AI, from start to finish, including fixing failures. |

**Caption:** Three of the index's measures, {{reference_period}}. All on the same 0–100 scale. Sources and data: [methodology page](diffusion-method.html).

**Chart alt text:** Bar chart. Money committed {{pillars.capital_intensity.level_score}}, companies using AI {{pillars.deployment.level_score}}, tasks done reliably {{pillars.cost_to_serve.level_score}}, out of 100.

*Build note (conditional): keep this headline only if the capital score is clearly above the other two after recalculation (plan TP4). If not, Wedgwood rewrites this section before release.*
*Build note (conditional): plan TP1 moves cost_to_serve to grade C until a Task Price Index exists. If it is not published in 1.0.0, drop the third bar and the third sentence of the paragraph and use two bars.*

---

## 3. How to read the score (anchor `#scale`)

**H2:** How to read the score

**{{headline.block_a_diffusion_core.score}}/100 ({{RANGE_LEVEL}} range {{headline.block_a_diffusion_core.p5}}–{{headline.block_a_diffusion_core.p95}}).** The range shows our uncertainty. The true value is most likely inside it.

100 is not “good” and 0 is not “bad”. The index measures how widely AI is used, not whether that is desirable. 100 means AI has become dependable everyday infrastructure, like electricity.

**Scale ruler:** left label "0 · Almost no real use" · marker "▲ {{headline.block_a_diffusion_core.score}} · {{reference_period}}" · right label "100 · Like electricity"

Three small cards:

1. **Weakest-link score: {{headline.block_a_diffusion_core.geometric_mean}}/100.** A stricter version of the score. It falls when any one part lags behind the others.
2. **Speed: {{headline.block_a_diffusion_core.velocity_pp_yr}} points a year.** How fast the score is changing at its current pace.
3. **Updated every quarter.** The score changes only on the fixed quarterly update. Next update: {{NEXT_UPDATE_DATE}}. Daily briefs do not move it in between.

*Build note (conditional): show the Speed card only if the frozen method allows it (plan TP1: at least 3 comparable time points). Otherwise remove the card. Show the speed with a sign, e.g. +3.*

---

## 4. Start here – doors for audiences (anchor `#doors`)

**H2:** Start here

- **Policymakers and officials:** [the result in three lines](#summary).
- **Journalists:** [quotable findings, chart images and contact](#press).
- **Researchers and analysts:** [full methodology, data and sources](diffusion-method.html).
- **Investors and companies:** [AI use by industry](#industry-matrix).

*Build note: `#industry-matrix` = id on the existing "10 Industries × 10 Pillars" heading. The data sections that follow (KPI cards, blocks, matrix, pillars, ledgers) are Kernelio's and Massi's; their headings still carry v0.6 numbers.*

---

## 5. For journalists (anchor `#press`)

**H3:** For journalists

**Quotable findings ({{reference_period}}):**

- The AI Diffusion Index stands at {{headline.block_a_diffusion_core.score}} out of 100 ({{RANGE_LEVEL}} range {{headline.block_a_diffusion_core.p5}}–{{headline.block_a_diffusion_core.p95}}).
- Capital commitments score {{pillars.capital_intensity.level_score}}. Company adoption scores {{pillars.deployment.level_score}}. Reliable task completion scores {{pillars.cost_to_serve.level_score}}.
- 100 would mean AI works like electricity: dependable, everyday infrastructure. A high score is not a judgement that AI is good.

**Chart images:** [headline score](assets/adi/adi-headline-1200x675.png) · [the gap](assets/adi/adi-gap-1200x675.png) · [industries](assets/adi/adi-industries-1200x675.png)

**Contact:** Harri Juntunen on [x.com/hjuntunen](https://x.com/hjuntunen) or [linkedin.com/in/hjuntunen](https://www.linkedin.com/in/hjuntunen).

**Methodology:** [how the index is calculated](diffusion-method.html).

*Build note: image files do not exist yet. Reuse terms for images follow the licence decision in plan TP3 (open item); add one line once decided.*

---

## 6. Who makes this (anchor `#credit`)

**H3:** Who makes this

**{{PUBLISHER_LINE}}**

AI Diffusion Index 1.0.0 · {{reference_period}} · Prepared with the help of AI tools.

---

## 7. Footer

Machine Learning Societies · AI Diffusion Index 1.0.0 · {{PUBLISHER_LINE}} · Daily Briefs · Methodology · Forecasts · About · RSS

*Build note: the main page has no open-data / replication section (Harri, 22 Nov 2026). Data files stay in `index/`; the methodology page links them.*

---

## Placeholders

Key paths refer to `index/computed.*.json` (checked against `computed.v0.6.json`, schema 0.6.0). `pillars` is an array; `pillars.<id>` means the item whose `id` is `<id>`. v0.6 values are for reference only and must not be reused.

| Placeholder | JSON key | Meaning | v0.6 value |
|---|---|---|---|
| `{{headline.block_a_diffusion_core.score}}` | yes | Headline score (show rounded to a whole number) | 42.7 |
| `{{headline.block_a_diffusion_core.p5}}` | yes | Lower end of range | 32.0 |
| `{{headline.block_a_diffusion_core.p95}}` | yes | Upper end of range | 53.4 |
| `{{headline.block_a_diffusion_core.geometric_mean}}` | yes | "Weakest-link score" (geometric mean, sensitivity check) | 40.5 |
| `{{headline.block_a_diffusion_core.velocity_pp_yr}}` | yes | Annual speed, points per year | 8.9 |
| `{{pillars.capital_intensity.level_score}}` | yes | Capital commitments (P3) | 58.6 |
| `{{pillars.deployment.level_score}}` | yes | Company adoption (P1) | 28.4 |
| `{{pillars.cost_to_serve.level_score}}` | yes | Reliable task completion (P2) | 41.2 |
| `{{reference_period}}` | yes | Quarter label | "2026-Q4 (as of 2026-10-28)" |
| `{{RANGE_LEVEL}}` | **no** | Range level label, e.g. "95%" | (90% in v0.6) |
| `{{SCOPE_LABEL}}` | **no** | Population covered, e.g. "EU27 and Finland" (plan §2.4) | – |
| `{{NEXT_UPDATE_DATE}}` | **no** | Next fixed quarterly update, e.g. "13 April 2027" | – |
| `{{PUBLISHER_LINE}}` | **no** | Publisher / author credit line (name not decided yet); static text, not from JSON | – |

Notes on missing or mismatched keys:
- `RANGE_LEVEL`: v0.6 gives `p5`/`p95`, which is a 90% range. Plan TP1/TP4 asks for a 95% range. If the method moves to 95%, the keys will change (e.g. `p2_5`/`p97_5`), and the label must match them. Suggest adding a key such as `range_level`.
- `reference_period` in v0.6 carries extra text "(as of 2026-10-28)". For the kicker and og:title a short quarter label (e.g. `2026-Q4`) reads better. Suggest a separate key such as `quarter_label`.
- `SCOPE_LABEL` and `NEXT_UPDATE_DATE`: no key in v0.6. Suggest adding `scope_label` and `next_update` to the computed JSON, or keeping them as static text.
- `PUBLISHER_LINE`: publisher name is still undecided (22 Nov 2026). No disclosure or candidacy line on the page: the transparency section is out of scope (Harri, 22 Nov 2026).
- Version "1.0.0" is written as text, not taken from `schema_version`.
