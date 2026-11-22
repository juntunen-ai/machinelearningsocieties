#!/usr/bin/env python3
"""Validate index/series.csv and index/brief_signals.csv.

Uses JSON Schema (schemas/*.schema.json) and Pandera DataFrame schemas.
Pandera is the open-source data-quality tool chosen from the 2026
toolsfordata.com open-source data quality list.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import pandera.pandas as pa
from jsonschema import Draft202012Validator, FormatChecker
from pandera.pandas import Check, Column, DataFrameSchema

ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT / "index"
SCHEMA_DIR = ROOT / "schemas"
REGISTRY_PATH = INDEX_DIR / "registry.v0.6.json"
SERIES_CSV = INDEX_DIR / "series.csv"
BRIEF_CSV = INDEX_DIR / "brief_signals.csv"

BOOL_VALUES = {"true": True, "false": False, "1": True, "0": False, "yes": True, "no": False}


def load_registry():
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _ids(items):
    return [item if isinstance(item, str) else item["id"] for item in items]


def enum_sets(registry):
    pillars = [p["id"] for p in registry["pillars"]]
    sectors = [s["id"] for s in registry["sectors"]]
    return {
        "pillars": pillars,
        "sectors": sectors,
        "sectors_with_all": sectors + ["ALL"],
        "sources": [s["id"] for s in registry["sources"]],
        "channels": _ids(registry["channels"]),
        "layers": _ids(registry["layers"]),
        "pace_layers": _ids(registry["pace_layers"]),
        "blocks": list(registry["blocks"].keys()),
        "grades": [f"{p}-{f}" for p in "ABC" for f in "MQY"],
        "ai_specificity": ["specific", "proxy", "macro_context"],
        "levels": ["macro", "meso", "micro"],
        "verified_sources": {s["id"] for s in registry["sources"] if s.get("verified")},
    }


def load_schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _as_bool(value):
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text not in BOOL_VALUES:
        raise ValueError(f"not a boolean: {value!r}")
    return BOOL_VALUES[text]


def load_series_frame(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    frame["value"] = pd.to_numeric(frame["value"])
    frame["trust_tier"] = pd.to_numeric(frame["trust_tier"], downcast="integer")
    frame["bridge_factor"] = pd.to_numeric(frame["bridge_factor"])
    frame["break_flag"] = frame["break_flag"].map(_as_bool)
    return frame


def load_brief_frame(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    frame["signal_score"] = pd.to_numeric(frame["signal_score"])
    frame["stakes_score"] = pd.to_numeric(frame["stakes_score"])
    return frame


def series_pandera_schema(enums: dict) -> DataFrameSchema:
    return DataFrameSchema(
        {
            "obs_id": Column(str, checks=Check.str_matches(r"^OBS-\d{3}$"), unique=True),
            "date_logged": Column(str, checks=Check.str_matches(r"^\d{4}-\d{2}-\d{2}$")),
            "period": Column(str, checks=Check.str_length(min_value=4)),
            "pillar": Column(str, checks=Check.isin(enums["pillars"])),
            "sector": Column(str, checks=Check.isin(enums["sectors_with_all"])),
            "channel": Column(str, checks=Check.isin(enums["channels"])),
            "layer": Column(str, checks=Check.isin(enums["layers"])),
            "geo": Column(str, checks=Check.str_length(min_value=1)),
            "value": Column(float),
            "unit": Column(str, checks=Check.str_length(min_value=1)),
            "source_id": Column(str, checks=Check.isin(enums["sources"])),
            "series_id": Column(str, checks=Check.str_length(min_value=1)),
            "series_version": Column(str, checks=Check.str_length(min_value=1)),
            "grade": Column(str, checks=Check.isin(enums["grades"])),
            "trust_tier": Column(int, checks=Check.in_range(1, 5)),
            "break_flag": Column(bool),
            "bridge_factor": Column(float, checks=Check.gt(0)),
            "ai_specificity": Column(str, checks=Check.isin(enums["ai_specificity"])),
            "brief_ref": Column(str, nullable=False),
            "notes": Column(str, checks=Check.str_length(min_value=1)),
        },
        coerce=True,
        strict=True,
    )


def brief_pandera_schema(enums: dict) -> DataFrameSchema:
    return DataFrameSchema(
        {
            "brief_date": Column(str, checks=Check.str_matches(r"^\d{4}-\d{2}-\d{2}$"), unique=True),
            "title_en": Column(str, checks=Check.str_length(min_value=1)),
            "title_fi": Column(str, checks=Check.str_length(min_value=1)),
            "pillar": Column(str, checks=Check.isin(enums["pillars"])),
            "secondary_pillar": Column(str, checks=Check.isin(enums["pillars"])),
            "sector": Column(str, checks=Check.isin(enums["sectors"])),
            "block": Column(str, checks=Check.isin(enums["blocks"])),
            "pace_layer": Column(str, checks=Check.isin(enums["pace_layers"])),
            "channel": Column(str, checks=Check.isin(enums["channels"])),
            "layer": Column(str, checks=Check.isin(enums["layers"])),
            "level": Column(str, checks=Check.isin(enums["levels"])),
            "signal_score": Column(float, checks=Check.in_range(0, 10)),
            "stakes_score": Column(float, checks=Check.in_range(0, 10)),
            "market_test": Column(
                str, checks=Check.str_matches(r"^Primary=\d+;Confirmation=\d+;FirstMover=\d+$")
            ),
            "source_id": Column(str, checks=Check.isin(enums["sources"])),
            "quant_metric": Column(str, checks=Check.str_length(min_value=1)),
            "primary_urls": Column(str, checks=Check.str_length(min_value=1)),
            "brief_path": Column(str, checks=Check.str_matches(r"^briefs/\d{4}-\d{2}-\d{2}\.html$")),
            "summary_note": Column(str, checks=Check.str_length(min_value=1)),
        },
        coerce=True,
        strict=True,
    )


def _row_for_jsonschema(row: dict) -> dict:
    out = dict(row)
    # jsonschema wants native types already applied on the pandas side
    return out


def validate_jsonschema(frame: pd.DataFrame, schema: dict, label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    records = json.loads(frame.to_json(orient="records"))
    for index, row in enumerate(records):
        for err in validator.iter_errors(row):
            path = ".".join(str(p) for p in err.path) or "(row)"
            errors.append(f"{label} row {index}: {path}: {err.message}")
    return errors


def extra_series_rules(frame: pd.DataFrame, enums: dict) -> list[str]:
    errors = []
    unverified = frame.loc[~frame["source_id"].isin(enums["verified_sources"]), "obs_id"]
    for obs_id in unverified:
        errors.append(f"series {obs_id}: source_id is not a verified [V] source")
    return errors


def extra_brief_rules(frame: pd.DataFrame) -> list[str]:
    errors = []
    root = ROOT
    for _, row in frame.iterrows():
        path = root / row["brief_path"]
        if not path.is_file():
            errors.append(f"brief {row['brief_date']}: missing file {row['brief_path']}")
    return errors


def validate_all(series_path: Path = SERIES_CSV, brief_path: Path = BRIEF_CSV) -> list[str]:
    registry = load_registry()
    enums = enum_sets(registry)
    errors: list[str] = []

    series = load_series_frame(series_path)
    briefs = load_brief_frame(brief_path)

    try:
        series_pandera_schema(enums).validate(series, lazy=True)
    except pa.errors.SchemaErrors as exc:
        errors.append(f"Pandera series.csv:\n{exc.failure_cases}")

    try:
        brief_pandera_schema(enums).validate(briefs, lazy=True)
    except pa.errors.SchemaErrors as exc:
        errors.append(f"Pandera brief_signals.csv:\n{exc.failure_cases}")

    errors.extend(validate_jsonschema(series, load_schema("series.schema.json"), "series.csv"))
    errors.extend(validate_jsonschema(briefs, load_schema("brief_signals.schema.json"), "brief_signals.csv"))
    errors.extend(extra_series_rules(series, enums))
    errors.extend(extra_brief_rules(briefs))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Diffusion Index CSV tables.")
    parser.parse_args()
    errors = validate_all()
    if errors:
        print(f"[FAIL] {len(errors)} validation error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("[OK] series.csv and brief_signals.csv passed Pandera and JSON Schema checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
