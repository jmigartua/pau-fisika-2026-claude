#!/usr/bin/env python3
"""How the penalties are SPREAD across candidates, and why the flat model is a ceiling.

Script 26 asks whether the change of marking regime is capable of producing the four
published 2026 figures.  It answers yes, at about twelve deductions of 0.10 per script.
But it applies those twelve to everybody: every candidate has the same expected count,
independent of how well the physics is done.  That is not what anybody thinks happens.
A candidate who handles units, vectors, prefixes and rounding well will collect few
deductions; a candidate who is weak in physics and weak in general will collect many.
The count per script ought to be a DISTRIBUTION, heaviest somewhere below the middle
and thinning towards the top.

This script asks what that costs, and the answer has a clean structure.

  A deduction of 0.10 removes a full 0.10 only if the sub-task it lands on is still
  worth at least that much to that candidate.  On a strong script every sub-task is
  nearly full, so every deduction lands in full.  On a weak script the sub-tasks are
  already worth 0.05 or 0.02, and the zero floor absorbs the rest: the mark cannot go
  below zero, so part of the penalty is spent on nothing.

  The single quantity that governs how much a deduction is worth is therefore not the
  shape's name but HOW MUCH OF THE PENALTY MASS LANDS ON WORK THAT IS ALREADY WORTH
  ALMOST NOTHING.  Across the shapes tested, the marks removed per deduction fall
  monotonically in the share of penalties landing on scripts below four out of ten.

  The flat model sits at exactly the proportionate share, because every script has the
  same expected count.  So any shape that sends MORE than its proportionate share of
  penalties to the weakest scripts — which is precisely the reading the coordination
  proposed, and precisely what one would expect of candidates who are weak in physics
  and weak in general — removes fewer marks per deduction than the flat model.  At a
  fixed number of penalties, flat is the CEILING over that family.

  It is not the ceiling over every conceivable shape, and the script says so.  A shape
  that SPARES the weakest — a symmetric hump light at both ends, or an outright tilt
  towards the best scripts — removes MORE per deduction, because none of its penalties
  is wasted on work with nothing left to take.  Both are reported.  Neither is a
  reading anybody has offered: the claim on the table is that the weak collect more
  penalties, not fewer, and over that claim flat is the bound.

  Over-dispersion works the same way.  Giving scripts unequal rates at the same average
  — some collecting many penalties, some almost none — also lowers the marks removed
  per deduction, because the scripts that collect many run out of marks to lose.  Equal
  and flat is the most expensive way to spend a fixed number of penalties.

The consequence for the dossier is the one that matters.  If the regime is read flat,
it can carry the whole of the year-on-year fall and there is nothing left to explain.
If it is read as a distribution — which is the realistic reading — it carries less, and
the remainder is left for the other components the analysis has isolated: the part of
the fall that is not Física's at all, the reading load, the optionality, the paper.
The flat number is the maximum the regime can be worth at a given count; the
distributed number is what it is plausibly worth; the difference is the room the rest
of the analysis needs, and the dossier does not have to claim that room, only to leave
it open.

A second consequence is a test.  Flat and distributed shapes can both be made to fit
the four published figures — mean, pass rate, share at or below two, share at zero —
or nearly so, because the count and the voiding absorb the difference.  They separate
by a factor of more than twenty on the FIFTH figure, the share at or above nine, which Euskadi
has not published for 2026.  So the top band is the statistic that discriminates
between a flat regime and a distributed one, and that is one more reason, and a sharp
one, to ask for the 2026 band table.

Reads : data/analysis/euskadi_grade_bands_2015_2025.csv, data/analysis/results.json
Writes: data/analysis/penalty_shape.json, data/tables/penalty_shape.md,
        data/tables/penalty_budget.md, plots/fig31_penalty_shape.(png|svg)
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

from plot_style import C, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "data" / "analysis"
TABLES = ROOT / "data" / "tables"
PLOTS = ROOT / "plots"

# The model is imported from script 26 rather than copied, so the two cannot drift.
_spec = importlib.util.spec_from_file_location(
    "penalty_regime", Path(__file__).resolve().parent / "26_penalty_regime.py")
PR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PR)

N = 200_000
OBS_2026 = PR.OBS_2026
OBS_2025 = PR.OBS_2025
FALL = -1.48            # the observed year-on-year change in the Basque Física mean
FISICA_SPECIFIC = -1.10  # the part of it that the subject split assigns to Física
BETA_TOP_2026 = 0.0209   # MODELLED, not published: see the note below

# The shapes.  w(a) = a^(p-1) (1-a)^(q-1) in the candidate's own level a = mark/10,
# normalised to mean one, so the mean count per script is the same in every row and
# only the spread changes.
SHAPES = [
    ((1.0, 1.0), "flat — every script the same expected count"),
    ((1.0, 2.0), "tilted to the weak — count falls linearly with the mark"),
    ((1.0, 3.0), "strongly tilted to the weak — heaviest at the very bottom"),
    ((2.0, 2.0), "hump in the middle — symmetric, light at both ends"),
    ((1.5, 3.0), "middle and left — peak at about 2, thin above 7"),
    ((2.0, 3.0), "middle, leaning left — peak at about 3.3"),
    ((3.0, 1.0), "tilted to the STRONG — reported only to bound the claim"),
]
# The reading on the table: the weakest scripts collect AT LEAST their
# proportionate share of the penalties. Membership is tested, not assumed.
WEAK_CUT = 4.0

# The fitted regime from script 26, held fixed so that only the shape varies.
FIT = dict(ded_rate=12, p_partial=0.16, p_total=0.030)


def profile(shape, tot=None, n=200_000):
    """Where a shape sends its penalties, and how concentrated it is.

    `mass_below` is the share of the total expected penalty count that lands on
    scripts scoring below WEAK_CUT out of ten. For the flat shape it equals the share
    of scripts below that mark, by construction; a shape above that value sends more
    than its proportionate share to the weakest work, which is the family the
    coordination's reading belongs to.
    """
    if tot is None:
        tot = PR.baseline_scores(n)
    a = np.clip(tot / 10.0, 1e-3, 1 - 1e-3)
    pw, qw = shape
    w = a ** (pw - 1.0) * (1.0 - a) ** (qw - 1.0)
    w = w / w.mean()
    return dict(
        mass_below=float(w[tot < WEAK_CUT].sum() / w.sum() * 100),
        mass_below_2=float(w[tot < 2.0].sum() / w.sum() * 100),
        top_decile_rate=float(w[tot >= 8.0].mean()),
        peak_at=float(np.clip((pw - 1) / (pw + qw - 2), 0, 1) * 10)
        if (pw + qw) > 2 else float("nan"),
    )


def run(shape, ded_rate, voiding=True, overdispersion=None, n=N, fit=None):
    f = fit or FIT
    kw = dict(ded_mode="shape", shape=shape, overdispersion=overdispersion, n=n)
    if voiding:
        return PR.simulate(ded_rate, f["p_partial"], f["p_total"], **kw)
    return PR.simulate(ded_rate, 0.0, 0.0, **kw)


def invert_shift(shape, target, overdispersion=None, n=60_000, hi=90.0):
    """Mean deductions per script that this shape needs to carry `target` marks."""
    lo = 0.0
    for _ in range(30):
        mid = (lo + hi) / 2
        s = run(shape, mid, voiding=False, overdispersion=overdispersion, n=n)["shift"]
        lo, hi = (mid, hi) if s > target else (lo, mid)
    return (lo + hi) / 2


def refit(shape, n=25_000):
    """Refit the whole regime for this shape, so the losses are comparable.

    An earlier version held the voiding parameters at the values fitted under the FLAT
    model and then compared losses, which loads the comparison against every other
    shape. Here each shape gets its own three numbers.
    """
    best = None
    for ded in (8, 10, 13, 16, 20, 25, 31, 38):
        for pp in (0.0, 0.02, 0.04, 0.10, 0.16, 0.24, 0.34):
            for pt in (0.0, 0.005, 0.010, 0.025, 0.040, 0.060):
                r = PR.simulate(ded, pp, pt, ded_mode="shape", shape=shape, n=n)
                L = PR.loss(r)
                if best is None or L < best[0]:
                    best = (L, dict(ded_rate=ded, p_partial=pp, p_total=pt))
    f = best[1]
    r = PR.simulate(f["ded_rate"], f["p_partial"], f["p_total"],
                    ded_mode="shape", shape=shape, n=100_000)
    r["loss"] = float(PR.loss(r))
    r["on_grid_boundary"] = bool(f["ded_rate"] in (8, 38) or f["p_partial"] in (0.0, 0.34)
                                 or f["p_total"] in (0.0, 0.060))
    return r


def write_tables(at12, budget, disc, need, flat, rho, top_range, top_range_all):
    """The three tables. Split out so they can be rewritten from the JSON alone."""
    L = ["| Shape | Penalties below 4/10 | Shift | Marks per deduction | "
         "Relative to flat | Pass % | At or above 9 % |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for r in at12:
        L.append(f"| {r['label']} | {r['mass_below']:.0f} % | {r['shift']:+.2f} | "
                 f"{r['marks_per_deduction']:.3f} | {r['relative_to_flat']*100:.0f} % | "
                 f"{r['pass_pct']:.1f} | {r['top_pct']:.2f} |")
    L += ["", f"Twelve deductions of 0.10 per script on average in **every** row, with "
          "the voiding channel switched off so that only the deduction channel is in "
          "view. The rows differ only in how those twelve are spread across "
          "candidates. The second column is the share of the penalties landing on "
          f"scripts below {WEAK_CUT:.0f} out of 10; the flat row sits at "
          f"{flat['mass_below']:.0f} per cent because that is the share of scripts "
          "there. A deduction on a sub-task already worth less than 0.10 is partly "
          "absorbed by the zero floor, so the marks removed per deduction fall as that "
          f"share rises (correlation ${rho:.2f}$ across the seven rows). Every shape "
          "that sends more than the proportionate share to the weakest work — the "
          "reading on the table — costs less than flat. The two rows that cost more "
          "are the two that **spare** the weak, and neither is a reading anybody has "
          "offered. File: `data/analysis/penalty_shape.json`."]
    (TABLES / "penalty_shape.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = ["| Shape | Marks carried at twelve | Share of the $-1.48$ | "
         "Left over, against $-1.48$ | Share of the Física-specific $-1.10$ | "
         "Left over, against $-1.10$ | Deductions to carry the $-1.48$ alone |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for b in budget:
        nd = need[str(tuple(b["shape"]))]["deductions_for_whole_fall"]
        flag = "" if nd <= PR.SUBTASK.size else " ⚠"
        L.append(f"| {b['label']} | {b['carried']:.2f} | {b['share_of_fall']:.0f} % | "
                 f"{b['residual']:.2f} | "
                 f"{b['carried']/abs(FISICA_SPECIFIC)*100:.0f} % | "
                 f"{b['residual_vs_fisica']:.2f} | {nd:.0f}{flag} |")
    L += ["", "The same twelve deductions read as a budget, against two things. The "
          "observed year-on-year fall is $-1.48$, but the marking regime is a **Física** "
          "change — the deduction schedule is in the Física criteria and the decision "
          "to apply it was taken at the Física correctors' meeting — so what it can "
          "properly be asked to explain is the $-1.10$ the subject split assigns to "
          "Física specifically. The $-1.18$ that the same split assigns to every Basque "
          "subject at once cannot be the Física marking sheet, and the regime is not "
          "asked to carry it here. The flat row is the most the deduction "
          "channel can be worth at that count under any reading that does not spare "
          "the weakest scripts; every shape of the kind the coordination describes "
          "carries less and leaves more for the components the rest of the analysis "
          "has isolated — the part of the fall that is not Física's at all, the "
          "reading load, the optionality, the paper itself. The last column inverts "
          "the question: how many deductions each shape would need to carry the whole "
          "fall alone. A ⚠ marks a figure above the paper's twenty-eight marked "
          "sub-tasks, that is, a shape that cannot carry the fall by itself at any "
          "credible intensity."]
    (TABLES / "penalty_budget.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = ["| Shape | Deductions | Partial cascade % | Whole paper % | Mean | Pass % | "
         "At or below 2 % | Zero % | **At or above 9 %** | Loss |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for d in disc:
        L.append(f"| $p={d['shape'][0]:g},q={d['shape'][1]:g}$ | "
                 f"{d['deductions_per_script']:.0f} | {d['p_partial']*100:.0f} | "
                 f"{d['p_total']*100:.1f} | {d['mean']:.2f} | {d['pass_pct']:.1f} | "
                 f"{d['le2_pct']:.1f} | {d['zero_pct']:.1f} | **{d['top_pct']:.2f}** | "
                 f"{d['loss']:.1f} |")
    L.append(f"| *published 2026* | — | — | — | *{OBS_2026['mean']:.2f}* | "
             f"*{OBS_2026['pass_pct']:.1f}* | *{OBS_2026['le2_pct']:.1f}* | "
             f"*{OBS_2026['zero_pct']:.1f}* | *not published* | — |")
    nb = [d for d in disc if d["on_grid_boundary"] and d["sends_more_to_the_weak"]]
    L += ["", "Each shape refitted on its own three numbers — count, partial cascade, "
          "whole-paper cascade — against the four published figures, so the losses are "
          "comparable. They are not equal: the shapes tilted hardest to the weak "
          "overshoot the share at or below two, which is itself evidence about the "
          "shape. The column in bold was **not** fitted and is **not** published. "
          f"Across the readings on the table it runs from {top_range[0]:.2f} to "
          f"{top_range[1]:.2f} per cent — a factor of "
          f"{top_range[1]/max(top_range[0],1e-9):.0f} — which makes the 2026 band table "
          "the single measurement that would separate a flat regime from a distributed "
          f"one. (The two shapes that *spare* the weakest are shown for contrast and "
          f"are not readings anybody has offered; including them the range starts at "
          f"{top_range_all[0]:.2f}.) "
          + (f"Of the five readings on the table, {len(nb)} have their optimum on an "
             "edge of the search grid, and in every case it is the *lower* edge of the "
             "partial-cascade share: those shapes want no partial cascade at all, "
             "because deductions concentrated on weak work already carry the weakest "
             "scripts down without help. That is a corner of the model rather than a "
             "limit of the grid, and it is reported rather than hidden."
             if nb else "No reading on the table has its optimum on an edge of the "
                        "search grid.")]
    (TABLES / "penalty_topband.md").write_text("\n".join(L) + "\n", encoding="utf-8")



def draw(at12, budget, disc, flat, rho, tot_ref):
    """Figure 31. Split out so it can be redrawn from the JSON alone."""
    fig, axes = plt.subplots(2, 2, figsize=(13.2, 9.4))
    show = [(1.0, 1.0), (1.0, 3.0), (2.0, 2.0), (1.5, 3.0), (2.0, 3.0)]
    cols = [INK2, C["aqua"], C["green"], C["orange"], C["violet"]]

    ax = axes[0, 0]
    a = np.linspace(0.02, 0.98, 400)
    ta = np.clip(tot_ref / 10.0, 1e-3, 1 - 1e-3)
    for (pw, qw), col in zip(show, cols):
        m = (ta ** (pw - 1) * (1 - ta) ** (qw - 1)).mean()
        w = a ** (pw - 1) * (1 - a) ** (qw - 1) / m
        lab = "flat" if (pw, qw) == (1.0, 1.0) else f"$p={pw:g},\\ q={qw:g}$"
        ax.plot(a * 10, FIT["ded_rate"] * w, color=col, lw=2.0,
                ls="--" if (pw, qw) == (1.0, 1.0) else "-", label=lab)
    ax.set_xlim(0, 10); ax.set_ylim(0, 40)
    ax.set_xlabel("the script's 2025 mark")
    ax.set_ylabel("expected deductions on that script")
    ax.legend(fontsize=7.8, loc="upper right")
    ax.set_title("(a) Five ways to spread the same twelve\nthe average is twelve under "
                 "every curve", loc="left")

    ax = axes[0, 1]
    # offsets are set by hand: two of the shapes sit almost on top of each other
    OFF = {(1.0, 1.0): (9, -10), (1.0, 2.0): (-4, -15), (1.0, 3.0): (-46, -6),
           (2.0, 2.0): (-52, 2), (1.5, 3.0): (8, 3), (2.0, 3.0): (9, -2),
           (3.0, 1.0): (9, -3)}
    for r in at12:
        sh = tuple(r["shape"])
        col = C["violet"] if r["sends_more_to_the_weak"] else C["red"]
        if sh == (1.0, 1.0):
            col = INK2
        ax.scatter(r["mass_below"], r["marks_per_deduction"], s=62, color=col, zorder=3)
        ax.annotate(f"$p={r['shape'][0]:g},q={r['shape'][1]:g}$",
                    (r["mass_below"], r["marks_per_deduction"]),
                    textcoords="offset points", xytext=OFF[sh], fontsize=7.6, color=INK)
    ax.axvline(flat["mass_below"], color=MUTED, lw=1.0, ls=":")
    ax.axhline(flat["marks_per_deduction"], color=MUTED, lw=1.0, ls=":")
    ax.text(flat["mass_below"] + 1.0, 0.0405,
            "flat sends exactly the\nproportionate share here",
            fontsize=7.4, color=MUTED)
    ax.set_xlabel(f"per cent of the penalties landing below {WEAK_CUT:.0f}/10")
    ax.set_ylabel("marks removed per deduction")
    ax.set_xlim(0, 72); ax.set_ylim(0.038, 0.098)
    ax.set_title(f"(b) Why flat bounds the reading on the table\n"
                 f"cost falls as penalties move down (r $= {rho:.2f}$)", loc="left")

    ax = axes[1, 0]
    bshow = [b for b in budget if tuple(b["shape"]) in show]
    y = np.arange(len(bshow))[::-1]
    for yy, b in zip(y, bshow):
        ax.barh(yy, b["carried"], color=C["violet"], height=0.55)
        ax.barh(yy, b["residual"], left=b["carried"], color=C["yellow"], height=0.55)
        ax.text(b["carried"] / 2, yy, f"{b['carried']:.2f}", ha="center", va="center",
                fontsize=8.6, color="white")
        ax.text(b["carried"] + b["residual"] / 2, yy, f"{b['residual']:.2f}",
                ha="center", va="center", fontsize=8.6, color=INK)
    from matplotlib.patches import Patch
    ax.axvline(abs(FISICA_SPECIFIC), color=INK2, lw=1.3, ls="--", zorder=4)
    ax.text(abs(FISICA_SPECIFIC) - 0.022, (len(bshow) - 1) / 2.0,
            "the Física-specific $-1.10$", rotation=90, fontsize=7.6, color=INK2,
            ha="right", va="center")
    ax.set_yticks(y)
    ax.set_yticklabels([f"$p={b['shape'][0]:g},q={b['shape'][1]:g}$" for b in bshow],
                       fontsize=8.5)
    ax.set_xlim(0, abs(FALL) * 1.02)
    ax.set_ylim(-0.75, len(bshow) - 0.4)
    ax.set_xlabel("marks, out of the observed $-1.48$")
    ax.legend(handles=[Patch(color=C["violet"], label="carried by twelve deductions"),
                       Patch(color=C["yellow"], label="left for everything else")],
              fontsize=7.6, loc="lower center", ncol=2, frameon=True,
              bbox_to_anchor=(0.5, -0.02))
    ax.set_title("(c) The budget each reading leaves\nthe flatter the read, the less "
                 "there is left to explain", loc="left")
    ax.grid(axis="y", visible=False)

    ax = axes[1, 1]
    y = np.arange(len(disc))[::-1]
    vals = [d["top_pct"] for d in disc]
    cs = [(INK2 if tuple(d["shape"]) == (1.0, 1.0)
           else C["violet"] if d["sends_more_to_the_weak"] else C["red"]) for d in disc]
    ax.barh(y, vals, color=cs, height=0.58)
    for yy, v in zip(y, vals):
        ax.text(v + 0.12, yy, f"{v:.2f}", va="center", fontsize=8.2, color=INK)
    ax.axvline(BETA_TOP_2026 * 100, color=C["orange"], lw=1.4, ls="--")
    ax.text(BETA_TOP_2026 * 100 + 0.12, len(disc) - 0.7,
            "the smooth-curve\nextrapolation, 2.09\n(modelled, not published)",
            fontsize=7.4, color=C["orange"], va="top")
    ax.set_yticks(y)
    ax.set_yticklabels([f"$p={d['shape'][0]:g},q={d['shape'][1]:g}$" for d in disc],
                       fontsize=8.5)
    ax.set_xlim(0, max(max(vals), 2.09) * 1.45)
    ax.set_xlabel("per cent of scripts at or above 9, after refitting each shape")
    ax.set_title("(d) The one figure that separates them\nand the one Euskadi has not "
                 "published", loc="left")
    ax.grid(axis="y", visible=False)

    fig.suptitle("Figure 31 — The same penalties, spread differently: what the flat "
                 "model bounds, and what it leaves for the rest of the analysis",
                 x=0.005, ha="left", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    _save(fig, "fig31_penalty_shape", PLOTS)


def replot() -> None:
    """Redraw figure 31 from the saved results, without refitting anything.

    The fit takes minutes; the figure gets adjusted far more often than the numbers
    change, and redrawing from the JSON guarantees that the picture and the tables
    cannot disagree.
    """
    d = json.loads((A / "penalty_shape.json").read_text(encoding="utf-8"))
    at12 = d["at_fixed_count"]
    budget = d["budget_at_twelve"]
    disc = d["refit_per_shape"]
    flat = at12[0]
    rho = d["mechanism"]["correlation_cost_vs_weak_end_mass"]
    tot_ref = PR.baseline_scores(200_000)
    fam_d = [x for x in disc if x["sends_more_to_the_weak"]]
    top_range = (min(x["top_pct"] for x in fam_d), max(x["top_pct"] for x in fam_d))
    top_range_all = (min(x["top_pct"] for x in disc), max(x["top_pct"] for x in disc))
    d["top_band_spread"] = dict(
        min=top_range[0], max=top_range[1],
        ratio=float(top_range[1] / max(top_range[0], 1e-9)),
        scope="the readings on the table; the two shapes that spare the weak are apart",
        min_all=top_range_all[0], max_all=top_range_all[1],
        beta_extrapolation=BETA_TOP_2026 * 100,
        beta_over_flat=float(BETA_TOP_2026 * 100 / max(disc[0]["top_pct"], 1e-9)))
    (A / "penalty_shape.json").write_text(json.dumps(d, indent=2, ensure_ascii=False),
                                          encoding="utf-8")
    write_tables(at12, budget, disc, d["deductions_required"], flat, rho,
                 top_range, top_range_all)
    draw(at12, budget, disc, flat, rho, tot_ref)
    print("figure 31 and the three tables redrawn from data/analysis/penalty_shape.json")


def main() -> None:
    base = PR.simulate(n=N)
    print("baseline vs published 2025:",
          {k: round(base[k], 2) for k in ("mean", "pass_pct", "le2_pct", "zero_pct")})
    tot_ref = PR.baseline_scores(200_000)

    # ---- A.  the same twelve deductions, spread seven ways ---------------------
    at12 = []
    for shape, label in SHAPES:
        r = run(shape, FIT["ded_rate"], voiding=False)
        r["label"] = label
        r["marks_per_deduction"] = abs(r["shift"]) / max(r["deductions_per_script"], 1e-9)
        r.update(profile(shape, tot_ref))
        at12.append(r)
    flat = at12[0]
    for r in at12:
        r["relative_to_flat"] = r["marks_per_deduction"] / flat["marks_per_deduction"]
        r["sends_more_to_the_weak"] = bool(r["mass_below"] >= flat["mass_below"] - 1e-9)

    # Is flat the ceiling over the family on the table?  Tested, not assumed.
    fam = [r for r in at12 if r["sends_more_to_the_weak"]]
    spare = [r for r in at12 if not r["sends_more_to_the_weak"]]
    ceiling_holds = bool(all(r["marks_per_deduction"] <= flat["marks_per_deduction"] + 1e-4
                             for r in fam))
    # ... and the mechanism: does cost per deduction fall in the weak-end mass?
    xs = np.array([r["mass_below"] for r in at12])
    ys = np.array([r["marks_per_deduction"] for r in at12])
    rho = float(np.corrcoef(xs, ys)[0, 1])

    # ---- B.  over-dispersion: the same shape, more unequal ---------------------
    over = []
    for shape in [(1.0, 1.0), (2.0, 3.0)]:
        for k in [None, 2.0, 0.5]:
            r = run(shape, FIT["ded_rate"], voiding=False, overdispersion=k)
            r["marks_per_deduction"] = abs(r["shift"]) / max(r["deductions_per_script"], 1e-9)
            r["relative_to_equal"] = None
            over.append(r)
    for r in over:
        ref = [o for o in over if o["shape"] == r["shape"] and o["overdispersion"] is None][0]
        r["relative_to_equal"] = float(r["marks_per_deduction"] / ref["marks_per_deduction"])

    # ---- C.  what each shape would need to carry things on its own -------------
    need = {}
    for shape, label in SHAPES:
        c_fall = invert_shift(shape, FALL)
        c_fis = invert_shift(shape, FISICA_SPECIFIC)
        need[str(shape)] = dict(
            shape=list(shape), label=label,
            deductions_for_whole_fall=float(c_fall),
            deductions_for_fisica_specific=float(c_fis),
            exceeds_subtasks=bool(c_fall > PR.SUBTASK.size),
        )

    # ---- D.  the budget at a common, defensible count --------------------------
    budget = []
    for r in at12:
        carried = abs(r["shift"])
        budget.append(dict(
            shape=r["shape"], label=r["label"], mass_below=r["mass_below"],
            carried=float(carried),
            share_of_fall=float(carried / abs(FALL) * 100),
            residual=float(abs(FALL) - carried),
            residual_vs_fisica=float(max(abs(FISICA_SPECIFIC) - carried, 0.0)),
        ))

    # ---- E.  refit each shape, then read the unfitted top band -----------------
    disc = []
    for shape, label in SHAPES:
        r = refit(shape)
        r["label"] = label
        r.update(profile(shape, tot_ref))
        r["sends_more_to_the_weak"] = bool(
            r["mass_below"] >= flat["mass_below"] - 1e-9)
        disc.append(r)
    fam_d = [d for d in disc if d["sends_more_to_the_weak"]]
    top_range = (min(d["top_pct"] for d in fam_d), max(d["top_pct"] for d in fam_d))
    top_range_all = (min(d["top_pct"] for d in disc), max(d["top_pct"] for d in disc))

    out = dict(
        note=("The shape of the penalty distribution, not its size. `ded_rate` is the "
              "MEAN number of deductions per script in every row, so rows differ only "
              "in how those deductions are spread across candidates."),
        modelled_not_published=dict(
            top_band_2026=BETA_TOP_2026,
            explanation=("The 2.09 per cent at or above nine in 2026 is an OUTPUT of "
                         "the Beta-mixture fitted to the same four published figures, "
                         "not an observation. Euskadi has not published a 2026 band "
                         "table. Any comparison against it is model against model, "
                         "and the dossier states it as such."),
        ),
        baseline=dict(achieved={k: base[k] for k in
                                ("mean", "pass_pct", "le2_pct", "zero_pct", "top_pct")},
                      target_2025=OBS_2025),
        fitted_regime=FIT,
        weak_cut=WEAK_CUT,
        at_fixed_count=at12,
        mechanism=dict(
            correlation_cost_vs_weak_end_mass=rho,
            statement=("What a deduction is worth depends on whether there is 0.10 "
                       "left on the sub-task it lands on. The marks removed per "
                       "deduction fall monotonically in the share of penalties landing "
                       "on scripts below four out of ten."),
        ),
        ceiling=dict(
            family_on_the_table=[r["shape"] for r in fam],
            shapes_that_spare_the_weak=[r["shape"] for r in spare],
            holds_over_family_on_the_table=ceiling_holds,
            flat_marks_per_deduction=float(flat["marks_per_deduction"]),
            statement=("Flat sends exactly the proportionate share of penalties to the "
                       "weakest scripts. Every shape that sends MORE — the reading the "
                       "coordination proposed — removes fewer marks per deduction, so "
                       "at a fixed count flat is a ceiling over that family. It is NOT "
                       "a ceiling over shapes that SPARE the weak: a symmetric hump or "
                       "a tilt towards the best scripts removes more per deduction, "
                       "because none of its penalties is wasted on work with nothing "
                       "left to take. Nobody has proposed either."),
        ),
        overdispersion=over,
        deductions_required=need,
        budget_at_twelve=budget,
        refit_per_shape=disc,
        top_band_spread=dict(
            min=top_range[0], max=top_range[1],
            ratio=float(top_range[1] / max(top_range[0], 1e-9)),
            scope="the readings on the table; the two shapes that spare the weak are apart",
            min_all=top_range_all[0], max_all=top_range_all[1],
            beta_extrapolation=BETA_TOP_2026 * 100,
            beta_over_flat=float(BETA_TOP_2026 * 100 / max(disc[0]["top_pct"], 1e-9))),
        what_to_measure=[
            "the 2026 band table, and above all the share at or above nine",
            "deductions of 0.10 per script plotted against the script's final mark",
            "the same plot for 2025, where the rules existed but were not applied",
        ],
    )
    (A / "penalty_shape.json").write_text(json.dumps(out, indent=2, ensure_ascii=False),
                                          encoding="utf-8")

    write_tables(at12, budget, disc, need, flat, rho, top_range, top_range_all)
    draw(at12, budget, disc, flat, rho, tot_ref)

    # ---- console ---------------------------------------------------------------
    print(f"\nAt {FIT['ded_rate']} deductions per script, voiding off:")
    for r in at12:
        print(f"  p={r['shape'][0]:>3g} q={r['shape'][1]:>3g}  "
              f"below4 {r['mass_below']:5.1f}%  shift {r['shift']:+.3f}  "
              f"per ded {r['marks_per_deduction']:.4f} "
              f"({r['relative_to_flat']*100:5.1f}% of flat)  "
              f"weak-loaded {str(r['sends_more_to_the_weak']):>5}")
    print(f"\ncost vs weak-end mass, correlation: {rho:.3f}")
    print(f"ceiling holds over the family on the table: {ceiling_holds}")
    print(f"  family   : {[r['shape'] for r in fam]}")
    print(f"  spare the weak (flat is NOT a bound for these): "
          f"{[r['shape'] for r in spare]}")
    print("\nOver-dispersion (Gamma(k,1/k) on each script's rate):")
    for r in over:
        print(f"  p={r['shape'][0]:g} q={r['shape'][1]:g}  k={str(r['overdispersion']):>4}  "
              f"per ded {r['marks_per_deduction']:.4f}  "
              f"({r['relative_to_equal']*100:5.1f}% of the equal-rate case)")
    print("\nDeductions needed to carry, on its own:")
    for k, v in need.items():
        print(f"  {k:<12} whole fall {v['deductions_for_whole_fall']:5.1f}   "
              f"Física-specific {v['deductions_for_fisica_specific']:5.1f}"
              f"{'   [> 28 sub-tasks]' if v['exceeds_subtasks'] else ''}")
    print("\nRefitted per shape (three numbers each) — the top band is not fitted:")
    for d in disc:
        print(f"  p={d['shape'][0]:>3g} q={d['shape'][1]:>3g}  "
              f"ded {d['deductions_per_script']:5.1f}  pp {d['p_partial']*100:4.0f}  "
              f"pt {d['p_total']*100:4.1f}  mean {d['mean']:.2f}  "
              f"pass {d['pass_pct']:5.1f}  <=2 {d['le2_pct']:5.1f}  "
              f"zero {d['zero_pct']:4.2f}  >=9 {d['top_pct']:5.2f}  "
              f"loss {d['loss']:5.1f}{'  [boundary]' if d['on_grid_boundary'] else ''}")
    print(f"  published 2026        mean {OBS_2026['mean']:.2f}  "
          f"pass {OBS_2026['pass_pct']:5.1f}  <=2 {OBS_2026['le2_pct']:5.1f}  "
          f"zero {OBS_2026['zero_pct']:4.2f}  >=9  (not published)")
    print(f"  Beta extrapolation (MODELLED) >=9 = {BETA_TOP_2026*100:.2f}")


if __name__ == "__main__":
    import sys
    replot() if "--replot" in sys.argv else main()
