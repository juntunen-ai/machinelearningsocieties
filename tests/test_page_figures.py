"""The dashboard must not hard-code figures for components that are not measured."""

from __future__ import annotations

import json
import re
from pathlib import Path

FORBIDDEN_TOKENS = ("52.4", "26.8", "42.7", "+52.4", "-26.8", "−26.8")


def test_page_js_and_html_have_no_hardcoded_not_measured_figures(repo_root: Path):
    js = (repo_root / "assets" / "diffusion-index.js").read_text(encoding="utf-8")
    html = (repo_root / "diffusion-index.html").read_text(encoding="utf-8")
    for token in FORBIDDEN_TOKENS:
        assert token not in js, f"page JS still contains {token!r}"
        assert token not in html, f"main page HTML still contains {token!r}"
    assert not re.search(r"35\s*%", js), "page JS still contains a hardcoded Jevons 35%"
    assert "0.35" not in js
    # renderPlanetary must not format burden_score / abatement_score as numbers
    assert "formatNumber(b.burden_score" not in js
    assert "formatNumber(b.abatement_score" not in js
    assert "headline_rule_en" not in js
    computed = json.loads((repo_root / "index" / "computed.v1.0.json").read_text(encoding="utf-8"))
    meter = computed["planetary_boundaries"]["summary_meter"]
    assert meter["burden_increase_score"] is None
    assert meter["burden_reduction_score"] is None
    assert meter["rebound_discount_factor"] is None
    for boundary in computed["planetary_boundaries"]["boundaries"]:
        assert boundary["burden_score"] is None
        assert boundary["abatement_score"] is None


def test_page_marks_rc_figures_as_preliminary(repo_root: Path):
    html = (repo_root / "diffusion-index.html").read_text(encoding="utf-8")
    assert "Preliminary, data cut-off 31 Dec 2026" in html
