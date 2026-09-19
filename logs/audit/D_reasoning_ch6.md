# Audit D — reasoning audit of Chapter 6 ("Interpretation and the 2027 question")

Read by the lead auditor, section by section and in the order the chapter was built (steps 1–12 of `analysis_path.json`). This file records the logic, not the arithmetic (arithmetic is in C). Three new computations were made to test gaps found here; their outputs are in `data/audit/`.

## 0. Structure

The chapter has grown by accretion and now reads as a diary. The hypotheses list (H1–H4) is interrupted by six sub-sections (drift, Basque signal, PISA, slopes, reading load, PISA 2025) before H5 and H6 resume; the "shift or shape" and "reference frame" sections, which the H4 paragraph and the Basque-signal section already rely on (`@fig-locus`), come after them; an orphan sentence ("That round has since been published, and the section below reads it") sits after the section it announces; and at least four passages describe "an earlier version of this section" and what it got wrong. A reader who is not the author cannot tell what the chapter currently claims from what it once claimed.

Recommendation: three parts. (1) The hypotheses, one paragraph each, stating the current verdict only. (2) The tests, in logical not chronological order: shape vs location → reference frame → drift → Basque conditional residual → PISA level and top band → PISA vs PAU slopes → reading load → 2027. (3) "How this reading was arrived at" as the single place where the history, the retractions and the audit are recorded, with the figure-18 ladder extended to the audit (see §9). The record, the requests and the design questions stay as they are.

## 1. H1 and the reference frame (steps 2 and 6)

The re-baselining result is genuine and important: measured against 2015–2019, the 2025 national Física mean is at its norm (−0.15) and the 2020–2024 years are a plateau (+0.4 to +1.0). Two problems follow from how it is used.

(a) The causal sentence — "the visible −0.81 is the withdrawal of five years of COVID-era leniency, and would have appeared in 2025 under any marking scheme that stopped being lenient" — is not identified by these data. The end of the plateau and the first LOMLOE papers coincide in 2025 by construction; nothing in the PAU series separates "leniency withdrawn" from "the reform's new papers and marking instructions ended the plateau". The chapter picks one. The honest statement is: the 2025 level is normal; the 2024→2025 fall is the plateau ending; why it ended in 2025 rather than 2023 is exactly what the reform would explain, and cannot be excluded.

(b) A cheap discriminating test was available and not run: does the plateau, and its end in 2025, appear in *every* subject? If the COVID-era regime lifted all subjects and 2025 returned all of them, the pattern is subject-general and H1's Física-specific form ("the competency model bites Física") is weakened further. Computed here from the Ministry cube (17 communities, unweighted, each subject against its own 2015–19 baseline, `data/audit/plateau_by_subject.csv`):

| subject | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| Física | −0.17 | +0.41 | +0.92 | +0.59 | +0.56 | +0.71 | −0.06 |
| Matemáticas II | −0.09 | +0.48 | +0.96 | +0.50 | +0.76 | +0.63 | +0.11 |
| Química | +0.05 | +0.58 | +0.94 | +0.69 | +0.69 | +0.82 | +0.20 |
| Biología | +0.03 | +0.33 | +0.55 | +0.46 | +0.43 | +0.17 | −0.21 |
| Historia de España | +0.07 | +0.29 | +0.65 | +0.48 | +0.62 | +0.75 | +0.53 |
| Lengua Castellana II | +0.06 | +0.22 | +0.31 | +0.38 | +0.39 | +0.47 | +0.13 |
| Dibujo Técnico II | −0.15 | +0.45 | +0.59 | +0.57 | +0.66 | +0.44 | +0.18 |

The plateau is in every subject and ended in every science subject in 2025 (Historia kept most of its lift). So the 2025 fall was neither Física-specific nor Basque-specific; it was the simultaneous end of a subject-general regime — in the first LOMLOE year. This strengthens the chapter's re-baselining point and, at the same time, keeps the confound: LOMLOE changed every paper.

(c) The nine-community average (+0.02 above baseline in 2026) hides a ±1-point dispersion that is the real 2026 story. Against their own pre-COVID baselines (Ministry pooled means; Cataluña 2026 on its aptes basis), 2026 sits at Madrid +1.02, CLM +0.86, Cataluña +0.63, Andalucía +0.48, Asturias +0.48, Valencia +0.34, Extremadura −0.78, Canarias −0.86, País Vasco −1.91 (`data/audit/baseline_2026_by_community.csv`). Six communities are *above* their pre-COVID norm in 2026, three below; the Basque value is the outlier in either frame. The chapter's table of frames should carry this dispersion rather than only the average, because "Spain is where it was" (row three) is as much a frame artefact as the rows it criticises.

## 2. Shift or shape (steps 3–5, 7)

The locus construction is sound and the caveats (extrapolation below 4.5, uncalibrated SD units on skewed panels, "consistent with" not "demonstrated") are correctly drawn. Two claims do not hold.

(a) "The plateau reshaped the distribution: the ratio rose from 0.353 to 0.466 (t = 7.14, p = 4 × 10⁻¹¹) … a regime that simply moved every mark up by two-thirds of a point would have left that ratio roughly where it was." The chapter's own r = 0.905 between the ratio and the mean says otherwise. The locus predicts a ratio of 0.357 at the pre-COVID mean (5.77) and 0.443 at the plateau mean (6.44): about 0.09 of the 0.11 rise is what a pure level shift produces. Tested on the locus residual, the plateau's excess is +0.02 (≈ 0.5 SD), p = 0.0013 on 85 non-independent region-years and p = 0.17 on the five-vs-five year means, and it is carried by 2020 alone (+0.06; 2021–2024 are +0.01, 0.00, −0.02, 0.00). The reshaping claim, and its use in step 7 ("the plateau did not merely lift the level, it reshaped the distribution"), should be withdrawn: the plateau was, to the precision available, a lift.

(b) The regime test around 2017 quotes p = 0.008 on the full series and attributes it to 2020; that is fine, but it is the same 2020 outlier driving (a), and the chapter should say once that 2020 — the year of the emergency sittings — is the single most anomalous year on the conditional measure and drives every "shape" result that includes it.

## 3. "A Basque signal that arrives a year early" (step 7)

This section does not survive.

(a) The factual premise ("a two-year turn away from eight consecutive years on the other side") is false: Euskadi's residual against the field is negative in 2015 (−0.10), 2020 (−0.82) and 2021 (−0.33), positive in six of the nine years 2015–2023.

(b) No base rate was computed. Recomputed here (`data/audit/conditional_turn_base_rate.csv`): five of the seventeen communities — Aragón, Castilla y León, Comunitat Valenciana, La Rioja and País Vasco — have a conditional residual below −0.5 SD in *both* 2024 and 2025; nine of seventeen have some two-year run below −0.5 SD in the panel; three communities have longer positive runs over 2016–2023 than Euskadi (Galicia 8 of 8, Extremadura and Baleares 7 of 8). A two-year negative turn after a mostly positive run is what a quarter of the panel shows in the same two years. It is not a Basque signal.

(c) The units are, by the chapter's own admission, not calibrated on this panel (right-skewed ratio), and the residual's year-to-year autocorrelation is never examined, so "two years" is not two independent observations.

(d) The section is then used as a premise: the PISA cohort table tests whether PISA "agrees" with this measure, and the 2022/2024 "match" was, the chapter says, what the PISA section was originally built around. With (a)–(c), the PISA cohort comparison loses its Basque-side variable; what remains of it (three noisy points, one agreement) is correctly discounted already.

Recommendation: reduce to one sentence in the drift section — "on the conditional top-band measure Euskadi turns negative in 2024–25, as do four other communities; nothing Basque-specific is visible on it" — and remove it from the monitoring recommendation, or keep it there as a panel-wide measure rather than a Basque one.

## 4. The drift (step 8)

The tests are adequate and the conclusion ("not visible on any measure that can see composition") is the right one. Three points of hygiene: the "national mean" used for the 2015–19 trend is the unweighted mean of 17 communities (5.67 in 2025), not the Ministry's Total (5.65) or a presented-weighted mean (5.73) — say which and why; the "fifteen clean years" rule of thumb is not derived from anything (with the observed residual the drift is detectable with about six clean years, which is why the five pre-COVID points already give p = 0.058); and "the number presented grew 30 %" is true but take-up is flat, which the section itself shows — the two sentences should be adjacent so the reader does not carry the 30 % as evidence of recruitment.

## 5. PISA as the outside instrument (step 9)

(a) "The cohorts can be matched exactly" overstates. PISA samples the whole 15-year-old cohort (repeaters included; the Basque repetition rate at 15 is not negligible); the PAU is sat by the Bachillerato half of that cohort two years later; Física by about a quarter of the PAU candidates. The matching is by birth year, not by population. The section says "self-selected quarter" later; it should say it first.

(b) Sampling error is never mentioned, and it matters for the narrative of a "break in 2015 … stayed a deficit". From the INEE tables (`E.T.` columns): País Vasco science SE 2.4 (2012), 3.0 (2015), 4.2 (2018), 4.6 (2022), 4.3 (2025); Spain 1.6–2.1. The gap changes are therefore: 2012→2015 −18.9 ± ≈4.5 (robust), 2015→2018 +13.8 ± ≈6 (2σ), 2018→2022 −9.1 ± ≈6.7 (not significant), 2022→2025 −13.6 ± ≈6.8 (2σ); link error between rounds (≈2–3 points) is on top. The 2015 break and the 2025 gap (−18.6 ± 4.7) are real; "+4.1 in 2018" and "−5.0 in 2022" are within noise of each other, so "stayed a deficit" is a reading of two noisy points. The top-band shares (3.25 / 3.87 / 3.32 / 1.83 %) carry SEs of roughly ±0.5–0.7 pp; "halves" in 2025 is about a 2σ change.

(c) The section retracts an earlier draft in its own text twice. The retractions belong in §9.

(d) "The slow-drift version of H4 … is clearly present in the schooling that precedes it" is supported for the level (a step down in 2015, a further step in 2025); it is not supported as a *drift* (steady decline): the PISA record is two steps, not a slope — which matters for the next section.

## 6. Do the two instruments fall at the same rate? (step 10)

(a) Stale (see C): with PISA 2025 in the series both PISA slopes are significant and the Euskadi/Spain ratio is 2.10, not 1.66; "every interval includes zero" is false in the figure as committed. The section must be rewritten or the fit pinned to 2012–2022 with the reason stated (2025 held out for the estimator).

(b) Even on the 2012–2022 window the comparison is not well-posed. The chapter's own description of the Basque PISA series is a break in 2015 followed by noise; the Basque PAU series is a plateau followed by a step. Fitting straight lines through step changes and comparing the slopes measures the position of the steps in the window, not a common rate. The "1.72 × vs 1.66 ×" agreement is a ratio of two slopes whose own p-values are 0.19–0.38 (PAU) — a ratio with no usable interval — and the difference test uses a normal z on standard errors from regressions with 2–4 degrees of freedom. The chapter concludes "not worth believing on its own"; the section would be more honest as one paragraph saying that the two records are not comparable as trends, and dropping the ratio.

(c) The PAU SD (2.34) comes from thirteen Comunitat Valenciana figures, not thirteen regions, and the PISA SD (90) is Spain's p10–p90, not the Basque one (86.7). Immaterial to the sign, material to the wording.

## 7. How much of the paper is reading? (step 12)

(a) The measurement is contaminated for Madrid (embedded solutions; the true statement change is −3 %, not +9 %), and the robustness sentence about stripping rubric is not true of what was stripped. Removing the contamination strengthens the correlation (r = −0.92, ρ = −0.86), so the direction is safe; the numbers in the text are not.

(b) The section is transparent that length and competency content are one signal seen twice (r = +0.87) and that the reading × length interaction is untested. It should add two things: that the correlation is leveraged by País Vasco (raw r = −0.72, p = 0.07 without it; −0.88 after the Madrid fix), and that the hypothesis was generated from the author's knowledge of his own paper's length (the disclosure says so) — which is the definition of a post-hoc variable and is the reason the result should be framed as exploratory, not as "the strongest association this study has found".

(c) The Basque PISA reading fall (−72 points 2015→2025) is quoted as motivation; with SEs of ≈4–5 points per round it is real. But the section should note that the reading decline is national too (Spain −44) and that the *gap* widening (−4 → −32) is the Basque-specific part.

## 8. What PISA 2025 says about PAU 2027 (step 11)

(a) Internal inconsistency: the cohort term is prorated 2/3 on the grounds that PAU 2025 corresponds to a notional PISA 2023; by the same logic PAU 2026 corresponds to PISA 2024, so the term to add to the 2026 mark is 1/3 of the three-year change (−0.18), not −0.36. "The cohort contributes 0.36 to both" is wrong; the 2026-based scenario should read 3.81.

(b) The "paper-and-marking term" (±2.37) is mislabelled. The year-to-year SD of the Basque mean (0.855) is the *total* variance of everything — paper, marking, cohort, sitting composition — not the paper's share; the decomposition is not clean, and the 0.855 is carried by 2012 (+2.05) and the COVID years (0.72 without 2020–22). The band also assumes independent annual changes (a random walk) in a series that is visibly mean-reverting, so it overstates the two-year band. None of this changes the conclusion (the paper dominates; a forecast spanning 2.7–7.5 is not a forecast), which is robust.

(c) The section's most useful sentence — that −0.36 is the part of 2027 that should not be blamed on the paper — should carry the SE of the PISA change it rests on (−21 ± ≈7 points → cohort term −0.36 ± 0.12).

## 9. "How this reading was arrived at, and what it cost each earlier one"

The idea of the section is right and worth keeping: the frame-dependence of the headline claims is the most transferable lesson of the study. But as written it has four defects.

(a) It is stale: "four of its six steps" and a narrative of steps 1–7 against a twelve-step figure; the figure's step 10 hard-codes "every interval includes zero", which the script's own data no longer support — so the claim that "every value is read from the JSON, so the figure cannot drift" is false for the step text.

(b) Figure 18's caption is false: the −0.81 national point is the 17-community 2024→2025 change, not a nine-community figure; the nine-community value is −0.65. Part of the "sign change" in panel a is a change of transition year, not of frame.

(c) It stops before the audit. The section argues that stopping at step 2 would have produced "a coherent, quotable and partly wrong account"; the same is true of stopping at step 12 — the slope section, the reshaping claim and the Basque-signal section are each coherent, quotable and wrong in the committed text. The ladder should record the audit as step 13 with what it cost: the reshaping claim withdrawn (level effect), the Basque signal withdrawn (base rate 5 of 17), the slope agreement withdrawn (stale window; steps, not slopes), the 2027 proration corrected, the Madrid length corrected. That is the honest end of the sequence, and it is a stronger version of the section's own point.

(d) The lesson drawn — "every step which narrowed the claim came from asking about the data rather than about the subject" — is true of steps 4–6 and false of the audit's findings, most of which came from asking about the subject (what the plateau did in other subjects; what a base rate is; what PISA's sampling error is; what a PDF contains). Both kinds of question are needed; the section should say so.

## 10. Sub-questions the chapter should pose (and, where cheap, answer)

1. Is the plateau subject-general, and did it end in 2025 for every subject? — Yes (§1b). To be added to the reference-frame section.
2. What is the base rate of the 2024–25 conditional turn? — 5 of 17 (§3b). Ends the Basque-signal section.
3. Do Euskadi's *other* subjects show a Basque-specific drift against their own baselines? — No: relative to 2015–19, Basque Mat II, Química and Biología sat +0.3 to +1.4 through 2021–2024 and +0.27, −0.01, +0.31 in 2025, while Física was −0.39 in 2025 (`data/audit/basque_subjects_vs_baseline.csv`). Whatever PISA sees in the Basque science base, the Basque PAU sees it in Física only, and only from 2025. That is evidence for the paper and against a general cohort weakening — and it is the cleanest within-Basque comparison available.
4. Are the PISA gap changes larger than their sampling and link errors? — 2012→2015 and 2022→2025 yes; 2015→2018→2022 no (§5b).
5. Which national mean? — declare one (Ministry Total, presented-weighted, or unweighted) and use it throughout.
6. What does the ordinary–extraordinary relation predict for Euskadi July 2026, and does the July 2026 paper (mass spectrometer obligatory) match the June one in type? — the exam data are in hand (Chapter 12); the July result is not; worth stating as the first check when it is published.
7. Does the 2026 Basque result look different by tribunal, sex, language, territory? — unanswerable now; already in the requests.

## 11. Verdicts on the chapter's ranking (H1–H6)

- H1 "explains 2025, not 2026": revise to "the 2025 level is the pre-COVID norm in every subject; the reform coincides with the end of a subject-general plateau and cannot be separated from it; it does not explain the 2026 Basque result". Weaker than the chapter's "no national 2025 anomaly for it to describe" but defensible.
- H2 (the paper): unchanged — the strongest hypothesis, now supported by Chapters 11–12 and by §10.3 (Física-only, 2025-onward).
- H3 (marking): unchanged, unresolved.
- H4 slow drift: the PISA level evidence stands (two steps, 2015 and 2025); the Basque-signal and slope-comparison supports should be withdrawn; §10.3 argues against a general Basque cohort effect in the PAU.
- H5, H6: unchanged.
