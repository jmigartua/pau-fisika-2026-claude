"""The examination week as a designed object: what moved in the calendar, and
what the weighting table pays for.

Finding 19 has two halves and they are usually run together, which is why the
usual "Física is sat last" argument gets nowhere. This figure keeps them apart.

Panel a is the calendar. Position is a constant and differences out; what has to
be shown is a *change*. Matemáticas II left the Wednesday morning for the slot
forty-five minutes before Física, so for the first time the two heaviest
quantitative papers were sat back to back. The four subject changes partition
along exactly that pairing — and the panel says so and no more, because
"adjacent" and "hardest" name the same two papers and the contrast has two
observations a side.

Panel b is the weighting table. Física weights 0.2 in 28 of 37 relevant degrees,
which reads as demand and is the reverse of demand once the rule printed at the
head of every page is applied: only the two most favourable marks count, and
Matemáticas II is compulsory in the access phase and carries forward. One of the
two slots is therefore filled before any elective is chosen, and the second is
contested. The panel counts how often that contest exists.

Sources: data/analysis/ponderaciones_ehu_2026.json (coded from the UPV/EHU
parameters document); the calendar table in chapters/06-interpretation.qmd.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

from plot_style import C, DECK, INK, INK2, MUTED, SURF, T, apply_style, save as _save

ROOT = Path(__file__).resolve().parents[1]
apply_style()

# subject, day index (0 = Tue, 1 = Wed), start, end, Δ mean 2025→2026, day certain
Y2025 = [("Química",        0, 14.50, 16.00, -0.21, True),
         ("Biología",       1, 14.50, 16.00, +0.15, False),
         ("Matemáticas II", 1, 11.25, 12.75, -1.67, True),
         ("Física",         1, 16.50, 18.00, -1.48, False)]
Y2026 = [("Química",        0, 16.75, 18.25, -0.21, True),
         ("Biología",       0, 14.50, 16.00, +0.15, True),
         ("Matemáticas II", 1, 14.50, 16.00, -1.67, True),
         ("Física",         1, 16.75, 18.25, -1.48, True)]


def _hhmm(h):
    return "%d:%02d" % (int(h), round((h - int(h)) * 60))


def _calendar(ax):
    """Both years on one time axis: four columns, 2025 then 2026.

    Drawing the years as two separate axes gave each its own invisible y-scale
    and put two "14:30" labels a centimetre apart on different panels, which is
    exactly the confusion the figure exists to remove. One axis, one clock.
    """
    cols = [(0.0, "2025", "martes"), (1.0, "2025", "miércoles"),
            (2.6, "2026", "martes"), (3.6, "2026", "miércoles")]
    ax.set_xlim(-0.95, 4.70)
    ax.set_ylim(19.35, 9.75)
    for h in (11, 12, 13, 14, 15, 16, 17, 18):
        ax.axhline(h, color=MUTED, lw=0.45, alpha=0.30, zorder=0)
        ax.text(-1.0, h, _hhmm(h), ha="right", va="center", fontsize=7.4, color=MUTED)
    ax.axvline(1.8, color=MUTED, lw=0.8, alpha=0.55, zorder=1)
    for x, yr, day in cols:
        ax.text(x, 10.62, T(day), ha="center", va="bottom", fontsize=8.6, color=INK2)
    for x, yr in ((0.5, "2025"), (3.1, "2026")):
        ax.text(x, 10.02, yr, ha="center", va="bottom", fontsize=11.5, color=INK,
                fontweight="bold")

    for rows, base in ((Y2025, 0.0), (Y2026, 2.6)):
        for name, d, a, b, delta, certain in rows:
            x = base + d
            col = C["red"] if delta <= -1.0 else (C["orange"] if delta < 0 else C["blue"])
            heavy = name in ("Matemáticas II", "Física")
            ax.add_patch(Rectangle((x - 0.42, a), 0.84, b - a, facecolor=col,
                                   alpha=0.92 if heavy else 0.52,
                                   edgecolor=INK if heavy else col,
                                   lw=1.3 if heavy else 0.9,
                                   ls="-" if certain else (0, (3, 2)), zorder=3))
            ax.text(x, (a + b) / 2 - 0.16, name, ha="center", va="center",
                    fontsize=8.4, color="white",
                    fontweight="bold" if heavy else "normal", zorder=4)
            ax.text(x, (a + b) / 2 + 0.30, "%+.2f" % delta, ha="center", va="center",
                    fontsize=8.0, color="white", zorder=4)

    # the 2026 adjacency
    ax.add_patch(FancyArrowPatch((4.20, 16.00), (4.20, 16.75),
                                 arrowstyle="<|-|>", mutation_scale=9,
                                 color=INK, lw=1.2, zorder=5))
    ax.text(4.28, 16.38, T("45 min"), ha="left", va="center", fontsize=8.0,
            color=INK, fontweight="bold", rotation=90)
    # Routed through the empty 13:00 band between the two Matemáticas II blocks,
    # rather than over the top of the panel where the year labels live.
    ax.annotate("", xy=(3.60, 14.35), xytext=(1.46, 12.05),
                arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.4,
                                connectionstyle="arc3,rad=-0.28"), zorder=5)
    ax.text(2.52, 12.72, T("Matemáticas II\nse mueve aquí"), ha="center", va="center",
            fontsize=8.2, color=C["red"], fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", fc=SURF, ec="none", alpha=0.92))
    ax.text(-0.95, 19.05,
            T("borde discontinuo: las dos fuentes de 2025\nno coinciden en el día"),
            fontsize=7.2, color=MUTED, va="bottom", ha="left")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    # Standing alone on a slide, the panel letter points at a panel that is not
    # there, so it goes — the same convention figure 25 already uses.
    _ta = T("a. What moved in the examination week")
    ax.set_title(_ta[3:] if DECK else _ta, loc="left")
    ax.text(-0.95, 18.50, T("the two papers made adjacent are the two that fell"),
            fontsize=8.8, color=INK, fontweight="bold", va="bottom", ha="left")


def main() -> None:
    pond = json.load(open(ROOT / "data" / "analysis" / "ponderaciones_ehu_2026.json"))

    # The dossier gets one figure with both halves of finding 19 side by side.
    # The deck gets them as two, because they belong on two different slides —
    # the calendar is a fact about 2026, the weighting table is a candidate
    # mechanism for 2024 — and because a 16:9 slide has no room for both.
    if DECK:
        fig = plt.figure(figsize=(9.4, 5.0))
        _calendar(fig.add_subplot(111))
        fig.text(0.005, 0.005,
                 T("UPV/EHU timetables for the ordinary sitting, with each subject's change in "
                   "mean beneath its name. Física's own slot did not move — it was last on its "
                   "day in both years — so what being last\ncosts differences out. What changed is "
                   "what precedes it. The contrast is confounded and enters no budget: the pair "
                   "made adjacent is also the pair that is most quantitative."),
                 fontsize=7, color=MUTED, linespacing=1.5)
        fig.subplots_adjust(left=0.055, right=0.985, top=0.90, bottom=0.135)
        _save(fig, "fig40_timetable_weights", ROOT / "plots")
        fig = plt.figure(figsize=(9.6, 4.6))
        ab = fig.add_subplot(111)
    else:
        fig = plt.figure(figsize=(11.4, 5.1))
        gs = fig.add_gridspec(1, 2, width_ratios=[1.30, 1.0], wspace=0.14)
        _calendar(fig.add_subplot(gs[0]))
        ab = fig.add_subplot(gs[1])

    # ------------------------------------------------------------- panel b
    n = pond["n_degrees_coded"]
    steps = [
        (T("grados de Ciencias, Ingeniería\ny Ciencias de la Salud codificados"), n, MUTED),
        (T("Física pondera $0.2$"), pond["n_fisica_02"], C["blue"]),
        (T("…y Matemáticas II también"), pond["n_fisica_and_matii_02"], C["orange"]),
        (T("…y Química también:\nlas tres a $0.2$, y solo caben dos"), pond["n_fisica_matii_quim_all_02"], C["red"]),
    ]
    ys = range(len(steps))[::-1]
    for y, (lab, v, col) in zip(ys, steps):
        ab.barh(y, v, color=col, height=0.40, zorder=2, alpha=0.9)
        ab.text(v + 0.6, y, str(v), va="center", fontsize=10.5, color=INK,
                fontweight="bold")
        # The step labels go above their own bar, inside the panel. Hung off the
        # left in data coordinates they ran out of the axes and over the calendar.
        ab.text(0.0, y + 0.40, lab, va="bottom", ha="left", fontsize=8.6, color=INK2)
    ab.set_xlim(0, n * 1.12)
    ab.set_ylim(-1.75, len(steps) - 0.20)
    ab.set_yticks([])
    ab.set_xlabel(T("grados (de 37)"))
    _tb = T("b. “Se utilizarán las 2 calificaciones que sean más favorables”")
    ab.set_title(_tb[3:] if DECK else _tb, loc="left")
    ab.text(0.0, -0.80,
            T("Matemáticas II es obligatoria en la fase de acceso y se arrastra:\n"
              "una de las dos plazas está ocupada antes de elegir nada.\n"
              "En Ciencias de la Salud, Física pondera $0.1$ y Biología y Química $0.2$:\n"
              "ahí no hay contienda — Física no entra."),
            fontsize=8.0, color=INK2, ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=MUTED, lw=0.7), zorder=5)
    for sp in ("top", "right", "left"):
        ab.spines[sp].set_visible(False)

    fig.text(0.005, 0.005,
             T("Panel b: the weighting parameters for 2026-27, coded degree by degree for the "
               "three branches in which Física appears at all. Only the two most favourable "
               "marks count, and Matemáticas II is compulsory in the access phase.")
             if DECK else
             T("Panel a: UPV/EHU timetables for the ordinary sitting, 2025 and 2026, with each subject's change in mean beneath its name. Física's own slot did not move — it was last on its day in both years — "
               "so what being last costs\ndifferences out. What changed is what precedes it. The contrast is confounded: the pair made adjacent is also the pair that is most quantitative and whose own papers changed most, and it enters no "
               "budget.\nPanel b: the weighting parameters for 2026-27, coded degree by degree for the three branches in which Física appears at all."),
             fontsize=7, color=MUTED, linespacing=1.5)
    if DECK:
        fig.subplots_adjust(left=0.035, right=0.985, top=0.90, bottom=0.145)
        _save(fig, "fig41_weighting_table", ROOT / "plots")
    else:
        fig.subplots_adjust(left=0.055, right=0.985, top=0.90, bottom=0.175)
        _save(fig, "fig40_timetable_weights", ROOT / "plots")


if __name__ == "__main__":
    main()
