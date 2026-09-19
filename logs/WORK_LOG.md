# Work log — `claude_analysis_2026-09-18`

Independent data hunt and analysis of Physics PAU results (Euskadi 2010–2026 in its Spanish context), prepared on 18 September 2026 in a cloud workspace linked to the user's computer. Nothing outside this folder was modified; the July package, `hist_evolution` and `analysis_2026-09-18` are untouched. The rendered site is in `_site/` (open `_site/index.html`); the same log is Chapter 9 of the site.

## Request (verbatim intent)

Study the project in depth; since it started (6 July 2026) new data have been published — search exhaustively (Ministry, other universities' analyses, press, literature); report the findings; perform a more detailed analysis with the existing data plus the new ones; create a dedicated folder; conserve everything already there; organise the project; keep a log; math in LaTeX; Markdown for a Quarto website in the Zensical style; look at the analysis produced earlier today but stay independent of it; the most important point is to find the data.

## Chronology (times are Europe/Madrid)

| Time | Step | Outcome |
|---|---|---|
| 14:30 | Read the project: `fisica_pau_ehu_package` (README, dossier, CSVs, 16 EHU reports, Ministry cubes, parse script), `hist_evolution` (README, digitised centre-level data, Física tables, Cataluña series, 2026 press comparison), and the README / work log / data of `analysis_2026-09-18` (to know what it found; not reused for analysis) | Central fact confirmed: EHU Física 2026 = 3.99 (press 3.98), 39.8 % pass, 24.5 % ≤ 2, 3.2 % zeros, N = 2 066 |
| 14:35 | Task list (6 tasks) and cloud working folder | — |
| 14:40 | **First wave**: five parallel search agents with written briefs (Euskadi/EHU · Ministry + NE · South · NW/Madrid/Valencia · literature + national press) | 552 tool calls, 200 web searches (session budget), 37 files downloaded, five structured reports (`logs/SEARCH_REPORTS.md`) |
| 14:55 | Retry of the blocked official sites with the cloud fetcher | unirioja 429; unex 403; uclm 403 |
| 14:57 | **Second wave in the built-in browser** on the user's computer: unirioja → 4 PDFs, Física chart page 18 read visually (2010–2022 series) | La Rioja series recovered |
| 15:02 | alumnado.unex.es reachable — no statistics section | Extremadura stays press-level |
| 15:03 | uclm.es Power BI (through the Azure WAF bot check); Física slicer; tables read from the DOM | Castilla-La Mancha 2021–2026 recovered, both sittings, by province |
| 15:06 | ull.es Power BI "Calificaciones en la PAU por asignatura": FÍSICA × JUN/JUL × 2023-24 … 2025-26 + mean history 2010–2026 | Tenerife histograms recovered |
| 15:09 | ulpgc.es Power BI Informe 2 (page updated 11 Sep 2026): Física × JUNIO × 2024–2026 | Las Palmas histograms recovered |
| 15:10 | indicadores.usal.es → dead Infogram embed | dead end documented |
| 15:11 | legebiltzarra.eus search form not drivable | lead |
| 15:12 | universitats.gva.es: same three 2026 files as in July; downloaded from the user's machine; p. 43 re-extracted | Valencia verified independently |
| 15:15 | Staged the Ministry cubes and July CSVs from the user's machine | — |
| 15:20 | `pxparse.py` (pyaxis does not build here) + `01_build_ministry_panel.py` | 11/11 means and counts identical to the July package |
| 15:30 | Hand-coded `data/regional_fisica_found.csv` (80 rows) + dashboard transcriptions (4 CSVs) | — |
| 15:40 | `02_analysis.py` → `data/analysis/` + `results.json` | — |
| 16:00 | `03_plots.py` (10 figures), contact-sheet review, layout fixes | — |
| 16:15 | `04_tables.py`, `05_registry.py` | 16 tables, 44 files registered |
| 16:30 | Quarto site: `_quarto.yml`, `styles.scss`, `styles-dark.scss`, `index.qmd`, 10 chapters, `references.bib` (45 entries), `apa.csl` | rendered with Quarto 1.7.32; 0 broken local references; screenshots checked (desktop light/dark, mobile) |
| 17:00 | Corrections after self-review: 15/17 → 14/17 communities down in 2025; the "parallel shift" claim in Chapter 4 was wrong and was replaced by the correct statement (three moments cannot distinguish a J-shape from a floor-compressed bell; they do exclude a subgroup effect); presentation-rate range 64–76 % | — |
| 17:20 | Copied the folder to the user's computer; rendered there as well; project index written | — |
| 18:05 | User (on the phone) asks to continue unattended. Watch-list poll (`scripts/06_poll_watchlist.py`): nothing new. Browser searches on the open leads: UJI study identified (Sánchez-Tarazaga & Gimeno Rovira 2026, DOI 10.64628/AAO.atrdhyeha; País Vasco rated among the most competency-oriented PAU systems 2015–2025) and folded into Chapters 6–7; national coverage of the Basque Física figures corrected in Chapter 7; Parliament search still not drivable; no 2026 Física figure for the eight missing communities; EHU July Física still unpublished. Blocked sites listed in Chapter 9. Site re-rendered and re-copied to the Mac | — |
| 19 Sep 07:00–09:30 | **Day 2.** Exam papers 2025/2026 for nine communities collected (`sources/exams/`, 40 files); CLM read in the browser and transcribed; Valencia 2025 and Extremadura 2026 recovered from FiQuiPedia's GitLab archive; every item coded (`scripts/07_exam_coding.py`, 146 rows); figures 11–12; Chapter 11 written; Chapters 1, 6, 9, index, registry, README updated; site re-rendered and copied to the Mac | Rising communities did not move towards the competency model; Euskadi's paper changed genre on three axes; Canarias cut optionality and fell |

## Decisions

- **Independence.** The earlier session's folder was read only to learn what it had already found; every number here is recomputed from raw files or read directly from the source. Where both sessions read the same official file (Valencia p. 43, EHU deck, Ministry cubes) the values agree.
- **Denominators are kept visible**: every regional row carries its denominator and source type; Cataluña is compared on its own "aptes" basis; Canarias is pooled by presented students.
- **No causal language**: the study sorts hypotheses by what the data allow (Chapter 6) and stops there.
- **Static site**: every table is a Markdown include generated by a script, so the site renders without Jupyter.
- **Model labelled as model**: the Beta reconstruction appears only with that label; the 2026 band shares in Fig. 6 are outlined as implied, not observed.

## Numbers changed during self-review

- Chapter 4 originally claimed that a parallel shift of the 2025 density by −1.48 would give P(≤2) ≈ 0.17 and P(≥5) ≈ 0.45; recomputed: 0.23 and 0.38. The argument was rewritten.
- Index and Chapter 2 originally said 15 of 17 communities fell in 2025; the panel says 14.
- Chapter 5 presentation-rate range 2017–2024 corrected from 68–76 % to 64–76 %.

## Open items (see Chapter 9 watch-list for URLs and dates)

Item-level marks of the 2026 Basque Física scripts (by sub-task, exercise and option); comparison of the 2024 and earlier Basque papers on the same coding; second coder for `data/exam_coding_2025_2026.csv`; CLM 2026 PDF file (only transcribed); Cataluña official 2026 criteria file (404).


EHU July 2026 Física; EHU tribunal-level Física; Física revision statistics; Física by sex/language/territory 2023–2026; Basque *Resultados escolares 2025-26*; Cataluña Recull 2026; Canarias PAU-2027 minutes; Andalucía ponencias 2026-27; Murcia Informe 2026; Aragón/Navarra/Cantabria 2026 files; Galicia working-group report; Ministry EPAU 2026 (June 2027); Basque Parliament initiatives (manual BOPV check).
