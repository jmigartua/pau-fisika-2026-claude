"""Independent analysis of Physics PAU results: Euskadi 2010–2026 in its Spanish context.

Inputs  : data/original/* (July package), data/ministry_fisica_panel.csv (script 01),
          data/regional_fisica_found.csv, data/found_canarias_*.csv, hand-coded 2026 EHU figures.
Outputs : data/analysis/*.csv and data/analysis/results.json (all numbers quoted in the report).

Every derived quantity is computed here so the Quarto chapters can cite a single source of truth.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "analysis"
OUT.mkdir(exist_ok=True)
R: dict = {}

# --------------------------------------------------------------------------------------
# 1. Euskadi Física long series 2010–2026 (ordinary sitting)
# --------------------------------------------------------------------------------------
ehu = pd.read_csv(DATA / "original" / "fisica_pau_ehu_2010_2022.csv")
mini = pd.read_csv(DATA / "ministry_fisica_panel.csv")
pv = mini[(mini.ccaa == "País Vasco") & (mini.sitting == "ordinary") & (mini.phase == "specific")].set_index("year")
es = mini[(mini.ccaa == "Total") & (mini.sitting == "ordinary") & (mini.phase == "pooled")].set_index("year")

rows = []
for _, r in ehu.iterrows():
    rows.append(dict(year=int(r.year), enrolled=r.matricula, presented=r.presentados, passed=r.aptos,
                     pass_pct=r.pct_aptos_sobre_presentados, mean=r.media, source="EHU informe (all phases)"))
for y in (2023, 2024, 2025):
    rows.append(dict(year=y, enrolled=pv.loc[y, "enrolled"], presented=pv.loc[y, "presented"], passed=pv.loc[y, "passed"],
                     pass_pct=round(pv.loc[y, "pass_pct"], 2), mean=pv.loc[y, "mean"], source="Ministry EPAU (specific phase)"))
rows.append(dict(year=2026, enrolled=np.nan, presented=2066, passed=np.nan, pass_pct=39.8, mean=3.99,
                 source="EHU presentation 6 Jul 2026 (pass count not published)"))
series = pd.DataFrame(rows)
series["spain_mean"] = series.year.map(es["mean"])
series["gap_vs_spain"] = series["mean"] - series["spain_mean"]
series["delta_mean"] = series["mean"].diff()
series["delta_pass_pct"] = series["pass_pct"].diff()
series.to_csv(OUT / "euskadi_fisica_series_2010_2026.csv", index=False, float_format="%.4g")

# implied pass count in 2026 (rounded percentage → interval)
lo = int(np.ceil(0.3975 * 2066)); hi = int(np.floor(0.3985 * 2066))
R["ehu2026_pass_count_interval"] = [lo, hi]
R["ehu2026_low_count_interval"] = [int(np.ceil(0.2445 * 2066)), int(np.floor(0.2455 * 2066))]
R["ehu2026_zero_count_interval"] = [int(np.ceil(0.0315 * 2066)), int(np.floor(0.0325 * 2066))]

# --------------------------------------------------------------------------------------
# 2. How unusual is a −1.48 one-year change?  Empirical distribution of annual changes
#    of the ordinary-sitting Física mean across all CCAA (ministry panel, 2015–2025).
# --------------------------------------------------------------------------------------
wide = mini[(mini.sitting == "ordinary") & (mini.phase == "pooled") & (~mini.ccaa.isin(["Total", "Estado"]))]
wide = wide.pivot_table(index="ccaa", columns="year", values="mean")
d = wide.diff(axis=1).iloc[:, 1:]
changes = d.stack().rename("delta").reset_index().rename(columns={"level_1": "year"})
changes["year"] = changes["year"].astype(int)
changes.to_csv(OUT / "annual_changes_all_ccaa.csv", index=False, float_format="%.3f")


def summarize(x):
    x = np.asarray(x, dtype=float)
    return dict(n=int(len(x)), mean=float(x.mean()), sd=float(x.std(ddof=1)), q05=float(np.quantile(x, .05)),
                q95=float(np.quantile(x, .95)), min=float(x.min()), max=float(x.max()))


all_d = changes.delta
non_covid = changes[~changes.year.isin([2020, 2021, 2022])].delta   # 2020–2022 are the COVID entry/exit years
R["annual_change_dist_all"] = summarize(all_d)
R["annual_change_dist_noncovid"] = summarize(non_covid)
R["annual_change_dist_2025"] = summarize(changes[changes.year == 2025].delta)   # first year of the new model
z_all = (-1.48 - all_d.mean()) / all_d.std(ddof=1)
z_nc = (-1.48 - non_covid.mean()) / non_covid.std(ddof=1)
R["ehu2026_delta_z_all"] = float(z_all)
R["ehu2026_delta_z_noncovid"] = float(z_nc)
R["ehu2026_delta_empirical_rank"] = dict(
    n_changes_more_negative=int((all_d <= -1.48).sum()), n_total=int(len(all_d)),
    most_negative=changes.sort_values("delta").head(6)[["ccaa", "year", "delta"]].to_dict("records"))
# Euskadi's own history of changes
pv_d = series.set_index("year")["delta_mean"].dropna()
R["euskadi_own_changes"] = {int(k): round(float(v), 2) for k, v in pv_d.items()}
R["euskadi_own_change_sd_excl2026"] = float(pv_d.drop(2026).std(ddof=1))

# Euskadi rank among 17 CCAA each year (ordinary pooled)
rank = wide.rank(ascending=False, axis=0)
R["euskadi_rank_by_year"] = {int(y): int(rank.loc["País Vasco", y]) for y in wide.columns}
wide.round(2).to_csv(OUT / "ministry_ord_mean_wide.csv")

# --------------------------------------------------------------------------------------
# 3. 2026 cross-regional picture (ordinary sitting) vs 2025 ministry baseline
# --------------------------------------------------------------------------------------
reg = pd.read_csv(DATA / "regional_fisica_found.csv")
base = wide[2025]
found26 = {
    "País Vasco": dict(mean=3.99, pass_pct=39.8, presented=2066, basis="presented", quality="official"),
    "Cataluña": dict(mean=6.84, pass_pct=np.nan, presented=8021, basis="eligible students (aptes)", quality="official"),
    "Andalucía": dict(mean=5.86, pass_pct=np.nan, presented=np.nan, basis="presented (N unpublished)", quality="official"),
    "Extremadura": dict(mean=5.27, pass_pct=np.nan, presented=np.nan, basis="presented (N unpublished)", quality="press"),
    "Asturias (Principado de)": dict(mean=6.62, pass_pct=76.87, presented=np.nan, basis="presented (N unpublished)", quality="official"),
    "Madrid (Comunidad de)": dict(mean=6.7, pass_pct=np.nan, presented=np.nan, basis="chart label, 1 decimal", quality="official"),
    "Comunitat Valenciana": dict(mean=6.396, pass_pct=76.35, presented=5259, basis="presented", quality="official"),
    "Castilla-La Mancha": dict(mean=6.80, pass_pct=80.07, presented=1781, basis="presented", quality="official"),
    "Canarias": dict(mean=(683 * 4.08 + 712 * 4.41) / (683 + 712), pass_pct=100 * (263 + 305) / (683 + 712), presented=683 + 712,
                     basis="ULL+ULPGC pooled, presented-weighted", quality="official"),
}
# Catalonia comparator on the same 'aptes' basis is 6.04 (not the ministry 5.98)
cmp_rows = []
for c, v in found26.items():
    b25 = 6.04 if c == "Cataluña" else float(base[c])
    cmp_rows.append(dict(ccaa=c, mean_2025=b25, mean_2026=v["mean"], delta=v["mean"] - b25, pass_pct_2026=v["pass_pct"],
                         presented_2026=v["presented"], basis=v["basis"], quality=v["quality"]))
cmp = pd.DataFrame(cmp_rows).sort_values("delta")
cmp.to_csv(OUT / "regions_2026_vs_2025.csv", index=False, float_format="%.3f")
R["regions_2026"] = dict(n_with_data=len(cmp), n_up=int((cmp.delta > 0).sum()), n_down=int((cmp.delta < 0).sum()),
                         presented_weighted_delta_excl_pv=float(np.average(cmp[cmp.presented_2026.notna() & (cmp.ccaa != "País Vasco")].delta,
                                                                            weights=cmp[cmp.presented_2026.notna() & (cmp.ccaa != "País Vasco")].presented_2026)),
                         median_delta_excl_pv=float(cmp[cmp.ccaa != "País Vasco"].delta.median()),
                         table=cmp.round(3).to_dict("records"))
not_published = ["Aragón", "Balears (Illes)", "Cantabria", "Castilla y León", "Galicia", "Murcia (Región de)",
                 "Navarra (Comunidad Foral de)", "Rioja (La)"]
R["regions_2026_not_published"] = not_published

# 2025 pass rates vs 2026 where both known
pr = mini[(mini.sitting == "ordinary") & (mini.phase == "pooled") & (mini.year == 2025)].set_index("ccaa")["pass_pct"]
R["pass_pct_2025"] = {k: round(float(pr[k]), 1) for k in ["País Vasco", "Canarias", "Castilla-La Mancha", "Comunitat Valenciana",
                                                          "Asturias (Principado de)", "Total"]}

# --------------------------------------------------------------------------------------
# 4. Distribution modelling: what do mean 3.99 / 39.8 % pass / 24.5 % ≤2 / 3.2 % zeros imply?
#    Fit a mixture  p0·δ(0) + (1−p0)·Beta(a,b) on [0,10]  to (mean, P(x<5), P(x≤2)).
# --------------------------------------------------------------------------------------

def fit_beta_mixture(mean, p_pass, p_low, p_zero, low_thr=2.0):
    """Return (a, b) of the Beta component matching mean, P(x>=5) and P(x<=low_thr) given a zero mass p_zero."""
    def resid(theta):
        a, b = np.exp(theta)
        m = p_zero * 0 + (1 - p_zero) * 10 * a / (a + b)
        pp = (1 - p_zero) * stats.beta.sf(0.5, a, b)
        pl = p_zero + (1 - p_zero) * stats.beta.cdf(low_thr / 10, a, b)
        return [(m - mean), (pp - p_pass), (pl - p_low)]
    sol = optimize.least_squares(resid, x0=np.log([1.5, 1.5]))
    a, b = np.exp(sol.x)
    return a, b, resid(sol.x)


fits = {}
for label, (mean, pp, pl, pz) in {
    "EHU_2026": (3.99, 0.398, 0.245, 0.032),
    "EHU_2025": (5.47, 0.623, 0.10, 0.012),   # 2025 zero share not published; 1.2 % assumed (Canarias-like), sensitivity below
}.items():
    a, b, res = fit_beta_mixture(mean, pp, pl, pz)
    x = np.linspace(0, 10, 1001)
    pdf = (1 - pz) * stats.beta.pdf(x / 10, a, b) / 10
    fits[label] = dict(a=float(a), b=float(b), residuals=[float(r) for r in res],
                       sd=float(np.sqrt((1 - pz) * (100 * a * b / ((a + b) ** 2 * (a + b + 1)) + (10 * a / (a + b)) ** 2) - mean ** 2)),
                       band_shares={f"[{i}-{i+1})": float((1 - pz) * (stats.beta.cdf((i + 1) / 10, a, b) - stats.beta.cdf(i / 10, a, b)) + (pz if i == 0 else 0))
                                    for i in range(10)},
                       p_ge7=float((1 - pz) * stats.beta.sf(0.7, a, b)), p_ge9=float((1 - pz) * stats.beta.sf(0.9, a, b)),
                       median=float(10 * stats.beta.ppf((0.5 - pz) / (1 - pz), a, b)))
    pd.DataFrame({"x": x, "pdf": pdf}).to_csv(OUT / f"beta_fit_{label}.csv", index=False, float_format="%.5g")
# sensitivity of the 2025 fit to the assumed zero share
for pz in (0.0, 0.02):
    a, b, _ = fit_beta_mixture(5.47, 0.623, 0.10, pz)
    fits[f"EHU_2025_pz{pz}"] = dict(a=float(a), b=float(b))
R["beta_fits"] = fits

# Canarias observed histograms (ULL + ULPGC) as an empirical check of the low-tail shape
ull = pd.read_csv(DATA / "found_canarias_ull_powerbi.csv")
ulp = pd.read_csv(DATA / "found_canarias_ulpgc_powerbi.csv")
hcols = [c for c in ull.columns if c.startswith("h_")]
hist = {}
for name, df in (("ULL", ull), ("ULPGC", ulp)):
    for _, r in df[df.sitting == "ordinary"].iterrows():
        h = r[hcols].astype(float).values
        n = h.sum()
        mids = np.arange(0.5, 10, 1.0)
        hist[f"{name}_{int(r.year)}"] = dict(n=int(n), shares=[float(v / n) for v in h], mean_from_bins=float((h * mids).sum() / n),
                                             mean_published=float(r["mean"]), p_lt2=float(h[:2].sum() / n), p_lt5=float(h[:5].sum() / n),
                                             p_ge9=float(h[-1] / n), pile_up_5_6=float(h[5] / n))
R["canarias_hist"] = hist
pd.DataFrame({k: v["shares"] for k, v in hist.items()}, index=[f"[{i}-{i+1})" for i in range(10)]).to_csv(OUT / "canarias_histograms.csv", float_format="%.4f")

# Ministry grade bands for Euskadi 2015–2025 (specific phase, ordinary)
dist = pd.read_csv(DATA / "ministry_fisica_distr.csv")
pvd = dist[(dist.ccaa == "País Vasco") & (dist.sitting == "ordinary") & (dist.phase == "specific")].set_index("year").drop(columns=["ccaa", "sitting", "phase"])
pvd = pvd.div(pvd.sum(axis=1), axis=0) * 100
pvd.round(2).to_csv(OUT / "euskadi_grade_bands_2015_2025.csv")
R["euskadi_low_band_0_5"] = {int(y): round(float(v), 1) for y, v in pvd["[0-5)"].items()}
R["euskadi_top_band_9_10"] = {int(y): round(float(v), 1) for y, v in pvd["[9-10]"].items()}

# --------------------------------------------------------------------------------------
# 5. Ordinary vs extraordinary gap (where both known), and Euskadi ministry extraordinary series
# --------------------------------------------------------------------------------------
ext = mini[(mini.phase == "pooled") & (~mini.ccaa.isin(["Total", "Estado"]))].pivot_table(index=["ccaa", "year"], columns="sitting", values="mean")
ext["gap"] = ext["ordinary"] - ext["extraordinary"]
R["ord_extra_gap"] = dict(mean_gap_all=float(ext["gap"].mean()), sd_gap_all=float(ext["gap"].std()),
                          euskadi={int(y): round(float(g), 2) for (c, y), g in ext["gap"].items() if c == "País Vasco"})
ext.reset_index().to_csv(OUT / "ord_vs_extra_ministry.csv", index=False, float_format="%.3f")
R["found_2026_extraordinary"] = {"Comunitat Valenciana": 4.162, "Castilla-La Mancha": 3.97, "ULL": 3.27, "EHU global pass % (all subjects)": 71.40}

# --------------------------------------------------------------------------------------
# 6. Participation: presentation rate, share of cohort, Bachillerato vs PAU in Euskadi
# --------------------------------------------------------------------------------------
part = pv[["enrolled", "presented", "presentation_pct"]].copy()
part.loc[2026] = [np.nan, 2066, np.nan]
part.to_csv(OUT / "euskadi_participation.csv", float_format="%.4g")
R["bachillerato_2024_25"] = dict(students=4541, passed=4455, pass_pct=98.11, mean=7.09, source="Gobierno Vasco, Resultados escolares 2024-2025, 2º Bachillerato Física (A+B+D, all networks)")
R["pau_share_of_bach"] = dict(pau2025_presented_over_bach2425=2189 / 4541, pau2026_presented_over_bach2425=2066 / 4541,
                              note="cohort offset: the 2024-25 Bachillerato cohort sits PAU 2025; 2025-26 school results not yet published")
R["school_pau_gap"] = dict(gap_2025=7.09 - 5.47, gap_2026_if_school_unchanged=7.09 - 3.99)

# --------------------------------------------------------------------------------------
# 7. Subject block comparison 2025→2026: Física, Matemáticas II, Química where both years known
# --------------------------------------------------------------------------------------
subj = pd.DataFrame([
    # region, subject, 2025, 2026, basis
    ("País Vasco", "Física", 5.47, 3.99, "EHU deck"), ("País Vasco", "Matemáticas II", 6.73, 5.06, "EHU deck"),
    ("País Vasco", "Química", 6.24, 6.03, "EHU deck"), ("País Vasco", "Biología", 6.45, 6.60, "EHU deck"),
    ("País Vasco", "Historia de España", 6.91, 6.08, "EHU deck"), ("País Vasco", "Euskara II", 6.81, 6.33, "EHU deck"),
    ("País Vasco", "Lengua Castellana", 6.39, 6.42, "EHU deck"), ("País Vasco", "Hª Filosofía", 7.10, 6.81, "EHU deck"),
    ("Cataluña", "Física", 6.04, 6.84, "Govern dossier (aptes)"), ("Cataluña", "Matemáticas II", 6.12, 4.18, "Govern dossier (aptes)"),
    ("Cataluña", "Química", 6.38, 6.04, "Govern dossier (aptes)"), ("Cataluña", "Biología", 6.23, 6.02, "Govern dossier (aptes)"),
    ("Madrid", "Física", 5.6, 6.7, "CM chart"), ("Madrid", "Matemáticas II", 5.8, 6.3, "CM chart"), ("Madrid", "Química", 6.2, 5.9, "CM chart"),
    ("Madrid", "Biología", 5.6, 6.3, "CM chart"),
    ("Andalucía", "Física", 5.69, 5.86, "Junta table / ministry 2025"),
    ("Andalucía", "Matemáticas II", float(mini[(mini.ccaa == "Andalucía") & (mini.year == 2025) & (mini.sitting == "ordinary") & (mini.phase == "pooled")]["mean"].iloc[0]) if False else np.nan, 5.95, "Junta table; 2025 baseline from ministry below"),
    ("Andalucía", "Química", np.nan, 5.27, "Junta table; 2025 baseline from ministry below"),
    ("Asturias", "Física", 5.49, 6.62, "Uniovi release / ministry 2025"), ("Asturias", "Matemáticas II", np.nan, 6.862, "Uniovi release"),
    ("Asturias", "Química", np.nan, 7.67, "Uniovi release"),
], columns=["region", "subject", "mean_2025", "mean_2026", "basis"])

# fill 2025 baselines for Mat II / Química from the ministry cube (ordinary, pooled phases)
from pxparse import parse_px  # noqa: E402
nota = parse_px(ROOT / "sources" / "ministry" / "px_pau_gen_materias_nota_fase_ca.px")
matr = parse_px(ROOT / "sources" / "ministry" / "px_pau_gen_materias_matric_fase_ca.px")


def ministry_mean(ccaa, materia, year=2025):
    q = lambda df: df[(df["Comunidad autónoma"] == ccaa) & (df["Materia"] == materia) & (df["Tipo de estudio de acceso"] == "Total")
                      & (df["Convocatoria"] == "Ordinaria") & (df["Periodo"] == str(year))]
    n = q(nota); n = n[n["Indicador"] == "Nota media de la materia"].set_index("Fase de la materia")["value"]
    m = q(matr); m = m[m["Indicador"] == "Presentados por materia"].set_index("Fase de la materia")["value"]
    ok = n.notna() & m.notna() & (m > 0)
    return float(np.average(n[ok], weights=m[ok])) if ok.any() else np.nan


mat_name = [x for x in nota["Materia"].unique() if x.startswith("Matemáticas II")][0]
qui_name = [x for x in nota["Materia"].unique() if x.startswith("Química")][0]
for i, r in subj.iterrows():
    if np.isnan(r.mean_2025):
        cc = {"Andalucía": "Andalucía", "Asturias": "Asturias (Principado de)"}[r.region]
        subj.loc[i, "mean_2025"] = ministry_mean(cc, {"Matemáticas II": mat_name, "Química": qui_name}[r.subject])
        subj.loc[i, "basis"] = r.basis.replace("below", "(ministry EPAU 2025, ordinary, presented-weighted phases)")
subj["delta"] = subj.mean_2026 - subj.mean_2025
subj.to_csv(OUT / "subjects_2025_2026_by_region.csv", index=False, float_format="%.3f")
R["ministry_subject_names"] = dict(mat=mat_name, qui=qui_name)
R["subjects_table"] = subj.round(3).to_dict("records")

# --------------------------------------------------------------------------------------
# 8. Gender & language (Euskadi 2010–2022) + Canarias 2024–2026 gender
# --------------------------------------------------------------------------------------
g = ehu[["year", "media_hombres", "media_mujeres", "pct_mujeres_matricula", "media_euskera", "media_castellano", "pct_euskera_matricula"]].copy()
g["gender_gap_f_minus_m"] = g.media_mujeres - g.media_hombres
g["lang_gap_eu_minus_es"] = g.media_euskera - g.media_castellano
g.to_csv(OUT / "euskadi_gender_language.csv", index=False, float_format="%.3g")
R["gender_gap_mean_2011_2022"] = float(g[g.year >= 2011].gender_gap_f_minus_m.mean())
R["canarias_gender_2026"] = dict(ULL=dict(women=4.09, men=4.07), ULPGC=dict(women=4.50, men=4.38))

# --------------------------------------------------------------------------------------
# 9. Regional long series (found) for the multi-region timeline plot
# --------------------------------------------------------------------------------------
long_rows = []
for c in ["País Vasco", "Cataluña", "Comunitat Valenciana", "Castilla-La Mancha", "Canarias", "Andalucía", "Madrid (Comunidad de)",
          "Asturias (Principado de)", "Extremadura", "Rioja (La)", "Aragón", "Galicia", "Navarra (Comunidad Foral de)", "Murcia (Región de)", "Cantabria", "Total"]:
    s = mini[(mini.ccaa == c) & (mini.sitting == "ordinary") & (mini.phase == "pooled")]
    for _, r in s.iterrows():
        long_rows.append(dict(ccaa=c, year=int(r.year), mean=r["mean"], pass_pct=r.pass_pct, source="ministry"))
for c, v in found26.items():
    long_rows.append(dict(ccaa=c, year=2026, mean=v["mean"], pass_pct=v["pass_pct"], source="found 2026"))
# pre-2015 from found regional sources
for _, r in reg[(reg.year < 2015) & (reg.sitting == "ordinary")].iterrows():
    cc = {"La Rioja": "Rioja (La)", "País Vasco": "País Vasco"}.get(r.region, r.region)
    if cc in ("Rioja (La)",):
        long_rows.append(dict(ccaa=cc, year=int(r.year), mean=r["mean"], pass_pct=r.pass_pct, source="UR chart"))
for _, r in series[series.year < 2015].iterrows():
    long_rows.append(dict(ccaa="País Vasco", year=int(r.year), mean=r["mean"], pass_pct=r.pass_pct, source="EHU informe"))
pd.DataFrame(long_rows).sort_values(["ccaa", "year"]).to_csv(OUT / "regional_long_series.csv", index=False, float_format="%.4g")

# --------------------------------------------------------------------------------------
# 10. Simple structural-break model for Euskadi: regime means (2010-11, 2012-16, 2017-19, 2020-21, 2022-24, 2025-26)
# --------------------------------------------------------------------------------------
regimes = {"2010-11 PAU (RD 1892/2008) first years": (2010, 2011), "2012-16 PAU settled": (2012, 2016), "2017-19 EAU/LOMCE": (2017, 2019),
           "2020-21 COVID flexibility": (2020, 2021), "2022-24 post-COVID": (2022, 2024), "2025-26 LOMLOE competency model": (2025, 2026)}
reg_stats = []
for k, (a, b) in regimes.items():
    s = series[(series.year >= a) & (series.year <= b)]
    reg_stats.append(dict(regime=k, years=f"{a}-{b}", mean=float(s["mean"].mean()), pass_pct=float(s.pass_pct.mean()), n_years=len(s)))
pd.DataFrame(reg_stats).to_csv(OUT / "euskadi_regimes.csv", index=False, float_format="%.3f")
R["regimes"] = reg_stats

# trend 2012–2024 excluding 2021 (linear) and the 2026 residual
t = series[(series.year >= 2012) & (series.year <= 2024) & (series.year != 2021)]
slope, intercept, rvalue, pvalue, stderr = stats.linregress(t.year, t["mean"])
resid_sd = float(np.std(t["mean"] - (intercept + slope * t.year), ddof=2))
R["trend_2012_2024"] = dict(slope_per_year=float(slope), intercept=float(intercept), r=float(rvalue), p=float(pvalue), resid_sd=resid_sd,
                            pred_2025=float(intercept + slope * 2025), pred_2026=float(intercept + slope * 2026),
                            resid_2025=float(5.47 - (intercept + slope * 2025)), resid_2026=float(3.99 - (intercept + slope * 2026)),
                            resid_2026_in_sd=float((3.99 - (intercept + slope * 2026)) / resid_sd))

with open(OUT / "results.json", "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2, default=float)
print(json.dumps({k: R[k] for k in ["annual_change_dist_all", "annual_change_dist_noncovid", "ehu2026_delta_z_all", "ehu2026_delta_z_noncovid",
                                    "ehu2026_delta_empirical_rank", "euskadi_rank_by_year", "regions_2026", "trend_2012_2024", "beta_fits"]}, indent=1, ensure_ascii=False, default=float)[:6000])
