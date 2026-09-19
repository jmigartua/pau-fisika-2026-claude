# Audit E — blind second coding of the 2025/2026 papers (agent report, verbatim)

# Second independent coding of the 18 Física papers — agreement with the first coder and robustness of Chapter 11

Output file: `/home/claude/work/logs/audit/E_second_coding.csv` (149 rows: 146 first-coder items plus Canarias 2025 coded at question level, Q1–Q11, which I aggregated by max into the first coder's option items I.A … IV.B for the comparison). No other file was edited. Working script: `/tmp/claude-0/-home-claude/ac6276f8-e09f-58f2-a35c-aec4bd1f5273/scratchpad/agree.py`.

Coding was done blind, from `/home/claude/work/sources/exams/*.txt` only (plus one check of `cat_2025_ord_crit.txt` to confirm that the block depth in Cataluña 2025 3A is only in the figure). The first coder's CSV, script and chapter were read only afterwards.

## 1. Agreement (146 matched items)

| code | % agreement | Cohen κ | disagreements | prevalence coder 1 | prevalence coder 2 |
|---|---|---|---|---|---|
| ctx (0/1/2) | 83.6 | 0.70 (linear-weighted 0.75) | 24 | ctx=2: 11.6 % | ctx=2: 7.5 % |
| ctx==2 (binary) | 93.2 | 0.61 | 10 | 11.6 % | 7.5 % |
| app | 91.1 | 0.76 | 13 | 22.6 % | 27.4 % |
| explain | 92.5 | 0.85 | 11 | 43.8 % | 43.2 % |
| graph | 97.3 | 0.83 | 4 | 9.6 % | 8.2 % |
| draw | 100.0 | 1.00 | 0 | 23.3 % | 23.3 % |
| evaluate | 99.3 | 0.91 | 1 | 4.1 % | 3.4 % |
| **competency flag** (ctx==2 & (explain or evaluate)) | 96.6 | 0.76 | 5 | 8.9 % | 6.8 % |

Points and obligatory status agree on all 146 items. The first coder's stored `competency` and `criteria_met` columns reproduce exactly from their codes.

Reading: draw, evaluate, graph and explain are reliable (κ ≥ 0.83). The soft spot is `ctx`, and specifically the 1/2 boundary: I am the stricter coder (11 items ctx=2 vs 17). All five competency-flag disagreements are ctx 1↔2 calls, and all five sit in the two "competency-style" communities (Cataluña ×3, País Vasco ×2).

## 2. Disagreements (coder 1 → coder 2), with my view

**Affect the competency flag (5)**
- Cataluña 2025 ex. 1 (ISS toolbox/deorbit): ctx 2→1. The narrative supplies numbers and orders the tasks (deorbit → fall into the Pacific) but nothing is interpreted or decided. Genuinely borderline; either reading fits the scheme's wording.
- Cataluña 2025 2A (Millikan): ctx 2→1. A canonical physics experiment, not a scenario; but the setup does have to be interpreted (plate signs, what happens if the drop loses an electron). Either.
- Cataluña 2026 1A (Generalitat nanosatellite): ctx 2→1. Standard T, ΔEp, Emec; "closed orbit? justify" is a generic physics question. I think mine is right.
- País Vasco 2026 3b (choose the lupa or the spectacle lens to build a projector): ctx 1→2, evaluate 1→0. I read the design decision as substantive context; coder 1 kept ctx=1 and coded the suitability judgement as evaluate. Both give the item 3 criteria; the paper share is unchanged because…
- País Vasco 2026 4b (C-14 dating of bones): ctx 2→1. The explanations asked are about the decay law itself, not the context; coder 1's reading (real application that has to be interpreted) is defensible. Either. Net for PV 2026: 3b swaps with 4b, same 1.25 expected points.

**ctx only, no effect on the flag (14)**
- Cataluña 2025 3B flute, 2026 ex. 2 X-ray tube, 2026 ex. 3 phone vibrator: 2→1 — standard calculations, nothing driven by the setting; mine. (Coder 1 coded every Cataluña context as 2; this inflates Cataluña's "substantive" share, see §4.)
- País Vasco 2026 3a violin/concert: 2→1 — standard λ, fingering, dB with two sources; mine.
- Comunitat Valenciana 2026 4A Tc-99m: 1→2 — the spec (400 MBq at test time, 5 h delay) drives a backward calculation, i.e. a "design specification"; mine, but no explain/evaluate so irrelevant to the flag.
- Generic-object cases coded 1 by coder 1 and 0 by me: Madrid 2026 1 (probe-measured potential) and 2A (unnamed comms satellite), Canarias 2026 1a/1b1/1b2 (unnamed microsatellite) and 3 ("en un laboratorio"), Extremadura 2026 3 (lab velocity selector), 4 ("en un experimento"), 6 (photoelectric table), Valencia 2025 1B (unnamed space station), Andalucía 2025 C.b2 (container of water and oil), Andalucía 2026 C.b1 (projection on a screen); and the reverse, Asturias 2026 8 (a rock containing U-238) 0→1. These are all "does an unnamed device/lab count as a named real setting" — definitional, harmless for the headline.

**app (13)** — all definitional: I count musical instruments (flute, guitar, violin), unnamed satellites/space stations/spacecraft and a ship's sonar as applications; coder 1 does not; coder 1 counts a lab velocity selector, a "research project" on boron fission and a screen projection as applications; I do not. Either convention is fine if applied consistently, and each coder is internally consistent.

**explain (11)**
- Derivations: Andalucía 2025 B.a, D.a, 2026 C.a2, Canarias 2025 I.A ("demostrar", "deduzca y justifique"): 1→0. I treated derivations as calculation; given the scheme text ("not itself a calculation") I still prefer mine, but coder 1's reading of Andalucía's conceptual "a" sections is reasonable. Andalucía 2026 A.b ("responda razonadamente"): 1→0, mine.
- Image characteristics from ray tracing: Asturias 2025 5, 2026 6, Valencia 2025 5B: 0→1. Coder 1 coded the identical demand as explain=1 in Andalucía 2026 C.a1, CLM 2026 C1 and Extremadura 2025 5, so coder 1 is internally inconsistent here; mine.
- Trivial qualitative asks: Andalucía 2026 B.b2 (attractive/repulsive) 0→1 and Valencia 2025 5A ("what type of motion") 0→1 — coder 1 is probably right that these are not explanations; Valencia 2025 6A (A and Z of the daughter, "razonadamente") 1→0 — either.

**graph (4)**
- Cataluña 2025 3A: 0→1. The block depth (2 m) appears only in the figure; the official solution uses d_max = 2·tan θ_lim. Mine, confirmed.
- Madrid 2026 1: 1→0. The V(x) graph is displayed but the text states V(x) = −3x, so nothing has to be read off it. Mine. This weakens the chapter's remark that Madrid's obligatory item is "the one non-optional item with graph interpretation".
- País Vasco 2025 A1: 1→0. "Puedes comprobar tus resultados… utilizando la figura" is optional; the scheme says "must read data off". Mine (drops PV 2025 criteria/item from 0.86 to 0.71; no effect on the flag).
- CLM 2025 P2: 1→0. From the transcript the semicircle widths are given in the text; coder 1 saw the rendered page, so lean coder 1.

**evaluate (1)** — PV 2026 3b, see above.

## 3. Structure facts (all 18 papers) — verified

All of the first coder's structure facts check out against the texts: item counts (Canarias 2025 is 8 options = 11 numbered questions; both counts are correct at their own granularity), obligatory items, points per item, optional share: Cataluña 50/50; Madrid 75/75; Asturias 100/100 (5 of 8 × 2 pts); Andalucía 60 → 75 (a-sections became optional in 2026); Canarias 100 → 70 (obligatory 1a + 2 = 3 pts); Extremadura 75/75; Valencia 85 → 80; País Vasco 75 → 50; CLM 100 (internal 2-of-3 choice in every question) → 70 (A + B1 + C1 = 3 pts fixed). No mismatch in points or obligatory status on any item.

One latent weighting issue in `scripts/07_exam_coding.py`: the expected-exposure weight is `points / n_options`, and Asturias is entered with n_options = 8, so its weights sum to 2.0 instead of 10 (each item should weigh 2 × 5/8 = 1.25). It has no effect today because every Asturias item is competency = 0, but it would understate any Asturias competency item fivefold.

## 4. Paper-level comparison — expected competency share (% of 10 points)

| paper | coder 1 (`exp_share_competency`) | coder 2 | substantive-ctx share, coder 1 → 2 |
|---|---|---|---|
| País Vasco 2025 | 25.0 | 25.0 | 25 → 25 |
| País Vasco 2026 | 62.5 | 62.5 | 75 → 62.5 |
| Cataluña 2025 | 75.0 | 37.5 | 87.5 → 37.5 |
| Cataluña 2026 | 37.5 | 25.0 | 87.5 → 25 |
| Castilla-La Mancha 2025 | 0 | 0 | 0 → 0 |
| Castilla-La Mancha 2026 | 20.0 | 20.0 | 20 → 20 |
| Comunitat Valenciana 2025 | 15.0 | 15.0 | 15 → 15 |
| Comunitat Valenciana 2026 | 0 | 0 | 0 → 10 |
| Madrid 2025 / 2026 | 0 / 0 | 0 / 0 | 0 |
| Asturias 2025 / 2026 | 0 / 0 | 0 / 0 | 0 |
| Andalucía 2025 / 2026 | 0 / 0 | 0 / 0 | 0 |
| Canarias 2025 / 2026 | 0 / 0 | 0 / 0 | 0 |
| Extremadura 2025 / 2026 | 0 / 0 | 0 / 0 | 0 |

Changes 2025 → 2026 and correlation with the grade change: identical for eight of nine communities; Cataluña is −37.5 (coder 1) vs −12.5 (coder 2). r(Δcompetency, Δgrade) = −0.47 under both codings; r on criteria-per-item = −0.62 (coder 1) vs −0.73 (coder 2). Criteria per item, coder 2: PV 0.71 → 2.50, still the highest of the 18 (Cataluña 1.83 both years).

## 5. Verdict on Chapter 11's claims

**Survives, unchanged in every direction and in 16 of 18 levels:**
- País Vasco 25 → 62.5 % — identical (the two obligatory 2026 items are the only two in the whole set on which both coders score ctx=2, explain=1 and evaluate=1; the optional-item swap 3b/4b cancels).
- Castilla-La Mancha 0 → 20 % — identical (rests on reading "compare v_orb with v_esc" as an explanation; I made the same call).
- Valencia 15 → 0 — identical.
- Cataluña fell — direction identical (37.5 → 25 on my codes vs 75 → 37.5).
- Asturias, Madrid, Andalucía, Canarias, Extremadura 0 → 0 — identical; no coding decision anywhere in those ten papers gets close to a competency flag (no ctx=2 item exists in them under either coder).
- "Of the six rising communities only Castilla-La Mancha increased competency content, and by a fifth of the Basque step" — survives verbatim.
- "The Basque 2026 paper differs from its 2025 predecessor more than any other paper differs from its own" — survives (largest Δ on both competency share and criteria/item).

**Coder-sensitive wording that should be softened:**
- Cataluña's absolute level. "75 → 38 %" and "substantive-context share stayed above 85 %" rest on coding every Cataluña narrative as substantive; a stricter reader gets 37.5 → 25 and a substantive share of 25–37.5 %. The claim that Cataluña is the most contextualised paper (100 % of items carry a context) and that it did not change genre are unaffected; the sentence "the most competency-oriented paper in 2025" is stronger than the coding supports on its own — Cataluña 2025 and País Vasco 2026 are close (37.5 vs 62.5 with my codes; 75 vs 62.5 with coder 1's).
- Madrid 2026 obligatory item as a "graph-reading item": V(x) is given in the text, so the graph is decorative; this affects the CRUE "graph interpretation" remark, not the competency claim.
- "Asturias 2026 criteria-per-item 0.25, lowest of the eighteen": under my codes Madrid 2026 (0.29) is lowest and Asturias 2026 is 0.375; safer to say "among the lowest".
- The `ctx` 1/2 boundary is the least reliable element of the scheme (κ 0.61 on ctx==2, with the coders differing in strictness rather than at random). The chapter would be more defensible if it stated the inter-coder result and noted that the headline is insensitive to it: every direction of change, and the Basque and Castilla-La Mancha levels, are the same under both coders.

Overall: the chapter's central argument is robust to a second, stricter, blind coding; only the Cataluña magnitudes and two side remarks move.
</agent-message>