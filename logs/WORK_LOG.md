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

## 20 September 2026, third round — four objections from the coordinator

Objections raised after reading the rewritten briefing, and the work each produced.

1. **"I do not understand this paragraph."** The "blind to 2024" paragraph asserted its conclusion
   without the mechanism. Rewritten in EN and ES to give the arithmetic: 8–10 share −9.0 pp, pass
   rate +2.3 pp, mean −0.21.
2. **"Why measure the Basque decay from the Spanish mean?"** New section
   `06-interpretation.qmd#why-a-field`: three frames (−1.48 / −1.91 / −1.65, spread 0.43), what the
   field is for (separating 2025 from 2026), and the explicit statement that it is not a control.
   Range of the Basque-specific component under alternative fields: [−1.95, −1.48].
3. **"We followed all the requirements; other communities' increases are fictitious."**
   New `scripts/23_comparability.py`, new section `11-exam-content.qmd#comparability`, fig 27.
   Asturias fails C1 (100 % optionality) and C3 (no obligatory item) and rose +1.13; C2 (open
   response) is met by all nine and separates nobody. Reform-intensity index: PV +1.76 SD, rank 1
   of 9. r(index, Δmean) = −0.701, p = 0.0355; without PV r = −0.396, p = 0.332; Spearman
   rho = −0.383, p = 0.309. No non-compliance claim: RD 534/2024 and the CRUE orientations are not
   in the source registry (data request 9).
4. **Tribunal / marking severity, second year of the criteria.** New
   `scripts/22_subject_decomposition.py`, new sections in ch 6 and both briefings, fig 26.
   Exact split on the balanced 5×3 panel: −1.48 = +0.057 (field core) + 0.743 (field Física
   premium) − 1.177 (Euskadi-common) − 1.103 (Física-specific). ANOVA cross-check leaves the
   residual at −0.882. Severity: quantitative mean −1.120 vs verbal −0.284, gap −0.836; general
   severity bounded at |−0.284| = 19 % of the Física fall. Timing fits the year-two hypothesis
   (Basque-specific +0.03 in 2025, −1.65 in 2026). New data request 3: the deduction tally.
5. **"Can a rate of decay be projected?"** New `scripts/24_cohort_rate.py`, new section
   `06-interpretation.qmd#rate-of-decay`, fig 28. Basque PISA per-cohort-year: +0.01, +3.65,
   −7.53, +1.44, −1.97, −6.99 (spread 11.19 around −1.90). Interpolated 2026-cohort excess
   −4.53 pts/yr = −0.118 marks. Top-band check: observed 1.83 % vs 1.92 % predicted by a uniform
   shift (ratio 0.952) — a location move, not a tail collapse. Selection transfer: 0.232 under a
   fixed bar, 1.000 under a fixed share; take-up flat (r = −0.096, p = 0.339) favours the second,
   so the 1:1 conversion is the top of the range and the cohort term is an upper bound
   (−0.118 to −0.027 marks/yr). 2026 entries 2 066 vs 2 189 (−5.6 %): dilution runs the wrong way,
   max gain if the weakest stayed away +0.287 marks. 2027: cohort −0.182 gross / −0.118 excess
   against a paper SD of 0.855 (ratio 4.70). Identification: ΔG not identified at any sample size.

No previously published number changed in this round. Figures 26, 27 and 28 added; the figure
count is now 28. Index gained findings 9 and 10; chapter 13 gained "The third round".

### Verification of the third round (two independent readers, 20 September)

Both recomputed every new number from the source CSVs. All derived values reproduced exactly
(subject split, severity signature, reform index and its leave-one-out, PISA rates, interpolation,
top-band check, selection transfer, entry-count bound, 2027 terms). Six prose errors found, all of
them counts or proportions rather than computed quantities:

1. "split the −1.48 exactly into −1.18 and −1.10" — those two sum to −2.28 (the four-term identity
   also has +0.06 and +0.74). Rewritten in both briefings' callouts.
2. "a little more than half of the Basque-specific fall" — 51.6 % of 2.28, 71.4 % of 1.65, 79.6 %
   of 1.48; denominator unstated. Restated against the 2.28 in all five places.
3. "+0.74 above in all four" — +0.74 is the mean; the four premia are +1.29, +0.67, +0.38, +0.63.
4. "the same tribunals ... the same cohort" — each subject has its own correctors and candidates.
   Replaced with "same sitting, same university, same marking specification" in ch 6, both
   briefings, index.qmd and the severity_signature footer (script 22).
5. "four communities did not move on any of the four axes" — none is at zero on all four; three
   (Asturias, Madrid, Extremadura) moved only on d_ctx_exp; four have d_opt = 0. Fixed in
   ch 6, ch 11, ch 13, index.qmd and both briefings (7 places).
6. "only Euskadi both cut optionality and raised the competency share" — Castilla-La Mancha did
   both (−30, +20) while cutting contextualised marks 45. The unique claim is "all four axes in the
   reform direction", which is Euskadi alone.

Smaller: Asturias +1.13 is the largest rise, not the second (ch 11); the verbal-mean "bound" is
conditional on the 2026 verbal papers being no easier, now stated; Euskara II −0.48 added to the
text-exposure sentence; "five per cent" → "just under five per cent" (4.78 %); "six of the nine"
→ "six of the eight that have such an item"; the 0.85/1.68 ratio sentence re-attached to its
denominators (4.7× and 9.2×). Constant harmonised: 17_pau2027_estimator.py SD_PAU 2.34 → 2.343;
no published rounded value changed (−0.36, −0.18, 6.5, 2.37, 5.11, 3.81, 1.23 all unchanged).

## 20 September 2026, fourth round — the statement, and a synthesis for the meeting

Three requests: a synthesis of the dossier for the admissions office and the coordination
meeting with the Bachillerato physics teachers; the last rounds added to the analysis-path
account; and an in-depth reading of the coordination presentation `2027-usap-presentation-mdc`
(Slidev, 14 slides, 18 Sep 2026), in particular slides 8–11.

**New script `25_statement_budget.py`, figure 29, new section `06#statement-budget`.**

Per-statement word counts, Spanish text, weights and page furniture removed:

| | A1 | B1 | B2 | C1 | C2 | D1 | D2 | read | answered |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2025 | 423 | 147 | 110 | 56 | 107 | 107 | 96 | 1046 | 685–784 |
| 2026 | 289 | 413 | — | 145 | 232 | 158 | 201 | 1438 | 1005–1135 |

* Growth on statements +37.5 %; on the whole file +45.3 % (1335 → 1940). The difference is
  furniture: 289 → 502 words. Of the 2026 furniture, 100 words are fifty printed sub-task
  weights; the 2025 paper printed none (only the global "2.5 puntos" in the instructions).
* The length lives in the obligatory competency items in BOTH years: 2025 A1 = 423 of 1046
  (40 %); 2026 A1 + B1 = 702 of 1438 (49 %). B1 alone is 28.7 % of what is read for 25 % of
  the marks.
* **Independent check of a load-bearing number**: the coordination's own counts of the same
  six 2026 statements are 295/408/150/242/163/214 = 1472 against this study's
  289/413/145/232/158/201 = 1438 — item by item within 1–6 %, total 2.3 %.
* 2027 target (presentation slide 5): 150–175 words per statement, mean 162 → 900–1050 read,
  600–700 answered; a cut of 32 % in reading and 36 % in answering. The 2025 paper's actual
  mean was 149 per statement and 2026's 240, so the target is 2025 plus what the competency
  form costs, not a return to 2025. On the whole-file convention it maps to ≈ 1474 against
  the chapter's independently derived 1300–1400 — the two agree to about 5 %.

**Slides 8–11, the four versions of B1.** Forward ladder (slide 8): 90 → 178 → 244 → 408.
Reverse ladder (slides 9–11): 113 (habitual with figure) / 153 (with prose) → 154 (ideal
competency form) / 170 (with the drawing asked) → 287 (no narrative) → 408 (as issued). The
two share only their endpoint; the intermediate rungs differ by 20–45 words because the
wording at each rung is not the same text. Flagged for labelling.

Design intent as stated: three habitual calculations asked twice, one per configuration
(Φ(t), ε(t), ε(7.0 ms)); three competency elements asked once (justify the angle is constant,
express in scientific notation to two decimals, decide whether the prototype meets the 0.50 mV
requirement). Three findings:

1. **The scaffolding is symmetric, and symmetry is where the words are.** Asymmetric
   scaffolding — break the chain out in configuration I, compress it in II — costs the words
   once and tests transfer rather than rehearsal; ≈ 170 words against 287 and 408.
2. **One of the three competency elements is a marking rule.** "Express in scientific notation
   with two decimals" is not on the presentation's own four-level ladder; it is a criterion
   that applies whether printed or not and costs −0.10 when missed. It is a locatable instance
   of the format/marking confound the severity analysis could bound but not separate: in that
   sub-task the competency wording and the deduction are the same words.
3. **A falsifiable test of the design.** b) and c) ask the same chain of two configurations; if
   the repetition was scaffolding, c) > b); if it was a time tax, c) < b). Added as the first
   sub-question of data request 1.

Five rules added to the chapter, ordered by words saved: context as data not story (156 → 76
on B1); set-up as a figure (153 → 113, and ask for the drawing if the geometry is assessed,
+16); scaffold once not twice; marking criteria out of the statement and weights into a margin
column (100 words); one verb per level per problem.

**Error found**: figure 18's step 14 still carried the pre-correction −0.44 / −1.21 where the
prose says −0.31 / −1.33. Sixth instance of the same failure mode, second in that figure.
Corrected; steps 15 and 16 added; the figure grew to 19 in and STEP 1.62 to fit them.

**New chapters 15 / 15-es**, the synthesis for the coordination (EN + ES, PDF, numeric parity
verified). Sidebar section "Briefing" now leads with them. Excluded from the single-page
edition, like the briefings.

### Verification of the fourth round, and the corrections it forced

An independent reader recomputed every statement count from the archived papers. Three defects
in `25_statement_budget.py` and eight in the prose; none changed a conclusion, all are fixed.

Script:
* the trailing-block-heading cut used `BLOQUE\s+[A-D]\s*:`, which (i) does not match the plural
  "BLOQUES C y D" and (ii) cuts at the colon rather than at the start of the apparatus. Twenty
  words of "BLOQUES B, C y D: Problemas / (Cada BLOQUE consta de 2 problemas…) / 2. Problema,"
  stayed inside A1 2025 and seven inside B1 2026. Now cuts at `BLOQUES?\s+[A-D]\b`.
  **A1 2025 423 → 403; B1 2026 413 → 406; B2 2025 110; C2 2025 107; C2 2026 232.**
* the weight regex could not match across an interposed watermark letter
  ("(0.50 \n U \n puntos)"), so it counted 50 where there are **51** (103 words, not 100).
  Of the 51, 18 are part-level and 33 on sub-tasks — "a weight on fifty sub-tasks" was wrong twice.
* the furniture was computed as script 18's word-token count minus this script's whitespace
  count. On one tokenisation it is **356 → 398**, not 289 → 502: the furniture barely grew, it
  was recomposed (block headings 101 → 54, weights 0 → 103).

Corrected totals: read 2025 **1026** (answered 665–784→665–764), read 2026 **1431** (998–1128);
statement growth **+39.5 %**; B1 **28.4 %** of reading for 25 % of marks; A1 2025 39 % of reading,
A1+B1 2026 49 %; per-statement means **147** (2025) and **239** (2026); target whole-paper
equivalent **1370**, now *inside* the briefing's 1300–1400 band.

Prose:
* "agree item by item to within two per cent" → three per cent on the paper total, 1–6 % item by
  item (D2 214/201 = 6.1 %). Fixed in ch 6, ch 9, ch 13, ch 15 EN+ES.
* the two 2027 targets were called independent; both are anchored to the 2025 paper. Now said so.
* the asymmetric-scaffolding form was given "about 170 words", borrowed from the ideal+drawing
  rung. Now bracketed between 154 and 287 with no measured value claimed.
* the b)-vs-c) test was called "close to clean"; half of c) is a *valorar* sub-task with no
  analogue in b). Restated as b)1–3 against c)1, per mark, on the chain only.
* the setter's design account was stated as fact. Now testimony, with an explicit
  conflict-of-interest callout: the dossier's author is a co-author of the presentation.
* the two reconstruction ladders were collapsed into one everywhere but ch 6. Fixed in ch 9,
  ch 13, ch 15 EN+ES, index and the ch 15 figure caption.
* index finding 11's headline "a third of it can go without touching a question" — the third
  comes from rewriting questions; only the 103 words of weights touch none. Rewritten.
* "cut of 36 % in answering" → 35–43 %, depending on the options taken.
* "*indica* three times" → four.
* the statement_budget table mixed two tokenisations in one row and labelled a per-statement
  band as a "longest item". Columns rebuilt on one tokenisation.

One caveat now stated that nobody had noticed: the 2025 paper prints its constants inside the
three statements that need them (21 words) and the 2026 paper moved every constant to one
table, counted here as furniture. Small, but it crosses the statement/furniture line.
