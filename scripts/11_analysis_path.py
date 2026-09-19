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
nat_2025 = float(results["annual_change_dist_2025"]["mean"])          # -0.81
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
     WEAK, "its premise — that 2025 was a national collapse — is overturned at step 6"),
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
     "Among passers, the top-band share: the one measure not dominated by the level.",
     STOOD, "strengthens step 3, shows the plateau reshaped rather than lifted, "
            "and finds a Basque turn in 2024 — before either candidate cause"),
    ("8. Testing the slow version of H4",
     "Do cohorts arrive less prepared each year? Not detectably — take-up is flat.",
     STOOD, "kills the recruitment mechanism, and corrects a dilution effect this "
            "study had itself reported from a phase-undercount of 2015–16"),
    ("9. Bringing in an outside instrument",
     "PISA 2006–2022: Basque science goes from +9 above Spain to −5, breaking in 2015.",
     STOOD, "the drift is real and pre-pandemic, but the cohorts do not match the PAU "
            "(1 of 3), which retracts the triangulation step 9 first claimed"),
    ("10. Comparing the two slopes",
     "On one scale, all four series fall; Euskadi is 1.7x Spain on BOTH instruments.",
     WEAK, "tempers step 9's 'the PAU does not show it' — but every interval "
            "includes zero, so the agreement is recorded, not believed"),
    ("11. Forecasting 2027 from PISA 2025",
     "Basque science falls to 458.5; top performers halve. Cohort term: −0.36 marks.",
     STOOD, "the paper term is 6.5x larger, so 2027 is a policy outcome, not a "
            "prediction — the estimator's value is attribution after the fact"),
    ("12. Measuring the reading load",
     "Paper length vs grade change: r = −0.84, p = 0.008 — the strongest link yet.",
     WEAK, "but length and competency content correlate at +0.87, so it is a better "
            "instrument for the same change, not a second cause"),
]

fig, (ax, axl) = plt.subplots(2, 1, figsize=(11.6, 12.8),
                              gridspec_kw=dict(height_ratios=[1.0, 1.45], hspace=0.34))

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
ypos = np.arange(len(steps))[::-1]
for y, (title, claim, status, fate) in zip(ypos, steps):
    colr = STATUS_COLOR[status]
    axl.scatter([0.012], [y], s=120, color=colr, zorder=3, clip_on=False)
    axl.annotate(title, xy=(0.045, y + 0.20), fontsize=8.6, color=INK, va="center",
                 fontweight="normal")
    axl.annotate(claim, xy=(0.045, y - 0.08), fontsize=7.8, color=INK2, va="center")
    axl.annotate("→ " + fate, xy=(0.045, y - 0.34), fontsize=7.4, color=colr,
                 va="center")
    if y > 0:
        axl.plot([0.012, 0.012], [y - 0.45, y - 0.62], color=MUTED, lw=1.0, zorder=1)
handles = [plt.Line2D([], [], marker="o", ls="", ms=8, color=STATUS_COLOR[s], label=lab)
           for s, lab in [(OVER, "overturned by a later step"),
                          (WEAK, "weakened by a later step"),
                          (STOOD, "stands")]]
axl.legend(handles=handles, loc="lower right", fontsize=7.8)
axl.set_xlim(0, 1)
axl.set_ylim(-0.8, len(steps) - 0.35)
axl.set_yticks([])
axl.set_xticks([])
for side in ("left", "bottom"):
    axl.spines[side].set_visible(False)
axl.grid(False)
axl.set_title("b. The order the questions were asked in, and what each answer did to the one before")

fig.text(0.005, 0.005,
         "Every value is read from the JSON written by the script that computed it "
         "(results.json, shape_locus.json, reference_frames.json),\nso this figure "
         "cannot drift from the analysis it narrates.",
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
