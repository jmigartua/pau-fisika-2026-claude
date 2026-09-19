#!/usr/bin/env python3
"""What an externally marked instrument says about the Basque cohorts, 2006–2022.

An earlier version of this script read two PISA rounds, found the Basque top tail
thin in 2022, and concluded that this was the pandemic cohort and therefore a
one-off. Both halves of that were wrong, and reading the earlier rounds is what
showed it.

The Basque science mean runs +6 to +9 points ABOVE Spain across 2006, 2009 and
2012, and then falls 22.6 points between 2012 and 2015 while Spain falls 3.7. It
has not recovered: −9.7 against Spain in 2015, +4.1 in 2018, −5.0 in 2022. The
decade-long fall is 26 points against Spain's 12. None of that is pandemic; the
break is in the 2015 round, five years before the schools closed.

The second correction concerns the cohort alignment. PISA tests 15-year-olds who
reach the PAU two years later, and three rounds fall inside this study's PAU
window. Of those three matched cohorts, only one agrees with the PAU conditional
top-band measure:

    PISA 2015 (−9.7 vs Spain)  ->  PAU 2017 (+0.70 SD vs field)   disagree
    PISA 2018 (+4.1)           ->  PAU 2020 (−0.82 SD)            disagree
    PISA 2022 (−5.0)           ->  PAU 2024 (−0.96 SD)            agree

One of three is noise. So PISA establishes a long Basque decline that the PAU
cannot see, and fails to predict the PAU cohort by cohort. Both statements belong
in the chapter; neither on its own is the finding.

Reads : sources/pisa/pisa2015_cap2_tablas.xls  (INEE, tables 2.2 and 2.7)
        sources/pisa/pisa2018_cap2_tablas.xlsx (INEE, tables 2.3 and 2.9)
        sources/pisa/pisa2022_cap2_tablas.xlsx (INEE, tables 2.21 and 2.24)
        data/analysis/shape_locus.json
Writes: plots/fig21_pisa_link.(png|svg), data/analysis/pisa_link.json,
        data/pisa_science_series.csv
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from plot_style import C, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
A = DATA / "analysis"
SRC = ROOT / "sources" / "pisa"
P = ROOT / "plots"

F15, F18, F22 = (SRC / "pisa2015_cap2_tablas.xls",
                 SRC / "pisa2018_cap2_tablas.xlsx",
                 SRC / "pisa2022_cap2_tablas.xlsx")


def _row(path: Path, sheet: str, name: str, cols: list[int]) -> list[float]:
    d = pd.read_excel(path, sheet_name=sheet, header=None)
    hit = d[d.iloc[:, 1].astype(str).str.strip().str.startswith(name)]
    if hit.empty:
        raise KeyError(f"{name!r} not in {path.name}/{sheet}")
    return [float(hit.iloc[0, c]) for c in cols]


# Means. The 2015 report carries the whole back-series by community in table 2.7
# (2015, 2012, 2009, 2006 in that column order); 2018 and 2022 give their own round.
back_pv = _row(F15, "Tabla 2.7", "País Vasco", [2, 4, 6, 8])
back_es = _row(F15, "Tabla 2.7", "España", [2, 4, 6, 8])
mean_pv = dict(zip([2015, 2012, 2009, 2006], back_pv))
mean_es = dict(zip([2015, 2012, 2009, 2006], back_es))
mean_pv[2018] = _row(F18, "2.3", "País Vasco", [2])[0]
mean_es[2018] = _row(F18, "2.3", "España", [2])[0]
mean_pv[2022] = _row(F22, "2.21", "País Vasco", [2])[0]
mean_es[2022] = _row(F22, "2.21", "España", [2])[0]

# Proficiency levels 5+6, available by community from 2015 onwards.
top_pv, top_es = {}, {}
for yr, path, sheet in [(2015, F15, "Tabla 2.2"), (2018, F18, "2.9"), (2022, F22, "2.24")]:
    a, b = _row(path, sheet, "País Vasco", [14, 16])
    top_pv[yr] = a + b
    a, b = _row(path, sheet, "España", [14, 16])
    top_es[yr] = a + b

years = sorted(mean_pv)
series = pd.DataFrame({
    "pisa_year": years, "pau_year": [y + 2 for y in years],
    "pv_mean": [mean_pv[y] for y in years], "es_mean": [mean_es[y] for y in years],
    "gap": [mean_pv[y] - mean_es[y] for y in years],
    "pv_top56": [top_pv.get(y, np.nan) for y in years],
    "es_top56": [top_es.get(y, np.nan) for y in years],
})
series.to_csv(DATA / "pisa_science_series.csv", index=False)

vs_field = json.load(open(A / "shape_locus.json", encoding="utf-8"))[
    "euskadi_conditional_vs_field"]
matched = [(y, mean_pv[y] - mean_es[y], vs_field.get(str(y + 2)))
           for y in years if str(y + 2) in vs_field]

fig, (ax, axg, axm) = plt.subplots(1, 3, figsize=(16.6, 5.2),
                                   gridspec_kw=dict(width_ratios=[1.25, 1.0, 1.0],
                                                    wspace=0.30))

# --- a. the long series ----------------------------------------------------------
ax.plot(years, [mean_es[y] for y in years], color=INK2, lw=1.9, marker="o", ms=5,
        zorder=3, label="Spain")
ax.plot(years, [mean_pv[y] for y in years], color=C["violet"], lw=1.9, marker="o",
        ms=5, zorder=4, label="País Vasco")
ax.axvspan(2019.5, 2022.5, color=C["yellow"], alpha=0.12, lw=0, zorder=0)
ax.annotate("schools closed\n2020–21", xy=(2021, 474), fontsize=7.4,
            color="#8a6a00", ha="center")
ax.annotate("the break is here:\nPV $-22.6$, Spain $-3.7$", xy=(2016.0, 501),
            fontsize=7.8, color=C["red"], ha="left")
ax.plot([2012, 2015], [mean_pv[2012], mean_pv[2015]], color=C["red"], lw=2.6,
        alpha=0.5, zorder=2)
ax.set_xticks(years)
ax.set_xlabel("PISA round")
ax.set_ylabel("Science score")
ax.set_title("a. Basque science fell before the pandemic, not during it")
ax.legend(loc="lower left", fontsize=7.8)

# --- b. the gap ------------------------------------------------------------------
gaps = [mean_pv[y] - mean_es[y] for y in years]
axg.axhline(0, color=INK2, lw=1.0, zorder=2)
axg.bar(years, gaps, width=1.7,
        color=[C["aqua"] if g > 0 else C["red"] for g in gaps], lw=0, zorder=3)
for y, g in zip(years, gaps):
    axg.annotate("%+.1f" % g, (y, g), textcoords="offset points",
                 xytext=(0, 5 if g > 0 else -12), ha="center", fontsize=7.6,
                 color=INK2)
axg.set_xticks(years)
axg.set_xticklabels(["%d\n(PAU %d)" % (y, (y + 2) % 100) for y in years],
                    fontsize=7.0)
axg.set_ylabel("País Vasco − Spain, science score")
axg.set_title("b. A standing advantage became a deficit")

# --- c. do the matched cohorts line up? ------------------------------------------
axm.axhline(0, color=INK2, lw=0.9, zorder=1)
axm.axvline(0, color=INK2, lw=0.9, zorder=1)
for py, gap, pau in matched:
    agree = (gap < 0) == (pau < 0)
    colr = C["aqua"] if agree else C["red"]
    axm.scatter([gap], [pau], s=90, color=colr, zorder=3)
    axm.annotate("PISA %d\n→ PAU %d" % (py, py + 2), (gap, pau),
                 textcoords="offset points", xytext=(9, 6), fontsize=7.6, color=colr)
axm.annotate("agreement would put every point in the\nlower-left or upper-right quadrant;\n"
             "one of three does",
             xy=(0.97, 0.96), xycoords="axes fraction", fontsize=7.8, color=INK2,
             ha="right", va="top")
axm.set_xlim(-13, 8)
axm.set_ylim(-1.35, 1.15)
axm.set_xlabel("PISA: País Vasco − Spain, science")
axm.set_ylabel("PAU: Euskadi's conditional top-band\nshare vs the field (SD)")
axm.set_title("c. But they do not track cohort by cohort")

fig.text(0.005, 0.015,
         "PISA: INEE Spanish reports — 2015 tables 2.2 and 2.7 (which carries the "
         "2006–2015 back-series by community), 2018 tables 2.3 and 2.9, 2022 tables "
         "2.21 and 2.24.\nThe alignment in b and c is PISA year + 2: a 15-year-old in "
         "4º ESO reaches the PAU two years later. Three rounds fall inside this study's "
         "PAU window, so c has three\npoints and no correlation is computed from them.",
         fontsize=7, color=MUTED, linespacing=1.5)
fig.subplots_adjust(bottom=0.26, top=0.90, left=0.055, right=0.985)
_save(fig, "fig21_pisa_link", P, dpi=200)

json.dump({
    "alignment": "PISA year + 2 (4º ESO -> 1º Bach -> 2º Bach -> PAU)",
    "science_mean": {"pais_vasco": mean_pv, "espana": mean_es},
    "gap_pv_minus_spain": {y: mean_pv[y] - mean_es[y] for y in years},
    "top56_pct": {"pais_vasco": top_pv, "espana": top_es},
    "decade_change_2012_2022": {"pais_vasco": mean_pv[2022] - mean_pv[2012],
                                "espana": mean_es[2022] - mean_es[2012]},
    "break_2012_2015": {"pais_vasco": mean_pv[2015] - mean_pv[2012],
                        "espana": mean_es[2015] - mean_es[2012]},
    "matched_cohorts": [{"pisa_year": py, "pau_year": py + 2, "pisa_gap": gap,
                         "pau_conditional_vs_field_sd": pau,
                         "same_sign": bool((gap < 0) == (pau < 0))}
                        for py, gap, pau in matched],
}, open(A / "pisa_link.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

for y in years:
    print(f"  {y}  PV {mean_pv[y]:7.2f}  ES {mean_es[y]:7.2f}  gap {mean_pv[y]-mean_es[y]:+6.2f}"
          + (f"   top5+6 PV {top_pv[y]:.2f} ES {top_es[y]:.2f}" if y in top_pv else ""))
print(f"\n  2012->2022: PV {mean_pv[2022]-mean_pv[2012]:+.1f}, Spain {mean_es[2022]-mean_es[2012]:+.1f}")
print(f"  matched cohorts agreeing: {sum(1 for _, g, p in matched if (g < 0) == (p < 0))} of {len(matched)}")
