# Snapshot 1.0.0-dev

Frozen curated inputs for pipeline version `1.0.0-dev` on branch `release/1.0.0`.

This is not a published GitHub Release. Live scoring uses the v1.0 files (`method.v1.0.json`, `registry.v1.0.json`, `computed.v1.0.json`). The v0.6 companions are kept for comparison.

Refresh the curated files from `index/` when the series, method or briefs change, then run:

```
python3 scripts/make_checksums.py data/snapshots/1.0.0-dev
```

`series.csv` and `series.seed.csv` must be identical in this snapshot.

Raw Eurostat API responses for `isoc_eb_ai`, `isoc_ai_iaiu` and `nama_10_an6` (retrieved 2026-11-22) sit under `raw/<source_id>/` with a `*.meta.json` sidecar.
