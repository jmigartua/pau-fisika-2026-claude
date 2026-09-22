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

**Status:** **implemented**, 21 September, together with R6 — the fix *is* an aside, so
rewriting the paragraph and building the margin were one job. Every number was right and
traceable; the paragraph was badly written, and the confusion was the paragraph's fault.

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

**Status:** **implemented**, 21 September. Decision taken: **the widened PDF with true side
notes**. The mechanism is built and used once, in the 2024 paragraph of both synthesis
documents; every later aside reuses it.

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

**Status:** **implemented**, 21 September, at the proposed sizes.

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

---

## R4 + R6 + R7, 21 September

**R4 — the 2024 paragraph, both languages.** It quoted three quantities and defined none.
It now does four things it did not do.

- It says what moved: the 8–10 band **fell 9.0 points where a fall of 0.21 in the mean
  normally costs 3.1**, and the pass rate **rose 2.3 where it would normally have fallen
  2.8**. Observed against expected, in both cases, rather than a bare number.
- It **names the third quantity**. The rank of 2 belongs to neither of the above: it belongs
  to the *conditional top-band residual* — how much top band a community has given its mean,
  against the other communities that year — which moved $-3.08$ standard deviations. The
  paragraph now introduces it before ranking it. The old sentence said "as a move of that
  measure" with no antecedent, in both languages.
- It gives **both ranks**: second of 170 on that residual, eleventh of 170 on the combined
  size of the two departures from the locus. The old text quoted the dramatic one alone.
- The method goes to the **margin**, not into the sentence: what the locus is, the four
  observed-against-expected figures, what the conditional residual is, why 170 and not 187,
  and the source file.

**R6 — the mechanism.** Quarto's `.column-margin` is used, so one piece of markup serves both
outputs, but neither output worked out of the box and both needed solving.

- *PDF.* The page is widened — `left=22mm, right=64mm, marginparwidth=50mm` — and the
  síntesis figures are marked `.column-page` so they span body **and** margin; without that
  the text column narrows from 162 mm to 124 mm and figure 1's annotations become illegible
  in print. Two consecutive notes then printed **on top of each other**: `marginnote`
  deliberately bypasses the margin-par mechanism, so `marginfix`, which manages `\marginpar`,
  could not see them. `\marginnote` is redirected to `\marginpar` and `marginfix` keeps the
  notes in order and apart. Long code paths were also overrunning the 50 mm column and are
  shortened, with the full paths left in Chapter 10.
- *HTML.* Quarto places `.column-margin` in the page grid's right margin — which is exactly
  where this theme keeps the sticky table of contents, so the two would have ridden over each
  other on scroll. The note is brought back into the text column and floated right, with
  `clear: right`, and falls back to a plain bordered block below 992 px. The PDF is untouched
  by that, the rule being HTML-only.

**R7 — the "In this page".** Entries 12 px → **11 px**, line-height 1.65 → 1.6; the heading
12 px → **10.5 px** with letter-spacing, so it reads as a label and not as another entry.

---

## Session of 21 September, continued

### R8 · The verdicts table: "el modelo competencial" is not one thing {#r8}

**Remark.** "I think that this table should be revisited. The idea, in my remarks and questions
regarding the features of the 2025 and 2026 exams: *el modelo competencial en la EHU ha sido
implementado completamente, cosa que en el resto no*, and with specific characteristics — so
for sure it is the model, with its characteristics. The re-structuration of the model gave
rise to some gaps in which the high schools were teaching, and the model with the recovery of
the complete syllabus."

**Status:** **implemented**, 21 September, as proposed and in all five places at once.
**The objection is correct, and the table contradicted the dossier's own measurements.** Two
distinct faults, one of them an internal contradiction inside a single document.

#### Fault one: the row treats the model as a uniform treatment, and the dossier says it is not

The row's warrant is *"se aplicó en las diecisiete comunidades los dos años; seis de nueve
subieron en 2026 con él"*. The first clause is true **of the law**. The second is offered as
evidence about the *model*, and it is not evidence about any paper, because the six that rose
are, five of six, communities whose papers **did not move in the competency direction at
all**:

| Rose in 2026 | Δ mean | Reform-intensity index |
|---|---:|---:|
| Asturias | $+1.13$ | $-0.19$ |
| Madrid | $+1.05$ | $-0.44$ |
| Castilla-La Mancha | $+0.94$ | $+0.39$ |
| Cataluña | $+0.80$ | $-0.72$ |
| Comunitat Valenciana | $+0.51$ | $-0.71$ |
| Andalucía | $+0.17$ | $-0.45$ |

Against **Euskadi at $+1.76$** — rank 1 of nine, more than four times the second, and the only
community that moved all four axes in the direction the orientations ask: optionality
$-25$ pp, competency marks $+37.5$, substantive context $+50$, contextualised marks $+75$
(`data/tables/reform_intensity.md`). Across the nine, the more a paper moved, the more its
mean fell: $r = -0.701$, $p = 0.035$.

**So the coordinator's distinction is the dossier's own finding.** The competency model *as a
national framework* was applied everywhere; the competency model *as EHU implemented it* was
applied in one place. The row uses evidence about the first to acquit the second.

**And the same document already says so.** The Spanish briefing states, four sections before
its own verdict table, that the nine "no son un grupo de control", that Euskadi is the only
community to move all four axes, and that $r = -0.70$ across the nine. The verdict row and
that paragraph cannot both stand as written. This is the 20 September lesson again: the
finding is in the dossier and has not reached the table the chief reads.

**One argument in the row does survive, and it sharpens rather than weakens the coordinator's
point.** The Jaume I rating places País Vasco and Cataluña among the *most* competency-oriented
papers **before** the reform, and Cataluña rose. But Cataluña did not move further in 2026 —
its index is $-0.72$, the lowest of the nine. What distinguishes Euskadi is therefore not
*being* competency-based but **becoming so, completely, in one year**. The rating is evidence
for the coordinator's reading, not against it.

**What must not be overstated, and the table must say it.** Euskadi is the extreme point on
both axes. Drop it and the association among the other eight is $r = -0.396$, $p = 0.332$ —
one community making the point, not eight agreeing. With $n = 9$ this is consistency, not
proof, and the corrected row has to carry that in the same breath as the correction.

#### Fault two: the reopened syllabus and the teaching gap are missing entirely

The second half of the remark — the restructuring creating gaps between what the schools were
teaching and what was examined — **is already in the dossier, stated precisely, and is in
none of the verdict tables.** [Chapter 12](12-ehu-paper-history.qmd) records that the
narrowing was *de facto*: no document ever excluded mirrors, standing waves or nuclear decay;
they simply were never set, and *"fifteen years of never being set is a stronger signal to a
school than any syllabus."* It also records the bound: in June 2026 the new sub-topics sat in
**optional** slots, so the effect acted through **preparation** — schools covering the
modern-physics block in full for the first time, and blocks C and D in a form that made the
option unpredictable — rather than through an unavoidable item.

The long briefing carries it in its components table as *"newly examined topics — not
identified (bounded: optional in June)"*. The síntesis carries it nowhere.

#### Proposal

Replace the single row with three, in all the places the argument appears.

1. **El modelo competencial como marco nacional** — *describe 2025; no puede explicar por sí
   solo una caída que solo tuvo Euskadi.* Warrant: applied in all seventeen both years; 14 of
   17 fell in 2025 with Euskadi milder; 2025 was the end of a subject-general plateau and
   cannot be separated from it. **The "six of nine rose" clause is kept but restricted to what
   it is evidence about**: the law, not any paper.
2. **El modelo competencial tal como lo implementó la EHU** — *variable de primer orden; es la
   explicación que el dosier menos puede descartar.* Warrant: the index of $+1.76$ against
   $+0.39$ for the next; the only community to move all four axes; $r = -0.701$ across the
   nine; the Jaume I rating read correctly. **Caveat in the same cell**: $r = -0.396$,
   $p = 0.332$ without Euskadi.
3. **El temario reabierto y la preparación de los centros** — *plausible, acotada, no medida.*
   Warrant: the fifteen-year *de facto* narrowing; the new sub-topics optional in June, so the
   channel is preparation and not an unavoidable item; bounded by option take-up, which is
   data request 5.

Row 2 of the present table, *"La prueba de 2026"*, then narrows to what is genuinely
format — length, optionality, genre — so that it no longer duplicates the new row 2.

**Where it has to be done.** The row appears in the English briefing (as H1), in both synthesis
documents, and the underlying argument in Chapter 6's hypothesis review. The Spanish briefing
has the correct analysis in its prose and the uncorrected verdict elsewhere. All of them move
together or the contradiction simply relocates.

**Implementation.** The single row is now three, and the format row narrows, in:

| File | Where | Form |
|---|---|---|
| `chapters/06-interpretation.qmd` | hypothesis review | H1 split into **H1a** (national frame), **H1b** (the EHU's implementation), **H1c** (reopened syllabus); H2 narrowed to length, optionality and genre |
| `chapters/14-briefing.qmd` | H-table, `#tbl-b-hyp` | same split; ranking caption rewritten |
| `chapters/14-briefing-es.qmd` | tabla H, `#tbl-e-hyp` | same split; ordenación reescrita |
| `chapters/15-synthesis.qmd` | `#tbl-s-hyp` | three rows replace one; "The 2026 paper **as a format**" |
| `chapters/15-synthesis-es.qmd` | `#tbl-ss-hyp` | three rows replace one; "La prueba de 2026 **como formato**" |

`onepage.qmd` inherits the change from chapter 6 on the next build.

**The ranking moved, which is the substantive consequence.** It read *H2 first, H1 a 2025
coincidence*. It now reads **H1b and H2 together at the front, not separable on published
aggregates because they are two descriptions of the same paper; H1c plausible behind them and
equally unseparable; H1a a 2025 coincidence.** Splitting the hypothesis moved half of it from
the back of the list to the front, because the objection that sank it — *everyone had the
model* — applies only to the frame. That is the whole of the coordinator's point, and the
dossier had the measurements to support it four sections before the table that denied it.

**The caveat travels with the claim, in the same cell, in all five.** $r = -0.70$, $p = 0.035$
across the nine; $r = -0.40$, $p = 0.33$ without Euskadi. One community making the point, not
eight agreeing.

---

### R9 · The COVID tint: one sitting or two {#r9}

**Remark.** "Settle this: the darker tint should cover both years, and the series' own shape
says it probably should. This is his to settle."

**Status:** **settled and implemented**, 21 September. The darker tint now covers **2020 and
2021**.

**Answer.** Two reasons, and the second is the stronger. The relief measures — reduced
syllabus, widened optionality, softened marking — were in force for *both* sittings, not for
the first alone, so "the COVID sitting" was never one year. And the series says so without
being asked: 2020 is 6.45, 2021 is **7.69** — the highest mean in seventeen years, 1.24 above
2020 and **1.63 above 2022**. If exactly one sitting were to be marked as anomalous it would
be 2021, so shading 2020 alone marked the wrong year. The peak now sits inside the tint, which
is what makes the figure argue its own case.

Implemented in `scripts/03_plots.py` (`axvspan(2019.5, 2021.5, ...)`, label recentred on
2020.5, model label moved to 2023.0), both languages regenerated, and the caption corrected in
all six places that carry it: `02-euskadi.qmd`, `14-briefing.qmd`, `14-briefing-es.qmd`,
`15-synthesis.qmd`, `15-synthesis-es.qmd`, `onepage.qmd`.

---

### R11 · Four remarks in one message, 21 September {#r11}

**Remark.** "Smaller the font size of the right side, En esta página!! · In the front
matter, take into account the changes we are doing; the document started on the 19th,
if I am not wrong, but today we are actualizing, every actualization should be taken
into account · I do not like the effect of the figures taking all the room in the
screen, I prefer as it was previously · Many figures in the briefing are still in
English · In Table 4 you have dropped the labels for the hypothesis, H1 etc."

**Status:** **all four implemented**, 21 September.

#### a. The index

10 px to **9 px**, heading 10.5 to **8.5**. Taken together with the body column at
880px, the index now occupies about a third less of the eye's field than it did
yesterday.

#### b. The front matter

Correction to the premise, on the record: the dossier opened on **18 September**, not
the 19th — `logs/WORK_LOG.md` and `data/` timestamps both say so; the 19th is when the
paper audits and the first external audit were added, which is probably the day being
remembered.

Every document now carries `date-modified` in its front matter, and Quarto prints it
under "Fecha de modificación" beside the publication date. The seven documents changed
today carry 2026-09-21; the rest keep the date of their own last change, so the field
means something rather than being stamped uniformly. The four documents the
coordination reads also carry a short **"Esta versión"** paragraph naming what each
day's revision did, with links to the work log and the record of remarks.

#### c. The figures

`.column-page` removed from all six figures that carried it. They return to the body
column — which is itself 160px wider than it was yesterday, so they lose less than the
class suggested. The PDF text block was widened to compensate (left 22→20mm,
right 64→58mm, margin column 50→44mm), since in the PDF the class was doing real work.

#### d. The Spanish figures

This is R1, outstanding since 20 September, and it is now done for every figure the
Spanish documents actually use: **fig03, fig10, fig23, fig25, fig26, fig28, fig29**,
joining fig01.

The mechanism is worth recording because it decides whether the two versions can drift.
Each script is run twice — once as it always has been, once with `PAU_LANG=es` — and
`plot_style.T()` looks each display string up in `scripts/es_strings.py`. The figure
code is untouched apart from wrapping its strings, so **the two versions cannot differ
in anything but wording**: same data, same fits, same layout, same file. A string with
no glossary entry falls through unchanged, which is what we want for numerals,
community names and file paths. `save()` refuses to write an `_es` file for any figure
not on the list the Spanish documents include, so no `_es` file can exist with English
still in it.

Three labels had to be shortened rather than translated literally, because Spanish runs
about a fifth longer than English and at full length they collided with the neighbouring
panel: the four term labels in fig26c, and both axis labels in fig28b. The shortenings
are recorded as comments in the glossary.

#### e. Table 4

The labels were dropped when the single row became three — an oversight, not a decision.
Restored, and **aligned with the briefing's numbering** rather than invented afresh:
H1a, H1b, H1c, H2, H2b (marking severity), H3 (tribunal severity), H4, H5, H6. Marking
severity is H2b and not H3 because in chapter 6 H3 has always been the tribunals; the
briefing and the synthesis now use one numbering, which they did not before this round.

---

### R12 · The index font, for the third time — and why the first two did nothing {#r12}

**Remark.** "That is the font whose font size I want smaller!!!!" — with the entries
circled.

**Status:** **fixed**, 21 September. The complaint was repeated twice because the fix
was never applied to the thing being looked at.

**What was wrong.** Both earlier rounds set `font-size` on `#TOC`, the container.
Quarto gives the index links a font-size rule of their own, so they never inherited it.
The container obediently went 11 px → 10 px → 9 px while the **links stayed at
14.875 px throughout**. Measured, not inferred:

| | before | after |
|---|---:|---:|
| Index links | **14.875 px** | **11 px** |
| Index heading | 8.5 px | 9.5 px |
| Left-hand nav | 12.5 px | 12.5 px |
| Body text | 13.8 px | 13.8 px |

The second row is the whole story: the index was **larger than the left-hand navigation
and larger than the body text**, which is backwards for something meant to sit quietly
beside the prose. Every reported symptom follows from that one number, including the
entries wrapping to three lines.

**The fix.** Set the size on the anchors, not the container — `#TOC a`, `.nav-link` and
the nested list items — with an id selector, so it wins on specificity without
`!important`. Second-level entries go to 10.5 px so the hierarchy reads. The heading
went *up* slightly, to 9.5 px in small caps, because at 8.5 px it had become smaller
than the entries beneath it, which is the same mistake in the other direction.

**The lesson, which is the one worth keeping.** A CSS change is not verified by reading
the stylesheet; it is verified by asking the browser what it computed for the element
the reader is actually looking at. One `getComputedStyle` call on the anchor would have
caught this the first time, and it is now the check used before reporting any style
change as done.

---

### R13 · The grey columns in the waterfall {#r13}

**Remark.** "In the image, I have a problem with this figure, which we have been
using all the time: what do the grey columns mean, represent?"

**Status:** **defect confirmed and fixed**, 22 September. The question exposed a
real error that had survived three audits.

**What they represented.** The 2025 and 2026 *levels*, 5.47 and 3.99, drawn as bars
from the bottom of the axes.

**Why that was wrong.** The axes do not start at zero. They start at 3.44 — a value
with no meaning, chosen only to frame the steps. So the columns had heights of
**2.03 and 0.55** for levels whose ratio is 1.37:1. Read as bars, they said the
2025 level was **3.7 times** the 2026 level: an overstatement by a factor of 2.7,
produced entirely by where the axis was cut. A bar's height reads as a magnitude,
and on a truncated axis that magnitude is an artefact.

Worse, they were also redundant: the two dotted rules already carry 5.47 and 3.99
across the panel, and both values are annotated.

**The fix.** The endpoints are now level *caps* — a short heavy mark at the value,
carrying no height at all. Nothing in the panel now encodes a quantity it should
not, and the coloured steps carry all the vertical weight, which is what a
waterfall is for.

**Two traps on the way, both worth recording.** Stripping the panel letter "c." for
the standalone versions failed twice. `ax.get_title()` returns the *centre* title
and this one is set with `loc="left"`, so the first attempt read an empty string.
The second attempt read it correctly but edited the rendered title, which
`plot_style` hands out as a LaTeX-wrapped object subclassing `str`: the edit
returned a plain string, which the style layer then escaped a second time,
printing `\{}textbf{` on the figure. The letter is now removed from the plain
translated string *before* `set_title` is called.

**Reach.** One panel, six files: `fig25_decomposition` and `fig25_decomposition_es`
in the dossier, `fig08_attribution_budget` and `_es` in the paper, and the deck's
`datos-presupuesto.png`. This is what the shared-panel discipline is for — the
correction was made once.

---

### R14 · Four challenges to the field comparison, and what the Cataluña archive settles {#r14}

**Remarks (22 September).** (a) The field is nine communities of seventeen — what if
the missing eight would pull the mean down? (b) In 2026 the others did not merely
fail to follow: they went backwards. (c) Castilla-La Mancha is not comparable —
2026 is *its* first year, as 2025 was ours. (d) What were Cataluña's papers before
2025?

**Status:** (a) closed with a test; (b), (c) accepted, and they change the wording of
the argument; (d) **settled with new evidence**, and it is the most consequential of
the four.

#### a. The eight that did not publish — testable, and tested

For 2015–2025 all seventeen are known, so the nine can be checked as a proxy for the
whole. Over ten transitions: mean error $-0.004$, sd $0.138$, largest error $0.242$,
$r = 0.943$. Essentially unbiased.

For the region-specific $-1.65$ to vanish, the missing eight would have to average
$-3.34$ in 2026: more than twice Euskadi's own fall, and three times the worst they
have ever collectively produced ($-0.99$, in 2025). Repeat that worst year exactly
and the component is still $-1.10$ — two thirds survives. The shift required is
**twelve standard deviations** of the historical error. The worry is legitimate and
quantitatively small; it belongs in the paper, which does not yet contain it.

#### b. The field retreated

The competency-coded share of marks across the other eight fell from **11.2 % to
7.2 %** between 2025 and 2026. Cataluña halved its own, 75 % → 37.5 %, while holding
total substantive context at 87.5 % — it kept the dressing and dropped the demand.
Comunitat Valenciana went to zero. Five were at zero and stayed. Only
Castilla-La Mancha rose, by 20 points.

This narrows the refutation. "Six of nine rose under the same decree" refutes that
**the decree** lowered marks. It says nothing about competency examining, because
almost nobody else did any. And the $-1.65$ is measured against a field moving the
other way, so it mixes *we advanced* with *they retreated*.

#### c. Castilla-La Mancha is stage one, not a counter-case

| | stage | competency share | Δ mean | Δ field | specific |
|---|---|---:|---:|---:|---:|
| Euskadi | 2025 — **first** year | 0 → 25 | $-0.62$ | $-0.65$ | $+0.03$ |
| Euskadi | 2026 — **second** year | 25 → 62.5 | $-1.48$ | $+0.17$ | $\mathbf{-1.65}$ |
| C.-La Mancha | 2026 — **first** year | 0 → 20 | $+0.94$ | $+0.17$ | $+0.77$ |

Both first years were harmless. The collapse is a second-year event. Comparing CLM's
2026 with Euskadi's 2026 compares stage one with stage two, which is not a
comparison — an error made and corrected here. **This also generates a prediction:**
if the mechanism is the depth of conversion in year two, CLM should fall in 2027 if
it goes deeper and not if it stays at 20 %.

Note that the marking-severity hypothesis predicts the same first-year/second-year
shape ("cautious in year one, full in year two"). Two hypotheses, one signature:
another instance of the collinearity, not an escape from it.

#### d. Cataluña had been examining this way since 2020

The ordinary papers for 2020–2025 were obtained from `examenesdepau.com` and are in
`data/catalunya/`; the measurement is `scripts/31_catalunya_history.py`.

| Year | Structure | Problems with a justification demand | Problems in a real setting |
|---|---|---:|---:|
| 2020 | 4 of 8 | 37.5 % | 37.5 % |
| 2021 | 4 of 8 | 62.5 % | 43.8 % |
| 2022 | 4 of 8 | 50.0 % | 50.0 % |
| 2023 | 4 of 7 | 50.0 % | 64.3 % |
| 2024 | 4 of 7 | 28.6 % | 85.7 % |
| 2025 | 4 exercises, A/B inside two | 66.7 % | 100 % |

Freddie Mercury's voice and the Apollo 15 feather (2020); Tycho Brahe (2021); an
eel's locomotion and a NASA launch (2022); Phobos and Deimos, and what the media
said about the 2022 fusion announcement (2023); BepiColombo and the altitude of a
Sant Joan firework (2024). Contexts and justification demands are present in every
year, five years before the decree.

**So Cataluña's 75 % in 2025 was not a conversion. It was steady state.** The
*structure* changed in 2025 — four block exercises with internal options, as the
decree asks — but the substance did not. Cataluña sat about $+0.65$ above the field
in both 2025 and 2026, with three quarters of its marks competency-coded and then
half that.

**What this does to the argument.** It is the strongest evidence in the study
against "competency examining lowers marks" as a general proposition: a neighbour
has examined that way for five years without a collapse. The weight moves onto the
**transition** rather than the paradigm — 0 → 25 → 62.5 in two years, with
optionality halved, the syllabus reopened and a new marking regime in its second
year, in a system with no prior experience of the style. H1b in the paper is
therefore worded too loosely: it should name this conversion, not the model.

**Limitation, stated because it bounds the claim.** 2025 and 2026 were coded blind
by two readers ($\kappa = 0.76$). 2020–2024 were coded once, by one reader, after
the result was known.
