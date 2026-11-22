# Machine Learning Societies – Diffusion Index 1.0.0-rc.3: main page copy (English)

Status: draft copy for `diffusion-index.html` in branch `release/1.0.0`. Written by Wedgwood, 22 Nov 2026. Not published. Release needs Harri's separate approval.

Rules for this copy (Harri, 22 Nov 2026): English only, no Finnish text on the page. Plain English for a broad audience. Short sentences. No jargon in the top sections (Blocks A–C, geometric mean and Monte Carlo belong on the methodology page). The methodology page `diffusion-method.html` is Massi's and is only linked from here. No transparency or open-data section on the main page. No analytics.

All numbers are `{{placeholders}}`. The page JS fills them from `index/computed.*.json`. Names use the JSON key path. The full list is at the end of this file. Nothing goes live while any `{{...}}` remains.

Notes for Kernelio are in *italics, prefixed "Build note"*. They are not page text.

---

## 0. Page metadata (head)

- **title:** Machine Learning Societies – Diffusion Index 1.0.0-rc.3
- **meta description:** The Machine Learning Societies – Diffusion Index measures how far AI has moved from the lab into everyday work, machines and society. Updated every quarter.
- **og:title:** Machine Learning Societies – Diffusion Index: {{headline.display}}/100 ({{reference_period}})
- **og:description:** Most companies have not yet put AI to work. Company adoption scores 9 out of 100 in the EU27 and 17 in Finland.
- **og:site_name:** Machine Learning Societies – Diffusion Index
- **twitter:title:** Machine Learning Societies – Diffusion Index
- **og:image:** `assets/adi/adi-og-1200x675.png` (not yet created; see image plan)
- **og:image:alt:** Machine Learning Societies – Diffusion Index {{headline.display}} out of 100, {{reference_period}}
- **twitter:card:** summary_large_image

*Build note: language toggle and Finnish RSS link removed from this page. Force English on this page without writing to localStorage, so the bilingual daily briefs keep the reader's own choice.*

---

## 1. Opening (anchor `#summary`)

**Kicker:** Machine Learning Societies – Diffusion Index 1.0.0-rc.3 · {{reference_period}} · {{SCOPE_LABEL}}

**H1:** Machine Learning Societies – Diffusion Index

**What we measure:** how far AI has moved from the lab into everyday work, machines and society.

**The result:** {{headline.display}}/100 in {{reference_period}} ({{RANGE_LEVEL}} range {{headline.p2_5}}–{{headline.p97_5}}). The headline is the deployment pillar (company adoption) alone.

**What it means:** Most companies have not yet put AI to work. Company adoption scores {{populations.EU27.headline.display}} out of 100 in the EU27 and {{populations.FI.headline.display}} in Finland. The width of the range comes almost entirely from how digital and physical adoption are weighed (digital share 25–75 %), not from the data.

Buttons: [See the gap](#gap) · [How we calculate it →](diffusion-method.html)

*Build note: headline score is shown rounded to a whole number (plan TP4). Range ends rounded the same way.*

---

## 2. The gap (anchor `#gap`)

**H2:** The money has arrived. The use hasn't.

Companies and investors are committing large sums to AI. Far fewer companies use AI in their daily work. And AI still cannot be trusted to finish multi-step tasks on its own.

**Chart slot: one simple bar chart, three bars, same 0–100 scale.**

| Bar label | Value | One-line explanation |
|---|---|---|
| Money committed | {{pillars.capital_intensity.score}}/100 | Capital commitments: a context indicator, outside the headline. Money locked into data centres, AI chips and long-term cloud contracts. |
| Companies using AI | {{pillars.deployment.score}}/100 | Company adoption: the headline. How many companies, public agencies and people use AI in daily work. |

**Caption:** Capital commitments (context, outside the headline) vs company adoption (the headline), {{reference_period}}. Both on the same 0–100 scale. Reliable task completion is experimental and is not in this chart or the headline. Sources and data: [methodology page](diffusion-method.html).

**Chart alt text:** Bar chart. Money committed {{pillars.capital_intensity.score}} (context, outside the headline), companies using AI {{pillars.deployment.score}} (the headline), out of 100.

*Build note: the H2 “The money has arrived. The use hasn't.” is kept as context framing for capital (EU27 34, Finland 39) versus use (9 and 17). It is no longer the headline message. The live lead is Wedgwood’s final wording: “Most companies have not yet put AI to work. Company adoption scores 9 out of 100 in the EU27 and 17 in Finland.” (9 and 17 are the rounded headline display values.)*
*Build note: cost_to_serve remains experimental; the third bar stays off.*

---

## 3. How to read the score (anchor `#scale`)

**H2:** How to read the score

**{{headline.display}}/100 ({{RANGE_LEVEL}} range {{headline.p2_5}}–{{headline.p97_5}}).** The range shows how sensitive the score is to the digital-versus-physical channel-weight choice (the digital share is drawn from 25–75 %). Almost all of its width comes from that choice, not from the data.

100 is not “good” and 0 is not “bad”. The index measures how widely AI is used, not whether that is desirable. 100 means AI has become dependable everyday infrastructure, like electricity.

**Scale ruler:** left label "0 · Almost no real use" · marker "▲ {{headline.display}} · {{reference_period}}" · right label "100 · Like electricity"

Three small cards:

1. **Weakest-link score: {{headline.geometric_mean}}/100.** A stricter version of the score. With one headline pillar (company adoption) it equals the headline.
2. **Speed: {{headline.velocity_pp_yr}} points a year.** How fast the score is changing at its current pace.
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

- The Machine Learning Societies – Diffusion Index stands at {{headline.display}} out of 100 ({{RANGE_LEVEL}} range {{headline.p2_5}}–{{headline.p97_5}}). The headline is the deployment pillar (company adoption) alone. The two scores for the EU27 and Finland are published separately and are not averaged. The width of the range comes almost entirely from the digital-versus-physical channel weighting, not from the data.
- For the EU27, capital commitments score 34 (context, not in the headline), while company adoption, the headline, is 9 (range 6–13). For Finland, capital is 39 (context) and the headline is 17 (range 10–24). Reliable task completion is experimental and is not in the headline.
- 100 would mean AI works like electricity: dependable, everyday infrastructure. A high score is not a judgement that AI is good.

**Chart images:** [headline score](assets/adi/adi-headline-1200x675.png) · [the gap](assets/adi/adi-gap-1200x675.png) · [industries](assets/adi/adi-industries-1200x675.png)

**Contact:** Harri Juntunen on [x.com/hjuntunen](https://x.com/hjuntunen) or [linkedin.com/in/hjuntunen](https://www.linkedin.com/in/hjuntunen).

**Methodology:** [how the index is calculated](diffusion-method.html).

*Build note: image files do not exist yet. Reuse terms for images follow the licence decision in plan TP3 (open item); add one line once decided.*

---

## 6. Who makes this (anchor `#credit`)

**H3:** Who makes this

**{{PUBLISHER_LINE}}**

Machine Learning Societies – Diffusion Index 1.0.0-rc.3 · {{reference_period}} · Prepared with the help of AI tools.

---

## 7. Footer

Machine Learning Societies – Diffusion Index 1.0.0-rc.3 · {{PUBLISHER_LINE}} · Daily Briefs · Methodology · Forecasts · About · RSS

*Build note: the main page has no open-data / replication section (Harri, 22 Nov 2026). Data files stay in `index/`; the methodology page links them.*

---

## Placeholders

Key paths refer to `index/computed.*.json` (checked against `computed.v0.6.json`, schema 0.6.0). `pillars` is an array; `pillars.<id>` means the item whose `id` is `<id>`. v0.6 values are for reference only and must not be reused.

| Placeholder | JSON key | Meaning | v0.6 value |
|---|---|---|---|
| `{{headline.display}}` (was `headline.block_a_diffusion_core.score`) | yes | Headline, whole number (deployment pillar alone) | EU27 9, FI 17 (v0.6 was 42.7) |
| `{{headline.p2_5}}` / `{{headline.p97_5}}` (was p5/p95) | yes | Ends of the published range (2.5 and 97.5 percentiles; page rounds to whole numbers). This is a channel-weight sensitivity band, not a measurement-error interval. | EU27 6–13 (5.6–13.2), FI 10–24 (10.4–24.4) |
| `{{headline.geometric_mean}}` | yes | "Weakest-link score" (equals the headline when one pillar is eligible) | EU27 9.3, FI 17.3 |
| `{{headline.velocity_pp_yr}}` | yes | Annual speed, points per year (omit the card if not published) | — |
| `{{pillars.capital_intensity.score}}` | yes | Capital commitments (P3), Block B context, outside the headline | EU27 34, FI 39 (v0.6 was 58.6) |
| `{{pillars.deployment.score}}` | yes | Company adoption (P1), the headline | EU27 9.3, FI 17.3 (v0.6 was 28.4) |
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
