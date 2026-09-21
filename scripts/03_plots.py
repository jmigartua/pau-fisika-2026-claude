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

# All styling — LaTeX text stack, sizes, colour registry — lives in the shared
# module (ThesisFigures E1); this script defines none of its own.
from plot_style import C, GRID, INK, INK2, MUTED, SURF, apply_style, bf, save as _save

apply_style()

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "data" / "analysis"
P = ROOT / "plots"
P.mkdir(exist_ok=True)
R = json.load(open(A / "results.json", encoding="utf-8"))


def save(fig, name):
    _save(fig, name, P, dpi=200)


# ---------------------------------------------------------------- 1. Euskadi series
# Rebuilt 21 September 2026 on the coordination's remarks R2 and R3 (logs/REMARKS.md).
#
# R3.  The six bands this figure used to carry — "PAU 2010–11", "PAU 2012–16",
#      "EAU (LOMCE)", "COVID", "post-COVID", "LOMLOE" — were one shading channel doing
#      three different jobs: two of them were laws, two were exam formats decided
#      locally, and two were a circumstance that is neither.  Worse, the LOMCE band
#      ended in 2019, which implied the law ended there; it did not.  The bands are now
#      two labelled rows in a ribbon between the panels: what governed the exam, and
#      what the paper actually looked like.  They deliberately do not coincide — LOMCE
#      from 2017 but the paper unchanged until 2020, and then changed for COVID rather
#      than for the law — and that non-coincidence is the reason for separating them.
#      COVID is marked as two years, not as a regime.
#
# R9.  Settled 21 September 2026 by the coordination: the darker tint covers 2020 AND
#      2021, not 2020 alone.  Two reasons.  The relief measures — reduced syllabus,
#      wider optionality, softened marking — were in force for both sittings, not for
#      the first alone.  And the series says so: 2020 is 6.45 and 2021 is 7.69, the
#      highest mean in seventeen years and 1.63 above 2022.  If one sitting were the
#      anomaly it would be 2021, so shading 2020 alone marked the wrong year.
#
# R2.  The grey Ministry line stops at 2025 because the 2026 EPAU cube is not published
#      until June 2027.  What exists for 2026 is this study's assembled cross-section of
#      the nine communities that have published a result — a different population, nine
#      against seventeen, from sources of mixed quality — so it is drawn detached, in
#      its own colour, for 2025 and 2026 only.  The two falls are then shown as arrows
#      of CHANGE, each from its own 2025 point, with the Basque-specific −1.65 as the
#      bracket between the two arrowheads.  No arrow runs between the two 2026 levels:
#      that distance is 1.87, because the series did not start level in 2025, and an
#      arrow of that length labelled −1.65 would misstate the finding by 0.22.
s = pd.read_csv(A / "euskadi_fisica_series_2010_2026.csv")
dec = json.load(open(A / "decomposition.json", encoding="utf-8"))
_brow = {r["year"]: r for r in dec["budget"]["rows"]}
FIELD = {y: _brow[y]["field"] for y in (2025, 2026)}          # the nine, Euskadi included
D_PV = _brow[2026]["total"]                                    # -1.48
D_FIELD = _brow[2026]["common"]                                # +0.17
D_SPEC = _brow[2026]["basque_specific"]                        # -1.65
BASE = 5.47                       # Euskadi 2025
CF = BASE + D_FIELD               # where Euskadi would have ended moving with the nine
# The first draft of this figure drew the bracket between the two 2026 LEVELS, 3.99 and
# 5.86, and labelled it -1.65.  That distance is 1.87: the two series did not start
# level in 2025 (5.47 against 5.69).  It is the very error R2 was written to avoid, and
# it survived one drawing.  Both arrows now leave the SAME point, Euskadi's own 2025
# mean, so the field arrow reads "where we would have ended had we moved with the nine"
# and the bracket between the two heads is exactly the -1.65 it is labelled.

# R1: one figure, two languages.  Every string that appears in the plot is in this
# table, so the Spanish documents stop carrying English axes.  The decimal separator
# is the point in both, which is the PAU convention the dossier's Spanish prose uses.
TXT01 = dict(
    en=dict(
        title="Physics in the Basque university-entrance exam, ordinary sitting, 2010–2026",
        ylab="Mean grade (0–10)", ylab2="Pass rate, % of presented",
        spain="Spain (all CCAA), Ministry cube",
        nine="the nine communities with a published 2026 result",
        eus="Euskadi (UPV/EHU)",
        covid="COVID sittings, 2020–21", covid_model="the paper they forced, kept to 2024",
        law="law", model="paper",
        laws=["PAU (RD 1892/2008)", "EAU (LOMCE)", "LOMLOE"],
        models=["two whole options A/B", "four of eight", "L1", "L2"],
        offset="the law changed in 2017; the paper, in 2020",
        key="L1 = 1 competency item + 3 × (1 of 2)   ·   L2 = 2 competency items + 2 × (1 of 2)",
        cf="had we moved\nwith the field: {cf:.2f}",
        spec="{d:+.2f}\nBasque-specific\ncomponent",
        src=("Sources: EHU annual reports (2010–22), Ministry EPAU (2023–25), EHU "
             "presentation of 6 Jul 2026 (2026). The nine communities:\nthis study's "
             "cross-section; the 2026 cube is not published until June 2027, which is "
             "why the grey line stops at 2025."),
    ),
    es=dict(
        title="Física en la prueba de acceso vasca, convocatoria ordinaria, 2010–2026",
        ylab="Nota media (0–10)", ylab2="Tasa de aprobados, % de presentados",
        spain="España (todas las CCAA), cubo del Ministerio",
        nine="las nueve comunidades con resultado de 2026 publicado",
        eus="Euskadi (UPV/EHU)",
        covid="convocatorias COVID, 2020–21", covid_model="el examen que impusieron, hasta 2024",
        law="ley", model="modelo",
        laws=["PAU (RD 1892/2008)", "EAU (LOMCE)", "LOMLOE"],
        models=["dos opciones completas A/B", "cuatro de ocho", "L1", "L2"],
        offset="la ley cambió en 2017; el examen, en 2020",
        key="L1 = 1 competencial + 3 × (1 de 2)   ·   L2 = 2 competenciales + 2 × (1 de 2)",
        cf="moviéndonos con\nel conjunto: {cf:.2f}",
        spec="{d:+.2f}\ncomponente\nespecíficamente\nvasco",
        src=("Fuentes: informes anuales de la EHU (2010–22), EPAU del Ministerio "
             "(2023–25), presentación de la EHU de 6-VII-2026 (2026). Las nueve "
             "comunidades:\nsección transversal de este estudio; el cubo de 2026 no se "
             "publica hasta junio de 2027, por lo que la línea gris termina en 2025."),
    ),
)
LAW_SPANS = [(2009.5, 2016.5), (2016.5, 2024.5), (2024.5, 2026.5)]
MODEL_SPANS = [(2009.5, 2019.5), (2019.5, 2024.5), (2024.5, 2025.5), (2025.5, 2026.5)]
LAW_C = ["#e9eef4", "#dde6ef", "#cbd9e8"]
MOD_C = ["#f2efe8", "#eae5da", "#e2dbcb", "#d8cfb9"]


def fig01(lang):
    L = TXT01[lang]
    fig = plt.figure(figsize=(9.4, 7.3))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 0.26, 0.74], hspace=0.09)
    ax = fig.add_subplot(gs[0])
    axr = fig.add_subplot(gs[1], sharex=ax)
    ax2 = fig.add_subplot(gs[2], sharex=ax)

    # --- the ribbon: two rows, law above, paper model below ----------------------
    for (a, b), lab, col in zip(LAW_SPANS, L["laws"], LAW_C):
        axr.add_patch(plt.Rectangle((a, 0.60), b - a, 0.38, color=col, lw=0))
        axr.text((a + b) / 2, 0.79, lab, ha="center", va="center", fontsize=7.2,
                 color=INK)
    for (a, b), lab, col in zip(MODEL_SPANS, L["models"], MOD_C):
        axr.add_patch(plt.Rectangle((a, 0.18), b - a, 0.38, color=col, lw=0))
        axr.text((a + b) / 2, 0.37, lab, ha="center", va="center",
                 fontsize=6.4 if len(lab) <= 3 else 7.2, color=INK)
    axr.text(2009.3, 0.79, L["law"], ha="right", va="center", fontsize=7.0, color=MUTED)
    axr.text(2009.3, 0.37, L["model"], ha="right", va="center", fontsize=7.0,
             color=MUTED)
    for x in (2016.5, 2024.5):                       # law boundaries, law row only
        axr.plot([x, x], [0.60, 0.98], color=SURF, lw=1.2, zorder=3)
    for x in (2019.5, 2024.5, 2025.5):               # model boundaries, model row only
        axr.plot([x, x], [0.18, 0.56], color=SURF, lw=1.2, zorder=3)
    # the two layers do not line up, and that is the point of separating them
    axr.annotate("", xy=(2017, 0.09), xytext=(2020, 0.09),
                 arrowprops=dict(arrowstyle="<->", color=C["orange"], lw=0.9))
    axr.text(2018.5, 0.04, L["offset"], ha="center", va="top", fontsize=6.8,
             color=C["orange"])
    axr.text(2026.5, -0.30, L["key"], ha="right", va="top", fontsize=6.4, color=MUTED)
    axr.set_ylim(-0.52, 1.02); axr.set_xlim(2009.4, 2026.6)
    axr.axis("off")

    # --- COVID: two sittings, and a paper model that outlived them ----------------
    # The pandemic sittings are 2020 and 2021: both were set under the relief measures,
    # and 2021 is the highest mean in the whole series (7.69).  The four-of-eight paper
    # they forced was then kept through 2024, so the light shading covers the life of
    # the model and the darker tint marks the two sittings that caused it.  The two
    # spans are deliberately different.
    for a in (ax, ax2):
        a.axvspan(2019.5, 2024.5, facecolor="#f7f5f1", edgecolor="none", lw=0, zorder=0)
        a.axvspan(2019.5, 2021.5, facecolor="#e9e4da", edgecolor="none", lw=0, zorder=0)
    ax.text(2020.5, 3.60, L["covid"], ha="center", va="bottom", fontsize=6.8, color=MUTED)
    ax.text(2023.0, 3.37, L["covid_model"], ha="center", va="bottom", fontsize=6.8,
            color=MUTED)

    # --- a. the means -------------------------------------------------------------
    ax.plot(s.year, s.spain_mean, color=MUTED, lw=1.6, marker="o", ms=4,
            label=L["spain"], zorder=2)
    ax.plot([2025, 2026], [FIELD[2025], FIELD[2026]], color=C["green"], lw=1.6,
            ls="--", marker="o", ms=6, mfc=SURF, mew=1.6, zorder=3, label=L["nine"])
    ax.plot(s.year, s["mean"], color=C["blue"], lw=2.2, marker="o", ms=5.5,
            label=L["eus"], zorder=4)
    ax.scatter([2026], [3.99], s=110, facecolor=C["red"], edgecolor=SURF, lw=1.5,
               zorder=5)
    for y, v, dx, dy in [(2010, 4.45, 0, -13), (2012, 6.49, 0, 9),
                         (2025, 5.47, -14, -9), (2026, 3.99, 0, -14)]:
        ax.annotate(f"{v:.2f}", (y, v), textcoords="offset points", xytext=(dx, dy),
                    ha="center", fontsize=8.5, color=INK)
    ax.annotate("7.69", (2021, 7.69), textcoords="offset points", xytext=(12, -2),
                ha="left", fontsize=8.5, color=INK)
    ax.annotate(f"{FIELD[2026]:.2f}", (2026, FIELD[2026]), textcoords="offset points",
                xytext=(2, 10), ha="center", fontsize=8.5, color=C["green"])

    # --- the two falls, as arrows of CHANGE from a common origin ------------------
    xa, xb, xbr = 2027.35, 2028.45, 2029.55
    ax.plot([2025, xb + 0.3], [BASE, BASE], color=MUTED, lw=0.9, ls=":",
            clip_on=False, zorder=1)
    ax.plot([xa - 0.35, xbr + 0.1], [CF, CF], color=C["green"], lw=0.8, clip_on=False,
            zorder=1)
    ax.plot([xa - 0.35, xbr + 0.1], [3.99, 3.99], color=C["blue"], lw=0.8,
            clip_on=False, zorder=1)
    ax.annotate("", xy=(xa, 3.99), xytext=(xa, BASE),
                arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=2.2),
                annotation_clip=False)
    ax.annotate("", xy=(xb, CF), xytext=(xb, BASE),
                arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=2.2),
                annotation_clip=False)
    ax.text(xa - 0.14, (3.99 + BASE) / 2, f"{D_PV:+.2f}", ha="right", va="center",
            fontsize=9.5, color=C["blue"], clip_on=False)
    ax.text(xb, BASE - 0.13, f"{D_FIELD:+.2f}", ha="center", va="top", fontsize=9.5,
            color=C["green"], clip_on=False)
    ax.text(xbr + 0.12, CF + 0.08, L["cf"].format(cf=CF), ha="right", va="bottom",
            fontsize=7.0, color=C["green"], linespacing=1.3, clip_on=False)
    ax.annotate("", xy=(xbr, 3.99), xytext=(xbr, CF),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.2),
                annotation_clip=False)
    ax.text(xbr + 0.18, (3.99 + CF) / 2, L["spec"].format(d=D_SPEC), ha="left",
            va="center", fontsize=8.2, color=INK2, linespacing=1.35, clip_on=False)

    ax.set_ylabel(L["ylab"])
    ax.set_ylim(3.3, 8.2)
    ax.set_xlim(2009.4, 2026.6)
    ax.legend(loc="upper left", fontsize=7.8, framealpha=0.94)
    ax.set_title(L["title"])
    plt.setp(ax.get_xticklabels(), visible=False)

    # --- b. the pass rate ---------------------------------------------------------
    ax2.plot(s.year, s.pass_pct, color=C["blue"], lw=2.2, marker="o", ms=5.5, zorder=3)
    ax2.scatter([2026], [39.8], s=110, facecolor=C["red"], edgecolor=SURF, lw=1.5,
                zorder=4)
    for y, v in [(2010, 46.3), (2021, 89.6), (2025, 62.3), (2026, 39.8)]:
        ax2.annotate(f"{v:.1f} %", (y, v), textcoords="offset points",
                     xytext=(0, 9 if v > 60 else -14), ha="center", fontsize=8.5,
                     color=INK)
    ax2.set_ylabel(L["ylab2"])
    ax2.set_ylim(30, 96)
    ax2.set_xticks(range(2010, 2027))
    ax2.tick_params(axis="x", labelrotation=45)
    fig.text(0.012, 0.012, L["src"], fontsize=6.6, color=MUTED, linespacing=1.5)
    fig.subplots_adjust(right=0.705, bottom=0.115)
    save(fig, "fig01_euskadi_series" + ("" if lang == "en" else "_es"))


fig01("en")
fig01("es")

# ---------------------------------------------------------------- 2. annual changes distribution
ch = pd.read_csv(A / "annual_changes_all_ccaa.csv")
fig, ax = plt.subplots(figsize=(8.4, 3.6))
bins = np.arange(-2.3, 2.4, 0.2)
ax.hist(ch.delta, bins=bins, color=C["blue"], alpha=0.85, edgecolor=SURF, lw=1)
ax.axvline(-1.48, color=C["red"], lw=2)
ax.text(-1.5, ax.get_ylim()[1] * 0.92, "Euskadi 2025→2026\nΔ = −1.48", ha="right", va="top", color=C["red"], fontsize=9)
ax.axvline(-0.62, color=C["orange"], lw=1.6, ls="--")
ax.text(-0.72, ax.get_ylim()[1] * 0.98, "Euskadi 2024→2025\nΔ = −0.62", ha="right", va="top", color=C["orange"], fontsize=9)
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
REG = pd.read_csv(A / "regions_2026_vs_2025.csv")
order = ["País Vasco", "Canarias", "Extremadura", "Andalucía", "Comunitat Valenciana", "Cataluña", "Castilla-La Mancha", "Madrid (Comunidad de)", "Asturias (Principado de)"]
fig, axes = plt.subplots(3, 3, figsize=(9.2, 7.2), sharex=True, sharey=True, gridspec_kw=dict(hspace=0.35, wspace=0.12))
spain = L[L.ccaa == "Total"]
for ax, c in zip(axes.flat, order):
    d = L[(L.ccaa == c) & (L.year >= 2015)]
    ax.plot(spain.year, spain["mean"], color=MUTED, lw=1.3, zorder=1)
    ax.plot(d[d.year <= 2025].year, d[d.year <= 2025]["mean"], color=C["blue"], lw=1.9, marker="o", ms=3.5, zorder=2)
    d26 = d[d.year == 2026]
    if len(d26):
        # Cataluña's 2026 figure is on the "aptes" basis, which is not the basis of the
        # ministry series: the comparison the chapter makes (+0.80) is aptes-to-aptes, so
        # the segment is drawn from the aptes 2025 value, marked hollow, rather than from
        # the ministry point. Before the audit of 20 September this panel silently drew a
        # ministry-to-aptes segment of +0.86 under a title that said "aptes basis".
        base_25 = float(REG.loc[REG.ccaa == c, "mean_2025"].iloc[0]) if c in set(REG.ccaa) \
            else float(d[d.year == 2025]["mean"].iloc[0])
        ministry_25 = float(d[d.year == 2025]["mean"].iloc[0])
        if abs(base_25 - ministry_25) > 0.005:
            ax.scatter([2025], [base_25], s=40, facecolor="none", edgecolor=C["blue"],
                       lw=1.4, zorder=4)
        col = C["red"] if d26["mean"].iloc[0] < base_25 else C["aqua"]
        ax.plot([2025, 2026], [base_25, d26["mean"].iloc[0]], color=col, lw=1.9, zorder=3)
        ax.scatter([2026], d26["mean"], s=48, facecolor=col, edgecolor=SURF, zorder=4)
        ax.text(2026.45, d26["mean"].iloc[0], f"{d26['mean'].iloc[0]:.2f}", fontsize=8, va="center", color=INK, zorder=6)
    _basis = {"Cataluña": " (2025–26 on the aptes basis)",
              "Canarias": " (2026: ULL + ULPGC)"}.get(c, "")
    ax.set_title(short.get(c, c) + _basis, fontsize=9.0)
    ax.set_ylim(3.4, 8.8)
    ax.set_xticks([2015, 2018, 2021, 2024, 2026])
    ax.tick_params(labelsize=8)
axes[0, 0].plot([], [], color=MUTED, lw=1.3, label="Spain total")
axes[0, 0].plot([], [], color=C["blue"], lw=1.9, label="Region (ministry 2015–25)")
axes[0, 0].plot([], [], marker="o", ls="", mfc="none", mec=C["blue"], ms=6,
                label="2025 on the same basis as 2026")
axes[0, 0].legend(loc="lower left", fontsize=7.0, framealpha=0.9)
# fontweight is inert under usetex, so the emphasis comes from bf() (LaTeX \textbf).
fig.suptitle(bf("Ordinary-sitting Physics mean, 2015–2026: ministry series plus the 2026 values located in this study"), fontsize=11, y=0.94)
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
            ax.scatter(v.delta, i + (j - 2) * 0.17, s=60, color=col, edgecolor=SURF, lw=1, zorder=3, label=("Euskadi" if rg == "País Vasco" else rg) if i == 0 else None)
ax.axvline(0, color=INK2, lw=1)
ax.set_yticks(range(len(subjects)))
ax.set_yticklabels(subjects)
ax.invert_yaxis()
ax.set_xlabel("Change of the ordinary-sitting mean, 2025 → 2026 (points)")
ax.legend(loc="lower left", ncol=5, bbox_to_anchor=(0, 1.0))
ax.set_title("Science subjects, 2025→2026, in the five regions with subject means for both years", pad=28)
fig.text(0.005, 0.005,
         "Each region is compared with itself on its own published basis. Madrid's values are the "
         "Comunidad de Madrid chart labels (Física +1.10); against the ministry 2025 baseline the "
         "same change is +1.05,\nwhich is the figure used in the cross-regional table and in figures 3 and 4.",
         fontsize=7, color=MUTED, linespacing=1.4)
fig.subplots_adjust(bottom=0.22)
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
ax.text(4.16, 6.45, "Euskadi 2026\nordinary 3.99\n(extraordinary\nnot published)", fontsize=8, color=C["red"], ha="left")
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
ax = axes[1]
ax.bar(g.year, g.lang_gap_eu_minus_es, color=[C["aqua"] if v > 0 else C["orange"] for v in g.lang_gap_eu_minus_es], width=0.7, zorder=2)
ax.axhline(0, color=INK2, lw=1)
ax.set_title("Euskera track − Castilian track, mean grade")
ax.set_ylabel("Points")
_lim = max(abs(g.gender_gap_f_minus_m).max(), abs(g.lang_gap_eu_minus_es).max()) * 1.35
for ax in axes:
    ax.set_xticks(range(2010, 2023, 2))
    ax.set_ylim(-_lim, _lim)
axes[0].text(2010, _lim * 0.86, f"women are {g.pct_mujeres_matricula.min():.1f}–{g.pct_mujeres_matricula.max():.1f} % of Physics enrolment", fontsize=8, color=INK2)
axes[1].text(2010, _lim * 0.86, f"euskera track share rose {g.pct_euskera_matricula.iloc[0]:.0f} % → {g.pct_euskera_matricula.iloc[-1]:.0f} %", fontsize=8, color=INK2)
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
