#!/usr/bin/env python3
"""Is a fall in the Física mean a location shift or a change of shape?

Pass rate and the 8–10 share are both functionals of the same grade distribution,
so both are near-deterministic functions of the mean: across 17 communities and
2015–2025 the correlations are r = 0.97 and r = 0.96. A scatter of either against
the mean therefore mostly redraws arithmetic. The information is in the RESIDUAL —
a cohort sitting off the common locus has a differently shaped distribution, not
merely a lower one.

That turns the open question of chapter 6 into a testable one. If 2026 lies on the
locus, the whole distribution slid down together (a uniformly harder paper or
uniformly stricter marking). If it lies below on the pass panel while holding its
place on the 8–10 panel, the bottom of the cohort was hit and the top was not.

Reads : data/ministry_fisica_panel.csv, data/ministry_fisica_distr.csv,
        data/found_canarias_ull_powerbi.csv, data/found_canarias_ulpgc_powerbi.csv,
        data/analysis/results.json
Writes: plots/fig16_shape_locus.(png|svg), data/analysis/shape_locus.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import (anderson, beta as beta_dist, kurtosis, norm,
                         shapiro, skew, ttest_ind)

from plot_style import C, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
A = DATA / "analysis"
P = ROOT / "plots"

# The Ministry publishes Física under the specific (voluntary) phase for the whole
# 2015–2025 window — the general phase carries it only in 2015–16, before LOMCE
# moved it out — and the band file exists for that phase only. 02_analysis.py uses
# the same phase for the País Vasco distribution, so the series match.
PHASE, SITTING = "specific", "ordinary"
AGGREGATES = ["Total", "Estado"]

panel = pd.read_csv(DATA / "ministry_fisica_panel.csv")
distr = pd.read_csv(DATA / "ministry_fisica_distr.csv")
hist = (
    panel[(panel.sitting == SITTING) & (panel.phase == PHASE)]
    .merge(distr[(distr.sitting == SITTING) & (distr.phase == PHASE)],
           on=["ccaa", "year", "sitting", "phase"])
)
hist = hist[~hist.ccaa.isin(AGGREGATES)].dropna(subset=["mean", "pass_pct"]).copy()
hist["top"] = hist["[8-9)"] + hist["[9-10]"]

# The two published quantities should agree: the pass rate is 100 - the [0,5) share.
# They do for 185 of 187 region-years, to floating-point. The exceptions are Galicia
# 2015 (5.64 pp) and Galicia 2016 (4.48 pp) — the two years in which Física still
# appeared in the general phase as well, so the Ministry's own cube is carrying the
# two cells on different bases. The band rows themselves are sound (every row sums to
# 100.0), so the points are kept rather than dropped: two of 187 do not move a fit,
# and discarding published data to make a check pass would be the wrong trade. They
# are recorded in the summary so the chapter can name them.
hist["pass_gap"] = (hist.pass_pct - (100 - hist["[0-5)"])).abs()
inconsistent = hist[hist.pass_gap > 1.0][["ccaa", "year", "pass_gap"]]
band_sums = hist[["[0-5)", "[5-6)", "[6-7)", "[7-8)", "[8-9)", "[9-10]"]].sum(axis=1)
assert band_sums.between(99.0, 101.0).all(), "a band row does not sum to 100"

# Quadratic rather than linear: both relations bend near the ends, where a bounded
# 0–10 scale compresses them. Degree 2 is the lowest that does not leave visible
# structure in the residuals.
coef_pass = np.polyfit(hist["mean"], hist.pass_pct, 2)
coef_top = np.polyfit(hist["mean"], hist.top, 2)
sd_pass = float((hist.pass_pct - np.polyval(coef_pass, hist["mean"])).std())
sd_top = float((hist.top - np.polyval(coef_top, hist["mean"])).std())

# Does the locus survive the 2017 regime change? Física left the general phase under
# LOMCE, and the presented cohort grew by more than half, so if the relation depended
# on who sits the paper it should step here. Tested on residuals, pre (2015–16) vs
# post (2017–25), with and without the COVID sittings.
hist["resid_pass"] = hist.pass_pct - np.polyval(coef_pass, hist["mean"])
hist["resid_top"] = hist.top - np.polyval(coef_top, hist["mean"])


def regime_test(df):
    a, b = df[df.year <= 2016], df[df.year >= 2017]
    out = {"n": int(len(df))}
    for key in ("pass", "top"):
        col = f"resid_{key}"
        t = ttest_ind(a[col], b[col], equal_var=False)
        out[key] = {"pre_pp": float(a[col].mean()), "post_pp": float(b[col].mean()),
                    "t": float(t.statistic), "p": float(t.pvalue)}
    return out


regimes = {"all_years": regime_test(hist),
           "excluding_covid_2020_21": regime_test(hist[~hist.year.isin([2020, 2021])])}
cohort = {int(y): int(hist[hist.year == y].presented.sum()) for y in (2015, 2025)}


def band_share_8_10(row, total):
    return (row.h_8_9 + row.h_9_10) / total * 100.0


def observed_2026():
    """The only 2026 cohorts with a published histogram, so the only ones whose
    SHAPE is observed rather than inferred."""
    out = []
    ull = pd.read_csv(DATA / "found_canarias_ull_powerbi.csv")
    r = ull[(ull.year == 2026) & (ull.sitting == SITTING)].iloc[0]
    out.append(("ULL (Tenerife) 2026", r["mean"], r.pass_pct, band_share_8_10(r, r.exams)))

    ulpgc = pd.read_csv(DATA / "found_canarias_ulpgc_powerbi.csv")
    r = ulpgc[(ulpgc.year == 2026) & (ulpgc.sitting == SITTING)].iloc[0]
    n = sum(r[f"h_{i}_{i + 1}"] for i in range(10))
    out.append(("ULPGC (Las Palmas) 2026", r["mean"], r.pass_pct, band_share_8_10(r, n)))
    return out


results = json.load(open(A / "results.json", encoding="utf-8"))
fit = results["beta_fits"]["EHU_2026"]
ehu26_mean, ehu26_pass = 3.99, 39.8
ehu26_top = float((1 - beta_dist.cdf(0.8, fit["a"], fit["b"])) * 100)

PASS_MARK, TOP_MARK = "o", "s"          # C7b: one marker per quantity, both panels
COL_CLOUD, COL_EHU = MUTED, C["violet"]
COL_OBS, COL_MODEL = C["aqua"], C["red"]
# The pre-2017 regime is a property of the background cloud, not a quantity of its
# own, so it is distinguished by fill and tone rather than by a hue. Giving it a
# colour would put a second hollow warm marker next to the hollow red model marker
# and make two unrelated things look related.
COL_PRE = INK2

# Standard error of the fitted locus itself, which the flat residual-SD band does
# not show. It is smallest where the region-years pile up and grows towards both
# ends — at mean 4.0, where the 2026 cohorts sit, the curve is uncertain to about
# ±1.4 pp at 95 %, against ±0.3 pp at mean 6.0. Without this the reader cannot tell
# that a 2026 point is being compared with an extrapolated curve.
def locus_ci(xq, coef, xs, ys, deg=2):
    """95 % confidence interval of the fitted mean response at xq."""
    X = np.vander(xs, deg + 1)
    resid = ys - np.polyval(coef, xs)
    s2 = float(resid @ resid) / (len(xs) - (deg + 1))
    XtXi = np.linalg.inv(X.T @ X)
    Xq = np.vander(np.atleast_1d(xq), deg + 1)
    se = np.sqrt(s2 * np.einsum("ij,jk,ik->i", Xq, XtXi, Xq))
    return 1.96 * se


fig = plt.figure(figsize=(11.6, 10.4))
gs = fig.add_gridspec(3, 2, height_ratios=[3.0, 1.35, 1.35], hspace=0.62, wspace=0.22)
axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])]
margs = [fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])]
margs_nc = [fig.add_subplot(gs[2, 0]), fig.add_subplot(gs[2, 1])]
grid = np.linspace(hist["mean"].min() - 0.15, hist["mean"].max() + 0.15, 200)
ehu = hist[hist.ccaa == "País Vasco"].sort_values("year")
obs = observed_2026()

# Labels are written as plain text: plot_style's guard escapes them on the way in,
# so pre-escaping "\%" here would be escaped a second time and render as "\{}%".
panels = [
    (axes[0], "pass_pct", coef_pass, sd_pass, PASS_MARK,
     "Pass rate (% of presented)", "a. Pass rate against the mean",
     ehu26_pass, [(lab, mu, pa) for lab, mu, pa, _ in obs]),
    (axes[1], "top", coef_top, sd_top, TOP_MARK,
     "Share in the 8–10 band (%)", "b. Top band against the mean",
     ehu26_top, [(lab, mu, tp) for lab, mu, _, tp in obs]),
]

# Annotation offsets are per point AND per panel: the four 2026 labels crowd the
# same lower-left corner, and on the top-band panel ULL and ULPGC nearly coincide
# (9.8 % at mean 4.08 against 10.8 % at 4.41), so one of the two has to go below.
OFFSETS = {
    "a. Pass rate against the mean": {
        "ULL (Tenerife) 2026": (9, -3),
        "ULPGC (Las Palmas) 2026": (9, 3),
        "model": (-9, -20),
    },
    "b. Top band against the mean": {
        # ULL sits at mean 4.08 and the EHU model marker at 3.99, so a left-going
        # ULL label runs straight into the model label; both 2026 observations go
        # right, separated vertically.
        "ULL (Tenerife) 2026": (10, -13),
        "ULPGC (Las Palmas) 2026": (15, -7),
        "model": (-9, -22),
    },
}

for ax, col, coef, sd, marker, ylab, title, ehu26_y, overlay in panels:
    curve = np.polyval(coef, grid)
    ax.fill_between(grid, curve - 2 * sd, curve + 2 * sd, color="#e9e8e4",
                    zorder=0, lw=0, label="scatter of region-years (±2 SD)")
    # The locus's own 95 % interval, which widens where the data thin out. This is
    # the band a 2026 point should be judged against, and at mean 4 it is wide.
    ci = locus_ci(grid, coef, hist["mean"].values, hist[col].values)
    ax.fill_between(grid, curve - ci, curve + ci, color=INK2, alpha=0.22,
                    zorder=1, lw=0, label="locus, 95 % CI of the fit")
    ax.plot(grid, curve, color=INK2, lw=1.2, zorder=2,
            label="2015--2025 locus (17 regions)")
    # The cloud is split at the 2017 regime change. Until 2016 Física could also be
    # sat in the general phase; from 2017 LOMCE left it in the voluntary phase only,
    # and the presented cohort then grew 59 % (30,839 to 49,010). Showing the two
    # regimes separately is the point: they lie on the SAME locus, so the mapping
    # from mean to pass rate is a property of the marking scale rather than of who
    # sits the paper — which is what licenses reading a 2026 point off it at all.
    pre = hist[hist.year <= 2016]
    post = hist[hist.year >= 2017]
    ax.scatter(post["mean"], post[col], s=13, color=COL_CLOUD, alpha=0.55,
               marker=marker, lw=0, zorder=2,
               label="region-year 2017--2025 (voluntary phase)")
    ax.scatter(pre["mean"], pre[col], s=20, facecolor="none", edgecolor=COL_PRE,
               marker=marker, lw=0.8, alpha=0.9, zorder=2,
               label="region-year 2015--2016 (also general phase)")
    ax.plot(ehu["mean"], ehu[col], color=COL_EHU, lw=1.4, alpha=0.9, zorder=3)
    ax.scatter(ehu["mean"], ehu[col], s=26, color=COL_EHU, marker=marker,
               lw=0, zorder=4, label="Euskadi (UPV/EHU) 2015--2025")
    for yr in (2015, 2021, 2025):
        row = ehu[ehu.year == yr]
        if len(row):
            ax.annotate(str(yr), (row["mean"].iloc[0], row[col].iloc[0]),
                        textcoords="offset points", xytext=(5, 5),
                        fontsize=7.5, color=COL_EHU)
    for lab, mu, val in overlay:
        ax.scatter([mu], [val], s=62, color=COL_OBS, marker=marker,
                   edgecolor="white", lw=0.9, zorder=6)
        ax.annotate(lab.split(" (")[0] + " 2026", (mu, val), textcoords="offset points",
                    xytext=OFFSETS[title][lab], fontsize=7.5, color=COL_OBS,
                    ha="right" if OFFSETS[title][lab][0] < 0 else "left")
    # The EHU 2026 shape is a Beta fitted to the published mean, pass rate and zero
    # count, so on these axes it can only reproduce the arithmetic it was given. It
    # is drawn hollow to mark it as a model, never as a test of the model.
    ax.scatter([ehu26_mean], [ehu26_y], s=78, facecolor="none", edgecolor=COL_MODEL,
               marker=marker, lw=1.6, zorder=6)
    ax.annotate("EHU 2026\n(fitted model)", (ehu26_mean, ehu26_y),
                textcoords="offset points", xytext=OFFSETS[title]["model"],
                fontsize=7.5, color=COL_MODEL, ha="right")
    # The x-marginal is the same variable in both panels, so instead of drawing it
    # twice the sparse end of it is marked here: only 2 of 187 region-years lie
    # below 4.5, which is where all three 2026 cohorts fall.
    ax.axvspan(grid[0], 4.5, color=COL_MODEL, alpha=0.055, lw=0, zorder=0)
    ax.set_xlabel("Mean Física mark, ordinary sitting")
    ax.set_ylabel(ylab)
    ax.set_title(title)

axes[0].legend(loc="upper left", fontsize=7.6)
# fig.text does not wrap, and an over-long single line stretches the canvas, so the
# in-figure note stays short and the full statement of sources, denominators and the
# regime test lives in the Quarto caption (ThesisFigures T5/E5).
# ---------------------------------------------------------------------------
# Panels c and d — the distribution of each joint panel's own y variable.
#
# These are deliberately NOT the distribution of the mean: that is the same
# variable on both x axes, so drawing it under each panel would repeat one
# histogram. The two y distributions are different quantities and they give
# opposite answers, which is the reason to separate them. The pass rate sits in
# the middle of a bounded scale and comes out symmetric; the 8–10 share is a tail
# quantity pressed against zero and is strongly right-skewed. That asymmetry is
# also why a residual quoted "in SD" is better behaved on the pass panel than on
# the top-band panel, where the scatter it is normalised by is not symmetric.
# ---------------------------------------------------------------------------
means = hist["mean"].values
n_below = int((means < 4.5).sum())

marginals = [
    (margs[0], "pass_pct", np.arange(30, 100, 3.0), "Pass rate (% of presented)",
     "c. Distribution of the pass rate", PASS_MARK),
    (margs[1], "top", np.arange(0, 80, 3.0), "Share in the 8–10 band (%)",
     "d. Distribution of the 8–10 band share", TOP_MARK),
]

normality = {}
for axm, col, bins, xlab, title, marker in marginals:
    v = hist[col].values
    sw, ad = shapiro(v), anderson(v, "norm")
    is_normal = bool(ad.statistic < ad.critical_values[2])
    normality[col] = {"skew": float(skew(v)), "excess_kurtosis": float(kurtosis(v)),
                      "shapiro_p": float(sw.pvalue), "anderson_A2": float(ad.statistic),
                      "anderson_crit_5pct": float(ad.critical_values[2]),
                      "normal_at_5pct": is_normal}
    axm.hist(v, bins=bins, color=COL_CLOUD, alpha=0.55, lw=0)
    xs = np.linspace(bins[0], bins[-1], 400)
    width = bins[1] - bins[0]
    axm.plot(xs, norm.pdf(xs, v.mean(), v.std(ddof=1)) * len(v) * width,
             color=INK2, lw=1.2, label="normal, same mean and SD")
    # Where the three 2026 cohorts fall on this quantity.
    vals = ([pa for _, _, pa, _ in obs] + [ehu26_pass]) if col == "pass_pct" \
        else ([tp for _, _, _, tp in obs] + [ehu26_top])
    for val, colr in zip(vals, [COL_OBS, COL_OBS, COL_MODEL]):
        axm.axvline(val, color=colr, lw=1.1, ymax=0.55)
    axm.annotate(
        "skew $%+.2f$, excess kurtosis $%+.2f$\n"
        "Shapiro--Wilk $p = %s$, Anderson--Darling $A^2 = %.2f$ (5 %% crit. %.2f)\n"
        "%s"
        % (normality[col]["skew"], normality[col]["excess_kurtosis"],
           ("%.3f" % sw.pvalue) if sw.pvalue >= 1e-3 else ("%.0e" % sw.pvalue),
           ad.statistic, ad.critical_values[2],
           "normality cannot be rejected" if is_normal else "not normal"),
        xy=(0.97, 0.92), xycoords="axes fraction", fontsize=7.2,
        color=INK2 if is_normal else COL_MODEL, ha="right", va="top")
    axm.set_xlabel(xlab)
    axm.set_ylabel("Region-years")
    axm.set_title(title)
    axm.legend(loc="upper left", fontsize=7.4)

# ---------------------------------------------------------------------------
# Panels e and f — the same two distributions with the COVID-era cohorts removed.
#
# The window is 2020–2024, not 2020–2022. The national mean sits +0.41, +1.03,
# +0.63, +0.61 and +0.71 above the 2015–2019 baseline in those five years and then
# returns to it in 2025 (−0.10): the relaxation does not decay year by year, it
# holds on a plateau for three years after the 2021 peak and ends in one step. The
# cut therefore follows the data rather than the calendar of the pandemic.
#
# The question this answers: do the distributions become normal once that regime is
# taken out? The pass rate was already normal and stays so. The 8–10 share does not
# become normal — but its Anderson–Darling statistic falls from 5.80 to 1.53, where
# the 2020–2022 cut alone leaves it at 4.20. What remains is the intrinsic skew of a
# tail quantity bounded at zero, not a COVID artefact.
# ---------------------------------------------------------------------------
COVID_PLATEAU = [2020, 2021, 2022, 2023, 2024]
nc = hist[~hist.year.isin(COVID_PLATEAU)]

normality_nc = {}
for axm, col, bins, xlab, title_all, marker in marginals:
    idx = 0 if col == "pass_pct" else 1
    axn = margs_nc[idx]
    v_all, v_nc = hist[col].values, nc[col].values
    sw, ad = shapiro(v_nc), anderson(v_nc, "norm")
    is_normal = bool(ad.statistic < ad.critical_values[2])
    ad_all = anderson(v_all, "norm")
    normality_nc[col] = {"n": int(len(v_nc)), "skew": float(skew(v_nc)),
                         "excess_kurtosis": float(kurtosis(v_nc)),
                         "shapiro_p": float(sw.pvalue),
                         "anderson_A2": float(ad.statistic),
                         "anderson_A2_all_years": float(ad_all.statistic),
                         "normal_at_5pct": is_normal}
    # All years, dimmed, as the reference the reader just looked at one row above.
    axn.hist(v_all, bins=bins, color=COL_CLOUD, alpha=0.20, lw=0,
             label="all years (as above)")
    axn.hist(v_nc, bins=bins, color=COL_CLOUD, alpha=0.70, lw=0,
             label="excluding 2020--2024")
    xs = np.linspace(bins[0], bins[-1], 400)
    width = bins[1] - bins[0]
    axn.plot(xs, norm.pdf(xs, v_nc.mean(), v_nc.std(ddof=1)) * len(v_nc) * width,
             color=INK2, lw=1.2, label="normal, same mean and SD")
    axn.annotate(
        "skew $%+.2f$, excess kurtosis $%+.2f$\n"
        "Anderson--Darling $A^2$: $%.2f \\rightarrow %.2f$ (5 %% crit. %.2f)\n%s"
        % (normality_nc[col]["skew"], normality_nc[col]["excess_kurtosis"],
           ad_all.statistic, ad.statistic, ad.critical_values[2],
           "still normal" if is_normal else "closer to normal, still not normal"),
        xy=(0.97, 0.92), xycoords="axes fraction", fontsize=7.2,
        color=INK2 if is_normal else COL_MODEL, ha="right", va="top")
    axn.set_xlabel(xlab)
    axn.set_ylabel("Region-years")
    axn.set_title(("e." if idx == 0 else "f.") +
                  title_all.split(".", 1)[1] + ", COVID plateau removed")
    axn.legend(loc="upper left", fontsize=7.0)

note = (
    "Ministry EPAU, Física, ordinary sitting, specific phase, 17 communities, "
    "n = %d region-years. Hollow markers in a and b: 2015–16, when Física could still "
    "be sat in the general phase;\nthe two regimes share one locus (pass p = %.2f, top "
    "band p = %.2f, excluding COVID). Tinted strip: only %d of %d region-years have a "
    "mean below 4.5, where all three 2026 cohorts sit.\nPanels c and d show each joint "
    "panel's own y variable — not the mean, which is the same variable on both x axes."
    % (len(hist), regimes["excluding_covid_2020_21"]["pass"]["p"],
       regimes["excluding_covid_2020_21"]["top"]["p"], n_below, len(hist))
)
fig.text(0.005, 0.005, note, fontsize=7, color=MUTED, linespacing=1.5)
fig.tight_layout(rect=[0, 0.03, 1, 1])
_save(fig, "fig16_shape_locus", P, dpi=200)

# Residuals, in units of the historical scatter, for the chapter text.
summary = {"n_region_years": int(len(hist)), "sd_pass_pp": sd_pass, "sd_top_pp": sd_top,
           "r_mean_pass": float(hist["mean"].corr(hist.pass_pct)),
           "r_mean_top": float(hist["mean"].corr(hist.top)),
           "pass_vs_bands_inconsistent_rows": [
               {"ccaa": r.ccaa, "year": int(r.year), "gap_pp": round(float(r.pass_gap), 2)}
               for r in inconsistent.itertuples()],
           "regime_change_2017": regimes,
           "presented_2015_2025": cohort,
           "y_normality": normality,
           "y_normality_excl_covid_plateau": normality_nc,
           "covid_plateau_years": COVID_PLATEAU,
           "mean_axis": {
               "skew": float(skew(means)), "excess_kurtosis": float(kurtosis(means)),
               "shapiro_p": float(sw.pvalue),
               "anderson_A2": float(ad.statistic),
               "anderson_crit_5pct": float(ad.critical_values[2]),
               "normal": bool(ad.statistic < ad.critical_values[2]),
               "n_below_4_5": int((means < 4.5).sum()),
               "n_below_5_0": int((means < 5.0).sum()),
               "locus_ci95_pp_at_mean_4_08": float(
                   locus_ci(4.08, coef_pass, hist["mean"].values, hist.pass_pct.values)[0]),
               "locus_ci95_pp_at_mean_6_00": float(
                   locus_ci(6.00, coef_pass, hist["mean"].values, hist.pass_pct.values)[0]),
           },
           "points": {}}
for lab, mu, pa, tp in obs + [("EHU 2026 (model)", ehu26_mean, ehu26_pass, ehu26_top)]:
    summary["points"][lab] = {
        "mean": float(mu),
        "pass_resid_pp": float(pa - np.polyval(coef_pass, mu)),
        "pass_resid_sd": float((pa - np.polyval(coef_pass, mu)) / sd_pass),
        "top_resid_pp": float(tp - np.polyval(coef_top, mu)),
        "top_resid_sd": float((tp - np.polyval(coef_top, mu)) / sd_top),
    }
json.dump(summary, open(A / "shape_locus.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print(json.dumps(summary["points"], indent=2, ensure_ascii=False))
