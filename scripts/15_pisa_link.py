#!/usr/bin/env python3
"""Does an independent instrument see the Basque top tail thin as well?

The conditional top-band measure of figure 16 found the Basque cohort turning in
2024 — from +0.64 SD above the field across 2016–2023 to −0.96 SD — a year before
the competency model and two before the 2026 paper. That measurement is made by
the PAU, marked by Basque tribunals, so it cannot by itself distinguish a thinner
cohort from a paper that stopped rewarding the top. An external instrument can.

PISA tests 15-year-olds, modal 4º ESO, who reach the PAU two years later:

    PISA 2015 -> PAU 2017    PISA 2018 -> PAU 2020
    PISA 2022 -> PAU 2024    PISA 2025 -> PAU 2027

That is three matched points inside the PAU window and two of them fall in the
marking plateau, so a PAU–PISA correlation is not available and is not attempted.
What is available is one aligned cohort — PISA 2022 / PAU 2024 — and a comparison
made on the right quantity. PISA reports proficiency levels, and levels 5 and 6
are the direct analogue of the 8–10 band: the top of the distribution, which is
exactly where the PAU signal sits.

Reads : sources/pisa/pisa2018_cap2_tablas.xlsx (INEE, table 2.9)
        sources/pisa/pisa2022_cap2_tablas.xlsx (INEE, table 2.24)
        data/analysis/shape_locus.json
Writes: plots/fig21_pisa_link.(png|svg), data/analysis/pisa_link.json,
        data/pisa_science_top_levels.csv
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
DATA = ROOT / "data"
A = DATA / "analysis"
SRC = ROOT / "sources" / "pisa"
P = ROOT / "plots"


def top_levels(path: Path, sheet: str, col5: int, col6: int) -> pd.DataFrame:
    """Share of students at proficiency levels 5 and 6 in science, by jurisdiction.

    The INEE tables put countries first and the Spanish communities after, in one
    block with a single header; the jurisdiction name is the only reliable key, so
    rows are selected by name rather than by position.
    """
    d = pd.read_excel(path, sheet_name=sheet, header=None)
    sub = d.iloc[:, [1, col5, col6]].copy()
    sub.columns = ["jurisdiccion", "n5", "n6"]
    sub = sub.dropna(subset=["jurisdiccion"])
    sub["top56"] = (pd.to_numeric(sub.n5, errors="coerce")
                    + pd.to_numeric(sub.n6, errors="coerce"))
    return sub.dropna(subset=["top56"])[["jurisdiccion", "top56"]]


p18 = top_levels(SRC / "pisa2018_cap2_tablas.xlsx", "2.9", 14, 16)
p22 = top_levels(SRC / "pisa2022_cap2_tablas.xlsx", "2.24", 14, 16)


def pick(df: pd.DataFrame, name: str) -> float:
    hit = df[df.jurisdiccion.astype(str).str.strip().str.startswith(name)]
    if hit.empty:
        raise KeyError(f"{name!r} not found")
    return float(hit.top56.iloc[0])


rows = []
for year, df in [(2018, p18), (2022, p22)]:
    for label, key in [("País Vasco", "País Vasco"), ("España", "España"),
                       ("Promedio OCDE", "Promedio OCDE")]:
        rows.append({"pisa_year": year, "pau_year": year + 2,
                     "jurisdiccion": label, "top56_pct": pick(df, key)})
top = pd.DataFrame(rows)
top.to_csv(DATA / "pisa_science_top_levels.csv", index=False)

pv = {y: float(top[(top.pisa_year == y) & (top.jurisdiccion == "País Vasco")].top56_pct.iloc[0])
      for y in (2018, 2022)}
es = {y: float(top[(top.pisa_year == y) & (top.jurisdiccion == "España")].top56_pct.iloc[0])
      for y in (2018, 2022)}
ratio = {y: pv[y] / es[y] for y in (2018, 2022)}

locus = json.load(open(A / "shape_locus.json", encoding="utf-8"))
vs_field = locus["euskadi_conditional_vs_field"]

fig, (axp, axa) = plt.subplots(1, 2, figsize=(12.6, 5.2),
                               gridspec_kw=dict(width_ratios=[1.15, 1.0], wspace=0.26))

# --- a. the top of the distribution, two instruments, one direction ---------------
order = p22.copy()
order = order[order.jurisdiccion.astype(str).str.strip().isin(
    [c.strip() for c in
     ["Andalucía", "Aragón", "Asturias, P. de", "Balears, Illes", "C. Valenciana",
      "Canarias ", "Cantabria", "Castilla y León", "Castilla-La Mancha", "Cataluña",
      "Extremadura", "Galicia", "Madrid, C. de", "Murcia, R. de", "Navarra, C. F. de",
      "País Vasco", "Rioja, La"]])]
order = order.sort_values("top56")
colours = [C["violet"] if str(j).strip() == "País Vasco" else MUTED
           for j in order.jurisdiccion]
axp.barh(range(len(order)), order.top56, color=colours, height=0.72, lw=0)
axp.set_yticks(range(len(order)))
axp.set_yticklabels([str(j).strip() for j in order.jurisdiccion], fontsize=7.6)
axp.axvline(es[2022], color=INK2, lw=1.1, ls=(0, (5, 3)), zorder=3,
            label="Spain (%.2f %%)" % es[2022])
axp.axvline(pick(p22, "Promedio OCDE"), color=C["red"], lw=1.1, ls=(0, (2, 2)),
            zorder=3, label="OECD average (%.2f %%)" % pick(p22, "Promedio OCDE"))
axp.set_xlabel("Students at PISA science levels 5–6 (%)")
axp.set_title("a. PISA 2022 science, top performers\n(the cohort that sat the PAU in 2024)")
axp.legend(loc="lower right", fontsize=7.6)
axp.grid(axis="y", visible=False)

# --- b. the two instruments side by side, as changes ------------------------------
axa.axhline(0, color=INK2, lw=1.0, zorder=1)
bars = [
    ("PISA science,\nlevels 5–6\n(PV as share of Spain)", ratio[2018], ratio[2022],
     "2018", "2022"),
]
# PISA panel: plotted as the Basque share of the Spanish figure, so that a national
# move does not read as a Basque one.
axa.plot([0, 1], [ratio[2018], ratio[2022]], color=C["violet"], lw=2.2, marker="o",
         ms=8, zorder=3)
for x, y, lab in [(0, ratio[2018], "PISA 2018\n%.2f" % ratio[2018]),
                  (1, ratio[2022], "PISA 2022\n%.2f" % ratio[2022])]:
    axa.annotate(lab, (x, y), textcoords="offset points", xytext=(0, 14),
                 ha="center", fontsize=8, color=C["violet"])
axa.axhline(1.0, color=MUTED, lw=1.0, ls=(0, (4, 3)), zorder=1)
axa.annotate("parity with Spain", xy=(1.42, 1.005), fontsize=7.6, color=MUTED,
             ha="right")
axa.set_xlim(-0.35, 1.5)
axa.set_ylim(0.55, 1.15)
axa.set_xticks([0, 1])
axa.set_xticklabels(["PISA 2018\n→ PAU 2020", "PISA 2022\n→ PAU 2024"], fontsize=8)
axa.set_ylabel("País Vasco ÷ Spain, top-performer share")
axa.set_title("b. The Basque top tail relative to Spain")
axa.annotate(
    "PAU, same cohorts: Euskadi's top-band share among passers,\n"
    "measured against the other communities in the same year,\n"
    "runs $%+.2f$ SD on average across 2016–2023 and $%+.2f$ SD in 2024."
    % (vs_field["mean_2016_2023"], vs_field["2024"]),
    xy=(0.5, 0.06), xycoords="axes fraction", fontsize=7.8, color=INK2, ha="center")

fig.text(0.005, 0.015,
         "PISA: INEE Spanish reports, science proficiency levels — PISA 2018 table 2.9, "
         "PISA 2022 table 2.24. The alignment is PISA year + 2: a 15-year-old in 4º ESO\n"
         "reaches the PAU two years later. Only three PISA rounds fall inside the PAU "
         "window and two of them land in the marking plateau, so no correlation is "
         "computed;\nthis is a comparison of one aligned cohort on the one quantity both "
         "instruments measure, the top of the distribution.",
         fontsize=7, color=MUTED, linespacing=1.5)
fig.subplots_adjust(bottom=0.24, top=0.88, left=0.13, right=0.97)
_save(fig, "fig21_pisa_link", P, dpi=200)

json.dump({
    "alignment": "PISA year + 2 (4º ESO -> 1º Bach -> 2º Bach -> PAU)",
    "matched_points_in_pau_window": {"PISA 2015": 2017, "PISA 2018": 2020,
                                     "PISA 2022": 2024},
    "pais_vasco_top56": pv, "espana_top56": es,
    "pv_over_spain": ratio,
    "oecd_2022_top56": pick(p22, "Promedio OCDE"),
    "pau_euskadi_conditional_vs_field": {
        "mean_2016_2023": vs_field["mean_2016_2023"], "2024": vs_field["2024"],
        "2025": vs_field["2025"]},
}, open(A / "pisa_link.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"PISA science levels 5-6:  PV {pv[2018]:.2f} -> {pv[2022]:.2f}   "
      f"Spain {es[2018]:.2f} -> {es[2022]:.2f}")
print(f"PV as share of Spain:     {ratio[2018]:.3f} -> {ratio[2022]:.3f}")
print(f"PAU conditional vs field: {vs_field['mean_2016_2023']:+.2f} SD (2016-23) -> "
      f"{vs_field['2024']:+.2f} SD (2024)")
