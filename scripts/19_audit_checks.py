#!/usr/bin/env python3
"""Audit of 19 September 2026 — the checks the audit added to the study.

Three tests that Chapter 6 should have run, now reproducible:
  1. Is the 2020–2024 plateau, and its end in 2025, present in every subject?
  2. What is the base rate of a two-year negative turn on the conditional top-band
     residual, and how many communities show the 2024–25 turn attributed to Euskadi?
  3. Do Euskadi's other subjects sit above or below their own pre-COVID norms, and
     where does each of the nine 2026 communities sit against its pre-COVID norm?

Reads : sources/ministry/px_pau_gen_materias_nota_fase_ca.px, data/ministry_fisica_panel.csv,
        data/ministry_fisica_distr.csv, data/analysis/regions_2026_vs_2025.csv
Writes: data/audit/*.csv, data/tables/audit_*.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pxparse import parse_px  # noqa: E402

DATA = ROOT / "data"
OUT = DATA / "audit"
TABLES = DATA / "tables"
OUT.mkdir(exist_ok=True)

df = parse_px(ROOT / "sources" / "ministry" / "px_pau_gen_materias_nota_fase_ca.px")
df = df[(df["Tipo de estudio de acceso"] == "Total") & (df["Convocatoria"] == "Ordinaria")
        & (df["Indicador"] == "Nota media de la materia")].copy()
df["year"] = df.Periodo.astype(int)
SUBJECTS = ["Física", "Matemáticas II", "Química", "Biología", "Historia de España",
            "Lengua Castellana", "Dibujo Técnico II", "Geografía"]
CCAAS = [c for c in df["Comunidad autónoma"].unique() if c != "Total"]


def series(ccaa: str, materia: str) -> pd.Series:
    x = df[(df["Comunidad autónoma"] == ccaa) & (df.Materia.str.startswith(materia))]
    g = x.groupby(["year", "Fase de la materia"])["value"].mean().unstack()
    v = g["Fase general"].fillna(g["Fase específica"]) if "Fase general" in g else g["Fase específica"]
    return v.dropna()


def md(df_, cols, headers, fmts):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for _, r in df_.iterrows():
        out.append("| " + " | ".join(f.format(r[c]) if pd.notna(r[c]) else "—" for c, f in zip(cols, fmts)) + " |")
    return "\n".join(out) + "\n"


YEARS = list(range(2015, 2026))

# 1. plateau by subject (17 communities, unweighted, each subject vs its own 2015–19 norm)
rows = []
for s in SUBJECTS:
    per = pd.DataFrame({c: series(c, s) for c in CCAAS})
    ym = per.mean(axis=1)
    b = ym.loc[2015:2019].mean()
    rows.append(dict(subject=s, baseline_2015_19=round(b, 3), **{str(y): round(ym.get(y, np.nan) - b, 3) for y in YEARS}))
plateau = pd.DataFrame(rows)
plateau.to_csv(OUT / "plateau_by_subject.csv", index=False)
(TABLES / "audit_plateau_by_subject.md").write_text(md(
    plateau, ["subject"] + [str(y) for y in range(2019, 2026)],
    ["Subject (17 communities, unweighted)"] + [str(y) for y in range(2019, 2026)],
    ["{}"] + ["{:+.2f}"] * 7))

# 3a. Euskadi's subjects vs own baseline
rows = []
for s in SUBJECTS:
    v = series("País Vasco", s)
    b = v.loc[2015:2019].mean()
    rows.append(dict(subject=s, baseline_2015_19=round(b, 3), **{str(y): round(v.get(y, np.nan) - b, 3) for y in YEARS}))
bsq = pd.DataFrame(rows)
bsq.to_csv(OUT / "basque_subjects_vs_baseline.csv", index=False)
(TABLES / "audit_basque_subjects.md").write_text(md(
    bsq, ["subject", "baseline_2015_19"] + [str(y) for y in range(2020, 2026)],
    ["Euskadi subject", "2015–19 mean"] + [str(y) for y in range(2020, 2026)],
    ["{}", "{:.2f}"] + ["{:+.2f}"] * 6))

# 3b. 2026 vs pre-COVID baseline, nine communities
reg = pd.read_csv(DATA / "analysis" / "regions_2026_vs_2025.csv")
P = pd.read_csv(DATA / "ministry_fisica_panel.csv")
p = P[(P.sitting == "ordinary") & (P.phase == "pooled")]
rows = []
for _, r in reg.iterrows():
    s = p[p.ccaa == r.ccaa].set_index("year")["mean"]
    b = s.loc[2015:2019].mean()
    rows.append(dict(ccaa=r.ccaa, baseline_2015_19=round(b, 3), d2024=round(s[2024] - b, 3),
                     d2025=round(r.mean_2025 - b, 3), d2026=round(r.mean_2026 - b, 3),
                     yoy_2026=r.delta, basis=r.basis))
base26 = pd.DataFrame(rows).sort_values("d2026", ascending=False)
base26.to_csv(OUT / "baseline_2026_by_community.csv", index=False)
(TABLES / "audit_baseline_2026.md").write_text(md(
    base26, ["ccaa", "baseline_2015_19", "d2024", "d2025", "d2026", "yoy_2026"],
    ["Community", "2015–19 mean", "2024 vs norm", "2025 vs norm", "2026 vs norm", "2025 → 2026"],
    ["{}", "{:.2f}", "{:+.2f}", "{:+.2f}", "{:+.2f}", "{:+.2f}"]))

# 2. base rate of the conditional-ratio turn
D = pd.read_csv(DATA / "ministry_fisica_distr.csv")
dd = D[(D.sitting == "ordinary") & (D.phase == "specific")]
pp = P[(P.sitting == "ordinary") & (P.phase == "specific") & (~P.ccaa.isin(["Estado", "Total"]))]
m = pp.merge(dd, on=["ccaa", "year", "sitting", "phase"])
m["ratio"] = (m["[8-9)"] + m["[9-10]"]) / m["pass_pct"]
coef = np.polyfit(m["mean"], m["ratio"], 2)
m["res"] = m["ratio"] - np.polyval(coef, m["mean"])
m["resf"] = m.res - m.groupby("year").res.transform("mean")      # against the field in the same year
sd = m.resf.std(ddof=1)
m["z"] = m.resf / sd
w = m.pivot(index="ccaa", columns="year", values="z").round(2)
w["neg_2024_and_2025"] = (w[2024] < -0.5) & (w[2025] < -0.5)
w["any_two_year_run_below_-0.5"] = [any((row[y] < -0.5 and row[y + 1] < -0.5) for y in range(2015, 2025)) for _, row in w.iterrows()]
w["positive_years_2016_2023"] = (w.loc[:, 2016:2023] > 0).sum(axis=1)
w.to_csv(OUT / "conditional_turn_base_rate.csv")
summary = pd.DataFrame([
    dict(statistic="communities with residual < −0.5 SD in both 2024 and 2025", value=int(w.neg_2024_and_2025.sum()), of=17,
         which=", ".join(sorted(w[w.neg_2024_and_2025].index))),
    dict(statistic="communities with any two consecutive years below −0.5 SD", value=int(w["any_two_year_run_below_-0.5"].sum()), of=17, which=""),
    dict(statistic="communities with ≥ 7 positive years in 2016–2023 (Euskadi: 6)", value=int((w.positive_years_2016_2023 >= 7).sum()), of=17,
         which=", ".join(sorted(w[w.positive_years_2016_2023 >= 7].index))),
])
(TABLES / "audit_turn_base_rate.md").write_text(md(summary, ["statistic", "value", "of", "which"],
                                                    ["Statistic", "n", "of", "Communities"], ["{}", "{}", "{}", "{}"]))
print(plateau.to_string(index=False))
print(summary.to_string(index=False))
