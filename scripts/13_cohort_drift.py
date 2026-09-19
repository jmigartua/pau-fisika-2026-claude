#!/usr/bin/env python3
"""Are the cohorts arriving less prepared, year after year?

The intuition is specific and testable: Física is a voluntary subject whose
examined population grew by 59 % over this decade, from 30,839 to 49,010, and a
subject that recruits more widely should recruit further down the distribution.
If so, part of what 2025 and 2026 show would be a slow drift rather than an event.

Three tests, and the honest answer is "a little, and the data cannot say more".

1. The pre-COVID trend. 2015–2019 falls at −0.071 points a year (p = 0.058,
   R² = 0.75). Extrapolated to 2025 it predicts 5.20; the actual 2025 mean is
   5.67, +0.47 above it. The early decline did not continue at that rate.
2. Dilution within regions. Comparing each community with itself, years in which
   more of its students sat the paper are years with a lower mean: r = −0.212,
   p = 0.032 across the non-plateau years. Real, but it accounts for about 4 % of
   the within-region variance.
3. Shape. The conditional top-band share shows no significant trend at all
   (−0.0029 a year, p = 0.082), so whatever is drifting is not obviously the
   composition of the top.

The deeper problem is visible in panel a: the five years best placed to measure a
decade-long drift are exactly the plateau years, and they are unusable for it. Six
year-points remain. That is why nothing here reaches significance, and it is a
better reason to withhold judgement than any of the individual p-values.

Reads : data/ministry_fisica_panel.csv, data/ministry_fisica_distr.csv
Writes: plots/fig20_cohort_drift.(png|svg), data/analysis/cohort_drift.json
"""
from __future__ import annotations

import json
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
P = ROOT / "plots"
PLATEAU = [2020, 2021, 2022, 2023, 2024]

panel = pd.read_csv(DATA / "ministry_fisica_panel.csv")
distr = pd.read_csv(DATA / "ministry_fisica_distr.csv")
m = (panel[(panel.sitting == "ordinary") & (panel.phase == "specific")]
     .merge(distr[(distr.sitting == "ordinary") & (distr.phase == "specific")],
            on=["ccaa", "year", "sitting", "phase"]))
m = m[~m.ccaa.isin(["Total", "Estado"])].dropna(
    subset=["mean", "pass_pct", "presented"]).copy()
m["top"] = m["[8-9)"] + m["[9-10]"]
m["ratio"] = m.top / m.pass_pct
nc = m[~m.year.isin(PLATEAU)]

nat = m.groupby("year")["mean"].mean()
presented = m.groupby("year").presented.sum()
pre = nat.loc[2015:2019]
tr = stats.linregress(pre.index, pre.values)
proj_2025 = tr.intercept + tr.slope * 2025

# Within-region dilution: both variables expressed as deviations from the region's
# own average, so the comparison is a community against itself rather than against
# other communities, which differ for reasons that have nothing to do with size.
m["d_presented"] = m.groupby("ccaa").presented.transform(lambda s: (s - s.mean()) / s.std())
m["d_mean"] = m.groupby("ccaa")["mean"].transform(lambda s: s - s.mean())
nc = m[~m.year.isin(PLATEAU)]
dil = stats.pearsonr(nc.d_presented, nc.d_mean)
dil_fit = np.polyfit(nc.d_presented, nc.d_mean, 1)

ratio_by_year = nc.groupby("year").ratio.mean()
ratio_tr = stats.linregress(ratio_by_year.index, ratio_by_year.values)

fig, (ax, axd) = plt.subplots(1, 2, figsize=(12.4, 5.2),
                              gridspec_kw=dict(width_ratios=[1.35, 1.0], wspace=0.28))

# --- a. the series, the early trend, and what the plateau costs -------------------
ax.axvspan(2019.5, 2024.5, color=C["yellow"], alpha=0.12, lw=0, zorder=0)
ax.annotate("the five years best placed to measure a\ndecade-long drift are unusable for it",
            xy=(2022, 5.32), fontsize=7.6, color="#8a6a00", ha="center")
yrs = np.array([2015, 2026])
ax.plot(yrs, tr.intercept + tr.slope * yrs, color=C["red"], lw=1.2, ls=(0, (5, 3)),
        zorder=2, label="2015--19 trend (%+.3f/yr, $p = %.3f$)" % (tr.slope, tr.pvalue))
ax.plot(nat.index, nat.values, color=INK2, lw=1.8, marker="o", ms=5, zorder=3,
        label="Mean Física mark, 17 communities")
ax.scatter([2025], [nat.loc[2025]], s=80, color=C["aqua"], zorder=4)
ax.annotate("2025 lands %+.2f above\nthe early trend's projection" % (nat.loc[2025] - proj_2025),
            xy=(2025, nat.loc[2025]), textcoords="offset points", xytext=(-12, 16),
            fontsize=7.8, color=C["aqua"], ha="right")
ax.scatter([2025], [proj_2025], s=40, facecolor="none", edgecolor=C["red"], zorder=4)
ax.annotate("projected %.2f" % proj_2025, xy=(2025, proj_2025),
            textcoords="offset points", xytext=(-8, -13), fontsize=7.6,
            color=C["red"], ha="right")
ax.set_xticks(range(2015, 2027, 2))
ax.set_xlabel("Year")
ax.set_ylabel("Mean Física mark, ordinary sitting")
ax.set_title("a. The early decline did not continue")
ax.legend(loc="upper left", fontsize=7.6)

axp = ax.twinx()
axp.plot(presented.index, presented.values / 1000, color=C["violet"], lw=1.3,
         alpha=0.55, zorder=1)
axp.set_ylabel("Thousands presented", color=C["violet"], fontsize=9)
axp.tick_params(axis="y", colors=C["violet"])
axp.grid(False)
axp.annotate("presented: %d to %d (+%.0f %%)"
             % (presented.loc[2015], presented.loc[2025],
                100 * (presented.loc[2025] / presented.loc[2015] - 1)),
             xy=(2015.1, presented.loc[2015] / 1000 + 1.0), fontsize=7.6,
             color=C["violet"])

# --- b. the dilution test --------------------------------------------------------
axd.axhline(0, color=INK2, lw=0.9, zorder=1)
axd.axvline(0, color=INK2, lw=0.9, zorder=1)
axd.scatter(nc.d_presented, nc.d_mean, s=16, color=MUTED, alpha=0.65, lw=0, zorder=2)
xs = np.linspace(nc.d_presented.min(), nc.d_presented.max(), 50)
axd.plot(xs, np.polyval(dil_fit, xs), color=C["red"], lw=1.5, zorder=3)
axd.annotate("$r = %+.3f$, $p = %.3f$, $n = %d$\nabout %.0f %% of the within-region variance"
             % (dil[0], dil[1], len(nc), 100 * dil[0] ** 2),
             xy=(0.97, 0.96), xycoords="axes fraction", fontsize=7.8, color=C["red"],
             ha="right", va="top")
axd.set_xlabel("Cohort size that year, relative to the region's own average (SD)")
axd.set_ylabel("Mean mark, relative to the region's own average")
axd.set_title("b. Within a community, bigger cohorts score a little lower")

fig.text(0.005, 0.015,
         "Ministry EPAU, Física, ordinary sitting, specific phase. Panel b uses the "
         "non-plateau years only (n = %d) and expresses both variables as deviations "
         "from each\ncommunity's own average, so it compares a community with itself. "
         "The conditional top-band share shows no significant trend over the same years "
         "(%+.4f/yr, p = %.3f),\nso whatever drifts is not obviously the composition of "
         "the top." % (len(nc), ratio_tr.slope, ratio_tr.pvalue),
         fontsize=7, color=MUTED, linespacing=1.5)
fig.subplots_adjust(bottom=0.26, top=0.91, left=0.07, right=0.93)
_save(fig, "fig20_cohort_drift", P, dpi=200)

json.dump({
    "presented_2015": int(presented.loc[2015]), "presented_2025": int(presented.loc[2025]),
    "growth_pct": float(100 * (presented.loc[2025] / presented.loc[2015] - 1)),
    "pre_covid_trend_per_year": float(tr.slope), "pre_covid_trend_p": float(tr.pvalue),
    "pre_covid_trend_r2": float(tr.rvalue ** 2),
    "projected_2025": float(proj_2025), "actual_2025": float(nat.loc[2025]),
    "actual_minus_projected": float(nat.loc[2025] - proj_2025),
    "dilution_r": float(dil[0]), "dilution_p": float(dil[1]), "dilution_n": int(len(nc)),
    "ratio_trend_per_year": float(ratio_tr.slope), "ratio_trend_p": float(ratio_tr.pvalue),
}, open(A / "cohort_drift.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"pre-COVID trend {tr.slope:+.4f}/yr p={tr.pvalue:.3f}; 2025 {nat.loc[2025]:.2f} "
      f"vs projected {proj_2025:.2f} ({nat.loc[2025] - proj_2025:+.2f})")
print(f"dilution r={dil[0]:+.3f} p={dil[1]:.3f}; ratio trend {ratio_tr.slope:+.4f} p={ratio_tr.pvalue:.3f}")
