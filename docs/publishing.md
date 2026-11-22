# Single publishing channel

GitHub Pages and Firebase Hosting must serve the **same site artifact** produced from a single commit. They must not run divergent compute or brief-sync steps at deploy time.

## Current host setup (read-only check, 22 November 2026)

- GitHub Pages: legacy build from branch `main`, path `/`. Changing this setting is out of scope until publication is approved.
- Firebase Hosting: `.github/workflows/firebase-hosting.yml`, project `machine-learning-societies`, **job runs only when `github.ref == refs/heads/main`**.

Work on `release/1.0.0` must not deploy.

## Build step (every branch)

The `CI` workflow (`.github/workflows/ci.yml`) has no access to Firebase secrets. It:

1. Validates `series.csv` and `brief_signals.csv` (Pandera + JSON Schema).
2. Runs pytest (formulas, `[K]` block, seeded Monte Carlo, golden JSON).
3. Re-runs `scripts/compute_index.py` and confirms the committed golden file still matches, ignoring `generated_at`.
4. Packages the public site with `scripts/package_site_artifact.py` into `dist/site/` plus `dist/SHA256SUMS`, and uploads it as a workflow artifact named `site`.

## Deploy step (`main` only, not run from this branch)

The Firebase workflow is gated to `main`. It must deploy the **committed** public tree (or the `site` artifact built from that commit). It must **not**:

- run `scripts/sync_briefs_to_index.py` or `scripts/fetch_open_series.py` in a way that rewrites `index/` on the runner and then publishes the dirty tree
- publish from any branch other than `main`, including `workflow_dispatch`

Until a Pages settings change is approved, Pages continues to serve the `main` tree at `/`. After this design lands on `main`, that tree and the Firebase public set (see `firebase.json` ignore rules) will share the same committed index files and the same `computed.v1.0.json`. Residual extras on Pages (for example `scripts/` and `tests/`) do not change scores; a later settings change can point Pages at the packed artifact if desired.

## Local package

```
python3 scripts/package_site_artifact.py
sha256sum -c dist/SHA256SUMS
```
