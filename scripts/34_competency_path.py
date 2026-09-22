"""Where each community moved in the competency–outcome plane, 2025 to 2026.

The scatter panels of figure 11 plot one year against one change. They cannot
show a *route*, and the route is what the Cataluña archive turned into the
question: two systems can arrive at similar competency content having come from
opposite directions and from different distances.

So each community is drawn as an arrow from (competency share 2025, mean 2025) to
(competency share 2026, mean 2026). One measure throughout — the competency-coded
share of the paper's expected marks — so the horizontal axis means the same thing
for every arrow.

What the figure is for: Euskadi's arrow runs right and steeply down; Cataluña's
runs left and slightly up; six communities have no horizontal component at all
because they were at zero in both years and stayed there. The note on Cataluña
records what the arrow cannot: it had been near its 2025 position since at least
2020 (scripts/31_catalunya_history.py), so its leftward arrow is a retreat from a
mature practice and not the reversal of a conversion.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plot_style import C, INK, INK2, MUTED, SURF, apply_style, save as _save

ROOT = Path(__file__).resolve().parents[1]
PLOTS = ROOT / "plots"
apply_style()

SHORT = {"País Vasco": "Euskadi", "Castilla-La Mancha": "C.-La Mancha",
         "Comunitat Valenciana": "C. Valenciana",
         "Madrid (Comunidad de)": "Madrid", "Asturias (Principado de)": "Asturias"}
OFFS = {"Euskadi": (8, -14), "Cataluña": (-10, 8), "C.-La Mancha": (8, 4),
        "Canarias": (11, -2), "Extremadura": (-11, -9), "Asturias": (8, 2),
        "Madrid": (8, -10), "Andalucía": (8, 2), "C. Valenciana": (-8, 8)}


def main() -> None:
    d = pd.read_csv(ROOT / "data" / "exam_change_vs_grade.csv")
    d["label"] = d.ccaa.map(lambda c: SHORT.get(c, c))

    fig, ax = plt.subplots(figsize=(9.2, 6.0))
    ax.axhline(0, color=MUTED, lw=0.9, ls="--", zorder=1)

    for r in d.itertuples():
        x0, x1 = r.comp_exp_2025, r.comp_exp_2026
        y0, y1 = 0.0, r.delta                      # change measured from its own 2025
        col = C["red"] if r.label == "Euskadi" else (
            C["violet"] if r.label == "Cataluña" else (
                C["orange"] if r.delta < 0 else C["blue"]))
        moved = abs(x1 - x0) > 0.01
        if moved:
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="-|>", lw=2.0, color=col,
                                        shrinkA=3, shrinkB=3,
                                        connectionstyle="arc3,rad=0.12"), zorder=3)
        else:
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="-|>", lw=1.4, color=col,
                                        alpha=0.6, shrinkA=3, shrinkB=3), zorder=2)
        ax.scatter([x0], [y0], s=26, facecolor=SURF, edgecolor=col, lw=1.4, zorder=4)
        ax.scatter([x1], [y1], s=74, color=col, zorder=5)
        # Extremadura (-0.82) and Canarias (-0.83) coincide at zero competency to
        # within a hundredth, so their markers sit on top of one another. Labelling
        # them separately would invite the reader to tell apart two points that are
        # not distinguishable on the page; they get one label instead.
        if r.label in ("Extremadura", "Canarias"):
            continue
        off = OFFS.get(r.label, (8, 3))
        ax.annotate(r.label, (x1, y1), textcoords="offset points", xytext=off,
                    ha="right" if off[0] < 0 else "left", fontsize=8.8,
                    color=INK if r.label in ("Euskadi", "Cataluña") else INK2)

    ax.annotate("Extremadura $-0.82$\nCanarias $-0.83$", (0, -0.825),
                textcoords="offset points", xytext=(12, -2), ha="left",
                fontsize=8.8, color=INK2, va="center")

    ax.annotate("its 2025 paper: it had been\nnear here since at least 2020",
                xy=(75, 0.04), xytext=(71, 0.70), fontsize=8.2, color=C["violet"],
                ha="center", arrowprops=dict(arrowstyle="->", color=C["violet"], lw=0.9))
    ax.annotate("six communities at zero\nin both years", xy=(0, 0.6), xytext=(9, 1.15),
                fontsize=8.2, color=MUTED, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))

    ax.set_xlabel("Competency-coded share of the paper's expected marks (%)")
    ax.set_ylabel("Change in the ordinary-sitting Física mean, 2026 − 2025 (marks)")
    ax.set_xlim(-6, 86)
    ax.set_ylim(-1.85, 1.55)
    ax.set_title("Each community's route, 2025 → 2026: hollow point is 2025, filled point 2026",
                 loc="left")
    fig.text(0.005, 0.012,
             "One measure on the horizontal axis throughout: the competency-coded share of expected marks, "
             "from the item coding of the eighteen ordinary papers.\nThe vertical axis is each community's own "
             "change, so every arrow starts at zero. Euskadi runs right and down; Cataluña runs left and up, "
             "from a position it had held for five years.",
             fontsize=7, color=MUTED, linespacing=1.5)
    fig.subplots_adjust(bottom=0.155, top=0.93, left=0.105, right=0.985)
    _save(fig, "fig36_competency_path", PLOTS, dpi=200)


if __name__ == "__main__":
    main()
