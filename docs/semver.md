# Versioning policy

The file `VERSION` at the repository root is the **single source of truth** for the pipeline and release version. Do not copy a different version string into scripts or documentation without updating `VERSION` first.

`scripts/check_version.py` fails CI if listed files drift out of sync with `VERSION`.

## How numbers are assigned

This project follows [Semantic Versioning 2.0.0](https://semver.org/). During development the version is `MAJOR.MINOR.PATCH-dev` (currently `1.0.0-dev`). Drop the `-dev` suffix only when a GitHub Release and tag are created, which requires a separate publication approval.

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

Method v1.0 is frozen on `release/1.0.0` (`index/method.v1.0.json` is authoritative). `VERSION` remains `1.0.0-dev` until a 1.0.0 tag is approved. The public dashboard may still be labelled v0.6 until the main-page copy is wired; after that, the method file, `schema_version` in `computed.v1.0.json`, and the dashboard label must move together with `VERSION`.
