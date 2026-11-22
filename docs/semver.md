# Versioning policy

The file `VERSION` at the repository root is the **single source of truth** for the pipeline and release version. Do not copy a different version string into scripts or documentation without updating `VERSION` first.

`scripts/check_version.py` fails CI if listed files drift out of sync with `VERSION`.

## How numbers are assigned

This project follows [Semantic Versioning 2.0.0](https://semver.org/). During development the version is `MAJOR.MINOR.PATCH-dev`. A release candidate uses a pre-release suffix such as `1.0.0-rc.3` (currently `1.0.0-rc.3`). Drop the pre-release suffix only when a GitHub Release and tag are created, which requires a separate publication approval. This branch must not create that tag.

| Change | Bump | Examples |
| --- | --- | --- |
| Methodology-breaking change | **MAJOR** | New goalposts, new Block A aggregation, dropping or redefining a pillar, changing the 0–100 meaning, a new `method.v*` document that invalidates previous scores |
| Backward-compatible method or data additions | **MINOR** | A new verified `[V]` series that does not change existing goalposts, a new diagnostic that is not part of the headline |
| Bug fixes and tooling | **PATCH** | Schema typo, accessibility fix, checksum script, CI, typo in notes that does not change a published number |

If a patch would change a previously published headline score or confidence interval, treat it as **MAJOR** (or publish a corrected release with a clear changelog entry and a new method note). Do not silently rewrite a published number under the same tag.

## What a release must contain

A tagged release (not created from this branch) should include:

- The `VERSION` string matching the tag (`v1.0.0` ↔ `1.0.0`)
- `CHANGELOG.md` entry for that version
- Data payload described in `docs/data-release.md` (snapshots + `SHA256SUMS`)
- The site artifact described in `docs/publishing.md`

Method v1.0 is frozen on `release/1.0.0` (`index/method.v1.0.json` is authoritative). `VERSION` is `1.0.0-rc.3` on this candidate. A 1.0.0 tag still needs a separate publication approval. The method file, `pipeline_version` in `computed.v1.0.json`, and the dashboard must stay consistent with `VERSION` (the public method edition may still read “1.0.0”).
