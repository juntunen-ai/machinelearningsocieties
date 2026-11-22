# Data release layout

This describes the payload for a versioned data release. The current pipeline version is `1.0.0-rc.1`. **Do not create a GitHub Release or git tag from the `release/1.0.0` branch** until publication is separately approved. The scripts below only prepare files.

## Directory layout

```
data/
  snapshots/<VERSION>/
    README.md                 # what is frozen, and how to refresh it
    series.csv                # curated observations (copy of index/series.csv)
    series.seed.csv           # must match series.csv at snapshot time
    brief_signals.csv
    registry.v1.0.json        # method registry in force when snapshotted
    planetary_boundaries.json
    method.v1.0.json          # authoritative method parameters
    method.v1.0.md
    computed.v1.0.json
    SHA256SUMS                # checksums of every file in the snapshot except this file
    raw/<source_id>/          # optional frozen API responses plus *.meta.json sidecars
```

The 1.0.0-dev snapshot may also keep the v0.6 companions (`registry.v0.6.json`, `method.v0.6.md`, `computed.v0.6.json`) for comparison. Live scoring uses the v1.0 files.

Each raw file should record the request URL, retrieval time (UTC), and HTTP status in a sidecar `*.meta.json`.

## Commands

Rebuild checksums for a snapshot directory (paths in `SHA256SUMS` are relative):

```
python3 scripts/make_checksums.py data/snapshots/1.0.0-dev
```

If `index/series.csv` is intentionally updated, sync the seed in the same commit:

```
python3 scripts/fetch_open_series.py --sync-seed
```

CI fails if `index/series.csv` and `index/series.seed.csv` differ, so the seed cannot drift silently.

## Verifying a payload

```
cd data/snapshots/1.0.0-dev && sha256sum -c SHA256SUMS
```
