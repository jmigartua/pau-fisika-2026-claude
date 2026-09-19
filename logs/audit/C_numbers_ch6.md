# Audit C — numeric/statistical verification of Chapter 6 (agent report, verbatim)

# Audit of `chapters/06-interpretation.qmd` — numeric and statistical claims

Everything below was recomputed from `/home/claude/work/data/...`, `/home/claude/work/sources/pisa/*.xls(x)` and `/home/claude/work/sources/exams/*.pdf|.txt` with independent Python/pdftotext runs (no files edited). Verdicts: **OK** = reproduces; **IMPRECISE** = right in substance, wrong in wording/rounding; **STALE** = was true of an earlier data state, false now; **ERROR** = wrong; **UNVERIFIABLE** = not checkable from the repo.

## Claim-by-claim table

| # | Section | Claim (≤ 15 words) | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 1 | H1 | 2025 fell in 14 of 17, −0.81 avg; Euskadi −0.62 | 14/17, −0.81, PV −0.62 | OK | ministry panel, ordinary/specific, 2024→2025 |
| 2 | H1 | "at least six of nine rose by +0.5 to +1.1" in 2026 | 6 rose: +0.17, +0.51, +0.80, +0.94, +1.05, +1.13 | IMPRECISE | Andalucía rose only +0.17; five rose by +0.5–1.1 |
| 3 | H4 | Presentation fell 6 % from 2025 | 2189→2066 = −5.6 % | OK | euskadi series |
| 4 | H4 | School–PAU gap 1.62 (2025) → 3.10 (2026) | 7.09−5.47=1.62; 7.09−3.99=3.10 | OK | 7.09 itself not checkable here |
| 5 | Drift | Física presented grew 30 %, 37,661 → 49,010 | pooled: 37,661 → 49,010 (+30.1 %) | OK | pooled phases, ordinary |
| 6 | Drift | Specific-only count understates 2015 by ~18 % (30,839 vs 37,661) | 30,839; 1−30839/37661 = 18.1 % | OK | but `shape_locus.json` still records `presented_2015 = 30839` (script 09 uses specific-phase `hist`) — JSON contradicts fig-16 caption |
| 7 | Drift | 2015–19 trend −0.071/yr, R² 0.75, p 0.058 | −0.0710, R² 0.748, p 0.058 | OK | n = 5 year-points, unweighted mean of 17 communities |
| 8 | Drift | Projection 5.20 vs actual 2025 5.67 (+0.47) | 5.201 vs 5.672, +0.471 | OK | "5.67" is the unweighted 17-community mean; Ministry Total is 5.65, presented-weighted 5.73 |
| 9 | Drift | Undercounted dilution r −0.212, p 0.032 | −0.212, p 0.032, n 102 | OK | |
| 10 | Drift | Pooled dilution r −0.064, p 0.525, n 102 | −0.064, p 0.525, n 102 | OK | |
| 11 | Drift | Take-up 0.222 → 0.241, +8 % relative | 0.2224 → 0.2405, +8.2 % | OK | national linear trend in take-up is itself p = 0.044 (not mentioned) |
| 12 | Drift | Take-up vs mean r −0.020, p 0.839 | −0.020, p 0.839, n 102 | OK | |
| 13 | Drift | Conditional ratio trend −0.0029/yr, p 0.082 | −0.00288/yr, p 0.082 (6 year-means) | OK | on 102 region-years p = 0.235 |
| 14 | Drift | "−0.07/yr would need about fifteen clean years" | with observed residual σ ≈ 0.11 marks, ~6–7 clean years give 80 % power; the 5 pre-COVID points already give p 0.058 | IMPRECISE | unsupported rule of thumb |
| 15 | Basque signal | Euskadi conditional +0.64 SD above field, mean 2016–2023 | 0.642 | OK | |
| 16 | Basque signal | 2024 −0.96; 2025 −0.52; 2017 +0.70; 2020 −0.82 | −0.960, −0.523, +0.704, −0.816 | OK | |
| 17 | Basque signal | "two-year turn away from eight consecutive years on the other side" | 2016–23 values: +1.31, +0.70, +0.70, +1.12, **−0.82, −0.33**, +0.68, +1.78 (2015 also −0.10) | ERROR | 2020 and 2021 are negative; only 6 of 8 positive; the chapter's own PISA table shows 2020 = −0.82 |
| 18 | PISA | 2006 +6.2, 2009 +6.4, 2012 +9.2 | 6.25, 6.44, 9.21 | OK | 2015 workbook, `Tabla 2.7`, rows "País Vasco"/"España", cols 8/6/4 (P. Media) — **the back-series is in the repo** (INEE 2015 report carries 2006–2015 by community) |
| 19 | PISA | 2015 −9.7; 2018 +4.1; 2022 −5.0 | −9.73 (2015 `Tabla 2.7` col 2: 483.06/492.79); +4.12 (2018 sheet `2.3` col 2: 487.38/483.25); −5.02 (2022 sheet `2.21` col 2: 479.51/484.53) | OK | |
| 20 | PISA | 2012→2015: PV −22.6, Spain −3.7 | −22.60, −3.66 | OK | |
| 21 | PISA | Decade to 2022: PV −26, Spain −12 | 2012→2022: −26.14, −11.91 | OK | correct rounds |
| 22 | PISA | Top 5–6: PV 3.25/3.87/3.32 vs ES 4.98/4.18/4.92 | 2015 `Tabla 2.2` cols 14+16: 3.135+0.115=3.25 / 4.673+0.306=4.98; 2018 `2.9` cols 14+16: 3.874 / 4.184; 2022 `2.24` cols 14+16: 3.315 / 4.919 | OK | |
| 23 | PISA | Basque top share "below Spain's in two rounds of three" | below in **all three** (3.87 < 4.18 in 2018 too) | ERROR | probably conflated with the mean gap sign |
| 24 | PISA | OECD top 7.47 % in 2022; PV below OECD in all | 2022 `2.24`: 6.285+1.184=7.47; 2015 7.72; 2018 6.75 | OK | |
| 25 | PISA | Matched cohorts −9.7/+0.70, +4.1/−0.82, −5.0/−0.96; 1 of 3 agree | reproduced | OK | |
| 26 | PISA fig-21 caption | "every PISA round from 2006 to 2022" | series and script now include 2025 | STALE | caption predates 2025 |
| 27 | Slopes | Student SD 2.34 = median of "thirteen published regional SDs" | median 2.343 of 13 values — **all from Comunitat Valenciana** (SUV pooled ×3 + UA/UJI/UMH/UPV/UV × 2025, 2026) | IMPRECISE | one region, five universities; "regional" is misleading |
| 28 | Slopes | PISA SD ≈ 90 from p10–p90 of 2015 tables | 2015 `Tabla 2.6` Spain p10 373.99, p90 604.98 → 231.0/2.563 = 90.1 | OK | PV gives 86.7, OECD 96.4 |
| 29 | Slopes | Table: PAU ES −0.092 [−0.251,+0.068]; PAU PV −0.157 [−0.601,+0.286] | same (n = 6) | OK | |
| 30 | Slopes | Table: PISA ES −0.147 [−0.381,+0.086]; PISA PV −0.245 [−0.785,+0.296] | **n = 4 (2012–2022)** reproduces exactly; **n = 5 (2012–2025, current CSV/JSON)**: ES −0.155 [−0.256, −0.054] p 0.016; PV −0.327 [−0.603, −0.051] p 0.033 | STALE | see known issue below |
| 31 | Slopes | Differences +0.06/+0.09, p 0.48/0.67 | n=4: +0.056/+0.087, p 0.48/0.67. n=5: +0.064/+0.169, p 0.33/0.35 | STALE | |
| 32 | Slopes | Ratio Euskadi/Spain 1.72 (PAU) vs 1.66 (PISA), "within 4 %" | n=4: 1.72/1.66. n=5: 1.72/**2.10** (22 % apart) | STALE | |
| 33 | Slopes | "every interval includes zero"; "four PISA rounds" | n=5: both PISA intervals exclude zero; five rounds | STALE | fig-22 PNG regenerated 16:53 today with n=5 while chapter (16:03) still says four |
| 34 | Reading | PV reading 491.4 → 419.1 (−72), science −24.5, gap −4.1 → −32.2 | 2015 `Tabla 2.11` col 2 (491.448; ES 495.576) → 2025 `Figura 2.14` col 1 (419.110; ES 451.356): −72.3; science 483.06→458.53 = −24.5; gaps −4.13 → −32.25 | OK | "decade to 2025" = 2015→2025, consistent for both |
| 35 | Reading | No 2018 reading point in Spanish report | 2018 workbook sheets: maths and science only | OK | |
| 36 | Reading | r −0.84, p 0.008; ρ −0.76, p 0.028; n 8 | −0.8435, p 0.0085; ρ −0.762, p 0.028 | OK | reproduces from the .txt files and from fresh `pdftotext` (identical counts) |
| 37 | Reading | "Stripping rubric and constants leaves it at −0.84" | −0.844 with the script's BOILER regex | OK-as-computed | the regex does **not** strip Madrid's embedded solutions or Valencia's second language (see 39–40) |
| 38 | Reading | PV lengthened 39.5 %, 1,452 → 2,026 | 1,452 → 2,026 = +39.5 % (raw). Statement text only (bilingual instructions and 2026 constants table removed): 1,176 → 1,769 = **+50.4 %**; instructions kept, constants removed: +34.9 % | IMPRECISE | direction and magnitude hold; 2026 prints 6 problems vs 7 in 2025 yet is longer |
| 39 | Reading | Madrid 3,737 → 4,070 (+8.9 %); "4,070 words … more choice prints more text" | Madrid PDFs embed *Criterios específicos* + full *Soluciones*: statement text is **1,127 → 1,093 (−3.0 %)** | ERROR | ~70 % of the Madrid count is solutions; the chapter's explanation (choice) is wrong; Madrid's true change has the opposite sign |
| 40 | Reading | Valencia 2,485 → 2,325 (−6.4 %) | PDFs are bilingual (Castellano pp.1–2 + Valencià pp.3–4) both years; Spanish half 1,228 → 1,152 (−6.2 %) | OK | contamination symmetric, change unaffected |
| 41 | Reading | Correlation after removing contamination | Madrid+Valencia fixed: **r −0.92 (p 0.001), ρ −0.86 (p 0.007)**; + PV constants removed: r −0.93; statement-text-only for all eight: r −0.86 (p 0.006), ρ −0.905 (p 0.002); excl. PV (fixed counts): r −0.88 (p 0.008) | — | the association strengthens once the contaminated components are removed |
| 42 | Reading | Competency change vs length r +0.87; −0.84 vs −0.47 | 0.872 (n 8); −0.468 (n 9, `exam_correlations.json`) | OK | different n |
| 43 | PISA 2025 | PV 458.5, ES 477.1, OECD 481.9, gap −18.6 | `Figura 2.1` col 1 (key col 0): 458.53 / 477.13 / 481.91; −18.60 | OK | |
| 44 | PISA 2025 | "more than double the previous worst" gap | 18.6 / 9.7 = 1.92 | ERROR | less than double |
| 45 | PISA 2025 | Top share halves 3.32 → 1.83 %; Spain "holds near 4.2 %" | `Figura 2.4` cols 13+15: PV 1.658+0.175 = 1.83 (−45 %); ES 3.851+0.357 = 4.21 (from 4.92 in 2022, −0.7 pp) | IMPRECISE | "halves" ≈ ok; Spain fell 14 %, "holds" is generous |
| 46 | 2027 | 21.0 pts = 0.233 SD; ×2.34 = 0.546; ×2/3 = −0.36 | −20.98/90 = −0.2331; −0.5455; −0.3637 | OK | |
| 47 | 2027 | Decade 2012→2025 = 1.23 marks | (458.53−505.65)/90×2.34 = −1.225 | OK | |
| 48 | 2027 | Year-to-year SD 0.855; 2-yr band ±2.37; 6.5× | SD of 15 changes 2011–2025 = 0.8549; 1.96×0.855×√2 = 2.370; 2.37/0.364 = 6.5 | OK | SD is dominated by 2012 (+2.05) and COVID (+1.24, −1.63); excluding 2020–22 it is 0.72 (band ±2.00) |
| 49 | 2027 | Central 5.11 / 3.63; bands [2.74, 7.48] / [1.26, 6.00] | 5.106 / 3.626; [2.737, 7.476] / [1.257, 5.996] | OK | but see methodological note on the 2026-baseline scenario |
| 50 | 2027 | "cohort term an order of magnitude smaller than the choice" | 1.48/0.36 = 4.1; band/term = 6.5 | IMPRECISE | not 10× |
| 51 | 2027 | Stray sentence "That round has since been published, and the section below reads it" (line 146) | the referenced section is *above* it | ERROR (structural) | leftover from the pre-2025 draft |
| 52 | Locus | n = 187; r 0.974 / 0.961 / 0.905 | 187 (17 × 11); 0.974, 0.961, 0.905 | OK | |
| 53 | Locus | Residual SDs 1.9 / 2.7 pp | 1.90 / 2.74 | OK | |
| 54 | Locus | Regime test p 0.40 / 0.12 (excl. COVID); 0.008 full | 0.401 / 0.119; 0.0084 | OK | Welch t on residuals |
| 55 | Locus | 2020 residual +3.6 pp largest | year-mean top residual 2020 = +3.55, largest | OK | as a year mean; single largest region-year is Asturias 2024 (+6.97) |
| 56 | Locus | ULL −0.08/+0.65; ULPGC −1.04/+0.24; scatter reaches ±3.5 SD | −0.083/+0.646; −1.037/+0.245; max |resid| 2.99 (pass), 3.52 (top) | OK | |
| 57 | Locus | Conditional ULL +1.05, ULPGC +0.53 SD | +1.055, +0.529 | OK | |
| 58 | Locus | 2 of 187 below 4.5; none within ±0.25 of 4.08 / 3.99 | 2 (Canarias 2019 3.60, Balears 2025 4.45); 0; 0 | OK | |
| 59 | Locus | CI ±1.41 pp at 4.08 vs ±0.32 at 6.0; ULL −0.16 pp | 1.407 / 0.319 (pass panel); −0.157 | OK | |
| 60 | Locus | Means: skew +0.60, kurt +0.88, SW p 0.00017, A² 2.06 vs 0.77 | 0.604, 0.880, 0.00017, 2.064; crit 0.749 (scipy 1.17) / 0.771 (older scipy formula) | OK | **`shape_locus.json["mean_axis"]` is wrong** (shapiro_p 0.0048, A² 0.94): script 09 reuses `sw`/`ad` from the last marginal loop (ratio, plateau-removed) instead of the means; the chapter's numbers are right, the JSON is not |
| 61 | Locus | Pass: skew +0.01, kurt +0.39, SW 0.096, A² 0.58; top skew +1.29, A² 5.80; ratio +0.98, A² 3.90 | all reproduce | OK | |
| 62 | Locus | EHU model top residual −0.05 SD | −0.048 | OK | (its pass-panel residual is +1.51 SD, not mentioned) |
| 63 | Locus | Galicia 2015/2016 pass vs [0,5) gap 5.64 / 4.48 pp | 5.64 / 4.48; all band rows sum to 100 | OK | |
| 64 | Frames | Nine communities +0.4 to +1.0 above baseline 2020–24; 2022–24 ≈ +0.65 | nine: +0.52, +1.05, +0.62, +0.53, +0.50 (2022–24 ≈ +0.55); 17: +0.41, +1.03, +0.63, +0.61, +0.71 | IMPRECISE | text mixes the 17-community figures (script docstring) into a nine-community figure |
| 65 | Frames | −0.65; +0.17; +0.02; −1.48; −1.93 | −0.647; +0.169; +0.021; −1.48; −1.932 | OK | Cataluña 2025 is 6.04 in `regions_2026_vs_2025.csv` but 5.98 in the ministry panel (does not change rounding) |
| 66 | Frames | Euskadi baseline 5.92; 2025 already 0.45 below; "0.15 below" for nine 2025 | 5.922; −0.452; −0.148 | OK | |
| 67 | Frames | Ratio 0.353 → 0.466 (t 7.14, p 4e-11) → 0.331 (p 0.30) | 0.353 / 0.466 / 0.331; Welch t 7.14, p 4.3e-11; p 0.296 | OK-as-computed | see methodological concern 3 |
| 68 | Frames | A² 3.90 → 0.94 (ratio), 1.53 (top) | 0.939, 1.526 | OK | |
| 69 | Frames | "enriched the top band among passers by about a third" | 0.466/0.353 = 1.32 | OK arithmetically | but see concern 3 |
| 70 | Path | Fit interval "four times its width at the centre" | 1.41/0.32 = 4.4 | OK | |
| 71 | Record | Tribunal ranges, 71.4 % / 90.6 %, 12,000 signatures, dates | not in repo data | UNVERIFIABLE | |
| 72 | 2027 | PISA 2025 published 8 Sept 2026 | not checkable | UNVERIFIABLE | |

## The known issue, verified

`data/analysis/slope_compare.json` on this machine was regenerated at 16:53 today and already carries **n = 5** (PISA 2012–2025): Spain −0.155 [−0.256, −0.054], p = 0.016; Euskadi −0.327 [−0.603, −0.051], p = 0.033; ratio PAU 1.72 / PISA 2.10; difference tests p = 0.33 / 0.35. Re-running the 2012–2022 window (n = 4) reproduces every number in the chapter's table (−0.147 [−0.381, +0.086]; −0.245 [−0.785, +0.296]; diffs +0.056/+0.087, p 0.48/0.67; ratios 1.72/1.66). The chapter (16:03) is therefore stale relative to both the current JSON and `plots/fig22_slope_compare.png`: "every interval includes zero", "four PISA rounds", "two ratios to within 4 %" and the panel-b title are all now false. Adding 2025 makes both PISA slopes significant on their own, which changes the section's conclusion ("consistent with no decline at all in either" no longer holds for PISA).

## Ranked list of the most serious problems

1. **Stale slope-comparison section (§Do the two instruments fall…)**: table, difference tests, ratio agreement and the "every interval includes zero" headline are all from the n = 4 run; the current data/figure give n = 5 with both PISA slopes significant and a 2.10 vs 1.72 ratio (22 % apart, not 4 %). The section's central rhetorical point is no longer supported.
2. **Madrid word count is ~70 % embedded solutions and marking criteria** (`mad_2025_ord.pdf`, `mad_2026_ord.pdf`, 10 and 13 pages). The statement itself went 1,127 → 1,093 (−3 %), not +8.9 %; the chapter's "4,070 words … more choice prints more text" is a wrong explanation of a contaminated number. Removing the contamination (and Valencia's bilingual half, which is symmetric) *strengthens* the result to r = −0.92 / ρ = −0.86, so the conclusion survives, but the reported numbers and the robustness sentence ("stripping rubric and constants leaves it unchanged") are misleading: the BOILER regex never touched the solutions.
3. **"Eight consecutive years on the other side" (Basque signal)** is false: 2020 (−0.82) and 2021 (−0.33) are negative, and the chapter's own PISA cohort table prints the 2020 value. The 2024 turn is real (−0.96) but it is not a break from an unbroken run.
4. **Basque top-band share "below Spain's in two rounds of three"** — it is below in all three (2018: 3.87 vs 4.18).
5. **"More than double the previous worst"** for the 2025 gap: 18.6/9.7 = 1.92.
6. **"Thirteen published regional standard deviations"**: all thirteen are Comunitat Valenciana (SUV pooled and five universities, 2025–26). One region, not thirteen; the phrase should be corrected even though 2.34 is a reasonable student-level SD.
7. **Structural leftover** at line 146 ("That round has since been published, and the section below reads it") points to a section that is now above it.
8. **Reference-frame numbers for the nine communities** are quoted from the 17-community series (+0.4 to +1.0; "2022–24 all about +0.65"); for the nine the plateau is +0.50 to +1.05 and 2022–24 ≈ +0.55.
9. **Script/JSON defects** that do not (yet) affect the chapter text: `shape_locus.json["mean_axis"]` normality stats are wrong (loop-variable leak in `09_shape_locus.py`); `shape_locus.json["presented_2015_2025"]` records the specific-phase 30,839 while the caption says 37,661 pooled; `18_reading_load.py` docstring numbers (1202/1484/1946, +62 %/+31 %) do not match its own output (1452/2026, +39.5 %); `data/pisa_science_top_levels.csv` only has 2018/2022 and is no longer written by any script; fig-21 caption still says "2006 to 2022".

## Methodological concerns noticed while recomputing

- **The plateau "reshaping" test (0.353 → 0.466, p = 4×10⁻¹¹) is mostly the level effect the chapter says the ratio removes.** The ratio tracks the mean at r = 0.905 (the chapter's own number); the locus predicts 0.356 at the pre-COVID mean (5.77) and 0.442 at the plateau mean (6.45). So ~0.09 of the 0.11 rise is what a pure shift of +0.68 marks produces. Testing the *locus residual* instead gives +0.022 (≈0.46 SD), Welch p = 0.002 on region-years and **p = 0.17 on the five-vs-five year means**. The sentence "a regime that simply moved every mark up by two-thirds of a point would have left that ratio roughly where it was" is contradicted by the locus. The 4×10⁻¹¹ also treats 85 region-years as independent when they are 17 communities × 5 years.
- **Ratio of two slopes that are individually insignificant** (PAU: p 0.19 and 0.38) — the "1.72×" has no usable interval; and the difference test uses a normal z on standard errors from n = 4–6 regressions (a t with 2–4 df would be appropriate). The Euskadi PISA series is also scaled by Spain's p10–p90 (90) rather than País Vasco's (86.7).
- **2027 estimator, 2026-baseline scenario**: the cohort term is prorated 2/3 because PAU 2025 ↔ notional PISA 2023; by the same logic PAU 2026 ↔ notional PISA 2024, so the term to add to the 2026 mark should be 1/3 (−0.18 → 3.81), not −0.36. "The cohort contributes 0.36 to both" is internally inconsistent. The ±2.37 band also assumes independent (random-walk) yearly changes, whereas the series is mean-reverting, so it overstates the 2-year band; and the 0.855 SD is carried largely by 2012 and the COVID years (0.72 without 2020–22).
- **"National mean" is an unweighted mean of 17 communities** (5.67 in 2025) whereas the Ministry's own Total is 5.65 and a presented-weighted mean is 5.73; the drift trend and the 5.20 projection depend on that choice (not wrong, but unstated).
- **Reading-load correlation with n = 8** is leveraged by País Vasco (raw: r −0.72, p 0.066 without PV; after fixing Madrid/Valencia: r −0.88, p 0.008 without PV). Worth stating, since the section is about the author's own paper.
- The Anderson–Darling 5 % critical value 0.77 comes from the older scipy formula (0.771); scipy 1.17 reports 0.749 — cosmetic, but the text quotes a version-dependent constant.
- The "fifteen clean years" power statement is not derived from anything: with the observed non-plateau residual (σ ≈ 0.11 marks) a −0.07/yr drift is detectable with ~6–7 clean years.
</agent-message>