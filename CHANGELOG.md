# Changelog

All notable changes to the Machine Learning Societies AI Diffusion Index are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and version numbers follow the policy in `docs/semver.md`.

The pipeline version in the `VERSION` file is the single source of truth. Method v1.0 is frozen on this branch (`index/method.v1.0.json` is authoritative). The current pipeline version is **1.0.0-rc.2**. This is a release candidate on `release/1.0.0`, not a GitHub Release or git tag.

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
