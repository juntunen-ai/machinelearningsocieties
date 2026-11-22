# Snapshot 1.0.0-dev

Frozen curated inputs for pipeline version `1.0.0-dev` on branch `release/1.0.0`.

This is not a published GitHub Release. Refresh the files from `index/` when the curated series or briefs change, then run:

```
python3 scripts/make_checksums.py data/snapshots/1.0.0-dev
```

`series.csv` and `series.seed.csv` must be identical in this snapshot.

Raw API responses (Eurostat, Statistics Finland, and others) are not included yet. When live fetches are implemented, store them under `raw/<source_id>/` with a `*.meta.json` sidecar as described in `docs/data-release.md`.
