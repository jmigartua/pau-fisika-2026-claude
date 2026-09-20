#!/usr/bin/env python3
"""Did the papers get longer, and does that track the fall in the grade?

The 2026 Basque paper carries a deliberately expanded statement: the setter chose
to spell out every requirement and to repeat it, because the competency-style
"saber básico" was entering the examined set for the first time. That is a design
decision with a measurable footprint, and it raises a hypothesis the rest of this
study has not tested — that part of the 2026 fall is a reading load applied to a
cohort whose reading has deteriorated faster than its science.

Both halves are measurable. Paper length comes from the archived text extractions;
the cohort side is PISA reading, which for País Vasco has fallen three times as far
as PISA science over the decade.

Two measurement traps, both of which bite.

The first is language. The Basque paper is issued in Basque and in Spanish, and
the 2025 extraction is split across two files while the 2026 one is Spanish only.
Comparing pv_2025_ord (Basque, 1202 words) with pv_2026_ord (Spanish, 1946) gives
+62 %; the like-for-like Spanish comparison is 1484 to 1946, or +31 %. Only the
second is a fact about the paper.

The second is structure. Communities differ in how much choice they offer, so a
paper that prints eight questions for a student who answers five is longer on the
page without being longer to read. Raw length is therefore NOT compared across
communities; only each community's change against itself is.

Reads : sources/exams/*.txt, data/analysis/regions_2026_vs_2025.csv,
        data/exam_coding_2025_2026.csv, sources/pisa/*
Writes: plots/fig24_reading_load.(png|svg), data/analysis/reading_load.json,
        data/exam_length_2025_2026.csv
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from plot_style import C, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
A = DATA / "analysis"
EX = ROOT / "sources" / "exams"
SRC = ROOT / "sources" / "pisa"
P = ROOT / "plots"

# Explicit file map rather than a glob: the archive holds reserve papers, corrector
# documents, second models and language variants, and picking the wrong member is
# exactly the error described in the docstring. Where a community publishes in two
# languages the Spanish text is used in BOTH years so the change is like-for-like.
PAPERS = {
    "Andalucía":                ("and_2025_ord", "and_2026_ord"),
    "Asturias (Principado de)": ("ast_2025_ord", "ast_2026_ord"),
    "Canarias":                 ("can_2025_ord", "can_2026_ord"),
    "Cataluña":                 ("cat_2025_ord", "cat_2026_ord"),
    "Extremadura":              ("ext_2025_ord", "ext_2026_ord"),
    "Madrid (Comunidad de)":    ("mad_2025_ord", "mad_2026_ord"),
    "País Vasco":               ("pv_2025_ord_es", "pv_2026_ord"),   # Spanish, both
    "Comunitat Valenciana":     ("val_2025_ord", "val_2026_ord"),
}

# Front matter that is not statement text: rubrics, timing, constant tables. Removing
# it is crude and is reported both ways so the reader can see whether it matters.
BOILER = re.compile(
    r"(INSTRUCCIONES|AZTERKETARAKO|CALIFICACI[ÓO]N|TIEMPO|DATOS|CONSTANTES|"
    r"Responda|Jarraibide|OPTATIVIDAD|ESTRUCTURA)", re.I)


def statement_only(text: str, stem: str) -> str:
    """Keep the examination statement only (audit of 19 Sep 2026).

    Three archived files carry text that is not the statement the candidate reads:
    the Madrid PDFs embed the marking criteria and full worked solutions after the
    paper (about 70 % of their words); the Valencia PDFs are bilingual, Spanish
    pages first then the Valencian repeat; the EHU Spanish files open with the
    Basque instruction block before the Spanish one. Each is cut at its marker.
    """
    if stem.startswith("mad_"):
        text = text.split("CRITERIOS ESPECÍFICOS", 1)[0]
    elif stem.startswith("val_"):
        parts = re.split(r"PROVA D[’']ACC[ÉE]S", text)
        text = parts[1] if len(parts) > 2 else text          # the Spanish half only
    elif stem.startswith("pv_"):
        parts = text.split("INSTRUCCIONES PARA EL EXAMEN", 1)
        text = parts[1] if len(parts) == 2 else text          # drop the Basque instruction block
    return text


def words(path: Path, strip_boiler: bool = False, raw: bool = False) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not raw:
        text = statement_only(text, path.stem)
    if strip_boiler:
        text = "\n".join(l for l in text.splitlines() if not BOILER.search(l))
    return len(re.findall(r"\b[\wáéíóúüñÁÉÍÓÚÜÑ]+\b", text))


rows = []
for ccaa, (f25, f26) in PAPERS.items():
    p25, p26 = EX / f"{f25}.txt", EX / f"{f26}.txt"
    if not (p25.exists() and p26.exists()):
        print(f"  MISSING text for {ccaa}: {f25} / {f26}")
        continue
    rows.append({"ccaa": ccaa, "file_2025": f25, "file_2026": f26,
                 "words_2025": words(p25), "words_2026": words(p26),
                 "words_2025_nb": words(p25, True), "words_2026_nb": words(p26, True),
                 "words_2025_raw": words(p25, raw=True), "words_2026_raw": words(p26, raw=True)})
length = pd.DataFrame(rows)
length["len_change"] = 100 * (length.words_2026 / length.words_2025 - 1)
length["len_change_nb"] = 100 * (length.words_2026_nb / length.words_2025_nb - 1)
length["len_change_raw"] = 100 * (length.words_2026_raw / length.words_2025_raw - 1)

reg = pd.read_csv(A / "regions_2026_vs_2025.csv")[["ccaa", "delta"]]
length = length.merge(reg, on="ccaa", how="left")
length.to_csv(DATA / "exam_length_2025_2026.csv", index=False)

ok = length.dropna(subset=["delta"])
r_len = stats.pearsonr(ok.len_change, ok.delta)
r_len_nb = stats.pearsonr(ok.len_change_nb, ok.delta)
r_sp = stats.spearmanr(ok.len_change, ok.delta)
r_raw = stats.pearsonr(ok.len_change_raw, ok.delta)          # the pre-audit count, for the record
r_excl_pv = stats.pearsonr(ok[ok.ccaa != "País Vasco"].len_change, ok[ok.ccaa != "País Vasco"].delta)

# Is length just restating the competency coding of chapter 11?
coding = pd.read_csv(DATA / "exam_coding_2025_2026.csv")
comp = (coding.groupby(["ccaa", "year"])
        .apply(lambda g: float((g.competency * g.points).sum() / g.points.sum() * 100),
               include_groups=False)
        .unstack())
comp_delta = (comp[2026] - comp[2025]).rename("d_competency").reset_index()
# The coding file uses the short community names and the length table the long ones,
# so a plain merge silently dropped Asturias and Madrid and computed the collinearity
# on six papers instead of eight (found in the audit of 20 September).
_LONG = {"Asturias": "Asturias (Principado de)", "Madrid": "Madrid (Comunidad de)"}
comp_delta["ccaa"] = comp_delta.ccaa.replace(_LONG)
ok = ok.merge(comp_delta, on="ccaa", how="left")
_c = ok.dropna(subset=["d_competency"])
r_collin = stats.pearsonr(_c.len_change, _c.d_competency)

# PISA reading, the cohort side. There is no 2018 point: the Spanish PISA 2018
# report carries mathematics and science only, because the OECD withheld Spain's
# 2018 reading results over anomalous response patterns. An earlier version of this
# script read table 2.1 of that workbook as reading; it is mathematics, and the
# resulting "reading" series showed a spurious Basque advantage of +17.8 in 2018.
def pisa_row(path, sheet, name, col, keycol=1):
    d = pd.read_excel(path, sheet_name=sheet, header=None)
    hit = d[d.iloc[:, keycol].astype(str).str.strip().str.startswith(name)]
    return float(hit.iloc[0, col])


reading = {
    2015: {"pv": pisa_row(SRC / "pisa2015_cap2_tablas.xls", "Tabla 2.11", "País Vasco", 2),
           "es": pisa_row(SRC / "pisa2015_cap2_tablas.xls", "Tabla 2.11", "España", 2)},
    2022: {"pv": pisa_row(SRC / "pisa2022_cap2_tablas.xlsx", "2.20", "País Vasco", 2),
           "es": pisa_row(SRC / "pisa2022_cap2_tablas.xlsx", "2.20", "España", 2)},
    2025: {"pv": pisa_row(SRC / "pisa2025_cap2_tablas.xlsx", "Figura 2.14", "País Vasco", 1, 0),
           "es": pisa_row(SRC / "pisa2025_cap2_tablas.xlsx", "Figura 2.14", "España", 1, 0)},
}
science = json.load(open(A / "pisa_link.json", encoding="utf-8"))["science_mean"]
sci_pv = {int(k): v for k, v in science["pais_vasco"].items()}

fig, (axl, axr) = plt.subplots(1, 2, figsize=(12.8, 5.2),
                               gridspec_kw=dict(width_ratios=[1.0, 1.05], wspace=0.26))

# --- a. paper length against the change in the grade -----------------------------
axl.axhline(0, color=INK2, lw=0.9, zorder=1)
axl.axvline(0, color=INK2, lw=0.9, zorder=1)
for _, r in ok.iterrows():
    colr = C["violet"] if r.ccaa == "País Vasco" else MUTED
    axl.scatter([r.len_change], [r.delta], s=70 if colr == C["violet"] else 44,
                color=colr, zorder=3)
    # Canarias (+13.4, -0.83) and Extremadura (+19.5, -0.82) printed on top of each
    # other, and the fitted line ran through the Valencian label (audit, 20 September).
    _off = {"Canarias": (-8, -4), "Extremadura": (8, -4), "Comunitat Valenciana": (7, -11),
            "Cataluña": (7, 4), "Andalucía": (7, -11), "Madrid": (-8, 5),
            "Asturias": (7, 4), "País Vasco": (-9, 4)}
    _name = r.ccaa.split(" (")[0]
    dx, dy = _off.get(_name, (7, 4))
    axl.annotate(_name, (r.len_change, r.delta), textcoords="offset points",
                 xytext=(dx, dy), fontsize=7.2, color=colr,
                 ha="right" if dx < 0 else "left")
xs = np.linspace(ok.len_change.min() - 4, ok.len_change.max() + 4, 40)
axl.plot(xs, np.polyval(np.polyfit(ok.len_change, ok.delta, 1), xs),
         color=C["red"], lw=1.5, zorder=2)
axl.annotate("Pearson $r = %+.2f$ ($p = %.3f$, $n = %d$)\nSpearman $\\rho = %+.2f$ "
             "($p = %.3f$)\nboilerplate stripped: $r = %+.2f$"
             % (r_len[0], r_len[1], len(ok), r_sp.statistic, r_sp.pvalue, r_len_nb[0]),
             xy=(0.97, 0.96), xycoords="axes fraction", fontsize=7.8, color=INK2,
             ha="right", va="top")
axl.set_xlabel("Change in paper length, 2025 → 2026 (%)")
axl.set_ylabel("Change in the mean Física mark")
axl.set_title("a. Longer paper, larger fall ($r = %+.2f$)" % r_len[0])

# --- b. the cohort side: reading against science ---------------------------------
yrs_r = sorted(reading)
axr.plot(yrs_r, [reading[y]["pv"] for y in yrs_r], color=C["red"], lw=1.9,
         marker="o", ms=6, zorder=4, label="País Vasco, reading")
axr.plot(yrs_r, [reading[y]["es"] for y in yrs_r], color=C["red"], lw=1.3,
         marker="o", ms=4, alpha=0.45, ls="--", zorder=3, label="Spain, reading")
yrs_s = [y for y in sorted(sci_pv) if y >= 2015]
axr.plot(yrs_s, [sci_pv[y] for y in yrs_s], color=C["violet"], lw=1.9, marker="s",
         ms=6, zorder=4, label="País Vasco, science")
axr.annotate("reading $-%.0f$ points\nscience $-%.0f$ points"
             % (reading[2015]["pv"] - reading[2025]["pv"],
                sci_pv[2015] - sci_pv[2025]),
             xy=(2021.0, 432), fontsize=7.8, color=INK2)
axr.set_xticks(yrs_s)
axr.set_xlabel("PISA round")
axr.set_ylabel("PISA score")
axr.set_title("b. Basque reading fell three times as far as science")
axr.legend(loc="lower left", fontsize=7.6)

fig.text(0.005, 0.015,
         "Paper length: word counts of the archived text extractions of the ordinary "
         "papers, Spanish version in both years where a community publishes in two "
         "languages.\nOnly each community's change against itself is used: structures "
         "differ, so raw length is not comparable across communities. Length and the "
         "competency measure of\nchapter 11 correlate at r = %+.2f, so they are NOT "
         "independent and cannot be separated with eight points — length is better read "
         "as a cleaner measurement of\nthe same change than as a second cause. PISA "
         "reading: INEE tables 2.11 (2015), 2.20 (2022), figure 2.14 (2025); "
         "there is no 2018 point because Spain's PISA 2018 reading was withheld." % r_collin[0],
         fontsize=7, color=MUTED, linespacing=1.5)
fig.subplots_adjust(bottom=0.26, top=0.90, left=0.075, right=0.985)
_save(fig, "fig24_reading_load", P, dpi=200)

json.dump({
    "papers": PAPERS,
    "length_table": length.to_dict(orient="records"),
    "length_vs_grade": {"pearson_r": r_len[0], "pearson_p": r_len[1],
                        "spearman_rho": float(r_sp.statistic),
                        "spearman_p": float(r_sp.pvalue),
                        "pearson_r_boilerplate_stripped": r_len_nb[0], "n": int(len(ok)),
                        "pearson_r_raw_files_pre_audit": r_raw[0], "pearson_p_raw_files_pre_audit": r_raw[1],
                        "pearson_r_excl_pais_vasco": r_excl_pv[0], "pearson_p_excl_pais_vasco": r_excl_pv[1]},
    "collinearity_with_competency_change": {"r": r_collin[0], "p": r_collin[1],
                                            "n": int(len(_c))},
    "pisa_reading": reading,
    "pais_vasco_decade_fall": {"reading": reading[2015]["pv"] - reading[2025]["pv"],
                               "science": sci_pv[2015] - sci_pv[2025]},
}, open(A / "reading_load.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

print(length[["ccaa", "words_2025", "words_2026", "len_change", "delta"]].to_string(index=False))
print(f"\n  length vs grade change: r = {r_len[0]:+.3f} (p = {r_len[1]:.3f}), "
      f"rho = {r_sp.statistic:+.3f} (p = {r_sp.pvalue:.3f}), n = {len(ok)}")
print(f"  boilerplate stripped:   r = {r_len_nb[0]:+.3f}")
print(f"  collinearity with the competency change: r = {r_collin[0]:+.3f}")
print(f"  PISA País Vasco 2015->2025: reading {reading[2025]['pv']-reading[2015]['pv']:+.1f}, "
      f"science {sci_pv[2025]-sci_pv[2015]:+.1f}")
