# claude_analysis_2026-09-18 — Physics PAU 2026: independent data hunt and analysis

Prepared 18 September 2026. Everything in this folder was produced in this session; nothing outside it was modified.

**Start here:** open `_site/index.html` (rendered Quarto website, Zensical-style: header tabs, section sidebar, right TOC, search, light/dark), or read `index.qmd` and `chapters/*.qmd` directly.

## What is here

| Path | Content |
|---|---|
| `index.qmd`, `chapters/01…10-*.qmd` | The report: overview; data hunt; Euskadi series; Spain 2026; distributions; subjects/sittings/participation/groups; interpretation & 2027; literature; sources; log; methods & reproduction |
| `_quarto.yml`, `styles.scss`, `styles-dark.scss`, `assets/`, `references.bib`, `apa.csl` | Site configuration, theme, bibliography (45 entries) |
| `_site/` | Rendered site (Quarto 1.7.32) |
| `data/regional_fisica_found.csv` | **The consolidated regional Física dataset** located in this study (80 rows, with denominator, source type and URL) |
| `data/found_clm_powerbi.csv`, `data/found_canarias_ull_powerbi.csv`, `data/found_canarias_ull_history.csv`, `data/found_canarias_ulpgc_powerbi.csv` | Transcriptions of the UCLM, ULL and ULPGC dashboards (Física 2021–2026, histograms, zeros, tens, means by sex) |
| `data/ministry_fisica_panel.csv`, `ministry_fisica_distr.csv`, `ministry_fisica_ord_ccaa.csv` | Ministry EPAU Física panel 2015–2025, all CCAA, parsed here from the PC-Axis cubes |
| `data/original/` | Copies of the July package CSVs (validation targets) |
| `data/analysis/` | All computed outputs; `results.json` holds every scalar quoted in the text |
| `data/tables/` | Markdown tables included by the chapters (generated) |
| `sources/raw/` | 37 downloaded documents (PDF/XLSX/HTML) · `sources/ministry/` 3 cubes · `sources/text/` extractions · `sources/agent_extractions/` the search agents' raw CSVs · `sources/source_registry.csv` |
| `scripts/` | `pxparse.py`, `01_build_ministry_panel.py`, `02_analysis.py`, `03_plots.py`, `04_tables.py`, `05_registry.py` |
| `plots/` | Ten figures, PNG (200 dpi) and SVG |
| `logs/WORK_LOG.md`, `logs/SEARCH_REPORTS.md` | Chronological log; the five search agents' full reports |

## Rebuild

```bash
python3 scripts/01_build_ministry_panel.py && python3 scripts/02_analysis.py && python3 scripts/03_plots.py \
  && python3 scripts/04_tables.py && python3 scripts/05_registry.py && quarto render
```

Python ≥ 3.10 with numpy, pandas, scipy, matplotlib; Quarto ≥ 1.4; no Jupyter needed (static includes).

## Headline

Euskadi Física June 2026: mean 3.99, 39.8 % pass, 24.5 % at ≤ 2, 3.2 % zeros (N = 2 066). Nine communities have a 2026 Física mean: six rose (Asturias +1.13, Madrid +1.05, Castilla-La Mancha +0.94, Cataluña +0.80, C. Valenciana +0.51, Andalucía +0.17), three fell (Euskadi −1.48, Canarias −0.83, Extremadura −0.82). The 2025 fall was national (14 of 17 down, mean −0.81); the 2026 fall is regional. Canarias 2026 (ULL 4.08 / 38.5 %, ULPGC 4.41 / 42.8 %, with full histograms) is the Basque case's twin. The Basque cohort's school Física mark was 7.09 with 98 % passing.
