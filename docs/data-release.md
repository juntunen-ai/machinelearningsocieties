# Data release layout

This describes the payload for a versioned data release. **Do not create a GitHub Release or git tag from the `release/1.0.0` branch** until publication is separately approved. The scripts below only prepare files.

## Directory layout

```
data/
  snapshots/<VERSION>/
    README.md                 # what is frozen, and how to refresh it
    series.csv                # curated observations (copy of index/series.csv)
    series.seed.csv           # must match series.csv at snapshot time
    brief_signals.csv
    registry.v0.6.json        # method registry in force when snapshotted
    planetary_boundaries.json
    method.v0.6.md
    computed.v0.6.json
    SHA256SUMS                # checksums of the files above (except this file)
```

When live fetches against Eurostat or Statistics Finland are implemented, raw API responses belong in:

```
data/snapshots/<VERSION>/raw/<source_id>/<downloaded-at>-<filename>
```

Each raw file should record the request URL, retrieval time (UTC), and HTTP status in a sidecar `*.meta.json`. `scripts/fetch_open_series.py` currently validates registry links and can optionally ping Eurostat; it does not yet snapshot raw responses.

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
