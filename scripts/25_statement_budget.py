#!/usr/bin/env python3
"""Reading load item by item, and the 2027 statement-length target.

Chapter 6 measures reading load one paper at a time: the whole Basque statement grew
45 % between 2025 and 2026, which is the strongest cross-community correlate of the
grade change in this study and also the weakest causally.  A paper-level number cannot
say WHERE the growth is, and "where" is the only form in which the finding can be acted
on, because a paper is written one problem at a time.

This script measures each item's statement separately in both Basque papers, on one
convention, and places the 2027 target of the coordination presentation against them.

WHAT IS COUNTED.  The Spanish statement of each item, from its label to the next: the
context, the data, the sub-task text.  Not counted: the paper's instruction header, the
constants table, the block headings, the repeated page furniture, and the point weights
in parentheses — the last because the coordination's own count excludes them and the
two counts have to be comparable.  The difference between this convention and the
whole-file convention of `18_reading_load.py` is exactly that furniture, and both are
reported so the chapter's +45 % remains traceable.

THE TARGET.  The presentation of 18 September 2026 sets a band of 150-175 words per
statement, mean 162, which for a paper of six statements is 900-1050 words read and
600-700 answered.  Chapter 6's own design lever, derived from the cross-community
length data rather than from the papers, recommends 1300-1400 words on the whole-file
convention.  The two are converted into each other here; that they agree is a fact
about the two derivations, not a corroboration of either.

Reads : sources/exams/pv_2025_ord_es.txt, sources/exams/pv_2026_ord.txt,
        data/analysis/reading_load.json
Writes: data/analysis/statement_budget.json, data/analysis/statement_budget.csv,
        data/tables/statement_budget.md, plots/fig29_statement_budget.(png|svg)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

from plot_style import T, C, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "sources" / "exams"
A = ROOT / "data" / "analysis"
TABLES = ROOT / "data" / "tables"
PLOTS = ROOT / "plots"

# The 2027 band as the coordination presentation sets it (slide 5).
BAND_LO, BAND_HI, BAND_MEAN = 150, 175, 162

# Which items a candidate actually reads and answers, by year.
# 2025: seven statements printed, four answered (A obligatory; B, C, D one of two).
# 2026: six printed, four answered (1 and 2 obligatory; 3 and 4 one of two).
ANSWERED = {2025: [("A1",), ("B1", "B2"), ("C1", "C2"), ("D1", "D2")],
            2026: [("A1",), ("B1",), ("C1", "C2"), ("D1", "D2")]}

_PAGE = re.compile(r"UNIBERTSITATEAN.*?FÍSICA", re.S)
# The watermark letters are interposed inside at least one weight in the 2026 file
# ("(0.50   U    puntos)"), so the pattern has to tolerate them or it undercounts.
_WEIGHT = re.compile(r"\(\s*[\d.,]+[\s\n]*(?:U|EH)?[\s\n]*puntos?\s*\)")
_STRAY = re.compile(r"(?<![A-Za-zÀ-ÿ])(U|EH)(?![A-Za-zÀ-ÿ])")   # watermark letters


def statements(path: Path) -> dict[str, str]:
    """Split a paper's Spanish text into its item statements."""
    t = path.read_text(encoding="utf-8")
    t = _PAGE.sub(" ", t)
    t = _STRAY.sub(" ", t)
    marks = [(m.group(1), m.start()) for m in re.finditer(r"^\s*([A-D]\d)\.-", t, re.M)]
    out = {}
    for i, (label, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(t)
        body = t[start:end]
        body = re.sub(r"^\s*[A-D]\d\.-\s*", "", body)
        # A trailing block heading belongs to the next block, not to this statement.
        # Two traps, both found by the audit of 20 September: the plural heading
        # "BLOQUES C y D: Problemas" does not match a singular pattern, and cutting at
        # the colon leaves the words before it ("BLOQUES B, C y D: Problemas / (Cada
        # BLOQUE consta de 2 problemas...) / 2. Problema,") inside the previous item.
        # Cut at the first character of the apparatus instead.
        body = re.split(r"BLOQUES?\s+[A-D]\b", body)[0]
        out[label] = body
    return out


def wc(s: str) -> int:
    return len(re.findall(r"\S+", s))


def main() -> None:
    rows = []
    per_year = {}
    for year, fname in ((2025, "pv_2025_ord_es.txt"), (2026, "pv_2026_ord.txt")):
        st = statements(EX / fname)
        per_year[year] = {}
        for label, body in st.items():
            with_w = wc(body)
            no_w = wc(_WEIGHT.sub(" ", body))
            per_year[year][label] = no_w
            rows.append(dict(year=year, item=label, words=no_w, words_with_weights=with_w))

    # what a candidate reads, and what a candidate answers
    def read_answer(year):
        d = per_year[year]
        read = sum(d[i] for grp in ANSWERED[year] for i in grp if i in d)
        # answered: the cheapest and dearest route through the options
        lo = sum(min(d[i] for i in grp if i in d) for grp in ANSWERED[year])
        hi = sum(max(d[i] for i in grp if i in d) for grp in ANSWERED[year])
        return read, lo, hi

    r25, lo25, hi25 = read_answer(2025)
    r26, lo26, hi26 = read_answer(2026)

    # The 2025 paper prints its constants inside the statements that need them and the
    # 2026 paper moved them to a single table.  That migration is pure layout and it
    # crosses the statement/furniture line, so it is measured rather than left implicit.
    _t25 = (EX / "pv_2025_ord_es.txt").read_text(encoding="utf-8")
    _t26 = (EX / "pv_2026_ord.txt").read_text(encoding="utf-8")
    _datos = re.compile(r"Datos\s*:(?:[^\n]*\n){0,3}")
    n_datos_25 = len(re.findall(r"Datos\s*:", _t25))
    n_datos_26 = len(re.findall(r"Datos\s*:", _t26))
    datos_words_25 = sum(wc(_STRAY.sub(" ", m.group())) for m in _datos.finditer(_t25))

    # ---- the furniture, broken out --------------------------------------------
    # Everything a candidate's eye passes over that is not a question: the bilingual
    # title block and instructions, the block headings, and — new in 2026 — a printed
    # weight on every sub-task.  It is worth separating because it is the part that can
    # be cut without touching a single question.
    furniture = {}
    for year, fname in ((2025, "pv_2025_ord_es.txt"), (2026, "pv_2026_ord.txt")):
        raw = (EX / fname).read_text(encoding="utf-8")
        first = re.search(r"^\s*A1\.-", raw, re.M).start()
        head = raw[:first]
        m = re.search(r"INSTRUCCIONES PARA EL EXAMEN", head)
        heads = re.findall(r"BLOQUE\s+[A-D][^\n]*\n(?:[^\n]*\n){0,2}", raw)
        weights = _WEIGHT.findall(raw)
        furniture[year] = dict(
            preamble_total=wc(head),
            preamble_basque_and_title=wc(head[:m.start()]) if m else None,
            preamble_spanish=wc(head[m.start():]) if m else None,
            block_headings=sum(wc(x) for x in heads),
            n_weight_annotations=len(weights),
            weight_words=sum(wc(x) for x in weights),
        )

    # Conversion between this convention and the whole-file one of script 18.
    # The two must not be differenced directly: script 18 counts word tokens and this
    # script counts whitespace runs, so "H=23222" is two words there and one here.
    # The furniture is therefore measured here, on this script's own tokenisation, and
    # script 18's figure is carried alongside for the chapter's +45 % rather than
    # subtracted from.
    rl = json.loads((A / "reading_load.json").read_text(encoding="utf-8"))
    whole = {r["ccaa"]: r for r in rl["length_table"]}["País Vasco"]
    def whole_here(fname):
        raw = (EX / fname).read_text(encoding="utf-8")
        raw = _PAGE.sub(" ", raw)
        raw = _STRAY.sub(" ", raw)
        return wc(raw)
    whole_25_here, whole_26_here = (whole_here("pv_2025_ord_es.txt"),
                                    whole_here("pv_2026_ord.txt"))
    overhead_25 = whole_25_here - r25
    overhead_26 = whole_26_here - r26

    n26 = len(per_year[2026])
    target = dict(
        band=[BAND_LO, BAND_HI], mean=BAND_MEAN, n_statements=n26,
        read_lo=BAND_LO * n26, read_hi=BAND_HI * n26, read_mean=BAND_MEAN * n26,
        answered_lo=BAND_LO * 4, answered_hi=BAND_HI * 4, answered_mean=BAND_MEAN * 4,
        # what the target is worth on the whole-file convention the chapter uses,
        # assuming the 2026 furniture is unchanged
        whole_file_equivalent=BAND_MEAN * n26 + overhead_26,
        chapter_lever_band=[1300, 1400],
    )

    out = dict(
        convention=("Spanish statement of each item, page furniture and point weights "
                    "removed; the whole-file convention of script 18 additionally "
                    "counts the instruction header, the constants table, the block "
                    "headings and the weights"),
        items={str(y): per_year[y] for y in per_year},
        paper=dict(
            p2025=dict(read=r25, answered_lo=lo25, answered_hi=hi25,
                       n_printed=len(per_year[2025]), whole_file=whole["words_2025"],
                       whole_here=whole_25_here, furniture=overhead_25),
            p2026=dict(read=r26, answered_lo=lo26, answered_hi=hi26,
                       n_printed=len(per_year[2026]), whole_file=whole["words_2026"],
                       whole_here=whole_26_here, furniture=overhead_26),
            growth_statements_pct=(r26 - r25) / r25 * 100,
            growth_whole_file_pct=whole["len_change"],
        ),
        biggest_item=dict(
            label="B1", words=per_year[2026]["B1"],
            share_of_read=per_year[2026]["B1"] / r26 * 100,
            share_of_marks=25.0,
            note=("the electromagnetic problem, the one the coordination expanded "
                  "deliberately because the saber básico entered the competency "
                  "paradigm for the first time"),
        ),
        furniture=furniture,
        whole_file_same_tokenisation=dict(y2025=whole_25_here, y2026=whole_26_here,
                                          note=("counted here with this script's own "
                                                "whitespace tokenisation so that the "
                                                "furniture is a difference of like "
                                                "with like; script 18's word-token "
                                                "counts are 1335 and 1940")),
        constants_migration=dict(
            datos_blocks_2025=n_datos_25, datos_blocks_2026=n_datos_26,
            words_in_2025_statements=datos_words_25,
            note=("the 2025 paper prints its constants inside the statements that need "
                  "them; the 2026 paper moved them to one table for the whole paper, "
                  "which this convention counts as furniture.  About that many words "
                  "therefore move from 'statement' to 'furniture' between the years "
                  "for reasons of layout alone, which inflates both the statement "
                  "growth and the furniture growth reported here")),
        target_2027=target,
        four_versions_b1=dict(
            source="coordination presentation, 18 September 2026, slides 8-11",
            forward_ladder={"0 habitual (telegraphic)": 90, "1 competencial": 178,
                            "2 desglosado": 244, "3 as issued 2026": 408},
            reverse_ladder={"habitual with figure": 113, "habitual with text": 153,
                            "competencial ideal": 154,
                            "competencial ideal, drawing asked": 170,
                            "sin narrativa": 287, "as issued 2026": 408},
            note=("the two ladders are separate reconstructions and share only their "
                  "endpoint; the intermediate rungs differ by 20 to 45 words because "
                  "the wording at each rung is not the same"),
        ),
    )
    (A / "statement_budget.json").write_text(json.dumps(out, indent=2, ensure_ascii=False),
                                             encoding="utf-8")

    import csv
    with (A / "statement_budget.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["year", "item", "words", "words_with_weights"])
        w.writeheader()
        w.writerows(rows)

    # ---- table -----------------------------------------------------------------
    L = ["| Paper | Statements printed | Words read | Words answered | Longest statement | "
         "Furniture | Whole paper |", "|---|---:|---:|---:|---:|---:|---:|"]
    for y, d in (("2025", out["paper"]["p2025"]), ("2026", out["paper"]["p2026"])):
        longest = max(per_year[int(y)].items(), key=lambda kv: kv[1])
        L.append(f"| EHU {y} | {d['n_printed']} | {d['read']} | "
                 f"{d['answered_lo']}–{d['answered_hi']} | {longest[0]}, {longest[1]} | "
                 f"{d['furniture']} | {d['whole_here']} |")
    L.append(f"| **Target 2027** | {n26} | {target['read_lo']}–{target['read_hi']} | "
             f"{target['answered_lo']}–{target['answered_hi']} | "
             f"{BAND_LO}–{BAND_HI} each | (unchanged) | "
             f"≈ {target['whole_file_equivalent']:.0f} |")
    L += ["", "Statement words only, weights and page furniture removed; every column "
          "on one tokenisation, so that furniture plus statements equals the whole "
          "paper. \"Words read\" counts every statement a candidate must read, options "
          "included; \"words answered\" the cheapest and dearest route through the "
          "options. Furniture is the instruction header, the constants table, the "
          "block headings and the printed weights. The whole-paper figures of "
          "@fig-reading are 1 335 and 1 940 on a word-token count rather than this "
          "whitespace one, and the $+45$ % of that figure is computed on it "
          "throughout. The target row assumes the 2026 furniture unchanged. File: "
          "`data/analysis/statement_budget.csv`."]
    (TABLES / "statement_budget.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- figure ----------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.5))

    # (a) item by item, both years, against the band
    ax = axes[0]
    items = ["A1", "B1", "B2", "C1", "C2", "D1", "D2"]
    y = np.arange(len(items))[::-1]
    w25 = [per_year[2025].get(i, 0) for i in items]
    w26 = [per_year[2026].get(i, 0) for i in items]
    ax.barh(y + 0.19, w25, height=0.36,
            color=[C["red"] if i == "A1" else MUTED for i in items])
    ax.barh(y - 0.19, w26, height=0.36,
            color=[C["red"] if i in ("A1", "B1") else C["blue"] for i in items])
    ax.axvspan(BAND_LO, BAND_HI, color=C["aqua"], alpha=0.13, zorder=0)
    ax.text((BAND_LO + BAND_HI) / 2, len(items) - 0.35, T("target 2027"), ha="center",
            fontsize=8, color=C["aqua"])
    for yy, v in zip(y - 0.19, w26):
        if v:
            ax.text(v + 6, yy, str(v), va="center", fontsize=8, color=INK2)
    ax.set_yticks(y); ax.set_yticklabels(items, fontsize=9)
    ax.set_xlim(0, 460); ax.set_ylim(-0.8, len(items) - 0.2)
    ax.set_xlabel(T("statement words (weights and furniture removed)"))
    # explicit proxies: the bars are coloured by item, so the automatic legend would
    # pick up whichever colour was set last.
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=MUTED, label="2025"),
                       Patch(color=C["blue"], label="2026"),
                       Patch(color=C["red"], label=T("competency item"))],
              loc="lower right", fontsize=8)
    ax.set_title(T("(a) The long item is the competency item\n")
                 + T("2025: A1, 423 words. 2026: B1, 413"), loc="left")
    ax.grid(axis="y", visible=False)

    # (b) the two ladders for B1
    ax = axes[1]
    fwd = out["four_versions_b1"]["forward_ladder"]
    rev = [(T("habitual\n+ figure"), 113), (T("competencial\nideal"), 154),
           (T("sin\nnarrativa"), 287), (T("2026, as\nissued"), 408)]
    xf = np.arange(4)
    ax.plot(xf, list(fwd.values()), "o-", color=MUTED, lw=1.6,
            label=T("slide 8 (forward)"))
    ax.plot(xf, [v for _, v in rev], "s--", color=C["violet"], lw=1.6,
            label=T("slides 9–11 (reverse)"))
    # the two ladders nearly touch at the competency rung (178 against 154), so that
    # one label is pushed sideways rather than down.
    _off = {1: (26, -4)}
    for i_, (x_, v) in enumerate(zip(xf, list(fwd.values()))):
        ax.annotate(str(v), (x_, v), textcoords="offset points",
                    xytext=_off.get(i_, (0, -16)), ha="center", fontsize=8, color=MUTED)
    _offr = {1: (-26, -4)}
    for i_, (x_, (_, v)) in enumerate(zip(xf, rev)):
        ax.annotate(str(v), (x_, v), textcoords="offset points",
                    xytext=_offr.get(i_, (0, 9)), ha="center", fontsize=8,
                    color=C["violet"])
    ax.axhspan(BAND_LO, BAND_HI, color=C["aqua"], alpha=0.13, zorder=0)
    ax.text(0.05, (BAND_LO + BAND_HI) / 2, T("target band"), fontsize=8, color=C["aqua"],
            va="center")
    ax.set_xticks(xf)
    ax.set_xticklabels([T("habitual"), T("competencial"), T("broken out"), "2026"], fontsize=8.5)
    ax.set_ylim(40, 470)
    ax.set_ylabel(T("statement words"))
    ax.legend(loc="upper left", fontsize=8)
    ax.set_title(T("(b) Two reconstructions of B1\nsame endpoint, different rungs"),
                 loc="left")
    ax.grid(axis="x", visible=False)

    # (c) the paper budget
    ax = axes[2]
    cats = [T("2025\nas issued"), T("2026\nas issued"), T("2027\ntarget")]
    read = [r25, r26, target["read_mean"]]
    ansl = [lo25, lo26, target["answered_mean"]]
    x = np.arange(3)
    ax.bar(x - 0.18, read, width=0.34, color=MUTED, label=T("read (options included)"))
    ax.bar(x + 0.18, ansl, width=0.34, color=C["blue"], label=T("answered (four problems)"))
    ax.bar(x[2] - 0.18, target["read_mean"], width=0.34, color=C["aqua"])
    ax.bar(x[2] + 0.18, target["answered_mean"], width=0.34, color=C["aqua"], alpha=0.65)
    for xx, v in zip(x - 0.18, read):
        ax.text(xx, v + 22, f"{v:.0f}", ha="center", fontsize=9, color=INK)
    for xx, v in zip(x + 0.18, ansl):
        ax.text(xx, v + 22, f"{v:.0f}", ha="center", fontsize=9, color=INK)
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=8.5)
    ax.set_ylim(0, 1750)
    ax.set_ylabel(T("statement words"))
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title(T("(c) The 2027 budget\n{a} → {b} read, a cut of {c:.0f} per cent")
                 .format(a=r26, b=target["read_mean"],
                         c=100 * (1 - target["read_mean"] / r26)), loc="left")
    ax.grid(axis="x", visible=False)

    fig.suptitle(T("Figure 29 — Where the reading is, and what the 2027 target costs"),
                 x=0.005, ha="left", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _save(fig, "fig29_statement_budget", PLOTS)

    print("2025 items:", per_year[2025])
    print("2026 items:", per_year[2026])
    print(f"read 2025 {r25} (answered {lo25}-{hi25}); read 2026 {r26} "
          f"(answered {lo26}-{hi26}); growth {out['paper']['growth_statements_pct']:+.1f} %")
    print(f"whole file, same tokenisation: {whole_25_here} / {whole_26_here}; "
          f"furniture {overhead_25} / {overhead_26} "
          f"(script 18 word tokens: {whole['words_2025']} / {whole['words_2026']})")
    print(f"constants inside 2025 statements: {n_datos_25} blocks, {datos_words_25} "
          f"words; 2026 blocks: {n_datos_26}")
    print(f"B1 {per_year[2026]['B1']} words = "
          f"{out['biggest_item']['share_of_read']:.1f} % of what is read, for 25 % of the marks")
    for y in (2025, 2026):
        f_ = furniture[y]
        print(f"furniture {y}: preamble {f_['preamble_total']} "
              f"(ES {f_['preamble_spanish']}), block headings {f_['block_headings']}, "
              f"{f_['n_weight_annotations']} weights = {f_['weight_words']} words")
    print(f"target: read {target['read_lo']}-{target['read_hi']} "
          f"(mean {target['read_mean']}), whole-file equivalent "
          f"{target['whole_file_equivalent']:.0f} against the chapter's 1300-1400")


if __name__ == "__main__":
    main()
