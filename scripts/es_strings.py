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


# R23 · The three figures added on 21–23 September were written with English
# display strings and no `T()`, while their names had already been put into
# `plot_style.ES_FIGURES`. The allowlist was doing the opposite of its job: it
# let the pipeline write an `_es` file whose every word was English, and one of
# those files reached a Spanish slide. Wrapping the strings and filling them in
# here is the repair; the guard only works if both halves are done together.
ES.update({
    # ------------------------------------------------------------------ fig36
    "Extremadura $-0.82$\nCanarias $-0.83$":
        "Extremadura $-0.82$\nCanarias $-0.83$",
    "its 2025 paper: it had been\nnear here since at least 2020":
        "su prueba de 2025: ya estaba\ncerca de aquí desde 2020 al menos",
    "six communities at zero\nin both years":
        "seis comunidades a cero\nen los dos años",
    "Competency-coded share of the paper's expected marks (%)":
        "Puntos competenciales esperados de la prueba (%)",
    "Change in the ordinary-sitting Física mean, 2026 − 2025 (marks)":
        "Cambio de la media de Física, convocatoria ordinaria, 2026 − 2025 (puntos)",
    "Each community's route, 2025 → 2026: hollow point is 2025, filled point 2026":
        "El recorrido de cada comunidad, 2025 → 2026: el punto hueco es 2025; el relleno, 2026",
    "One measure on the horizontal axis throughout: the competency-coded share of expected marks, "
    "from the item coding of the eighteen ordinary papers.\nThe vertical axis is each community's own "
    "change, so every arrow starts at zero. Euskadi runs right and down; Cataluña runs left and up, "
    "from a position it had held for five years.":
        "Una sola medida en el eje horizontal: la proporción de puntos esperados codificados como "
        "competenciales, a partir de la codificación ítem a ítem de las dieciocho pruebas ordinarias."
        "\nEl eje vertical es el cambio propio de cada comunidad, de modo que todas las flechas parten "
        "de cero. Euskadi va a la derecha y hacia abajo; Cataluña, a la izquierda y hacia arriba, "
        "desde una posición que llevaba cinco años ocupando.",

    # ------------------------------------------------------------------ fig37
    "2010–2019   mean 17.7 %, sd 10.9":
        "2010–2019   media 17.7 %, desv. típ. 10.9",
    "2020–2023   mean 50.0 %":
        "2020–2023   media 50.0 %",
    "never zero: the lowest\nCatalan year is 6.2 %":
        "nunca cero: el año catalán\nmás bajo está en el 6.2 %",
    "items demanding\njustification (%)":
        "ítems que exigen\njustificar (%)",
    "a. The Catalan paper: one mechanical measure, sixteen years":
        "a. La prueba catalana: una medida mecánica, dieciséis años",
    "COVID\nsittings\nexcluded":
        "convocatorias\nde la COVID\nexcluidas",
    "shift $%+.2f$ — Welch $p=%.2f$, exact $p=%.2f$\n"
    "smallest shift detectable here: %.2f":
        "desplazamiento $%+.2f$ — Welch $p=%.2f$, permutación exacta $p=%.2f$\n"
        "menor desplazamiento detectable aquí: %.2f",
    "Cataluña $-$ field\n(marks)":
        "Cataluña $-$ conjunto\n(puntos)",
    "b. …and what it did to the mean, against the fifteen-community field":
        "b. …y qué le hizo a la media, frente al conjunto de quince comunidades",
    "A conversion that can be dated, and a cost that cannot be measured":
        "Una conversión que puede fecharse, y un coste que no puede medirse",

    # ------------------------------------------------------------------ fig38
    "best sinusoid $R^2$ on 11 points":
        "mejor $R^2$ sinusoidal sobre 11 puntos",
    "a. Fit a cosine to every community, and\n     Aragón fits better than Cataluña":
        "a. Ajústese un coseno a cada comunidad:\n     Aragón ajusta mejor que Cataluña",
    "the periods run 2.5 to 40 years.\nA common external driver would\nimpose a common period.\nThese do not agree.":
        "los periodos van de 2.5 a 40 años.\nUna causa externa común impondría\nun periodo común.\nEstos no concuerdan.",
    "Euskadi's own norm %+.2f":
        "norma propia de Euskadi %+.2f",
    "a shock: reverts":
        "un choque: revierte",
    "a level change: persists":
        "un cambio de nivel: persiste",
    "Euskadi $-$ field (marks)":
        "Euskadi $-$ conjunto (puntos)",
    "b. …and the one prediction a single\n     sitting can settle":
        "b. …y la única predicción que una sola\n     convocatoria puede zanjar",
    "separation %.1f$\\sigma$":
        "separación %.1f$\\sigma$",
    "A wave that eleven points cannot establish, and a reversion that 2027 will test":
        "Una onda que once puntos no pueden establecer, y una reversión que 2027 pondrá a prueba",
})

# fig38 / fig39 — the reversion panel, drawn twice.
ES.update({
    "%.0f y": "%.0f a",
    "What doing nothing predicts for 2027":
        "Lo que predice no hacer nada, para 2027",
    "Euskadi's position against the eight communities that published a 2026 mean, 2015–2026. "
    "Within a community the deviation from the field\nfollows an AR(1) with $\\phi = 0.186$: a shock "
    "gives back five sixths of itself in one year, a level change gives back none. The bars are "
    "95 % intervals\non an innovation sd of 0.47. A recovery of about a mark and a half in 2027 is "
    "what the panel predicts from changing nothing.":
        "Posición de Euskadi frente a las ocho comunidades que publicaron media de 2026, 2015–2026. "
        "Dentro de una comunidad, la desviación respecto del conjunto\nsigue un AR(1) con "
        "$\\phi = 0.186$: un choque devuelve cinco sextos de sí mismo en un año; un cambio de nivel no "
        "devuelve nada. Las barras son intervalos al 95 %\nsobre una desviación típica de la innovación "
        "de 0.47. Una recuperación de punto y medio en 2027 es lo que el panel predice si no se cambia nada.",
})

# fig40 — the examination week and the weighting table (finding 19).
ES.update({
    "martes": "martes",
    "miércoles": "miércoles",
    "45 min": "45 min",
    "Matemáticas II\nse mueve aquí": "Matemáticas II\nse mueve aquí",
    "borde discontinuo: las dos fuentes de 2025\nno coinciden en el día":
        "borde discontinuo: las dos fuentes de 2025\nno coinciden en el día",
    "a. What moved in the examination week":
        "a. Lo que se movió en la semana de exámenes",
    "the two papers made adjacent are the two that fell":
        "las dos pruebas que quedaron seguidas son las dos que cayeron",
    "grados de Ciencias, Ingeniería\ny Ciencias de la Salud codificados":
        "grados de Ciencias, Ingeniería\ny Ciencias de la Salud codificados",
    "Física pondera $0.2$": "Física pondera $0.2$",
    "…y Matemáticas II también": "…y Matemáticas II también",
    "…y Química también:\nlas tres a $0.2$, y solo caben dos":
        "…y Química también:\nlas tres a $0.2$, y solo caben dos",
    "grados (de 37)": "grados (de 37)",
    "b. “Se utilizarán las 2 calificaciones que sean más favorables”":
        "b. “Se utilizarán las 2 calificaciones que sean más favorables”",
    "Matemáticas II es obligatoria en la fase de acceso y se arrastra:\n"
    "una de las dos plazas está ocupada antes de elegir nada.\n"
    "En Ciencias de la Salud, Física pondera $0.1$ y Biología y Química $0.2$:\n"
    "ahí no hay contienda — Física no entra.":
        "Matemáticas II es obligatoria en la fase de acceso y se arrastra:\n"
        "una de las dos plazas está ocupada antes de elegir nada.\n"
        "En Ciencias de la Salud, Física pondera $0.1$ y Biología y Química $0.2$:\n"
        "ahí no hay contienda — Física no entra.",
    "Panel a: UPV/EHU timetables for the ordinary sitting, 2025 and 2026, with each subject's change in mean beneath its name. Física's own slot did not move — it was last on its day in both years — so what being last costs\ndifferences out. What changed is what precedes it. The contrast is confounded: the pair made adjacent is also the pair that is most quantitative and whose own papers changed most, and it enters no budget.\nPanel b: the weighting parameters for 2026-27, coded degree by degree for the three branches in which Física appears at all.":
        "Panel a: horarios de la UPV/EHU para la convocatoria ordinaria, 2025 y 2026, con el cambio de la media de cada materia bajo su nombre. La franja propia de Física no se movió — fue la última de su día en los dos años —, de modo que\nlo que cuesta ir la última se cancela en la diferencia. Lo que cambió es lo que la precede. El contraste está confundido: el par que quedó seguido es también el más cuantitativo y aquel cuyas pruebas más cambiaron, y no entra en ningún presupuesto.\nPanel b: los parámetros de ponderación para 2026-27, codificados grado a grado en las tres ramas en las que Física aparece.",
})

# fig25 / fig04 — the source note, split in three so that paper mode can leave
# out the sentence about a panel c it does not contain.
ES.update({
    "Ministry EPAU, ordinary sitting. Panels a and b: specific phase, 17 communities, "
    "locus fitted on all 187 region-years.":
        "EPAU del Ministerio, convocatoria ordinaria. Paneles a y b: fase específica, "
        "17 comunidades, lugar geométrico ajustado sobre las 187 observaciones comunidad-año.",
    " Panel c: pooled phase, the nine communities with a 2026 result in every year.":
        " Panel c: fase común, las nueve comunidades con resultado de 2026 en todos los años.",
    "\nThe choice term is a simulation of the two formats at item SD 0.2 "
    "net of the other eight communities' own cuts; the cohort term is the Basque PISA "
    "2022–2025 decline in excess of Spain's, one PAU year of it, transferred one-for-one.\nBoth are "
    "differences from the field, because the quantity they are subtracted from is one. Neither is a causal estimate.":
        "\nEl término de la elección es una simulación de los dos formatos con desviación típica "
        "por ítem de 0.2, neta de los recortes propios de las otras ocho comunidades; el término de "
        "promoción es la caída vasca en PISA 2022–2025 en exceso de la de España, un año de PAU de "
        "ella, transferida uno a uno.\nLos dos son diferencias respecto del conjunto, porque la "
        "cantidad de la que se restan es una. Ninguno es una estimación causal.",
})

# fig40 / fig41 — split in two for the deck, so each gets its own caption.
ES.update({
    "UPV/EHU timetables for the ordinary sitting, with each subject's change in "
    "mean beneath its name. Física's own slot did not move — it was last on its "
    "day in both years — so what being last\ncosts differences out. What changed is "
    "what precedes it. The contrast is confounded and enters no budget: the pair "
    "made adjacent is also the pair that is most quantitative.":
        "Horarios de la UPV/EHU para la convocatoria ordinaria, con el cambio de la media de "
        "cada materia bajo su nombre. La franja propia de Física no se movió — fue la última de "
        "su día en los dos años —, de modo que\nlo que cuesta ir la última se cancela en la "
        "diferencia. Lo que cambió es lo que la precede. El contraste está confundido y no entra "
        "en ningún presupuesto: el par que quedó seguido es también el más cuantitativo.",
    "Panel b: the weighting parameters for 2026-27, coded degree by degree for the "
    "three branches in which Física appears at all. Only the two most favourable "
    "marks count, and Matemáticas II is compulsory in the access phase.":
        "Los parámetros de ponderación para 2026-27, codificados grado a grado en las tres ramas "
        "en las que Física aparece. Solo cuentan las dos mejores calificaciones, y Matemáticas II "
        "es obligatoria en la fase de acceso.",
})
