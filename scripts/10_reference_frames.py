#!/usr/bin/env python3
"""The same data, four reference frames — and four different conclusions.

Every figure in this study measures a change against some baseline, and the choice
of baseline is rarely argued for. It turns out to decide the answer. Measured from
the previous year, Spanish Física collapsed in 2025 and recovered in 2026. Measured
from the pre-COVID norm, nothing whatever happened: the nine communities that have
published a 2026 mean are +0.02 away from where they were in 2015–2019. Both
statements are true of the same numbers.

The reason is a five-year plateau. The national mean sits +0.41, +1.03, +0.63, +0.61
and +0.71 above the 2015–2019 baseline in 2020–2024 and returns to it in 2025. The
COVID relaxation did not decay year by year; it held for three years after the 2021
peak and ended in a single step. Year-on-year framing measures the end of that
plateau and calls it a collapse.

Reads : data/ministry_fisica_panel.csv, data/analysis/regions_2026_vs_2025.csv
Writes: plots/fig17_reference_frames.(png|svg), data/analysis/reference_frames.json
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

BASELINE = (2015, 2019)          # the last pre-COVID sittings
PLATEAU = (2020, 2024)           # see the module docstring: a plateau, not a decay

panel = pd.read_csv(DATA / "ministry_fisica_panel.csv")
m = panel[(panel.sitting == "ordinary") & (panel.phase == "specific")]
m = m[~m.ccaa.isin(["Total", "Estado"])].dropna(subset=["mean"])

reg26 = pd.read_csv(A / "regions_2026_vs_2025.csv")
NINE = set(reg26.ccaa)
assert m[m.ccaa.isin(NINE)].ccaa.nunique() == 9, "the nine 2026 reporters must all be in the panel"

# Everything is computed on the SAME nine communities in every year, so that no part
# of the comparison is an artefact of which regions happen to have reported.
nine = m[m.ccaa.isin(NINE)]
series = nine.groupby("year")["mean"].mean()
series.loc[2026] = float(reg26.mean_2026.mean())
base = float(series.loc[BASELINE[0]:BASELINE[1]].mean())

ehu = m[m.ccaa == "País Vasco"].set_index("year")["mean"]
ehu.loc[2026] = 3.99
ehu_base = float(ehu.loc[BASELINE[0]:BASELINE[1]].mean())

frames = [
    ("2024 → 2025, nine communities",
     float(series.loc[2025] - series.loc[2024]),
     "“A national collapse: the competency model bites.”"),
    ("2025 → 2026, nine communities",
     float(series.loc[2026] - series.loc[2025]),
     "“A recovery everywhere — so 2026 is a Basque problem.”"),
    ("2015–19 baseline → 2026, nine communities",
     float(series.loc[2026] - base),
     "“Nothing has happened: Spain is where it was a decade ago.”"),
    ("2025 → 2026, Euskadi",
     float(ehu.loc[2026] - ehu.loc[2025]),
     "“The Basque fall is 1.5 points.”"),
    ("2015–19 baseline → 2026, Euskadi",
     float(ehu.loc[2026] - ehu_base),
     "“The Basque fall is nearly 2 points — a third larger.”"),
]

fig, (ax, axl) = plt.subplots(2, 1, figsize=(11.2, 8.6),
                              gridspec_kw=dict(height_ratios=[1.35, 1.0], hspace=0.40))

# --- a. the series, with the baseline and the plateau made explicit --------------
ax.axvspan(PLATEAU[0] - 0.5, PLATEAU[1] + 0.5, color=C["yellow"], alpha=0.10, lw=0,
           zorder=0)
ax.annotate("COVID-era plateau, 2020–2024:\n+0.4 to +1.0 above baseline,\nthen one step down",
            xy=(2022, 4.55), fontsize=7.6, color="#8a6a00", ha="center")
ax.axhline(base, color=INK2, lw=1.0, ls=(0, (5, 3)), zorder=1,
           label="2015–19 baseline, nine communities (%.2f)" % base)
ax.axhline(ehu_base, color=C["violet"], lw=1.0, ls=(0, (5, 3)), alpha=0.7, zorder=1,
           label="2015–19 baseline, Euskadi (%.2f)" % ehu_base)

ax.plot(series.index[:-1], series.values[:-1], color=INK2, lw=1.8, marker="o", ms=4,
        zorder=3, label="Nine communities that published a 2026 mean")
ax.plot([2025, 2026], [series.loc[2025], series.loc[2026]], color=INK2, lw=1.8,
        ls=":", marker="o", ms=4, zorder=3)
ax.plot(ehu.index[:-1], ehu.values[:-1], color=C["violet"], lw=1.8, marker="o", ms=4,
        zorder=4, label="Euskadi (UPV/EHU)")
ax.plot([2025, 2026], [ehu.loc[2025], ehu.loc[2026]], color=C["violet"], lw=1.8,
        ls=":", marker="o", ms=4, zorder=4)
ax.scatter([2026], [ehu.loc[2026]], s=70, color=C["red"], zorder=5)
ax.annotate("2026: 3.99", xy=(2026, ehu.loc[2026]), textcoords="offset points",
            xytext=(-8, -4), ha="right", fontsize=8, color=C["red"])
ax.set_xticks(range(2015, 2027, 1))
ax.set_xlabel("Year")
ax.set_ylabel("Mean Física mark, ordinary sitting")
ax.set_title("a. The same series: a plateau that ended, not a collapse that began")
ax.legend(loc="lower left", fontsize=7.8)

# --- b. the frame ledger ---------------------------------------------------------
ypos = np.arange(len(frames))[::-1]
for y, (label, delta, reading) in zip(ypos, frames):
    colr = C["aqua"] if delta > 0.05 else (C["red"] if delta < -0.05 else MUTED)
    axl.plot([0, delta], [y, y], color=colr, lw=2.2, solid_capstyle="round", zorder=2)
    axl.scatter([delta], [y], s=46, color=colr, zorder=3)
    axl.annotate("%+.2f" % delta, xy=(delta, y), textcoords="offset points",
                 xytext=(9 if delta >= 0 else -9, -3), fontsize=8, color=colr,
                 ha="left" if delta >= 0 else "right")
    axl.annotate(reading, xy=(0.10, y - 0.34), fontsize=7.6, color=INK2, va="center")
axl.axvline(0, color=INK2, lw=1.0, zorder=1)
axl.set_yticks(ypos)
axl.set_yticklabels([f[0] for f in frames], fontsize=8)
axl.set_xlim(-2.4, 1.5)
axl.set_ylim(-0.8, len(frames) - 0.4)
axl.set_xlabel("Change in the mean Física mark (points)")
axl.set_title("b. Five ways to measure the same thing, and what each invites you to conclude")
axl.grid(axis="y", visible=False)

fig.text(0.005, 0.005,
         "Ministry EPAU, Física, ordinary sitting, specific phase. Every row of b uses "
         "the same nine communities in every year — the nine that\nhave published a 2026 "
         "mean — so no part of the comparison is an artefact of which regions reported. "
         "Dotted segments carry 2026,\nwhich is not in the ministry cube and is assembled "
         "in this study.",
         fontsize=7, color=MUTED, linespacing=1.5)
_save(fig, "fig17_reference_frames", P, dpi=200)

summary = {
    "baseline_years": list(BASELINE), "plateau_years": list(PLATEAU),
    "nine_communities": sorted(NINE),
    "nine_baseline_mean": base,
    "nine_by_year": {int(y): float(v) for y, v in series.items()},
    "euskadi_baseline_mean": ehu_base,
    "euskadi_by_year": {int(y): float(v) for y, v in ehu.items()},
    "frames": [{"frame": f, "delta": d, "reading": r} for f, d, r in frames],
}
json.dump(summary, open(A / "reference_frames.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
for f, d, r in frames:
    print(f"  {f:46} {d:+.2f}   {r}")
