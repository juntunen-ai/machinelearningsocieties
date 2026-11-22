# Changelog

All notable changes to the Machine Learning Societies AI Diffusion Index are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and version numbers follow the policy in `docs/semver.md`.

The pipeline version in the `VERSION` file is the single source of truth. The published measurement method remains **v0.6** until the method freeze (TP1) and the “scores from data” work (TP2.1) land. User-facing pages may still say v0.6 during this development cycle.

## [1.0.0-dev] — Unreleased

Work on the `release/1.0.0` branch toward a 1.0.0 publication. This is not a release.

### Added

- Pytest suite for helper formulas, the `[K]` unverified-source block, seeded Monte Carlo bands, and a golden check of `index/computed.v0.6.json` (ignoring `generated_at`).
- CI workflow that runs on every branch and pull request without Firebase secrets.
- Pandera schemas and JSON Schema for `index/series.csv` and `index/brief_signals.csv`, validated in CI.
- Data-release layout, raw input snapshots, and a SHA256 checksum script.
- Site packaging script so GitHub Pages and Firebase can later serve the same artifact (deploy jobs stay gated to `main` and are not run from this branch).
- Semver policy (`docs/semver.md`) and a version consistency check.
- Accessibility fixes on the index page and shared chrome: skip link, in-content link underlines, table header `scope`, favicon, and `lang` updates on language toggle.

### Changed

- `scripts/compute_index.py` exposes `compute()` for tests and records `pipeline_version` from `VERSION`. Pillar scores remain the v0.6 hardcoded values until TP2.1.
- `scripts/fetch_open_series.py` no longer overwrites `index/series.seed.csv` unless `--sync-seed` is passed.
- Firebase Hosting deploy is a no-op on any ref other than `main`.

### Fixed

- `index/series.seed.csv` is synchronized with `index/series.csv` (includes OBS-057).
