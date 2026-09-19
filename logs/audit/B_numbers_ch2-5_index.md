# Audit B — numeric verification of index.qmd and Chapters 2–5 (agent report, verbatim)

Verdict key: OK / ERROR (correct value given) / IMPRECISE (rounding, wrong range, ambiguous basis) / UNVERIFIABLE (no source in repo). All values recomputed independently from the PX cubes, the July package CSVs, the dashboard transcriptions and the archived primary documents.

## index.qmd

| # | Location (quote) | Claim | Verified value / computation | Verdict | Note |
|---|---|---|---|---|---|
| I1 | Abstract: "mean fell to 3.99 with a 39.8 % pass rate, the lowest values since 2010–11" | lowest since 2010–11 | 2010: 4.45 / 46.3 %; 2011: 4.44 / 49.6 % — both higher than 2026 | IMPRECISE | 3.99 / 39.8 % are the lowest of the whole 2010–2026 series; "since 2010–11" implies those years were as low. A 3.98 variant exists in `comparativa_materias_2026.csv`. |
| I2–I7 | KPI tiles | 5.47; 62.3 %; 24.5/10; 9/17 (3 down, 6 up); 4.08/4.41; +0.80 (6.04 → 6.84, 8 021) | all verified | OK | 8 021 = aptes-basis count |
| I8 | "four of those (Castilla-La Mancha, Tenerife, Las Palmas and La Rioja's 2010–2022 series) were retrieved from dashboards" | 4 of 9 | Tenerife + Las Palmas = one community; La Rioja has no 2026 mean | IMPRECISE | two of the nine (CLM, Canarias) |
| I9–I10 | F1: −0.81, 14 of 17, Euskadi −0.62 | | recomputed −0.810, 14 | OK | |
| I11 | F1: "bounced back (+0.5 to +1.1: … Andalucía)" | six rose by +0.5…+1.1 | Andalucía +0.17; Asturias +1.13 | IMPRECISE | five ≥ +0.5 |
| I12–I13 | F1/F2 deltas; n = 170, SD 0.74 | | −0.832, −0.82; SD 0.737 | OK | |
| I14 | F2: "only 7 changes were as negative — [six named]" | 7 | 7 changes ≤ −1.48, but the list names six; Cantabria 2025 (−1.51) missing | ERROR (omission) | same in Ch.2 |
| I15 | F2: "twelve years of Ministry data" | 12 | cube = 2015–2025 = eleven years (187 = 17 × 11) | IMPRECISE | |
| I17–I18 | F3: ULL 683 / 4.08 / 38.5 % / 30 zeros / 25 % < 2; ULPGC 712 / 4.41 / 42.8 % / 22.6 % | | 263/683 = 38.51; 172/683 = 25.2; 305/712 = 42.84; 161/712 = 22.6 | OK | |
| I19 | F3: "flat-to-decreasing density with a heavy tail at 0–2" | shape | Beta(1.27, 1.81) band shares 13.1/12.9/13.4/13.1/12.3 % over 0–5 then declining | IMPRECISE | see D7 |
| I20–I23 | F4 subject deltas | | deck p.5; dossier; chart labels; Junta text | OK | Madrid Física delta printed as +1.1 here and +1.05 in Ch.3 |
| I24–I25 | F5 school marks 4 541 / 98.1 % / 7.09 …; 45–48 %; gaps 1.6 / 3.1 | | PDF text l.26240 ff.; 0.482 / 0.455; 1.62 / 3.10 | OK | |

## Chapter 2 — Euskadi 2010–2026

| # | Location (quote) | Claim | Verified value / computation | Verdict | Note |
|---|---|---|---|---|---|
| E1 | "EHU annual reports for 2010–2022 … Ministry cube 2023–2025 … agree to ±0.02 on the overlap 2017–2022" | | EHU − Ministry(specific): +0.01, 0.00, +0.02, +0.01, +0.01, 0.00 | OK | presented counts differ by 0–15; 2015–16 EHU "all phases" (5.45, 6.16; 2 179 / 2 082) = Ministry pooled (5.44, 6.139; 2 196 / 2 102) ≠ Ministry specific (5.53, 6.16; 1 464 / 1 369). See S1. |
| E2–E5 | series table 2010–2025; Spain mean; gap; Δ | | all recomputed | OK | 2022 Δ −1.63 (EHU) vs −1.62 (Ministry panel) both appear on the site |
| E6 | 2011 no-shows artefact; "pass rate roughly 55 %" | | no_presentados = 10; 1294/(2620−300) = 55.8 % | OK / UNVERIFIABLE | rests on an assumed ≈ 300 no-shows |
| E7 | "presented/enrolled ratio drops (≈ 89 % → ≈ 70 %) from 2017" | | 88.9 → 73.0, 67.3, 65.3, 64.0 (EHU all phases) | OK | Ch.5 participation table (specific phase) gives 83.4 % → 72.7 % for the same transition |
| E8–E9 | 2025: 2 189 of 2 597 (84 %); 2026 pool 2 066 | | 84.3 %; deck p.3 | OK | 2 066 read as presented |
| E10 | regimes table | | recomputed | OK | |
| E11–E13 | trend fit β = +0.013 (r 0.17, p 0.60), σ 0.31; x̂ 6.17, residual −2.18 ≈ −7.0 σ; 2025 residual −0.69 ≈ −2.2 σ | | 0.01299; 0.171; 0.596; 0.311; 6.173; −2.183; −7.02; −0.690; −2.22 | OK | |
| E14 | "means between 5.45 and 6.49 in normal years; 2025 fell just outside that band" | | 2025 = 5.47, inside [5.45, 6.49] | ERROR | the residual is outside; the level is not |
| E15–E18 | 2010–11 pass ≈ half; n = 170; Δ̄ −0.03, s 0.74 (non-COVID 0.69); z = −1.97 | | 46.3/49.6 %; −0.031; 0.737; 0.687; −1.966 | OK | |
| E19 | "only 7 of the 170 … [six named]" | | Cantabria 2025 (−1.51) missing | ERROR (omission) | |
| E20 | "a typical community moves by ±0.7 points" | | SD 0.74; mean |Δ| 0.57; median |Δ| 0.51 | IMPRECISE | |
| E21–E23 | ≈ 4 % of transitions; Basque own SD 0.85; 187 means, only Canarias 2019 below 3.99; next lowest 4.45, 4.65, 4.67 | | 4.1 %; 0.855; verified | OK | |
| E24 | "the Basque case is the only one in the panel with two consecutive falls summing to more than two points" | uniqueness | Extremadura 8.55 → 6.45 → 6.09 (−2.46, 2023–25) and Baleares 6.49 → 6.10 → 4.45 (−2.04, 2023–25) qualify inside the cube | ERROR | and the 2026 point is not in the panel |
| E25–E27 | changes-by-year table; 14 of 17, −0.81, Euskadi 11th-most-negative; rank table | | recomputed | OK | |
| E28 | "never been a top region … median rank 7–8, low of 15th in 2015 and 13th in 2024" | | median 8; Euskadi ranked 4th in 2016, 2018 and 2021 | IMPRECISE | |
| E29–E32 | 2025 rank 12, −0.18; 2026 0.46 below Baleares 2025; wide table; fig-1 caption | | verified; pooling reproduces to 0.0005 | OK | |

## Chapter 3 — Spain 2026

| # | Location (quote) | Claim | Verified value / computation | Verdict | Note |
|---|---|---|---|---|---|
| S1–S9 | regions table | | Canarias pooled 4.248 / 40.72 %; 2025 pooled ULL+ULPGC = 5.081 = Ministry 5.08; Valencia p.43 5 259 / 76.350 / 6.396 / SD 2.380, 2025 5.889; Cataluña dossier p.20; CLM 80.07 %; Madrid chart 5.6/6.7 vs Ministry 5.65; Asturias 6.62 / 76.87 (press, not in repo); Extremadura 5.27 (press, not in repo) | OK (S3, S9 UNVERIFIABLE) | Madrid delta +1.05 (Ministry base) here vs +1.10 (chart base) in Ch.5/index |
| S10–S11 | six rose, three fell; weighted change outside Euskadi +0.58; median +0.65 | | 0.583; 0.653 | OK | |
| S12 | blockquote "recovered in at least six … by +0.5 to +1.1" | | Andalucía +0.17; Asturias +1.13 | IMPRECISE | |
| S13–S14 | gap within ±0.5 except 2021; Canarias 5.36 → 3.60 → 5.25 | | −0.39…+0.46; 2021 +1.04 | OK | |
| S15 | Canarias "(5.88 → 5.08 → 4.25) is the same two-step fall as Euskadi's (6.09 → 5.47 → 3.99), one point higher" | | Canarias is 0.21 and 0.39 lower in 2024–25 and 0.26 higher in 2026; steps −0.80/−0.83 vs −0.62/−1.48 | ERROR | |
| S16 | Extremadura "highest in Spain in 2021–2023 (8.03, 8.44, 8.55)" | | 2021: La Rioja 8.31 > 8.03; highest in 2022–2023 only | IMPRECISE | |
| S17 | 5.27 "lowest subject in the UEx table" | | press, not in repo | UNVERIFIABLE | |
| S18 | CLM series and pass rates | | found_clm rows | OK | |
| S19 | "≈ 1 750 presented each year" | | 1 589, 1 708, 1 751, 1 795, 1 784, 1 781 | IMPRECISE | 2021 is 1 589 |
| S20 | CLM "extraordinary sitting sits 2–3 points lower every year" | | gaps 1.36, 2.50, 1.97, 2.09, 1.24, 2.83 | ERROR | range 1.2–2.8 |
| S21–S22 | province spread 0.23; La Rioja series | | verified; 2015–2022 chart values coincide with the cube | OK | |
| S23 | La Rioja pass rates "settling at 66–80 %" | | 2012 82.3 %, 2021 94.4 %, 2022 85.7 % | IMPRECISE | |
| S24 | "both jumped by two points in 2012" | | Euskadi +2.05; La Rioja +1.24 in 2012 (+2.24 over 2010→2012) | IMPRECISE | |
| S25–S26 | Cataluña 6.04 aptes basis; Madrid chart labels; three publish no N | | verified | OK | Ministry 2025 Cataluña = 5.98 |
| S27 | "FP and foreign-access students … effect ≤ 0.05 where both are known" | | Total vs Título de Bachiller, 2025: PV 0.00, And 0.02, CLM 0.00, Can 0.02, Ast 0.02, Val 0.05, Madrid 0.06, Extremadura 0.06, Cataluña 0.11, Total 0.13 | IMPRECISE | |
| S28 | "after the revision window" | | deck dated 6 July | UNVERIFIABLE | |

## Chapter 4 — Distributions

| # | Location (quote) | Claim | Verified value / computation | Verdict | Note |
|---|---|---|---|---|---|
| D1–D3 | published moments; implied counts 822–823 / 506–507 / 66–67; 2025 fit inputs | | verified | OK | |
| D4–D5 | Beta tables 2025 (2.00, 1.61; SD 2.39; median 5.61; 30.3 / 5.9 / 41.5) and 2026 (1.27, 1.81; SD 2.52; 3.80; 14.6 / 2.1 / 64.9) | | refits stable from three starts; exact mixture SDs 2.38 / 2.51 (script uses the published mean in the variance) | OK / IMPRECISE (SD) | immaterial |
| D6 | 2025 fit "mode near 6" | | 6.2 | OK | |
| D7 | "The 2026 fit has a = 1.27 < b = 1.81: a density that is highest near the origin and decreases monotonically" | | with a = 1.27 > 1 the density is 0 at the origin, rises to a mode at 2.5, then decreases; not monotone, not J-shaped (needs a ≤ 1) | ERROR | band shares are ≈ flat (12–13 %) over 0–5 then decline; the prose about the density is wrong; affects "J-shaped 2026" wording and index F3 |
| D8–D9 | median 3.8; 30 → 15 %, 6 → 2 %; shifted-2025 fit gives 0.23 / 0.38 | | 3.80; 30.3 → 14.6; 5.9 → 2.1; 0.225 / 0.376 | OK | |
| D10–D11 | 41 tribunals; bands table 2015–2025 | | deck p.2; cube specific phase renormalised, all rows match | OK | 2015–16 specific phase only, whereas the Ch.2 series uses all phases |
| D12 | "[0,5) had been 25–34 % in every normal year" | | 2015 36.4 %; 2020 24.9 % | IMPRECISE | |
| D13 | 2026 fit near 65 % | | 64.9 | OK | |
| D14 | top band "17–20 % in 2018–2023" | | 2019 15.4; 2021 36.0 | IMPRECISE | |
| D15–D17 | Canarias summary and histogram tables; ULL/ULPGC 2026 shares | | all cells recomputed from h_* columns | OK | |
| D18 | "bell-shaped 2024 (ULL mode [5,6), ULPGC mode [9,10]), flattened 2025, J-shaped 2026" | | ULPGC 2024 rises monotonically 2.9 → 16.1 (not a bell); ULPGC 2026 (11.2, 11.4, 10.0, 13.1, 11.5, 12.8, 9.8, 9.4, 5.9, 4.9) is flat rather than J | IMPRECISE | |
| D19 | "[5,6) … in 2026 it is 11.9 %, no larger than its neighbours" | | neighbours [4,5) 10.0, [6,7) 9.7 — 11.9 is larger than both (4th-highest band) | IMPRECISE | the pile-up is muted, not gone |
| D20–D23 | zeros 5 → 18 → 30 (0.7 → 2.3 → 4.4 %); Valencia SDs 2.38 / 2.28; CV 0.44 → 0.63; school 7.1 | | verified | OK | |

## Chapter 5 — Subjects, sittings, participation, groups

| # | Location (quote) | Claim | Verified value / computation | Verdict | Note |
|---|---|---|---|---|---|
| F1–F5 | subject tables (Euskadi deck; Cataluña dossier; Madrid chart labels; Andalucía Junta text with cube 2025 baselines Mat II 6.542, Química 5.49; Asturias cube 2025 Mat II 6.762, Química 7.39; 2026 press) | | verified (Asturias 2026 UNVERIFIABLE) | OK | Ministry 2025 PV Química 6.22 / Biología 6.44 / Mat II 6.74 vs deck 6.24 / 6.45 / 6.73 — deck used |
| F6 | directional summary Física / Mat II / Química | | table | OK | |
| F7 | "Biología rose in Euskadi, Madrid and Asturias and fell in Cataluña" | | no Asturias Biología value exists (table "—") | ERROR | |
| F8 | Euskadi only community with both quantitative subjects down > 1.5 while Química/Biología/Lengua held | | | OK | |
| F9 | Matemàtiques 4.18 lowest in a decade; 2 057 revision requests; Física 6.84 best in five years | | 4.18 lowest since 2014 (4.00); 6.84 highest since 2021 (6.99); 2 057 not in any repo source | OK / UNVERIFIABLE | |
| F10 | "every dataset in this study shows [July] 1.5 to 3 points below June" | | only 56 % of the 187 Ministry community-years lie in [1.5, 3]; 63 < 1.5 (min −0.34), 19 > 3 (max 4.05); Euskadi 2022 1.18; CLM 1.36 / 1.24; ULL 2026 0.81 | ERROR | |
| F11–F12 | Euskadi ord/extra table; gap 1.85 ± 0.86 | | 1.851 ± 0.862 | OK | |
| F13 | "Valencia 4.16 (777), CLM 3.97 (142), Tenerife 3.27 (97) — sit exactly on the historical relation" | | gaps 2.23, 2.83, 0.81 (ULL 1.2 SD below the mean gap) | IMPRECISE | |
| F14 | "global July pass rate (71.40 % of 1 332, against 90.6 % in July 2025)" | 90.6 % = July 2025 | EHU Informe PAU 2025: July 2025 Bachillerato 1 170 presented, 973 apto = 83.16 %; 90.57 % is the July 2024 figure (Informe EAU 2024) | IMPRECISE / likely wrong year | 71.40 % / 1 332 press, unverifiable |
| F15–F16 | 624 re-sitters; July Física "near 2" | | press; 3.99 − 1.85 = 2.14 | UNVERIFIABLE / OK | |
| F17–F19 | participation table; enrolment flat, cohort ≈ 9 900 → 12 300, share quarter → fifth; presentation 64–76 % → 84 % | | verified; 9 900 not in repo; 2597/12321 = 21 % | OK / UNVERIFIABLE | 2015–16 differ from the Ch.2 series (phase basis) |
| F20 | "some 400 candidates who … would not have sat" | | 205 (2024 rate) to 371 (70 %) | IMPRECISE | 200–370 |
| F21–F23 | −5.6 %, +15.5 %; school-marks block; ratios and gaps | | fully verified (PDF text) | OK | |
| F24 | centre-level scatter of the July package | | not in repo | UNVERIFIABLE | |
| F25 | gender/language table | | recomputed; data flaw: 2014 euskera + castellano enrolment = 2 195 ≠ 2 495; the 61.5 % share is not reproducible | OK / data flaw | |
| F26–F29 | women 31–36 %; +0.21 every year from 2011; ULL/ULPGC by sex; euskera 61 → 75 %, below castellano by 0.1–0.3 except 2012/2020/2021 | | 30.6–36.0; 2014 W−M = −0.01; 2010 −0.53, 2011 −0.02, 2019 −0.04 | OK / IMPRECISE | |

## Most serious problems (ranked by the agent)

1. Ch.2 E24 — false uniqueness claim (Extremadura and Baleares 2023–25 also fell > 2 points over two years).
2. Ch.4 D7 — the fitted 2026 density is mischaracterised (interior mode at 2.5; not monotone; not J-shaped).
3. Ch.2 / index — the "7 changes as negative" list names six (Cantabria 2025, −1.51, missing).
4. Ch.5 F7 — Asturias Biología "rose" with no value in the data.
5. Ch.5 F10 / Ch.3 S20 — ordinary–extraordinary gap ranges overstated.
6. Ch.5 F14 — "90.6 % in July 2025" is the July 2024 figure (July 2025 = 83.2 %).
7. Ch.3 S15 — Canarias "one point higher" is not true on any reading.
8. Ch.2 E14 — 2025 (5.47) is inside the 5.45–6.49 band.
9. Index/Ch.3 "+0.5 to +1.1" for six risers; "twelve years"; "four of the nine … La Rioja".
10. Range statements that exclude data points (bands 25–34 %; top band 17–20 %; La Rioja 66–80 %; Extremadura highest 2021–23; women every year; FP effect ≤ 0.05).

## Systematic issues

- S1. The Euskadi series splice (EHU informes to 2022, Ministry from 2023) is continuous (≤ 0.02 on 2017–2022), but 2015–16 use the all-phases basis in Ch.2 and the specific-phase basis in Ch.4/5 (enrolled/presented differ by ≈ 700; pre-2017 presentation rate ≈ 89 % vs 83.4 %).
- S2. Phase pooling of the Ministry ordinary means is correct and reproduces `ministry_fisica_ord_ccaa.csv` to 0.0005; the change panel, ranks, levels and gap statistics reproduce exactly.
- S3. Mixed 2025 baselines for the same region (Madrid: Ministry 5.65 vs chart 5.6 → two deltas on the site).
- S4. Beta fits stable; SD formula uses the published mean (immaterial); density prose contradicts the parameters.
- S5. Press-sourced numbers not in `sources/` (Extremadura 5.27; Asturias 6.62 / 76.87 / 6.86 / 7.67; EHU July 2026 71.40 % / 1 332 / 624 / 90.6 %; Cataluña 2 057 revision requests; 2017 Basque cohort ≈ 9 900). Dashboard transcriptions are internally consistent and cross-validate against the cube (Canarias 2024–25 pooled; La Rioja 2015–22).
- S6. July-package data flaw: 2014 language enrolment columns sum to 2 195 instead of 2 495.
