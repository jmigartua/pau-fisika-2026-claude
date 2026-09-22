"""How much does the Basque-specific component depend on who is in the field?

R14. Two objections were put to the nine-community comparison. The field is nine
of seventeen, so the eight that did not publish a 2026 figure might have moved it.
And Cataluña had been examining in the competency style since at least 2020
(scripts/31_catalunya_history.py), so it is a mature practice rather than a
converting system and arguably does not belong in a field used to judge a
conversion.

Both are answered the same way: not by deleting a community, which would be a
researcher's choice dressed as a measurement, but by showing what every possible
deletion does. Removing one community from a nine-point mean moves it by exactly
(x_i - mean)/8, so the whole space of single removals is small and can simply be
drawn.

Figure 33 does that, and puts the two waterfalls on top of each other so the size
of the Cataluña question is visible rather than argued about. Figure 34 is the
budget recomputed on the eight-community field, for readers who want that number
on its own.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import plot_style as _ps
from plot_style import C, INK, INK2, MUTED, SURF, apply_style, save as _save

ROOT = Path(__file__).resolve().parents[1]
PLOTS = ROOT / "plots"
A = ROOT / "data" / "analysis"
apply_style()


def save(fig, name):
    _save(fig, name, PLOTS, dpi=200)


EUS = "País Vasco"


def main() -> None:
    d = pd.read_csv(ROOT / "data" / "exam_change_vs_grade.csv")[["ccaa", "delta"]]
    d = d.set_index("ccaa")["delta"]
    mu9 = d.mean()
    comp9 = d[EUS] - mu9

    # ---- leave-one-out over the eight communities that are not Euskadi
    loo = []
    for c in d.index:
        if c == EUS:
            continue
        f = d.drop(c).mean()
        loo.append((c, f, d[EUS] - f))
    loo.sort(key=lambda r: r[2])

    # ---- the two budgets
    att = json.load(open(A / "decomposition.json"))["attribution"]
    choice = att["choice"]["central"]
    ch = att["cohort"]
    cohort = next(v for k, v in ch.items()
                  if isinstance(v, (int, float)) and -0.5 < v < 0)
    comp8 = d[EUS] - d.drop("Cataluña").mean()

    # Side by side on a screen; stacked on a page, where 12 inches of width do
    # not exist. The panel code below is the same in both.
    if _ps.PAPER:
        fig = plt.figure(figsize=(_ps.PAGE_W, _ps.PAGE_W * 1.02))
        gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.86], hspace=0.52)
        fig._pau_scale = _ps.PAGE_W / 6.6
    else:
        fig = plt.figure(figsize=(12.2, 5.0))
        gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.28)
    ax1, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    # ---- (a) every single removal
    y = np.arange(len(loo))[::-1]
    for yi, (c, f, comp) in zip(y, loo):
        col = C["red"] if c == "Cataluña" else MUTED
        ax1.plot([comp9, comp], [yi, yi], color=col, lw=1.2, alpha=0.5, zorder=2)
        ax1.scatter([comp], [yi], s=62, color=col, zorder=3)
        ax1.annotate(f"{comp:+.2f}", (comp, yi), textcoords="offset points",
                     xytext=(9, -3), fontsize=8.4,
                     color=C["red"] if c == "Cataluña" else INK2)
    ax1.axvline(comp9, color=INK, lw=1.4, zorder=1)
    ax1.annotate(f"all nine: {comp9:+.2f}", (comp9, len(loo) - 0.35),
                 ha="center", fontsize=9, color=INK)
    ax1.set_yticks(y)
    ax1.set_yticklabels([("Cataluña" if c == "Cataluña" else c) for c, _, _ in loo],
                        fontsize=8.6)
    ax1.set_xlim(-1.95, -1.36)
    ax1.set_ylim(-0.8, len(loo) - 0.05)
    ax1.set_xlabel("Basque-specific component with that community removed from the field (marks)")
    ax1.set_title("a. Every single removal, and what it does\n"
                  "the whole space of one-community choices", loc="left")
    ax1.grid(axis="y", visible=False)

    # ---- (b) the two budgets, paired bar by bar
    # Both start at 5.47 and both end at 3.99: the mark is what it is. What the
    # choice of field changes is only how the same fall is *labelled* — how much
    # of it is charged to the country and how much is left over. So the endpoints
    # carry no information here and are not drawn; the two bars that move are.
    start = 5.47
    names = ["Común al\nconjunto", "Elección\nretirada", "Promoción\n(PISA)", "Sin\nidentificar"]
    cols = [C["aqua"], C["blue"], C["yellow"], C["red"]]
    variants = [("las nueve", comp9, -0.19, 1.00),
                ("las ocho, sin Cataluña", comp8, 0.19, 0.62)]
    for label, comp, off, alpha in variants:
        rem = comp - choice - cohort
        deltas = [d[EUS] - comp, choice, cohort, rem]
        for i_, (dd, cc) in enumerate(zip(deltas, cols)):
            ax2.bar(i_ + off, dd, 0.36, color=cc, alpha=alpha,
                    edgecolor=SURF, lw=0.7, zorder=2)
            if i_ in (0, 3):
                ax2.annotate(f"{dd:+.2f}", (i_ + off, dd + (0.06 if dd > 0 else -0.10)),
                             ha="center", va="bottom" if dd > 0 else "top",
                             fontsize=8.6, color=INK)
        ax2.scatter([], [], s=70, color=INK2, alpha=alpha,
                    label=f"campo = {label}:  {comp:+.2f}")
    ax2.axhline(0, color=INK, lw=0.9)
    ax2.set_xticks(range(4))
    ax2.set_xticklabels(names, fontsize=8.6)
    ax2.set_ylabel("Marks")
    ax2.set_ylim(-1.62, 0.42)
    ax2.legend(loc="lower left", fontsize=8.4, framealpha=0.92)
    ax2.set_title("b. The same fall, labelled two ways\n"
                  f"only two bars move, and by {abs(comp8 - comp9):.2f} marks", loc="left")
    ax2.grid(axis="x", visible=False)

    fig.text(0.005, 0.006,
             "Removing one community from a nine-point mean moves it by (x − mean)/8; "
             "for Cataluña that is 0.08. Panel a shows every such removal, panel b the two "
             "budgets drawn together.\nNo single removal changes a conclusion: the component "
             f"ranges from {min(r[2] for r in loo):+.2f} to {max(r[2] for r in loo):+.2f} "
             f"against {comp9:+.2f} as published.",
             fontsize=7, color=MUTED, linespacing=1.5)
    fig.subplots_adjust(bottom=0.20, top=0.87, left=0.13, right=0.985)
    save(fig, "fig33_field_sensitivity")

    # ---------------------------------------------------------------- figure 34
    fig2, ax = plt.subplots(figsize=(8.6, 4.8))
    rem8 = comp8 - choice - cohort
    labels = ["Euskadi 2025", "Común a\nlas ocho", "Elección\nretirada",
              "Promoción\n(PISA)", "Sin\nidentificar", "Euskadi 2026"]
    deltas = [d[EUS] - comp8, choice, cohort, rem8]
    cols = [C["aqua"], C["blue"], C["yellow"], C["red"]]
    end = start + sum(deltas)
    lo, hi = min(end, start + sum(deltas)) - 0.55, start + 0.55

    def cap(x, v):
        ax.plot([x - 0.28, x + 0.28], [v, v], color=INK2, lw=5.0,
                solid_capstyle="butt", zorder=3)

    ax.axhline(start, color=MUTED, lw=0.9, ls=":")
    ax.axhline(end, color=MUTED, lw=0.9, ls=":")
    cap(0, start)
    ax.annotate(f"{start:.2f}", (0, start + 0.10), ha="center", fontsize=10, color=INK)
    level = start
    for i_, (dd, cc) in enumerate(zip(deltas, cols), start=1):
        bottom = level + min(dd, 0)
        ax.bar(i_, abs(dd), 0.56, bottom=bottom, color=cc)
        ax.annotate(f"{dd:+.2f}", (i_, bottom + abs(dd) / 2), ha="center", va="center",
                    fontsize=9.5, color="white" if abs(dd) > 0.3 else INK)
        ax.plot([i_ - 0.28, i_ + 0.72], [level + dd, level + dd], color=MUTED, lw=0.8, zorder=1)
        level += dd
    cap(5, end)
    ax.annotate(f"{end:.2f}", (5, end + 0.10), ha="center", fontsize=10, color=INK)
    ax.set_xticks(range(6))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Mean Física mark")
    ax.set_ylim(lo, hi)
    ax.set_title("Cataluña removed from the field: the same budget, one comparator fewer", loc="left")
    ax.annotate(f"Específicamente vasco: {comp8:+.2f} (frente a {comp9:+.2f} con las nueve).  "
                f"Sin atribuir: {abs(rem8):.2f} ({100*rem8/comp8:.0f} %).",
                xy=(0.5, hi - 0.16), fontsize=9, color=C["red"], ha="left")
    fig2.text(0.005, 0.006,
              "Cataluña has examined in the competency style since at least 2020, so it is a mature "
              "practice and not a converting system. Removing it is defensible and is shown here; it "
              "moves the component by 0.08 marks.\nThe published figure keeps all nine, because a field "
              "is meant to measure the national movement rather than to be a matched control, and "
              "because selecting comparators by their papers is a free parameter.",
              fontsize=7, color=MUTED, linespacing=1.5)
    fig2.subplots_adjust(bottom=0.22, top=0.90, left=0.10, right=0.985)
    save(fig2, "fig34_budget_no_catalunya")

    out = {
        "field_nine": mu9, "component_nine": comp9,
        "field_eight_no_catalunya": float(d.drop("Cataluña").mean()),
        "component_eight_no_catalunya": comp8,
        "difference": comp8 - comp9,
        "leave_one_out": {c: {"field": f, "component": comp} for c, f, comp in loo},
        "range": [min(r[2] for r in loo), max(r[2] for r in loo)],
    }
    (A / "field_sensitivity.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False)[:700])


if __name__ == "__main__":
    main()
