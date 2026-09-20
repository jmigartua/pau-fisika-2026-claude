#!/usr/bin/env python3
"""The path this analysis took, and what each step did to the previous conclusion.

The figures in chapters 2–6 were not produced in one pass. Each was built to answer
the question the previous one raised, and several of them weakened or overturned the
finding that motivated them. That sequence is itself a result: it shows how far the
answer moves as the frame widens, and that two of the statements most likely to be
quoted from this study were true only in the frame that produced them.

Nothing here is re-derived. Every number is read from the JSON emitted by the scripts
that computed it, so this figure cannot drift away from the analysis it narrates.

Reads : data/analysis/results.json, shape_locus.json, reference_frames.json
Writes: plots/fig18_analysis_path.(png|svg), data/analysis/analysis_path.json
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import numpy as np

from plot_style import C, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "data" / "analysis"
P = ROOT / "plots"

results = json.load(open(A / "results.json", encoding="utf-8"))
locus = json.load(open(A / "shape_locus.json", encoding="utf-8"))
frames = json.load(open(A / "reference_frames.json", encoding="utf-8"))

fr = {f["frame"]: f["delta"] for f in frames["frames"]}
nat_2025 = fr["2024 → 2025, nine communities"]                   # -0.65 (same nine communities as the other frames)
nat_2026 = fr["2025 → 2026, nine communities"]                   # +0.17
nat_base = fr["2015–19 baseline → 2026, nine communities"]  # +0.02
ehu_yoy = fr["2025 → 2026, Euskadi"]                             # -1.48
ehu_base = fr["2015–19 baseline → 2026, Euskadi"]           # -1.93

# STOOD / WEAKENED / OVERTURNED — what the LATER steps did to each step's claim.
STOOD, WEAK, OVER = "stood", "weakened", "overturned"
STATUS_COLOR = {STOOD: C["aqua"], WEAK: C["yellow"], OVER: C["red"]}

steps = [
    ("1. The July framing",
     "Euskadi Física fell 1.48 points; the new competency model is to blame.",
     OVER, "overturned at step 2: six of nine communities rose in 2026 under the same model"),
    ("2. The 2026 cross-section",
     "The 2026 fall is regional, not national. H1 survives only as a description of 2025.",
     STOOD, "the finding stands; its premise — that 2025 was a national collapse — does "
            "not, and is overturned at step 6"),
    ("3. Shape against location",
     "Canarias 2026 sits on the historical locus: the whole distribution moved down.",
     WEAK, "weakened at steps 4 and 5"),
    ("4. Where the evidence lies",
     "Only 2 of 187 region-years sit below mean 4.5; the locus there is extrapolated.",
     STOOD, "the claim of step 3 becomes 'consistent with', not 'demonstrated'"),
    ("5. The two distributions, decoupled",
     "The pass rate is normal; the 8–10 share is not, so its SD units are not calibrated.",
     STOOD, "top-band residuals are directional only"),
    ("6. Re-baselining to pre-COVID",
     "2020–24 was a plateau, not a decline; 2025 returned to the 2015–19 norm.",
     STOOD, "reverses the sign of the national story and enlarges the Basque one"),
    ("7. Conditioning on passing",
     "Among passers, the top-band share: the one measure least dominated by the level.",
     WEAK, "strengthens step 3; its two further claims — a plateau that reshaped, and a "
           "Basque turn in 2024 — were withdrawn at step 13, and the second was "
           "reinstated in a different form at step 14"),
    ("8. Testing the slow version of H4",
     "Do cohorts arrive less prepared each year? Not detectably — take-up is flat.",
     STOOD, "kills the recruitment mechanism, and corrects a dilution effect this "
            "study had itself reported from a phase-undercount of 2015–16"),
    ("9. Bringing in an outside instrument",
     "PISA 2006–2022: Basque science goes from +9 above Spain to −5, breaking in 2015.",
     WEAK, "the drift is real and pre-pandemic, but the cohorts do not match the PAU "
           "(1 of 3), which retracts the triangulation step 9 first claimed"),
    ("10. Comparing the two slopes",
     "On one scale, all four series fall; Euskadi is 1.7x Spain on BOTH instruments.",
     OVER, "on 2012–22 every interval includes zero; with PISA 2025 the PISA slopes are "
           "significant and the ratio is 2.1 — the records are steps, not slopes (step 13)"),
    ("11. Forecasting 2027 from PISA 2025",
     "Basque science falls to 458.5; top performers halve. Cohort term: −0.36 marks.",
     STOOD, "the two-year band of year-to-year variation is 6.5x larger, so 2027 is a policy "
            "outcome, not a prediction — the estimator's value is attribution after the fact"),
    ("12. Measuring the reading load",
     "Paper length vs grade change: r = −0.84, p = 0.008 — the strongest link yet.",
     WEAK, "but length and competency content correlate at +0.79, so it is a better "
            "instrument for the same change, not a second cause; the Madrid count was "
            "70 % solutions — corrected at step 13 (r = −0.905)"),
    ("13. The first audit (19 Sep, evening)",
     "Re-run everything, second-code the papers, recompute every number, read the logic.",
     STOOD, "withdrew the plateau reshaping (a level effect), the Basque 2024 signal "
            "(5 of 17 communities show it), the slope agreement (stale window); fixed the "
            "2027 proration and the Madrid count; found the plateau in every subject"),
    ("14. The second audit (20 Sep) and the decomposition",
     "Re-audit everything again; then ask what the fall is MADE of, not how large it is.",
     STOOD, "found 2024: a shape step (top band −5.9 pp off the locus, pass rate +5.0) "
            "invisible to every mean-based test, second-most-negative of 170 "
            "transitions; and split 2026 into a common part (+0.17), a quantified "
            "Basque part (−0.31) and −1.33 that no published data can yet attribute"),
    ("15. Four objections from the coordinator (20 Sep)",
     "Why the Spanish field? Were the nine exams comparable? Is the marking stricter?",
     STOOD, "the subject panel splits the Basque-specific fall exactly: −1.18 moved all "
            "of Euskadi's quantitative subjects together, −1.10 is Física's own. A "
            "general marking severity is bounded at a fifth of the fall; a severity "
            "confined to the numerical deductions fits and is confounded with the "
            "format change. No cohort rate can be projected: PISA is steps, not a slope"),
    ("16. The statement, item by item (20 Sep)",
     "Where is the reading, and what would a word budget cost the 2027 paper?",
     STOOD, "the length lives in the competency items in BOTH years (2025 A1 423 of "
            "1046; 2026 A1 289 and B1 413 of 1438), and 100 of the 2026 growth is fifty "
            "printed sub-task weights the 2025 paper did not carry. One of the three "
            "competency elements of B1 is a marking rule, not a competence"),
]

fig, (ax, axl) = plt.subplots(2, 1, figsize=(11.6, 19.0),
                              gridspec_kw=dict(height_ratios=[1.0, 2.4], hspace=0.16))

# --- a. how the headline numbers moved as the frame widened ---------------------
stages = ["As published:\nyear-on-year", "This study:\n2026 cross-section",
          "Re-baselined:\nvs 2015–19 norm"]
x = np.arange(len(stages))
nat = [nat_2025, nat_2026, nat_base]
ehu = [ehu_yoy, ehu_yoy, ehu_base]

ax.axhline(0, color=INK2, lw=1.0, zorder=1)
ax.plot(x, nat, color=INK2, lw=2.0, marker="o", ms=7, zorder=3,
        label="The national headline")
ax.plot(x, ehu, color=C["violet"], lw=2.0, marker="o", ms=7, zorder=3,
        label="The Basque headline")
for xi, v in zip(x, nat):
    ax.annotate("%+.2f" % v, (xi, v), textcoords="offset points", xytext=(0, 11),
                ha="center", fontsize=8.5, color=INK2)
for xi, v in zip(x, ehu):
    ax.annotate("%+.2f" % v, (xi, v), textcoords="offset points", xytext=(0, -17),
                ha="center", fontsize=8.5, color=C["violet"])
ax.annotate("the national number changes sign", xy=(0.95, -0.30), fontsize=7.8,
            color=C["red"], ha="center")
ax.set_xticks(x)
ax.set_xticklabels(stages, fontsize=8.2)
ax.set_xlim(-0.35, len(stages) - 0.65)
# Headroom so the value labels clear the title and the tick labels.
ax.set_ylim(-2.35, 0.62)
ax.set_ylabel("Change in the mean Física mark")
ax.set_title("a. The same two headlines, as the reference frame widens")
ax.legend(loc="lower left", fontsize=8)

# --- b. the ladder of claims and what happened to each --------------------------
STEP = 1.62                                   # vertical pitch: room for three-line fates
ypos = np.arange(len(steps))[::-1] * STEP
for y, (title, claim, status, fate) in zip(ypos, steps):
    colr = STATUS_COLOR[status]
    axl.scatter([0.012], [y], s=120, color=colr, zorder=3, clip_on=False)
    axl.annotate(title, xy=(0.045, y + 0.20), fontsize=8.6, color=INK, va="center",
                 fontweight="normal")
    axl.annotate(claim, xy=(0.045, y - 0.08), fontsize=7.8, color=INK2, va="center")
    fate_txt = textwrap.fill("→ " + fate, width=125, subsequent_indent="   ")
    axl.annotate(fate_txt, xy=(0.045, y - 0.24), fontsize=7.4, color=colr,
                 va="top", linespacing=1.15)
    if y > 0:
        axl.plot([0.012, 0.012], [y - 0.72, y - 0.92], color=MUTED, lw=1.0, zorder=1)
handles = [plt.Line2D([], [], marker="o", ls="", ms=8, color=STATUS_COLOR[s], label=lab)
           for s, lab in [(OVER, "overturned by a later step"),
                          (WEAK, "weakened by a later step"),
                          (STOOD, "stands")]]
axl.legend(handles=handles, loc="upper right", fontsize=7.8)
axl.set_xlim(0, 1)
axl.set_ylim(-0.5, (len(steps) - 1) * STEP + 0.5)
axl.set_yticks([])
axl.set_xticks([])
for side in ("left", "bottom"):
    axl.spines[side].set_visible(False)
axl.grid(False)
axl.set_title("b. The order the questions were asked in, and what each answer did to the one before")

fig.text(0.005, 0.005,
         "The numbers in panel a are read from the JSON written by the scripts that "
         "computed them (results.json, shape_locus.json, reference_frames.json); the step "
         "texts in panel b are written by hand.\nBoth can drift, and both have: step 10's "
         "text drifted from its own data, and this footnote itself claimed it could not.",
         fontsize=7, color=MUTED, linespacing=1.5)
_save(fig, "fig18_analysis_path", P, dpi=200)

json.dump({"headlines": {"national": dict(zip(["year_on_year", "cross_section_2026",
                                               "vs_baseline"], nat)),
                         "euskadi": dict(zip(["year_on_year", "cross_section_2026",
                                              "vs_baseline"], ehu))},
           "steps": [{"step": t, "claim": c, "status": s, "fate": f}
                     for t, c, s, f in steps]},
          open(A / "analysis_path.json", "w", encoding="utf-8"), indent=2,
          ensure_ascii=False)
print("national:", nat, "\neuskadi :", ehu)
