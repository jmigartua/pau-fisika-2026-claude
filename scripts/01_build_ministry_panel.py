"""Build the Ministry (SIIU/EPAU) Física panel 2015–2025 for all CCAA from the three PC-Axis cubes.

Outputs (data/):
  ministry_fisica_panel.csv      one row per CCAA × year × sitting × phase (+ a 'both phases' pooled row)
  ministry_fisica_distr.csv      grade-band distribution per CCAA × year × sitting × phase
  ministry_fisica_ord_ccaa.csv   wide table: ordinary-sitting mean per CCAA × year (pooled phases, presentados-weighted)
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from pxparse import parse_px  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "ministry"
OUT = ROOT / "data"

nota = parse_px(SRC / "px_pau_gen_materias_nota_fase_ca.px")
matr = parse_px(SRC / "px_pau_gen_materias_matric_fase_ca.px")
dist = parse_px(SRC / "px_pau_gen_materias_distr_fase_ca.px")

CCAA = "Comunidad autónoma"
ACC = "Tipo de estudio de acceso"


def fisica(df):
    d = df[(df["Materia"] == "Física") & (df[ACC] == "Total") & (df["Convocatoria"] != "Total")].copy()
    d["year"] = d["Periodo"].astype(int)
    d["sitting"] = d["Convocatoria"].map({"Ordinaria": "ordinary", "Extraordinaria": "extraordinary"})
    d["phase"] = d["Fase de la materia"].map({"Fase general": "general", "Fase específica": "specific"})
    return d


n = fisica(nota).pivot_table(index=[CCAA, "year", "sitting", "phase"], columns="Indicador", values="value", aggfunc="first")
n.columns = ["mean", "mean_passed"]
m = fisica(matr).pivot_table(index=[CCAA, "year", "sitting", "phase"], columns="Indicador", values="value", aggfunc="first")
m.columns = ["passed", "enrolled", "presented"]
panel = n.join(m, how="outer").reset_index().rename(columns={CCAA: "ccaa"})
panel = panel[["ccaa", "year", "sitting", "phase", "enrolled", "presented", "passed", "mean", "mean_passed"]]

# pooled (both phases) rows, presentados-weighted mean
def pool(g):
    g = g.dropna(subset=["presented"])
    if g.empty:
        return pd.Series({"enrolled": np.nan, "presented": np.nan, "passed": np.nan, "mean": np.nan, "mean_passed": np.nan})
    w = g["presented"]
    mean = np.nan if g["mean"].isna().all() else np.average(g["mean"].fillna(0), weights=w.where(g["mean"].notna(), 0)) if w.where(g["mean"].notna(), 0).sum() > 0 else np.nan
    wp = g["passed"].where(g["mean_passed"].notna(), 0)
    meanp = np.average(g["mean_passed"].fillna(0), weights=wp) if wp.sum() > 0 else np.nan
    return pd.Series({"enrolled": g["enrolled"].sum(min_count=1), "presented": w.sum(), "passed": g["passed"].sum(min_count=1), "mean": mean, "mean_passed": meanp})


pooled = panel.groupby(["ccaa", "year", "sitting"]).apply(pool, include_groups=False).reset_index()
pooled["phase"] = "pooled"
panel = pd.concat([panel, pooled[panel.columns]], ignore_index=True)
panel["pass_pct"] = 100 * panel["passed"] / panel["presented"]
panel["presentation_pct"] = 100 * panel["presented"] / panel["enrolled"]
panel = panel.sort_values(["ccaa", "year", "sitting", "phase"]).reset_index(drop=True)
panel.to_csv(OUT / "ministry_fisica_panel.csv", index=False, float_format="%.4g")

# distribution
d = fisica(dist)
d = d.rename(columns={CCAA: "ccaa", "Distribución de la nota": "band"})
distr = d.pivot_table(index=["ccaa", "year", "sitting", "phase"], columns="band", values="value", aggfunc="first").reset_index()
distr.to_csv(OUT / "ministry_fisica_distr.csv", index=False, float_format="%.6g")

# wide ordinary means (pooled phases)
wide = panel[(panel["sitting"] == "ordinary") & (panel["phase"] == "pooled")].pivot_table(index="ccaa", columns="year", values="mean")
wide.to_csv(OUT / "ministry_fisica_ord_ccaa.csv", float_format="%.3f")

# sanity checks against the original July package (Euskadi, specific phase, ordinary)
pv = panel[(panel["ccaa"].str.contains("Vasco")) & (panel["sitting"] == "ordinary") & (panel["phase"] == "specific")].set_index("year")
orig = pd.read_csv(OUT / "original" / "fisica_pau_ministerio_2015_2025.csv").set_index("year")
chk = pd.DataFrame({"mean_new": pv["mean"], "mean_orig": orig["media_ordinaria"], "pres_new": pv["presented"], "pres_orig": orig["presentados"]})
print(chk)
assert (chk["mean_new"].round(2) == chk["mean_orig"].round(2)).all(), "mean mismatch vs original package"
assert (chk["pres_new"] == chk["pres_orig"]).all(), "presented mismatch vs original package"
print("\nOK: ministry panel reproduces the July package Euskadi series exactly.")
print(wide.round(2).to_string())
