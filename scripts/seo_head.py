#!/usr/bin/env python3
"""Normalise crawl metadata on every brief page at deploy time.

Pages are assembled from the previous day's file, so head metadata added to one
edition is not inherited by the next. This pass adds, only where missing:
  - <meta name="description"> derived from the page's og:description
  - hreflang alternates for the English/Finnish pair
  - a robots directive allowing large image previews

It never rewrites editorial content and never fails the deploy.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://machine-learning-societies.web.app"
BRIEFS = os.path.join(ROOT, "briefs")
PAGE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:\.fi)?\.html$")


def patched(html, day, name):
    head_end = html.find("</head>")
    if head_end == -1:
        return html
    head = html[:head_end]
    add = []
    if 'name="description"' not in head:
        match = re.search(r'<meta property="og:description" content="([^"]*)"', head)
        if match:
            add.append('<meta name="description" content="' + match.group(1) + '">')
    if 'name="robots"' not in head:
        add.append('<meta name="robots" content="index,follow,max-image-preview:large">')
    if 'rel="canonical"' not in head:
        add.append('<link rel="canonical" href="' + BASE + '/briefs/' + name + '">')
    if 'hreflang="x-default"' not in head:
        en = BASE + "/briefs/" + day + ".html"
        fi = BASE + "/briefs/" + day + ".fi.html"
        add.append('<link rel="alternate" hreflang="en" href="' + en + '">')
        add.append('<link rel="alternate" hreflang="fi" href="' + fi + '">')
        add.append('<link rel="alternate" hreflang="x-default" href="' + en + '">')
    if not add:
        return html
    block = "\n".join(add)
    return head.rstrip("\n") + "\n" + block + "\n" + html[head_end:]


def main():
    changed = 0
    checked = 0
    for name in sorted(os.listdir(BRIEFS)):
        match = PAGE_RE.match(name)
        if not match:
            continue
        path = os.path.join(BRIEFS, name)
        try:
            with open(path, encoding="utf-8") as handle:
                html = handle.read()
            updated = patched(html, match.group(1), name)
            if updated != html:
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(updated)
                changed += 1
            checked += 1
        except Exception as exc:  # never break a deploy over metadata
            print("warning: %s: %s" % (name, exc))
    print("seo_head: %d pages checked, %d updated" % (checked, changed))


if __name__ == "__main__":
    main()
