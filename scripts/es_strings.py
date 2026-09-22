"""Spanish display strings for the figures the Spanish documents include.

R1 · The Spanish briefing and synthesis carried English figures. Rather than
fork the plotting scripts, each is run twice — once as before, once with
PAU_LANG=es — and `plot_style.T()` looks each display string up here. A string
with no entry falls through unchanged, which is what we want for numerals,
community names, LaTeX fragments and file paths.

Conventions. Spanish PAU usage puts the decimal separator on the point, not
the comma, so numerals are never reformatted here: they are produced by the
same f-strings in both languages. "Física" keeps its accent; "Euskadi" is the
name used for País Vasco throughout the dossier, as the coordination uses it.
Titles keep sentence case, matching the English.
"""

ES = {
    # ---------------------------------------------------------------- fig03
    "Ordinary-sitting Physics mean (open = 2025, filled = 2026)":
        "Nota media de Física, convocatoria ordinaria (hueco = 2025, relleno = 2026)",
    "2025 → 2026 by region: nine communities have published a 2026 Physics mean":
        "2025 → 2026 por comunidad: nueve han publicado una media de Física de 2026",
    "press": "prensa",

    # fig10 bar overlay
    "pass": "aprobados",

    # ---------------------------------------------------------------- fig10
    "2º Bachillerato Física\n2024-25 (school marks)\nn = 4 541":
        "2.º Bachillerato Física\n2024-25 (notas de centro)\nn = 4 541",
    "PAU Física 2025\nordinary\nn = 2 189":
        "PAU Física 2025\nordinaria\nn = 2 189",
    "PAU Física 2026\nordinary\nn = 2 066":
        "PAU Física 2026\nordinaria\nn = 2 066",
    "Mean grade": "Nota media",
    "Same subject, three measurements: school marks vs entrance exam (Euskadi)":
        "La misma materia, tres medidas: notas de centro frente a prueba de acceso (Euskadi)",
    "Sources: Gobierno Vasco 'Resultados escolares 2024-2025'; Ministry EPAU 2025; EHU 6 Jul 2026. Cohorts are offset by one year.":
        "Fuentes: Gobierno Vasco, «Resultados escolares 2024-2025»; EPAU del Ministerio 2025; EHU, 6-VII-2026. Las promociones están desfasadas un año.",

    # ---------------------------------------------------------------- fig23
    "Euskadi Física, ordinary sitting": "Física en Euskadi, convocatoria ordinaria",
    "Year": "Año",
    "Mean Física mark, ordinary sitting": "Nota media de Física, convocatoria ordinaria",
    "a. Two scenarios for 2027; the error bar is the year-to-year term, not a prediction interval":
        "a. Dos escenarios para 2027; la barra de error es el término interanual, no un intervalo de predicción",
    "Effect on the mean Física mark": "Efecto sobre la nota media de Física",
    "b. Why the estimate cannot be sharpened": "b. Por qué la estimación no puede afinarse más",
    "the cohort signal is %.1f times smaller\nthan the band it has to be read against":
        "la señal de la promoción es %.1f veces menor\nque la banda contra la que hay que leerla",

    # ---------------------------------------------------------------- fig25
    "Euskadi, 2016–2025": "Euskadi, 2016–2025",
    "Change of level: Δ mean mark": "Cambio de nivel: Δ nota media",
    "Change of shape: Δ top band minus what\nthe level alone predicts (pp)":
        "Cambio de forma: Δ banda alta menos lo que\npredice el nivel por sí solo (pp)",
    "a. Two different kinds of year": "a. Dos clases distintas de año",
    "the locus": "el lugar geométrico",
    "observed": "observado",
    "what the level alone predicts": "lo que predice el nivel por sí solo",
    "Change, percentage points": "Cambio, en puntos porcentuales",
    "b. 2024 moved off the locus; 2025 moved along it":
        "b. 2024 se salió del lugar geométrico; 2025 se movió sobre él",
    "Mean Física mark": "Nota media de Física",
    "c. What the 2026 fall is made of — and how much of it is still unattributed":
        "c. De qué está hecha la caída de 2026 — y cuánto sigue sin atribuir",

    # ---------------------------------------------------------------- fig26
    "change in the subject mean, 2025 → 2026 (marks)":
        "cambio de la media de la materia, 2025 → 2026 (puntos)",
    "(a) One sitting, eight subjects\nquantitative (orange) vs the rest ":
        "(a) Una convocatoria, ocho materias\ncuantitativas (naranja) frente al resto ",
    "Física = own mean": "Física = su propia media",
    "community's mean change over the three shared subjects (marks)":
        "cambio medio de la comunidad en las tres materias comunes (puntos)",
    "change in Física (marks)": "cambio en Física (puntos)",
    "(b) Euskadi is low on both axes\nthe fall is not only Física's":
        "(b) Euskadi está baja en los dos ejes\nla caída no es solo de Física",
    "marks": "puntos",
    "Figure 26 — Is the 2026 fall Física's, or Euskadi's?":
        "Figura 26 — ¿La caída de 2026 es de Física o de Euskadi?",

    # ---------------------------------------------------------------- fig28
    "Euskadi": "Euskadi",
    "Spain": "España",
    "PISA round (the cohort sits the PAU two years later)":
        "Ronda PISA (la promoción hace la PAU dos años después)",
    "PISA science points per cohort-year":
        "Puntos PISA de ciencias por año de promoción",
    "(a) Steps, not a slope\nEuskadi: $+3.7$ to $-7.5$ a year":
        "(a) Escalones, no una pendiente\nEuskadi: de $+3.7$ a $-7.5$ al año",
    "absolute standard": "criterio absoluto",
    "relative (top $q$ always)": "relativo (siempre el $q$ superior)",
    # Shortened against the English: Spanish runs about a fifth longer, and at
    # full length these two ran into the neighbouring panels.
    "share of the cohort sitting Física (per cent)":
        "presentados a Física (por ciento)",
    "fraction of the population shift reaching the candidates":
        "fracción del desplazamiento\nque llega a los presentados",
    "marks, one year ahead": "puntos, a un año vista",
    "Figure 28 — A rate of cohort decay, and what it can and cannot ":
        "Figura 28 — Una tasa de declive de la promoción, y qué puede y qué no puede ",

    # ---------------------------------------------------------------- fig29
    "target 2027": "objetivo 2027",
    "statement words (weights and furniture removed)":
        "palabras de enunciado (sin pesos ni elementos fijos)",
    "competency item": "ítem competencial",
    "(a) The long item is the competency item\n":
        "(a) El ítem largo es el ítem competencial\n",
    "slide 8 (forward)": "diapositiva 8 (hacia adelante)",
    "slides 9–11 (reverse)": "diapositivas 9–11 (hacia atrás)",
    "target band": "banda objetivo",
    "habitual": "habitual",
    "competencial": "competencial",
    "broken out": "desglosado",
    "statement words": "palabras de enunciado",
    "(b) Two reconstructions of B1\nsame endpoint, different rungs":
        "(b) Dos reconstrucciones de B1\nmismo punto final, peldaños distintos",
    "read (options included)": "leídas (con las opciones)",
    "answered (four problems)": "respondidas (cuatro problemas)",
    "Figure 29 — Where the reading is, and what the 2027 target costs":
        "Figura 29 — Dónde está la lectura, y qué cuesta el objetivo de 2027",
}

# Appended: the remaining fig23 terms and the long source notes. Kept separate
# from the block above only because they were collected in a second pass.
ES.update({
    "2027 paper like 2025's": "prueba de 2027 como la de 2025",
    "2027 paper like 2026's": "prueba de 2027 como la de 2026",
    "Cohort, from PISA 2025\n(prorated 2022→2025)":
        "Promoción, desde PISA 2025\n(prorrateado 2022→2025)",
    "Decade of cohort drift\n(PISA 2012→2025, full)":
        "Una década de deriva de promoción\n(PISA 2012→2025, completa)",
    "Everything else, one year\n(Euskadi's own year-to-year SD)":
        "Todo lo demás, un año\n(desviación típica interanual de Euskadi)",
    "Everything else, 2025→2027\n(95 % band, random-walk assumption)":
        "Todo lo demás, 2025→2027\n(banda del 95 %, supuesto de paseo aleatorio)",
    "What 2026 actually did\nin a single year":
        "Lo que hizo 2026 en realidad\nen un solo año",
})

# fig25 · the decomposition waterfall and the two panels above it.
ES.update({
    "the other {n} communities, {k} transitions":
        "las otras {n} comunidades, {k} transiciones",
    "top band\n2023→2024": "banda alta\n2023→2024",
    "pass rate\n2023→2024": "aprobados\n2023→2024",
    "top band\n2024→2025": "banda alta\n2024→2025",
    "pass rate\n2024→2025": "aprobados\n2024→2025",
    "Euskadi 2025": "Euskadi 2025",
    "Common to\nthe nine": "Común a\nlas nueve",
    "Choice\nremoved": "Elección\nretirada",
    "Cohort\n(PISA)": "Promoción\n(PISA)",
    "Not yet\nidentified": "Sin\nidentificar",
    "Euskadi 2026": "Euskadi 2026",
    "Basque-specific: {b:+.2f}.  Quantified: {q:.2f}.  Unattributed: {u:.2f} ({pc:.0f} %).":
        "Específicamente vasco: {b:+.2f}.  Cuantificado: {q:.2f}.  Sin atribuir: {u:.2f} ({pc:.0f} %).",
})

# fig26 · the subject decomposition.
ES.update({
    "(blue)": "(azul)",
    "Field core\n(3 subjects)": "Base\n(3 materias)",
    "Field Física\npremium": "Prima de\nFísica",
    "Euskadi-common\ndeviation": "Común de\nEuskadi",
    "Física-specific\ndeviation": "Propio de\nFísica",
    "(c) The four terms sum to {t:+.2f}\nexact identity, no fitting":
        "(c) Los cuatro términos suman {t:+.2f}\nidentidad exacta, sin ajuste",
})

# fig28 · the cohort rate.
ES.update({
    "take-up {q:.1f} per cent\ntransfer {t:.2f}":
        "presentados {q:.1f} por ciento\ntransferencia {t:.2f}",
    "(b) The rule matters: 0.23 or 1.00\nflat take-up favours the relative rule":
        "(b) La regla importa: 0.23 o 1.00\ncon presentados estables gana la regla relativa",
    "Cohort term,\nexcess of the field": "Término de promoción,\nexceso sobre el conjunto",
    "Cohort term,\ngross Basque move": "Término de promoción,\nmovimiento vasco bruto",
    "One SD of\npaper-to-paper variation": "Una desviación típica de\nvariación entre pruebas",
    "95 per cent band of the\npaper alone, one year": "Banda del 95 por ciento de la\nprueba sola, un año",
    "(c) The cohort is worth {c:.2f} a year,\nthe paper {p:.2f}":
        "(c) La promoción vale {c:.2f} al año,\nla prueba {p:.2f}",
    "anticipate": "anticipar",
})

# fig29 · the statement budget.
ES.update({
    "2025: A1, 423 words. 2026: B1, 413": "2025: A1, 423 palabras. 2026: B1, 413",
    "habitual\n+ figure": "habitual\n+ figura",
    "competencial\nideal": "competencial\nideal",
    "sin\nnarrativa": "sin\nnarrativa",
    "2026, as\nissued": "2026, tal\ncomo salió",
    "2025\nas issued": "2025, tal\ncomo salió",
    "2026\nas issued": "2026, tal\ncomo salió",
    "2027\ntarget": "2027\nobjetivo",
    "(c) The 2027 budget\n{a} → {b} read, a cut of {c:.0f} per cent":
        "(c) El presupuesto de 2027\n{a} → {b} leídas, un recorte del {c:.0f} por ciento",
})

# Figure source notes, verbatim keys.
ES.update({
    "PISA 2025 (OECD, published 8 September 2026; INEE Spanish tables, figure 2.1) gives País Vasco 458.5 in science against Spain's 477.1 — a fall of 21.0 points from 2022.\nThe cohort term converts that at one standard deviation of PISA to one of the PAU, the relation figure 22 could not reject and could not establish, prorated over the\ntwo years between the PAU cohorts. The paper term is the standard deviation of Euskadi's own year-to-year change excluding 2026. Neither scenario is a prediction.":
        'PISA 2025 (OCDE, publicado el 8 de septiembre de 2026; tablas españolas del INEE, figura 2.1) da al País Vasco 458.5 en ciencias frente a los 477.1 de España — una caída de 21.0 puntos desde 2022.\nEl término de promoción convierte eso a razón de una desviación típica de PISA por una de la PAU, la relación que la figura 22 no pudo rechazar ni establecer, prorrateado sobre los\ndos años que separan las promociones de la PAU. El término de la prueba es la desviación típica del cambio interanual de Euskadi excluido 2026. Ninguno de los dos escenarios es una predicción.',
    "Ministry EPAU, ordinary sitting. Panels a and b: specific phase, 17 communities, locus fitted on all 187 region-years. Panel c: pooled phase, the nine communities with a 2026 result in every year.\nThe choice term is a simulation of the two formats at item SD 0.2 net of the other eight communities' own cuts; the cohort term is the Basque PISA 2022–2025 decline in excess of Spain's, one PAU year of it, transferred one-for-one.\nBoth are differences from the field, because the quantity they are subtracted from is one. Neither is a causal estimate.":
        'EPAU del Ministerio, convocatoria ordinaria. Paneles a y b: fase específica, 17 comunidades, lugar geométrico ajustado sobre las 187 observaciones comunidad-año. Panel c: fase común, las nueve comunidades con resultado de 2026 en todos los años.\nEl término de la elección es una simulación de los dos formatos con desviación típica por ítem de 0.2, neta de los recortes propios de las otras ocho comunidades; el término de promoción es la caída vasca en PISA 2022–2025 en exceso de la de España, un año de PAU de ella, transferida uno a uno.\nLos dos son diferencias respecto del conjunto, porque la cantidad de la que se restan es una. Ninguno es una estimación causal.',
})
