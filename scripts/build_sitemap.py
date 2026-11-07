#!/usr/bin/env python3
"""Regenerate sitemap.xml from the published brief files.

Run in the deploy workflow after the brief index is rebuilt, so every edition
is listed with its English/Finnish alternates. Writes only when content changes.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://machine-learning-societies.web.app"
BRIEFS = os.path.join(ROOT, "briefs")
BRIEF_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.html$")

STATIC_PAGES = [
    ("", "1.0"),
    ("about.html", "0.7"),
    ("forecasts.html", "0.8"),
    ("diffusion-index.html", "0.8"),
    ("diffusion-method.html", "0.5"),
]


def edition_dates():
    dates = []
    for name in os.listdir(BRIEFS):
        match = BRIEF_RE.match(name)
        if match:
            dates.append(match.group(1))
    return sorted(set(dates), reverse=True)


def url_entry(loc, lastmod, priority, alternates):
    lines = ["  <url>"]
    lines.append("    <loc>" + loc + "</loc>")
    lines.append("    <lastmod>" + lastmod + "</lastmod>")
    for hreflang, href in alternates:
        lines.append(
            '    <xhtml:link rel="alternate" hreflang="' + hreflang + '" href="' + href + '"/>'
        )
    lines.append("    <priority>" + priority + "</priority>")
    lines.append("  </url>")
    return "\n".join(lines)


def build(dates):
    lastmod = dates[0] if dates else "2026-01-01"
    entries = []
    for path, priority in STATIC_PAGES:
        entries.append(url_entry(BASE + "/" + path, lastmod, priority, []))
    for day in dates:
        en = BASE + "/briefs/" + day + ".html"
        fi = BASE + "/briefs/" + day + ".fi.html"
        alternates = [("en", en), ("fi", fi), ("x-default", en)]
        entries.append(url_entry(en, day, "0.9", alternates))
        entries.append(url_entry(fi, day, "0.9", alternates))
    header = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    )
    return header + "\n".join(entries) + "\n</urlset>\n"


def main():
    dates = edition_dates()
    if not dates:
        sys.exit("no brief files found; refusing to write an empty sitemap")
    xml = build(dates)
    path = os.path.join(ROOT, "sitemap.xml")
    old = None
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            old = handle.read()
    changed = xml != old
    if changed:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(xml)
    print("sitemap.xml: %d editions, %s" % (len(dates), "updated" if changed else "unchanged"))


if __name__ == "__main__":
    main()
