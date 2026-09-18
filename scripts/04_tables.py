"""Write the Markdown tables included by the Quarto chapters (data/tables/*.md) from the analysis outputs,
so the site renders without an execution engine and every table has one machine-generated source."""
from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "data" / "analysis"
T = ROOT / "data" / "tables"
T.mkdir(exist_ok=True)
R = json.load(open(A / "results.json", encoding="utf-8"))


def f(x, d=2, thousands=False):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    if d == 0:
        return f"{x:,.0f}".replace(",", " ") if thousands else f"{x:.0f}"
    return f"{x:.{d}f}"


def md_table(header, rows, align=None):
    align = align or ["---"] * len(header)
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(align) + "|"]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out) + "\n"


# 1. Euskadi series
s = pd.read_csv(A / "euskadi_fisica_series_2010_2026.csv")
rows = []
for _, r in s.iterrows():
    rows.append([str(int(r.year)), f(r.enrolled, 0, True), f(r.presented, 0, True), f(r.passed, 0, True), f(r.pass_pct, 1), f(r["mean"]),
                 f(r.spain_mean), f(r.gap_vs_spain), ("" if pd.isna(r.delta_mean) else f"{r.delta_mean:+.2f}"), r.source])
(T / "euskadi_series.md").write_text(md_table(["Year", "Enrolled", "Presented", "Passed", "Pass %", "Mean", "Spain mean", "Gap vs Spain", "Δ mean", "Source"], rows,
                                              ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---"]), encoding="utf-8")

# 2. regimes
rows = [[r["regime"], r["years"], f(r["mean"]), f(r["pass_pct"], 1)] for r in R["regimes"]]
(T / "regimes.md").write_text(md_table(["Regime", "Years", "Mean", "Pass %"], rows, ["---", "---", "---:", "---:"]), encoding="utf-8")

# 3. rank
rk = R["euskadi_rank_by_year"]
(T / "rank.md").write_text(md_table(list(rk.keys()), [[str(v) for v in rk.values()]], ["---:"] * len(rk)), encoding="utf-8")

# 4. regions 2026 vs 2025
c = pd.read_csv(A / "regions_2026_vs_2025.csv")
short = {"Asturias (Principado de)": "Asturias", "Madrid (Comunidad de)": "Comunidad de Madrid", "País Vasco": "País Vasco (EHU)"}
rows = []
for _, r in c.iterrows():
    rows.append([short.get(r.ccaa, r.ccaa), f(r.mean_2025), f(r.mean_2026), f"{r.delta:+.2f}", f(r.pass_pct_2026, 1), f(r.presented_2026, 0, True), r.basis, r.quality])
(T / "regions_2026.md").write_text(md_table(["Community", "2025", "2026", "Δ", "Pass % 2026", "Presented 2026", "Basis of the 2026 figure", "Source type"], rows,
                                            ["---", "---:", "---:", "---:", "---:", "---:", "---", "---"]), encoding="utf-8")

# 5. ministry wide table 2015–2025 (ordinary)
w = pd.read_csv(A / "ministry_ord_mean_wide.csv", index_col=0)
w = w.drop(index=["Estado"], errors="ignore")
w = w.sort_values("2025", ascending=False)
rows = [[("**" + i + "**" if i in ("País Vasco", "Total") else i)] + [f(v) for v in r.values] for i, r in w.iterrows()]
(T / "ministry_wide.md").write_text(md_table(["Community"] + list(w.columns), rows, ["---"] + ["---:"] * len(w.columns)), encoding="utf-8")

# 6. annual-change summary by year
ch = pd.read_csv(A / "annual_changes_all_ccaa.csv")
g = ch.groupby("year").delta.agg(["mean", "median", "min", "max", lambda x: (x < 0).sum()])
g.columns = ["mean", "median", "min", "max", "n_down"]
rows = [[str(y), f"{r['mean']:+.2f}", f"{r['median']:+.2f}", f"{r['min']:+.2f}", f"{r['max']:+.2f}", f"{int(r['n_down'])}/17"] for y, r in g.iterrows()]
(T / "changes_by_year.md").write_text(md_table(["Transition to", "Mean Δ", "Median Δ", "Min", "Max", "Communities down"], rows, ["---", "---:", "---:", "---:", "---:", "---:"]), encoding="utf-8")

# 7. subjects
sub = pd.read_csv(A / "subjects_2025_2026_by_region.csv")
piv = sub.pivot_table(index="subject", columns="region", values="delta")
order_s = ["Física", "Matemáticas II", "Química", "Biología", "Historia de España", "Euskara II", "Lengua Castellana", "Hª Filosofía"]
order_r = ["País Vasco", "Cataluña", "Madrid", "Andalucía", "Asturias"]
piv = piv.reindex(order_s)[order_r]
rows = [[i] + [("—" if pd.isna(v) else f"{v:+.2f}") for v in r.values] for i, r in piv.iterrows()]
(T / "subjects_delta.md").write_text(md_table(["Subject, Δ 2025→2026"] + ["Euskadi" if x == "País Vasco" else x for x in order_r], rows, ["---"] + ["---:"] * 5), encoding="utf-8")
lv = sub.pivot_table(index="subject", columns="region", values="mean_2026").reindex(order_s)[order_r]
rows = [[i] + [("—" if pd.isna(v) else f"{v:.2f}") for v in r.values] for i, r in lv.iterrows()]
(T / "subjects_2026.md").write_text(md_table(["Subject, mean 2026"] + ["Euskadi" if x == "País Vasco" else x for x in order_r], rows, ["---"] + ["---:"] * 5), encoding="utf-8")

# 8. beta fits
bf = R["beta_fits"]
rows = []
for k, lab in (("EHU_2025", "Euskadi 2025 (5.47 / 62.3 % / 10 % ≤2)"), ("EHU_2026", "Euskadi 2026 (3.99 / 39.8 % / 24.5 % ≤2)")):
    b = bf[k]
    rows.append([lab, f(b["a"]), f(b["b"]), f(b["sd"]), f(b["median"]), f(100 * b["p_ge7"], 1), f(100 * b["p_ge9"], 1),
                 f(100 * sum(b["band_shares"][f"[{i}-{i+1})"] for i in range(5)), 1)])
(T / "beta_fits.md").write_text(md_table(["Fit", "a", "b", "SD (model)", "Median", "% ≥ 7", "% ≥ 9", "% < 5"], rows, ["---"] + ["---:"] * 7), encoding="utf-8")

# 9. Canarias histograms
H = pd.read_csv(A / "canarias_histograms.csv", index_col=0)
ch_ = R["canarias_hist"]
rows = []
for k in ["ULL_2024", "ULL_2025", "ULL_2026", "ULPGC_2024", "ULPGC_2025", "ULPGC_2026"]:
    v = ch_[k]
    rows.append([k.replace("_", " "), str(v["n"]), f(v["mean_published"]), f(100 * v["p_lt2"], 1), f(100 * v["p_lt5"], 1), f(100 * v["pile_up_5_6"], 1), f(100 * v["p_ge9"], 1)])
(T / "canarias_summary.md").write_text(md_table(["University, year (June)", "Exams", "Mean", "% < 2", "% < 5", "% in [5,6)", "% ≥ 9"], rows, ["---"] + ["---:"] * 6), encoding="utf-8")
rows = [[band] + [f(100 * v, 1) for v in r.values] for band, r in H.iterrows()]
(T / "canarias_hist.md").write_text(md_table(["Band"] + [c.replace("_", " ") for c in H.columns], rows, ["---"] + ["---:"] * len(H.columns)), encoding="utf-8")

# 10. Euskadi bands
gb = pd.read_csv(A / "euskadi_grade_bands_2015_2025.csv", index_col=0)
rows = [[str(y)] + [f(v, 1) for v in r.values] for y, r in gb.iterrows()]
(T / "euskadi_bands.md").write_text(md_table(["Year"] + list(gb.columns), rows, ["---"] + ["---:"] * len(gb.columns)), encoding="utf-8")

# 11. ordinary vs extraordinary (Euskadi + found 2026)
oe = pd.read_csv(A / "ord_vs_extra_ministry.csv")
pv = oe[oe.ccaa == "País Vasco"].dropna()
rows = [[str(int(r.year)), f(r.ordinary), f(r.extraordinary), f(r.gap)] for _, r in pv.iterrows()]
(T / "euskadi_ord_extra.md").write_text(md_table(["Year", "Ordinary", "Extraordinary", "Gap"], rows, ["---", "---:", "---:", "---:"]), encoding="utf-8")

# 12. regional found long table (compact)
reg = pd.read_csv(ROOT / "data" / "regional_fisica_found.csv")
rows = []
for _, r in reg.iterrows():
    rows.append([r.region, r.university, str(int(r.year)), r.sitting, f(r.enrolled, 0, True), f(r.presented, 0, True), f(r.passed, 0, True), f(r.pass_pct, 1), f(r["mean"], 2), f(r.sd, 2), r.source_type])
(T / "regional_found.md").write_text(md_table(["Region", "University", "Year", "Sitting", "Enrolled", "Presented", "Passed", "Pass %", "Mean", "SD", "Source type"], rows,
                                              ["---", "---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]), encoding="utf-8")

# 13. gender/language
g = pd.read_csv(A / "euskadi_gender_language.csv")
rows = [[str(int(r.year)), f(r.media_hombres), f(r.media_mujeres), f"{r.gender_gap_f_minus_m:+.2f}", f(r.pct_mujeres_matricula, 1), f(r.media_euskera), f(r.media_castellano), f"{r.lang_gap_eu_minus_es:+.2f}", f(r.pct_euskera_matricula, 1)] for _, r in g.iterrows()]
(T / "gender_language.md").write_text(md_table(["Year", "Men", "Women", "W − M", "% women enrolled", "Euskera track", "Castilian track", "EU − ES", "% euskera track"], rows, ["---"] + ["---:"] * 8), encoding="utf-8")

# 14. participation
p = pd.read_csv(A / "euskadi_participation.csv", index_col=0)
rows = [[str(int(y)), f(r.enrolled, 0, True), f(r.presented, 0, True), f(r.presentation_pct, 1)] for y, r in p.iterrows()]
(T / "participation.md").write_text(md_table(["Year", "Enrolled", "Presented", "Presented / enrolled %"], rows, ["---", "---:", "---:", "---:"]), encoding="utf-8")
print("tables written:", sorted(x.name for x in T.glob("*.md")))
