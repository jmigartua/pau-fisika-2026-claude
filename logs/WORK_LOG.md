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
| 19 Sep 09:30–12:00 | **Day 2, part 2.** User's account of the pre-2025 Basque format and conventions. EHU archive 2010–2026 downloaded (`sources/exams_ehu_hist/`, 77 PDFs); inventory of 146 problems and 118 theory questions; marking-rules table (11 corrector regimes); selection-premium simulation; figs 13–15; Chapter 12; index, Ch. 1, 6, 9, README, registry updated; re-rendered; copied to the Mac | 2025 break absorbed better than the national average; 2026 step moves on all axes at once; choice worth ≈ −0.25; penalty list shared with Canarias |
| 19 Sep 16:00–23:00 | **Day 2, part 3 — the audit.** Seven layers (`logs/audit/`): clean re-run of the pipeline; delegated recomputation of every number in Chapters 2–5 and 6; blind second coding of the 18 papers (κ = 0.76, all directions identical); figure/table check; sourcing and consistency check; reasoning audit of Chapter 6 with four new tests (`scripts/19_audit_checks.py`). Corrections applied to scripts 03, 05, 08, 09, 11, 12, 13, 16, 17, 18 and to every chapter; Chapter 13 written; `scripts/20_build_onepage.py` now generates the single-page edition; consolidated report `logs/AUDIT_2026-09-19.md`; re-rendered; copied to the Mac | Stale slope section (n = 4 text against n = 5 data) rewritten; Madrid word count was 70 % solutions (r −0.84 → −0.91 after stripping); 2027 cohort term re-prorated (−0.36 → −0.18); the "Basque turn in 2024" is shared by 5 of 17 communities and was withdrawn; the plateau "reshaping" was a level effect and was withdrawn; the plateau is present in every subject |
| 20 Sep | **Day 3 — second audit and decomposition.** Clean re-run (every JSON/CSV/table identical, every PNG pixel-identical). Five independent readers: Ch. 2–5 + index, Ch. 6 with its statistics, Ch. 11–12 against the exam PDFs, Ch. 13–14, and all 24 figures. Fixed: Asturias weighting bug in script 07 (d_ctx correlation −0.89 → −0.85), two missing 2019 theory questions (118 → 120), reading-load merge (collinearity +0.90 → +0.79, n=8), take-up centring (r −0.020 → −0.096), figures 4, 7, 9, 11, 14, 16, 17, 19, 20, 22, 23, 24. New: `scripts/21_decay_decomposition.py` and figure 25. Chapters 13 and 14 rewritten; Ch. 6 gained the decomposition and a rewritten data-request list | 2024 was a shape step (second largest of 170 transitions) and 2025 a level step; the Basque-specific 2026 component is −1.65, of which −0.44 is quantified and −1.21 is not attributable with published data |

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

## Numbers changed during the audit (19 September, evening)

See `logs/AUDIT_2026-09-19.md` (consolidated) and Chapter 13 of the site; the layer reports are in `logs/audit/`.

## Open items (see Chapter 9 watch-list for URLs and dates)

Item-level marks of the 2026 Basque Física scripts (by sub-task, exercise and option); comparison of the 2024 and earlier Basque papers on the same coding; CLM 2026 PDF file (only transcribed); Cataluña official 2026 criteria file (404); the author's decisions on the audit's open questions (Chapter 13). The second coding of `data/exam_coding_2025_2026.csv` was done in the audit (`logs/audit/E_second_coding.csv`).


EHU July 2026 Física; EHU tribunal-level Física; Física revision statistics; Física by sex/language/territory 2023–2026; Basque *Resultados escolares 2025-26*; Cataluña Recull 2026; Canarias PAU-2027 minutes; Andalucía ponencias 2026-27; Murcia Informe 2026; Aragón/Navarra/Cantabria 2026 files; Galicia working-group report; Ministry EPAU 2026 (June 2027); Basque Parliament initiatives (manual BOPV check).
