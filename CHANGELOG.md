# Changelog

All notable changes to the Machine Learning Societies – Diffusion Index are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and version numbers follow the policy in `docs/semver.md`.

The pipeline version in the `VERSION` file is the single source of truth. Method v1.0 is frozen on this branch (`index/method.v1.0.json` is authoritative). The current pipeline version is **1.0.0-rc.3**. This is a release candidate on `release/1.0.0`, not a GitHub Release or git tag.

## [1.0.0-rc.3] — 2026-11-22

Release candidate on branch `release/1.0.0`. Not tagged and not deployed. **Method change before the 1.0.0 tag**, by Harri Juntunen's decision (22 November 2026, 18:15, rc review option (a)+(c)).

### Changed

- **Headline impact (method change):** the headline is now the deployment pillar alone. Capital intensity (K1, ICT equipment + IPP investment, % of GDP) is a national-accounts proxy, not AI-specific. It made up 69–78 % of the rc.2 headline and correlated 0.98 with it across the 27 member states, so it moves from Block A to Block B (context/enablers). It is still computed and shown with n, grade, interval and pace, but never enters the headline.

  | | rc.2 | rc.3 |
  |---|---|---|
  | EU27 headline (range by weighting) | 21.7 (16.7–27.0), display 22 | **9.3 (5.6–13.2)**, display 9 |
  | EU27 geometric / median | 17.8 / 21.6 | 9.3 / 9.4 |
  | Finland headline (range by weighting) | 28.3 (23.8–33.3), display 28 | **17.3 (10.4–24.4)**, display 17 |
  | Finland geometric / median | 26.1 / 28.3 | 17.3 / 17.3 |
  | Variance shares data / weights / aggregation | EU27 5/61/34, FI 11/72/17 | 1/99/0 in both |
  | K1 capital (Block B) | in headline: EU27 34.0, FI 39.3 | not in headline: EU27 34.0 (31.0–37.0), FI 39.3 (35.8–42.8) |

- Evidence rule: the headline needs at least 1 eligible Block A pillar, not 2. Block A is now deployment and cost_to_serve (nominal 1/2 each). While cost_to_serve is experimental, deployment alone is a valid headline.
- Channel weights decided: the point estimate stays digital 0.5 / physical 0.5, and the Monte Carlo draws the digital weight from U[0.25, 0.75] (`monte_carlo.channel_weights`, generator PCG64(seed + 2)). The headline interval now includes the channel choice. Its variance is 99 % channel weights and 1 % data in both populations.
- The noise matrix covers every indicator that enters any pillar score, so Block B pillars such as capital_intensity get data-noise intervals.
- DAI is no longer proxy-flagged: Block A has only AI-specific inputs. EU27 DAI 17.3, PAI 1.4; Finland DAI 31.9, PAI 2.7.
- Paces are unchanged (separate generator).
- The public name of the index is now “Machine Learning Societies – Diffusion Index” (en dash). It previously appeared as “AI Diffusion Index”.
- Added an internal appendix, `docs/analysis/1.0.0-sensitivity-and-coherence.md`, with reproducible scripts in `scripts/analysis/` and Eurostat 2025 member-state inputs. It covers sensitivity scenarios (channel weights, goalposts, K1 placement and weight, cost_to_serve bounds, D5, the 2025 break bound) and a coherence matrix across the 27 member states. It is not linked from the pages and no published number changes.
- Registry licences applied from the TP3 licence audit (2026-11-22): every source now has `licence`, `licence_url`, `licence_checked`, `reuse_class`, `redistribution` and `attribution`. `gdpval` and `ramp_ai_index` are marked `use: context_only` (no open licence). `iea_energy_ai` is split into the Energy and AI report (CC BY 4.0, stays a possible score input) and `iea_energy_ai_observatory` (IEA non-CC terms, context only); OBS-051 retagged to the Observatory. No score changes.
- Public pages (`diffusion-index.html`, `copy/main-page.en.md`, `assets/diffusion-index.js`) now present the headline as company adoption alone. Capital intensity is labelled context and shown in Block B, not in the headline number. The live lead is Wedgwood’s final wording: “Most companies have not yet put AI to work. Company adoption scores 9 out of 100 in the EU27 and 17 in Finland.” The previous lead, “The money has arrived. The use hasn't.”, is kept only as context framing on the capital-versus-use card, where capital (EU27 34, Finland 39) still sits well above use (9 and 17).
- The public page and the methodology page (`diffusion-method.html`) state that the width of the published range comes almost entirely from the digital-versus-physical channel weighting (the digital share is drawn from U[0.25, 0.75]), not from the data. The v1.0 method content (`index/method.v1.0.md` and `index/method.v1.0.json`) changed in 1.0.0-rc.3; it is frozen only when the 1.0.0 tag is created. The methodology page was brought into line with that updated method for the rc.3 architecture, weights, Monte Carlo, worked example and limitations.

## [1.0.0-rc.2] — 2026-11-22

Release candidate on branch `release/1.0.0`. Not tagged and not deployed. Succeeds 1.0.0-rc.1, which was rejected in review because the planetary panel still showed v0.6 constants while ecological_balance was not measured.

### Changed

- **Headline impact:** the v0.6 headline 42.7 was a hand-set constant, not a computed score. Under method v1.0 the compiled headlines are EU27 22 and Finland 28 (display integers). The change is the move from those constants to scores computed from `series.csv`.
- The compiler reads four previously hardcoded parameters only from `index/method.v1.0.json`: `staleness_limit_months`, population geo codes (`series_geo_codes`), the missing-sigma fallback by grade, and the geometric-mean floor used in the Monte Carlo path. Frozen values are unchanged.
- Pillar cards report observation and source counts for the selected population (EU27 and Finland separately), following the per-population evidence rule (OECD K1x is the second official source for capital; never scored).
- Ecological-balance figures inherited from v0.6 (`+52.4`, `−26.8`, Jevons 35%) are nulled in the computed payload. The page renders “not measured”.
- The industry matrix states how many of the 100 cells are scored, and unmeasured cells show “n/m” with a legend (not colour alone).
- Release-candidate figures on the page are marked “Preliminary, data cut-off 31 Dec 2026” and will be recomputed before release.

### Added

- Tests that each of the four method parameters is read from JSON (changing the parameter changes the output), and a check that page JavaScript does not hard-code numeric figures for not-measured components.
- Draft release notes in `docs/release-notes-1.0.0-rc.2.md` (documentation only; no tag or GitHub Release).

## [1.0.0-rc.1] — 2026-11-22

Release candidate on branch `release/1.0.0`. Not tagged and not deployed.

### Added

- English main page copy from `copy/main-page.en.md` wired into `diffusion-index.html`. The page is English only (`lang=en`), with no Finnish toggle or Finnish strings, and does not write a language choice to `localStorage`.
- Live binding of scores and statuses from `index/computed.v1.0.json`. EU27 and Finland are shown separately. Every published figure carries a status: scored, experimental, not measured, stale or incomplete.
- Draft release notes in `docs/release-notes-1.0.0-rc.1.md` (documentation only; no tag or GitHub Release).

### Changed

- The opening of the dashboard follows Wedgwood's section order: result, the gap, how to read the score, audience doors, press, credit. Reliable task completion is experimental, so the gap chart has two bars, not three. There is no headline speed card (no three comparable headline points yet).
- `{{PUBLISHER_LINE}}` and `{{NEXT_UPDATE_DATE}}` remain visible placeholders, pending Harri's decisions.

## [1.0.0-dev] — Unreleased

Work that led to this candidate (still documented here; not a separate release).

### Added

- v1.0 compiler (`scripts/compute_index.py`) reads every scoring parameter from `index/method.v1.0.json` and writes `index/computed.v1.0.json`. No pillar or headline score is hard-coded.
- `index/registry.v1.0.json`, including the official Eurostat `nama_10_an6` source for capital intensity.
- series.csv columns `segment_id`, `sigma`, `sigma_basis`, `bridge_source`, `bridge_period`, `indicator_id`, `source_release_date`, and `source_flag`.
- Golden-file and sensitivity tests for the v1.0 compiler, plus pytest coverage for goalpost formulas and the `[K]` unverified-source block.
- English methodology page `diffusion-method.html`, generated from `index/method.v1.0.md`.
- CI workflow that runs on every branch and pull request without Firebase secrets.
- Pandera schemas and JSON Schema for `index/series.csv` and `index/brief_signals.csv`, validated in CI.
- Data-release layout, raw Eurostat snapshots, and a SHA256 checksum script.
- Site packaging script so GitHub Pages and Firebase can later serve the same artifact (deploy jobs stay gated to `main` and are not run from this branch).
- Semver policy (`docs/semver.md`) and a version consistency check.
- Accessibility fixes on the index page and shared chrome: skip link, in-content link underlines, table header `scope`, favicon, and `lang` updates on language toggle.

### Changed

- Method v1.0 (TP1 review, 2026-11-22, pre-tag, no version bump): the 36-month staleness limit applies to level selection only; pace history uses the whole comparable segment (K1 2019–2025, isoc_eb_ai S1 2021/2023/2024). Pace OLS t-interval from n ≥ 3 (was n ≥ 4), and pace Monte Carlo on its own stream PCG64(seed + 1). New source rule (one designated source per indicator for every population; Eurostat for D1–D4 and K1) and grid rules for multi-section sectors and Eurostat survey scope. `channel_weights` marked provisional pending Harri Juntunen's decision. Headlines unchanged: EU27 21.7 [16.7–27.0], FI 28.3 [23.8–33.3] (FI interval moved by 0.1 because pace draws no longer share the level stream).
- Scores are computed from `series.csv` through the published chain. Channel weights (digital/physical) are a single JSON parameter, default 0.5 / 0.5, pending a decision by Harri Juntunen.
- `scripts/fetch_open_series.py` no longer overwrites `index/series.seed.csv` unless `--sync-seed` is passed, and it validates against `registry.v1.0.json`.
- Firebase Hosting deploy is a no-op on any ref other than `main`.

### Fixed

- Sector D1 rows checked against Eurostat `isoc_eb_ain2` 2025: OBS-013/015/016/017 corrected to 62.52 (J), 40.43 (M), 18.16 (D_E), 17.27 (C); OBS-014 (K), OBS-019 (Q), OBS-020 (P), OBS-021 (O), OBS-022 (A) removed as outside the survey scope; OBS-018 (G+H) removed because no combined value is published.
- OBS-012 (FI × software) now uses Eurostat FI NACE J 79.79 instead of the rounded Statistics Finland ICT-sector figure.
- OBS-040 retagged: sector software, source `anthropic_research_formal_verification` (new tier-4 registry entry; context only), also in `brief_signals.csv`.
- OBS-027 EU27 2025 D3 corrected from 6.4 to 8.28 (official Eurostat `E_AI_TGE3`).
- OBS-025 / OBS-026 no longer carry the rejected 0.563 BTOS bridge factor (US context only; no bridge).
- `index/series.seed.csv` is synchronized with `index/series.csv`.
- Evidence rule counted per population (rc review): a pillar's observations and sources are counted only from rows of the population being scored, not across all geographies. capital_intensity previously met the two-source test in EU27 and Finland only through US/GLOBAL K2 context rows; it now meets it through a second official source, OECD national accounts Table 1 (`oecd_sna_table1`, cross-check indicator K1x, OBS-091 to OBS-103, never scored, agrees with Eurostat within 0.1 pp). New indicator role `cross_check`. Scores, intervals, eligibility and headlines are unchanged; only the evidence counts (n, sources) per pillar change.
- Method text on the DAI/PAI proxy flag (`block_a.dai_pai`, methodology §7): both channels carry the flag when a proxy contributes. v1.0 flags DAI (K1 is a national-accounts proxy) and not PAI (only D4 E_AI_TAR, AI-specific); v0.6 flagged PAI because it used IFR robot density. Metadata only; the computed flags were already correct.
