#!/usr/bin/env python3
"""Subject-level decomposition of the 2026 Basque fall, and the severity hypothesis.

The mark budget in `21_decay_decomposition.py` separates the Basque Física change into
a part common to the nine-community field and a Basque-specific remainder.  That split
uses Física alone, so it cannot tell whether the Basque-specific part is something that
happened to *Física in Euskadi* or something that happened to *Euskadi* — to its
cohort, its tribunals, its marking regime — and landed on Física along with everything
else.

The 2026 subject table separates those two.  Euskadi published eight subjects; four
comparator communities published three of them (Física, Matemáticas II, Química).  That
gives a balanced 5x3 panel, on which the Basque Física change decomposes exactly into
three additive terms:

    d(PV, Física) = field core  +  field Física premium
                  + Euskadi-common deviation  +  Euskadi Física-specific deviation

The first two are what a community with a stable exam and a stable cohort saw.  The
third is everything that moved all of Euskadi's quantitative subjects together — the
cohort, the tribunals, the marking regime.  The fourth is what is left for Física's own
paper.  The identity is exact by construction; no fitting is involved.

THE SEVERITY HYPOTHESIS.  2026 was the second year in which the linguistic component
(0.2 pt for grammar, spelling and presentation) and the seven minor-error deductions
(-0.10 each: units, vector notation, intermediate rounding, SI prefixes, factor of ten,
transcription) were in force, and the first in which correctors had a full year's
experience of applying them.  A severity effect has a testable signature, and it is a
different signature depending on which rule is doing the work:

  * a GENERAL severity effect (spelling, presentation, "apply the criteria in full")
    reaches every subject that asks for written text, so it should move Lengua
    Castellana, Euskara II, Historia and Filosofía with Física;
  * a QUANTITATIVE-SPECIFIC severity effect (the seven minor-error types are written for
    numerical work) reaches Física, Química and Matemáticas II and no one else.

Those predictions are separable in the eight-subject table, and this script separates
them.  What comes out is a bound, not a measurement: the subject means say how much of
the Física fall *could* be general severity, not how much *was*.

Reads : data/analysis/subjects_2025_2026_by_region.csv, data/analysis/decomposition.json
Writes: data/analysis/subject_decomposition.json,
        data/analysis/subject_decomposition_panel.csv,
        data/tables/subject_decomposition.md, data/tables/severity_signature.md,
        plots/fig26_subject_decomposition.(png|svg)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from plot_style import C, GRID as GRIDLINE, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "data" / "analysis"
TABLES = ROOT / "data" / "tables"
PLOTS = ROOT / "plots"

PV = "País Vasco"
CORE = ["Física", "Matemáticas II", "Química"]      # the three every community published

# Subject families for the severity signature.  "Quantitative" is not a judgement about
# difficulty: it is the set of subjects to which the seven minor-error deductions of the
# marking specification (units, vector notation, rounding, SI prefixes, factor of ten,
# data transcription) can apply at all.  The rest still carry the 0.2 linguistic
# component, so a general severity effect reaches them and a numerical one does not.
QUANT = {"Física", "Matemáticas II", "Química"}


def two_way_split(df: pd.DataFrame) -> dict:
    """Exact additive split of the Basque Física change on the balanced 5x3 panel."""
    w = df.pivot(index="region", columns="subject", values="delta")[CORE]
    field = w.drop(index=PV)

    field_core = float(field.mean(axis=1).mean())          # field's mean over 3 subjects
    field_fis = float((field["Física"] - field.mean(axis=1)).mean())   # its Física premium
    pv_core = float(w.loc[PV].mean())
    pv_fis = float(w.loc[PV, "Física"] - pv_core)

    common = pv_core - field_core                          # Euskadi-common deviation
    specific = pv_fis - field_fis                          # Física-specific deviation
    total = float(w.loc[PV, "Física"])
    assert abs((field_core + field_fis + common + specific) - total) < 1e-9

    # Cross-check with the symmetric two-way ANOVA (region + subject effects estimated
    # on all five communities).  It apportions the same total differently because the
    # subject effect then includes Euskadi; reporting both keeps the choice visible.
    g = float(w.values.mean())
    reg = w.mean(axis=1) - g
    sub = w.mean(axis=0) - g
    anova_resid = float(w.loc[PV, "Física"] - (g + reg[PV] + sub["Física"]))

    return dict(
        total=total,
        field_core=field_core,
        field_fisica_premium=field_fis,
        euskadi_common=common,
        fisica_specific=specific,
        pv_core_mean=pv_core,
        pv_fisica_minus_own_core=pv_fis,
        anova_grand_mean=g,
        anova_region_effect_pv=float(reg[PV]),
        anova_subject_effect_fisica=float(sub["Física"]),
        anova_residual_pv_fisica=anova_resid,
        field_regions=[r for r in w.index if r != PV],
        per_region_core={r: float(field.loc[r].mean()) for r in field.index},
        per_region_fisica_premium={
            r: float(field.loc[r, "Física"] - field.loc[r].mean()) for r in field.index
        },
    )


def severity_signature(df: pd.DataFrame) -> dict:
    """What the eight Basque subjects say about a general vs a numerical severity shift."""
    pv = df[df.region == PV].set_index("subject")["delta"]
    quant = pv[[s for s in pv.index if s in QUANT]]
    verbal = pv[[s for s in pv.index if s not in QUANT]]

    # A general severity effect is common to both families, so it is bounded above (in
    # magnitude) by the verbal mean: anything beyond that has to come from somewhere the
    # verbal subjects did not share.  This is a bound, not an estimate — part of the
    # verbal fall is itself cohort or paper.
    bound_general = float(verbal.mean())
    gap = float(quant.mean() - verbal.mean())

    return dict(
        all_subjects_mean=float(pv.mean()),
        quantitative=dict(subjects=list(quant.index), mean=float(quant.mean()),
                          values={k: float(v) for k, v in quant.items()}),
        verbal=dict(subjects=list(verbal.index), mean=float(verbal.mean()),
                    values={k: float(v) for k, v in verbal.items()}),
        quant_minus_verbal=gap,
        general_severity_upper_bound_marks=bound_general,
        general_severity_share_of_fisica=abs(bound_general) / abs(float(pv["Física"])),
        n_subjects_up=int((pv > 0).sum()),
        range_marks=float(pv.max() - pv.min()),
        # The two subjects that carry the linguistic component most directly.
        lengua_castellana=float(pv["Lengua Castellana"]),
        euskara=float(pv["Euskara II"]),
    )


def main() -> None:
    df = pd.read_csv(A / "subjects_2025_2026_by_region.csv")
    dec = json.loads((A / "decomposition.json").read_text(encoding="utf-8"))

    core = df[df.subject.isin(CORE)].copy()
    assert len(core) == 15, f"expected a balanced 5x3 panel, got {len(core)} cells"

    split = two_way_split(core)
    sev = severity_signature(df)

    # The 2025 budget is the other half of the second-year argument: if the marking
    # regime had bitten in its first year, 2025 should already carry a Basque-specific
    # negative.  It does not — 2025 is common almost in full.
    budget = {r["year"]: r for r in dec["budget"]["rows"]}
    timing = dict(
        basque_specific_2025=budget[2025]["basque_specific"],
        common_2025=budget[2025]["common"],
        basque_specific_2026=budget[2026]["basque_specific"],
        common_2026=budget[2026]["common"],
    )

    out = dict(
        note=("Exact additive split of the 2026 Basque Física change on the balanced "
              "5x3 subject panel, plus the severity signature in the eight Basque "
              "subjects.  No causal claim is made by either."),
        split=split,
        severity=sev,
        timing=timing,
        # How much of the Basque-specific remainder of the mark budget is *not* specific
        # to Física: the Euskadi-common deviation, expressed against that remainder.
        basque_specific_remainder=dec["budget"]["basque_specific_2026"],
        euskadi_common_share_of_remainder=(
            split["euskadi_common"] / dec["budget"]["basque_specific_2026"]),
    )
    (A / "subject_decomposition.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- panel CSV -------------------------------------------------------------
    w = core.pivot(index="region", columns="subject", values="delta")[CORE]
    panel = w.copy()
    panel["core_mean"] = w.mean(axis=1)
    panel["fisica_minus_core"] = w["Física"] - w.mean(axis=1)
    panel.round(4).to_csv(A / "subject_decomposition_panel.csv")

    # ---- tables ----------------------------------------------------------------
    lines = ["| Community | Física | Matemáticas II | Química | Mean of the three | "
             "Física − own mean |", "|---|---:|---:|---:|---:|---:|"]
    for r in ["País Vasco", "Cataluña", "Madrid", "Andalucía", "Asturias"]:
        if r not in panel.index:
            continue
        row = panel.loc[r]
        lines.append(f"| {r} | {row['Física']:+.2f} | {row['Matemáticas II']:+.2f} | "
                     f"{row['Química']:+.2f} | {row['core_mean']:+.2f} | "
                     f"{row['fisica_minus_core']:+.2f} |")
    f = panel.drop(index=PV)
    lines.append(f"| **Field (four communities)** | {f['Física'].mean():+.2f} | "
                 f"{f['Matemáticas II'].mean():+.2f} | {f['Química'].mean():+.2f} | "
                 f"{f['core_mean'].mean():+.2f} | {f['fisica_minus_core'].mean():+.2f} |")
    lines += ["", "Change in the subject mean, 2025 to 2026, in marks out of ten. The "
              "last two columns are the terms of the additive split: a community's mean "
              "over the three subjects, and how far its Física sits from that mean."]
    (TABLES / "subject_decomposition.md").write_text("\n".join(lines) + "\n",
                                                     encoding="utf-8")

    pv = df[df.region == PV].set_index("subject")["delta"]
    order = ["Física", "Matemáticas II", "Química", "Historia de España", "Euskara II",
             "Hª Filosofía", "Biología", "Lengua Castellana"]
    s = ["| Basque subject | Change 2025→2026 | Family | Reached by the 0.2 linguistic "
         "component | Reached by the seven minor-error rules |", "|---|---:|---|:-:|:-:|"]
    for sub in order:
        fam = "quantitative" if sub in QUANT else "verbal / other"
        s.append(f"| {sub} | {pv[sub]:+.2f} | {fam} | yes | "
                 f"{'yes' if sub in QUANT else 'no'} |")
    s += [f"| **Quantitative mean** | **{sev['quantitative']['mean']:+.2f}** | | | |",
          f"| **Verbal mean** | **{sev['verbal']['mean']:+.2f}** | | | |",
          f"| **Gap** | **{sev['quant_minus_verbal']:+.2f}** | | | |", "",
          "Both families are examined in the same sitting at the same university, under "
          "the same marking specification and in the same second year of it — but by "
          "each subject's own correctors and on each subject's own candidates, so this "
          "is not a within-person comparison. A marking change written into the shared "
          "specification and applied across the board would move both columns together; "
          "the gap is what such a change cannot produce."]
    (TABLES / "severity_signature.md").write_text("\n".join(s) + "\n", encoding="utf-8")

    # ---- figure ----------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.5))

    # (a) the eight Basque subjects, families coloured
    ax = axes[0]
    vals = pv[order]
    cols = [C["orange"] if s_ in QUANT else C["blue"] for s_ in order]
    y = np.arange(len(order))[::-1]
    ax.barh(y, vals.values, color=cols, height=0.66)
    ax.set_yticks(y)
    ax.set_yticklabels([s_.replace("Matemáticas II", "Matemáticas II")
                        for s_ in order], fontsize=8.5)
    for yy, v in zip(y, vals.values):
        ax.text(v + (0.06 if v >= 0 else -0.06), yy, f"{v:+.2f}", va="center",
                ha="left" if v >= 0 else "right", fontsize=8, color=INK2)
    ax.axvline(0, color=INK, lw=0.9)
    ax.axvline(sev["quantitative"]["mean"], color=C["orange"], lw=1.0, ls="--")
    ax.axvline(sev["verbal"]["mean"], color=C["blue"], lw=1.0, ls="--")
    ax.set_xlim(-2.0, 0.65)
    ax.set_xlabel("change in the subject mean, 2025 → 2026 (marks)")
    ax.set_title("(a) One tribunal, eight subjects\nquantitative (orange) vs the rest "
                 "(blue)", loc="left")
    ax.grid(axis="y", visible=False)

    # (b) the 5x3 panel: Física against the community's own core mean
    ax = axes[1]
    for r in panel.index:
        c = C["red"] if r == PV else MUTED
        ax.scatter(panel.loc[r, "core_mean"], panel.loc[r, "Física"], s=54,
                   color=c, zorder=3)
        # Asturias and Madrid sit almost on top of each other (core means 0.50 and
        # 0.43, Física +1.13 and +1.10), so their labels are placed by hand.
        off = {"Asturias": (-9, 6), "Madrid": (9, -9)}.get(r, (9, -3))
        ax.annotate(r, (panel.loc[r, "core_mean"], panel.loc[r, "Física"]),
                    textcoords="offset points", xytext=off,
                    ha="right" if off[0] < 0 else "left",
                    fontsize=8, color=INK if r == PV else INK2)
    lim = [-1.35, 0.85]
    ax.plot(lim, lim, color=GRIDLINE, lw=1.0, ls=":", zorder=1)
    ax.text(0.30, 0.34, "Física = own mean", fontsize=8, color=MUTED, rotation=38)
    ax.set_xlim(*lim); ax.set_ylim(-1.75, 1.35)
    ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
    ax.set_xlabel("community's mean change over the three shared subjects (marks)")
    ax.set_ylabel("change in Física (marks)")
    ax.set_title("(b) Euskadi is low on both axes\nthe fall is not only Física's",
                 loc="left")

    # (c) the exact four-term split
    ax = axes[2]
    terms = [("Field core\n(3 subjects)", split["field_core"], MUTED),
             ("Field Física\npremium", split["field_fisica_premium"], C["aqua"]),
             ("Euskadi-common\ndeviation", split["euskadi_common"], C["violet"]),
             ("Física-specific\ndeviation", split["fisica_specific"], C["red"])]
    x = np.arange(4)
    ax.bar(x, [t[1] for t in terms], color=[t[2] for t in terms], width=0.62)
    for xx, (_, v, _) in zip(x, terms):
        ax.text(xx, v + (0.05 if v >= 0 else -0.05), f"{v:+.2f}", ha="center",
                va="bottom" if v >= 0 else "top", fontsize=9, color=INK)
    ax.set_xticks(x); ax.set_xticklabels([t[0] for t in terms], fontsize=8)
    ax.axhline(0, color=INK, lw=0.9)
    ax.set_ylim(-1.45, 1.05)
    ax.set_ylabel("marks")
    ax.set_title(f"(c) The four terms sum to {split['total']:+.2f}\n"
                 "exact identity, no fitting", loc="left")
    ax.grid(axis="x", visible=False)

    fig.suptitle("Figure 26 — Is the 2026 fall Física's, or Euskadi's?", x=0.005,
                 ha="left", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _save(fig, "fig26_subject_decomposition", PLOTS)

    print(f"total {split['total']:+.3f} = field core {split['field_core']:+.3f} "
          f"+ field Física premium {split['field_fisica_premium']:+.3f} "
          f"+ Euskadi-common {split['euskadi_common']:+.3f} "
          f"+ Física-specific {split['fisica_specific']:+.3f}")
    print(f"quantitative {sev['quantitative']['mean']:+.3f} vs verbal "
          f"{sev['verbal']['mean']:+.3f}; gap {sev['quant_minus_verbal']:+.3f}")
    print(f"ANOVA cross-check: residual for PV/Física "
          f"{split['anova_residual_pv_fisica']:+.3f}")


if __name__ == "__main__":
    main()
