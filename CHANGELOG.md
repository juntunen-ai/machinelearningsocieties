# Changelog

All notable changes to the Machine Learning Societies AI Diffusion Index are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and version numbers follow the policy in `docs/semver.md`.

The pipeline version in the `VERSION` file is the single source of truth. Method v1.0 is frozen on this branch (`index/method.v1.0.json` is authoritative). The current pipeline version is **1.0.0-rc.1**. This is a release candidate on `release/1.0.0`, not a GitHub Release or git tag.

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

- Scores are computed from `series.csv` through the published chain. Channel weights (digital/physical) are a single JSON parameter, default 0.5 / 0.5, pending a decision by Harri Juntunen.
- `scripts/fetch_open_series.py` no longer overwrites `index/series.seed.csv` unless `--sync-seed` is passed, and it validates against `registry.v1.0.json`.
- Firebase Hosting deploy is a no-op on any ref other than `main`.

### Fixed

- OBS-027 EU27 2025 D3 corrected from 6.4 to 8.28 (official Eurostat `E_AI_TGE3`).
- OBS-025 / OBS-026 no longer carry the rejected 0.563 BTOS bridge factor (US context only; no bridge).
- `index/series.seed.csv` is synchronized with `index/series.csv`.
