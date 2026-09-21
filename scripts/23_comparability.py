#!/usr/bin/env python3
"""Were the nine 2026 papers the same kind of exam?  A compliance and reform-intensity audit.

The mark budget of `21_decay_decomposition.py` measures the Basque change against a
nine-community field.  That is only a control if the nine sat comparable exams.  They
did not, and this script says by how much.

Three structural criteria are applied to each paper.  They are the criteria as the EHU
coordination applies them, taken from the orientation document that governs the Basque
paper:

  C1  optionality between 50 % and 85 % of the paper's marks;
  C2  at least 70 % of the marks from open or semi-constructed response;
  C3  at least one obligatory item carrying a substantive real-world context.

A fourth measure, not a pass/fail criterion, is the one that discriminates: the share of
the paper's expected marks that is COMPETENCY-coded in the blind double-coded scheme
(substantive context AND a demand to explain or to evaluate).

WHAT THIS CAN AND CANNOT ESTABLISH.  It can establish that the nine papers moved in
different directions and by very different amounts in 2026, and it can measure how far
each moved.  It cannot establish that the criteria bind nationally: the text of RD
534/2024 and the Ministry / CRUE orientations are not in the dossier's source registry,
and were not retrievable during the data hunt.  Whether a community was *required* to
do what Euskadi did, or merely invited to, is therefore an open question and is carried
as a data request, not as a finding.  What follows is a comparison of papers, not a
finding of non-compliance by anybody.

Reads : data/exam_change_vs_grade.csv, data/exam_structure_2025_2026.csv,
        data/exam_coding_2025_2026.csv, data/analysis/regions_2026_vs_2025.csv
Writes: data/analysis/comparability.json, data/tables/comparability_criteria.md,
        data/tables/reform_intensity.md, plots/fig27_comparability.(png|svg)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from plot_style import panels3, C, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
A = DATA / "analysis"
TABLES = DATA / "tables"
PLOTS = ROOT / "plots"

PV = "País Vasco"
OPT_LO, OPT_HI = 50.0, 85.0        # C1 band, in per cent of the paper's marks
OPEN_MIN = 70.0                    # C2 threshold


def main() -> None:
    ch = pd.read_csv(DATA / "exam_change_vs_grade.csv").set_index("ccaa")
    st = pd.read_csv(DATA / "exam_structure_2025_2026.csv")
    cod = pd.read_csv(DATA / "exam_coding_2025_2026.csv")

    s26 = st[st.year == 2026].set_index("ccaa")

    # C3: obligatory items carrying a substantive context, counted from the item coding.
    ob = (cod[(cod.year == 2026) & (cod.obligatory == 1) & (cod.contextualised == 1)]
          .groupby("ccaa").agg(oblig_ctx_items=("item", "size"),
                               oblig_ctx_pts=("points", "sum")))

    # C2: on a reading of the eighteen papers, no paper in the nine uses closed-response
    # items — every item in the 146-item coding is open or semi-constructed.  The coding
    # scheme records what an item DEMANDS, not how it is answered, so this is a judgement
    # from the papers and not a coded variable; it is recorded and then set aside as
    # non-discriminating rather than dropped in silence.
    open_share = {c: 100.0 for c in s26.index}

    rows = []
    for c in ch.index:
        opt = float(s26.loc[c, "optionality_pct"])
        oc = ob.loc[c] if c in ob.index else pd.Series({"oblig_ctx_items": 0,
                                                        "oblig_ctx_pts": 0.0})
        rows.append(dict(
            ccaa=c,
            optionality_2026=opt,
            c1_pass=bool(OPT_LO <= opt <= OPT_HI),
            open_share_2026=open_share[c],
            c2_pass=bool(open_share[c] >= OPEN_MIN),
            oblig_ctx_items=int(oc["oblig_ctx_items"]),
            oblig_ctx_pts=float(oc["oblig_ctx_pts"]),
            c3_pass=bool(oc["oblig_ctx_items"] >= 1),
            competency_share_2026=float(s26.loc[c, "exp_share_competency"]),
            oblig_competency_pts_2026=float(s26.loc[c, "oblig_pts_competency"]),
            delta_mean=float(ch.loc[c, "delta"]),
        ))
    crit = pd.DataFrame(rows).set_index("ccaa")
    crit["n_criteria_met"] = crit[["c1_pass", "c2_pass", "c3_pass"]].sum(axis=1)

    # ---- reform intensity ------------------------------------------------------
    # One number per community for "how far the 2026 paper moved toward the
    # competency model": the mean of four standardised movements.  Optionality enters
    # with its sign flipped, because reducing choice is the direction the orientation
    # asks for.  Standardising inside the nine keeps the index unit-free; it is a
    # ranking device, not a scale with meaning of its own.
    mv = pd.DataFrame({
        "less optionality": -ch["d_opt"],
        "more competency marks": ch["d_comp_exp"],
        "more substantive context": ch["d_subst_exp"],
        "more contextualised marks": ch["d_ctx_exp"],
    })
    z = (mv - mv.mean()) / mv.std(ddof=1)
    crit["reform_intensity"] = z.mean(axis=1)
    crit["reform_rank"] = crit["reform_intensity"].rank(ascending=False).astype(int)

    r_ri, p_ri = stats.pearsonr(crit["reform_intensity"], crit["delta_mean"])
    rho_ri, prho_ri = stats.spearmanr(crit["reform_intensity"], crit["delta_mean"])
    sl, ic, _, _, _ = stats.linregress(crit["reform_intensity"], crit["delta_mean"])

    # Leverage.  Euskadi is the extreme point on both axes, so the Pearson coefficient
    # could be one observation wearing a correlation's clothes.  Every community is
    # dropped in turn; the result is reported whatever it says.
    loo = {}
    for c in crit.index:
        xx = crit["reform_intensity"].drop(c)
        yy = crit["delta_mean"].drop(c)
        rr, pp = stats.pearsonr(xx, yy)
        loo[c] = dict(r=float(rr), p=float(pp))

    # The field of the mark budget, restricted to the communities that did NOT reform
    # their paper appreciably (index below zero).  If the field is contaminated by
    # papers that got easier relative to Euskadi's, this is the cleaner comparison —
    # and it moves the Basque-specific remainder, so it is reported, not buried.
    low = crit[crit["reform_intensity"] < 0]
    high = crit[crit["reform_intensity"] >= 0]

    out = dict(
        note=("Comparison of the nine 2026 papers against the three structural criteria "
              "as the EHU coordination applies them, plus a standardised index of how "
              "far each paper moved in 2026.  No finding of non-compliance is made: the "
              "binding text is not in the source registry."),
        criteria=dict(optionality_band=[OPT_LO, OPT_HI], open_response_min=OPEN_MIN,
                      c3="at least one obligatory item with a substantive context"),
        c2_non_discriminating=("on a reading of the papers, all 146 coded items across the "
                               "nine communities are open or semi-constructed and no paper "
                               "uses closed response; the coding scheme records what an item "
                               "demands, not how it is answered, so this is a judgement from "
                               "the papers rather than a coded variable"),
        per_community=json.loads(crit.reset_index().to_json(orient="records")),
        failures_2026=[c for c in crit.index if crit.loc[c, "n_criteria_met"] < 3],
        reform_intensity=dict(
            components=list(mv.columns),
            values={c: float(crit.loc[c, "reform_intensity"]) for c in crit.index},
            pearson_r=float(r_ri), pearson_p=float(p_ri),
            spearman_rho=float(rho_ri), spearman_p=float(prho_ri),
            slope_marks_per_index_sd=float(sl), intercept=float(ic),
            pais_vasco_index=float(crit.loc[PV, "reform_intensity"]),
            pais_vasco_rank=int(crit.loc[PV, "reform_rank"]),
            n=int(len(crit)),
            leave_one_out=loo,
            without_pais_vasco=loo[PV],
        ),
        split_field=dict(
            low_reform=list(low.index),
            high_reform=list(high.index),
            mean_delta_low=float(low["delta_mean"].mean()),
            mean_delta_high=float(high["delta_mean"].mean()),
            mean_delta_low_excl_pv=float(low.drop(index=PV, errors="ignore")["delta_mean"].mean()),
            mean_delta_high_excl_pv=float(high.drop(index=PV, errors="ignore")["delta_mean"].mean()),
        ),
        # What the Basque-specific remainder becomes if the comparison field is the
        # four communities whose paper barely moved, rather than all eight.
        counterfactual_field=None,
    )

    others = crit.drop(index=PV)
    quiet = others[others["reform_intensity"] < 0]
    out["counterfactual_field"] = dict(
        field_all_eight=float(others["delta_mean"].mean()),
        field_quiet_only=float(quiet["delta_mean"].mean()),
        quiet_members=list(quiet.index),
        basque_vs_all_eight=float(crit.loc[PV, "delta_mean"] - others["delta_mean"].mean()),
        basque_vs_quiet=float(crit.loc[PV, "delta_mean"] - quiet["delta_mean"].mean()),
    )

    (A / "comparability.json").write_text(json.dumps(out, indent=2, ensure_ascii=False),
                                          encoding="utf-8")

    # ---- tables ----------------------------------------------------------------
    tick = {True: "yes", False: "**no**"}
    L = ["| Community | Optionality | C1 50–85 % | Open response | C2 ≥70 % | "
         "Obligatory contextualised items | C3 ≥1 | Competency marks | Change in the mean |",
         "|---|---:|:-:|---:|:-:|---:|:-:|---:|---:|"]
    for c in crit.sort_values("reform_intensity", ascending=False).index:
        r = crit.loc[c]
        L.append(f"| {c} | {r.optionality_2026:.0f} % | {tick[r.c1_pass]} | "
                 f"{r.open_share_2026:.0f} % | {tick[r.c2_pass]} | "
                 f"{r.oblig_ctx_items:.0f} ({r.oblig_ctx_pts:.1f} pt) | "
                 f"{tick[r.c3_pass]} | {r.competency_share_2026:.1f} % | "
                 f"{r.delta_mean:+.2f} |")
    L += ["", "The 2026 papers against the three structural criteria. C2 is met by every "
          "paper — on a reading of the eighteen papers, none of the 146 coded items uses a "
          "closed response format — so it separates nobody. \"Competency marks\" is the "
          "share of expected marks from "
          "items that carry a substantive context *and* ask the candidate to explain or "
          "to evaluate; it is not a criterion, and it is where the nine differ most."]
    (TABLES / "comparability_criteria.md").write_text("\n".join(L) + "\n",
                                                      encoding="utf-8")

    L = ["| Community | Optionality | Competency marks | Substantive context | "
         "Contextualised marks | Index | Rank | Change in the mean |",
         "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for c in crit.sort_values("reform_intensity", ascending=False).index:
        L.append(f"| {c} | {ch.loc[c,'d_opt']:+.0f} pp | {ch.loc[c,'d_comp_exp']:+.1f} pp | "
                 f"{ch.loc[c,'d_subst_exp']:+.1f} pp | {ch.loc[c,'d_ctx_exp']:+.1f} pp | "
                 f"{crit.loc[c,'reform_intensity']:+.2f} | {crit.loc[c,'reform_rank']} | "
                 f"{crit.loc[c,'delta_mean']:+.2f} |")
    L += ["", f"Movement of each 2026 paper from its own 2025 paper, in percentage points "
          f"of the paper's marks, and the standardised index built from the four columns "
          f"(optionality enters with its sign reversed). Across the nine communities the "
          f"index correlates with the change in the mean at r = {r_ri:.3f} "
          f"(p = {p_ri:.4f}); the fitted slope is {sl:+.2f} marks per index unit. "
          f"Euskadi is the extreme point on both axes: dropping it leaves "
          f"r = {loo[PV]['r']:.3f} (p = {loo[PV]['p']:.3f}) among the other eight, so "
          f"the coefficient is largely one community making the point. The rank "
          f"correlation over all nine is rho = {rho_ri:.3f} (p = {prho_ri:.3f})."]
    (TABLES / "reform_intensity.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- figure ----------------------------------------------------------------
    fig, axes = panels3(13.4, 4.6)

    # (a) the four movements, stacked as a slope chart of optionality
    ax = axes[0]
    order = crit.sort_values("reform_intensity", ascending=True).index
    y = np.arange(len(order))
    ax.hlines(y, [ch.loc[c, "opt_2025"] for c in order],
              [ch.loc[c, "opt_2026"] for c in order], color=MUTED, lw=1.4, zorder=2)
    ax.scatter([ch.loc[c, "opt_2025"] for c in order], y, s=28, color=MUTED, zorder=3)
    ax.scatter([ch.loc[c, "opt_2026"] for c in order], y,
               s=46, color=[C["red"] if c == PV else C["blue"] for c in order], zorder=4)
    ax.axvspan(OPT_LO, OPT_HI, color=C["aqua"], alpha=0.10, zorder=0)
    ax.text(67.5, -0.72, "criterion band", ha="center", fontsize=8, color=C["aqua"])
    ax.set_yticks(y); ax.set_yticklabels(order, fontsize=8.5)
    ax.set_xlim(40, 108); ax.set_ylim(-1.3, len(order) - 0.4)
    ax.set_xlabel("optionality (per cent of the paper's marks)")
    ax.set_title("(a) 2025 (grey) → 2026\nonly Asturias is outside the band", loc="left")
    ax.grid(axis="y", visible=False)

    # (b) reform intensity against the change in the mean
    ax = axes[1]
    xs = crit["reform_intensity"].values
    ys = crit["delta_mean"].values
    ax.scatter(xs, ys, s=58, color=[C["red"] if c == PV else MUTED for c in crit.index],
               zorder=3)
    gx = np.linspace(xs.min() - 0.2, xs.max() + 0.2, 20)
    ax.plot(gx, ic + sl * gx, color=C["violet"], lw=1.3, zorder=2)
    off = {"País Vasco": (-11, 4), "Cataluña": (10, -3), "Castilla-La Mancha": (10, -3),
           "Comunitat Valenciana": (10, -3), "Extremadura": (-10, 2),
           "Canarias": (10, -3), "Asturias": (-10, 3), "Madrid": (-10, -8),
           "Andalucía": (10, -3)}
    for c in crit.index:
        o = off.get(c, (8, 2))
        ax.annotate(c, (crit.loc[c, "reform_intensity"], crit.loc[c, "delta_mean"]),
                    textcoords="offset points", xytext=o,
                    ha="right" if o[0] < 0 else "left", fontsize=8,
                    color=INK if c == PV else INK2)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xlim(-1.5, 2.9); ax.set_ylim(-1.95, 1.65)
    ax.set_xlabel("reform-intensity index (SD units within the nine)")
    ax.set_ylabel("change in the mean, 2025 → 2026 (marks)")
    ax.set_title(f"(b) The papers that moved, fell\nr = {r_ri:.2f}, p = {p_ri:.3f}, n = 9",
                 loc="left")

    # (c) competency marks, 2025 and 2026
    ax = axes[2]
    y = np.arange(len(order))
    ax.barh(y - 0.19, [ch.loc[c, "comp_exp_2025"] for c in order], height=0.36,
            color=MUTED, label="2025")
    ax.barh(y + 0.19, [ch.loc[c, "comp_exp_2026"] for c in order], height=0.36,
            color=[C["red"] if c == PV else C["blue"] for c in order], label="2026")
    ax.set_yticks(y); ax.set_yticklabels(order, fontsize=8.5)
    ax.set_xlabel("competency-coded share of the marks (per cent)")
    ax.set_xlim(0, 84)
    ax.legend(loc="lower right", fontsize=8)
    ax.set_title("(c) Euskadi 25 → 62.5 per cent\nCataluña moved the other way", loc="left")
    ax.grid(axis="y", visible=False)

    fig.suptitle("Figure 27 — Nine communities, nine different exams", x=0.005,
                 ha="left", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _save(fig, "fig27_comparability", PLOTS)

    print("criteria failures 2026:", out["failures_2026"])
    print(f"reform intensity vs delta: r = {r_ri:.3f}, p = {p_ri:.4f}; "
          f"rho = {rho_ri:.3f}, p = {prho_ri:.4f}; slope {sl:+.3f}")
    print(f"without País Vasco: r = {loo[PV]['r']:.3f}, p = {loo[PV]['p']:.4f}")
    print(f"PV index {crit.loc[PV,'reform_intensity']:+.2f} (rank "
          f"{crit.loc[PV,'reform_rank']} of 9)")
    print(f"field all eight {out['counterfactual_field']['field_all_eight']:+.3f}; "
          f"quiet only {out['counterfactual_field']['field_quiet_only']:+.3f} "
          f"({', '.join(quiet.index)})")
    print(f"Basque vs all eight {out['counterfactual_field']['basque_vs_all_eight']:+.3f}; "
          f"vs quiet {out['counterfactual_field']['basque_vs_quiet']:+.3f}")


if __name__ == "__main__":
    main()
