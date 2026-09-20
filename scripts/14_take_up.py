#!/usr/bin/env python3
"""How large a share of the PAU cohort chooses Física, and does it explain the drift?

Figure 20 measured dilution with the raw size of each community's Física cohort,
which conflates two things: a community whose whole candidate population grew, and
a community in which a larger fraction of the same population chose Física. Only
the second is a composition effect. Separating them needs a denominator.

The ministry cube carries all 44 subjects, so one is available. Lengua Castellana y
Literatura II is compulsory in the general phase, which makes its enrolment a count
of PAU candidates in that community and year. Take-up is then

    take-up = Física enrolled (specific phase) / Lengua Castellana enrolled (general phase)

and it is the variable that actually corresponds to "the subject is recruiting
further down the distribution".

Reads : sources/ministry/px_pau_gen_materias_matric_fase_ca.px,
        data/ministry_fisica_panel.csv
Writes: data/analysis/take_up.csv, data/analysis/take_up.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pxparse import parse_px  # noqa: E402

DATA = ROOT / "data"
A = DATA / "analysis"
SRC = ROOT / "sources" / "ministry"
PLATEAU = [2020, 2021, 2022, 2023, 2024]
DENOM = "Lengua Castellana y Literatura II"
ACC = "Tipo de estudio de acceso"

matr = parse_px(SRC / "px_pau_gen_materias_matric_fase_ca.px")


def enrolled(materia: str, fase: str) -> pd.DataFrame:
    d = matr[(matr.Materia == materia)
             & (matr[ACC] == "Total")
             & (matr.Convocatoria == "Ordinaria")
             & (matr["Fase de la materia"] == fase)
             & (matr.Indicador == "Matriculados por materia")].copy()
    d = d.rename(columns={"Comunidad autónoma": "ccaa", "Periodo": "year"})
    d["year"] = d.year.astype(int)
    return d[["ccaa", "year", "value"]]


# Física must be counted across BOTH phases. Until 2016 it could also be sat in the
# general phase, so a specific-phase-only numerator undercounts 2015 and 2016 and
# produces a spurious jump of +0.05 at the 2017 reform — which would otherwise have
# been read as a surge in recruitment. Summing the phases removes the artefact.
fis_s = enrolled("Física", "Fase específica").rename(columns={"value": "fisica_spec"})
fis_g = enrolled("Física", "Fase general").rename(columns={"value": "fisica_gen"})
fis = fis_s.merge(fis_g, on=["ccaa", "year"], how="outer")
fis["fisica"] = fis[["fisica_spec", "fisica_gen"]].fillna(0).sum(axis=1)
fis = fis[["ccaa", "year", "fisica"]]
den = enrolled(DENOM, "Fase general").rename(columns={"value": "candidates"})
t = fis.merge(den, on=["ccaa", "year"])
t = t[~t.ccaa.isin(["Total", "Estado"])].dropna()
t = t[t.candidates > 0].copy()
t["take_up"] = t.fisica / t.candidates

panel = pd.read_csv(DATA / "ministry_fisica_panel.csv")
mark = panel[(panel.sitting == "ordinary") & (panel.phase == "specific")][
    ["ccaa", "year", "mean", "pass_pct"]]
t = t.merge(mark, on=["ccaa", "year"]).dropna(subset=["mean"])

# Within-community comparison again: a community against itself, so that stable
# differences between communities (which have many causes) drop out.
t["d_take_up"] = t.groupby("ccaa").take_up.transform(lambda s: (s - s.mean()) / s.std())
t["d_mean"] = t.groupby("ccaa")["mean"].transform(lambda s: s - s.mean())
# The test uses the non-plateau years only, so the within-community centring has to be
# computed on those years as well: centring on all eleven and then dropping five left
# the plotted cloud sitting at -0.3 under an axis reading "relative to the community's
# own average" (found in the audit of 20 September). The correlation is essentially
# unchanged; the picture is no longer off-centre.
nc = t[~t.year.isin(PLATEAU)].copy()
nc["d_take_up"] = nc.groupby("ccaa").take_up.transform(lambda s: (s - s.mean()) / s.std())
nc["d_mean"] = nc.groupby("ccaa")["mean"].transform(lambda s: s - s.mean())
nc = nc.dropna(subset=["d_take_up", "d_mean"])

r_takeup = stats.pearsonr(nc.d_take_up, nc.d_mean)
fit = np.polyfit(nc.d_take_up, nc.d_mean, 1)
national = t.groupby("year").apply(
    lambda g: g.fisica.sum() / g.candidates.sum(), include_groups=False)

t.assign(d_take_up_nc=lambda d: d.merge(nc[["ccaa", "year", "d_take_up"]].rename(
    columns={"d_take_up": "_x"}), on=["ccaa", "year"], how="left")["_x"].values,
       d_mean_nc=lambda d: d.merge(nc[["ccaa", "year", "d_mean"]].rename(
    columns={"d_mean": "_y"}), on=["ccaa", "year"], how="left")["_y"].values)\
    .to_csv(A / "take_up.csv", index=False)
summary = {
    "denominator_subject": DENOM,
    "n_region_years": int(len(t)),
    "n_non_plateau": int(len(nc)),
    "national_take_up_by_year": {int(y): round(float(v), 4) for y, v in national.items()},
    "take_up_r": float(r_takeup[0]), "take_up_p": float(r_takeup[1]),
    "take_up_slope_per_sd": float(fit[0]),
}
json.dump(summary, open(A / "take_up.json", "w", encoding="utf-8"), indent=2,
          ensure_ascii=False)
print("national take-up by year:")
for y, v in national.items():
    print(f"  {int(y)}  {v:.3f}{'  (plateau)' if y in PLATEAU else ''}")
print(f"\nwithin-community, non-plateau years (n={len(nc)}):")
print(f"  take-up vs mean mark: r = {r_takeup[0]:+.3f}, p = {r_takeup[1]:.3f}, "
      f"slope {fit[0]:+.3f} points per SD of take-up")
