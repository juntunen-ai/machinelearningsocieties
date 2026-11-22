# AI Diffusion Index — Methodology v1.0

Machine Learning Societies · method version 1.0 (covers index releases 1.0.x) · frozen candidate, 22 November 2026 · owner: Harri Juntunen · method freeze (work package TP1): Massi

Machine-readable specification: `index/method.v1.0.json`. If this page and the JSON ever disagree, the JSON is authoritative and the disagreement is a bug to be fixed in a PATCH release.
Companion files: `index/series.csv` (logged observations), `index/registry.v1.0.json` (sources, sectors; to be created from `registry.v0.6.json` in TP2), `index/brief_signals.csv` (curated brief log, not scored).
Supersedes: Methodology v0.6 (`index/method.v0.6.md`, 22 October 2026) and the scoring constants in `scripts/compute_index.py` v0.6.

Status of this document: every rule below is frozen for 1.0.0 once the release is tagged. Until the tag, the team may still reopen a rule, but only by editing both this page and the JSON in the same commit.

---

## 0. What changed from v0.6, and why

An internal review on 22 November 2026 found that the v0.6 numbers did not come from data. All ten pillar scores, all pillar velocities and all 100 sector × pillar cells were typed into `scripts/compute_index.py` (lines 79–403) as constants. The 56 logged observations were checked and counted but never passed through the published goalposts. Adding observation OBS-057 on 13 November 2026 changed nothing in the output. Version 1.0 fixes that and freezes every choice that changes a number.

| Topic | v0.6 | v1.0 |
|---|---|---|
| Source of scores | Hard-coded constants | Computed from `series.csv` through fixed goalposts; a test proves that changing an input changes the output |
| Target | Mixed EU27, US, global and national figures | Two populations, EU27 and Finland, scored separately; other geographies are context only |
| Deployment ceiling | Registry 100 %, page text "100 = 80 %" | 100 % (section 4.2) |
| Physical indicator | IFR robot density (not AI-specific, restricted licence) | Eurostat share of enterprises using autonomous robots, vehicles or drones (`E_AI_TAR`); IFR is a sensitivity only |
| Capital intensity | One company's S-1 commitments, global | Eurostat gross fixed capital formation in ICT equipment and intellectual property, % of GDP (proxy, official); filings are context |
| cost_to_serve | Graded A-Q without a price index | Grade C, experimental, outside the headline until the Task Price Index exists |
| Block A weights | Implicit 1/3 | Nominal 1/3 written down; renormalised over eligible pillars |
| Headline | Arithmetic; "bottleneck score" was the median of randomly weighted geometric draws | Arithmetic headline; geometric mean only as a labelled sensitivity with floor 1.0 |
| Monte Carlo | 1,000 draws, Dirichlet(1,1,1) weights, hand-set noise, 70/30 arithmetic/geometric mix, 90 % band | 20,000 draws, seed 20261028, ±50 % weights, noise from source standard errors, 95 % interval, three-way variance decomposition |
| Velocity | Hard-coded; Block A 8.9 = mean of three typed numbers in mixed units | Pace in index points per year from at least 3 comparable points, with its own 95 % interval |
| Breaks | BTOS factor 0.563 from two different weeks | Segments by default; bridging only from a published overlap period; BTOS factor rejected |
| Grid | 100 hand-set cells, fixed multipliers for reach, depth and embeddedness | Only cells with sector-specific evidence are scored; others say "not measured" |
| Grades | Set by hand (agriculture A) | Derived from the data (weakest link); agriculture capped at C |
| Momentum percentile | Hard-coded, reference distribution undocumented | Abolished |
| Versioning | "0.6-proposed" in the registry, "0.6.0" in the output | Semantic versioning with a CHANGELOG and frozen data vintages |

---

## 1. Construct and measurement model

**Construct.** AI diffusion is the extent to which learning systems are embedded in productive and social activity, measured as use, not capability (Edgerton's "technology in use").

**Formative, not reflective.** The pillars are not interchangeable symptoms of one latent trait. A country can have high deployment and weak human capital. The index is therefore a formative composite: there is no factor analysis and no Cronbach's alpha as a validity argument. Validity is argued from content (is every relevant facet covered?) and from convergent checks against independent sources (OECD/JRC 2008, steps 1, 7 and 8).

**Three layers per sector.**

| Layer | Question | Digital example | Physical example |
|---|---|---|---|
| Reach (extensive margin) | What share of units use it? | % of enterprises using at least one AI technology; % of individuals using generative AI | % of enterprises using autonomous robots, self-driving vehicles or drones |
| Depth (intensive margin) | How much of the work runs through it? | % of enterprises using three or more AI technologies | Share of robots that are learning-based (not measured in 1.0) |
| Embeddedness (workflow) | Does it run without a human for the routine case? | Named production workflows (curated log) | Operational fleets, driverless miles, devices in clinical use |

Reach is measurable now from official statistics. Depth is partly measurable. Embeddedness is not observable from open data at scale; it stays a curated log (`brief_signals.csv`), grade C, and is "not measured" in every 1.0 score.

**Two channels.** The **Digital AI Index (DAI)** covers software and cloud AI used by enterprises, public bodies and individuals. The **Physical AI Index (PAI)** covers embodied systems. A pillar that has both channels combines them with equal weight (digital 0.5, physical 0.5), as in v0.6. DAI and PAI are always published beside the combined score.

**Target populations.** Every score belongs to one population and one reference period:

- **EU27** (Eurostat code `EU27_2020`)
- **Finland** (`FI`)

EU27 and Finland are computed and published separately and never averaged together. Observations for other geographies (United States, global, other member states) may be shown as context but never enter a population score. The reference period of an edition is the calendar quarter ending on the data cut-off (section 11). For each indicator the latest period that ended on or before the cut-off is used; a value whose period ended more than 36 months before the cut-off is "stale" and excluded.

---

## 2. Architecture: three blocks, one headline

| Block | Pillars | In headline? |
|---|---|---|
| **A. Diffusion proper** | deployment (P1), cost_to_serve (P2), capital_intensity (P3) | **Yes** (eligible pillars only, section 6) |
| **B. Conditions** | energy_capacity (P8), governance_burden (P5), human_capital (P6), market_openness (P10) | Dashboard, never blended |
| **C. Consequences and distribution** | labour_reorganisation (P4), ownership_distribution (P9), ecological_balance (P7) | Dashboard, never blended |

The headline is Block A only. Blocks B and C are published beside it as pillar scores with their observation count, grade and coverage; 1.0 publishes no Block B or Block C composite. The direction of every pillar is fixed in the specification: +1 means more is more diffusion, −1 means less is more diffusion, and 0 means diagnostic only (scored but never aggregated).

### 2.1 Pace layers: why the blocks move at different speeds

Stewart Brand's pace-layering essay (*Journal of Design and Science*, 2018, from *The Clock of the Long Now*, 1999) gives the theoretical reason for the A/B/C split: a system stays resilient when layers move at different speeds, the fast layers learning and the slow layers remembering. "Fast learns, slow remembers." "Fast proposes, slow disposes." "Fast gets all our attention, slow has all the power." His six layers, fast to slow, are fashion/art, commerce, infrastructure, governance, culture and nature.

The essay is conceptual: it has no data and no method, and it says nothing about AI. The mapping below is **our proposal, not Brand's finding**.

| Pace layer | Index pillars | Block | Typical speed of change |
|---|---|---|---|
| Fashion / attention | not measured on purpose (the index refuses to score hype) | — | days to months |
| Commerce | deployment, cost_to_serve, capital_intensity | A (headline) | months to years |
| Infrastructure | energy_capacity | B | years to decades |
| Governance | governance_burden, market_openness, ownership_distribution | B / C | years to decades |
| Culture | human_capital; labour_reorganisation | B / C | decades |
| Nature | ecological_balance | C | decades and longer |

Consequences for the method:

1. **The headline measures the fastest layer we score.** A high Block A number says commerce has absorbed the technology; it does not say the slower layers have.
2. **Slow layers constrain fast ones.** The pace-mismatch ("pace shear") diagnostic compares Block A pace with slow-layer pace. In 1.0 it is **suspended** until at least one slow-layer pillar has a data-based pace (section 10); v0.6's ratio of 1.95 was built from typed-in velocities.
3. **Guard against "fast gets all our attention".** Each edition reports the pace-layer mix of the briefs it logged and flags a quarter with no slow-layer observation. Briefs never change the index between editions.

*Link to the productivity J-curve.* Brynjolfsson, Rock and Syverson (NBER w25148) argue that complementary intangible investment (process redesign, training, new business models) lags the technology and is mostly unrecorded. In pace-layer terms, the organisation and culture layers catch up with what commerce adopted quickly. This is an interpretation, not a claim made by either source.

---

## 3. Scoring chain

Every published number is produced by the same chain:

> observation (`series.csv`) → indicator value for a population and period → goalpost normalisation → indicator score 0–100 → layer → channel → pillar → Block A headline

### 3.1 Normalisation

For an indicator with raw value *x*, floor *f* and ceiling *c*:

- linear: *s* = 100 × (*x* − *f*) / (*c* − *f*)
- log: *s* = 100 × (ln *x* − ln *f*) / (ln *c* − ln *f*)

If the pillar's direction is −1, the score is 100 − *s*. After normalisation *s* is **clipped to [0, 100]**. Every clipped value is flagged `clipped = true` and its raw value is kept in the output. If a headline-pillar indicator clips in two consecutive editions, its goalposts are reviewed at the next MINOR version, never silently. On a log scale a raw value of zero or below is invalid input and the build fails (no silent epsilon).

### 3.2 Within a pillar

- **Layer score** = arithmetic mean of the measured indicators in that layer.
- **Channel score** = arithmetic mean of the measured layers in that channel.
- **Pillar score** = equal-weighted mean of the measured channels (digital 0.5, physical 0.5). If only one channel is measured, the pillar score is that channel and carries `channel_coverage = digital_only` or `physical_only`.
- Unmeasured indicators, layers and channels are omitted and listed. They are never imputed and never scored as zero.

### 3.3 Rounding

All arithmetic runs in double precision with no intermediate rounding. Scores, interval bounds and paces are rounded once, at output, to one decimal with ROUND_HALF_UP (Python `decimal`). The main page rounds the same unrounded value to a whole number with ROUND_HALF_UP. Weights are published to four decimals.

---

## 4. Goalposts (frozen)

### 4.1 Per pillar and indicator

| Pillar | Indicator (series) | Channel / layer | Scale | Floor | Ceiling | Dir. | Goalpost source and date | Role in 1.0 |
|---|---|---|---|---|---|---|---|---|
| P1 deployment | D1 % enterprises (10+) using ≥1 AI technology — Eurostat `isoc_eb_ai` `E_AI_TANY`, GE10, C10-S951_X_K | digital / reach | linear | 0 | 100 | +1 | Natural bounds of a share; TP1 decision 2026-11-22 | scored |
| P1 deployment | D2 % individuals 16–74 using generative AI tools (last 3 months) — Eurostat `isoc_ai_iaiu` `I_IUAI` | digital / reach | linear | 0 | 100 | +1 | Natural bounds; 2026-11-22 | scored |
| P1 deployment | D3 % enterprises using ≥3 AI technologies — `isoc_eb_ai` `E_AI_TGE3` | digital / depth | linear | 0 | 100 | +1 | Natural bounds; 2026-11-22 | scored |
| P1 deployment | D4 % enterprises using autonomous robots, self-driving vehicles or drones — `isoc_eb_ai` `E_AI_TAR` | physical / reach | linear | 0 | 100 | +1 | Natural bounds; 2026-11-22 | scored (AI-specific) |
| P1 deployment | D5 industrial robots per 10,000 manufacturing employees — IFR World Robotics | physical / reach | log | 10 | 1500 | +1 | registry v0.6, 2026-10-28 | sensitivity only (proxy, restricted licence) |
| P2 cost_to_serve | C1 AI Task Price Index, cost per accepted deliverable relative to human cost (2026 = 100) | digital / depth | log | 10 | 200 | −1 | registry v0.6 and v0.6 score guide ("100 = one tenth of today's cost"), 2026-10-28. TPI 10 → 100, TPI 100 → 23.1, TPI 200 → 0 | experimental: index does not exist yet |
| P3 capital_intensity | K1 GFCF in ICT equipment (N1132G) + intellectual property products (N117G), % of GDP — Eurostat `nama_10_an6` | digital / reach | linear | 0 | 15 | +1 | Ceiling ≈ 1.7 × highest member state in 2024 (DK 9.0 %, SE 8.6 %); EU27 2025 5.1 %, FI 5.9 %; retrieved 2026-11-22 | scored (proxy, official) |
| P3 capital_intensity | K2 AI compute commitments in filings, USD bn (global) — SEC EDGAR | digital / reach | log | 1 | 500 | +1 | registry v0.6, 2026-10-28 | context only (no EU27/FI population) |
| P4 labour_reorganisation | L1 % firms that reorganised tasks or workflows because of AI | — | linear | 0 | 100 | 0 | registry v0.6, 2026-10-28 | dashboard; source [K] |
| P5 governance_burden | G1 count of binding AI obligations / harmonised standards in force (named authority + date + sanction/standard) — EUR-Lex | — | linear | 0 | 50 | 0 | registry v0.6, 2026-10-28 | dashboard |
| P6 human_capital | H1 % ICT specialists in total employment — Eurostat `isoc_sks_itspt` [K] | — | linear | 0 | 25 | +1 | registry v0.6, 2026-10-28 | dashboard; source to verify |
| P7 ecological_balance | E1 data-centre electricity demand, TWh — IEA | — | log | 10 | 2000 | 0 | registry v0.6, 2026-10-28 | dashboard, two-way, no net figure |
| P8 energy_capacity | N1 requested MW ÷ connected MW (queue ratio) — Fingrid / ENTSO-E [K] | — | log | 0.5 | 10 | −1 | registry v0.6; scale frozen as log (a ratio) and direction −1, 2026-11-22 | dashboard; source to verify |
| P9 ownership_distribution | O1 % broad / public / employee equity share — ECB DWA, Fed DFA [K] | — | linear | 0 | 100 | 0 | registry v0.6, 2026-10-28 | dashboard; source [K] |
| P10 market_openness | M1 % open-weights / non-concentrated share — Epoch AI, OpenRouter | — | linear | 0 | 100 | +1 | registry v0.6, 2026-10-28 | dashboard |

Indicators marked [K] cannot enter `series.csv` until someone has opened the source and recorded the series id. K1 (`nama_10_an6`) must be added to the registry as a verified source and logged before release candidate 1.

### 4.2 Deployment ceiling: 100, not 80

**Decision: 100 %.**

1. A fixed goalpost should be the natural bound of its unit. 100 % needs no external justification; an 80 % "saturation level" does, and we have none that would survive review.
2. With 80 the scores would clip soon. The share of large EU enterprises using AI was 55.0 % in 2025, rising 13.9 points a year, and the share of large Finnish firms was 68 % (Statistics Finland). Sector cells such as information and communication would clip first.
3. It matches the other share-based pillars (labour, ownership and market openness all use 0–100).
4. The score reads directly as "percent adopting", which the main page can explain in one sentence.

The cost is that scores look lower: EU enterprise reach in 2025 scores 20.0 instead of 24.9. An 80 % saturation reading may be shown as a labelled sensitivity, never as the headline. The v0.6 page text "100 = 80 % of organizations" must be removed.

---

## 5. Evidence rules and "not measured"

**Which observations count.** Only rows from registry sources marked verified ([V]) that pass the `series.csv` schema. [K] sources never count.

**Pillar eligibility for the headline.** A pillar enters the headline for a population only if all of these hold:

- at least **5 verified observations**,
- from at least **2 distinct verified sources**,
- at least **1 of them official statistics** (registry trust tier 1),
- a derived grade of **A or B**, and
- at least one scored indicator value for that population and reference period.

Observations and sources are counted per pillar across all geographies (plan section 2.3); the score itself uses only the target population's values.

**Experimental pillars.** A pillar with at least one scored indicator value that fails the eligibility test is published as "experimental", with n and grade, and excluded from the headline.

**Headline completeness.** The headline for a population needs at least **2 eligible Block A pillars**. Otherwise it is null with status "incomplete", and the pillar scores are still published.

**Grid cells.** The grid is 10 sectors (NACE sections, as in the registry) × 10 pillars, per population. A cell is scored only from at least **1 verified observation whose sector matches the cell's NACE section(s)** and whose geography matches the population, within the 36-month staleness limit. Observations for all sectors ("ALL") never fill a sector cell. Otherwise the cell's score and grade are null and its status is "not measured". The v0.6 fixed multipliers (reach ×1.14, depth ×0.88, embeddedness ×0.98; sector DAI ×1.08/0.92, PAI ×1.15/0.45) are abolished.

**Display.** Unmeasured values are shown as the words "not measured": never 0, never blank, never a colour that implies a score. Every published number carries n (observations) and coverage (measured indicators ÷ defined indicators).

For scale: in v0.6 only 23 of the 100 cells had any sector-specific observation, and deployment held 37 of 57 observations. Most grid cells and most Block B and C pillars will read "not measured" or "experimental" in 1.0. That is intended.

---

## 6. Grades

Provenance grades: **A** official or administrative register or filing; **B** academic, intergovernmental or documented commercial series with a stable definition; **C** proxy, voluntary or single-source. A frequency tag (M monthly, Q quarterly, Y annual) is kept from v0.6.

- **Indicator grade** = the provenance grade of its source series. Trust tier 4 (vendor telemetry, company disclosure) is at most B and never the only A/B evidence. Tier 5 is never a source.
- **Derived grade** of a pillar or cell = the **lowest** grade among the indicators that enter its score (weakest link).
- **Caps:**
  - Agriculture: maximum **C**, until a sector-specific A/B series is logged (precision-agriculture adoption has no open official series).
  - cost_to_serve: maximum **C** until the Task Price Index exists.
  - Proxy indicators in the physical channel: maximum C for the AI dimension. `E_AI_TAR` is AI-specific and not capped.
- **Sector gap** is computed only between scored cells of grade A or B for the same population and pillar set. Capped sectors are excluded, so agriculture (one observation in v0.6) can no longer be the "laggard" end of the gap.

---

## 7. Block A weights and aggregation

**Nominal weights:** deployment 1/3, cost_to_serve 1/3, capital_intensity 1/3.

**Missing or grade-C pillar:** weights are renormalised over the eligible pillars only, *w*ᵢ = nominalᵢ / Σ nominalⱼ (eligible *j*). With cost_to_serve experimental, the effective weights are **deployment 0.5000, capital_intensity 0.5000**.

**Headline (arithmetic):** *H* = Σ *w*ᵢ *s*ᵢ.

**Sensitivity check, geometric mean (weakest link):** *G* = exp(Σ *w*ᵢ ln max(*s*ᵢ, 1.0)). The floor of 1.0 keeps a near-zero pillar from sending *G* to zero. *G* is always labelled "sensitivity check: geometric mean (weakest link)", is never called the headline, and is never mixed into the headline interval. It shows how much a weak pillar would pull the score down if pillars could not compensate for each other. For example, with v0.6's typed-in pillars, a deployment score of 10 instead of 28.4 would have moved *H* to 36.6 and *G* to 28.9.

**DAI and PAI** apply the same aggregation to the digital and physical channel scores of each pillar; pillars without that channel are omitted and the weights renormalised. PAI carries the proxy flag whenever a proxy indicator contributes.

---

## 8. Uncertainty: Monte Carlo specification

| Parameter | Frozen value |
|---|---|
| Seed | 20261028 |
| Draws | 20,000 per population |
| Generator | `numpy.random.Generator(numpy.random.PCG64(20261028))` |
| Draw order | (1) noise matrix *Z* (draws × indicators) from `standard_normal`, indicators sorted by id; (2) weight factors *U* (draws × eligible Block A pillars) from `uniform(0.5, 1.5)`, pillars in Block A order; populations in the order EU27, FI |
| Weights | independent multiplicative factors uniform on [0.5, 1.5] (±50 %), then renormalised |
| Data noise | *x*ᵈʳᵃʷ = *x* (1 + σʳᵉˡ *z*), one *z* per indicator value; the score is recomputed through goalpost and clipping |
| Interval | 95 %: 2.5 %, 50 % and 97.5 % quantiles of *H* over joint data and weight draws |
| Aggregation | separate component, *H* − *G*; not mixed into the interval |

**Why ±50 % weights and not ±20 %.** Equal weights have no empirical basis in a formative index, so the plausible range should be wide. ±20 % would understate how arbitrary the weights are and would make the interval mostly data noise. ±50 % is also what method v0.6 promised. The v0.6 code instead drew weights from Dirichlet(1,1,1), which allows weights near 0 and 1. In the review's replication that made the interval about 2.5 times wider: 32.0–53.4 versus 38.0–46.5 under ±50 %. Weight uncertainty is reported as its own variance component, so readers can see how much of the interval comes from weight choice rather than data. Dirichlet sampling is abolished.

**Why 20,000 draws.** At 1,000 draws the v0.6 interval bounds moved by up to 0.6 points between seeds. At 20,000 the Monte Carlo error of the 2.5 % and 97.5 % quantiles is about 0.2 points or less for intervals of that width.

**Noise from source standard errors.** σ for each indicator value is chosen in this order:

1. The standard error or confidence interval the source publishes for that value (half-width of a 95 % CI ÷ 1.96).
2. For survey proportions with a known sample size *n*: σ = √(*p*(1 − *p*) / (*n* / deff)), with design effect deff = 2.0. The Eurostat ICT enterprise survey 2025 sampled 157,000 enterprises in the EU (ESMS `isoc_e`, section 3.6).
3. **Fallback** by derived grade, relative: A 0.045, B 0.075, C 0.15. A and B continue the v0.6 values; C is new.

Each observation row records `sigma` and `sigma_basis` (published, binomial, fallback_A, fallback_B or fallback_C). Eurostat states that standard errors are reported in national quality reports for a selection of indicators (ESMS section 13); where those can be located they replace rule 2.

**Point and median.** The published point is *H* at the effective nominal weights with unperturbed data; the Monte Carlo median is published beside it. If they differ by more than 1.0 point the compiler warns. (In v0.6 they differed: 42.7 against 41.7.)

**Variance decomposition** (published for each population's headline):

| Output | Definition |
|---|---|
| V_total | variance of *H*, data noise and weights both random |
| V_data | variance of *H*, data noise only (weights fixed) |
| V_weights | variance of *H*, weights only (data fixed) |
| V_aggregation | variance of a 50/50 mix of *H* and *G* at fixed data and weights = ((*H* − *G*)/2)² |
| share_data, share_weights, share_aggregation | each V ÷ (V_data + V_weights + V_aggregation), whole per cent |
| interaction | V_total − V_data − V_weights |

The data component is also run for DAI, PAI and every pillar score.

For reference, the v0.6 replication split its 90 % band 95 % weights and 5 % data noise. Under v1.0 the weight share falls, and the aggregation share becomes visible whenever pillars diverge.

---

## 9. Series breaks

**Default: segments.** A break (definition, question wording, population or classification change) starts a new segment. Levels may use the latest segment; paces and any chaining never cross a segment boundary.

**Bridging** is allowed only if the source publishes the same period under both definitions (an overlap period). Bridge factor = old ÷ new for that overlap period, recorded with source URL, overlap period, date and its standard error. A ratio of two different periods is never a bridge factor.

**Schema.** Rows carry `break_flag` (true on the first row of a new segment), `segment_id` and, only when bridged, `bridge_factor`, `bridge_source` and `bridge_period`. Eurostat "b" flags are imported per value.

**Decisions for 1.0:**

- **US Census BTOS (V1 → V2, 17 November 2025): two segments, no bridge.** The v0.6 factor 0.563 equals 9.8 ÷ 17.4, i.e. OBS-024 (week 44, old question) divided by OBS-025 (week 48, new question). It divides different weeks under different questions, so four weeks of real growth are counted as part of the break. It is rejected. BTOS is US data, outside the EU27/FI target, so it is context only. OBS-026 must lose its bridge factor (it carries 0.563 with `break_flag = false`).
- **Eurostat `isoc_eb_ai` "any AI", "≥2" and "≥3 technologies": segment S1 = 2021, 2023, 2024; segment S2 from 2025** (see 9.1).
- **Eurostat `E_AI_TAR`: one segment 2021–2025 at EU27 level.** Country "b" flags start a new segment for that country.

### 9.1 Eurostat `isoc_eb_ai`: definition check, 2021–2025

Checked on 22 November 2026 against:

- ESMS metadata `isoc_e` (metadata last updated 11 December 2025): https://ec.europa.eu/eurostat/cache/metadata/en/isoc_e_esms.htm
- Eurostat dissemination API, dataset `isoc_eb_ai` (data updated 15 June 2026; periods 2021, 2023, 2024, 2025): https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai
- Statistics Explained, "Use of artificial intelligence in enterprises" (data extracted December 2025; planned update 15 December 2026): https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises

Findings:

1. **There was no AI module in survey year 2022.** The series has 2021, 2023, 2024 and 2025 only.
2. **EU27 values** (`E_AI_TANY`, 10+ persons): 2021 7.65 %, 2023 8.06 %, 2024 13.48 %, 2025 19.95 %. **No "b" flag on any EU27 value.**
3. **2025 adds a technology.** The `E_AI_TANY` definition now reads "at least one of AI_TTM, AI_TSR, AI_TNLG, AI_TIR, AI_TML, AI_TPA, AI_TAR, E_AI_TPVSG". `E_AI_TPVSG` (AI generating pictures, videos, sound/audio) exists only for 2025 (EU27 9.55 %). The 2025 "any AI" share therefore covers eight technologies against seven in 2021–2024. Eurostat neither flags this as a break nor publishes a 2025 total on the seven-technology basis. The effect is bounded (between 0 and 9.55 points, the share of firms using that technology) but not identified, because firms using image, video or audio generation mostly also use other AI technologies.
4. Purpose indicators changed between 2021 and 2023 (`E_AI_PBA`, `E_AI_PHR` and `E_AI_PME` exist only for 2021). Indicators on how the AI was obtained (`E_AI_ADOWN` and others) exist only for 2021 and 2024. Neither group is used for scoring.
5. **Country break flags on `E_AI_TANY`:** France 2023 "b", Sweden 2023 "b", Netherlands 2025 "b". Finland has no flag (2021 15.79 %, 2023 15.10 %, 2024 24.37 %, 2025 37.82 %).
6. `E_AI_TANY` + `E_AI_TX` does not sum to 100 (EU27: 94.78 in 2021, 98.18 in 2023, 98.19 in 2024, 99.04 in 2025). This is consistent with item non-response; it is not a definition break, but it is noted.
7. ESMS section 15.2 says comparability over time is restricted where definitions change to follow ICT, and section 12.3 says changed questions get new indicator codes and break series.
8. The v0.6 registry notes a "German definition break 2025". The API carries no "b" flag for Germany on `E_AI_TANY` in 2023–2025. **Not confirmed.**

**Outcome.** 2025 is treated as a soft definition break for `E_AI_TANY`, `E_AI_TGE2` and `E_AI_TGE3`: segment S1 (2021, 2023, 2024) and S2 (from 2025). Levels use 2025 (S2). Paces use S1 until S2 has three points (expected with the 2027 data), unless Eurostat publishes a 2025 value on the seven-technology basis, which would allow an overlap bridge. 2023 against 2021 is comparable at EU27 level apart from flagged countries. `E_AI_TAR` is unaffected.

---

## 10. Pace (annual change)

- **Unit:** index points per year on the 0–100 score scale, never percentage points of the raw unit. (v0.6's deployment velocity of 6.5 was the change in the EU adoption share, 13.5 % → 20.0 %, not a change in score.)
- **Minimum:** 3 comparable points: same population, same indicator set, same segment for every indicator, same goalposts.
- **Estimator:** ordinary least squares slope of score on time in years (period midpoints), unweighted.
- **Interval:** 95 %. A Monte Carlo over data noise (same generator stream, after the level draws) recomputes the slope per draw. With 4 or more points the OLS t-interval (df = n − 2) is also computed, and the wider of the two is published.
- **Wording:** a pace is called rising or falling only if its 95 % interval excludes zero; otherwise it is "not distinguishable from zero".
- **Levels:** a pillar pace is published only when the whole indicator set of the pillar meets the minimum. Otherwise indicator-level paces are published and labelled as such. A headline pace is published only when every eligible Block A pillar has a pillar pace over the same periods.
- **Momentum percentile:** abolished. **Pace shear:** suspended until a slow-layer pillar has a data-based pace.

Illustration (OLS only, Eurostat values retrieved 22 November 2026; not a published number):

| Series | Points | Slope (points/yr) | 95 % OLS interval |
|---|---|---|---|
| EU27 D1 any AI, segment S1 | 2021, 2023, 2024 | +1.70 | −14.70 to +18.09 |
| Finland D1, segment S1 | 2021, 2023, 2024 | +2.40 | −27.83 to +32.63 |
| EU27 D4 autonomous systems | 2021, 2023, 2024, 2025 | +0.11 | −0.13 to +0.35 |
| EU27 K1 capital, % of GDP | 2019–2025 | −0.52 | −1.26 to +0.22 |
| Finland K1 capital | 2019–2025 | +0.95 | +0.13 to +1.78 |

Under these rules the deployment pillar has no pillar pace in 1.0, because D2 (individuals) has only one year (2025). The adoption series accelerates (2024 → 2025: +6.5 points, but across the 2025 definition change), but three points within one segment cannot yet show that with confidence.

---

## 11. Data vintage

- **Cut-off** = the last day of the reference quarter (Europe/Helsinki). An observation counts if `date_logged` and the source's release date are both on or before the cut-off. Nothing logged after the cut-off changes a published edition.
- **Proposed cut-off for 1.0.0: 31 December 2026** (2026-Q4). It captures Eurostat's planned December 2026 `isoc_eb_ai` release; publication is proposed for January 2027.
- **Hashes:** SHA-256 of `index/series.csv`, `index/registry.v1.0.json`, `index/method.v1.0.json`, `index/brief_signals.csv` and `index/planetary_boundaries.json` are written into the computed JSON (`vintage.hashes`) and into the release's SHA256SUMS.
- **Raw snapshots:** the API responses used to log Eurostat values are stored as dated files in the release assets.
- **Cadence:** quarterly, on a fixed day. Daily briefs never change the index between editions.

---

## 12. Versioning and CHANGELOG

The index uses semantic versioning **MAJOR.MINOR.PATCH**. The method file carries MAJOR.MINOR (method v1.0 covers 1.0.x).

- **MAJOR:** change to the construct, block membership, headline aggregation formula, goalpost form (scale type) or target populations. Comparability with earlier editions breaks; back series are recomputed or marked non-comparable.
- **MINOR:** change to goalpost values, nominal weights, the indicator set, evidence thresholds, the Monte Carlo specification (seed, N, weight range, noise rule) or a break decision. The full back series is recomputed under the new method and published with the release.
- **PATCH:** a new data vintage under an unchanged method, a correction of logged data errors, or a documentation fix that changes no number.

`CHANGELOG.md` follows the Keep a Changelog format. Every release lists method changes, data vintage (cut-off), hashes and the effect on the headline (old value against new). There is one VERSION source and a git tag `vX.Y.Z` per release. Once 1.0.0 is tagged, nothing in `method.v1.0.json` changes without a version bump and a CHANGELOG entry.

---

## 13. Worked example (illustrative, not a published number)

Values from the Eurostat API, retrieved 22 November 2026, reference year 2025. Noise: binomial for EU27 enterprise-survey shares (n = 157,000, deff 2); fallback A (4.5 %) otherwise. Script: `/workspace/adi-review/work/worked_example.py` (outside the repo; Kernelio's compiler replaces it).

| | EU27 | Finland |
|---|---|---|
| D1 any AI (enterprises) | 19.95 | 37.82 |
| D2 generative AI (individuals) | 32.66 | 46.27 |
| D3 ≥3 AI technologies | 8.28 | 21.81 |
| D4 autonomous robots, vehicles or drones | 1.39 | 2.73 |
| Digital channel = mean(reach mean(D1, D2), depth D3) | 17.29 | 31.93 |
| Physical channel = D4 | 1.39 | 2.73 |
| **Deployment** = 0.5 digital + 0.5 physical | **9.34** | **17.33** |
| K1 capital (ICT equipment + IPP, % of GDP) | 5.1 → **34.00** | 5.9 → **39.33** |
| **Headline *H*** (0.5 / 0.5) | **21.67** | **28.33** |
| Geometric sensitivity *G* | 17.82 | 26.11 |
| Monte Carlo median; 95 % interval | 21.61; 16.71–26.98 | 28.29; 23.78–33.32 |
| Variance shares data / weights / aggregation | 5 % / 61 % / 34 % | 11 % / 72 % / 17 % |

What the example shows:

- Built from data, the headline falls far below v0.6's 42.7.
- Capital clearly exceeds use, so the "money has arrived, use has not" message survives.
- The equal digital/physical split inside deployment is the single choice that moves the number most: with digital only, deployment would be 17.3 for EU27 and the headline 25.6.
- These numbers change once K1 and the 2026 Eurostat data are logged; they must not be reused on any page.

---

## 14. Compiler contract (for TP2)

The compiler must:

1. read goalposts, weights, evidence thresholds and Monte Carlo parameters only from `index/method.v1.0.json` (no constants in code);
2. compute every score from `series.csv` through the chain in section 3, with no hard-coded scores;
3. fail the build if a [K] source is used, a log-scale value is ≤ 0, or a required field is missing;
4. emit n, coverage, grade, status (scored, experimental, not measured, stale or incomplete), clipped flags and `sigma_basis` for every published number;
5. pass a golden test: a rerun on the frozen vintage reproduces the computed JSON byte for byte (except `generated_at`);
6. pass a sensitivity test: changing one input value changes the dependent score.

Outputs: headline per population (point, median, 2.5 %, 97.5 %); geometric sensitivity; variance decomposition; DAI and PAI; pillar scores and statuses; grid cells; paces with intervals; vintage block with hashes; `method_version` and `index_version`.

---

## 15. Sources by pillar (carried over from v0.6, status updated)

Source status: **[V]** checked live in primary form; **[K]** known source, URL or licence still to be confirmed before logging. Licence status is audited separately (TP3).

**P1 deployment (digital).** Eurostat `isoc_eb_ai`, `isoc_eb_ain2` [V], A-Y, annual, next release planned December 2026. Statistics Finland StatFin `13vg` [V], A-Y. CSO Ireland `BIIESA20` [V], A-Y (context). US Census BTOS [V], A-M, series break 17 November 2025 (context). Eurostat `isoc_ai_iaiu` [V], A-Y. Microsoft AI Economy Institute AI User Share [V], tier 4 vendor telemetry, B-Q (context; global). TED open data [V] and Hilma [K] for public-sector deployment (A-M after classification work; not scored in 1.0).

**P1 deployment (physical).** Eurostat `isoc_eb_ai` `E_AI_TAR` [V], A-Y (scored). IFR World Robotics [V], B-Y, restricted licence, not AI-specific (sensitivity only). CPUC, NHTSA SGO, Waymo hub [K] (not scored). FDA AI-Enabled Medical Device List [V], A-Q, list not exhaustive (context; US).

**P2 cost_to_serve.** No open price series exists. The AI Task Price Index is to be built on a fixed basket of standardised workflow tasks (GDPval gold subset `openai/gdpval`, 220 public tasks across 44 occupations; arXiv 2510.04374 [V]), priced quarterly from public list prices and measured tokens per task with a published harness, divided by the human cost of the same task (Eurostat `lc_lci` or BLS [K]). Unit: (inference cost + human review and rework at wage cost + integration overhead) ÷ share of outputs rated at least "as good as" the expert baseline, indexed to 100 in the 2026 baseline. Grade C until the harness is published and replicated. Vendor "price fell X %" claims are not used.

**P3 capital_intensity.** Eurostat `nama_10_an6` [V as of 2026-11-22 API check; add to registry] for K1. SEC EDGAR filings [V] (context: Anthropic S-1, H1 2026 compute 8.95 bn USD of 16.29 bn revenue; 265.6 bn USD commitments). Epoch AI data [V], CC BY 4.0 (context). *Lower-bound rule (productivity J-curve):* national accounts miss most complementary intangible investment (multipliers of about 2 for R&D and about 10 for software and hardware in Brynjolfsson, Rock and Syverson), so K1 is read as a lower bound on total adoption investment and the multiplier is a sensitivity case.

**P8 energy_capacity.** IEA Energy and AI Observatory [V]; LBNL "Queued Up", ERCOT/PJM large-load queues [V for Texas]; Fingrid open data [K]; ENTSO-E Transparency Platform [K]. Ratio rule: requested MW ÷ connected MW.

**P5 governance_burden.** EUR-Lex / CELLAR for Regulation (EU) 2024/1689 and implementing acts [V]; FSB Sound Practices [V]; OECD.AI policy database and AI Incidents Monitor [V]; AI Incident Database [K]. Counting rule: named authority + date + sanction or standard.

**P6 human_capital.** Eurostat ICT specialists and Digital Decade series [K]; Statistics Finland / Vipunen [K]; OECD.AI skills data [V]; Stanford AI Index for context only (tier 5: locate the primary).

**P10 market_openness.** Hugging Face Hub API [K]; Epoch AI Models [V]; Epoch finding that five hyperscalers hold over two-thirds of global AI compute [V]; Anthropic S-1 marketplace share [V]; OpenRouter rankings [V, tier 4]; OECD PMR [K]; TED procurement neutrality [V].

**P4 labour_reorganisation.** Eurostat LFS and job vacancies [K]; Census BTOS AI supplement [V, US context]; Indeed Hiring Lab [K]; Cedefop Skills-OVATE [K]; Anthropic Economic Index [V, tier 4].

**P9 ownership_distribution.** Fed DFA and ECB DWA [K]; SEC EDGAR 13F, proxy and S-1 filings [V]; pledge events logged as announced, executed or lapsed.

**P7 ecological_balance.** Planetary boundaries framework (Rockström et al. 2009, Steffen et al. 2015, Richardson et al. 2023) [V] as the reference frame: (a) a boundary status panel, never scored; (b) direct footprint as a share of the global flow behind each control variable ("not measured" where no AI-specific series exists, never zero); (c) enabled reduction with a mandatory rebound multiplier. No net figure until both components are A/B in the same sector.

---

## 16. Known limitations of 1.0

- K1 capital is a national-accounts proxy (ICT hardware, software, databases and R&D), not AI-specific.
- Embeddedness is not measured anywhere in the headline.
- The physical channel rests on one indicator (`E_AI_TAR`), which scores low and pulls deployment down by design.
- Most Block B and C pillars and most grid cells will be experimental or not measured.
- The 2025 Eurostat definition extension is bounded but not identified.
- Weights are a convention; their effect is shown, not removed.

---

## 17. References

- Brand, S. (2018). *Pace Layering: How Complex Systems Learn and Keep Learning.* Journal of Design and Science, DOI 10.21428/7f2e5f08.
- Brynjolfsson, E., Rock, D. and Syverson, C. (2018, revised 2020). *The Productivity J-Curve: How Intangibles Complement General Purpose Technologies.* NBER Working Paper 25148.
- Bonney, K. et al. (2024). *Tracking Firm Use of AI in Real Time: A Snapshot from the Business Trends and Outlook Survey.* U.S. Census Bureau CES-WP-24-16.
- Eurostat. *ICT usage in enterprises (isoc_e), Reference Metadata in Euro SDMX Metadata Structure (ESMS)*, last updated 11 December 2025. https://ec.europa.eu/eurostat/cache/metadata/en/isoc_e_esms.htm
- Eurostat. *Use of artificial intelligence in enterprises.* Statistics Explained, data extracted December 2025.
- Misra, A., Wang, J., McCullers, S., White, K. and Lavista Ferres, J. (2025). *Measuring AI Diffusion: A Population-Normalized Metric for Tracking Global AI Usage.* arXiv:2511.02781.
- OECD/JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide.*
- OpenAI (2025). *GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks.* arXiv:2510.04374.
- Richardson, K. et al. (2023). *Earth beyond six of nine planetary boundaries.* Science Advances.
