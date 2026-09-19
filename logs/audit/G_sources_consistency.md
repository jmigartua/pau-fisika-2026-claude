# Audit G — sources, citations, cross-chapter consistency, site integrity (agent report, verbatim)

# Sourcing and consistency audit — `/home/claude/work` (PAU Física 2026 Quarto site)

Read-only audit, 19 Sep 2026. No files were edited. All paths below are under `/home/claude/work/`.

## Ranked summary

| # | Severity | Finding | Where | Fix |
|---|---|---|---|---|
| 1 | **Critical** | `_site/` and `docs/` (the deployed GitHub Pages copy) were rendered at **09:33 on 19 Sep**; chapters 06 and 10 were rewritten at **16:03**, and figures 16–24 were generated at **16:51–16:53**. The rendered chapter 6 contains only 4 sections (hypotheses, institutional record, asks, design) — none of "Is the drift real?", the Basque 2024 signal, PISA, slope comparison, reading load, PAU 2027, shape/locus, reference frames, analysis path — and no **Disclosure** callout; rendered chapter 10 lacks "Provenance and interest" and "The figures". `_site/plots/` holds only figs 01–15. | `_site/`, `docs/` | `quarto render && quarto render onepage.qmd && rm -rf docs && cp -R _site docs && cp onepage.html docs/ && touch docs/.nojekyll` (per `DEPLOY_GITHUB_PAGES.md`). |
| 2 | **Critical** | Chapter 6 slope table (lines 87–98) is **stale relative to `data/analysis/slope_compare.json` and fig 22**. `scripts/16_slope_compare.py` filters PISA years `>= 2012` with no upper bound; after `15_pisa_link.py` gained PISA 2025 and everything was re-run at 16:53, the PISA fits use 5 rounds. Text says PISA-Spain −0.147 [−0.381, +0.086], PISA-Euskadi −0.245 [−0.785, +0.296], "four PISA rounds", "every interval includes zero", slope differences p = 0.48/0.67, ratio 1.72 vs 1.66. JSON: PISA-Spain **−0.155 [−0.256, −0.054], p = 0.016**; PISA-Euskadi **−0.327 [−0.603, −0.051], p = 0.033**; differences 0.064 (p = 0.33) and 0.169 (p = 0.35); ratios 1.72 vs **2.10**. Two of four intervals now exclude zero, which reverses the section's stated conclusion. The script's own caption string (line 162–163) still says "2012–2022, four rounds", and `analysis_path.json` step 10 hard-codes "every interval includes zero". | `chapters/06-interpretation.qmd:87-98`, `scripts/16_slope_compare.py:59-75,162`, `scripts/11_analysis_path.py` | Either add `PISA_TO = 2022` in script 16 (if 2025 is meant to be held out for the 2027 estimator) or rewrite the section to the 5-round numbers; regenerate fig 18/22; update caption. |
| 3 | High | `sources/pisa/` (4 INEE workbooks feeding scripts 15–18, chapter 6 and figs 21–24) is **not in the source registry** (no URL, size or hash). Chapter 10 says "every figure is regenerated from those files", chapter 8 claims to register "every file … used". | `sources/source_registry.csv`, `scripts/05_registry.py` | Add the four PISA files (with INEE URLs) to `URLS` in `05_registry.py`. |
| 4 | High | Provenance: the Disclosure (ch 6) and provenance note (ch 10) say "the author … was involved in setting the 2026 Basque Física paper". Chapter 12 repeatedly cites "the coordinator, who has held the Física coordination since the 2018 edition" in the third person as testimony, chapter 1/9 say the theory list was "supplied by the coordinator"/"the user", and the index byline says "prepared for Josu M. Igartua" and calls the study "independent". If author = coordinator = user, no chapter says so; chapter 12's "testimony of the coordinator" should be identified as the author's own account. Also ch 10 line 15 "Nothing in the analysis depends on privileged access … every paper used is public" sits beside ch 12's use of a non-public official list. | `chapters/06-interpretation.qmd:103-105`, `chapters/10-reproduce.qmd:11-15`, `chapters/12-ehu-paper-history.qmd:11,13,97`, `index.qmd:5` | One sentence in ch 6/10 stating the identity; reword ch 12 "coordinator's account" as first-person disclosure. |
| 5 | High | Chapter 6 "How this reading was arrived at" says "**four of its six steps**" then narrates **Steps 1–7**; `analysis_path.json`/fig 18 now carry **12 steps** (8 take-up, 9 PISA, 10 slopes, 11 PAU 2027, 12 reading load). Text and figure disagree. | `chapters/06-interpretation.qmd:210-224` | Extend the narrative to steps 8–12 (or say the figure carries the later steps). |
| 6 | High | Chapter 6 mean-axis normality numbers (line 166: "Shapiro–Wilk p = 0.00017, Anderson–Darling A² = 2.06 against 0.77") do not match `shape_locus.json → mean_axis` (shapiro_p = 0.0047, A² = 0.94, crit = 0.746). Note the JSON's mean_axis shapiro_p is byte-identical to `y_normality_excl_covid_plateau.ratio.shapiro_p`, which suggests a copy bug in `09_shape_locus.py`. | `chapters/06-interpretation.qmd:166`, `scripts/09_shape_locus.py` | Check the script; re-quote. |
| 7 | Medium | "+0.5 to +1.1" range for the six risers (index :61, ch 3 :21, ch 6 :13) includes Andalucía, whose change is **+0.17** (regions table). Actual range +0.17 to +1.13. | `index.qmd:61`, `chapters/03-spain-2026.qmd:21`, `chapters/06-interpretation.qmd:13` | "five of them by +0.5 to +1.1, Andalucía by +0.17". |
| 8 | Medium | Madrid delta appears as **+1.1** (index :67, `subjects_delta.md`: 5.6 chart → 6.7) and **+1.05** (README, ch 11 :62, `regions_2026.md`: 5.65 ministry → 6.70). Two baselines in two tables. | `data/tables/subjects_delta.md`, `data/tables/regions_2026.md`, `index.qmd:67` | Pick one baseline (ministry 5.65) or footnote both. |
| 9 | Medium | "7 of the 170 changes were as negative" but only six are named (index :63, ch 2 :53); the seventh is **Cantabria 2025 (−1.51)** per `annual_changes_all_ccaa.csv`. | `index.qmd:63`, `chapters/02-euskadi.qmd:53` | Add Cantabria 2025. |
| 10 | Medium | Chapter 1 :61 "**No archive or mirror of a blocked site was used**" contradicts the same paragraph (Extremadura 2026 from FiQuiPedia GitLab because "uex.es behind WAF"; Cataluña 2026 criteria from the Betevé mirror). | `chapters/01-data-hunt.qmd:61` | "No Internet-Archive/Wayback copy was used" (which is what ch 9 :56 describes). |
| 11 | Medium | Dates: index, ch 01, 06, 08, 09 are `date: 2026-09-18` but contain 19 Sep work (findings 6–7; "added 19 September"; PISA section written "eleven days" after 8 Sep = 19 Sep). Footer says "prepared 18 September". Ch 9 subtitle "What was done on 18 September". | `index.qmd:7`, `chapters/01,06,08,09`, `_quarto.yml:90` | Date to 2026-09-19 or use `date-modified`. |
| 12 | Medium | `onepage.qmd` (09:34) is stale: 0 mentions of PISA/Disclosure, only figs 01–15; `onepage.html` (16:04) is a render of that stale source. | `onepage.qmd`, `onepage.html` | Regenerate onepage.qmd from the chapters before rendering. |
| 13 | Low | Stale counts: ch 8 description "161 raw files" (registry = **162**; the coordinator's theory list was added later — even the 09:33 render already showed 78 `exams_ehu_hist` rows); README :23 and ch 9 :105 "`sources/raw/` 37 downloaded documents" (actual **41**); ch 9 :106 lists only scripts 01–05; ch 9 :107 "plots/: ten figures" (24); ch 10 :47 "All ten figures were … inspected"; ch 10 :101 "shared by the three scripts" vs README :44 "the four plotting scripts" (there are 12 plotting scripts); ch 8 :14 caption "Files in `sources/raw/` and `sources/ministry/`" (table also lists exams/, exams_ehu_hist/). | as listed | Update numbers. |
| 14 | Low | `plots/fig19_conditional_top.png` (script 12) is generated, listed in ch 10 :99 and README ("twenty-four figures"), but **included in no chapter** (orphan; chapter 6 uses panel c of fig 16 instead). `data/tables/exam_coding_full.md` is also never included. | `chapters/06-interpretation.qmd` | Include fig 19 in the "Basque signal" subsection, or drop it from the counts. |
| 15 | Low | Ch 12 heading "**Three** formats in sixteen years" vs table caption "The **four** formats" and 4-row table. Ch 12 :37 "photographic camera and Biot–Savart title once each" — Biot–Savart was set **twice** in 2010–2024 (once in 2012–2024), while the other counts in the sentence use the 2010–2024 column. | `chapters/12-ehu-paper-history.qmd:15,20,37` | Align. |
| 16 | Low | Ch 6 :146 orphan sentence "That round has since been published, and [the section below](#what-pisa-2025-says-about-pau-2027) reads it." sits **after** that section, between it and H5. | `chapters/06-interpretation.qmd:146` | Delete or move to the end of the PISA-instrument section. |
| 17 | Low | Reading-load section uses "eight communities" (CLM excluded because its papers are abridged transcripts) while every other exam statement says nine; the exclusion is never stated. | `chapters/06-interpretation.qmd:113,119,121` | Add "(Castilla-La Mancha has no archived PDF)". |
| 18 | Low | `shape_locus.json → presented_2015_2025.2015 = 30839` (specific phase) while the fig 16 caption and ch 6 say 37,661 pooled and claim the values are read from the JSON. | `scripts/09_shape_locus.py:107` | Pool phases in the script. |
| 19 | Low | Bibliography: `ruizdegauna2013comparado` URL (`ehu.eus/ikastorratza/11_alea/pau.pdf`) returns **404**; `ruizdegauna2011matematicas` and `mengual2019criterios` have no URL/DOI; `uma2025ponencia` is never cited; `ruizdegauna2013selectividad` DOI reads `RE-2011-362-159` for a 2013 article (RdE convention, but verify). | `references.bib` | Fix URL, add locators, cite or drop UMA. |
| 20 | Low | "Chapter N" in prose refers to file numbers, but `number-sections: false` and the sidebar (Findings → 02,03,04,05,06 → 11,12 → 01,07 → 08,09,10) shows no numbers, so a reader cannot map "Chapter 11" to "The papers themselves" (7th sidebar item). | `_quarto.yml`, all chapters | Use titles in links (as ch 6 partly does) or number the sidebar. |

---

## 1. Citations and bibliography

**Keys.** 44 distinct keys cited across `index.qmd` + `chapters/*.qmd`; all 44 exist in `references.bib` (45 entries: 17 `@article`, 27 `@misc`, 1 `@phdthesis`). Chapter 8's "45 entries: 10 new, 9 classic, 26 official/press" is correct.

- **Cited but missing from bib:** none.
- **In bib, never cited:** `uma2025ponencia` (the UMA ponencia is mentioned in prose in ch 1/9 and its PDF is in `sources/raw/`, but never cited with `@`).

**Fields.** Every entry has author/organisation, title and year. Locator gaps:

| Key | Problem |
|---|---|
| `ruizdegauna2011matematicas` | no URL and no DOI (Sigma 36) |
| `mengual2019criterios` | no URL and no DOI (PNA 13(2)) |
| `ruizdegauna2013selectividad` | DOI `10.4438/1988-592X-RE-2011-362-159` — "2011" in the DOI of a 2013 vol. 362 paper; RdE does use acceptance year, but worth verifying |
| `unizar2025asig` | `year = 2026` for "Resultados PAU por asignaturas 2025" (probably the page date; harmless but odd) |
| `ehu2026notak` | title is Basque-only ("USaP kalifikazioen inguruan"); fine but a reader gets no Spanish/English gloss |
| all `@misc` dashboards (`uclm_powerbi`, `ull_powerbi`, `ulpgc_powerbi`) | URL is the landing page, not the report; acceptable, and `howpublished`/note give the report name |

No URL is malformed (all match `https?://\S+`).

**URL spot-check (curl -sI, 12 URLs):**

| Status | URL |
|---|---|
| 200 | ehu.eus `20260706-notak-po` (EHU deck) |
| **403** | govern.cat `Dossier_resultats PAU 2026.pdf` (bot block; not circumvented) |
| 200 | comunidad.madrid `presentacion-resultados-pau-2026_vd.pdf` |
| 200 | euskadi.eus `resultados-escolares-Todo-2024-2025.pdf` |
| 200 | gobiernodecanarias.org Física acta 9 Oct 2025 |
| **403** | mdpi.com `2254-9625/15/6/102` (bot block) |
| 200 | revistas.uned.es Educación XX1 42170 |
| 200 | boe.es RD 534/2024 |
| 200 | unavarra.es `Informe_PAU_2024-25.pdf` |
| 200 | theconversation.com Sánchez-Tarazaga piece |
| 200 | ull.es/estadisticas/pau/ |
| **404** | ehu.eus `ikastorratza/11_alea/pau.pdf` (`ruizdegauna2013comparado`) — dead link |

## 2. Registry

- `sources/source_registry.csv`: **162 rows** (raw 41, ministry 3, exams 40, exams_ehu_hist 78). `data/tables/source_registry.md`: 169 table rows = 162 files + 7 dashboard/page rows (the `DASH` list in `05_registry.py`).
- **All 162 files exist; byte size and SHA-256 recomputed and match for all 162** (0 mismatches).
- **Not registered but used by the analysis:** `sources/pisa/` (4 workbooks: pisa2015 `.xls`, 2018/2022/2025 `.xlsx`) — inputs of scripts 15, 17, 18 and chapter 6. Also unregistered (acceptable, derived): `sources/text/*.txt`, `sources/exams/*.txt`, `exams_ehu_hist/*.txt`, `MANIFEST.txt`, `urls_tried.log`, the two extracted `and_20xx_zip/` trees, `sources/agent_extractions/*.csv`.
- **Counts in prose vs registry:** ch 9 "40 files" in `sources/exams/` ✓ (40 registered: 36 PDF + 2 zip + 2 transcripts); ch 1/9 "77 PDFs" downloaded from ehu.eus ✓ (78 registered = 77 + coordinator's theory list; ch 1 correctly separates them); ch 8 "44 on 18 September" ✓ (41 + 3); ch 8 "161 raw files" ✗ (162); README/ch 9 "37 downloaded documents" in `sources/raw/` ✗ (41).
- **URLs:** all well-formed except the theory list (empty URL, retrieval "provided by the coordinator (not published online)" — correct). Seven rows carry a *landing page* rather than a file URL (`can_acta2… → gobiernodecanarias.org/`, `cat_Mitjanes… → universitats.gencat.cat/`, `and_uca… → webacceso.uca.es/`, `and_us… → us.es/pevau/coordinacion`, `mad_uam_* → uam.es/…/comisiones-materia`, `gal_ciug_modelos2027/home → ciug.gal/`, `cyl_uva… → pruebasdeacceso.uva.es/9.resultadosestadisticos/`) — resolvable but not reproducible as a download.
- **Mirror flags:** correctly flagged in the `retrieval` column — `cat_2026_ord_crit.pdf` "Betevé mirror of the official criteria (gencat pau_fisi26jt.pdf returns 404)"; `ext_2026_ord.pdf` / `ext_2026_ord_crit.pdf` "FiQuiPedia GitLab archive (uex.es behind WAF)"; `val_2025_ord.pdf` / `_crit` / `_reserva` "FiQuiPedia GitLab archive (official file overwritten at gva.es; byte-identical to the angelcuesta.com copy)". `val_2025_ord_sol_angelcuesta.pdf` flagged "unofficial worked solutions (not used)". Chapter 1 :61 and chapter 9 :56 describe the same routes — but ch 1's closing sentence "No archive or mirror of a blocked site was used" contradicts the FiQuiPedia route for WAF-blocked uex.es (finding 10).

## 3. Cross-chapter consistency

| Quantity | Status |
|---|---|
| 2026 Euskadi mean 3.99 / 3.98 | consistent: 3.99 everywhere; 3.98 only as the press variant (ch 1 :79, ch 9 :11) |
| 2025 mean 5.47, pass 62.3 %, 2026 pass 39.8 %, 24.5 % ≤ 2 (2025: 10 %), 3.2 % zeros, N = 2 066 | consistent across index, ch 1, 2, 4, 5, 10, README, tables |
| 14 of 17 fell in 2025, mean −0.81, Euskadi −0.62 | consistent (index, ch 2, 3, 6, 12, README; `results.json` −0.81) |
| "six of nine rose" | consistent; but "**+0.5 to +1.1**" (index :61, ch 3 :21, ch 6 :13) excludes Andalucía +0.17 (finding 7) |
| Madrid delta | **+1.1** (index :67, `subjects_delta.md`) vs **+1.05** (README, ch 11, `regions_2026.md`, `exam_change_vs_grade.csv`) (finding 8) |
| "7 changes as negative" | 6 named; Cantabria 2025 −1.51 missing (finding 9) |
| Reference frames −0.65 / +0.17 / +0.02 / −1.48 / −1.93, baseline 5.92 | match `reference_frames.json` (−0.647, +0.169, +0.021, −1.932, 5.922). Ch 6 :186 "2022, 2023 and 2024 are all about +0.65" — JSON gives +0.62, +0.53, +0.50 |
| Beta fits (a = 2.0/1.6; 1.27/1.81; median 3.8; >7: 30 → 15 %; >9: 6 → 2 %; SD 2.4 → 2.5; [0,5) ≈ 65 %) | match `beta_fits.md` / `results.json` |
| PISA numbers (+6.2/+6.4/+9.2; −22.6 vs −3.7; −9.7/+4.1/−5.0; 26 vs 12; L5–6 3.25/3.87/3.32 vs 4.98/4.18/4.92; 2025: 458.5/477.1, −18.6, 1.83 %; reading 491.4 → 419.1, −4.1 → −32.2) | match `pisa_link.json` / `reading_load.json` |
| Slope table | **does not match** `slope_compare.json` (finding 2) |
| Analysis-path steps | 6/7 in text vs 12 in JSON/fig 18 (finding 5) |
| Mean-axis normality | mismatch (finding 6) |
| Cohort drift (−0.071/yr, R² 0.75, p 0.058; 5.20 vs 5.67; r −0.064 p 0.525 n 102; take-up 0.222 → 0.241, r −0.020 p 0.839) | match `cohort_drift.json`, `take_up.json` |
| Conditional ratio (+0.64 SD 2016–23; 2024 −0.96; 2025 −0.52; 0.353 → 0.466 → 0.331; t 7.14, p 4e-11; ULL +1.05, ULPGC +0.53; EHU model −0.05) | match `shape_locus.json` / `conditional_top.json` |
| PAU 2027 (−0.36; 0.855; ±2.37; 6.5×; 1.23; 5.11 [2.74, 7.48]; 3.63 [1.26, 6.00]) | match `pau2027_estimator.json` |
| Reading load (r −0.84 p 0.008; ρ −0.76 p 0.028; +0.87; 39.5 %, 1,452 → 2,026; Madrid 4,070, Asturias 899) | match; "eight communities" = nine minus CLM, unexplained (finding 17) |
| The two 146s | **coincidence, both correct**: `exam_coding_2025_2026.csv` has 146 rows (items, ch 11); `ehu_problem_inventory_2010_2026.csv` has 146 rows (problems, ch 12). Worth a footnote so readers do not assume a copy error. |
| 22 titles / 118 questions / 34 papers / 30 papers with theory | consistent everywhere ("21" appears nowhere); `ehu_theory_inventory.csv` 118 rows, 22 titles |
| Formats "three" vs "four" | ch 12 heading vs caption/table (finding 15) |
| Dates | 18 Sep front-matter on chapters with 19 Sep content (finding 11); ch 6 :125 "eleven days before this chapter was written" implies 19 Sep |
| "Chapter N" links | every `[Chapter N](0N-….qmd)` points at the right file; index "Chapters 2–6", "Chapters 8–9" fine. But the numbers are invisible in the UI (finding 20) |
| Site self-description | README: 12 chapters, 24 figures, 45 bib entries ✓; ch 10 "twenty-four figures" ✓ but only 23 are included (fig 19 orphan); ch 9 :107 "ten figures", :106 scripts 01–05 only, ch 10 :47 "All ten figures" — stale; `PROJECT_INDEX.md` "ten figures" — stale |
| Minor wording | index :53 "four of those (… La Rioja's 2010–2022 series)" counts a non-2026 series among "nine communities … with a 2026 mean" |

## 4. Internal links, labels, includes, figures

- **Links:** all 40-odd `[text](0N-….qmd)` / `(chapters/…qmd)` links resolve. The two same-file `#…` anchors in ch 6 (:51 `#what-to-ask-for-in-order-of-value`, :202 `#the-hypotheses-one-by-one`) rely on Quarto auto-ids of existing headings — fine. `10-reproduce.qmd:13 → 06-interpretation.qmd#how-much-of-the-paper-is-reading` — explicit id exists.
- **`@fig-`/`@tbl-` references:** every referenced label is defined **in the same chapter**; no cross-chapter `@fig`/`@tbl` references exist (good — none would resolve). Ch 6 :45 references `@fig-locus` ~110 lines before its definition (forward ref, resolves).
- **Includes:** all 26 `{{< include ../data/tables/*.md >}}` files exist. Orphan table: `data/tables/exam_coding_full.md`.
- **Images:** all 23 `![](../plots/figNN.png)` files exist. **Orphan:** `plots/fig19_conditional_top.png` (+ .svg). Figure order in ch 5 is 07, 08, 10, 09 and in ch 6 is 20, 21, 22, 24, 23, 16, 17, 18 (numbering follows script order, not reading order — cosmetic).

## 5. `_quarto.yml`

- **Sidebar** lists all 12 chapters + index (order: 02, 03, 04, 05, 06 · 11, 12 · 01, 07 · 08, 09, 10). Nothing missing. Sidebar/navbar titles differ from the qmd titles by design.
- **Navbar:** index, 02, 03, 08 — all resolve.
- **Bibliography/CSL:** `references.bib` and `apa.csl` exist at root (a duplicate `apa.csl` also sits in `sources/`).
- **Render list:** `index.qmd`, `chapters/*.qmd` — `onepage.qmd` deliberately excluded (documented in `DEPLOY_GITHUB_PAGES.md`). Resources `plots/*`, `data/analysis/*.csv`, `data/*.csv` — note the `analysis/*.json` files that ch 6/10 point readers to (`shape_locus.json`, `results.json`) are **not** published as resources.
- `styles-dark.scss` exists and is listed in ch 9 :103 but is not referenced by `_quarto.yml` (theme uses `styles.scss` for both schemes).
- `number-sections: false` → prose "Chapter N" has no on-page counterpart (finding 20).

## 6. Dates and provenance

- Front-matter `date: 2026-09-18` on index, 01, 06, 08, 09 vs 19 Sep content (details in finding 11); 11 and 12 correctly dated 19 Sep.
- **Disclosure (ch 6 :102–105) vs provenance note (ch 10 :9–15):** substantively identical (author helped set the 2026 paper; expanded the second exercise's statement because a competency *saber básico* entered for the first time; cross-link ch 6 → ch 10 works). Disagreement is with chapter 12 and the index byline, not between the two notes (finding 4).
- **Scripts:** README table lists all 18 numbered scripts + `plot_style.py`, `pxparse.py`. README rebuild chain and ch 10 rebuild block both list 17 scripts in the same order: 01, 02, 03, 04, 07, 08, 09, 10, 11, 12, **14, 13**, 15, 16, 17, 18, **05** — `14_take_up` precedes `13_cohort_drift` ✓ (13 reads `take_up.json`) and `05_registry` is last ✓. `06_poll_watchlist.py` is (reasonably) omitted from the chain. Dependency check from the scripts' own file reads: 09 must precede 15 (15 reads `shape_locus.json`) ✓; 15 precedes 16/17/18 ✓; 07 precedes 18 (reads `exam_coding_2025_2026.csv`) ✓; 11 reads only `results/reference_frames/shape_locus.json` so its position is fine, but its steps 8–12 are hard-coded prose, not read from the later JSONs — which is why step 10 still says "every interval includes zero" after script 16's numbers changed. Ch 10's data dictionary (lines 51–69) lists only day-1 files (no exam_*, ehu_*, pisa_*, or analysis JSONs).

## 7. Rendered site

- `_site/` exists with `chapters/11-exam-content.html` and `12-ehu-paper-history.html`; `docs/` is a byte-identical copy (+ `.nojekyll`, `onepage.html`).
- **Both rendered 19 Sep 09:33.** Sources newer than the render: `chapters/06-interpretation.qmd` (16:03), `chapters/10-reproduce.qmd` (16:03), all `data/tables/*.md` (16:45–16:53 via re-run), `plots/fig16–24` (16:51–16:53), `data/analysis/*.json` (16:45–16:53), `sources/source_registry.csv` (16:53), README (16:03). Chapters 01–05, 07–09, 11, 12 and index have mtime 09:34:14 (one minute after the render; likely a copy — content appears to match, e.g. the rendered ch 8 already shows the 78 `exams_ehu_hist` rows and the "161" wording).
- Rendered ch 6 = day-1 version (4 sections; zero occurrences of "PISA", "Disclosure", or `fig16`–`fig24`); rendered ch 10 lacks "Provenance and interest" and "The figures"; `_site/plots/` has 30 files = figs 01–15 only. **The deployed site is missing figures 16–24, the disclosure, and ~60 % of chapter 6.**
- `onepage.html` (16:04) is fresher than `docs/onepage.html` (09:33) but was built from the stale `onepage.qmd` (09:34; no PISA/Disclosure, figs 01–15 only).

## Notes on things that check out

Registry hashes (162/162), all citation keys, all internal links, all includes and included images, the EHU headline numbers, the 2025/2026 regional table, beta fits, PISA levels, cohort-drift, conditional-ratio, reference-frame and PAU-2027 scalars all agree with their JSON/CSV sources; the "146 items" vs "146 problems" is a genuine coincidence of two different files, not an error.
</agent-message>