# Remarks and questions from the coordination, with answers

A running log. Each item keeps its number for the life of the project. Nothing in an item
is acted on until the coordinator refers to it by number and says so; an item that is never
referred to again is never implemented.

**Status values.** `open` — answered, awaiting a decision. `agreed` — to be implemented.
`implemented` — done, with the commit named. `dropped` — decided against.

---

## Session of 21 September 2026

---

## Sequence agreed, 21 September

The coordinator's instruction: **change the figures that are to change first, and only then
produce their Spanish versions** — so that no figure is translated twice. R1 is therefore
split: the figures that R2 and R3 alter are translated after those items are implemented;
the rest can be translated at any time.

Working order: **R2 + R3** (one redraw of figure 1) → **R4** → **R5** → **R6** → **R1 for
figure 1** → **R1 for the other seven** → **R7** (independent of everything else).

One item at a time: the change is proposed, agreed, implemented, and its status updated here.

---

### R1 · The figures in the Spanish documents are in English {#r1}

**Remark.** "The figures from the set of figures that are going to the Spanish versions of
the reports — do the Spanish versions."

**Status:** `fig01` **implemented**, 21 September, in the same pass as R2 and R3: the figure
is now built twice from one string table, `fig01_euskadi_series.png` (English) and
`fig01_euskadi_series_es.png` (Spanish), and the two Spanish chapters point at the second.
The other seven figures remain **open**.

**Answer.** Correct, and it is a real defect rather than an oversight of style. Every figure
in the dossier is generated once, in English, by the plotting scripts, and the *same PNG* is
included in both language versions of every chapter. So the Spanish briefing and the Spanish
synthesis — the two documents that go to the admissions office — carry English titles, axis
labels, legends and in-plot annotations throughout.

**Scope.** Eight distinct figures appear in the two Spanish documents:

| Figure | Script | Appears in |
|---|---|---|
| `fig01_euskadi_series` | `03_plots.py` | briefing ES, síntesis ES |
| `fig03_regions_2026_vs_2025` | `03_plots.py` | briefing ES |
| `fig10_school_vs_pau` | `03_plots.py` | briefing ES |
| `fig23_pau2027` | `17_pau2027_estimator.py` | briefing ES |
| `fig25_decomposition` | `21_decay_decomposition.py` | briefing ES |
| `fig26_subject_decomposition` | `22_subject_decomposition.py` | briefing ES, síntesis ES |
| `fig28_cohort_rate` | `24_cohort_rate.py` | briefing ES |
| `fig29_statement_budget` | `25_statement_budget.py` | briefing ES, síntesis ES |

**What it would take.** Each of those six scripts would take a language switch and emit a
second file (`fig01_euskadi_series_es.png` and so on) with every string translated; the two
Spanish chapters would then point at the `_es` files. The cleanest way is a small string
table per script rather than a translation layer, because the strings are few and some are
LaTeX. The decimal convention already differs by language in the dossier's prose (points in
Spanish, per the PAU convention) and the figures would have to follow it.

**One decision needed.** Whether the Basque-language material, if any of these documents is
ever produced in Basque, gets a third set — in which case the string table should be built
for three languages from the start rather than two.

---

### R2 · Figure 1 of the síntesis: add the 2026 field and show the two falls {#r2}

**Remark.** "In that figure the mean in Spain should be added, for 2026, and then show the
decays; graphically it is very visual — arrows in vertical on the right side?"

**Status:** **implemented**, 21 September — awaiting the coordinator's sight of the figure
before the site is re-rendered and the change committed. Decision taken: **the nine, Euskadi
included**, so that the $-1.65$ every document quotes is the figure drawn.

**Answer, part one: what exists for 2026.** The grey line in that figure is *Spain, all
seventeen communities, from the Ministry EPAU cube*, and it stops at 2025 because **the 2026
cube is not published until June 2027**. There is therefore no "Spain 2026" to add.

What does exist is this study's own assembled cross-section: the **nine communities that have
published a 2026 result**. That is a different object from the grey line — nine communities
instead of seventeen, assembled from official pages, press reports and dashboards of varying
quality, and on a mix of bases (presented, eligible students, chart labels). Continuing the
grey line into 2026 with it would splice two different populations at precisely the year the
whole argument turns on, which is the one thing the figure must not do. **It should be drawn
as a separate, visibly different mark** — a second colour or an open marker for 2025–2026
only — and labelled *las nueve comunidades con resultado de 2026 publicado*.

**Answer, part two: the numbers.**

| | 2025 | 2026 | change |
|---|---:|---:|---:|
| Euskadi | 5.47 | 3.99 | **$-1.48$** |
| The nine, **including** Euskadi | 5.69 | 5.86 | **$+0.17$** |
| The eight, **excluding** Euskadi | 5.72 | 6.09 | $+0.38$ |

The dossier's $-1.65$ is $-1.48$ minus $+0.17$, that is, Euskadi against a field that
*contains Euskadi*. Measured against the eight others alone it would be $-1.86$. The
dossier uses the nine deliberately, because it is the more conservative of the two and
because the nine are a fixed comparison population in every year back to 2015. Worth
knowing before the figure is drawn, because the caption has to say which one the arrow is.

**Answer, part three: the arrows, and the trap in them.** Two vertical arrows on the right,
one per series, is exactly the right picture, but they must be arrows of **change**, each
running from its own 2025 point to its own 2026 point — Euskadi down 1.48, the field up 0.17
— with a bracket between the two arrowheads labelled $-1.65$.

What must **not** be drawn is a single arrow between the two 2026 levels. That distance is
$5.86 - 3.99 = 1.87$, not 1.65, because the two series did not start level in 2025 (5.47
against 5.69, a gap of 0.22). An arrow of that length labelled "the Basque-specific fall"
would be wrong by 0.22 of a mark, and it is the kind of error a reader would never catch.

---

### R3 · Figure 1: are the shaded bands really regime changes? {#r3}

**Remark.** "Are the *sombreados* actual regime changes? If it is the case, indicate. And
the first image contains information that can be translated to this figure also: some
opacity marking the zones of the Laws, upper half; and in the lower half, the opacities
indicating the models of exam. It is richer."

**Status:** **implemented**, 21 September, together with R2 — one redraw. Decision taken: a
**two-row ribbon between the panels**. One law span was assumed rather than confirmed and is
flagged below.

**Answer, part one: no, they are not all regime changes, and they are not the same kind of
thing.** The six bands in figure 1 are `PAU 2010–11`, `PAU 2012–16`, `EAU (LOMCE)`, `COVID`,
`post-COVID`, `LOMLOE` (`scripts/03_plots.py`, line 35). Sorted by what they actually are:

- **Law:** `EAU (LOMCE)`, `LOMLOE`. Two of six.
- **Exam format, decided locally:** `PAU 2010–11` (two whole options A/B), `PAU 2012–16`.
- **Circumstance, neither law nor format:** `COVID`, `post-COVID`.

So a reader is shown one shading channel carrying three different kinds of fact, with no way
to tell them apart, and the labels do not say which is which. `post-COVID` in particular
looks like a regime and is not one: the four-of-eight format ran from 2020 to 2024 across
both the `COVID` and `post-COVID` bands, so the boundary drawn at 2021/22 is a boundary of
*circumstance* inside an unchanged exam.

**Answer, part two: the two-layer proposal.** Splitting the channel as you describe — laws
in the upper half of the plot area, exam models in the lower half — fixes exactly that, and
it is strictly more informative than the present single band. The material for the lower
layer already exists and is already correct in **figure 14** (chapter 12, *Sixteen years of
one paper*), which codes the formats properly as `Two whole options A/B: 2 problems (3) + 2
theory questions (2)`, `Four-of-eight: any 2 of 4 problems, any 2 of 4 questions`, and
`LOMLOE` split into its 2025 and 2026 forms. Figure 14 also carries a second panel with the
points awarded through closed-list theory questions and the optional share of the paper,
which is the other half of what makes it richer.

**Two notes on doing it.** First, the law bands and the format bands do **not** coincide:
LOMCE's exam (EAU) ran 2017–2019 while the four-of-eight format began in 2020, and LOMLOE's
first paper is 2025 while its second changes format again in 2026. That non-coincidence is
itself one of the dossier's points and a two-layer shading is what would let a reader see it.
Second, COVID then has nowhere to live in either layer, which is correct — it belongs as a
marked pair of years, not as a regime.

---

### R4 · The 2024 paragraph: where do those numbers come from? {#r4}

**Remark.** Quoting the síntesis: *"2024 cambió la forma y apenas tocó el nivel… la banda de
8 a 10 cayó nueve puntos donde el nivel predice tres, y la tasa de aprobados subió dos donde
el nivel predice una caída de tres… Como movimiento de esa medida es el segundo más negativo
de las 170 transiciones del panel nacional."* — "I do not understand very well that text;
where are those numbers coming from?"

**Status:** open. **Every number is right and traceable; the paragraph is badly written, and
the confusion is the paragraph's fault, not the reader's.**

**Answer, part one: the numbers.** All from `data/analysis/decomposition.json`,
`typology.pais_vasco.2024`, computed by `scripts/21_decay_decomposition.py`:

| Quantity | Value | In the text as |
|---|---:|---|
| `d_mean` | $-0.21$ | "la media se movió 0.21" |
| `d_top` (share in $[8,10]$, 2023 → 2024: 34.70 → 25.67) | $-9.03$ pp | "cayó nueve puntos" |
| `d_top_locus` | $-3.11$ pp | "donde el nivel predice tres" |
| `top_excess` | $-5.92$ pp | "seis puntos más de lo que el nivel implicaba" (briefing) |
| `d_pass` (70.71 → 72.99) | $+2.28$ pp | "subió dos" |
| `d_pass_locus` | $-2.76$ pp | "donde el nivel predice una caída de tres" |
| `pass_excess` | $+5.04$ pp | — |
| `dz` | $-3.0808$ | — |
| `rank_dz` | **2 of 170** | "el segundo más negativo" |
| `rank_shape` | 11 of 170 | — |

**What "el nivel predice" means.** A polynomial is fitted, across all **187 region-years** of
the panel, giving the share in $[8,10]$ as a function of the mean, and another giving the pass
rate as a function of the mean. That curve is the **locus**: it says what the shape of a
distribution normally is at a given level. `d_top_locus` is that curve evaluated at the 2024
mean minus the same curve at the 2023 mean. So "el nivel predice tres" means: *a community
whose mean falls by 0.21 normally loses about three points of its top band*. Euskadi lost
nine. And a community whose mean falls by 0.21 normally loses about 2.8 points of pass rate.
Euskadi **gained** 2.3. Fewer at the top and more just over the line, at an almost unchanged
mean — which is what "cambió la forma y apenas tocó el nivel" means.

**Answer, part two: the sentence that is genuinely broken.** *"Como movimiento de esa medida
es el segundo más negativo de las 170 transiciones"* — **"esa medida" has no antecedent.**
The rank of 2 does not belong to the $[8,10]$ band, and it does not belong to the pass rate.
It belongs to a **third** quantity the paragraph never names: `dz`, the year-to-year change
in the *conditional top-band residual*, measured against the field in the same year and
divided by that residual's standard deviation. Euskadi's moved $-3.08$ standard deviations
between 2023 and 2024, which is the second-most-negative of the 170 transitions, behind
Cantabria 2025 at $-3.98$.

The English version of the same paragraph has the identical fault ("As a move of that
measure"). Both should name the quantity.

**Answer, part three: something the paragraph does not tell the reader, and should.** There
are *two* rankings of 2024 in the data and the text quotes only the more dramatic one. On the
conditional residual it ranks **2nd of 170**. On the combined size of the two excesses
(`rank_shape`, $|{-5.92}| + |{+5.04}|$) it ranks **11th of 170**. Both are in the JSON, both
are defensible measures of "a large move", and quoting "second" without saying that another
reasonable measure says "eleventh" is the kind of selection this dossier has criticised
elsewhere. Chapter 6 does give both; the síntesis gives one.

**"170 transitions"** is 17 communities × 10 year-to-year steps (2015→2016 … 2024→2025). The
187 region-years mentioned elsewhere is 17 × 11 years; the panel has one fewer transition
than it has years, per community.

---

### R5 · The 2025 and 2026 paragraphs {#r5}

**Remark.** Quoted without a question attached: *"2025 cambió el nivel, y el cambio fue del
país. Euskadi perdió 0.62; el conjunto de las nueve perdió 0.65. Leído contra el conjunto, en
2025 no hay nada vasco."* and *"2026 es nuestro. El conjunto ganó 0.17 y nosotros perdimos
1.48, de modo que el componente específicamente vasco es $-1.65$, y está entero en un año."*

**Status:** open — **and it is not clear what is being asked.** Recorded as quoted. My reading
is that these were included because they are the rest of the same passage and should be
checked alongside R4; if something specific is wrong with them, say so against this number.

**Answer, such as it is.** The arithmetic checks: Euskadi $5.47 - 6.09 = -0.62$; the nine
$5.6889 - 6.3356 = -0.6467 \approx -0.65$; for 2026 the nine $5.8582 - 5.6889 = +0.1693
\approx +0.17$ and $-1.48 - 0.17 = -1.65$.

**One thing worth flagging without being asked.** "El conjunto" is the mean of the **nine
communities including Euskadi**. So the $+0.17$ is a field average that contains the
community that fell 1.48, which drags it down: the eight others alone rose $+0.38$, and
against them the Basque-specific component would be $-1.86$ rather than $-1.65$. The dossier
chooses the conservative direction on purpose, but neither the síntesis nor the briefing says
that Euskadi is inside the field it is being compared with. Two words — *"las nueve,
nosotros incluidos"* — would fix it, and it makes the argument stronger rather than weaker,
since the figure quoted is the smaller of the two.

---

### R6 · The method explanations belong in the síntesis, as asides {#r6}

**Remark.** "Change the text to be understandable; and the explanations about the numbers,
those explanations coming from the methods etc. that you have described in the log — take
them as asides, give them room in the síntesis, to the right."

**Status:** open.

**Answer.** Agreed, and it is the right instrument for exactly this material. The síntesis
is written to be read before a meeting, so a paragraph cannot stop to define a locus or a
standardised residual; but a reader who wants to know where a number came from should not
have to open Chapter 6 either. A margin column holds the provenance beside the claim without
interrupting the claim.

**What would go in the margin**, drawn from R4 and R5 above: what the *locus* is and what
"el nivel predice" therefore means; what the conditional residual is and why its rank is a
statement about a third quantity; that the panel has 187 region-years and 170 transitions and
why those differ; that the field includes Euskadi; and the source file behind each block.

**One decision this needs, because of the PDF.** The síntesis renders to HTML *and* to PDF
(`scrartcl`, `margin=24mm`). In HTML a right-hand margin column is native. In PDF, a 24 mm
margin has no room for one, so either the page geometry widens to carry a true side column —
Tufte-style, and it would change the look of the printed document — or the asides become
footnotes in the PDF while staying in the margin in HTML. The second keeps the printed
document as it is; the first is better to read. This has to be chosen before the first aside
is written, because the two are marked up the same way but sized differently.

---

### R7 · Reduce the font size of the right-hand "In this page" {#r7}

**Remark.** "By the way, a style change for the website: diminish the font size of the text
in the *In this page*."

**Status:** open. Independent of every other item; can be done at any point.

**Answer.** The rule is in `styles.scss`: `#TOC { font-size: 12px; line-height: 1.65; }` with
`#TOC h2 { font-size: 12px; }` for the heading itself. Both are 12 px, which is why the
heading does not read as a heading and the whole block competes with the body text.

**Proposal.** Entries to **11 px** with line-height 1.6, and the "In this page" heading to
**10.5 px** with its existing letter-spacing, so the heading reads as a label rather than as
another entry. A smaller step (11.5 px) is available if 11 px proves too light on a
high-resolution screen; the dark stylesheet inherits the size and needs no change.

---

## What was done on 21 September, and what it needs from the coordinator

**R2 + R3 + R1(fig01), one redraw of `fig01_euskadi_series`.** In `scripts/03_plots.py`, the
figure is now a function called once per language.

- The six mixed bands are gone. In their place a two-row ribbon between the panels: **ley**
  — PAU (RD 1892/2008) 2010–2016, EAU (LOMCE) 2017–2024, LOMLOE 2025–2026 — and **modelo** —
  dos opciones completas A/B 2010–2019, cuatro de ocho 2020–2024, L1 2025, L2 2026. Row
  dividers are drawn only inside their own row, so a law boundary no longer cuts a model
  label. A marked interval under the ribbon says *la ley cambió en 2017; el examen, en 2020*.
- **COVID** is no longer a regime: 2020 and 2021 are a light pair of years labelled
  *convocatorias COVID*, across both panels.
- The **nine-community 2026 field** is drawn detached, dashed and open-markered, for 2025 and
  2026 only, and the source note says the Ministry cube is not published until June 2027.
- The **two falls** are arrows from a common origin, Euskadi's own 2025 mean of 5.47: the
  blue arrow falls to 3.99 ($-1.48$), the green arrow rises to 5.64 ($+0.17$, *moviéndonos
  con el conjunto*), and the bracket between the two heads is $-1.65$ exactly.
- Captions rewritten in all five places that use the figure, in both languages, each stating
  why the two ribbon rows are separate and why the bracket is not the distance between the
  two 2026 levels.

**A note for the audit.** The first drawing of this figure put the bracket between the two
2026 *levels* and labelled it $-1.65$. That distance is 1.87. It is precisely the error R2
was written to prevent, and it survived into a rendered figure before the check caught it —
which is the same lesson as the propagation gap of 20 September: **a defect named in prose is
not thereby prevented in practice.**

**One thing the coordinator must confirm.** The law spans are assembled from
`euskadi_regimes.csv` and `ehu_formats.csv`. `EAU (LOMCE)` running **2017–2024** is this
study's reading — LOMCE's evaluation from 2017, LOMLOE's first paper in 2025 — and the legal
dates are the coordinator's to fix. If any span is wrong the figure is one line to change.

### Corrections to the redraw, same day

The coordinator returned four faults in the first build. All four are fixed.

1. **Incoherent notation in the key.** `L1` read "3 × (1 de 2)" and `L2` read "2 × (a/b)".
   Both are the same structural fact — a block offering a choice of one of two — labelled
   differently only because the 2026 paper prints its options as *a/b*. The key now says
   "1 de 2" in both.
2. **The marked interval did not span the years it named.** It ran from the band boundaries,
   2016.5 to 2019.5, while its label named 2017 and 2020. It now runs from **2017 to 2020**.
3. **The COVID shading was the wrong span.** The pandemic sitting is one, 2020; the
   four-of-eight paper it forced was then kept through 2024. The shading now does both: a
   darker tint on the 2020 sitting and a lighter one across 2020–2024, the life of the model,
   which coincides exactly with the `cuatro de ocho` span in the ribbon below.
4. **The caption did not explain the arrows.** It said the arrows existed and not what they
   were. All five captions now state that the arrows are **changes and not levels**, name the
   colours (blue = Euskadi's own change, green = the field's), explain why both leave the same
   origin and what the green arrowhead at 5.64 therefore means, give the 1.87 that the gap
   between the two 2026 levels would wrongly measure, say that the field includes Euskadi and
   what the figure would be without it, and name the source: the `total`, `common` and
   `basque_specific` terms of `data/analysis/decomposition.json`.

**One question back to the coordinator, raised rather than assumed.** The pandemic sitting is
taken as 2020 on his instruction. The dossier's own anomaly, however, is **2021**: 7.69 and
89.6 per cent, the highest pair in the sixteen-year series, against 6.45 and 75.2 in 2020.
If 2021 was also sat under pandemic arrangements, the darker tint should cover both years,
and the series' own shape says it probably should. This is his to settle.
