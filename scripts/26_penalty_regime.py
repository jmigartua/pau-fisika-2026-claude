#!/usr/bin/env python3
"""From non-award to deduction: what the change of marking regime is worth, in marks.

The severity section of Chapter 6 treats "the tribunals marked more severely" as one
hypothesis among several and bounds it from the subject table.  The coordination's
account of what changed is more specific, and it is not severity in the ordinary sense
of markers becoming harsher on the same scale.  It is a change of REGIME, in two parts.

  1. Until 2025 a missing unit, a vector arrow on a scalar, an intermediate rounding
     cost the candidate whatever part of the sub-task depended on it: the marker did
     not award that part.  From 2026 the same omission costs that part AND a deduction
     of 0.10, and the Basque 2026 criteria state no cap on those deductions.
  2. A grave error — a wrong equation, a conceptual scalar/vector confusion — voids the
     whole apartado.  In a physics problem a wrong starting relation propagates, so
     voiding does not fall independently: one conceptual error can carry most of a
     paper with it.

A third part of the regime, the linguistic component and the clarity/terminology/
coherence rules, is NOT modelled here: it applies to text production rather than to
sub-tasks and the dossier has no basis for a rate.  What follows therefore models two
of the three channels the coordination describes, and understates the regime by
whatever the third is worth.

WHAT THIS SCRIPT DOES.  It asks whether that regime is CAPABLE of producing the four
published 2026 figures, and what it would have to look like if it did.  It is a
sufficiency test and an inversion, not an estimate.

THE BASELINE.  An earlier version of this script took the Beta component of the 2025
mixture fit as if it were the whole 2025 distribution, and then rescaled it to a mean
of 5.47.  That was wrong twice over — the fit is a 1.2 % point mass at zero PLUS that
Beta, and deleting the mass should raise the remainder's mean, not lower it — and the
resulting baseline reproduced only one of the four 2025 figures it should have matched:
it gave a pass rate of 58.7 against 62.3, a low-mark mass of 6.7 against 10.0, and
1.9 % in the top band against a published 6.7 %.  The baseline is now built
non-parametrically from the PUBLISHED 2025 band shares, so it reproduces the 2025
distribution by construction and the 2026 figures are the only thing being fitted.

Reads : data/analysis/euskadi_grade_bands_2015_2025.csv, data/analysis/results.json
Writes: data/analysis/penalty_regime.json, data/tables/penalty_regime.md,
        data/tables/penalty_inversion.md, plots/fig30_penalty_regime.(png|svg)
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
A = ROOT / "data" / "analysis"
TABLES = ROOT / "data" / "tables"
PLOTS = ROOT / "plots"

RNG = np.random.default_rng(20260920)
N = 200_000
DEDUCTION = 0.10

# The 2026 Basque paper's marking granularity, read off problem B1: a) 0.25 + 0.25,
# b) 0.25 + 0.25 + 0.50, c) 0.50 + 0.50.  Assuming the same shape for the other three
# problems gives twenty-eight marked units in twelve apartados.  That IS an
# extrapolation from one of the four problems — the option items are shorter and may
# be marked more coarsely — so the sensitivity to a twelve-unit structure is reported.
SUBTASK = np.array([0.25, 0.25, 0.25, 0.25, 0.50, 0.50, 0.50] * 4)
APARTADO_OF = np.array([0, 0, 1, 1, 1, 2, 2] * 4) + np.repeat(np.arange(4), 7) * 3
N_APARTADOS = 12
SIGMA_ITEM = 0.20      # within-script dispersion; from 08_ehu_history.py

# The four published 2026 figures, and the 2025 ones the baseline must reproduce.
OBS_2026 = dict(mean=3.99, pass_pct=39.8, le2_pct=24.5, zero_pct=3.2)
OBS_2025 = dict(mean=5.47, pass_pct=62.3, le2_pct=10.0, zero_pct=1.2)

TARGETS = {
    "quantitative minus verbal": -0.84,
    "Física-specific (subject split)": -1.10,
    "Euskadi-common (subject split)": -1.18,
    "observed year-on-year": -1.48,
    "Basque-specific (mark budget)": -1.65,
}


def baseline_scores(n):
    """Draw 2025 total scores from the PUBLISHED band shares.

    The bands are [0,5) [5,6) [6,7) [7,8) [8,9) [9,10].  The first is split further
    using the two figures the dossier has for it: 1.2 % at exactly zero (assumed, and
    the same assumption the 2025 mixture fit makes) and 10 % at or below 2.  Within a
    band the draw is uniform, which is the least committed choice available.
    """
    b = pd.read_csv(A / "euskadi_grade_bands_2015_2025.csv")
    r = b[b.year == 2025].iloc[0]
    zero, le2 = OBS_2025["zero_pct"], OBS_2025["le2_pct"]
    edges = [(0.0, 0.0, zero), (0.0, 2.0, le2 - zero), (2.0, 5.0, r["[0-5)"] - le2),
             (5.0, 6.0, r["[5-6)"]), (6.0, 7.0, r["[6-7)"]), (7.0, 8.0, r["[7-8)"]),
             (8.0, 9.0, r["[8-9)"]), (9.0, 10.0, r["[9-10]"])]
    w = np.array([e[2] for e in edges], dtype=float)
    w /= w.sum()
    which = RNG.choice(len(edges), size=n, p=w)
    lo = np.array([e[0] for e in edges])[which]
    hi = np.array([e[1] for e in edges])[which]
    return lo + RNG.random(n) * (hi - lo)


def _allocate(total, sigma=SIGMA_ITEM):
    """Spread each candidate's total over the sub-tasks, preserving the total exactly."""
    n = total.size
    share = np.clip(total[:, None] / 10.0
                    + RNG.normal(0, sigma, size=(n, SUBTASK.size)), 0.0, 1.0)
    got = share * SUBTASK
    s = got.sum(axis=1, keepdims=True)
    s[s == 0] = 1.0
    return got * (total[:, None] / s)      # exact, so the baseline is reproduced


def simulate(ded_rate=0.0, p_partial=0.0, p_total=0.0, partial_frac=(0.34, 0.67),
             ded_mode="flat", void_mode="cascade", sigma=SIGMA_ITEM, n=N,
             subtask=None, apartado_of=None, shape=(1.0, 1.0),
             overdispersion=None, exposed=None, lang=None,
             lang_shape=(2.0, 2.0)) -> dict:
    """The 2025 distribution put through the 2026 regime.

    ded_rate      expected 0.10 deductions per script, applied in 2026 and not in 2025.
    ded_mode      "flat": slips fall independently of how well the physics is done —
                  forgetting a unit is a habit, not an ability.  "weak": they
                  concentrate where the work is weak.
    p_partial     share of scripts with a grave error that carries part of the paper.
    p_total       share of scripts with a grave error that carries essentially all of
                  it (eleven or twelve apartados).  This is the channel that makes
                  zeros, and it is read off the observed zero rate rather than fitted
                  through a twelfth power, which is what an earlier version did.
    void_mode     "cascade" as above; "independent" voids apartados independently at
                  the rate that gives the same expected number.
    exposed       boolean mask over the sub-tasks: which of them a unit, prefix or
                  rounding error can actually be made on. Default None means all of
                  them, which is what this script assumed before the sub-task coding
                  of 20 September showed that only about half of the paper produces a
                  numerical result at all. Deductions are spread over the exposed
                  sub-tasks only; `ded_rate` is still the mean count per script.
    lang          the third channel, the linguistic one, which the Basque criteria
                  cap: (mean spelling errors per script, share of scripts with a
                  syntax/coherence penalty). The rule is -0.10 from the THIRD error,
                  spelling capped at 1.00, syntax/coherence up to 0.50, and the two
                  together capped at 1.00 -- ten per cent of the paper. Default None
                  leaves the channel out, which is what the published version did.
    lang_shape    who makes spelling and syntax errors, as a Beta kernel in the
                  candidate's own level.  The first version of this channel simply
                  scaled the error rate up as the mark fell, and it produced 8 per cent
                  of scripts at exactly zero against a published 3.2 -- because a
                  candidate who writes almost nothing cannot misspell it.  Errors
                  require text, and text requires an attempt, so the rate has to
                  vanish at both ends: (2,2) is a hump in the middle, which is the
                  default.  The observed zero rate is what bounds this, and it bounds
                  it tightly.
    """
    st = SUBTASK if subtask is None else subtask
    ao = APARTADO_OF if apartado_of is None else apartado_of
    n_ap = int(ao.max()) + 1

    total = baseline_scores(n)
    global SUBTASK_ACTIVE
    share = np.clip(total[:, None] / 10.0 + RNG.normal(0, sigma, size=(n, st.size)), 0, 1)
    got = share * st
    s = got.sum(axis=1, keepdims=True); s[s == 0] = 1.0
    base = got * (total[:, None] / s)

    # How the deductions are spread across candidates.  `ded_rate` is always the MEAN
    # number per script; the shape only redistributes them, so the three modes are
    # directly comparable at the same rate.
    #   "flat"  every candidate has the same expected count, Poisson-scattered.
    #   "weak"  the count is proportional to how weak the work on each sub-task is.
    #   "shape" a Beta kernel in the candidate's own level a: w(a) = a^(p-1)(1-a)^(q-1),
    #           normalised to mean one, so (1,1) is flat, (1,2) tilts toward the weak,
    #           (2,2) is a hump in the middle and (2,3) a hump below the middle.
    # `overdispersion` multiplies each script's rate by a Gamma(k,1/k) draw (mean one),
    # which turns the Poisson counts into negative-binomial ones: some scripts collect
    # many penalties and some almost none, at the same average.
    if ded_mode == "shape":
        a = np.clip(total / 10.0, 1e-3, 1 - 1e-3)
        pw, qw = shape
        w_i = a ** (pw - 1.0) * (1.0 - a) ** (qw - 1.0)
        w_i = w_i / w_i.mean()
        per = ded_rate * w_i
    elif ded_mode == "flat":
        per = np.full(n, float(ded_rate))
    else:
        per = None
    ex = (np.ones(st.size, dtype=bool) if exposed is None
          else np.asarray(exposed, dtype=bool))
    n_ex = max(int(ex.sum()), 1)
    if per is not None:
        if overdispersion is not None and np.isfinite(overdispersion):
            per = per * RNG.gamma(overdispersion, 1.0 / overdispersion, size=n)
        lam = np.repeat(per[:, None] / n_ex, st.size, axis=1) * ex[None, :]
    else:
        w = (1.0 - share) * ex[None, :]
        lam = ded_rate * w / np.maximum(w.sum(axis=1, keepdims=True), 1e-9)
    k = RNG.poisson(lam)
    x = np.maximum(base - DEDUCTION * k, 0.0)

    n_voided = 0.0
    if p_partial > 0 or p_total > 0:
        u = RNG.random(n)
        # weaker scripts are likelier to carry a grave error
        rel = np.clip((1.0 - total / 10.0) / (1.0 - total.mean() / 10.0), 0, 3)
        hit_total = u < np.clip(p_total * rel, 0, 1)
        hit_part = (~hit_total) & (RNG.random(n) < np.clip(p_partial * rel, 0, 1))
        nv = np.zeros(n, dtype=int)
        nv[hit_total] = RNG.integers(n_ap - 1, n_ap + 1, size=hit_total.sum())
        frac = RNG.uniform(*partial_frac, size=hit_part.sum())
        nv[hit_part] = np.round(frac * n_ap).astype(int)
        if void_mode == "independent":
            per = nv.sum() / (n * n_ap)
            vd = RNG.random((n, n_ap)) < per
        else:
            order = RNG.random((n, n_ap)).argsort(axis=1)
            vd = order < nv[:, None]
        n_voided = float(vd.sum(axis=1).mean())
        x = x * (~vd[:, ao])

    sc = x.sum(axis=1)

    lang_mean = 0.0
    if lang is not None:
        e_mean, p_syntax = lang
        # Errors need text, and text needs an attempt. The rate therefore has to fall
        # to nothing at both ends -- a blank script has no spelling -- so it is a Beta
        # kernel in the candidate's own level, normalised to mean one so that `e_mean`
        # is the mean number of errors per script whatever the shape.
        al = np.clip(total / 10.0, 1e-3, 1 - 1e-3)
        pl, ql = lang_shape
        rel_l = al ** (pl - 1.0) * (1.0 - al) ** (ql - 1.0)
        rel_l = rel_l / rel_l.mean()
        e = RNG.poisson(np.clip(e_mean * rel_l, 0.0, None))
        spell = np.minimum(np.maximum(e - 2, 0) * DEDUCTION, 1.0)
        syn = np.where(RNG.random(n) < np.clip(p_syntax * rel_l, 0, 1),
                       RNG.choice([0.2, 0.3, 0.5], size=n), 0.0)
        pen = np.minimum(spell + syn, 1.0)     # the cap is on the two together
        before = sc.mean()
        sc = np.maximum(sc - pen, 0.0)
        lang_mean = float(before - sc.mean())

    return dict(
        ded_rate=ded_rate, p_partial=p_partial, p_total=p_total,
        ded_mode=ded_mode, void_mode=void_mode, sigma=sigma,
        shape=list(shape), overdispersion=overdispersion,
        n_exposed=int(n_ex), lang=list(lang) if lang else None,
        lang_shape=list(lang_shape), lang_shift=lang_mean,
        deductions_per_script=float(k.sum(axis=1).mean()),
        apartados_voided_per_script=n_voided,
        scripts_with_any_void=float((nv > 0).mean() * 100) if (p_partial or p_total) else 0.0,
        mean=float(sc.mean()), shift=float(sc.mean() - total.mean()),
        pass_pct=float((sc >= 5).mean() * 100),
        le2_pct=float((sc <= 2).mean() * 100),
        zero_pct=float((sc <= 1e-9).mean() * 100),
        top_pct=float((sc >= 9).mean() * 100),
        sd=float(sc.std(ddof=1)),
    )


def loss(r, obs=OBS_2026):
    return (((r["mean"] - obs["mean"]) / 0.15) ** 2
            + ((r["pass_pct"] - obs["pass_pct"]) / 2.0) ** 2
            + ((r["le2_pct"] - obs["le2_pct"]) / 2.0) ** 2
            + ((r["zero_pct"] - obs["zero_pct"]) / 1.0) ** 2)


def invert(target, channel="deduction", n=60_000) -> float:
    lo, hi = (0.0, 80.0) if channel == "deduction" else (0.0, 0.9)
    for _ in range(35):
        mid = (lo + hi) / 2
        s = (simulate(ded_rate=mid, n=n) if channel == "deduction"
             else simulate(p_partial=mid, n=n))["shift"]
        lo, hi = (mid, hi) if s > target else (lo, mid)
    return (lo + hi) / 2


def search(void_mode="cascade", sigma=SIGMA_ITEM, subtask=None, apartado_of=None,
           ded_modes=("flat", "weak"), n=40_000):
    """Grid search over both channels and both deduction modes.

    The grid is deliberately wider than the fitted values, so that an optimum sitting
    on a boundary is visible as such; an earlier version's grid was too narrow and its
    optimum sat in its top corner.
    """
    best = None
    for mode in ded_modes:
        for ded in (8, 12, 16, 20, 24, 30):
            for pp in (0.04, 0.10, 0.16, 0.22, 0.30):
                for pt in (0.005, 0.015, 0.030, 0.045):
                    r = simulate(ded, pp, pt, ded_mode=mode, void_mode=void_mode,
                                 sigma=sigma, subtask=subtask, apartado_of=apartado_of,
                                 n=n)
                    L = loss(r)
                    if best is None or L < best[0]:
                        best = (L, r)
    out = dict(best[1]); out["loss"] = float(best[0])
    out["on_grid_boundary"] = bool(
        out["ded_rate"] in (8, 30) or out["p_partial"] in (0.04, 0.30)
        or out["p_total"] in (0.005, 0.045))
    return out


def draw(grid, inverted_ded, best_full, best_indep, harder_add):
    """Figure 30. Split out so it can be redrawn from the JSON alone."""
    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.7))

    ax = axes[0]
    xs = np.array([g["deductions_per_script"] for g in grid])
    ys = np.array([g["shift"] for g in grid])
    ax.plot(xs, ys, color=C["violet"], lw=2.0, marker="o", ms=4, label="with the zero floor")
    ax.plot(xs, -DEDUCTION * xs, color=MUTED, lw=1.2, ls=":", label="0.10 each, no floor")
    for lab, v in [("Física-specific $-1.10$", -1.10), ("observed $-1.48$", -1.48)]:
        ax.axhline(v, color=C["orange"], lw=0.9, ls="--")
        ax.text(0.5, v + 0.07, lab, fontsize=7.8, color=C["orange"])
    ax.set_xlim(0, 31); ax.set_ylim(-3.2, 0.15)
    ax.set_xlabel("deductions of $0.10$ per script")
    ax.set_ylabel("shift in the mean (marks)")
    ax.legend(loc="lower left", fontsize=8)
    ax.set_title(f"(a) The deduction channel\n"
                 f"{inverted_ded['Física-specific (subject split)']:.0f} per script "
                 f"would carry the $-1.10$", loc="left")

    ax = axes[1]
    labels = ["mean", "pass rate", "at or below 2", "zero",
              "at or above 9\n(not published)"]
    # The top band is NOT published for 2026. An earlier version drew 2.1 here as an
    # "observed" value; it is this study's own Beta extrapolation from the same four
    # published figures, and drawing it as data was the dossier's worst error to date.
    series = [("published 2026", [OBS_2026["mean"], OBS_2026["pass_pct"],
                                  OBS_2026["le2_pct"], OBS_2026["zero_pct"],
                                  float("nan")], INK2),
              ("the regime, fitted", [best_full["mean"], best_full["pass_pct"],
                                      best_full["le2_pct"], best_full["zero_pct"],
                                      best_full["top_pct"]], C["violet"]),
              ("same, voiding independent", [best_indep["mean"], best_indep["pass_pct"],
                                             best_indep["le2_pct"],
                                             best_indep["zero_pct"],
                                             best_indep["top_pct"]], C["yellow"]),
              ("a harder paper, additive", [harder_add["mean"], harder_add["pass_pct"],
                                            harder_add["le2_pct"],
                                            harder_add["zero_pct"],
                                            harder_add["top_pct"]], C["aqua"])]
    x = np.arange(5)
    w = 0.2
    for i, (lab, vals, col) in enumerate(series):
        ax.bar(x + (i - 1.5) * w, vals, width=w, color=col, label=lab)
        for xx, v in zip(x + (i - 1.5) * w, vals):
            if np.isfinite(v):
                ax.text(xx, v + 0.7, f"{v:.1f}", ha="center", fontsize=6.4, color=INK)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, 52)
    ax.axvspan(3.55, 4.45, color=MUTED, alpha=0.10, zorder=0)
    ax.text(4.0, 12.0, "no 2026 band table:\nnothing to compare\nagainst. The readings\n"
            "differ here by a\nfactor of twenty-three —\nsee figure 31",
            fontsize=6.8, color=MUTED, ha="center", va="bottom")
    ax.legend(loc="upper right", fontsize=7.0)
    ax.set_title("(b) Four figures fitted, one not published\nthe top band is where the "
                 "readings separate", loc="left")
    ax.grid(axis="x", visible=False)

    ax = axes[2]
    items = [("deductions of 0.10\nper script", best_full["deductions_per_script"]),
             ("scripts with a partial\ncascade (per cent)", best_full["p_partial"] * 100),
             ("scripts with the whole\npaper voided (per cent)",
              best_full["p_total"] * 100)]
    y = np.arange(len(items))[::-1]
    ax.barh(y, [v for _, v in items], color=C["blue"], height=0.55)
    for yy, (_, v) in zip(y, items):
        ax.text(v + 0.35, yy, f"{v:.0f}" if v >= 3 else f"{v:.1f}", va="center",
                fontsize=10, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([k for k, _ in items], fontsize=8.5)
    ax.set_xlim(0, 20)
    ax.set_xlabel("value required to reproduce the 2026 figures")
    ax.set_title("(c) Three numbers, all of them\non the marking sheets", loc="left")
    ax.grid(axis="y", visible=False)

    fig.suptitle("Figure 30 — From non-award to deduction: can the regime change "
                 "produce 2026 on its own?", x=0.005, ha="left", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _save(fig, "fig30_penalty_regime", PLOTS)


def replot() -> None:
    """Redraw figure 30 from data/analysis/penalty_regime.json, without refitting."""
    d = json.loads((A / "penalty_regime.json").read_text(encoding="utf-8"))
    draw(d["dose_response"], d["inversion_deductions_only"], d["best_fit"],
         d["best_fit_independent_voiding"], d["harder_paper_additive"])
    print("figure 30 redrawn from data/analysis/penalty_regime.json")


def main() -> None:
    base = simulate(n=N)
    print("baseline vs published 2025:",
          {k: round(base[k], 2) for k in ("mean", "pass_pct", "le2_pct", "zero_pct")},
          "against", OBS_2025)

    rates = [0, 2, 4, 6, 8, 10, 12, 14, 16, 20, 25, 30]
    grid = [simulate(ded_rate=r) for r in rates]
    inverted_ded = {k: invert(v) for k, v in TARGETS.items()}

    best = search()
    best_full = simulate(best["ded_rate"], best["p_partial"], best["p_total"],
                         ded_mode=best["ded_mode"])
    best_full["loss"] = loss(best_full)

    # The same fit under independent voiding, searched rather than asserted.
    best_indep = search(void_mode="independent", n=25_000)

    # Sensitivity of the fitted values, on a coarser grid for cost.
    sens = {}
    for s_ in (0.10, 0.30):
        r = search(sigma=s_, ded_modes=(best["ded_mode"],), n=25_000)
        sens[f"sigma = {s_}"] = {k: r[k] for k in
                                 ("ded_rate", "p_partial", "p_total", "loss")}
    st12, ao12 = np.full(12, 10.0 / 12), np.arange(12)
    r = search(subtask=st12, apartado_of=ao12, ded_modes=(best["ded_mode"],), n=25_000)
    sens["12 equal sub-tasks"] = {k: r[k] for k in
                                  ("ded_rate", "p_partial", "p_total", "loss")}
    other = "weak" if best["ded_mode"] == "flat" else "flat"
    r = simulate(best["ded_rate"], best["p_partial"], best["p_total"],
                 ded_mode=other, n=60_000)
    sens[f"same values, deductions {other}"] = dict(
        ded_rate=best["ded_rate"], p_partial=best["p_partial"],
        p_total=best["p_total"], loss=float(loss(r)))

    # Comparators, on the same baseline.
    tot = baseline_scores(N)
    def moments(s):
        return dict(mean=float(s.mean()), pass_pct=float((s >= 5).mean() * 100),
                    le2_pct=float((s <= 2).mean() * 100),
                    zero_pct=float((s <= 1e-9).mean() * 100),
                    top_pct=float((s >= 9).mean() * 100))
    harder_add = moments(np.clip(tot - 1.48, 0, 10))
    harder_mul = moments(np.clip(tot * (OBS_2026["mean"] / OBS_2025["mean"]), 0, 10))
    harder_add["loss"] = loss(harder_add); harder_mul["loss"] = loss(harder_mul)

    out = dict(
        note=("A sufficiency test and an inversion, not an estimate. Two of the three "
              "channels the coordination describes are modelled; the linguistic one is "
              "not."),
        baseline=dict(source="published 2025 band shares, uniform within band",
                      achieved={k: base[k] for k in
                                ("mean", "pass_pct", "le2_pct", "zero_pct", "top_pct")},
                      target_2025=OBS_2025),
        model=dict(deduction=DEDUCTION, n_subtasks=int(SUBTASK.size),
                   n_apartados=N_APARTADOS, sigma_item=SIGMA_ITEM,
                   subtask_structure_note=("extrapolated from problem B1 to all four "
                                           "problems; the option items may be marked "
                                           "more coarsely — see sensitivity"),
                   channels_modelled=["0.10 deductions, uncapped",
                                      "grave-error voiding of apartados"],
                   top_band_note=("Euskadi has not published a 2026 band table. "
                                  "Any share at or above nine quoted for 2026 in "
                                  "this repository is MODELLED — see "
                                  "27_penalty_shape.py, which shows the readings "
                                  "differ there by a factor of twenty-three."),
                   channels_not_modelled=["the 0.2 linguistic component and the "
                                          "clarity/terminology/coherence rules"]),
        observed_2026=OBS_2026,
        dose_response=grid,
        inversion_deductions_only=inverted_ded,
        best_fit=best_full,
        best_fit_independent_voiding=best_indep,
        sensitivity=sens,
        harder_paper_additive=harder_add,
        harder_paper_proportional=harder_mul,
        what_to_measure=[
            "deductions of 0.10 applied per script, 2025 and 2026, by type",
            "share of scripts with at least one voided apartado, 2025 and 2026",
            "share of scripts with essentially the whole paper voided",
        ],
    )
    (A / "penalty_regime.json").write_text(json.dumps(out, indent=2, ensure_ascii=False),
                                           encoding="utf-8")

    # ---- tables ----------------------------------------------------------------
    L = ["| Deductions per script | Mean | Shift | Pass % | % at or below 2 | % zero |",
         "|---:|---:|---:|---:|---:|---:|"]
    for g in grid:
        L.append(f"| {g['deductions_per_script']:.0f} | {g['mean']:.2f} | "
                 f"{g['shift']:+.2f} | {g['pass_pct']:.1f} | {g['le2_pct']:.1f} | "
                 f"{g['zero_pct']:.1f} |")
    L += ["", "The published 2025 distribution under the deduction channel alone. Each "
          "deduction is 0.10 and the Basque 2026 criteria state no cap; a sub-task "
          "cannot fall below zero, which is why the mean moves by less than 0.10 per "
          "deduction. Row one is the 2025 paper unchanged. The last column barely "
          "moves: deductions spread over twenty-eight sub-tasks almost never reach a "
          "script's last mark, so this channel cannot make the 2026 zeros — it is the "
          "voiding channel that does. File: `data/analysis/penalty_regime.json`."]
    (TABLES / "penalty_regime.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = ["| To account for, on its own | Marks | Deductions per script |",
         "|---|---:|---:|"]
    for k, v in TARGETS.items():
        L.append(f"| {k} | {v:+.2f} | {inverted_ded[k]:.0f} |")
    L += ["", "The deduction channel carrying each quantity by itself, voiding switched "
          "off. The paper is taken to have twenty-eight marked sub-tasks, so a figure "
          "above about fourteen means a deduction on more than half the sub-tasks of "
          "every script."]
    (TABLES / "penalty_inversion.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    draw(grid, inverted_ded, best_full, best_indep, harder_add)

    print("inversion, deductions:", {k: round(v) for k, v in inverted_ded.items()})
    print(f"\nbest fit: {best_full['deductions_per_script']:.0f} deductions, "
          f"partial cascade {best_full['p_partial']*100:.0f} %, "
          f"total cascade {best_full['p_total']*100:.1f} %, loss {best_full['loss']:.2f}")
    for lab, d in [("  fitted regime   ", best_full),
                   ("  indep. voiding  ", best_indep),
                   ("  harder, additive", harder_add),
                   ("  harder, propor. ", harder_mul)]:
        print(f"{lab} mean {d['mean']:.2f}  pass {d['pass_pct']:5.1f}  "
              f"<=2 {d['le2_pct']:5.1f}  zero {d['zero_pct']:4.2f}  "
              f">=9 {d.get('top_pct', float('nan')):4.2f}  loss {d.get('loss', 0):.2f}")
    print(f"  published 2026    mean {OBS_2026['mean']:.2f}  pass "
          f"{OBS_2026['pass_pct']:5.1f}  <=2 {OBS_2026['le2_pct']:5.1f}  "
          f"zero {OBS_2026['zero_pct']:4.2f}  >=9  n/p  (no 2026 band table published)")
    print("\nsensitivity:", json.dumps(sens, indent=1))


if __name__ == "__main__":
    import sys
    replot() if "--replot" in sys.argv else main()
