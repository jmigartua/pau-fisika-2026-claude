#!/usr/bin/env python3
"""Exam-content coding: are the 2025 and 2026 ordinary Física papers competency-oriented?

Every exercise (each option counted as its own row) of the ordinary-sitting papers of
nine communities is coded by hand on the criteria used in the EHU competency conversion
scheme (real-world narrative context; technological/social application; explain/justify
section; graph/data interpretation or diagram production; evaluation/judgment section)
plus the structural facts (obligatory or optional, points, options in the slot).

Codes
-----
ctx      0 = no context; 1 = decorative (a named real object/setting, but the tasks are
         the standard calculation and the context adds no data or decision);
         2 = substantive (a scenario, role, claim, regulation or design specification
         that drives the tasks or must be interpreted).
app      1 if a technological, medical, social or environmental application is named.
explain  1 if at least one section demands a qualitative explanation / justification in
         words that is not itself a calculation (drawing-and-reasoning counts).
graph    1 if the student must read data off a given graph, table, photograph or figure
         (interpretation of a representation).
draw     1 if the student must produce a diagram (ray tracing, vector scheme, sketch of a
         curve, force diagram).
evaluate 1 if a numerical result must be judged against a real-world criterion, claim,
         specification or regulation (realistic? compliant? safe? possible?).

Summary flags
-------------
contextualised  = ctx >= 1
competency      = ctx == 2 and (explain == 1 or evaluate == 1)   (EHU-style exercise)
competency_full = ctx == 2 and explain == 1 and evaluate == 1    (all three EHU requirements)

Outputs: data/exam_coding_2025_2026.csv, data/exam_structure_2025_2026.csv,
data/tables/exam_*.md, plots/fig11_exam_content.(png|svg)
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TABLES = DATA / "tables"
PLOTS = ROOT / "plots"
TABLES.mkdir(parents=True, exist_ok=True)

COLS = ["ccaa", "year", "item", "block", "obligatory", "n_options", "points",
        "ctx", "app", "explain", "graph", "draw", "evaluate", "note"]

# ccaa, year, item, block, obligatory, n_options, points, ctx, app, explain, graph, draw, evaluate, note
ROWS = [
    # ---------------- País Vasco (UPV/EHU) ----------------
    ("País Vasco", 2025, "A1", "Gravitación", 1, 1, 2.5, 2, 1, 1, 1, 0, 0,
     "Galileo satellite; ESA/AVS narrative, design-team role; 'justifica', 'explica', 'discute'; figure for qualitative check"),
    ("País Vasco", 2025, "B1", "Electromagnetismo", 0, 2, 2.5, 0, 0, 1, 0, 1, 0,
     "two parallel wires; 'explica razonadamente con esquemas'"),
    ("País Vasco", 2025, "B2", "Electromagnetismo", 0, 2, 2.5, 0, 0, 0, 0, 1, 0,
     "two point charges; field and potential; vector scheme"),
    ("País Vasco", 2025, "C1", "Ondas/Óptica", 0, 2, 2.5, 0, 0, 0, 0, 1, 0,
     "concave mirror; ray tracing"),
    ("País Vasco", 2025, "C2", "Ondas/Óptica", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "harmonic wave equation"),
    ("País Vasco", 2025, "D1", "Moderna", 0, 2, 2.5, 0, 0, 1, 0, 0, 0,
     "photoelectric effect, potassium; 'razona si se produce'"),
    ("País Vasco", 2025, "D2", "Moderna", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "photoelectric effect, two wavelengths"),

    ("País Vasco", 2026, "1", "Gravitación", 1, 1, 2.5, 2, 1, 1, 0, 0, 1,
     "Starlink alarmist headline; geostationary orbit; compare impact energy with a firecracker; '¿te parece realista?'; reasoning without calculation"),
    ("País Vasco", 2026, "2", "Electromagnetismo", 1, 1, 2.5, 2, 1, 1, 0, 0, 1,
     "mountain weather-station microgenerator; two lab configurations; Faraday-Lenz explanation; spec check fem >= 0.50 mV"),
    ("País Vasco", 2026, "3a", "Ondas/Óptica", 0, 2, 2.5, 2, 0, 0, 0, 0, 0,
     "violin string (Mi/La), concert scenario, decibels with two violins"),
    ("País Vasco", 2026, "3b", "Ondas/Óptica", 0, 2, 2.5, 1, 1, 1, 0, 0, 1,
     "choose the lens for a projector and justify; projection of a slide; compare image properties"),
    ("País Vasco", 2026, "4a", "Moderna", 0, 2, 2.5, 1, 0, 1, 0, 0, 0,
     "photoelectric effect; explain Einstein equation terms; oxidised surface comparison"),
    ("País Vasco", 2026, "4b", "Moderna", 0, 2, 2.5, 2, 1, 1, 0, 1, 0,
     "C-14 dating of bone remains; explain law; qualitative sketch of decay curve; estimate age"),

    # ---------------- Cataluña ----------------
    ("Cataluña", 2025, "1", "Gravitación", 1, 1, 2.5, 2, 1, 1, 0, 0, 0,
     "space debris / ISS tool-box (Nov 2023) and ISS de-orbit 2031; 'justifiqueu el signe'"),
    ("Cataluña", 2025, "2A", "Electromagnetismo", 0, 2, 2.5, 2, 0, 1, 0, 1, 0,
     "Millikan experiment; scheme with forces; reason the sign; what if the drop loses an electron"),
    ("Cataluña", 2025, "2B", "Electromagnetismo", 0, 2, 2.5, 0, 0, 1, 0, 1, 0,
     "sliding bar on U-circuit; justify current direction; represent force"),
    ("Cataluña", 2025, "3A", "Ondas/Óptica", 0, 2, 2.5, 2, 0, 1, 0, 1, 0,
     "art exhibition: coin inside polycarbonate block; critical angle; where must the second viewer stand"),
    ("Cataluña", 2025, "3B", "Ondas/Óptica", 0, 2, 2.5, 2, 0, 0, 0, 1, 0,
     "transverse flute as open pipe; draw harmonics"),
    ("Cataluña", 2025, "4", "Moderna", 1, 1, 2.5, 2, 1, 1, 0, 0, 0,
     "Na-24 tracer to measure a patient's blood volume; reason electron vs positron emission"),

    ("Cataluña", 2026, "1A", "Gravitación", 0, 2, 2.5, 2, 1, 1, 0, 0, 0,
     "Generalitat nanosatellite (late 2025); deduce period; closed orbit? justify"),
    ("Cataluña", 2026, "1B", "Gravitación", 0, 2, 2.5, 2, 0, 1, 0, 1, 1,
     "Halley's comet from historical records; sketch orbit; could Halley have seen it twice? reason"),
    ("Cataluña", 2026, "2", "Electromagnetismo", 1, 1, 2.5, 2, 1, 0, 0, 1, 0,
     "X-ray tube; represent field and force on figure; photon energy"),
    ("Cataluña", 2026, "3", "Ondas/Óptica", 1, 1, 2.5, 2, 1, 0, 0, 0, 0,
     "mobile-phone vibration motor; wave on a metal surface; sound level at 3 m"),
    ("Cataluña", 2026, "4A", "Moderna", 0, 2, 2.5, 2, 1, 0, 0, 0, 1,
     "Chernobyl 40 years: Cs-137 remaining; in which year can the zone be re-inhabited (safety threshold)"),
    ("Cataluña", 2026, "4B", "Moderna", 0, 2, 2.5, 0, 0, 1, 0, 0, 0,
     "photoelectric cell; justify results for green and red light"),

    # ---------------- Madrid ----------------
    ("Madrid", 2025, "1", "Gravitación", 1, 1, 2.5, 1, 0, 0, 0, 0, 0,
     "dwarf planet Eris narrative (discovery, Palomar); mass, g, elliptical-orbit energy, perihelion speed"),
    ("Madrid", 2025, "2A", "Electromagnetismo", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "electron-positron pair; field; maximum separation"),
    ("Madrid", 2025, "2B", "Electromagnetismo", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "rotating loop / time-varying field; max current"),
    ("Madrid", 2025, "3A", "Ondas/Óptica", 0, 2, 2.5, 1, 0, 0, 0, 0, 0,
     "whale sound detected by two ships; depth, power, sound level"),
    ("Madrid", 2025, "3B", "Ondas/Óptica", 0, 2, 2.5, 0, 0, 1, 0, 1, 0,
     "lateral magnification proof; 'razone' whether a diverging lens can invert; ray tracing"),
    ("Madrid", 2025, "4A", "Moderna", 0, 2, 2.5, 1, 1, 0, 0, 0, 0,
     "ozone absorbing UV; photon energy; power on a person"),
    ("Madrid", 2025, "4B", "Moderna", 0, 2, 2.5, 1, 1, 0, 0, 0, 0,
     "Al-26 burial dating of quartz sediments"),

    ("Madrid", 2026, "1", "Electromagnetismo", 1, 1, 2.5, 1, 0, 0, 1, 0, 0,
     "potential measured with a probe between plates; V(x) graph given; E = -dV/dx; acceleration and speed of a charge"),
    ("Madrid", 2026, "2A", "Gravitación", 0, 2, 2.5, 1, 1, 0, 0, 0, 0,
     "communications satellite of known mechanical energy; radius, speed, orbits per day, escape speed"),
    ("Madrid", 2026, "2B", "Gravitación", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "two point masses; null-field point; field at a point"),
    ("Madrid", 2026, "3A", "Ondas/Óptica", 0, 2, 2.5, 0, 0, 0, 1, 0, 0,
     "wave parameters read from two graphs (y(x,0) and v(0,t))"),
    ("Madrid", 2026, "3B", "Ondas/Óptica", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "ray through a slab; refraction angle; time; separation of rays"),
    ("Madrid", 2026, "4A", "Moderna", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "silver plate; two stopping potentials; determine h and work function"),
    ("Madrid", 2026, "4B", "Moderna", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "Ra-228 beta decay; activity; decay constant; transformed mass"),

    # ---------------- Castilla-La Mancha ----------------
    ("Castilla-La Mancha", 2025, "P1", "Gravitación", 1, 1, 2.5, 1, 0, 0, 0, 0, 0,
     "spacecraft on Saturn; g, escape speed, max height, synchronous orbit (choose 2 of 3 sections)"),
    ("Castilla-La Mancha", 2025, "P2", "Electromagnetismo", 1, 1, 2.5, 1, 1, 1, 1, 0, 0,
     "mass spectrometer figure; reason the sign of charges; velocity selector (choose 2 of 3)"),
    ("Castilla-La Mancha", 2025, "P3", "Ondas/Óptica", 1, 1, 2.5, 0, 0, 1, 0, 1, 0,
     "diverging lens; ray tracing; real/virtual reasoning (choose 2 of 3)"),
    ("Castilla-La Mancha", 2025, "C", "Cuestiones", 1, 1, 2.5, 1, 0, 1, 0, 0, 0,
     "photoelectric; connected spheres; school-lab pendulum experiment: same result with another bob? why? (choose 2 of 3)"),

    ("Castilla-La Mancha", 2026, "A", "Gravitación", 1, 1, 2.0, 2, 1, 1, 0, 0, 0,
     "Artemis II / Orion re-entry safety; compare orbital and escape speed; energy to dissipate for a safe landing"),
    ("Castilla-La Mancha", 2026, "B1", "Electromagnetismo", 1, 1, 0.5, 0, 0, 1, 0, 0, 0,
     "work to move a charge between potentials; 'razona el resultado'"),
    ("Castilla-La Mancha", 2026, "B2.A", "Electromagnetismo", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "rotating rectangular loop; flux, emf, current"),
    ("Castilla-La Mancha", 2026, "B2.B", "Electromagnetismo", 0, 2, 2.5, 0, 0, 0, 0, 1, 0,
     "two charged spheres, one hanging under gravity; force diagram; connection by a wire"),
    ("Castilla-La Mancha", 2026, "C1", "Ondas/Óptica", 1, 1, 0.5, 0, 0, 1, 0, 1, 0,
     "construct the image for an object between f and 2f; describe it"),
    ("Castilla-La Mancha", 2026, "C2.A", "Ondas/Óptica", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "MAS from equation; spring constant; energies"),
    ("Castilla-La Mancha", 2026, "C2.B", "Ondas/Óptica", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "electromagnetic wave; wave equation; refractive index"),
    ("Castilla-La Mancha", 2026, "D1", "Moderna", 0, 2, 2.0, 0, 0, 0, 0, 0, 0,
     "alpha vs proton; speed and de Broglie ratios"),
    ("Castilla-La Mancha", 2026, "D2", "Moderna", 0, 2, 2.0, 1, 1, 0, 0, 0, 0,
     "F-18 PET tracer; decay constant; remaining mass"),

    # ---------------- Asturias ----------------
    ("Asturias", 2025, "1", "Gravitación", 0, 8, 2.0, 0, 0, 1, 0, 1, 0,
     "two point masses; field; potential; 'justifica el signo del trabajo y razona si depende de la trayectoria'"),
    ("Asturias", 2025, "2", "Gravitación", 0, 8, 2.0, 1, 1, 0, 0, 0, 0,
     "Meteosat MTG-I1 satellite; period, speed, escape energy"),
    ("Asturias", 2025, "3", "Electromagnetismo", 0, 8, 2.0, 0, 0, 1, 0, 0, 0,
     "two point charges; null field/potential points; justify work sign"),
    ("Asturias", 2025, "4", "Electromagnetismo", 0, 8, 2.0, 0, 0, 1, 0, 1, 0,
     "two parallel wires; reason whether the field cancels; scheme"),
    ("Asturias", 2025, "5", "Ondas/Óptica", 0, 8, 2.0, 1, 1, 0, 0, 1, 0,
     "wildlife observation centre in the Cordillera Cantábrica; concave mirror; ray tracing"),
    ("Asturias", 2025, "6", "Ondas/Óptica", 0, 8, 2.0, 1, 0, 1, 0, 0, 0,
     "Campomanes station master and a departing train: Doppler and echo, qualitative comparison"),
    ("Asturias", 2025, "7", "Moderna", 0, 8, 2.0, 1, 0, 0, 0, 0, 0,
     "Geiger-Müller measurement of activity on two days; half-life; mass; mean life"),
    ("Asturias", 2025, "8", "Moderna", 0, 8, 2.0, 0, 0, 0, 0, 0, 0,
     "relativistic proton with E = 3 E0"),

    ("Asturias", 2026, "1", "Gravitación", 0, 8, 2.0, 1, 0, 0, 0, 0, 0,
     "a melon weighed on Jupiter; g and mass of Jupiter"),
    ("Asturias", 2026, "2", "Gravitación", 0, 8, 2.0, 1, 0, 1, 0, 0, 0,
     "two pumpkins and an apple; field; work; 'razone si será espontáneo'"),
    ("Asturias", 2026, "3", "Electromagnetismo", 0, 8, 2.0, 0, 0, 0, 0, 0, 0,
     "electric dipole; field and potential at P"),
    ("Asturias", 2026, "4", "Electromagnetismo", 0, 8, 2.0, 0, 0, 0, 0, 0, 0,
     "alpha particle in B; circular path; electron in the same field"),
    ("Asturias", 2026, "5", "Ondas/Óptica", 0, 8, 2.0, 1, 0, 0, 0, 0, 0,
     "kayaking off Cudillero; wave speed; wave equation"),
    ("Asturias", 2026, "6", "Ondas/Óptica", 0, 8, 2.0, 1, 0, 0, 0, 1, 0,
     "porcelain figurine in front of a concave mirror; ray tracing"),
    ("Asturias", 2026, "7", "Moderna", 0, 8, 2.0, 1, 1, 0, 0, 0, 0,
     "electron-diffraction experiment on a material; de Broglie"),
    ("Asturias", 2026, "8", "Moderna", 0, 8, 2.0, 0, 0, 0, 0, 0, 0,
     "U-238 decay constant; time to one third of activity"),

    # ---------------- Andalucía (model A and model B 2025; one paper 2026) ----------------
    ("Andalucía", 2025, "A.a", "Gravitación", 1, 1, 1.0, 0, 0, 1, 0, 0, 0,
     "true/false reasoning on null field and potential"),
    ("Andalucía", 2025, "A.b1", "Gravitación", 0, 2, 1.5, 1, 0, 0, 0, 1, 0,
     "flight attendant dragging a suitcase; force scheme; work of each force"),
    ("Andalucía", 2025, "A.b2", "Gravitación", 0, 2, 1.5, 1, 0, 0, 0, 0, 0,
     "1960s satellite orbit; energies and speed"),
    ("Andalucía", 2025, "B.a", "Electromagnetismo", 1, 1, 1.0, 0, 0, 1, 0, 0, 0,
     "deduce radius in B; ratio of periods; 'razone'"),
    ("Andalucía", 2025, "B.b1", "Electromagnetismo", 0, 2, 1.5, 0, 0, 1, 0, 1, 0,
     "sliding side of a loop; emf; current; direction with drawing"),
    ("Andalucía", 2025, "B.b2", "Electromagnetismo", 0, 2, 1.5, 0, 0, 1, 0, 0, 0,
     "two charges; potentials; work; interpret the sign"),
    ("Andalucía", 2025, "C.a", "Ondas/Óptica", 1, 1, 1.0, 0, 0, 1, 0, 1, 0,
     "which lens gives a virtual enlarged image; ray tracing and explanation"),
    ("Andalucía", 2025, "C.b1", "Ondas/Óptica", 0, 2, 1.5, 0, 0, 0, 0, 0, 0,
     "wave on a string; equation; phase differences"),
    ("Andalucía", 2025, "C.b2", "Ondas/Óptica", 0, 2, 1.5, 1, 0, 0, 0, 1, 0,
     "light through air-oil-water; scheme; angles"),
    ("Andalucía", 2025, "D.a", "Moderna", 1, 1, 1.0, 0, 0, 1, 0, 0, 0,
     "stopping potential; deduce max speed; ratio if halved"),
    ("Andalucía", 2025, "D.b1", "Moderna", 0, 2, 1.5, 1, 1, 0, 0, 0, 0,
     "research project: boron-10 fission by neutrons; energy released"),
    ("Andalucía", 2025, "D.b2", "Moderna", 0, 2, 1.5, 0, 0, 1, 0, 0, 0,
     "proton and electron with the same kinetic energy; de Broglie; stopping potentials"),

    ("Andalucía", 2026, "A.a", "Gravitación", 1, 1, 1.0, 0, 0, 1, 0, 0, 0,
     "true/false reasoning on conservation of mechanical energy"),
    ("Andalucía", 2026, "A.b", "Gravitación", 1, 1, 1.5, 1, 0, 1, 0, 1, 0,
     "child on a slide with friction; force scheme; work; speed at the bottom"),
    ("Andalucía", 2026, "B.a1", "Electromagnetismo", 0, 2, 1.0, 0, 0, 1, 0, 0, 0,
     "true/false on flux and emf"),
    ("Andalucía", 2026, "B.a2", "Electromagnetismo", 0, 2, 1.0, 0, 0, 1, 0, 0, 0,
     "two identical charges; symbolic speed; effect of doubling charges"),
    ("Andalucía", 2026, "B.b1", "Electromagnetismo", 0, 2, 1.5, 1, 1, 1, 0, 0, 0,
     "wind farm in the Strait of Gibraltar: rotating loop; flux; emf; DC or AC?"),
    ("Andalucía", 2026, "B.b2", "Electromagnetismo", 0, 2, 1.5, 0, 0, 0, 0, 0, 0,
     "electron launched towards a fixed negative charge; stopping distance"),
    ("Andalucía", 2026, "C.a1", "Ondas/Óptica", 0, 2, 1.0, 0, 0, 1, 0, 1, 0,
     "diverging lens; ray tracing; image characteristics"),
    ("Andalucía", 2026, "C.a2", "Ondas/Óptica", 0, 2, 1.0, 0, 0, 1, 0, 0, 0,
     "wave changing medium; ratios"),
    ("Andalucía", 2026, "C.b1", "Ondas/Óptica", 0, 2, 1.5, 1, 1, 0, 0, 1, 0,
     "projecting an object onto a screen; focal length; scheme"),
    ("Andalucía", 2026, "C.b2", "Ondas/Óptica", 0, 2, 1.5, 1, 0, 1, 0, 0, 0,
     "guitar string standing wave; type of wave; speeds"),
    ("Andalucía", 2026, "D.a1", "Moderna", 0, 2, 1.0, 0, 0, 1, 0, 0, 0,
     "photoelectric threshold at yellow light: red light? more intensity? 'razone'"),
    ("Andalucía", 2026, "D.a2", "Moderna", 0, 2, 1.0, 0, 0, 1, 0, 0, 0,
     "proton vs K meson; de Broglie reasoning"),
    ("Andalucía", 2026, "D.b1", "Moderna", 0, 2, 1.5, 0, 0, 1, 0, 0, 0,
     "copper photocell with two frequencies; which produces emission; max speed"),
    ("Andalucía", 2026, "D.b2", "Moderna", 0, 2, 1.5, 0, 0, 0, 0, 0, 0,
     "proton and electron accelerated by 0.075 V; de Broglie"),

    # ---------------- Canarias ----------------
    ("Canarias", 2025, "I.A", "Gravitación", 0, 2, 2.5, 0, 0, 1, 0, 0, 0,
     "g at 400 km; prove E = Ep/2 for a circular orbit"),
    ("Canarias", 2025, "I.B", "Gravitación", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "two point masses; potential; force; work to infinity"),
    ("Canarias", 2025, "II.A", "Electromagnetismo", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "dipole; force on a third charge; work"),
    ("Canarias", 2025, "II.B", "Electromagnetismo", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "two parallel wires; field vector; alpha particles in B"),
    ("Canarias", 2025, "III.A", "Ondas/Óptica", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "MAS from initial conditions"),
    ("Canarias", 2025, "III.B", "Ondas/Óptica", 0, 2, 2.5, 1, 1, 0, 0, 1, 0,
     "slide projector; ray diagram; lens power"),
    ("Canarias", 2025, "IV.A", "Moderna", 0, 2, 2.5, 0, 0, 1, 0, 0, 0,
     "binding energies of H-3 and He-3; which is more stable; de Broglie ratio"),
    ("Canarias", 2025, "IV.B", "Moderna", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "photoelectric effect on aluminium"),

    ("Canarias", 2026, "1a", "Gravitación", 1, 1, 1.5, 1, 0, 0, 0, 0, 0,
     "microsatellite with period 5710 s; height; energy to orbit"),
    ("Canarias", 2026, "1b1", "Gravitación", 0, 2, 1.0, 1, 0, 0, 0, 0, 0,
     "speed, centripetal acceleration, energies in orbit"),
    ("Canarias", 2026, "1b2", "Gravitación", 0, 2, 1.0, 1, 0, 0, 0, 0, 0,
     "energy to double the orbital radius"),
    ("Canarias", 2026, "2", "Electromagnetismo", 1, 1, 1.5, 0, 0, 0, 0, 0, 0,
     "two antiparallel wires; field at two points"),
    ("Canarias", 2026, "3", "Electromagnetismo", 0, 2, 1.5, 1, 0, 0, 0, 0, 0,
     "'en un laboratorio': two charges producing a given field"),
    ("Canarias", 2026, "4", "Electromagnetismo", 0, 2, 1.5, 0, 0, 0, 0, 1, 0,
     "electron entering B; acceleration vector; drawing of trajectory and vectors"),
    ("Canarias", 2026, "5a", "Ondas/Óptica", 0, 2, 1.5, 0, 0, 0, 0, 0, 0,
     "point sound source; distance to inaudibility"),
    ("Canarias", 2026, "5b", "Ondas/Óptica", 0, 2, 1.5, 0, 0, 0, 0, 0, 0,
     "point sound source; distance for 30 dB"),
    ("Canarias", 2026, "6", "Ondas/Óptica", 0, 2, 1.5, 0, 0, 1, 0, 0, 0,
     "mass on a spring; energies; 'justifique las expresiones'"),
    ("Canarias", 2026, "7", "Ondas/Óptica", 0, 2, 1.5, 0, 0, 1, 0, 0, 0,
     "refraction; critical angle; from which medium"),
    ("Canarias", 2026, "8", "Moderna", 0, 2, 1.5, 1, 1, 0, 0, 0, 0,
     "Cs-137 in dust after a calima episode (nuclear tests 60 years ago); number of nuclei and mass"),
    ("Canarias", 2026, "9", "Moderna", 0, 2, 1.5, 0, 0, 0, 0, 0, 0,
     "photoelectric effect; stopping potential 1 V"),

    # ---------------- Extremadura ----------------
    ("Extremadura", 2025, "1", "Gravitación", 1, 1, 2.5, 1, 1, 0, 0, 0, 0,
     "two Extremaduran students on an ESA mission collecting space debris near the ISS; field of two people; weight on the Moon"),
    ("Extremadura", 2025, "2", "Electromagnetismo", 0, 2, 2.5, 0, 0, 1, 0, 0, 0,
     "electron accelerated then in crossed fields; 'razona' for a proton"),
    ("Extremadura", 2025, "3", "Electromagnetismo", 0, 2, 2.5, 0, 0, 1, 1, 0, 0,
     "three trajectories in B (figure): signs of charges; fastest particle; reason"),
    ("Extremadura", 2025, "4", "Ondas/Óptica", 0, 2, 2.5, 1, 0, 0, 0, 0, 0,
     "sitting at the station: Doppler of an approaching and receding train"),
    ("Extremadura", 2025, "5", "Ondas/Óptica", 0, 2, 2.5, 0, 0, 1, 1, 0, 0,
     "ray diagram given (figure): describe the image; s', f, power"),
    ("Extremadura", 2025, "6", "Moderna", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "photoelectric effect; four calculations"),
    ("Extremadura", 2025, "7", "Moderna", 0, 2, 2.5, 0, 0, 1, 0, 0, 0,
     "four fundamental forces; does the Standard Model cover them (recall)"),

    ("Extremadura", 2026, "1", "Gravitación", 1, 1, 2.5, 1, 1, 0, 0, 0, 0,
     "Artemis II / Orion launch narrative (1 Apr 2026); force; escape energy; orbital speed"),
    ("Extremadura", 2026, "2", "Electromagnetismo", 0, 2, 2.5, 0, 0, 0, 0, 1, 0,
     "two charges; scheme; force on a test charge; external work"),
    ("Extremadura", 2026, "3", "Electromagnetismo", 0, 2, 2.5, 1, 1, 1, 0, 0, 0,
     "laboratory velocity selector; reason the deflection; condition for straight motion"),
    ("Extremadura", 2026, "4", "Ondas/Óptica", 0, 2, 2.5, 1, 0, 0, 0, 0, 0,
     "mass-spring 'experiment': period from half-oscillation time; energy; equation"),
    ("Extremadura", 2026, "5", "Ondas/Óptica", 0, 2, 2.5, 1, 1, 1, 0, 1, 0,
     "projecting a slide magnified 20x; which lens; ray tracing explained in words"),
    ("Extremadura", 2026, "6", "Moderna", 0, 2, 2.5, 1, 0, 0, 1, 0, 0,
     "photoelectric data table and Vf-f plot; complete the table; determine h and W from two points"),
    ("Extremadura", 2026, "7", "Moderna", 0, 2, 2.5, 0, 0, 0, 0, 0, 0,
     "radioactive sample: decay constant; half-life; nuclei; energy released"),

    # ---------------- Comunitat Valenciana ----------------
    ("Comunitat Valenciana", 2025, "1A", "Gravitación", 0, 2, 2.0, 1, 0, 0, 1, 0, 0,
     "binary star IK Pegasi (figure with positions); field vector; escape speed"),
    ("Comunitat Valenciana", 2025, "1B", "Gravitación", 0, 2, 2.0, 1, 0, 0, 0, 0, 0,
     "space station around a planet; symbolic height and g"),
    ("Comunitat Valenciana", 2025, "2", "Electromagnetismo", 1, 1, 1.5, 2, 1, 1, 0, 1, 1,
     "worker in a chlorine electrolysis plant under an 18 kA cable; Biot-Savart with law statement; is she protected under RD 299/2016 (2 T)?"),
    ("Comunitat Valenciana", 2025, "3A", "Electromagnetismo", 0, 2, 1.5, 0, 0, 1, 0, 1, 0,
     "direction of the field of two charges in three regions with vector representation"),
    ("Comunitat Valenciana", 2025, "3B", "Electromagnetismo", 0, 2, 1.5, 0, 0, 1, 1, 1, 0,
     "square loop in B(t) given as a graph; emf; draw field and induced current; reason direction"),
    ("Comunitat Valenciana", 2025, "4A", "Ondas/Óptica", 0, 2, 1.5, 0, 0, 0, 1, 0, 0,
     "wave parameters from two graphs"),
    ("Comunitat Valenciana", 2025, "4B", "Ondas/Óptica", 0, 2, 1.5, 1, 1, 0, 0, 0, 0,
     "two air-conditioning compressors; sound levels; power of the second"),
    ("Comunitat Valenciana", 2025, "5A", "Ondas/Óptica", 0, 2, 2.0, 0, 0, 0, 0, 0, 0,
     "MAS from x(t); energies at half amplitude"),
    ("Comunitat Valenciana", 2025, "5B", "Ondas/Óptica", 0, 2, 2.0, 0, 0, 0, 0, 1, 0,
     "object in front of a 4 D lens; ray scheme; move the object for a given image"),
    ("Comunitat Valenciana", 2025, "6A", "Moderna", 0, 2, 1.5, 0, 0, 1, 0, 0, 0,
     "Po-218 alpha decay; mass numbers; mass ten minutes earlier"),
    ("Comunitat Valenciana", 2025, "6B", "Moderna", 0, 2, 1.5, 1, 0, 1, 0, 0, 0,
     "spaceship to Barnard's star; proper time; durations; reason"),

    ("Comunitat Valenciana", 2026, "1", "Gravitación", 1, 1, 2.0, 1, 1, 0, 0, 0, 0,
     "Deimos-2 Earth-observation satellite (620 km); deduce orbital speed and g(h)"),
    ("Comunitat Valenciana", 2026, "2A", "Electromagnetismo", 0, 2, 3.0, 0, 0, 1, 0, 0, 0,
     "two charges on a square; equipotential diagonal? Gauss law statement and flux reasoning"),
    ("Comunitat Valenciana", 2026, "2B", "Electromagnetismo", 0, 2, 3.0, 0, 0, 0, 1, 1, 0,
     "two parallel wires (figure); field; force on a moving charge; represent vectors; current for a given field"),
    ("Comunitat Valenciana", 2026, "3A", "Ondas/Óptica", 0, 2, 3.0, 0, 0, 0, 1, 0, 0,
     "photograph of a wave on a rope at t = 2 s: read wavelength and amplitude; wave function; phase"),
    ("Comunitat Valenciana", 2026, "3B", "Ondas/Óptica", 0, 2, 3.0, 0, 0, 1, 1, 0, 0,
     "laser on a material: read angles from the scheme; justify how angles change; lens image"),
    ("Comunitat Valenciana", 2026, "4A", "Moderna", 0, 2, 2.0, 1, 1, 0, 0, 0, 0,
     "Tc-99m radiopharmaceutical: activity at production; nuclei and mass to produce"),
    ("Comunitat Valenciana", 2026, "4B", "Moderna", 0, 2, 2.0, 0, 0, 1, 1, 0, 0,
     "photoelectric: work function; interpret slope and intercepts of the Ek-f graph"),
]

df = pd.DataFrame(ROWS, columns=COLS)
df["contextualised"] = (df.ctx >= 1).astype(int)
df["substantive_ctx"] = (df.ctx == 2).astype(int)
df["competency"] = ((df.ctx == 2) & ((df.explain == 1) | (df.evaluate == 1))).astype(int)
df["competency_full"] = ((df.ctx == 2) & (df.explain == 1) & (df.evaluate == 1)).astype(int)
df["criteria_met"] = df[["substantive_ctx", "app", "explain", "graph", "evaluate"]].sum(axis=1)
df.to_csv(DATA / "exam_coding_2025_2026.csv", index=False)

# ---------------------------------------------------------------- structure per paper
# Optional points of the paper = total points of slots where the student chooses.
# Weight of a row inside its slot = points / n_options for "expected exposure" (a
# student choosing at random); "guaranteed" = obligatory rows only.
STRUCT = {
    ("País Vasco", 2025): dict(n_items=7, answered=4, total=10, optional_pts=7.5,
                               fmt="Block A obligatory; blocks B, C, D: choose 1 of 2 (2.5 each)"),
    ("País Vasco", 2026): dict(n_items=6, answered=4, total=10, optional_pts=5.0,
                               fmt="Ex. 1 and 2 obligatory (competencial); ex. 3 and 4: choose a/b"),
    ("Cataluña", 2025): dict(n_items=6, answered=4, total=10, optional_pts=5.0,
                             fmt="Four exercises; options A/B in ex. 2 and 3"),
    ("Cataluña", 2026): dict(n_items=6, answered=4, total=10, optional_pts=5.0,
                             fmt="Four exercises; options A/B in ex. 1 and 4"),
    ("Madrid", 2025): dict(n_items=7, answered=4, total=10, optional_pts=7.5,
                           fmt="Block 1 obligatory; blocks 2-4: choose A/B"),
    ("Madrid", 2026): dict(n_items=7, answered=4, total=10, optional_pts=7.5,
                           fmt="Block 1 obligatory (graph item); blocks 2-4: choose A/B"),
    ("Castilla-La Mancha", 2025): dict(n_items=4, answered=4, total=10, optional_pts=10.0,
                                       fmt="Four questions, each: answer 2 of 3 sections"),
    ("Castilla-La Mancha", 2026): dict(n_items=9, answered=6, total=10, optional_pts=7.0,
                                       fmt="A obligatory (2); B, C: fixed 0.5 + choose 1 of 2 (2.5); D: choose 1 of 2 (2)"),
    ("Asturias", 2025): dict(n_items=8, answered=5, total=10, optional_pts=10.0,
                             fmt="Answer any 5 of 8 questions (2 each)"),
    ("Asturias", 2026): dict(n_items=8, answered=5, total=10, optional_pts=10.0,
                             fmt="Answer any 5 of 8 questions (2 each)"),
    ("Andalucía", 2025): dict(n_items=12, answered=8, total=10, optional_pts=6.0,
                              fmt="Four blocks: a) obligatory (1) + choose b1/b2 (1.5)"),
    ("Andalucía", 2026): dict(n_items=14, answered=8, total=10, optional_pts=7.5,
                              fmt="Block A obligatory (a + b); blocks B-D: choose a1/a2 and b1/b2"),
    ("Canarias", 2025): dict(n_items=8, answered=4, total=10, optional_pts=10.0,
                             fmt="Four blocks: choose option A or B (2.5 each)"),
    ("Canarias", 2026): dict(n_items=12, answered=7, total=10, optional_pts=7.0,
                             fmt="Obligatory 1a (1.5) and 2 (1.5); the rest in pairs (2.5/3/3/1.5 per block)"),
    ("Extremadura", 2025): dict(n_items=7, answered=4, total=10, optional_pts=7.5,
                                fmt="Block A obligatory; blocks B-D: choose 1 of 2"),
    ("Extremadura", 2026): dict(n_items=7, answered=4, total=10, optional_pts=7.5,
                                fmt="Block A obligatory; blocks B-D: choose 1 of 2"),
    ("Comunitat Valenciana", 2025): dict(n_items=11, answered=6, total=10, optional_pts=8.5,
                                         fmt="Six questions; question 2 obligatory (1.5); the other five A/B"),
    ("Comunitat Valenciana", 2026): dict(n_items=7, answered=4, total=10, optional_pts=8.0,
                                         fmt="Four apartados; apartado 1 single option (2); 2-4 A/B (3/3/2)"),
}

GRADES = pd.read_csv(DATA / "analysis" / "regions_2026_vs_2025.csv")
GRADES["ccaa_short"] = GRADES["ccaa"].str.replace(" (Comunidad de)", "", regex=False).str.replace(" (Principado de)", "", regex=False)

rows = []
for (ccaa, year), g in df.groupby(["ccaa", "year"], sort=False):
    st = STRUCT[(ccaa, year)]
    w = g.points / g.n_options                      # expected points of the row for a random chooser
    exp_total = w.sum()
    oblig = g[g.obligatory == 1]
    rows.append(dict(
        ccaa=ccaa, year=year, n_items=len(g), answered=st["answered"],
        optionality_pct=100 * st["optional_pts"] / st["total"],
        oblig_pts=oblig.points.sum(),
        share_items_contextualised=100 * g.contextualised.mean(),
        share_items_substantive=100 * g.substantive_ctx.mean(),
        share_items_competency=100 * g.competency.mean(),
        share_items_competency_full=100 * g.competency_full.mean(),
        exp_pts_competency=(w * g.competency).sum(),
        exp_pts_substantive=(w * g.substantive_ctx).sum(),
        exp_pts_contextualised=(w * g.contextualised).sum(),
        oblig_pts_competency=oblig.points[oblig.competency == 1].sum(),
        oblig_pts_substantive=oblig.points[oblig.substantive_ctx == 1].sum(),
        mean_criteria=g.criteria_met.mean(),
        share_explain=100 * g.explain.mean(), share_graph=100 * g.graph.mean(),
        share_draw=100 * g.draw.mean(), share_evaluate=100 * g.evaluate.mean(),
        share_app=100 * g.app.mean(),
        fmt=st["fmt"],
    ))
S = pd.DataFrame(rows)
S["exp_share_competency"] = 100 * S.exp_pts_competency / 10
S["exp_share_substantive"] = 100 * S.exp_pts_substantive / 10
S["exp_share_contextualised"] = 100 * S.exp_pts_contextualised / 10
S.to_csv(DATA / "exam_structure_2025_2026.csv", index=False)

# ---------------------------------------------------------------- change table
P = S.pivot(index="ccaa", columns="year")
chg = pd.DataFrame({
    "ccaa": P.index,
    "opt_2025": P[("optionality_pct", 2025)].values, "opt_2026": P[("optionality_pct", 2026)].values,
    "comp_items_2025": P[("share_items_competency", 2025)].values, "comp_items_2026": P[("share_items_competency", 2026)].values,
    "comp_exp_2025": P[("exp_share_competency", 2025)].values, "comp_exp_2026": P[("exp_share_competency", 2026)].values,
    "subst_exp_2025": P[("exp_share_substantive", 2025)].values, "subst_exp_2026": P[("exp_share_substantive", 2026)].values,
    "ctx_exp_2025": P[("exp_share_contextualised", 2025)].values, "ctx_exp_2026": P[("exp_share_contextualised", 2026)].values,
    "oblig_comp_2025": P[("oblig_pts_competency", 2025)].values, "oblig_comp_2026": P[("oblig_pts_competency", 2026)].values,
    "crit_2025": P[("mean_criteria", 2025)].values, "crit_2026": P[("mean_criteria", 2026)].values,
})
chg["d_opt"] = chg.opt_2026 - chg.opt_2025
chg["d_comp_exp"] = chg.comp_exp_2026 - chg.comp_exp_2025
chg["d_subst_exp"] = chg.subst_exp_2026 - chg.subst_exp_2025
chg["d_ctx_exp"] = chg.ctx_exp_2026 - chg.ctx_exp_2025
chg["d_crit"] = chg.crit_2026 - chg.crit_2025
chg = chg.merge(GRADES[["ccaa_short", "mean_2025", "mean_2026", "delta"]], left_on="ccaa", right_on="ccaa_short", how="left").drop(columns="ccaa_short")
chg = chg.sort_values("delta", ascending=False)
chg.to_csv(DATA / "exam_change_vs_grade.csv", index=False)

# ---------------------------------------------------------------- correlations
def spearman(a, b):
    a, b = pd.Series(a).rank(), pd.Series(b).rank()
    return float(np.corrcoef(a, b)[0, 1])

corr = {
    "n": int(len(chg)),
    "pearson_dgrade_dcomp_exp": float(np.corrcoef(chg.delta, chg.d_comp_exp)[0, 1]),
    "spearman_dgrade_dcomp_exp": spearman(chg.delta, chg.d_comp_exp),
    "pearson_dgrade_dsubst_exp": float(np.corrcoef(chg.delta, chg.d_subst_exp)[0, 1]),
    "spearman_dgrade_dsubst_exp": spearman(chg.delta, chg.d_subst_exp),
    "pearson_dgrade_dctx_exp": float(np.corrcoef(chg.delta, chg.d_ctx_exp)[0, 1]),
    "pearson_dgrade_dopt": float(np.corrcoef(chg.delta, chg.d_opt)[0, 1]),
    "spearman_dgrade_dopt": spearman(chg.delta, chg.d_opt),
    "pearson_dgrade_dcrit": float(np.corrcoef(chg.delta, chg.d_crit)[0, 1]),
    "pearson_dgrade_comp_exp_2026": float(np.corrcoef(chg.delta, chg.comp_exp_2026)[0, 1]),
    "pearson_dgrade_opt_2026": float(np.corrcoef(chg.delta, chg.opt_2026)[0, 1]),
}
(DATA / "exam_correlations.json").write_text(json.dumps(corr, indent=2))

# ---------------------------------------------------------------- Markdown tables
def md_table(df_, cols, headers, fmts):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for _, r in df_.iterrows():
        cells = []
        for c, f in zip(cols, fmts):
            v = r[c]
            cells.append(f.format(v) if not (isinstance(v, float) and np.isnan(v)) else "—")
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"

# Table A: structure and competency share per paper
tA = S.copy()
tA["paper"] = tA.ccaa + " " + tA.year.astype(str)
tA = tA.sort_values(["ccaa", "year"])
(TABLES / "exam_format.md").write_text(md_table(
    tA, ["paper", "fmt", "n_items", "answered", "optionality_pct", "oblig_pts"],
    ["Paper", "Structure", "Items offered", "Items answered", "Optional %", "Obligatory pts"],
    ["{}", "{}", "{}", "{}", "{:.0f}", "{:.1f}"]))
(TABLES / "exam_structure.md").write_text(md_table(
    tA, ["paper", "share_items_contextualised", "share_items_substantive", "share_items_competency",
         "exp_share_competency", "oblig_pts_competency"],
    ["Paper", "Contextualised items %", "Substantive-context items %", "Competency items %",
     "Expected competency pts %", "Obligatory competency pts"],
    ["{}", "{:.0f}", "{:.0f}", "{:.0f}", "{:.0f}", "{:.1f}"]))

# Table B: change vs grade change
(TABLES / "exam_change_vs_grade.md").write_text(md_table(
    chg, ["ccaa", "mean_2025", "mean_2026", "delta", "opt_2025", "opt_2026", "comp_exp_2025", "comp_exp_2026",
          "d_comp_exp", "oblig_comp_2025", "oblig_comp_2026", "crit_2025", "crit_2026"],
    ["Community", "Mean 2025", "Mean 2026", "Δ mean", "Optional % 2025", "Optional % 2026",
     "Competency pts % 2025", "Competency pts % 2026", "Δ competency pts %", "Oblig. competency pts 2025",
     "Oblig. competency pts 2026", "Criteria/item 2025", "Criteria/item 2026"],
    ["{}", "{:.2f}", "{:.2f}", "{:+.2f}", "{:.0f}", "{:.0f}", "{:.0f}", "{:.0f}", "{:+.0f}", "{:.1f}", "{:.1f}", "{:.2f}", "{:.2f}"]))

# Table C: criteria shares per paper
(TABLES / "exam_criteria.md").write_text(md_table(
    tA, ["paper", "share_app", "share_explain", "share_graph", "share_draw", "share_evaluate", "mean_criteria"],
    ["Paper", "Application %", "Explain/justify %", "Graph/data interpretation %", "Diagram production %",
     "Evaluation/judgment %", "Criteria met per item (of 5)"],
    ["{}", "{:.0f}", "{:.0f}", "{:.0f}", "{:.0f}", "{:.0f}", "{:.2f}"]))

# Table D: full coding listing (one row per item)
lst = df.copy()
lst["paper"] = lst.ccaa + " " + lst.year.astype(str)
lst["obl"] = np.where(lst.obligatory == 1, "yes", f"1 of n")
lst["obl"] = np.where(lst.obligatory == 1, "yes", "1 of " + lst.n_options.astype(str))
(TABLES / "exam_coding_full.md").write_text(md_table(
    lst, ["paper", "item", "block", "obl", "points", "ctx", "app", "explain", "graph", "draw", "evaluate", "competency", "note"],
    ["Paper", "Item", "Block", "Obligatory", "Pts", "Ctx", "App", "Expl", "Graph", "Draw", "Eval", "Comp.", "Content"],
    ["{}", "{}", "{}", "{}", "{:.1f}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"]))

# ---------------------------------------------------------------- figure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Colours come from the shared registry so a hue means the same thing in every
# figure of the study (ThesisFigures C1); styling is the shared module's job (E1).
from plot_style import C, apply_style

apply_style()

BLUE, ORANGE, AQUA, YELLOW = C["blue"], C["orange"], C["aqua"], C["yellow"]
MAGENTA, VIOLET, RED = C["magenta"], C["violet"], C["red"]
GREY = "#6b7280"

fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.0))
short = {"País Vasco": "Euskadi", "Comunitat Valenciana": "C. Valenciana", "Castilla-La Mancha": "C.-La Mancha"}
labels = [short.get(c, c) for c in chg.ccaa]

OFFS = {"Canarias": (6, -12), "Extremadura": (6, 3), "Madrid": (6, -10), "Asturias": (6, 3)}

def scatter(ax, x, y, xl, title, r):
    for xi, yi, lab in zip(x, y, labels):
        col = RED if lab == "Euskadi" else (ORANGE if yi < 0 else BLUE)
        ax.scatter(xi, yi, s=60, color=col, zorder=3)
        ax.annotate(lab, (xi, yi), textcoords="offset points", xytext=OFFS.get(lab, (5, 4)), fontsize=8.5, color="#111")
    ax.axhline(0, color=GREY, lw=0.8, ls="--")
    ax.axvline(0, color=GREY, lw=0.8, ls="--")
    ax.set_xlabel(xl)
    ax.set_title(f"{title}\nPearson r = {r:+.2f} (n = {corr['n']})", fontsize=10, loc="left")

scatter(axes[0], chg.d_comp_exp, chg.delta, "Δ expected points in competency-style exercises (pp, 2025→2026)",
        "a. Δ competency content vs Δ grade", corr["pearson_dgrade_dcomp_exp"])
axes[0].set_ylabel("Δ mean Física grade, ordinary sitting (2026 − 2025)")
scatter(axes[1], chg.d_opt, chg.delta, "Δ optional share of the paper (pp, 2025→2026)", "b. Δ optionality vs Δ grade",
        corr["pearson_dgrade_dopt"])
scatter(axes[2], chg.comp_exp_2026, chg.delta, "Expected points in competency-style exercises, 2026 paper (%)",
        "c. 2026 competency level vs Δ grade", corr["pearson_dgrade_comp_exp_2026"])
fig.suptitle("Física PAU 2025→2026, nine communities: what changed in the paper vs what changed in the grade",
             fontsize=11.5, x=0.01, ha="left")
fig.text(0.01, 0.005, "Coding of every exercise/option of the ordinary papers (data/exam_coding_2025_2026.csv). "
         "Competency-style = substantive real-world context and an explain/justify or evaluation section. "
         "Expected points assume a student choosing options at random.", fontsize=7.5, color=GREY)
fig.tight_layout(rect=(0, 0.04, 1, 0.94))
fig.savefig(PLOTS / "fig11_exam_content.png", dpi=170)
fig.savefig(PLOTS / "fig11_exam_content.svg")

# second figure: stacked profile per paper
fig, ax = plt.subplots(figsize=(12, 5.2))
order = chg.ccaa.tolist()
x = np.arange(len(order))
wbar = 0.38
for k, (yr, off, alpha) in enumerate([(2025, -wbar / 2, 0.55), (2026, wbar / 2, 1.0)]):
    sub = S.set_index(["ccaa", "year"])
    comp = [sub.loc[(c, yr), "exp_share_competency"] for c in order]
    subst = [sub.loc[(c, yr), "exp_share_substantive"] - sub.loc[(c, yr), "exp_share_competency"] for c in order]
    deco = [sub.loc[(c, yr), "exp_share_contextualised"] - sub.loc[(c, yr), "exp_share_substantive"] for c in order]
    ax.bar(x + off, comp, wbar, color=BLUE, alpha=alpha, label=f"{yr}: competency-style" if k == 1 else None)
    ax.bar(x + off, subst, wbar, bottom=comp, color=AQUA, alpha=alpha, label=f"{yr}: substantive context only" if k == 1 else None)
    ax.bar(x + off, deco, wbar, bottom=np.array(comp) + np.array(subst), color=YELLOW, alpha=alpha,
           label=f"{yr}: decorative context" if k == 1 else None)
    tops = np.array(comp) + np.array(subst) + np.array(deco)
    for xi, t in zip(x, tops):
        ax.text(xi + off, t + 1.5, str(yr)[2:], ha="center", fontsize=7.5, color=GREY)
ax.set_xticks(x)
ax.set_xticklabels([f"{short.get(c, c)}\n{d:+.2f}" for c, d in zip(order, chg.delta)], fontsize=9)
ax.set_ylabel("Expected share of the paper's points (%)")
ax.set_ylim(0, 110)
fig.suptitle("Contextualisation profile of each paper (left bar 2025, right bar 2026); Δ mean grade under each community",
             fontsize=10.5, x=0.01, ha="left")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=8.5, frameon=False, ncol=3)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(PLOTS / "fig12_exam_profiles.png", dpi=170)
fig.savefig(PLOTS / "fig12_exam_profiles.svg")

print(chg[["ccaa", "delta", "opt_2025", "opt_2026", "comp_exp_2025", "comp_exp_2026", "oblig_comp_2025", "oblig_comp_2026", "crit_2025", "crit_2026"]].round(2).to_string(index=False))
print(json.dumps(corr, indent=2))
