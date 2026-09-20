#!/usr/bin/env python3
"""What the paper is actually made of: exposure, granularity, and the capped channel.

Scripts 26 and 27 model the 2026 marking regime as twenty-eight sub-tasks, every one of
them able to attract a missing unit, a wrong prefix or a rounding error, and they leave
the linguistic channel out altogether on the grounds that the dossier has no basis for
a rate.  Both of those are wrong, and the coordination supplied the corrections.

  1. NOT EVERY SUB-TASK CAN ATTRACT A UNIT ERROR.  The paper is marked in quanta of
     0.25 and many of those quanta ask for something that has no units and no number:
     a definition, a qualitative judgement, a comparison with its justification, a
     statement of which law applies and why, a sketch.  A missing unit cannot be
     committed there.  This is measurable rather than assumable: the corrector's
     document for 2026 lists every sub-item with its point value and its content, so
     the coding in data/exam_subtask_coding_2026.csv reads the exposure off the paper.

  2. THE LINGUISTIC CHANNEL IS CAPPED.  The Basque criteria deduct 0.10 from the THIRD
     spelling error, up to 1.00; they allow up to 0.50 for syntax and coherence; and
     they cap the two together at 1.00, ten per cent of the paper.  This was already in
     data/marking_rules_2025_2026.csv when the regime sections were written, and those
     sections nonetheless said the channel was unmodelled and that the dossier
     therefore UNDERSTATED the regime.  A capped channel does not understate anything:
     it is bounded, and the bound is 1.00 mark however many errors are made.

  3. THE GRANULARITY IS ITSELF PART OF THE 2026 CHANGE, AND IT PUSHES THE OTHER WAY.
     The same table records that the 0.25 sub-items (a.1, a.2, …) are new in 2026; the
     2025 criteria did not itemise them.  Itemisation is a decision taken to help
     candidates — failing a sub-question costs a quarter of a point rather than an
     apartado, and more elements of knowledge get their own chance to be credited.  It
     therefore RAISES marks, against deductions that lower them, which means the true
     penalty burden behind an observed fall of 1.48 is larger than a model that omits
     the granularity implies.  It has two further consequences the dossier had not
     connected: it puts the competency items and the traditional ones on the same
     footing, diluting the paradigm change on purpose, and it generates statement text,
     which makes granularity a SECOND and independent source of the reading load.

WHAT THIS SCRIPT DOES.  It codes the 2026 paper sub-item by sub-item, measures the
exposure, re-runs the deduction channel restricted to the sub-tasks that can actually
receive a deduction, adds the capped linguistic channel, and re-states the budget.

Reads : data/exam_subtask_coding_2026.csv, data/marking_rules_2025_2026.csv,
        data/analysis/euskadi_grade_bands_2015_2025.csv
Writes: data/analysis/marking_exposure.json, data/tables/exposure_coding.md,
        data/tables/exposure_effect.md, data/tables/language_channel.md,
        plots/fig32_marking_exposure.(png|svg)
"""
from __future__ import annotations

import importlib.util
import json
import re
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

_spec = importlib.util.spec_from_file_location(
    "penalty_regime", Path(__file__).resolve().parent / "26_penalty_regime.py")
PR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PR)

N = 200_000
QUANTUM = 0.25          # the grading step the whole scheme is built on
DEDUCTION = 0.10        # and the penalty, which is not a multiple of it
LANG_CAP = 1.00         # ten per cent of the paper, spelling and syntax together
FREE_ERRORS = 2         # the deduction starts at the third
FALL = -1.48
FISICA_SPECIFIC = -1.10
OBS_2026 = PR.OBS_2026


WEIGHT = re.compile(r"\(\s*[\d.,]+[\s\n]*(?:U|EH)?[\s\n]*puntos?\s*\)")
EX = ROOT / "sources" / "exams"


def statement_structure(fname: str) -> dict:
    """Split each printed statement into narrative, demand text and printed weights.

    The dossier has been reading the 45 per cent growth in the statements as a cost of
    the competency items.  The coordination's account of the granularity suggests a
    different source: a paper marked in itemised quanta has to PRINT each quantum's
    demand and each quantum's price, and that is text nobody wrote for its own sake.
    The two readings are separable by measurement, because the contextual narrative
    and the demand text are different parts of the same statement.

      narrative   the scenario, the data, the framing — the competency wrapper
      demands     everything that says what to do: the apartado lead-ins and the
                  numbered sub-demands nested inside them.  The split between those
                  two is not clean (one 2026 item states its demands in the lead-in
                  and does not number them), so they are reported together as well as
                  separately.
      weights     the printed "(0.25 puntos)" annotations, which exist only because
                  the marking is itemised on the paper.
    """
    t = (EX / fname).read_text(encoding="utf-8")
    t = re.sub(r"UNIBERTSITATEAN.*?(FÍSICA|FISIKA)", " ", t, flags=re.S)
    t = "\n".join(l for l in t.split("\n") if l.strip() not in ("U", "EH", ""))
    starts = [(m.group(1), m.start()) for m in re.finditer(r"^\s*([ABCD]\d)\.-", t, re.M)]
    items, agg = {}, dict(total=0, narrative=0, lead=0, sub=0, demands=0,
                          n_ap=0, n_sub=0, n_weights=0, weight_w=0)
    for i, (lab, s) in enumerate(starts):
        e = starts[i + 1][1] if i + 1 < len(starts) else len(t)
        b = t[s:e]
        nw = WEIGHT.findall(b)
        b2 = WEIGHT.sub(" ", b)
        sub_w = n_sub = 0
        for m in re.finditer(r"^\s*\d\.\s+(.*?)(?=^\s*\d\.\s+|^\s*[abcd]\)|\Z)",
                             b2, re.M | re.S):
            sub_w += len(m.group(1).split()); n_sub += 1
        lead_w = n_ap = 0
        for m in re.finditer(r"^\s*[abcd]\)\s+(.*?)(?=^\s*\d\.\s+|^\s*[abcd]\)|\Z)",
                             b2, re.M | re.S):
            lead_w += len(m.group(1).split()); n_ap += 1
        tot = len(b2.split())
        items[lab] = dict(total=tot, narrative=tot - lead_w - sub_w, lead=lead_w,
                          sub=sub_w, demands=lead_w + sub_w, n_ap=n_ap, n_sub=n_sub,
                          n_weights=len(nw),
                          weight_w=sum(len(w.split()) for w in nw))
        for k in agg:
            agg[k] += items[lab][k]
    return dict(items=items, total=agg)


def paths():
    """The four papers a candidate can actually sit, from the corrector's document."""
    d = pd.read_csv(ROOT / "data" / "exam_subtask_coding_2026.csv")
    out = {}
    for a in "AB":
        for b in "AB":
            s = d[(d.option == "-")
                  | ((d.exercise == 3) & (d.option == a))
                  | ((d.exercise == 4) & (d.option == b))].reset_index(drop=True)
            # each apartado (exercise, letter) is the unit a grave error voids
            ap = (s.exercise.astype(str) + s.subitem.str[0]).astype("category").cat.codes
            out[f"3{a}+4{b}"] = dict(
                subtask=s.points.to_numpy(float),
                apartado_of=ap.to_numpy(int),
                exposed=s.units_exposed.to_numpy(bool),
                text=s.text_produced.to_numpy(bool),
                n=len(s), n_exposed=int(s.units_exposed.sum()),
                pts_exposed=float(s.loc[s.units_exposed == 1, "points"].sum()),
                n_text=int(s.text_produced.sum()),
                pts_text=float(s.loc[s.text_produced == 1, "points"].sum()),
                quanta=int(round(s.points.sum() / QUANTUM)),
                by_demand=s.groupby("demand").points.agg(["size", "sum"]).to_dict("index"),
            )
    return d, out


def run(p, ded_rate, voiding=None, lang=None, restrict=True, n=N, **kw):
    v = voiding or (0.0, 0.0)
    return PR.simulate(ded_rate, v[0], v[1], n=n,
                       subtask=p["subtask"], apartado_of=p["apartado_of"],
                       exposed=p["exposed"] if restrict else None,
                       lang=lang, **kw)


def invert(p, target, restrict=True, lang=None, n=60_000, hi=120.0):
    lo = 0.0
    for _ in range(30):
        mid = (lo + hi) / 2
        s = run(p, mid, restrict=restrict, lang=lang, n=n)["shift"]
        lo, hi = (mid, hi) if s > target else (lo, mid)
    return (lo + hi) / 2


def draw(struct, coding, eff, langs, bound, joint, f, a25, a26):
    """Figure 32. Split out so it can be redrawn from the JSON alone."""
    fig, axes = plt.subplots(2, 2, figsize=(13.2, 9.2))

    ax = axes[0, 0]
    order = ["numerical", "symbolic", "definition", "judgement", "graph"]
    cols = {"numerical": C["violet"], "symbolic": C["blue"], "definition": C["aqua"],
            "judgement": C["orange"], "graph": C["yellow"]}
    labels, left = list(struct.keys()), np.zeros(len(struct))
    y = np.arange(len(labels))[::-1]
    for dem in order:
        vals = []
        for k in labels:
            s = coding[(coding.option == "-")
                       | ((coding.exercise == 3) & (coding.option == k[1]))
                       | ((coding.exercise == 4) & (coding.option == k[4]))]
            vals.append(float(s.loc[s.demand == dem, "points"].sum()))
        vals = np.array(vals)
        ax.barh(y, vals, left=left, height=0.55, color=cols[dem], label=dem)
        for yy, v, l0 in zip(y, vals, left):
            if v >= 0.6:
                ax.text(l0 + v / 2, yy, f"{v:.2f}", ha="center", va="center",
                        fontsize=7.6, color="white" if dem in ("numerical", "blue") else INK)
        left = left + vals
    for yy, k in zip(y, labels):
        ax.text(10.2, yy, f"{struct[k]['pct_marks_exposed']:.0f} %\nexposed",
                va="center", fontsize=7.2, color=MUTED, linespacing=1.25)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlim(0, 15.4); ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_xlabel("marks, out of 10.00")
    ax.legend(fontsize=7.4, loc="center right", frameon=True, handlelength=1.1,
              borderpad=0.5)
    ax.set_title("(a) What the paper is made of\nonly the numerical part can lose a "
                 "unit", loc="left")
    ax.grid(axis="y", visible=False)

    ax = axes[0, 1]
    xs = np.array([e["ded_rate"] for e in eff], dtype=float)
    n_ex = eff[0]["ded_rate"] / eff[0]["per_exposed_subtask"]
    ax.plot(xs, [e["shift_all"] for e in eff], color=MUTED, lw=1.8, ls=":", marker="o",
            ms=4, label="spread over all sub-items")
    ax.plot(xs, [e["shift_exposed"] for e in eff], color=C["violet"], lw=2.2,
            marker="o", ms=4, label="spread over the exposed ones")
    for lab, v, c in [("the Física-specific $-1.10$", -1.10, C["orange"]),
                      ("the observed $-1.48$", FALL, INK2)]:
        ax.axhline(v, color=c, lw=0.9, ls="--")
        ax.text(0.04, v + 0.06, lab, fontsize=7.4, color=c)
    ax.axvline(n_ex, color=C["red"], lw=1.0, ls="-.")
    ax.text(n_ex - 0.6, -0.30, "one penalty on every\nnumerical answer\nof every "
            "script", fontsize=7.2, color=C["red"], ha="right")
    ax.set_xlabel("deductions of $0.10$ per script")
    ax.set_ylabel("shift in the mean (marks)")
    ax.set_xlim(0, 32); ax.set_ylim(-2.25, 0.05)
    ax.legend(fontsize=7.6, loc="lower left")
    top = ax.secondary_xaxis("top", functions=(lambda v: v / n_ex,
                                               lambda v: v * n_ex))
    top.set_xlabel("per exposed sub-item — the currency the tally can count",
                   fontsize=8.4)
    ax.set_title("(b) The price in the currency that can be counted\nper numerical "
                 "answer, not per script", loc="left")

    ax = axes[1, 0]
    xs = [l["mean_errors"] for l in langs]
    ax.plot(xs, [l["lang_shift"] for l in langs], color=C["green"], lw=2.2, marker="o",
            ms=4)
    ax.axhline(bound["lang_shift"], color=C["red"], lw=1.2, ls="--")
    ax.text(2.0, 0.985, f"the cap: {bound['lang_shift']:.2f} even if every script "
            "loses the maximum 1.00", fontsize=7.4, color=C["red"], ha="left")
    ax.scatter([f["em"]], [joint["lang_shift"]], s=90, color=C["violet"], zorder=4)
    ax.annotate(f"what the four published\nfigures actually want:\n{f['em']} error, "
                f"{joint['lang_shift']:.02f} marks",
                (f["em"], joint["lang_shift"]), textcoords="offset points",
                xytext=(52, 40), fontsize=7.4, color=C["violet"],
                arrowprops=dict(arrowstyle="->", color=C["violet"], lw=0.9))
    ax.set_xlabel("mean spelling errors per script")
    ax.set_ylabel("marks the linguistic channel removes")
    ax.set_xlim(-1, 41); ax.set_ylim(0, 1.05)
    ax.set_title("(c) The channel that was called an understatement\nit is capped, "
                 "and the data crowd it out", loc="left")

    ax = axes[1, 1]
    parts = [("narrative and context", "narrative", C["aqua"]),
             ("demand text", "demands", C["violet"]),
             ("printed weights", "weight_w", C["orange"])]
    x = np.arange(2)
    bottom = np.zeros(2)
    for lab, key, col in parts:
        vals = np.array([a25[key], a26[key]], dtype=float)
        ax.bar(x, vals, bottom=bottom, width=0.5, color=col, label=lab)
        for xx, v, b0 in zip(x, vals, bottom):
            if v >= 40:
                ax.text(xx, b0 + v / 2, f"{v:.0f}", ha="center", va="center",
                        fontsize=8.4, color="white" if col != C["orange"] else INK)
        bottom = bottom + vals
    ax.annotate("", xy=(0.26, a25["narrative"]), xytext=(0.74, a26["narrative"]),
                arrowprops=dict(arrowstyle="<-", color=INK2, lw=1.2))
    ax.text(0.5, 200, f"the competency wrapper got\nSHORTER by "
            f"{a25['narrative']-a26['narrative']} words",
            ha="center", fontsize=7.8, color=INK2)
    ax.set_xticks(x); ax.set_xticklabels(["2025", "2026"], fontsize=10)
    ax.set_ylabel("words in all the printed statements")
    ax.set_ylim(0, 1900)
    ax.legend(fontsize=7.6, loc="upper left")
    ax.set_title("(d) Where the reading load came from\nnesting and prices, not "
                 "narrative", loc="left")
    ax.grid(axis="x", visible=False)

    fig.suptitle("Figure 32 — What the paper is made of: exposure, the capped channel, "
                 "and the true source of the reading load",
                 x=0.005, ha="left", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    _save(fig, "fig32_marking_exposure", PLOTS)


def replot() -> None:
    """Redraw figure 32 from data/analysis/marking_exposure.json, without refitting."""
    d = json.loads((A / "marking_exposure.json").read_text(encoding="utf-8"))
    coding = pd.read_csv(ROOT / "data" / "exam_subtask_coding_2026.csv")
    draw(d["structure"], coding, d["exposure_effect"], d["language_dose"],
         d["language_bound"], d["joint_fit"]["result"], d["joint_fit"]["fitted"],
         d["statement_structure"]["y2025"], d["statement_structure"]["y2026"])
    print("figure 32 redrawn from data/analysis/marking_exposure.json")


def main() -> None:
    coding, P = paths()
    ref = P["3A+4B"]        # the modal path: 32 sub-items, the median exposure

    # ---- 1. what the paper is made of -----------------------------------------
    struct = {k: {kk: v[kk] for kk in
                  ("n", "n_exposed", "pts_exposed", "n_text", "pts_text", "quanta")}
              for k, v in P.items()}
    for k, v in struct.items():
        v["pct_subitems_exposed"] = round(v["n_exposed"] / v["n"] * 100, 1)
        v["pct_marks_exposed"] = round(v["pts_exposed"] / 10.0 * 100, 1)
        v["pct_marks_text"] = round(v["pts_text"] / 10.0 * 100, 1)

    # ---- 2. what restricting the deductions to the exposed sub-tasks costs -----
    eff = []
    for rate in (6, 9, 12, 16, 20, 25, 30):
        a = run(ref, rate, restrict=False)
        b = run(ref, rate, restrict=True)
        eff.append(dict(
            ded_rate=rate,
            shift_all=a["shift"], shift_exposed=b["shift"],
            per_ded_all=abs(a["shift"]) / max(a["deductions_per_script"], 1e-9),
            per_ded_exposed=abs(b["shift"]) / max(b["deductions_per_script"], 1e-9),
            ratio=abs(b["shift"]) / max(abs(a["shift"]), 1e-9),
            per_exposed_subtask=rate / ref["n_exposed"],
        ))

    need = {}
    for lab, tgt in [("the Física-specific −1.10", FISICA_SPECIFIC),
                     ("the observed −1.48", FALL)]:
        need[lab] = dict(
            all_subtasks=float(invert(ref, tgt, restrict=False)),
            exposed_only=float(invert(ref, tgt, restrict=True)),
        )
        need[lab]["per_exposed_subtask"] = (need[lab]["exposed_only"]
                                            / ref["n_exposed"])
        need[lab]["exceeds_exposed"] = bool(need[lab]["exposed_only"]
                                            > ref["n_exposed"])

    # ---- 2b. the quantum against the deduction ---------------------------------
    # The scheme is built on a 0.25 step -- forty quanta over the 10.00 -- and the
    # penalty is 0.10, which is not a multiple of it. A sub-item hit once is worth
    # 0.15. So the deductions take every script off the grid the design is built on.
    q = run(ref, 12, voiding=(0.16, 0.03), n=100_000)
    on_grid_before = run(ref, 0.0, n=100_000)
    grid = dict(
        quanta=ref["quanta"], quantum=QUANTUM, deduction=DEDUCTION,
        deduction_in_quanta=DEDUCTION / QUANTUM,
        note=("0.10 is two fifths of a quantum, so one deduction moves a sub-item off "
              "the grid and two do not bring it back. Whatever else the deductions "
              "did, they dissolved the granularity the same criteria had just "
              "introduced."),
    )

    # ---- 3. the capped linguistic channel --------------------------------------
    # The cap is what makes this channel bounded, so the dose-response is the point:
    # it saturates, and it saturates well below the fall it was once said to add to.
    langs = []
    for e_mean in (0, 1, 2, 3, 4, 6, 8, 12, 20, 40):
        r = run(ref, 0.0, lang=(e_mean, 0.10))
        langs.append(dict(mean_errors=e_mean, shift=r["shift"],
                          lang_shift=r["lang_shift"],
                          pass_pct=r["pass_pct"], le2_pct=r["le2_pct"],
                          zero_pct=r["zero_pct"]))
    # the absolute bound: every script at the cap
    bound = run(ref, 0.0, lang=(400.0, 1.0))

    # who writes badly: the shape matters because the zero rate constrains it
    lshapes = []
    for sh in [(2.0, 2.0), (2.0, 1.5), (1.5, 2.0), (3.0, 2.0), (1.2, 1.2)]:
        for em in (2, 4, 8):
            r = run(ref, 12, voiding=(0.16, 0.03), lang=(em, 0.10), lang_shape=sh,
                    n=80_000)
            lshapes.append(dict(lang_shape=list(sh), mean_errors=em,
                                mean=r["mean"], zero_pct=r["zero_pct"],
                                pass_pct=r["pass_pct"], le2_pct=r["le2_pct"],
                                lang_shift=r["lang_shift"], loss=float(PR.loss(r))))

    # ---- 4. the three channels together ----------------------------------------
    combos = []
    for lab, kw in [
            ("deductions only, all sub-tasks", dict(ded_rate=12, restrict=False)),
            ("deductions only, exposed only", dict(ded_rate=12, restrict=True)),
            ("+ voiding", dict(ded_rate=12, restrict=True, voiding=(0.16, 0.03))),
            ("+ voiding + language (4 errors)",
             dict(ded_rate=12, restrict=True, voiding=(0.16, 0.03), lang=(4.0, 0.10))),
            ("+ voiding + language (8 errors)",
             dict(ded_rate=12, restrict=True, voiding=(0.16, 0.03), lang=(8.0, 0.10))),
    ]:
        r = run(ref, **kw)
        r["label"] = lab
        r["loss"] = float(PR.loss(r))
        r["share_of_fisica"] = abs(r["shift"]) / abs(FISICA_SPECIFIC) * 100
        combos.append(r)

    # ---- 5. the three channels fitted together ---------------------------------
    # Every earlier fit held the language channel at zero because it was unmodelled.
    # With a cap, a shape and an exposure mask it can be fitted like the others, and
    # the point of doing so is that the four published figures then have to divide
    # themselves between three mechanisms instead of two.
    best = None
    for ded in (6, 9, 12, 15, 18, 22):
        for pp in (0.06, 0.10, 0.16, 0.22, 0.28, 0.36):
            for pt in (0.015, 0.030, 0.045, 0.060, 0.080):
                for em in (0, 1, 2, 3, 5):
                    r = PR.simulate(ded, pp, pt, n=30_000,
                                    subtask=ref["subtask"],
                                    apartado_of=ref["apartado_of"],
                                    exposed=ref["exposed"],
                                    lang=(em, 0.10) if em else None)
                    L = PR.loss(r)
                    if best is None or L < best[0]:
                        best = (L, dict(ded=ded, pp=pp, pt=pt, em=em))
    f = best[1]
    joint = PR.simulate(f["ded"], f["pp"], f["pt"], n=N, subtask=ref["subtask"],
                        apartado_of=ref["apartado_of"], exposed=ref["exposed"],
                        lang=(f["em"], 0.10) if f["em"] else None)
    joint["loss"] = float(PR.loss(joint))
    joint["on_grid_boundary"] = bool(f["ded"] in (6, 22) or f["pp"] in (0.06, 0.36)
                                     or f["pt"] in (0.015, 0.080) or f["em"] == 5)
    joint["language_wants_zero"] = bool(f["em"] == 0)
    # what each channel is worth at the joint optimum, added one at a time
    ladder = []
    prev = 0.0
    for lab, kw in [
            ("deductions alone", dict(ded_rate=f["ded"], restrict=True)),
            ("+ grave-error voiding",
             dict(ded_rate=f["ded"], restrict=True, voiding=(f["pp"], f["pt"]))),
            ("+ the capped language channel",
             dict(ded_rate=f["ded"], restrict=True, voiding=(f["pp"], f["pt"]),
                  lang=(f["em"], 0.10) if f["em"] else None)),
    ]:
        r = run(ref, **{k: v for k, v in kw.items() if k != "ded_rate"},
                ded_rate=kw["ded_rate"])
        ladder.append(dict(label=lab, cumulative=r["shift"],
                           marginal=r["shift"] - prev,
                           share_of_fisica=abs(r["shift"]) / abs(FISICA_SPECIFIC) * 100,
                           mean=r["mean"], pass_pct=r["pass_pct"],
                           le2_pct=r["le2_pct"], zero_pct=r["zero_pct"],
                           top_pct=r["top_pct"], loss=float(PR.loss(r))))
        prev = r["shift"]

    # ---- 6. the over-attribution the four figures force --------------------------
    # A regime fitted to the four published 2026 figures reproduces the whole observed
    # fall of -1.48 by construction. But the subject decomposition says at most -1.10
    # of that fall is Física's own: -1.18 of it moved every Basque subject at once and
    # cannot be the Física marking sheet. So a regime fitted to all four figures is
    # necessarily OVER-attributed, and by a knowable amount. Fitting the deduction
    # count to carry -1.10 instead says what the regime looks like when it is asked
    # only for the part that can be its.
    constrained = {}
    for lab, tgt in [("fitted to the observed −1.48", FALL),
                     ("constrained to the Física-specific −1.10", FISICA_SPECIFIC)]:
        lo, hi = 0.0, 40.0
        for _ in range(28):
            mid = (lo + hi) / 2
            s = run(ref, mid, voiding=(f["pp"], f["pt"]), n=50_000)["shift"]
            lo, hi = (mid, hi) if s > tgt else (lo, mid)
        c = (lo + hi) / 2
        r = run(ref, c, voiding=(f["pp"], f["pt"]))
        constrained[lab] = dict(
            target=tgt, ded_rate=float(c), shift=r["shift"], mean=r["mean"],
            pass_pct=r["pass_pct"], le2_pct=r["le2_pct"], zero_pct=r["zero_pct"],
            per_exposed_subtask=float(c) / ref["n_exposed"],
            loss=float(PR.loss(r)))
    over = (abs(constrained["fitted to the observed −1.48"]["shift"])
            - abs(FISICA_SPECIFIC))
    constrained["over_attribution"] = dict(
        marks=float(over),
        note=("A regime fitted to all four published figures carries this much more "
              "than the subject decomposition allows Física. It is not evidence that "
              "the decomposition is wrong; it is the arithmetic reason the fitted "
              "regime has to be read as a ceiling."))

    # ---- 7. what the statement growth is actually made of -----------------------
    st25 = statement_structure("pv_2025_ord_es.txt")
    st26 = statement_structure("pv_2026_ord.txt")
    a25, a26 = st25["total"], st26["total"]
    stmt = dict(
        y2025=a25, y2026=a26,
        change={k: a26[k] - a25[k] for k in a25},
        per_statement=dict(
            n_printed_2025=7, n_printed_2026=6,
            narrative=[a25["narrative"] / 7, a26["narrative"] / 6],
            demands=[a25["demands"] / 7, a26["demands"] / 6],
            weights=[a25["weight_w"] / 7, a26["weight_w"] / 6]),
        finding=("The contextual narrative did not grow. Per printed statement it is "
                 "unchanged -- 71 words against 70 -- while the demand text more than "
                 "doubled, 88 against 181. All of the growth "
                 "is in the text that states what to do, which is what an itemised "
                 "marking scheme forces onto the paper — a lead-in for each apartado, "
                 "a sentence for each quantum inside it, and a printed price for "
                 "both. The dossier had been attributing the reading load to the "
                 "competency items; on this measurement the competency wrapper is "
                 "the same size per statement as in 2025 and the granularity is the "
                 "whole of the increase."),
        caveat=("One 2026 item (C1, the waves option) states its demands in the "
                "apartado lead-in and does not number them, so the lead-in/sub-demand "
                "split is not clean item by item. Their SUM — the demand text — is, "
                "and it is the quantity the finding rests on."),
    )

    out = dict(
        note=("The exposure is measured from the corrector's document, not assumed. "
              "The linguistic channel is capped by the published criteria at 1.00, "
              "ten per cent of the paper, and the cap is the point."),
        source=("sources/text/ehu_fisica_solucionario_ord_2026.txt, the per-subitem "
                "point distribution of each of the six exercises; coded in "
                "data/exam_subtask_coding_2026.csv"),
        quantum=QUANTUM, deduction=DEDUCTION,
        quantum_note=("The paper is marked in quanta of 0.25 — forty of them over the "
                      "10.00 — and the deduction is 0.10, which is not a multiple of "
                      "the quantum. A 0.25 sub-item hit once is worth 0.15, off the "
                      "grid the scheme is built on."),
        language_rule=dict(cap=LANG_CAP, free_errors=FREE_ERRORS,
                           per_error=DEDUCTION, syntax_max=0.50,
                           source="data/marking_rules_2025_2026.csv, País Vasco 2025 "
                                  "and 2026 (the rule is the same in both years; what "
                                  "the coordination reports changing is its "
                                  "application)"),
        structure=struct,
        by_demand={k: dict(n=int(v["size"]), points=float(v["sum"]))
                   for k, v in coding.groupby("demand").points
                   .agg(["size", "sum"]).to_dict("index").items()},
        exposure_effect=eff,
        deductions_required=need,
        language_dose=langs,
        grid_vs_deduction=grid,
        language_shape_sensitivity=lshapes,
        joint_fit=dict(fitted=f, result=joint),
        channel_ladder=ladder,
        constrained_fit=constrained,
        statement_structure=stmt,
        language_bound=dict(shift=bound["shift"], lang_shift=bound["lang_shift"],
                            note="every script at the 1.00 cap; the absolute maximum "
                                 "the linguistic channel can be worth"),
        channels_together=combos,
        withdrawn=("The claim that the dossier 'understates the regime by whatever the "
                   "third channel is worth'. The third channel is capped at 1.00 and "
                   "the cap was in the repository's own marking-rules table when that "
                   "sentence was written."),
    )
    (A / "marking_exposure.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    # ---- tables ------------------------------------------------------------------
    L = ["| The paper a candidate sits | Sub-items | Quanta of 0.25 | "
         "Can take a unit error | Marks exposed | Produces text | Marks of text |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for k, v in struct.items():
        L.append(f"| {k} | {v['n']} | {v['quanta']} | {v['n_exposed']} "
                 f"({v['pct_subitems_exposed']:.0f} %) | {v['pts_exposed']:.2f} "
                 f"({v['pct_marks_exposed']:.0f} %) | {v['n_text']} | "
                 f"{v['pts_text']:.2f} ({v['pct_marks_text']:.0f} %) |")
    L += ["", "Read off the corrector's document for 2026, which lists every sub-item "
          "with its point value and its content, and coded in "
          "`data/exam_subtask_coding_2026.csv`. A candidate sits exercises 1 and 2 and "
          "one option of each of 3 and 4, so there are four papers. **Between a half "
          "and two thirds of the sub-items can attract a missing unit, a wrong prefix "
          "or a rounding error**; the rest ask for a definition, a judgement, a "
          "comparison with its justification or a sketch, where those errors cannot be "
          "made. The earlier model spread the deductions over all of them. The last "
          "two columns are the other side of the same coin: between a fifth and a "
          "third of the marks come from text, which is where the capped linguistic "
          "channel applies. File: `data/analysis/marking_exposure.json`."]
    (TABLES / "exposure_coding.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = ["| Deductions per script | Per exposed sub-item | Spread over all sub-items | "
         "Spread over the exposed ones | Ratio |", "|---:|---:|---:|---:|---:|"]
    for e in eff:
        L.append(f"| {e['ded_rate']} | {e['per_exposed_subtask']:.2f} | "
                 f"{e['shift_all']:+.2f} | {e['shift_exposed']:+.2f} | "
                 f"{e['ratio']*100:.0f} % |")
    L += ["", "Restricting the deductions to the sub-items that can actually receive "
          "one concentrates them, and concentration wastes them: two penalties on the "
          "same 0.25 sub-item cannot take 0.20 from it. The effect is small at the "
          "fitted intensity and grows with it. The second column is the one to read "
          f"in a meeting: at the fitted twelve deductions it is "
          f"{eff[2]['per_exposed_subtask']:.2f} — **a penalty on two out of every "
          "three numerical answers, in every script**. To carry the whole observed "
          f"fall alone it would be {need['the observed −1.48']['per_exposed_subtask']:.2f}"
          ", which is more than one penalty on every numerical answer there is."]
    (TABLES / "exposure_effect.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = ["| Mean spelling errors per script | What the channel costs | Pass % | "
         "At or below 2 % | Zero % |", "|---:|---:|---:|---:|---:|"]
    for l in langs:
        L.append(f"| {l['mean_errors']} | {l['lang_shift']:.3f} | {l['pass_pct']:.1f} | "
                 f"{l['le2_pct']:.1f} | {l['zero_pct']:.2f} |")
    L.append(f"| *every script at the cap* | *{bound['lang_shift']:.3f}* | — | — | — |")
    L += ["", "The third channel, which the regime sections said was unmodelled and "
          "which they said made the dossier **understate** the regime. It does not: "
          "the Basque criteria deduct 0.10 from the *third* spelling error, allow up "
          "to 0.50 for syntax and coherence, and **cap the two together at 1.00**, ten "
          "per cent of the paper — a rule that was already in "
          "`data/marking_rules_2025_2026.csv` when that sentence was written, and that "
          "is the same in 2025 and in 2026. A capped channel is bounded, and the last "
          f"row is the bound: {bound['lang_shift']:.2f} marks even if every script in "
          "Euskadi lost the maximum. The column that matters is not that one, though. "
          f"Fitted jointly with the other two channels, the four published figures "
          f"want **{f['em']} error per script**, worth "
          f"{joint['lang_shift']:.3f} marks — the channel is not merely bounded, it is "
          "crowded out. Push it harder and the fit degrades, because the mean and the "
          "pass rate move together in a way the published pair does not allow."]
    (TABLES / "language_channel.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    n25, n26 = 7, 6      # printed statements; a candidate answers four of either
    L = ["| | Narrative and context | Demand text | Printed prices | Statement total |",
         "|---|---:|---:|---:|---:|",
         f"| 2025, all {n25} printed statements | {a25['narrative']} | "
         f"{a25['demands']} | {a25['weight_w']} | {a25['total'] + a25['weight_w']} |",
         f"| 2026, all {n26} printed statements | {a26['narrative']} | "
         f"{a26['demands']} | {a26['weight_w']} | {a26['total'] + a26['weight_w']} |",
         f"| **2025, per printed statement** | **{a25['narrative']/n25:.0f}** | "
         f"**{a25['demands']/n25:.0f}** | **{a25['weight_w']/n25:.0f}** | "
         f"**{(a25['total']+a25['weight_w'])/n25:.0f}** |",
         f"| **2026, per printed statement** | **{a26['narrative']/n26:.0f}** | "
         f"**{a26['demands']/n26:.0f}** | **{a26['weight_w']/n26:.0f}** | "
         f"**{(a26['total']+a26['weight_w'])/n26:.0f}** |",
         f"| *2026 against 2025, per statement* | "
         f"*{(a26['narrative']/n26)/(a25['narrative']/n25)*100:.0f} %* | "
         f"*{(a26['demands']/n26)/(a25['demands']/n25)*100:.0f} %* | *—* | "
         f"*{((a26['total']+a26['weight_w'])/n26)/((a25['total']+a25['weight_w'])/n25)*100:.0f} %* |"]
    L += ["", "The words of all the printed statements of each paper, split by what "
          "they do. **Narrative and context** is the competency wrapper: the scenario, "
          "the data, the framing. **Demand text** is everything that says what to do — "
          "the apartado lead-ins and the numbered sub-demands nested inside them. "
          "**Printed prices** are the `(0.25 puntos)` annotations, which exist only "
          "because the marking is itemised on the paper. The result is not the one the "
          "dossier expected. The 2025 paper printed seven statements and the 2026 "
          "paper six, so the row to read is the per-statement one: **the competency "
          "wrapper is the same size it was** — 71 words a statement against 70, 99 per "
          "cent — while the **demand text more than doubled**, 88 words a statement "
          "against 181, and the printed prices went from nothing to 17. A paper "
          "marked in itemised quanta has "
          "to print each quantum's demand and each quantum's price; that is where the "
          f"reading load came from. The 2025 paper had {a25['n_sub']} numbered demands "
          f"and no nesting; the 2026 paper has {a26['n_ap']} apartado lead-ins with "
          f"{a26['n_sub']} numbered demands inside them and {a26['n_weights']} printed "
          "weights. One 2026 item states its demands in the lead-in without numbering "
          "them, so the lead-in and sub-demand columns are combined here; their sum is "
          "the measurement the finding rests on."]
    (TABLES / "statement_structure.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    draw(struct, coding, eff, langs, bound, joint, f, a25, a26)

    print(json.dumps(struct, indent=1))
    print("\nexposure effect:")
    for e in eff:
        print(f"  rate {e['ded_rate']:3d}  all {e['shift_all']:+.3f}  "
              f"exposed {e['shift_exposed']:+.3f}  ratio {e['ratio']*100:5.1f}%  "
              f"per exposed sub-task {e['per_exposed_subtask']:.2f}")
    print("\ndeductions required:")
    for k, v in need.items():
        print(f"  {k}: all {v['all_subtasks']:.1f}, exposed only "
              f"{v['exposed_only']:.1f} ({v['per_exposed_subtask']:.2f} per exposed "
              f"sub-task){'  [> the exposed sub-tasks there are]' if v['exceeds_exposed'] else ''}")
    print("\nlanguage channel (capped at 1.00):")
    for l in langs:
        print(f"  mean errors {l['mean_errors']:3d}  costs {l['lang_shift']:.3f}")
    print(f"  absolute bound, every script at the cap: {bound['lang_shift']:.3f}")
    print("\nlanguage shape sensitivity (ded 12, voiding fitted):")
    for l in lshapes:
        print(f"  shape {tuple(l['lang_shape'])}  errors {l['mean_errors']:2d}  "
              f"mean {l['mean']:.2f}  zero {l['zero_pct']:5.2f}  "
              f"lang {l['lang_shift']:.3f}  loss {l['loss']:6.1f}")
    print(f"\njoint fit: {f}  loss {joint['loss']:.2f}"
          f"{'  [boundary]' if joint['on_grid_boundary'] else ''}")
    print(f"  mean {joint['mean']:.2f}  pass {joint['pass_pct']:.1f}  "
          f"<=2 {joint['le2_pct']:.1f}  zero {joint['zero_pct']:.2f}  "
          f">=9 {joint['top_pct']:.2f}  language worth {joint['lang_shift']:.3f}")
    print("\nchannel ladder at the joint optimum:")
    for l in ladder:
        print(f"  {l['label']:<30} cumulative {l['cumulative']:+.2f}  "
              f"marginal {l['marginal']:+.2f}  {l['share_of_fisica']:5.1f}% of -1.10  "
              f"loss {l['loss']:6.1f}")
    print("\nstatement structure, 2025 -> 2026:")
    for k in ("total", "narrative", "lead", "sub", "demands", "n_ap", "n_sub",
              "n_weights", "weight_w"):
        print(f"  {k:10s} {a25[k]:5d} -> {a26[k]:5d}   {a26[k]-a25[k]:+5d}")
    print("\nconstrained fits (voiding held at the joint optimum):")
    for k, v in constrained.items():
        if k == "over_attribution":
            print(f"  over-attribution: {v['marks']:+.2f} marks")
            continue
        print(f"  {k:<44} {v['ded_rate']:5.1f} deductions "
              f"({v['per_exposed_subtask']:.2f} per exposed sub-task)  "
              f"mean {v['mean']:.2f}  pass {v['pass_pct']:5.1f}  "
              f"<=2 {v['le2_pct']:5.1f}  zero {v['zero_pct']:4.2f}  loss {v['loss']:6.1f}")
    print("\nchannels together:")
    for c in combos:
        print(f"  {c['label']:<34} mean {c['mean']:.2f}  shift {c['shift']:+.2f}  "
              f"{c['share_of_fisica']:5.1f}% of −1.10  pass {c['pass_pct']:5.1f}  "
              f"<=2 {c['le2_pct']:5.1f}  zero {c['zero_pct']:4.2f}  loss {c['loss']:.1f}")


if __name__ == "__main__":
    import sys
    replot() if "--replot" in sys.argv else main()
