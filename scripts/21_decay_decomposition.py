#!/usr/bin/env python3
"""Decomposition of the Basque Física decay into separable components.

The study's governing question is not "how large was the fall" but "what is it made
of": which parts of it are common to the whole country, which are specific to the
Basque exam, which of those can be quantified from published data, and which cannot be
separated from each other without data that does not yet exist.

Three things are computed here.

1. TYPOLOGY OF THE STEPS.  A change in a grade distribution is either a change of
   LOCATION (everything moves together; the pass rate and the top band move as the
   common mean-to-band locus says they should) or a change of SHAPE (they do not).
   Each Basque transition 2015->2025 is classified by the residual of its band moves
   from the locus fitted on all 187 region-years, and ranked inside the 170-transition
   panel.  This separates the 2024 event (shape) from the 2025 event (location).

2. THE MARK BUDGET.  Each year's Basque change is split into a component common to the
   nine communities that have a 2026 result (the same nine in every year, so the
   comparison population never changes) and a Basque-specific remainder.

3. ATTRIBUTION OF THE BASQUE-SPECIFIC 2026 REMAINDER.  Every component the dossier can
   put a number on is subtracted, with its range and its identification status, and the
   remainder is left explicitly unattributed.  The point of the exercise is the size of
   that remainder: it is what the item-level data would resolve, and it is the argument
   for asking for it.

Nothing here is a causal estimate.  A component is "quantified" when the dossier can
put a defensible magnitude on it under stated assumptions, not when it has been shown
to have caused anything.

Reads : data/ministry_fisica_panel.csv, ministry_fisica_distr.csv,
        data/analysis/regions_2026_vs_2025.csv, data/ehu_selection_premium.csv,
        data/analysis/pau2027_estimator.json, data/analysis/reading_load.json
Writes: data/analysis/decomposition.json, data/tables/decomposition_steps.md,
        data/tables/decomposition_budget.md, data/tables/decomposition_components.md,
        plots/fig25_decomposition.(png|svg)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from plot_style import T, C, INK, INK2, MUTED, apply_style, save as _save
import plot_style as _ps

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
A = DATA / "analysis"
TABLES = DATA / "tables"
PLOTS = ROOT / "plots"

PV = "País Vasco"
SHAPE_CUT = 4.0        # |top excess| + |pass excess|, in percentage points; declared in the table

# ---------------------------------------------------------------- 1. typology
P = pd.read_csv(DATA / "ministry_fisica_panel.csv")
D = pd.read_csv(DATA / "ministry_fisica_distr.csv")
pp = P[(P.sitting == "ordinary") & (P.phase == "specific") & (~P.ccaa.isin(["Estado", "Total"]))]
dd = D[(D.sitting == "ordinary") & (D.phase == "specific")]
m = pp.merge(dd, on=["ccaa", "year", "sitting", "phase"])
m["top"] = m["[8-9)"] + m["[9-10]"]
m["ratio"] = m["top"] / m["pass_pct"]

coef_top = np.polyfit(m["mean"], m["top"], 2)
coef_pass = np.polyfit(m["mean"], m["pass_pct"], 2)
coef_ratio = np.polyfit(m["mean"], m["ratio"], 2)
m["res_ratio"] = m["ratio"] - np.polyval(coef_ratio, m["mean"])
# one scale, used everywhere: the residual measured against the field in the same year,
# divided by the SD of that field-adjusted residual.  (The audit of 20 September found
# two different z-scales in circulation for this quantity.)
m["resf"] = m.res_ratio - m.groupby("year").res_ratio.transform("mean")
SD_RESF = float(m.resf.std(ddof=1))
m["z"] = m.resf / SD_RESF

wide_z = m.pivot(index="ccaa", columns="year", values="z")
steps = []
for ccaa in wide_z.index:
    g = m[m.ccaa == ccaa].set_index("year").sort_index()
    for y in range(2016, 2026):
        if y not in g.index or (y - 1) not in g.index:
            continue
        dmean = g.loc[y, "mean"] - g.loc[y - 1, "mean"]
        dtop = g.loc[y, "top"] - g.loc[y - 1, "top"]
        dtop_pred = np.polyval(coef_top, g.loc[y, "mean"]) - np.polyval(coef_top, g.loc[y - 1, "mean"])
        dpass = g.loc[y, "pass_pct"] - g.loc[y - 1, "pass_pct"]
        dpass_pred = np.polyval(coef_pass, g.loc[y, "mean"]) - np.polyval(coef_pass, g.loc[y - 1, "mean"])
        steps.append(dict(ccaa=ccaa, year=y, d_mean=dmean,
                          d_top=dtop, d_top_locus=dtop_pred, top_excess=dtop - dtop_pred,
                          d_pass=dpass, d_pass_locus=dpass_pred, pass_excess=dpass - dpass_pred,
                          dz=wide_z.loc[ccaa, y] - wide_z.loc[ccaa, y - 1]))
S = pd.DataFrame(steps)
S["shape_move"] = S.top_excess.abs() + S.pass_excess.abs()      # total departure from the locus
S["rank_dz"] = S.dz.rank(method="min").astype(int)
S["rank_shape"] = S.shape_move.rank(ascending=False, method="min").astype(int)
S.to_csv(A / "decomposition_steps.csv", index=False)

pv_steps = S[S.ccaa == PV].set_index("year").sort_index()
n_trans = len(S)

# ---------------------------------------------------------------- 2. mark budget
# The nine communities with a 2026 result, pooled phase, in every year: a fixed
# comparison population.  2026 comes from this study's assembled cross-section.
reg = pd.read_csv(A / "regions_2026_vs_2025.csv")
nine = list(reg.ccaa)
pool = P[(P.sitting == "ordinary") & (P.phase == "pooled") & (~P.ccaa.isin(["Estado", "Total"]))]
wide = pool.pivot(index="ccaa", columns="year", values="mean")
field = wide.loc[nine].mean()                                   # 2015-2025
field[2026] = reg.mean_2026.mean()
pv = wide.loc[PV].copy()
pv[2026] = float(reg.loc[reg.ccaa == PV, "mean_2026"].iloc[0])

budget = []
for y in range(2016, 2027):
    common = field[y] - field[y - 1]
    total = pv[y] - pv[y - 1]
    budget.append(dict(year=y, pv=pv[y], field=field[y], total=total,
                       common=common, basque_specific=total - common))
B = pd.DataFrame(budget)
B.to_csv(A / "decomposition_budget.csv", index=False)

norm_pv = float(pv.loc[2015:2019].mean())
norm_field = float(field.loc[2015:2019].mean())
vs_norm_pv = float(pv[2026] - norm_pv)
vs_norm_field = float(field[2026] - norm_field)
basque_2026 = float(B.loc[B.year == 2026, "basque_specific"].iloc[0])
basque_2025 = float(B.loc[B.year == 2025, "basque_specific"].iloc[0])
common_2025 = float(B.loc[B.year == 2025, "common"].iloc[0])

# ---------------------------------------------------------------- 3. attribution
prem = pd.read_csv(DATA / "ehu_selection_premium.csv")
p25 = prem[prem.format.str.startswith("2025")].set_index("item_sd").premium_vs_no_choice
p26 = prem[prem.format.str.startswith("2026")].set_index("item_sd").premium_vs_no_choice
choice = {sd: float(p26[sd] - p25[sd]) for sd in sorted(p25.index)}
choice_gross = choice[0.2]
# Same correction on this side. Euskadi cut optionality by 25 points; the other eight
# communities cut it by 6.25 on average, and whatever that cost them is already inside
# the common component. Only the excess cut belongs against the residual. The other
# formats are not simulated, so this is a linear approximation and the gross figure is
# kept as the other end of the range.
chg_opt = pd.read_csv(DATA / "exam_change_vs_grade.csv")
pv_cut = -float(chg_opt.loc[chg_opt.ccaa == PV, "d_opt"].iloc[0])
field_cut = -float(chg_opt.loc[chg_opt.ccaa != PV, "d_opt"].mean())
_net = (pv_cut - field_cut) / pv_cut
choice_net = {sd: v * _net for sd, v in choice.items()}
choice_central = choice_net[0.2]
choice_lo, choice_hi = min(choice_net.values()), max(choice_net.values())

est = json.load(open(A / "pau2027_estimator.json", encoding="utf-8"))
pisa = json.load(open(A / "pisa_link.json", encoding="utf-8"))["science_mean"]
SD_PISA, SD_PAU = 90.0, 2.34
# The target of this attribution is a DIFFERENCE from the field, so the subtracted terms
# have to be differences from the field too. The estimator's cohort term is the Basque
# PISA move on its own; Spain's science also fell over 2022-2025, and that part of the
# decline is already inside the "common" component. The excess is what belongs here.
pv_move = pisa["pais_vasco"]["2025"] - pisa["pais_vasco"]["2022"]
es_move = pisa["espana"]["2025"] - pisa["espana"]["2022"]
excess_move = pv_move - es_move
cohort_per_year_gross = float(est["cohort_term_marks"]) / 2.0     # Basque move alone
cohort_per_year = excess_move / SD_PISA * SD_PAU / 3.0            # excess over Spain, one PAU year
pisa_se_marks = 0.11                                              # +-, from PISA sampling error alone

rl = json.load(open(A / "reading_load.json", encoding="utf-8"))
L = pd.DataFrame(rl["length_table"]).dropna(subset=["len_change", "delta"])
slope, icept, r_len, p_len, se_len = stats.linregress(L.len_change, L.delta)
pv_len = float(L.loc[L.ccaa == PV, "len_change"].iloc[0])
length_implied = float(slope * pv_len)                            # association, NOT an effect

quantified = choice_central + cohort_per_year
remainder = basque_2026 - quantified

COMPONENTS = [
    dict(component="Common to the country",
         value=float(B.loc[B.year == 2026, "common"].iloc[0]),
         lo=None, hi=None, status="observed",
         basis="the same nine communities, 2025 to 2026",
         identifies="already separated: it is the field's own move"),
    dict(component="Choice removed from the paper",
         value=choice_central, lo=choice_lo, hi=choice_hi, status="quantified (modelled)",
         basis=f"selection-premium simulation of the two Basque formats ({choice_gross:+.2f} gross), "
               f"net of the {field_cut:.1f}-point average cut in the other eight communities",
         identifies="option-level marks: the realised premium is observable directly"),
    dict(component="Cohort (PISA-implied)",
         value=cohort_per_year, lo=cohort_per_year - pisa_se_marks, hi=cohort_per_year + pisa_se_marks,
         status="quantified (modelled)",
         basis=f"PISA 2022-2025 science, Basque decline in excess of Spain's "
               f"({excess_move:+.1f} of {pv_move:+.1f} points), one PAU year, transferred one-for-one in SD",
         identifies="nothing further inside the PAU; it is an outside measurement"),
    dict(component="Paper content and reading load",
         value=None, lo=None, hi=None, status="not identified (collinear)",
         basis=f"cross-community association r = {r_len:.3f}; taken literally it would "
               f"attribute {abs(slope * pv_len):.2f} marks, more than the whole Basque-specific fall",
         identifies="sub-task marks: where in the paper the marks were lost"),
    dict(component="Marking severity (penalty list, voided sections)",
         value=None, lo=None, hi=None, status="not identified",
         basis="rules documented; their cost in marks is not published",
         identifies="sub-task marks and the penalty ledger"),
    dict(component="Tribunal severity and spread",
         value=None, lo=None, hi=None, status="not identified",
         basis="EHU computed the table for Física and did not publish it",
         identifies="Física by tribunal: n, mean, SD, school composition"),
    dict(component="Syllabus exposure (newly examined topics)",
         value=None, lo=None, hi=None, status="not identified (bounded)",
         basis="in June 2026 the new topics sat in optional slots; in July two were obligatory",
         identifies="option take-up rates and per-option means"),
    dict(component="Who sat the exam",
         value=None, lo=None, hi=None, status="not identified (bounded small)",
         basis="presented fell 5.6 %; enrolment unpublished; the same cohort held Química and Biología",
         identifies="enrolment and the school marks of the 2025-26 cohort"),
]
comp_df = pd.DataFrame(COMPONENTS)
comp_df.to_csv(A / "decomposition_components.csv", index=False)

out = dict(
    scale=dict(sd_field_adjusted_conditional_residual=SD_RESF,
               note="one z-scale for the conditional top-band residual, used throughout"),
    typology=dict(
        n_transitions=int(n_trans),
        pais_vasco=pv_steps[["d_mean", "d_top", "d_top_locus", "top_excess",
                             "d_pass", "d_pass_locus", "pass_excess", "dz",
                             "rank_dz", "rank_shape"]].round(4).to_dict("index"),
        most_negative_dz=S.nsmallest(5, "dz")[["ccaa", "year", "dz"]].round(3).to_dict("records"),
        largest_shape_moves=S.nlargest(5, "shape_move")[["ccaa", "year", "shape_move", "d_mean"]].round(3).to_dict("records"),
    ),
    budget=dict(
        rows=B.round(4).to_dict("records"),
        pre_covid_norm_pais_vasco=norm_pv, pre_covid_norm_nine=norm_field,
        pais_vasco_2026_vs_norm=vs_norm_pv, nine_2026_vs_norm=vs_norm_field,
        basque_specific_2026=basque_2026, basque_specific_2025=basque_2025,
        common_2025=common_2025,
    ),
    attribution=dict(
        target=basque_2026,
        choice=dict(central=choice_central, gross=choice_gross, by_item_sd=choice, by_item_sd_net=choice_net,
                    lo=choice_lo, hi=choice_hi, pv_cut_pp=pv_cut, field_cut_pp=field_cut),
        cohort=dict(central=cohort_per_year, gross=cohort_per_year_gross,
                    se_marks=pisa_se_marks, pisa_move_pv=pv_move, pisa_move_es=es_move,
                    pisa_move_excess=excess_move),
        length_association=dict(slope_per_pct=float(slope), r=float(r_len), p=float(p_len),
                                pais_vasco_len_change_pct=pv_len, implied_marks=length_implied),
        quantified_total=quantified, unattributed=remainder,
        unattributed_share=remainder / basque_2026,
    ),
)
(A / "decomposition.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------- tables
def md(rows, headers, fmts):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(f.format(v) if v is not None else "—" for f, v in zip(fmts, r)) + " |")
    return "\n".join(out) + "\n"


rows = []
for y, r in pv_steps.iterrows():
    kind = "shape" if abs(r.top_excess) + abs(r.pass_excess) > SHAPE_CUT else "location"
    rows.append((y, r.d_mean, r.d_top, r.d_top_locus, r.top_excess, r.d_pass, r.d_pass_locus,
                 r.pass_excess, kind))
(TABLES / "decomposition_steps.md").write_text(md(
    rows, ["Year", "Δ mean", "Δ top band", "locus", "excess", "Δ pass %", "locus", "excess", "Reads as"],
    ["{}", "{:+.2f}", "{:+.2f}", "{:+.2f}", "{:+.2f}", "{:+.2f}", "{:+.2f}", "{:+.2f}", "{}"]), encoding="utf-8")

(TABLES / "decomposition_budget.md").write_text(md(
    [(int(r.year), r.pv, r.total, r.common, r.basque_specific) for r in B.itertuples()],
    ["Year", "Euskadi mean", "Δ total", "Common to the nine", "Basque-specific"],
    ["{}", "{:.2f}", "{:+.2f}", "{:+.2f}", "{:+.2f}"]), encoding="utf-8")

(TABLES / "decomposition_components.md").write_text(md(
    [(c["component"],
      ("{:+.2f}".format(c["value"]) if c["value"] is not None else "not quantified"),
      ("{:+.2f} to {:+.2f}".format(c["lo"], c["hi"]) if c["lo"] is not None else "—"),
      c["status"], c["identifies"]) for c in COMPONENTS],
    ["Component", "Marks", "Range", "Status", "What would identify it"],
    ["{}", "{}", "{}", "{}", "{}"]), encoding="utf-8")

# ---------------------------------------------------------------- figure
# In paper mode the three panels become two figures: (a, b) are the locus argument
# and (c) is the attribution budget, and they are cited pages apart. The panel code
# below is untouched and draws into whichever axes it is handed.
if _ps.PAPER:
    fig = plt.figure(figsize=(_ps.PAGE_W, _ps.PAGE_W * 0.52))
    gsA = fig.add_gridspec(1, 2, wspace=0.30)
    ax1 = fig.add_subplot(gsA[0, 0])
    ax2 = fig.add_subplot(gsA[0, 1])
    fig._pau_scale = (_ps.PAGE_W / 2.0) / (11.4 / 2.0)
    fig_c = plt.figure(figsize=(_ps.PAGE_W, _ps.PAGE_W * 0.56))
    fig_c._pau_scale = _ps.PAGE_W / 11.4
    ax3 = fig_c.add_subplot(111)
else:
    fig = plt.figure(figsize=(11.4, 9.2))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.82], hspace=0.38, wspace=0.26)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

# --- a. location against shape, every transition in the panel
other = S[S.ccaa != PV]
ax1.axvline(0, color=MUTED, lw=0.9, zorder=1)
# The vertical is merely "no change in the mean". The HORIZONTAL is the locus itself —
# y is already the residual from it — and it is what panel b is about, so it is drawn
# and labelled differently. Before this revision both lines were identical grey and the
# subject of the panel was unmarked.
ax1.axhline(0, color=INK2, lw=1.2, ls=(0, (6, 3)), zorder=1)
ax1.scatter(other.d_mean, other.top_excess, s=14, color=MUTED, alpha=0.55,
            label=T("the other {n} communities, {k} transitions").format(n=other.ccaa.nunique(), k=len(other)), zorder=2)
ax1.scatter(pv_steps.d_mean, pv_steps.top_excess, s=42, color=C["violet"], zorder=4,
            label=T("Euskadi, 2016–2025"))
for y in (2024, 2025):
    r = pv_steps.loc[y]
    ax1.scatter([r.d_mean], [r.top_excess], s=120, facecolor="none",
                edgecolor=C["red"], lw=1.8, zorder=5)
# Both callouts now carry a leader, because 2025 sits in the crowded middle and its
# label previously landed beside a different Basque point.
_cal = {2024: (26, -4), 2025: (6, 36)}
for y, off in _cal.items():
    r = pv_steps.loc[y]
    ax1.annotate(f"{y}", (r.d_mean, r.top_excess), textcoords="offset points",
                 xytext=off, fontsize=9.5, color=C["red"], zorder=6,
                 ha="left" if off[0] > 0 else "right", va="center",
                 arrowprops=dict(arrowstyle="-", lw=0.8, color=C["red"],
                                 shrinkA=1, shrinkB=9))
ax1.set_xlabel(T("Change of level: Δ mean mark"))
ax1.set_ylabel(T("Change of shape: Δ top band minus what\nthe level alone predicts (pp)"))
ax1.set_title(T("a. Two different kinds of year"), loc="left")
# Room is made below the data so the legend occludes nothing; it previously sat on
# top of the scatter with a grey point printed through the word "Euskadi".
_lo, _hi = ax1.get_ylim()
ax1.set_ylim(_lo - 0.34 * (_hi - _lo), _hi)
ax1.annotate(T("the locus"), (ax1.get_xlim()[1], 0), textcoords="offset points",
             xytext=(-4, 5), ha="right", va="bottom", fontsize=8.2, color=INK2)
ax1.legend(loc="lower left", fontsize=7.6, framealpha=0.0, borderpad=0.2)

# --- b. the same two years as bars: observed against locus
lbl = [T("top band\n2023→2024"), T("pass rate\n2023→2024"), T("top band\n2024→2025"), T("pass rate\n2024→2025")]
obs = [pv_steps.loc[2024, "d_top"], pv_steps.loc[2024, "d_pass"],
       pv_steps.loc[2025, "d_top"], pv_steps.loc[2025, "d_pass"]]
pred = [pv_steps.loc[2024, "d_top_locus"], pv_steps.loc[2024, "d_pass_locus"],
        pv_steps.loc[2025, "d_top_locus"], pv_steps.loc[2025, "d_pass_locus"]]
x = np.arange(4)
ax2.axhline(0, color=MUTED, lw=0.9)
ax2.bar(x - 0.19, obs, width=0.36, color=C["violet"], label=T("observed"))
ax2.bar(x + 0.19, pred, width=0.36, color=MUTED, alpha=0.6, label=T("what the level alone predicts"))
for xi, (o, p_) in enumerate(zip(obs, pred)):
    exc = o - p_
    y = max(o, p_, 0) + 0.7
    ax2.annotate(f"{exc:+.1f}", (xi, y), ha="center", fontsize=8.6,
                 color=C["red"] if abs(exc) > 2 else INK2)
ax2.set_xticks(x)
ax2.set_xticklabels(lbl, fontsize=8)
ax2.set_ylim(-12.5, 5.2)
ax2.set_ylabel(T("Change, percentage points"))
ax2.set_title(T("b. 2024 moved off the locus; 2025 moved along it"), loc="left")
ax2.legend(loc="lower left", fontsize=8, framealpha=0.92)

# --- c. the mark budget and what is left unattributed (floating waterfall)
labels = [T("Euskadi 2025"), T("Common to\nthe nine"), T("Choice\nremoved"),
          T("Cohort\n(PISA)"), T("Not yet\nidentified"), T("Euskadi 2026")]
deltas = [float(B.loc[B.year == 2026, "common"].iloc[0]), choice_central, cohort_per_year, remainder]
colors = [C["aqua"], C["blue"], C["yellow"], C["red"]]
start = float(pv[2025]); end = float(pv[2026])
lo = min(end, start + sum(deltas)) - 0.55
hi = max(start, start + deltas[0]) + 0.55

# The two endpoints used to be drawn as columns rising from the bottom of the
# axes. The axes do not start at zero — they start at 3.44, chosen to frame the
# steps — so those columns had heights of 2.03 and 0.55 for levels of 5.47 and
# 3.99: a ratio of 3.7:1 for a real ratio of 1.37:1, overstating the difference
# by a factor of 2.7. A bar's height reads as a magnitude, and on a truncated
# axis that magnitude is an artefact of where the axis was cut. The endpoints
# are now level *caps*: a mark at the value, carrying no height at all. The
# dotted rules already carry the eye across to them.
ax3.axhline(start, color=MUTED, lw=0.9, ls=":")
ax3.axhline(end, color=MUTED, lw=0.9, ls=":")


def _level_cap(x, y):
    ax3.plot([x - 0.28, x + 0.28], [y, y], color=INK2, lw=5.0,
             solid_capstyle="butt", zorder=3)


_level_cap(0, start)
ax3.annotate(f"{start:.2f}", (0, start + 0.10), ha="center", fontsize=10, color=INK)
level = start
for i_, (d, col) in enumerate(zip(deltas, colors), start=1):
    bottom = level + min(d, 0)
    ax3.bar(i_, abs(d), bottom=bottom, color=col, width=0.56)
    ax3.annotate(f"{d:+.2f}", (i_, bottom + abs(d) / 2), ha="center", va="center",
                 fontsize=9.5, color="white" if abs(d) > 0.3 else INK)
    ax3.plot([i_ - 0.28, i_ + 1 - 0.28], [level + d, level + d], color=MUTED, lw=0.8, zorder=1)
    level += d
_level_cap(5, end)
ax3.annotate(f"{end:.2f}", (5, end + 0.10), ha="center", fontsize=10, color=INK)
ax3.set_xticks(range(6))
ax3.set_xticklabels(labels, fontsize=9)
ax3.set_ylabel(T("Mean Física mark"))
ax3.set_ylim(lo, hi)
# Standing alone in the paper and in the coordination deck, this panel is no
# longer "panel c" of anything, so the letter goes. It is removed here, from the
# plain translated string, rather than afterwards from the rendered title:
# plot_style hands set_title a LaTeX-wrapped object, and editing that on the way
# out gets it escaped a second time.
_ttl_c = T("c. What the 2026 fall is made of — and how much of it is still unattributed")
if _ps.PAPER:
    _ttl_c = _ttl_c[3:]
ax3.set_title(_ttl_c, loc="left")
ax3.annotate(T("Basque-specific: {b:+.2f}.  Quantified: {q:.2f}.  Unattributed: {u:.2f} ({pc:.0f} %).")
             .format(b=basque_2026, q=abs(quantified), u=abs(remainder),
                     pc=100 * remainder / basque_2026),
             xy=(0.5, hi - 0.22), fontsize=9, color=C["red"], ha="left")

fig.text(0.005, 0.005,
         T("Ministry EPAU, ordinary sitting. Panels a and b: specific phase, 17 communities, "
           "locus fitted on all 187 region-years. Panel c: pooled phase, the nine communities with a "
           "2026 result in every year.\nThe choice term is a simulation of the two formats at item SD 0.2 "
           "net of the other eight communities' own cuts; the cohort term is the Basque PISA "
           "2022–2025 decline in excess of Spain's, one PAU year of it, transferred one-for-one.\nBoth are "
           "differences from the field, because the quantity they are subtracted from is one. Neither is a causal estimate."),
         fontsize=7, color=MUTED, linespacing=1.5)
if _ps.PAPER:
    # Standing alone, the budget panel is no longer "panel c" of anything, so the
    # letter is dropped; the same applies to the two locus panels, which keep
    # theirs because they are still a pair.
    _save(fig, "fig25_decomposition", PLOTS, dpi=200)          # -> fig04_locus
    _save(fig_c, "fig08_attribution_budget", PLOTS, dpi=200)
else:
    _save(fig, "fig25_decomposition", PLOTS, dpi=200)

print(pv_steps[["d_mean", "top_excess", "pass_excess", "dz", "rank_dz"]].round(2).to_string())
print(f"\nBasque-specific 2026: {basque_2026:+.3f}   2025: {basque_2025:+.3f}   common 2025: {common_2025:+.3f}")
print(f"choice {choice_central:+.3f} ({choice_lo:+.3f}..{choice_hi:+.3f}), cohort {cohort_per_year:+.3f}")
print(f"quantified {quantified:+.3f}, unattributed {remainder:+.3f} "
      f"({100 * remainder / basque_2026:.0f} % of the Basque-specific fall)")
print(f"length association: slope {slope:+.4f}/pp, r {r_len:.3f}, implies {length_implied:+.2f} for PV")
