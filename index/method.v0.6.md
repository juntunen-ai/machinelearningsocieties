# Diffusion Index v0.6 — proposal for a scientifically defensible, digital + physical index

Machine Learning Societies · drafted 22 October 2026 · builds on v0.5 · owner: Harri Juntunen
Companion files: `registry.v0.6.json` (pillars, sectors, sources), `series.csv` (logged observations, v0.6 schema), `brief_signals.csv` (curated brief & embeddedness log).

---

## 0. What this document does

1. Keeps what is right in v0.5: workflow-level thinking (Edgerton: technology in use), ten pillars, sector × pillar grid, published grades, the gap, the market test, append-only logging.
2. Fixes four methodological problems that would otherwise make the headline number invalid (section 4).
3. Adds the **physical** channel (robots, autonomous vehicles, AI-enabled devices) next to the **digital** one.
4. Names open, credible data sources for every pillar, rated by trust tier, and says plainly where **no open source exists** and the index has to build its own measurement (section 8).

Source status marks used throughout: **[V]** = checked live in primary/verified form; **[K]** = known source, URL/licence still to be confirmed before it is logged. Nothing marked [K] should enter `series.csv` until someone has opened the source and recorded the series id.

---

## 1. Construct and measurement model

**Construct.** AI diffusion = the extent to which learning systems are embedded in productive and social activity, measured as use, not capability.

**Formative, not reflective.** The pillars are not interchangeable symptoms of one latent trait (a country can have high deployment and weak human capital). The index is therefore a *formative composite*: no factor analysis, no Cronbach alpha as a validity argument. Validity must be argued from content (is every relevant facet covered?) and from convergent checks against independent sources (section 5).

**Three layers per sector (replaces the single "deployment" notion):**

| Layer | Question | Digital example | Physical example |
|---|---|---|---|
| Reach (extensive margin) | What share of units use it? | % enterprises using ≥1 AI technology; % working-age population using generative AI | Robots per 10,000 manufacturing workers; share of firms with autonomous robots |
| Depth (intensive margin) | How much of the work runs through it? | Number of business functions per using firm; share of O*NET tasks with observed AI use | Share of installed robots that are learning-based / collaborative; driverless paid rides as share of local taxi trips |
| Embeddedness (workflow) | Does it run without a human for the routine case? | Named production workflows (v0.5 §4.1) | Operational stock, driverless miles, devices in clinical use |

Reach is measurable now from official statistics. Depth is partly measurable. Embeddedness (the v0.5 "workflow" unit) is **not observable from open data at scale**; it stays a curated log (procurement notices, filings, enterprise announcements) with grade C until a register appears.

**Two channels, reported separately, then combined.**
- **Digital AI Diffusion Index (DAI):** software and cloud AI used by enterprises, public bodies and individuals.
- **Physical AI Diffusion Index (PAI):** embodied systems — industrial and service robots, autonomous vehicles, AI-enabled medical devices, drones.
- **Combined headline:** equal-weighted by default, with the DAI/PAI split always shown. Value-share weighting is a documented sensitivity test, not the default.

Honest limit on PAI: IFR robot statistics count *industrial robots*, not *AI-driven* robots. They measure the embodied-automation platform on which learning systems are deployed. Until a learning-based share is observable, the physical channel carries an "AI-specificity: proxy" flag and is capped at grade C for the AI dimension.

---

## 2. Architecture: three blocks, one headline

v0.5 averages seven pillars into "diffusion", mixing things that diffuse with things that enable or follow diffusion (governance burden, ecological load). That blurs causes and consequences. Proposed:

| Block | Pillars | In headline? |
|---|---|---|
| **A. Diffusion proper** | deployment, cost_to_serve, capital_intensity (reach, depth, price, investment) | **Yes** |
| **B. Conditions** | energy_capacity, governance_burden, human_capital, market_openness | Dashboard, never blended |
| **C. Consequences & distribution** | labour_reorganisation, ownership_distribution, ecological_balance | Dashboard, never blended |

The v0.5 sub-indices (diffusion, constraint, distribution, market) are kept as views over the same cells. The headline is Block A only; B and C are published beside it with their own gaps. This keeps the v0.5 principle that ownership and ecology are "never blended silently into the headline", and extends it to all enabling and outcome pillars. Direction of every pillar is declared in the registry (`direction`: +1 more is more diffusion, −1 less is more diffusion, 0 = diagnostic only).

### 2.1 Pace layers: why the blocks move at different speeds

Stewart Brand's pace-layering essay (*Journal of Design and Science*, 2018, from *The Clock of the Long Now*, 1999) gives the theoretical reason for the A/B/C split. His claim: a system stays resilient when layers move at different speeds, with the fast layers learning and the slow layers remembering. "Fast learns, slow remembers." "Fast proposes, slow disposes." "Slow and big controls small and fast by constraint and constancy." "Fast gets all our attention, slow has all the power." His six layers, fast to slow, are fashion/art, commerce, infrastructure, governance, culture, nature.

The essay is conceptual: it has no data and no method, the layer boundaries are loosely defined, and it says nothing about AI directly. What follows is therefore **our proposed mapping, to be tested in the Delphi (§5), not a finding of Brand's.**

| Pace layer | Index pillars | Block | Typical speed of change |
|---|---|---|---|
| Fashion / attention | not measured on purpose (discourse and hype are the fast layer the index refuses to score) | — | days to months |
| Commerce | deployment, cost_to_serve, capital_intensity | A (headline) | months to years |
| Infrastructure | energy_capacity | B | years to decades |
| Governance | governance_burden, market_openness, ownership_distribution | B / C | years to decades |
| Culture | human_capital; labour_reorganisation (transmits from commerce into governance and culture) | B / C | decades |
| Nature | ecological_balance | C | decades and longer |

Three consequences for the method:

1. **The headline measures the fastest layer we score.** Block A is the commerce layer, which "learns" quickest. A high Block A number says commerce has absorbed the technology; it does not say the slower layers have. This is the theoretical reason the headline never absorbs Blocks B and C.
2. **Slow layers constrain fast ones, so test for lags and bottlenecks.** Add a **pace-mismatch diagnostic**: for each sector, compare the growth of Block A with the growth and level of the slow-layer pillars it depends on (grid connection ratio, governance obligations in force, skills pipeline). A fast layer growing against a stalled slow layer is a constraint signal. It is a descriptive ratio, never a causal claim. The existing `energy_capacity` queue ratio is the first worked case.
3. **Guard against "fast gets all our attention".** The daily brief naturally logs commerce-layer events (launches, deals, listings). To keep the log from skewing, each monthly edition reports the **layer mix of its logged observations** and flags a month with no slow-layer observation.

*Link to the J-curve (§3, pillar 3).* The Brynjolfsson, Rock and Syverson lag can be read in pace-layer terms: complementary intangibles (process redesign, training, new business models) are the organisation and culture layers catching up with a technology that commerce adopted quickly. This is an interpretation, not a claim made by either source.

---

## 3. Pillar-by-pillar series and sources

Grade format proposed in §4.4: provenance A/B/C plus frequency tag (M monthly, Q quarterly, Y annual).

### Block A — diffusion proper

**1. deployment (digital)**
| Series | Source | Status | Grade |
|---|---|---|---|
| Share of enterprises (10+ staff) using ≥1 AI technology, by size and NACE; by AI type and purpose | Eurostat `isoc_eb_ai`, `isoc_eb_ain2` | [V] 2025 data published Dec 2025; next update planned Dec 2026 | A-Y |
| Finland, national detail and NACE | Statistics Finland StatFin table `13vg` (PxWeb API) | [V] 38 % in 2025, up from 24 % | A-Y |
| Ireland | CSO PxStat `BIIESA20` (JSON-stat API) | [V] | A-Y |
| US firms using AI, biweekly, by sector, size, state | Census BTOS | [V] wording broadened 17 Nov 2025 — **series break** | A-M (break flagged) |
| Individuals using generative AI (16–74) | Eurostat `isoc_ai_iaiu` | [V] | A-Y |
| Working-age population using AI tools, 147 economies | Microsoft AI Economy Institute, AI User Share | [V] vendor telemetry, documented method (arXiv 2511.02781) | B-Q |
| Public-sector deployment: tenders and awards naming AI/ML | TED open data / Search API, CPV 72*, 48*, full-text keywords; Finland Hilma | TED [V]; Hilma [K] | A-M after classification work |

**1b. deployment (physical)**
| Series | Source | Status | Grade |
|---|---|---|---|
| Industrial robot installations and operational stock by country and customer industry; robot density | IFR World Robotics (public executive summary; full tables paid) | [V] 542,076 installed in 2024; stock 4,663,698 | B-Y (access cost) |
| Share of enterprises using autonomous robots / self-driving vehicles / drones (one of the AI technology types in the Eurostat survey) | Eurostat `isoc_eb_ai` by AI type | [K] confirm variable code in dataset metadata | A-Y |
| Driverless paid rides, rider-only miles | CPUC quarterly filings (California), Waymo Safety Impact Data Hub, NHTSA Standing General Order crash data | CPUC/Waymo [V] via secondary reports; primary files to be opened | B-Q |
| AI-enabled medical devices authorised | FDA AI-Enabled Medical Device List | [V] 1,600+ entries as of 2026; FDA states list is not exhaustive | A-Q (list updated periodically) |
| Precision-agriculture adoption | USDA ERS / ARMS; Eurostat farm structure | [K] | C-Y (agriculture stays C) |

**2. cost_to_serve** — *no open price series exists, but an open task-and-quality benchmark does.* Token price lists are open, but v0.5 correctly says per-task cost, not per-token. Build an **AI Task Price Index** on a fixed basket of standardised workflow tasks, priced quarterly from public list prices and measured tokens-per-task with a published harness, divided by the human cost of the same task from Eurostat labour cost index (`lc_lci`) or BLS wage data [K]. Grade C until the harness is published and replicated. Do not use vendor "price fell X %" claims.

*Basket and quality anchor: GDPval [V].* OpenAI's GDPval (published 25 Sept 2025; arXiv 2510.04374) supplies what the basket was missing: real occupational tasks with reference files, expert-written rubrics and blind expert grading ("better", "as good as", "worse than" the human deliverable). The full set has 1,320 tasks across 44 occupations (30 per occupation), of which 220 (5 per occupation) are public as a gold subset on Hugging Face (`openai/gdpval`, with `sector`, `occupation`, `prompt`, `reference_files`, `rubric_json` fields).

*How the index uses it.* Cost is only meaningful at a fixed quality, so the unit is **cost per accepted deliverable**:

> (inference cost + human review and rework time at wage cost + integration overhead) ÷ share of outputs rated at least "as good as" the expert baseline

and `cost_to_serve` is this figure relative to the human cost of the same task, indexed to 100 in the 2026 baseline. Re-run quarterly on the same basket with the models in actual use.

**3. capital_intensity** — GFCF in software/databases and ICT equipment per worker from national accounts (Eurostat `nama_10_*`, BEA) [K]; hyperscaler and frontier-lab capex/commitments from SEC EDGAR XBRL / S-1 filings [V for Anthropic S-1]; AI chip sales and compute stock from Epoch AI (CC BY 4.0) [V]. Read as a level.
*Lower-bound rule (productivity J-curve).* Brynjolfsson, Rock and Syverson (2018/2020, NBER w25148) argue that general purpose technologies need large complementary intangible investment (process redesign, training, new business models) that national accounts do not record, and that the omitted amount is a multiple of the recorded one (estimated multipliers: ~2 for R&D; ~10 for software and hardware). The pillar is therefore published as a **lower bound on total adoption investment**, alongside an intangible multiplier sensitivity case.

### Block B — conditions

**8. energy_capacity** — IEA Energy and AI Observatory [V] (data-centre demand 485 TWh in 2025, projected ~945 TWh by 2030; +17 % in 2025 against +3 % for total demand); interconnection queues: LBNL "Queued Up" and ERCOT/PJM large-load queues (US) [V for Texas TCEQ 8.7 GW permit pause]; Fingrid open data (Finland) [K]; ENTSO-E Transparency Platform [K]. Keep the v0.5 ratio rule: requested MW ÷ connected MW.

**5. governance_burden** — EUR-Lex / CELLAR for Regulation (EU) 2024/1689 and implementing acts (such as Implementing Decision (EU) 2026/2274 citing EN 18286:2026 [V]); FSB Sound Practices [V]; OECD.AI national policies database and AI Incidents Monitor [V]; AI Incident Database [K]. Counting rule stays: named authority + date + sanction/standard.

**6. human_capital** — Eurostat ICT specialists and graduates, digital-skills indicators and Digital Decade series [K]; Statistics Finland / Vipunen education pipeline [K]; OECD.AI skills data [V]; Stanford AI Index for context only.

**10. market_openness** — open_interfaces: Hugging Face Hub API [K], Epoch AI Models dataset [V]; concentration: Epoch finding that five hyperscalers hold over two-thirds of global AI compute [V], Anthropic S-1 disclosure that 48 % of H1 2026 revenue ran through three hyperscaler marketplaces [V], OpenRouter public usage rankings [V]; entry_conditions: OECD PMR indicators [K]; procurement_neutrality: TED notices parsed for brand-name or vendor-specific requirements [V].

### Block C — consequences and distribution

**4. labour_reorganisation** — Eurostat LFS employment by NACE/ISCO and job vacancies [K]; Census BTOS AI supplement (effect on employment and tasks) [V]; Indeed Hiring Lab open postings data [K]; Cedefop Skills-OVATE online job ads [K]; Anthropic Economic Index automation-vs-augmentation shares [V, tier-4 flag].

**9. ownership_distribution** — Federal Reserve Distributional Financial Accounts and ECB Distributional Wealth Accounts [K]; SEC EDGAR 13F, proxy and S-1 filings for institutional/insider/employee share [V for Anthropic S-1]; pledge events logged as events with status announced/executed/lapsed.

**7. ecological_balance** — reference frame: the planetary boundaries framework (Stockholm Resilience Centre; Rockström et al. 2009, Steffen et al. 2015, Richardson et al. 2023) [V]. Three parts, all kept apart from the headline:
*(a) Boundary status panel (context, annual):* Nine boundaries, each with its control variable and the latest published status, shown beside the pillar and never scored.
*(b) direct_footprint:* AI-attributable load, expressed as a share of the global flow behind each control variable. Where a boundary has no AI-specific series the cell says `"not measured"`, never zero.
*(c) enabled_reduction:* modelled potentials only, rebound multiplier mandatory, **no net figure** until both components are A/B in the same sector.

---

## 4. Four fixes to v0.5 (the scientific-validity core)

1. **4.1 Fixed-goalpost levels vs. momentum:** Score *levels* on fixed, published goalposts (adoption shares 0–100 %; per-worker and per-capita quantities on a log scale between published floor and reference values; cost as log of the index against base 100). Keep the trailing percentile as a separate **momentum** score and report annual velocity (pp/yr).
2. **4.2 Comparable-level gap:** Compute the gap on comparable goalpost levels where both endpoint sectors have A or B provenance.
3. **4.3 Series breaks as first-class data:** Never chain across a break; store `break_flag` and `series_version` in the schema.
4. **4.4 Split coverage grade into provenance and frequency:** Provenance `A` (official/administrative register), `B` (academic/intergovernmental/documented commercial), `C` (proxy/voluntary/single-source) + frequency tag (`M`/`Q`/`Y`).
5. **4.5 Aggregation and uncertainty:** Equal weights default; geometric-mean sensitivity case; 1,000-draw Monte Carlo over weights (±50 %) and aggregation method; cell coverage printed next to every composite; no cross-cell imputation of grade-C cells.

---

## 5. Validity programme & References

- Brynjolfsson, E., Rock, D. and Syverson, C. (2018, revised 2020). *The Productivity J-Curve: How Intangibles Complement General Purpose Technologies.* NBER Working Paper 25148.
- Brand, S. (2018). *Pace Layering: How Complex Systems Learn and Keep Learning.* Journal of Design and Science, DOI 10.21428/7f2e5f08.
- OpenAI (2025). *GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks.* arXiv:2510.04374.
- Stockholm Resilience Centre. *Planetary boundaries.* Richardson, K. et al. (2023). *Earth beyond six of nine planetary boundaries.* Science Advances.
- OECD/JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide.*
- Misra, A., Wang, J., McCullers, S., White, K. and Lavista Ferres, J. (2025). *Measuring AI Diffusion: A Population-Normalized Metric for Tracking Global AI Usage.* arXiv:2511.02781.
- Bonney, K. et al. (2024). *Tracking Firm Use of AI in Real Time: A Snapshot from the Business Trends and Outlook Survey.* U.S. Census Bureau CES-WP-24-16.
