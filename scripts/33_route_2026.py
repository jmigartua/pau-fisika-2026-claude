"""Could a candidate prepared the old way still sit the 2026 paper that way?

R15. The reopened syllabus is usually described as the moment students met
material they had never been taught. For the June 2026 sitting — the one that
produced 3.99 — that description is wrong, and the paper itself says so.

Every genuinely new sub-topic sat in an OPTIONAL slot with a heavily drilled
alternative beside it, and the two slots that offered no choice were set on sub-topics from
the top of the sixteen-year frequency table. A candidate could answer 1, 2, 3b
and 4a and never touch anything new.

That matters for attribution. If the novelty was avoidable and the mean still
fell 1.48, then meeting unfamiliar content cannot be what happened in June. What
could not be avoided was the genre of the two no-choice slots, the marking
regime in its second year, the reading load, and the disappearance of the theory
block. The inertia argument survives, but it relocates: from content the students
met to preparation spread thinner across a syllabus that had to be covered
because nobody could know what would be set, and to familiar physics presented in
an unfamiliar way.

July is drawn alongside because it is the counter-case: there slot 2 offered no
choice and was a mass spectrometer, never set before.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import plot_style as _ps
from plot_style import C, INK, INK2, MUTED, SURF, apply_style, save as _save

ROOT = Path(__file__).resolve().parents[1]
PLOTS = ROOT / "plots"
apply_style()


def main() -> None:
    d = pd.read_csv(ROOT / "data" / "ehu_problem_inventory_2010_2026.csv")
    rec = d[(d.year >= 2010) & (d.year <= 2024)]["sub"].value_counts()

    fig, axes = plt.subplots(1, 2, figsize=(12.6, 4.4), sharex=True)
    for ax, sitting, title in zip(axes, ["ord", "extra"],
                                  ["a. June 2026 — every novelty sat where there was a choice",
                                   "b. July 2026 — one novelty did not"]):
        s = d[(d.year == 2026) & (d.sitting == sitting)]
        labels, vals, cols, marks = [], [], [], []
        for r in s.itertuples():
            n = int(rec.get(r.sub, 0))
            labels.append(f"{r.slot}  {r.subtopic[:32]}")
            vals.append(n)
            cols.append(C["red"] if r.obligatory else (MUTED if n == 0 else C["blue"]))
            marks.append(bool(r.obligatory))
        y = np.arange(len(vals))[::-1]
        ax.barh(y, vals, color=cols, height=0.62)
        for yi, v, ob in zip(y, vals, marks):
            ax.text(v + 0.35, yi, f"{v}×", va="center", fontsize=8.4,
                    color=INK if ob else INK2)
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=8.2)
        ax.set_xlim(0, 20.5)
        ax.set_xlabel("times that sub-topic had been set, 2010–2024")
        ax.set_title(title, loc="left")
        ax.grid(axis="y", visible=False)

    from matplotlib.patches import Patch
    axes[1].legend(handles=[Patch(color=C["red"], label="no optionality"),
                            Patch(color=C["blue"], label="with choice, set before"),
                            Patch(color=MUTED, label="with choice, never set before")],
                   loc="lower right", fontsize=8, frameon=False)
    axes[0].annotate("a candidate could answer 1, 2, 3b and 4a —\n"
                     "four sub-topics set 47 times between them",
                     xy=(0.97, 0.06), xycoords="axes fraction", ha="right", va="bottom",
                     fontsize=8.4, color=INK,
                     bbox=dict(boxstyle="round,pad=0.45", fc=SURF, ec=C["blue"], lw=0.9))
    fig.suptitle("The 2026 papers against sixteen years of their own precedent; "
                 "how often each 2026 sub-topic had been set before",
                 x=0.005, ha="left", fontsize=11)
    fig.text(0.005, 0.01,
             "The two June slots that offered no choice were on sub-topics ranked 1st and 11th of 15 by frequency; "
             "the two never-set sub-topics both sat where a choice was offered, each beside an alternative set 10 and 14 times.\n"
             "The reopened syllabus was therefore avoidable in June. What could not be avoided was the genre of "
             "the two no-choice slots, the marking regime, the reading load, and the loss of the theory block.",
             fontsize=7, color=MUTED, linespacing=1.5)
    fig.subplots_adjust(bottom=0.26, top=0.83, left=0.235, right=0.99, wspace=0.62)
    _save(fig, "fig35_route_2026", PLOTS, dpi=200)


if __name__ == "__main__":
    main()
