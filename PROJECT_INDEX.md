# 20260706_pau_fisika_analysis — project index

Project: Physics (Física / Fisika) in the university-entrance exam (PAU / USaP) at UPV/EHU — the 2026 result (mean 3.99) and its 2010–2026 context, for the 2027 reflection (`usap-fisika-2026-hausnarketa-2027`).

Nothing has been moved or edited; this file only describes what each folder holds and where to look first. Folders are listed in the order they were created.

| Folder | Created | What it is | Entry point |
|---|---|---|---|
| `fisica_pau_ehu_package/` | 6 Jul 2026 | The original working package: 16 EHU annual reports 2010–2025 (PDF), Ministry EPAU PC-Axis tables (2015–2025), the consolidated Euskadi Física CSVs, the evidence dossier | `fisica_pau_ehu_dossier.md`, `README.md` |
| `hist_evolution/` | 6 Jul 2026 | Digitised data from the EHU reports (centre-level Bachillerato-vs-exam distributions 2010–2016, Física tables 2010–2022, series to 2025), the Cataluña 2014–2026 press series and the 2026 cross-subject press comparison | `README.md` |
| `re36208-pdf.pdf` | 6 Jul 2026 | Ruiz de Gauna et al. (2013), Revista de Educación 362 — the Basque Mathematics PAU results/teacher-opinion study | — |
| `analysis_2026-09-18/` | 18 Sep 2026 (morning) | Research update produced by an earlier session (Codex): source audit of the July package, EHU/ministry/regional/literature searches, extended analyses, Quarto site | `README.md`, `_site/index.html`, `logs/WORK_LOG.md` |
| `claude_analysis_2026-09-18/` | 18 Sep 2026 (afternoon) | **Independent data hunt and analysis** (this session): the largest set of 2026 Física results located so far (nine communities; dashboards read in a browser), Ministry panel re-parsed and validated, ten figures, Quarto site in Zensical style, full logs and source registry | `README.md`, `_site/index.html`, `logs/WORK_LOG.md` |

## Where the key numbers live

- Euskadi Física series 2010–2026: `claude_analysis_2026-09-18/data/analysis/euskadi_fisica_series_2010_2026.csv` (spliced from `fisica_pau_ehu_package/data/*.csv`, the Ministry cubes and the EHU 6 July 2026 deck).
- All regional Física figures found (with denominators and URLs): `claude_analysis_2026-09-18/data/regional_fisica_found.csv`.
- Ministry Física panel, all CCAA 2015–2025: `claude_analysis_2026-09-18/data/ministry_fisica_panel.csv`.
- Canarias histograms (ULL, ULPGC) and Castilla-La Mancha 2021–2026: `claude_analysis_2026-09-18/data/found_*.csv`.
- Raw source documents: `fisica_pau_ehu_package/informes/`, `fisica_pau_ehu_package/ministerio_px/`, `analysis_2026-09-18/sources/raw/`, `claude_analysis_2026-09-18/sources/raw/`.

## Relationship between the two 18 September folders

Both were asked the same question. They were produced independently and overlap on the EHU deck, the Ministry cubes and the Valencia PDFs (values agree). `claude_analysis_2026-09-18` additionally holds: Cataluña's primary 2026 dossier with a five-year back-series; Andalucía, Extremadura, Asturias and Madrid 2026 means; Castilla-La Mancha 2021–2026 and Canarias 2024–2026 from their dashboards; La Rioja 2010–2022; Aragón 2020–2025, Navarra 2025, Murcia 2025, Cantabria 2025 and Galicia 2020–2023 series; the Basque school-results report (2º Bachillerato Física 2024-25); ten new literature references; and the post-6-July institutional record (Pedrosa interview, EHU extraordinary sitting, Galicia reform). Its watch-list (`chapters/09-log.qmd`) gives the URLs and expected dates of the next publications.
