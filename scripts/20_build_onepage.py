#!/usr/bin/env python3
"""Build the single-page edition (onepage.qmd) from index.qmd and the chapters.

Until the audit of 19 September 2026 the single-page edition was assembled by hand,
which is how it came to lag behind the chapters by half a day. It is now generated:
the chapters are the only source, and `quarto render onepage.qmd` produces the
self-contained HTML.

Rules applied to each chapter file:
  * the YAML title becomes `# <title> {#sec-chNN}` and the subtitle an italic line;
  * section headings keep their level (## / ###) and their explicit {#ids};
  * links to `NN-name.qmd` (or `chapters/NN-name.qmd` from index.qmd) become
    `#sec-chNN`; a `NN-name.qmd#anchor` link becomes `#anchor`;
  * `../plots/` and `../data/` become `plots/` and `data/` (the page is rendered
    from the project root);
  * `{.unnumbered}` is dropped from the overview's section headings (the overview
    itself is unnumbered; the chapters are numbered in the single page).

Reads : index.qmd, chapters/*.qmd (in the order of the site's sidebar, audit last)
Writes: onepage.qmd
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CH = ROOT / "chapters"

# The briefing chapters (14-*) and the synthesis chapters (15-*) are standalone
# documents with their own PDF output and are deliberately not part of the
# single-page edition.
ORDER = ["01-data-hunt", "02-euskadi", "03-spain-2026", "04-distributions",
         "05-subjects-sittings", "06-interpretation", "11-exam-content",
         "12-ehu-paper-history", "16-paradigm", "07-literature", "08-sources", "09-log",
         "10-reproduce", "13-audit"]

HEADER = """---
title: "Physics in the PAU, 2026: what the data now say"
subtitle: "Single-page edition of the report (all chapters) — Euskadi (UPV/EHU) 2010–2026 in its Spanish context"
date: 2026-09-19
toc: true
toc-depth: 2
number-sections: true
embed-resources: true
bibliography: references.bib
csl: apa.csl
---
"""


def split_front_matter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "no YAML front matter"
    meta = {}
    for line in m.group(1).splitlines():
        k = re.match(r'^(title|subtitle):\s*"(.*)"\s*$', line)
        if k:
            meta[k.group(1)] = k.group(2)
    return meta, text[m.end():]


def rewrite_links(body: str) -> str:
    # chapters/NN-name.qmd (from index) or NN-name.qmd (from chapters), optional #anchor
    def repl(m):
        num, anchor = m.group(1), m.group(2)
        return f"](#{anchor})" if anchor else f"](#sec-ch{num})"
    body = re.sub(r"\]\((?:chapters/)?(\d\d)-[a-z0-9-]+\.qmd(?:#([A-Za-z0-9_-]+))?\)", repl, body)
    body = body.replace("](../plots/", "](plots/").replace("](../data/", "](data/")
    body = body.replace("include ../data/", "include data/").replace("include ../plots/", "include plots/")
    return body


def build() -> str:
    parts = [HEADER]
    _, body = split_front_matter((ROOT / "index.qmd").read_text(encoding="utf-8"))
    body = rewrite_links(body).replace(" {.unnumbered}", "")
    parts.append("\n# Overview {#sec-overview .unnumbered}\n" + body.rstrip() + "\n")
    for stem in ORDER:
        meta, body = split_front_matter((CH / f"{stem}.qmd").read_text(encoding="utf-8"))
        num = stem[:2]
        head = f"\n\n# {meta['title']} {{#sec-ch{num}}}\n"
        if meta.get("subtitle"):
            head += f"\n*{meta['subtitle']}*\n"
        parts.append(head + "\n" + rewrite_links(body).strip() + "\n")
    return "".join(parts)


if __name__ == "__main__":
    out = build()
    (ROOT / "onepage.qmd").write_text(out, encoding="utf-8")
    n_links = len(re.findall(r"\]\(#sec-ch\d\d\)", out))
    leftover = re.findall(r"\]\([^)]*\.qmd[^)]*\)", out) + re.findall(r"\.\./(?:plots|data)/", out)
    print(f"onepage.qmd: {len(out.splitlines())} lines, {n_links} chapter links rewritten, "
          f"{len(leftover)} unresolved references")
    for x in leftover:
        print("  unresolved:", x)
