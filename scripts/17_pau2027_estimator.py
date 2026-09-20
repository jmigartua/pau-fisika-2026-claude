#!/usr/bin/env python3
"""What can PISA 2025 say about PAU 2027?

PISA 2025 was published on 8 September 2026 and science was its major domain. It
is the cohort that sits the PAU in 2027, so for the first time in this study a
forward-looking measurement exists. The question is whether it supports an
estimate of the 2027 Basque Física mean.

It supports one, and the estimate is worth writing down. What it does not support
is any confidence in it, and the reason is arithmetic rather than caution.

    the cohort term   PISA Basque science fell 21.0 points from 2022 to 2025,
                      which is 0.233 of a student standard deviation. Transferred
                      one-for-one — the relation figure 22 could not reject —
                      that is about 0.55 of a Física mark over the same span.

    the paper term    the standard deviation of Euskadi's own year-to-year change
                      in the Física mean, excluding 2026, is 0.855 marks. Over the
                      two years from 2025 to 2027 the 95 % band on that alone is
                      about +/- 2.4 marks.

The second is four times the first. And 2026 itself moved the mean by -1.48 in one
year on a changed paper, which is nearly three times the whole decade of cohort
drift. So the 2027 mark is not something PISA predicts; it is something the 2027
paper and its marking scheme decide, with the cohort contributing a slow nudge.

Two scenarios are therefore reported rather than one number, and the thing that
separates them is a choice not yet made.

Reads : data/analysis/pisa_link.json, data/analysis/results.json,
        data/ministry_fisica_panel.csv
Writes: plots/fig23_pau2027.(png|svg), data/analysis/pau2027_estimator.json
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
P = ROOT / "plots"

SD_PAU, SD_PISA = 2.343, 90.0   # 2.343 is the panel convention used by every other script
                                #  (2.34 until the audit of 20 September; the published
                                #   rounded values are unchanged)

pisa = json.load(open(A / "pisa_link.json", encoding="utf-8"))["science_mean"]
pv = {int(k): v for k, v in pisa["pais_vasco"].items()}
results = json.load(open(A / "results.json", encoding="utf-8"))
sd_annual = float(results["euskadi_own_change_sd_excl2026"])

panel = pd.read_csv(DATA / "ministry_fisica_panel.csv")
eus = panel[(panel.sitting == "ordinary") & (panel.phase == "specific")
            & (panel.ccaa == "País Vasco")].set_index("year")["mean"]
PAU_2025, PAU_2026 = float(eus.loc[2025]), 3.99

# The cohort term. PAU 2025 is fed by a notional PISA 2023 and PAU 2027 by PISA
# 2025; with no 2023 round, the 2022–2025 move is prorated over the two years that
# separate the two PAU cohorts.
pisa_move_sd = (pv[2025] - pv[2022]) / SD_PISA
cohort_term = pisa_move_sd * SD_PAU * (2 / 3)
# By the same alignment PAU 2026 is fed by a notional PISA 2024, one year before the
# PAU 2027 cohort, so the term to add to the 2026 mark is one third of the move
# (audit, 19 Sep 2026: the first version added the two-thirds term to both scenarios).
cohort_term_from_2026 = pisa_move_sd * SD_PAU * (1 / 3)

# The paper term, over the two years from 2025 to 2027.
paper_sd_2y = sd_annual * np.sqrt(2)
band = 1.96 * paper_sd_2y

scenarios = {
    "2027 paper like 2025's": PAU_2025 + cohort_term,
    "2027 paper like 2026's": PAU_2026 + cohort_term_from_2026,
}

fig, (ax, axb) = plt.subplots(1, 2, figsize=(12.8, 5.2),
                              gridspec_kw=dict(width_ratios=[1.3, 1.0], wspace=0.26))

# --- a. the series and the two scenarios -----------------------------------------
yrs = [y for y in eus.index]
ax.plot(yrs, [eus.loc[y] for y in yrs], color=C["violet"], lw=1.8, marker="o", ms=5,
        zorder=3, label="Euskadi Física, ordinary sitting")
ax.plot([2025, 2026], [PAU_2025, PAU_2026], color=C["red"], lw=1.8, ls=":",
        marker="o", ms=5, zorder=4)
ax.annotate("2026: 3.99", (2026, PAU_2026), textcoords="offset points",
            xytext=(-6, -14), ha="right", fontsize=7.8, color=C["red"])
# The two scenarios used to be drawn at the same x and superimposed, so they read as
# one bar with two colours of cap (audit, 20 September). They are offset now.
for (lab, val), colr, dx in zip(scenarios.items(), [C["aqua"], C["red"]], [-0.28, 0.28]):
    ax.errorbar([2027 + dx], [val], yerr=[band], fmt="D", ms=7, color=colr,
                ecolor=colr, elinewidth=1.6, capsize=5, zorder=5)
    ax.annotate("%s\n%.2f" % (lab, val), (2027 + dx, val), textcoords="offset points",
                xytext=(12, 0), va="center", fontsize=7.6, color=colr)
ax.set_xticks(range(2015, 2029, 2))
ax.set_xlim(2014.4, 2029.6)
ax.set_xlabel("Year")
ax.set_ylabel("Mean Física mark, ordinary sitting")
ax.set_title("a. Two scenarios for 2027; the error bar is the year-to-year term, not a prediction interval")
ax.legend(loc="lower left", fontsize=7.8)

# --- b. the size of each term ----------------------------------------------------
terms = [("Cohort, from PISA 2025\n(prorated 2022→2025)", abs(cohort_term), C["aqua"]),
         ("Decade of cohort drift\n(PISA 2012→2025, full)",
          abs((pv[2025] - pv[2012]) / SD_PISA * SD_PAU), C["violet"]),
         ("Everything else, one year\n(Euskadi's own year-to-year SD)", sd_annual, MUTED),
         ("Everything else, 2025→2027\n(95 % band, random-walk assumption)", band, INK2),
         ("What 2026 actually did\nin a single year", 1.48, C["red"])]
ypos = np.arange(len(terms))[::-1]
for y, (lab, val, colr) in zip(ypos, terms):
    axb.barh([y], [val], color=colr, height=0.6, lw=0)
    axb.annotate("%.2f" % val, (val, y), textcoords="offset points", xytext=(6, -3),
                 fontsize=8, color=colr)
axb.set_yticks(ypos)
axb.set_yticklabels([t[0] for t in terms], fontsize=7.6)
axb.set_xlabel("Effect on the mean Física mark")
axb.set_xlim(0, 3.1)
axb.set_title("b. Why the estimate cannot be sharpened")
axb.grid(axis="y", visible=False)
axb.annotate("the cohort signal is %.1f times smaller\nthan the band it has to be read against"
             % (band / abs(cohort_term)),
             xy=(0.97, 0.97), xycoords="axes fraction", fontsize=7.8, color=INK2,
             ha="right", va="top")

fig.text(0.005, 0.015,
         "PISA 2025 (OECD, published 8 September 2026; INEE Spanish tables, figure 2.1) "
         "gives País Vasco 458.5 in science against Spain's 477.1 — a fall of 21.0 points "
         "from 2022.\nThe cohort term converts that at one standard deviation of PISA to "
         "one of the PAU, the relation figure 22 could not reject and could not establish, "
         "prorated over the\ntwo years between the PAU cohorts. The paper term is the "
         "standard deviation of Euskadi's own year-to-year change excluding 2026. Neither "
         "scenario is a prediction.",
         fontsize=7, color=MUTED, linespacing=1.5)
fig.subplots_adjust(bottom=0.26, top=0.90, left=0.065, right=0.985)
_save(fig, "fig23_pau2027", P, dpi=200)

json.dump({
    "pisa_2025_pais_vasco": pv[2025], "pisa_2022_pais_vasco": pv[2022],
    "pisa_move_points": pv[2025] - pv[2022], "pisa_move_sd": pisa_move_sd,
    "cohort_term_marks": cohort_term,
    "cohort_term_marks_from_2026_baseline": cohort_term_from_2026,
    "decade_cohort_term_marks": (pv[2025] - pv[2012]) / SD_PISA * SD_PAU,
    "annual_paper_sd": sd_annual, "paper_band_95_2y": band,
    "noise_to_signal": band / abs(cohort_term),
    "pau_2025": PAU_2025, "pau_2026": PAU_2026,
    "scenarios": scenarios,
}, open(A / "pau2027_estimator.json", "w", encoding="utf-8"), indent=2,
    ensure_ascii=False)
print(f"  PISA Basque science 2022 {pv[2022]:.1f} -> 2025 {pv[2025]:.1f} "
      f"({pv[2025]-pv[2022]:+.1f} pts = {pisa_move_sd:+.3f} SD)")
print(f"  cohort term on PAU 2027: {cohort_term:+.2f} marks")
print(f"  paper/marking 95 % band over two years: +/- {band:.2f} marks")
print(f"  noise / signal: {band/abs(cohort_term):.1f}x")
for k, v in scenarios.items():
    print(f"  {k:26} -> {v:.2f}  [{v-band:.2f}, {v+band:.2f}]")
