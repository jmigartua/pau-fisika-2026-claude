"""Figures for the Quarto site (PNG 200 dpi + SVG). Palette and mark rules follow the dataviz reference
palette: categorical slots in fixed order, thin marks, recessive grid, selective direct labels, one axis per panel.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "data" / "analysis"
P = ROOT / "plots"
P.mkdir(exist_ok=True)
R = json.load(open(A / "results.json", encoding="utf-8"))

C = dict(blue="#2a78d6", orange="#eb6834", aqua="#1baf7a", yellow="#eda100", magenta="#e87ba4", green="#008300", violet="#4a3aa7", red="#e34948")
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8983", "#e6e5e1", "#fcfcfb"
rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2,
                 "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
                 "axes.spines.right": False, "axes.titleweight": "semibold", "axes.titlecolor": INK, "axes.titlesize": 10.5,
                 "figure.facecolor": SURF, "axes.facecolor": SURF, "legend.frameon": False, "legend.fontsize": 8.5, "savefig.facecolor": SURF})


def save(fig, name):
    fig.savefig(P / f"{name}.png", dpi=200, bbox_inches="tight")
    fig.savefig(P / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)
    print("saved", name)


# ---------------------------------------------------------------- 1. Euskadi series
s = pd.read_csv(A / "euskadi_fisica_series_2010_2026.csv")
fig, axes = plt.subplots(2, 1, figsize=(8.4, 6.2), sharex=True, gridspec_kw=dict(hspace=0.12))
regimes = [(2009.5, 2011.5, "PAU 2010–11"), (2011.5, 2016.5, "PAU 2012–16"), (2016.5, 2019.5, "EAU (LOMCE)"), (2019.5, 2021.5, "COVID"),
           (2021.5, 2024.5, "post-COVID"), (2024.5, 2026.5, "LOMLOE")]
for ax in axes:
    for i, (a, b, lab) in enumerate(regimes):
        if i % 2 == 0:
            ax.axvspan(a, b, color="#f1f0ec", zorder=0, lw=0)
ax = axes[0]
ax.plot(s.year, s.spain_mean, color=MUTED, lw=1.6, marker="o", ms=4, label="Spain (all CCAA), ordinary", zorder=2)
ax.plot(s.year, s["mean"], color=C["blue"], lw=2.2, marker="o", ms=5.5, label="Euskadi (UPV/EHU), ordinary", zorder=3)
ax.scatter([2026], [3.99], s=110, facecolor=C["red"], edgecolor=SURF, lw=1.5, zorder=4)
for y, v in [(2010, 4.45), (2012, 6.49), (2025, 5.47), (2026, 3.99)]:
    ax.annotate(f"{v:.2f}", (y, v), textcoords="offset points", xytext=(0, 9 if v > 5 else -13), ha="center", fontsize=8.5, color=INK)
ax.annotate("7.69", (2021, 7.69), textcoords="offset points", xytext=(12, -2), ha="left", fontsize=8.5, color=INK)
ax.set_ylabel("Mean grade (0–10)")
ax.set_ylim(3.3, 8.2)
for a, b, lab in regimes:
    ax.text((a + b) / 2, 8.08, lab, ha="center", va="top", fontsize=7.5, color=INK2)
ax.legend(loc="lower left", ncol=2)
ax.set_title("Physics in the Basque university-entrance exam, ordinary sitting, 2010–2026")
ax = axes[1]
ax.plot(s.year, s.pass_pct, color=C["blue"], lw=2.2, marker="o", ms=5.5, zorder=3)
ax.scatter([2026], [39.8], s=110, facecolor=C["red"], edgecolor=SURF, lw=1.5, zorder=4)
for y, v in [(2010, 46.3), (2021, 89.6), (2025, 62.3), (2026, 39.8)]:
    ax.annotate(f"{v:.1f} %", (y, v), textcoords="offset points", xytext=(0, 9 if v > 60 else -13), ha="center", fontsize=8.5, color=INK)
ax.set_ylabel("Pass rate, % of presented")
ax.set_ylim(30, 95)
ax.set_xticks(range(2010, 2027))
ax.tick_params(axis="x", labelrotation=45)
ax.text(2010, 32, "Sources: EHU annual reports (2010–22), Ministry EPAU (2023–25), EHU presentation of 6 Jul 2026 (2026).", fontsize=7, color=MUTED)
save(fig, "fig01_euskadi_series")

# ---------------------------------------------------------------- 2. annual changes distribution
ch = pd.read_csv(A / "annual_changes_all_ccaa.csv")
fig, ax = plt.subplots(figsize=(8.4, 3.6))
bins = np.arange(-2.3, 2.4, 0.2)
ax.hist(ch.delta, bins=bins, color=C["blue"], alpha=0.85, edgecolor=SURF, lw=1)
ax.axvline(-1.48, color=C["red"], lw=2)
ax.text(-1.5, ax.get_ylim()[1] * 0.92, "Euskadi 2025→2026\nΔ = −1.48", ha="right", va="top", color=C["red"], fontsize=9)
ax.axvline(-0.62, color=C["orange"], lw=1.6, ls="--")
ax.text(-0.6, ax.get_ylim()[1] * 0.92, "Euskadi 2024→2025\nΔ = −0.62", ha="left", va="top", color=C["orange"], fontsize=9)
ax.set_xlabel("Year-to-year change of the ordinary-sitting Physics mean, all 17 CCAA, 2015–2025 (n = 170)")
ax.set_ylabel("Count")
d = R["annual_change_dist_all"]
ax.set_title(f"How unusual is a −1.48 change?  panel SD = {d['sd']:.2f}; only {R['ehu2026_delta_empirical_rank']['n_changes_more_negative']} of {d['n']} changes were as negative")
save(fig, "fig02_annual_changes")

# ---------------------------------------------------------------- 3. regions 2026 vs 2025 dumbbell
cmp = pd.read_csv(A / "regions_2026_vs_2025.csv").sort_values("delta")
short = {"Asturias (Principado de)": "Asturias", "Madrid (Comunidad de)": "Madrid", "Comunitat Valenciana": "C. Valenciana",
         "Castilla-La Mancha": "Castilla-La Mancha", "País Vasco": "Euskadi (UPV/EHU)"}
cmp["label"] = cmp.ccaa.map(lambda c: short.get(c, c))
fig, ax = plt.subplots(figsize=(8.4, 4.6))
y = np.arange(len(cmp))
for i, r in enumerate(cmp.itertuples()):
    col = C["red"] if r.delta < 0 else C["aqua"]
    ax.plot([r.mean_2025, r.mean_2026], [i, i], color=col, lw=2.2, zorder=2)
    ax.scatter(r.mean_2025, i, s=55, facecolor=SURF, edgecolor=INK2, lw=1.4, zorder=3)
    ax.scatter(r.mean_2026, i, s=70, facecolor=col, edgecolor=SURF, lw=1.2, zorder=4)
    ax.text(max(r.mean_2025, r.mean_2026) + 0.12, i, f"{r.delta:+.2f}", va="center", fontsize=8.5, color=INK)
    if r.quality == "press":
        ax.text(min(r.mean_2025, r.mean_2026) - 0.12, i, "press", va="center", ha="right", fontsize=7.5, color=MUTED)
ax.set_yticks(y)
ax.set_yticklabels(cmp.label)
ax.set_xlabel("Ordinary-sitting Physics mean (open = 2025, filled = 2026)")
ax.set_xlim(3.5, 7.4)
ax.set_title("2025 → 2026 by region: nine communities have published a 2026 Physics mean")
save(fig, "fig03_regions_2026_vs_2025")

# ---------------------------------------------------------------- 4. regional small multiples
L = pd.read_csv(A / "regional_long_series.csv")
order = ["País Vasco", "Canarias", "Extremadura", "Andalucía", "Comunitat Valenciana", "Cataluña", "Castilla-La Mancha", "Madrid (Comunidad de)", "Asturias (Principado de)"]
fig, axes = plt.subplots(3, 3, figsize=(9.2, 7.2), sharex=True, sharey=True, gridspec_kw=dict(hspace=0.35, wspace=0.12))
spain = L[L.ccaa == "Total"]
for ax, c in zip(axes.flat, order):
    d = L[(L.ccaa == c) & (L.year >= 2015)]
    ax.plot(spain.year, spain["mean"], color=MUTED, lw=1.3, zorder=1)
    ax.plot(d[d.year <= 2025].year, d[d.year <= 2025]["mean"], color=C["blue"], lw=1.9, marker="o", ms=3.5, zorder=2)
    d26 = d[d.year == 2026]
    if len(d26):
        col = C["red"] if d26["mean"].iloc[0] < d[d.year == 2025]["mean"].iloc[0] else C["aqua"]
        ax.plot([2025, 2026], [d[d.year == 2025]["mean"].iloc[0], d26["mean"].iloc[0]], color=col, lw=1.9, zorder=3)
        ax.scatter([2026], d26["mean"], s=48, facecolor=col, edgecolor=SURF, zorder=4)
        ax.text(2026.15, d26["mean"].iloc[0], f"{d26['mean'].iloc[0]:.2f}", fontsize=8, va="center", color=INK)
    ax.set_title(short.get(c, c) + (" (aptes basis)" if c == "Cataluña" else ""), fontsize=9.5)
    ax.set_ylim(3.4, 8.8)
    ax.set_xticks([2015, 2018, 2021, 2024, 2026])
    ax.tick_params(labelsize=8)
axes[0, 0].plot([], [], color=MUTED, lw=1.3, label="Spain total")
axes[0, 0].plot([], [], color=C["blue"], lw=1.9, label="Region (ministry 2015–25)")
axes[0, 0].legend(loc="upper left", fontsize=7.5)
fig.suptitle("Ordinary-sitting Physics mean, 2015–2026: ministry series plus the 2026 values located in this study", fontsize=11, fontweight="semibold", y=0.94)
save(fig, "fig04_regional_small_multiples")

# ---------------------------------------------------------------- 5. distributions
fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.9), gridspec_kw=dict(wspace=0.22))
ax = axes[0]
for lab, col, name in [("EHU_2025", C["blue"], "Euskadi 2025 (mean 5.47, 62 % pass, 10 % ≤2)"), ("EHU_2026", C["red"], "Euskadi 2026 (mean 3.99, 40 % pass, 24.5 % ≤2)")]:
    f = pd.read_csv(A / f"beta_fit_{lab}.csv")
    ax.plot(f.x, f.pdf, color=col, lw=2.2, label=name)
    ax.fill_between(f.x, 0, f.pdf, color=col, alpha=0.12)
ax.axvline(5, color=MUTED, lw=1, ls=":")
ax.set_xlabel("Grade")
ax.set_ylabel("Density (Beta-mixture fit to published moments)")
ax.set_title("Implied grade distributions, Euskadi")
ax.legend(loc="upper right", fontsize=7.8)
ax.set_xlim(0, 10)
ax = axes[1]
H = pd.read_csv(A / "canarias_histograms.csv", index_col=0)
x = np.arange(10)
w = 0.27
for i, (k, col, lab) in enumerate([("ULL_2024", MUTED, "ULL 2024 (mean 5.60)"), ("ULL_2025", C["blue"], "ULL 2025 (4.92)"), ("ULL_2026", C["red"], "ULL 2026 (4.08)")]):
    ax.bar(x + (i - 1) * w, 100 * H[k], width=w * 0.92, color=col, label=lab, zorder=2)
ax.set_xticks(x)
ax.set_xticklabels([f"{i}–{i+1}" for i in range(10)], fontsize=8)
ax.set_xlabel("Grade band")
ax.set_ylabel("% of exams")
ax.set_title("Observed histograms, Tenerife (ULL), ordinary sitting")
ax.legend(fontsize=7.8)
save(fig, "fig05_distributions")

# ---------------------------------------------------------------- 6. Euskadi grade bands 2015–2025 (+2026 implied)
gb = pd.read_csv(A / "euskadi_grade_bands_2015_2025.csv", index_col=0)
gb["[5-7)"] = gb["[5-6)"] + gb["[6-7)"]
gb["[7-9)"] = gb["[7-8)"] + gb["[8-9)"]
gb = gb[["[0-5)", "[5-7)", "[7-9)", "[9-10]"]]
f26 = R["beta_fits"]["EHU_2026"]["band_shares"]
gb.loc[2026] = [100 * sum(f26[f"[{i}-{i+1})"] for i in range(5)), 100 * sum(f26[f"[{i}-{i+1})"] for i in (5, 6)), 100 * sum(f26[f"[{i}-{i+1})"] for i in (7, 8)), 100 * f26["[9-10)"]]
fig, ax = plt.subplots(figsize=(8.4, 3.9))
bottom = np.zeros(len(gb))
cols = [C["red"], C["yellow"], C["aqua"], C["blue"]]
for col, band in zip(cols, gb.columns):
    ax.bar(gb.index, gb[band], bottom=bottom, color=col, width=0.72, edgecolor=SURF, lw=1.2, label=band, zorder=2)
    for xi, (b0, v) in enumerate(zip(bottom, gb[band])):
        if v > 7:
            ax.text(gb.index[xi], b0 + v / 2, f"{v:.0f}", ha="center", va="center", fontsize=7.5, color="white")
    bottom += gb[band].values
ax.bar([2026], [100], color="none", edgecolor=C["red"], lw=1.6, ls="--", width=0.78, zorder=3)
ax.text(2026, 103, "2026: implied\n(model)", ha="center", fontsize=7.5, color=C["red"])
ax.set_xticks(gb.index)
ax.set_ylabel("% of presented")
ax.set_ylim(0, 112)
ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.13))
ax.set_title("Euskadi Physics, ordinary sitting: grade-band shares (Ministry EPAU 2015–2025; 2026 from the fitted distribution)", pad=22)
save(fig, "fig06_euskadi_grade_bands")

# ---------------------------------------------------------------- 7. subjects by region
sub = pd.read_csv(A / "subjects_2025_2026_by_region.csv")
subjects = ["Física", "Matemáticas II", "Química", "Biología"]
regions = ["País Vasco", "Cataluña", "Madrid", "Andalucía", "Asturias"]
fig, ax = plt.subplots(figsize=(8.4, 4.0))
cols = [C["blue"], C["orange"], C["aqua"], C["yellow"], C["violet"]]
for j, (rg, col) in enumerate(zip(regions, cols)):
    d = sub[sub.region == rg]
    for i, sj in enumerate(subjects):
        v = d[d.subject == sj]
        if len(v):
            ax.scatter(v.delta, i + (j - 2) * 0.13, s=60, color=col, edgecolor=SURF, lw=1, zorder=3, label=("Euskadi" if rg == "País Vasco" else rg) if i == 0 else None)
ax.axvline(0, color=INK2, lw=1)
ax.set_yticks(range(len(subjects)))
ax.set_yticklabels(subjects)
ax.invert_yaxis()
ax.set_xlabel("Change of the ordinary-sitting mean, 2025 → 2026 (points)")
ax.legend(loc="lower left", ncol=5, bbox_to_anchor=(0, 1.0))
ax.set_title("Science subjects, 2025→2026, in the five regions with subject means for both years", pad=28)
save(fig, "fig07_subjects_by_region")

# ---------------------------------------------------------------- 8. ordinary vs extraordinary
oe = pd.read_csv(A / "ord_vs_extra_ministry.csv").dropna()
fig, ax = plt.subplots(figsize=(6.4, 5.2))
ax.scatter(oe.ordinary, oe.extraordinary, s=22, color=MUTED, alpha=0.6, label="CCAA × year, 2015–2025 (ministry)", zorder=2)
pvo = oe[oe.ccaa == "País Vasco"]
ax.scatter(pvo.ordinary, pvo.extraordinary, s=50, color=C["blue"], edgecolor=SURF, label="Euskadi 2015–2025", zorder=3)
for x, y, lab in [(6.396, 4.162, "C. Valenciana 2026"), (6.80, 3.97, "C.-La Mancha 2026"), (4.08, 3.27, "ULL 2026")]:
    ax.scatter(x, y, s=70, color=C["red"], edgecolor=SURF, zorder=4)
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(6, -4), fontsize=8, color=INK)
ax.axvline(3.99, color=C["red"], lw=1.2, ls="--")
ax.text(4.02, 6.6, "Euskadi 2026\nordinary 3.99\n(extraordinary\nnot published)", fontsize=8, color=C["red"])
xx = np.linspace(3, 9, 10)
ax.plot(xx, xx - R["ord_extra_gap"]["mean_gap_all"], color=INK2, lw=1, ls=":", label=f"y = x − {R['ord_extra_gap']['mean_gap_all']:.2f} (mean gap)")
ax.set_xlabel("Ordinary-sitting mean")
ax.set_ylabel("Extraordinary-sitting mean")
ax.set_title("The two sittings are different populations")
ax.legend(loc="lower right", fontsize=8)
ax.set_xlim(3, 9)
ax.set_ylim(1.5, 7.5)
save(fig, "fig08_ordinary_vs_extraordinary")

# ---------------------------------------------------------------- 9. gender & language (Euskadi 2010–2022)
g = pd.read_csv(A / "euskadi_gender_language.csv")
fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6), gridspec_kw=dict(wspace=0.25))
ax = axes[0]
ax.bar(g.year, g.gender_gap_f_minus_m, color=[C["magenta"] if v > 0 else C["blue"] for v in g.gender_gap_f_minus_m], width=0.7, zorder=2)
ax.axhline(0, color=INK2, lw=1)
ax.set_title("Women − men, mean grade (Euskadi Physics)")
ax.set_ylabel("Points")
ax2 = ax.twinx(); ax2.set_axis_off()
ax.text(2010, 0.45, f"women are {g.pct_mujeres_matricula.min():.0f}–{g.pct_mujeres_matricula.max():.0f} % of Physics enrolment", fontsize=8, color=INK2)
ax = axes[1]
ax.bar(g.year, g.lang_gap_eu_minus_es, color=[C["aqua"] if v > 0 else C["orange"] for v in g.lang_gap_eu_minus_es], width=0.7, zorder=2)
ax.axhline(0, color=INK2, lw=1)
ax.set_title("Euskera track − Castilian track, mean grade")
ax.text(2010, 0.22, f"euskera track share rose {g.pct_euskera_matricula.iloc[0]:.0f} % → {g.pct_euskera_matricula.iloc[-1]:.0f} %", fontsize=8, color=INK2)
for ax in axes:
    ax.set_xticks(range(2010, 2023, 2))
save(fig, "fig09_gender_language_euskadi")

# ---------------------------------------------------------------- 10. school vs PAU
fig, ax = plt.subplots(figsize=(7.2, 3.6))
labels = ["2º Bachillerato Física\n2024-25 (school marks)\nn = 4 541", "PAU Física 2025\nordinary\nn = 2 189", "PAU Física 2026\nordinary\nn = 2 066"]
means = [7.09, 5.47, 3.99]
pas = [98.11, 62.3, 39.8]
x = np.arange(3)
ax.bar(x, means, width=0.5, color=C["blue"], label="Mean grade", zorder=2)
ax.set_ylabel("Mean grade")
ax.set_ylim(0, 10)
for xi, m in zip(x, means):
    ax.text(xi, m + 0.15, f"{m:.2f}", ha="center", fontsize=9, color=INK)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.5)
ax.set_title("Same subject, three measurements: school marks vs entrance exam (Euskadi)")
for xi, p in zip(x, pas):
    ax.text(xi, 0.3, f"pass {p:.1f} %", ha="center", va="bottom", fontsize=8.5, color="white")
ax.text(-0.5, 9.4, "Sources: Gobierno Vasco 'Resultados escolares 2024-2025'; Ministry EPAU 2025; EHU 6 Jul 2026. Cohorts are offset by one year.", fontsize=6.8, color=MUTED)
save(fig, "fig10_school_vs_pau")
print("done")
