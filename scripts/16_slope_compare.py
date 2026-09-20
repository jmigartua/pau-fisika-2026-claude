#!/usr/bin/env python3
"""Do the PAU and PISA series fall at the same rate?

Figure 20a and figure 21a are two attainment series over roughly the same decade,
measured by instruments with nothing in common: one is the Física mark awarded by
Spanish university tribunals, the other a science scale set by the OECD. Asking
whether they are parallel is a fair question and a better one than asking whether
they correlate, which three overlapping points cannot answer.

Comparison needs a common scale. Each series is expressed in units of its own
student-level standard deviation: 2.34 marks for PAU Física, from the thirteen
published regional standard deviations and confirmed by the Beta fits of chapter 4;
about 90 points for PISA science in Spain, from the p10–p90 spread of the 2015
table 2.6. A slope in SD per decade is then comparable across the two.

The point estimates agree, and the agreement is closer than it had any need to be.
What the data cannot do is establish it: with four PISA rounds and six usable PAU
years every interval is wide enough to include zero, so "parallel" and "unrelated"
are both consistent with what is here. The figure shows both facts at once.

Reads : data/ministry_fisica_panel.csv, data/analysis/pisa_link.json,
        data/regional_fisica_found.csv
Writes: plots/fig22_slope_compare.(png|svg), data/analysis/slope_compare.json
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

# Student-level spreads, used only to put the two instruments on one axis.
SD_PAU = float(pd.read_csv(DATA / "regional_fisica_found.csv").sd.dropna().median())
SD_PISA = 90.0          # p90 - p10 = 605 - 374 over 2.563, PISA 2015 table 2.6, Spain

panel = pd.read_csv(DATA / "ministry_fisica_panel.csv")
m = panel[(panel.sitting == "ordinary") & (panel.phase == "specific")]
m = m[~m.ccaa.isin(["Total", "Estado"])].dropna(subset=["mean"])
pau_es = m.groupby("year")["mean"].mean()
pau_pv = m[m.ccaa == "País Vasco"].set_index("year")["mean"]

pisa = json.load(open(A / "pisa_link.json", encoding="utf-8"))["science_mean"]
pisa_pv = {int(k): v for k, v in pisa["pais_vasco"].items()}
pisa_es = {int(k): v for k, v in pisa["espana"].items()}

# The PISA window starts at 2012 so that both instruments cover the same decade;
# the 2006–2009 rounds predate every PAU year in this study. It ends at 2022 because
# 2025 is the round the 2027 estimator treats as forward-looking, and because the
# PAU series compared here also ends at 2025 (its 2026 point is not in the cube).
# The fit including 2025 is computed too and written to the JSON (audit, 19 Sep 2026):
# with five rounds both PISA slopes are significant on their own.
PISA_FROM = 2012
PISA_TO = 2022


def fit(years, values, sd):
    r = stats.linregress(list(years), list(values))
    per_decade = r.slope / sd * 10
    se = r.stderr / sd * 10
    ci = stats.t.ppf(0.975, len(years) - 2) * se
    return {"slope_sd_decade": per_decade, "se": se, "ci95": ci,
            "n": len(years), "p": float(r.pvalue), "r2": float(r.rvalue ** 2)}


pau_years_es = [y for y in pau_es.index if y not in PLATEAU]
pau_years_pv = [y for y in pau_pv.index if y not in PLATEAU]
pisa_years = [y for y in sorted(pisa_es) if PISA_FROM <= y <= PISA_TO]
pisa_years_all = [y for y in sorted(pisa_es) if y >= PISA_FROM]

fits = {
    "PAU Física, Spain": fit(pau_years_es, [pau_es.loc[y] for y in pau_years_es], SD_PAU),
    "PISA science, Spain": fit(pisa_years, [pisa_es[y] for y in pisa_years], SD_PISA),
    "PAU Física, Euskadi": fit(pau_years_pv, [pau_pv.loc[y] for y in pau_years_pv], SD_PAU),
    "PISA science, Euskadi": fit(pisa_years, [pisa_pv[y] for y in pisa_years], SD_PISA),
}


def diff_test(a, b):
    d = fits[a]["slope_sd_decade"] - fits[b]["slope_sd_decade"]
    se = (fits[a]["se"] ** 2 + fits[b]["se"] ** 2) ** 0.5
    z = d / se
    return {"difference": d, "se": se, "z": z,
            "p": float(2 * (1 - stats.norm.cdf(abs(z))))}


tests = {"Spain": diff_test("PAU Física, Spain", "PISA science, Spain"),
         "Euskadi": diff_test("PAU Física, Euskadi", "PISA science, Euskadi")}
ratios = {
    "PAU": fits["PAU Física, Euskadi"]["slope_sd_decade"] / fits["PAU Física, Spain"]["slope_sd_decade"],
    "PISA": fits["PISA science, Euskadi"]["slope_sd_decade"] / fits["PISA science, Spain"]["slope_sd_decade"],
}

fig, (ax, axf) = plt.subplots(1, 2, figsize=(12.6, 5.2),
                              gridspec_kw=dict(width_ratios=[1.2, 1.0], wspace=0.28))

# --- a. both instruments, centred and in SD units --------------------------------
def centred(years, values, sd):
    v = np.array(values, dtype=float)
    return np.array(years), (v - v.mean()) / sd


styles = [("PAU Física, Spain", pau_years_es, [pau_es.loc[y] for y in pau_years_es],
           SD_PAU, INK2, "o", "-"),
          ("PISA science, Spain", pisa_years, [pisa_es[y] for y in pisa_years],
           SD_PISA, INK2, "s", "--"),
          ("PAU Física, Euskadi", pau_years_pv, [pau_pv.loc[y] for y in pau_years_pv],
           SD_PAU, C["violet"], "o", "-"),
          ("PISA science, Euskadi", pisa_years, [pisa_pv[y] for y in pisa_years],
           SD_PISA, C["violet"], "s", "--")]
ax.axvspan(2019.5, 2024.5, color=C["yellow"], alpha=0.10, lw=0, zorder=0)
# The annotation used to sit at y = 0.50, outside an axis that tops out near 0.21, so
# it was never rendered and the shaded band went unexplained (audit, 20 September).
ax.annotate("PAU plateau (excluded from the PAU fits)", xy=(2022, 0.175), fontsize=7.4,
            color="#8a6a00", ha="center")
ax.axhline(0, color=MUTED, lw=0.9, zorder=1)
for lab, yrs, vals, sd, colr, mk, ls in styles:
    xs, ys = centred(yrs, vals, sd)
    ax.scatter(xs, ys, s=26, color=colr, marker=mk, zorder=3, alpha=0.85)
    b = np.polyfit(xs, ys, 1)
    grid = np.linspace(min(xs), max(xs), 20)
    ax.plot(grid, np.polyval(b, grid), color=colr, ls=ls, lw=1.7, zorder=2, label=lab)
ax.set_xlabel("Year (PAU) / PISA round")
ax.set_ylabel("Deviation from the series mean, in student SD")
ax.set_title("a. The same decade, both instruments, one scale")
ax.legend(loc="lower left", fontsize=7.4)

# --- b. the four slopes with their intervals -------------------------------------
labels = list(fits)
ypos = np.arange(len(labels))[::-1]
for y, lab in zip(ypos, labels):
    f = fits[lab]
    colr = C["violet"] if "Euskadi" in lab else INK2
    axf.plot([f["slope_sd_decade"] - f["ci95"], f["slope_sd_decade"] + f["ci95"]],
             [y, y], color=colr, lw=2.0, solid_capstyle="round", zorder=2)
    axf.scatter([f["slope_sd_decade"]], [y], s=64,
                color=colr, marker="o" if "PAU" in lab else "s", zorder=3)
    axf.annotate("%+.3f" % f["slope_sd_decade"], (f["slope_sd_decade"], y),
                 textcoords="offset points", xytext=(0, 10), ha="center",
                 fontsize=7.8, color=colr)
axf.axvline(0, color=C["red"], lw=1.1, ls=(0, (4, 3)), zorder=1)
axf.set_yticks(ypos)
axf.set_yticklabels(labels, fontsize=8)
axf.set_xlabel("Slope, student SD per decade")
_all_zero = all(abs(f["slope_sd_decade"]) < f["ci95"] for f in fits.values())
axf.set_title("b. Every interval includes zero" if _all_zero
              else "b. Not every interval includes zero")
axf.annotate(
    "Euskadi falls %.2f times as fast as Spain in the PAU\n"
    "and %.2f times as fast in PISA. The PAU–PISA slope\n"
    "difference is not distinguishable from zero\n"
    "(Spain $p = %.2f$, Euskadi $p = %.2f$)."
    % (ratios["PAU"], ratios["PISA"], tests["Spain"]["p"], tests["Euskadi"]["p"]),
    xy=(0.03, 0.04), xycoords="axes fraction", fontsize=7.8, color=INK2, va="bottom")
axf.set_ylim(-1.35, len(labels) - 0.4)   # room for the note below the last row
axf.grid(axis="y", visible=False)

fig.text(0.005, 0.015,
         "PAU: ministry EPAU, Física, ordinary sitting, specific phase, mean of the 17 "
         "communities; plateau years excluded, so six year-points. PISA: INEE Spanish "
         "reports,\nscience, 2012–2022, four rounds (2025 held out; with it both PISA slopes are significant: see the JSON). Each series is divided by its own "
         "student-level standard deviation — %.2f marks for the PAU, %.0f points for "
         "PISA — so the\nslopes are comparable. Agreement of the point estimates is not "
         "evidence of a common cause; with four and six points the test has very little "
         "power." % (SD_PAU, SD_PISA),
         fontsize=7, color=MUTED, linespacing=1.5)
fig.subplots_adjust(bottom=0.26, top=0.90, left=0.075, right=0.985)
_save(fig, "fig22_slope_compare", P, dpi=200)

fits_incl_2025 = {
    "PISA science, Spain": fit(pisa_years_all, [pisa_es[y] for y in pisa_years_all], SD_PISA),
    "PISA science, Euskadi": fit(pisa_years_all, [pisa_pv[y] for y in pisa_years_all], SD_PISA),
}
fits_incl_2025["euskadi_over_spain_slope_ratio"] = (fits_incl_2025["PISA science, Euskadi"]["slope_sd_decade"]
                                                    / fits_incl_2025["PISA science, Spain"]["slope_sd_decade"])
json.dump({"sd_pau_marks": SD_PAU, "sd_pisa_points": SD_PISA,
           "pisa_window_from": PISA_FROM, "pisa_window_to": PISA_TO,
           "pisa_fits_2012_2025_incl_2025_round": fits_incl_2025, "fits": fits, "slope_difference_tests": tests,
           "euskadi_over_spain_slope_ratio": ratios},
          open(A / "slope_compare.json", "w", encoding="utf-8"), indent=2,
          ensure_ascii=False)
for lab, f in fits.items():
    print(f"  {lab:24} {f['slope_sd_decade']:+.3f} SD/decade  "
          f"[{f['slope_sd_decade']-f['ci95']:+.3f}, {f['slope_sd_decade']+f['ci95']:+.3f}]  n={f['n']}")
print(f"\n  ratio Euskadi/Spain: PAU {ratios['PAU']:.2f}x, PISA {ratios['PISA']:.2f}x")
for k, t in tests.items():
    print(f"  slope difference {k}: {t['difference']:+.3f} SD/decade, p = {t['p']:.2f}")
