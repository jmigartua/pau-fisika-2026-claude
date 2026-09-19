#!/usr/bin/env python3
"""Among students who passed, how many reached the top band?

The pass rate and the 8–10 share are both level quantities: they move with the mean
almost deterministically (r = 0.974 and r = 0.961), so neither can easily separate a
distribution that moved from one that changed shape. Their ratio can.

    ratio = (share in 8–10) / (share at or above 5) = P(x ≥ 8 | x ≥ 5)

is the chance that a student who passed landed in the top band. It is conditional on
passing, so a uniform shift of the whole distribution moves it far less than it moves
either component — and indeed it correlates with the mean at r = 0.905, leaving 11.7 %
relative scatter, against 3 % or so for the other two. What is left is shape.

Reads : data/ministry_fisica_panel.csv, data/ministry_fisica_distr.csv,
        data/found_canarias_ull_powerbi.csv, data/found_canarias_ulpgc_powerbi.csv,
        data/analysis/results.json
Writes: plots/fig19_conditional_top.(png|svg), data/analysis/conditional_top.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import beta as beta_dist, ttest_ind

from plot_style import C, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
A = DATA / "analysis"
P = ROOT / "plots"

PHASE, SITTING = "specific", "ordinary"
PLATEAU = list(range(2020, 2025))

panel = pd.read_csv(DATA / "ministry_fisica_panel.csv")
distr = pd.read_csv(DATA / "ministry_fisica_distr.csv")
hist = (panel[(panel.sitting == SITTING) & (panel.phase == PHASE)]
        .merge(distr[(distr.sitting == SITTING) & (distr.phase == PHASE)],
               on=["ccaa", "year", "sitting", "phase"]))
hist = hist[~hist.ccaa.isin(["Total", "Estado"])].dropna(subset=["mean", "pass_pct"]).copy()
hist["top"] = hist["[8-9)"] + hist["[9-10]"]
hist["ratio"] = hist.top / hist.pass_pct

coef = np.polyfit(hist["mean"], hist.ratio, 2)
sd = float((hist.ratio - np.polyval(coef, hist["mean"])).std())


def locus_ci(xq):
    X = np.vander(hist["mean"].values, 3)
    resid = hist.ratio.values - np.polyval(coef, hist["mean"].values)
    s2 = float(resid @ resid) / (len(hist) - 3)
    Xq = np.vander(np.atleast_1d(xq), 3)
    return 1.96 * np.sqrt(s2 * np.einsum("ij,jk,ik->i", Xq, np.linalg.inv(X.T @ X), Xq))


def obs_2026():
    out = []
    u = pd.read_csv(DATA / "found_canarias_ull_powerbi.csv")
    r = u[(u.year == 2026) & (u.sitting == SITTING)].iloc[0]
    out.append(("ULL 2026", r["mean"], (r.h_8_9 + r.h_9_10) / r.exams * 100 / r.pass_pct))
    g = pd.read_csv(DATA / "found_canarias_ulpgc_powerbi.csv")
    r = g[(g.year == 2026) & (g.sitting == SITTING)].iloc[0]
    n = sum(r[f"h_{i}_{i + 1}"] for i in range(10))
    out.append(("ULPGC 2026", r["mean"], (r.h_8_9 + r.h_9_10) / n * 100 / r.pass_pct))
    return out


fit = json.load(open(A / "results.json", encoding="utf-8"))["beta_fits"]["EHU_2026"]
ehu26_mean = 3.99
ehu26_ratio = float((1 - beta_dist.cdf(0.8, fit["a"], fit["b"])) * 100 / 39.8)

COL_OBS, COL_MODEL, COL_EHU = C["aqua"], C["red"], C["violet"]

fig, (ax, axy) = plt.subplots(1, 2, figsize=(11.8, 5.0),
                              gridspec_kw=dict(width_ratios=[1.25, 1.0], wspace=0.24))

# --- a. the conditional ratio against the mean ----------------------------------
grid = np.linspace(hist["mean"].min() - 0.15, hist["mean"].max() + 0.15, 200)
curve = np.polyval(coef, grid)
ci = locus_ci(grid)
ax.axvspan(grid[0], 4.5, color=COL_MODEL, alpha=0.055, lw=0, zorder=0)
ax.fill_between(grid, curve - 2 * sd, curve + 2 * sd, color="#e9e8e4", lw=0, zorder=0,
                label="scatter of region-years (±2 SD)")
ax.fill_between(grid, curve - ci, curve + ci, color=INK2, alpha=0.22, lw=0, zorder=1,
                label="locus, 95 % CI of the fit")
ax.plot(grid, curve, color=INK2, lw=1.2, zorder=2, label="2015--2025 locus")
plate = hist[hist.year.isin(PLATEAU)]
rest = hist[~hist.year.isin(PLATEAU)]
ax.scatter(rest["mean"], rest.ratio, s=14, color=MUTED, alpha=0.6, lw=0, zorder=2,
           label="region-year outside 2020--24")
ax.scatter(plate["mean"], plate.ratio, s=20, facecolor="none", edgecolor=C["yellow"],
           lw=0.9, zorder=2, label="region-year 2020--24 (plateau)")
ehu = hist[hist.ccaa == "País Vasco"].sort_values("year")
ax.plot(ehu["mean"], ehu.ratio, color=COL_EHU, lw=1.4, zorder=3)
ax.scatter(ehu["mean"], ehu.ratio, s=26, color=COL_EHU, lw=0, zorder=4,
           label="Euskadi (UPV/EHU)")
e25 = ehu[ehu.year == 2025].iloc[0]
ax.annotate("Euskadi 2025", (e25["mean"], e25.ratio), textcoords="offset points",
            xytext=(6, -12), fontsize=7.5, color=COL_EHU)
# ULL (4.08) and ULPGC (4.41) sit at almost the same height, so their labels are
# separated vertically rather than both going right.
OFF = {"ULL 2026": (7, 7), "ULPGC 2026": (8, -12)}
for lab, mu, rr in obs_2026():
    ax.scatter([mu], [rr], s=62, color=COL_OBS, edgecolor="white", lw=0.9, zorder=6)
    ax.annotate(lab, (mu, rr), textcoords="offset points", xytext=OFF[lab],
                fontsize=7.5, color=COL_OBS)
ax.scatter([ehu26_mean], [ehu26_ratio], s=78, facecolor="none", edgecolor=COL_MODEL,
           lw=1.6, zorder=6)
ax.annotate("EHU 2026\n(fitted model)", (ehu26_mean, ehu26_ratio),
            textcoords="offset points", xytext=(-8, -22), fontsize=7.5,
            color=COL_MODEL, ha="right")
ax.set_xlabel("Mean Física mark, ordinary sitting")
ax.set_ylabel("Top-band share among those who passed")
ax.set_title("a. $P(x \\geq 8 \\mid x \\geq 5)$ against the mean")
ax.legend(loc="upper left", fontsize=7.2)

# --- b. the same quantity by year ------------------------------------------------
years = sorted(hist.year.unique())
for y in years:
    v = hist[hist.year == y].ratio.values
    colr = C["yellow"] if y in PLATEAU else MUTED
    axy.scatter(np.full(len(v), y) + np.random.default_rng(y).normal(0, 0.07, len(v)),
                v, s=12, color=colr, alpha=0.55, lw=0, zorder=2)
    axy.plot([y - 0.28, y + 0.28], [v.mean()] * 2, color=INK2, lw=1.8, zorder=3)
pre = hist[hist.year <= 2019].ratio
plateau_v = hist[hist.year.isin(PLATEAU)].ratio
y25 = hist[hist.year == 2025].ratio
t_plate = ttest_ind(plateau_v, pre, equal_var=False)
t_25 = ttest_ind(y25, pre, equal_var=False)
axy.axhline(pre.mean(), color=INK2, lw=1.0, ls=(0, (5, 3)), zorder=1,
            label="2015--19 mean (%.3f)" % pre.mean())
axy.axvspan(2019.5, 2024.5, color=C["yellow"], alpha=0.10, lw=0, zorder=0)
axy.annotate("plateau %.3f\n$p = %.0e$ vs pre-COVID" % (plateau_v.mean(), t_plate.pvalue),
             xy=(2022, 0.70), fontsize=7.6, color="#8a6a00", ha="center")
axy.annotate("2025 back to %.3f\n($p = %.2f$)" % (y25.mean(), t_25.pvalue),
             xy=(2025, 0.63), fontsize=7.6, color=INK2, ha="center")
axy.set_xticks(years[::2])
axy.set_xlabel("Year")
axy.set_ylabel("Top-band share among those who passed")
axy.set_title("b. The plateau was a change of shape, not only of level")
axy.legend(loc="lower left", fontsize=7.4)

fig.text(0.005, 0.015,
         "Ministry EPAU, Física, ordinary sitting, specific phase, 17 communities, "
         "n = %d region-years. The ratio is conditional on passing, so a uniform shift of\n"
         "the distribution moves it far less than it moves either component: it "
         "correlates with the mean at r = %.3f, against %.3f and %.3f for the pass rate "
         "and the\n8–10 share. ULL and ULPGC 2026 are observed; the EHU 2026 marker is "
         "hollow because its band share is fitted, not measured."
         % (len(hist), hist["mean"].corr(hist.ratio), hist["mean"].corr(hist.pass_pct),
            hist["mean"].corr(hist.top)),
         fontsize=7, color=MUTED, linespacing=1.5)
fig.subplots_adjust(bottom=0.30, top=0.90, left=0.075, right=0.985)
_save(fig, "fig19_conditional_top", P, dpi=200)

summary = {
    "n": int(len(hist)), "locus_residual_sd": sd,
    "r_mean_ratio": float(hist["mean"].corr(hist.ratio)),
    "r_mean_pass": float(hist["mean"].corr(hist.pass_pct)),
    "r_mean_top": float(hist["mean"].corr(hist.top)),
    "pre_covid_mean": float(pre.mean()), "plateau_mean": float(plateau_v.mean()),
    "y2025_mean": float(y25.mean()),
    "plateau_vs_pre": {"t": float(t_plate.statistic), "p": float(t_plate.pvalue)},
    "y2025_vs_pre": {"t": float(t_25.statistic), "p": float(t_25.pvalue)},
    "points": {},
}
for lab, mu, rr in obs_2026() + [("EHU 2026 (model)", ehu26_mean, ehu26_ratio),
                                 ("EHU 2025 (observed)", float(e25["mean"]), float(e25.ratio))]:
    summary["points"][lab] = {"mean": float(mu), "ratio": float(rr),
                              "resid": float(rr - np.polyval(coef, mu)),
                              "resid_sd": float((rr - np.polyval(coef, mu)) / sd)}
json.dump(summary, open(A / "conditional_top.json", "w", encoding="utf-8"), indent=2,
          ensure_ascii=False)
print(json.dumps({k: summary[k] for k in
                  ["r_mean_ratio", "pre_covid_mean", "plateau_mean", "y2025_mean"]}, indent=2))
for k, v in summary["points"].items():
    print(f"  {k:22} ratio {v['ratio']:.3f}  resid {v['resid_sd']:+.2f} SD")
