#!/usr/bin/env python3
"""The Basque Física paper in its own history, 2010–2026.

Inventory of every problem and theory question of the UPV/EHU ordinary and extraordinary
papers (sources/exams_ehu_hist/, 34 papers), coded by sub-topic; format by period; the
closed list of theory titles 2012–2024; a simulation of the "selection premium" that each
format's optionality gives; and the corresponding tables and figures (13–15).

Outputs: data/ehu_problem_inventory_2010_2026.csv, data/ehu_theory_inventory.csv,
data/ehu_formats.csv, data/ehu_selection_premium.csv, data/tables/ehu_*.md,
plots/fig13_ehu_topics.(png|svg), plots/fig14_ehu_formats_series.(png|svg),
plots/fig15_selection_premium.(png|svg)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TABLES = DATA / "tables"
PLOTS = ROOT / "plots"

# ----------------------------------------------------------------------------- sub-topics
SUB = {
    "G1": ("Gravitación", "Circular orbit / satellite (v, T, energies, escape from orbit)"),
    "G2": ("Gravitación", "g on a planet's surface or at height (mass, radius, g(r))"),
    "G3": ("Gravitación", "Elliptical orbits, Kepler, angular momentum"),
    "G4": ("Gravitación", "Launch from the surface, maximum height, escape"),
    "E1": ("Electromagnetismo", "Point charges: field, potential, work"),
    "E2": ("Electromagnetismo", "Charged particle in a uniform E field (plates, accelerator)"),
    "E3": ("Electromagnetismo", "Charged particle in a uniform B field (circular motion)"),
    "E4": ("Electromagnetismo", "Field of straight currents, forces between wires"),
    "E5": ("Electromagnetismo", "Induction: loop or rod, emf, generator"),
    "E6": ("Electromagnetismo", "Velocity selector / mass spectrometer"),
    "W1": ("Ondas", "Travelling harmonic wave (equation, v, phase)"),
    "W2": ("Ondas", "Simple harmonic motion (spring–mass, energy)"),
    "W3": ("Ondas", "Standing waves (string, pipe)"),
    "W4": ("Ondas", "Sound intensity, decibels"),
    "O1": ("Óptica", "Refraction, Snell, total internal reflection"),
    "O2": ("Óptica", "Thin lenses (magnifier, projector, camera)"),
    "O3": ("Óptica", "Spherical mirrors"),
    "M1": ("Moderna", "Photoelectric effect / photon energy"),
    "M2": ("Moderna", "Radioactive decay, half-life, dating"),
    "M3": ("Moderna", "Nuclear mass–energy, binding energy, reactions"),
    "M4": ("Moderna", "Special relativity"),
    "M5": ("Moderna", "de Broglie wavelength"),
}

# (year, sitting, slot, subtopic, obligatory, short description)
# 2010–2019: two whole options A/B, each 2 problems (3 pts) + 2 questions (2 pts); the student answers one option.
# 2020–2024: block A = 4 problems answer 2 (3 pts); block B = 4 questions answer 2 (2 pts).
# 2025: A obligatory competencial; B, C, D choose 1 of 2 (2.5 each). 2026: 1, 2 obligatory; 3, 4 choose a/b.
P = [
    (2010, "ord", "A.P1", "G2", 0, "g(r) on a planet; escape and energy"), (2010, "ord", "A.P2", "W1", 0, "harmonic wave in a pool"),
    (2010, "ord", "B.P1", "E1", 0, "±q dipole on the axis: E, V, work"), (2010, "ord", "B.P2", "O2", 0, "converging projector lens"),
    (2010, "extra", "A.P1", "G1", 0, "satellite in circular orbit"), (2010, "extra", "A.P2", "E2", 0, "linear accelerator, protons in E"),
    (2010, "extra", "B.P1", "E4", 0, "B of an infinite wire, force"), (2010, "extra", "B.P2", "M1", 0, "solar light intensity, photons"),
    (2011, "ord", "A.P1", "G1", 0, "ISS orbit (280 000 kg)"), (2011, "ord", "A.P2", "E2", 0, "linear accelerator, uniform E"),
    (2011, "ord", "B.P1", "E4", 0, "infinite wire B field"), (2011, "ord", "B.P2", "M1", 0, "5 mW laser, photons"),
    (2011, "extra", "A.P1", "G2", 0, "g(r) on a planet (g0/2, g0/4)"), (2011, "extra", "A.P2", "W1", 0, "wave on a string"),
    (2011, "extra", "B.P1", "E1", 0, "two +q charges on an axis"), (2011, "extra", "B.P2", "O1", 0, "light wave refraction"),
    (2012, "ord", "A.P1", "G1", 0, "satellite 250 kg at 300 km"), (2012, "ord", "A.P2", "E3", 0, "electron 25 keV in B"),
    (2012, "ord", "B.P1", "W2", 0, "SHM, 20 g on a spring"), (2012, "ord", "B.P2", "E2", 0, "charged particle in E"),
    (2012, "extra", "A.P1", "G3", 0, "Earth–Sun orbit, Kepler"), (2012, "extra", "A.P2", "W1", 0, "SHM-driven string wave"),
    (2012, "extra", "B.P1", "O2", 0, "converging lens f = 20 cm, ray diagrams"), (2012, "extra", "B.P2", "E3", 0, "proton accelerated by E then in B"),
    (2013, "ord", "A.P1", "W1", 0, "harmonic wave on a string"), (2013, "ord", "A.P2", "E4", 0, "two parallel wires: B and force"),
    (2013, "ord", "B.P1", "O2", 0, "magnifier f = 5 cm"), (2013, "ord", "B.P2", "G1", 0, "satellite 500 kg launched"),
    (2013, "extra", "A.P1", "W2", 0, "SHM, 100 g on a spring"), (2013, "extra", "A.P2", "G2", 0, "planet R = 3200 km, gravity"),
    (2013, "extra", "B.P1", "E5", 0, "circular loop in B(t), emf"), (2013, "extra", "B.P2", "O1", 0, "water/oil refraction"),
    (2014, "ord", "A.P1", "G1", 0, "satellite 1200 kg to 6500 km"), (2014, "ord", "A.P2", "M1", 0, "photoelectric, Na 2.3 eV"),
    (2014, "ord", "B.P1", "W2", 0, "spring K = 5050 N/m, SHM"), (2014, "ord", "B.P2", "E5", 0, "square loop in B, induction"),
    (2014, "extra", "A.P1", "G1", 0, "satellite 2000 kg"), (2014, "extra", "A.P2", "M1", 0, "photoelectric λ = 512 nm"),
    (2014, "extra", "B.P1", "E3", 0, "proton and α in B"), (2014, "extra", "B.P2", "O2", 0, "lens f = 20 cm"),
    (2015, "ord", "A.P1", "G1", 0, "Mars moons Deimos/Phobos"), (2015, "ord", "A.P2", "W2", 0, "SHM 0.5 kg on a spring"),
    (2015, "ord", "B.P1", "M1", 0, "photoelectric cell, W = 2.97e-19 J"), (2015, "ord", "B.P2", "E1", 0, "system of point charges"),
    (2015, "extra", "A.P1", "E3", 0, "charge moving in B (Lorentz)"), (2015, "extra", "A.P2", "W1", 0, "harmonic wave on a string"),
    (2015, "extra", "B.P1", "G1", 0, "satellite 500 kg orbit"), (2015, "extra", "B.P2", "O1", 0, "flashlight into water, refraction"),
    (2016, "ord", "A.P1", "G1", 0, "ISS at 340 km"), (2016, "ord", "A.P2", "W2", 0, "SHM 50 g on a spring"),
    (2016, "ord", "B.P1", "E3", 0, "proton and electron in B"), (2016, "ord", "B.P2", "M1", 0, "photoelectric K, 300 nm"),
    (2016, "extra", "A.P1", "G4", 0, "projectile 1000 kg from the surface, escape"), (2016, "extra", "A.P2", "W1", 0, "transverse wave equation"),
    (2016, "extra", "B.P1", "E2", 0, "parallel plates 40 cm, E field"), (2016, "extra", "B.P2", "M1", 0, "photons 500 nm on a metal"),
    (2017, "ord", "A.P1", "G2", 0, "Moon: g and escape"), (2017, "ord", "A.P2", "W1", 0, "harmonic wave expression"),
    (2017, "ord", "B.P1", "O2", 0, "laboratory lens characterisation"), (2017, "ord", "B.P2", "E1", 0, "charges 3 µC, −2 µC"),
    (2017, "extra", "A.P1", "M1", 0, "UV 170 nm photoelectron"), (2017, "extra", "A.P2", "E5", 0, "sliding rod, motional emf"),
    (2017, "extra", "B.P1", "W1", 0, "transverse wave A = 4 cm, λ = 2 cm"), (2017, "extra", "B.P2", "G1", 0, "equatorial-orbit satellite"),
    (2018, "ord", "A.P1", "E4", 0, "two parallel wires 10 cm"), (2018, "ord", "A.P2", "O1", 0, "water tank with glass bottom, refraction"),
    (2018, "ord", "B.P1", "G1", 0, "satellite 25 000 kg around a planet"), (2018, "ord", "B.P2", "M1", 0, "two lights on a metal, photoelectric"),
    (2018, "extra", "A.P1", "E1", 0, "two fixed charges 6 m apart"), (2018, "extra", "A.P2", "W1", 0, "string end moved, wave"),
    (2018, "extra", "B.P1", "G4", 0, "probe launched from a planet"), (2018, "extra", "B.P2", "O2", 0, "converging lens"),
    (2019, "ord", "A.P1", "W1", 0, "wave equation"), (2019, "ord", "A.P2", "E3", 0, "electron 2e6 m/s into B"),
    (2019, "ord", "B.P1", "G1", 0, "Venus: mass and orbit"), (2019, "ord", "B.P2", "M1", 0, "EM radiation 2e-7 m on a metal"),
    (2019, "extra", "A.P1", "G2", 0, "g(r) on a planet (g0/3, g0/5)"), (2019, "extra", "A.P2", "M1", 0, "5 mW laser 633 nm, photons"),
    (2019, "extra", "B.P1", "E1", 0, "two +q charges on OY"), (2019, "extra", "B.P2", "W1", 0, "circular pool wave R = 7 m"),
    (2020, "ord", "A1", "E4", 0, "two parallel wires I2 = 4 I1"), (2020, "ord", "A2", "G1", 0, "satellite 2500 kg r = 3e4 km"),
    (2020, "ord", "A3", "E5", 0, "square loop 5 cm, emf (three cases)"), (2020, "ord", "A4", "O1", 0, "water/oil refraction"),
    (2020, "extra", "A1", "W2", 0, "SHM"), (2020, "extra", "A2", "E3", 0, "charge 1 µC in B"),
    (2020, "extra", "A3", "W1", 0, "transverse wave on a string"), (2020, "extra", "A4", "O2", 0, "lens characterisation"),
    (2021, "ord", "A1", "G1", 0, "satellite around a planet"), (2021, "ord", "A2", "W1", 0, "wave speed on a string"),
    (2021, "ord", "A3", "O2", 0, "converging lens 30 cm"), (2021, "ord", "A4", "E5", 0, "circular loop 20 cm in B"),
    (2021, "extra", "A1", "G1", 0, "satellite 700 kg"), (2021, "extra", "A2", "E1", 0, "three charges"),
    (2021, "extra", "A3", "W1", 0, "y = 0.6 sin(18πt − 2πx)"), (2021, "extra", "A4", "O1", 0, "ray 600 nm, refraction"),
    (2022, "ord", "A1", "G1", 0, "spacecraft trapped in a circular orbit"), (2022, "ord", "A2", "E1", 0, "charges +10 µC / −40 µC"),
    (2022, "ord", "A3", "W1", 0, "transverse wave"), (2022, "ord", "A4", "O1", 0, "media A/B refraction"),
    (2022, "extra", "A1", "G2", 0, "Uranus g = 8.9"), (2022, "extra", "A2", "W1", 0, "harmonic wave on a string"),
    (2022, "extra", "A3", "O2", 0, "diverging lens, object 7 cm"), (2022, "extra", "A4", "M5", 0, "electron 25 eV: de Broglie and photon wavelengths"),
    (2023, "ord", "A1", "G4", 0, "Io (Jupiter): rocket maximum height"), (2023, "ord", "A2", "E1", 0, "three point charges at vertices"),
    (2023, "ord", "A3", "O2", 0, "converging lens f = 0.5 m"), (2023, "ord", "A4", "O1", 0, "ray f = 5e14 Hz, refraction"),
    (2023, "extra", "A1", "G2", 0, "100 kg body on Mars (g = 3.7)"), (2023, "extra", "A2", "W1", 0, "transverse wave λ = 1.5 m"),
    (2023, "extra", "A3", "M1", 0, "silver work function 4.73 eV"), (2023, "extra", "A4", "O1", 0, "swimmer sees an object, refraction"),
    (2024, "ord", "A1", "G1", 0, "crewed ship 2500 kg at 315 km"), (2024, "ord", "A2", "E1", 0, "+1 µC / +2 µC on a 3 m segment"),
    (2024, "ord", "A3", "O1", 0, "red light in a 30 cm glass slab"), (2024, "ord", "A4", "M1", 0, "photons 150 nm on a metal plate"),
    (2024, "extra", "A1", "G1", 0, "Earth-like exoplanet orbit"), (2024, "extra", "A2", "E3", 0, "proton in B"),
    (2024, "extra", "A3", "W2", 0, "SHM mechanical energy"), (2024, "extra", "A4", "M1", 0, "photons 500 nm, threshold"),
    (2025, "ord", "A1", "G1", 1, "Galileo satellite (competencial, obligatory)"), (2025, "ord", "B1", "E4", 0, "two parallel wires 9 A / 15 A"),
    (2025, "ord", "B2", "E1", 0, "±5 nC charges: V, E"), (2025, "ord", "C1", "O3", 0, "concave mirror f = 50 cm"),
    (2025, "ord", "C2", "W1", 0, "harmonic wave v = 400 m/s"), (2025, "ord", "D1", "M1", 0, "potassium 2.29 eV, photoelectric"),
    (2025, "ord", "D2", "M1", 0, "metal, two wavelengths, photoelectric"),
    (2025, "extra", "A1", "G1", 1, "SENER satellite orbit (competencial, obligatory)"), (2025, "extra", "B1", "E5", 0, "coil 50 turns in changing B"),
    (2025, "extra", "B2", "E1", 0, "charges qA, qB (3:1), equilibrium"), (2025, "extra", "C1", "O1", 0, "monochromatic ray, refraction"),
    (2025, "extra", "C2", "W2", 0, "SHM mechanical energy"), (2025, "extra", "D1", "M1", 0, "400 nm on a cerium photocathode"),
    (2025, "extra", "D2", "M1", 0, "photoelectric, two wavelengths"),
    (2026, "ord", "1", "G1", 1, "Starlink headline: geostationary orbit, fall (competencial)"), (2026, "ord", "2", "E5", 1, "weather-station microgenerator (competencial)"),
    (2026, "ord", "3a", "W3", 0, "violin string standing waves + decibels"), (2026, "ord", "3b", "O2", 0, "projector lens choice"),
    (2026, "ord", "4a", "M1", 0, "photoelectric, stopping potential, oxidised surface"), (2026, "ord", "4b", "M2", 0, "C-14 dating of bones"),
    (2026, "extra", "1", "G3", 1, "Mars probe: two orbits, Kepler check (competencial)"), (2026, "extra", "2", "E6", 1, "mass spectrometer (competencial)"),
    (2026, "extra", "3a", "W2", 0, "0.30 kg on a spring, Kmax = 15 J"), (2026, "extra", "3b", "O2", 0, "converging lens, object at 4f"),
    (2026, "extra", "4a", "M1", 0, "500 nm on a metal, threshold 612 nm"), (2026, "extra", "4b", "M2", 0, "Pu-239 decay"),
]
prob = pd.DataFrame(P, columns=["year", "sitting", "slot", "sub", "obligatory", "desc"])
prob["block"] = prob["sub"].map(lambda s: SUB[s][0])
prob["subtopic"] = prob["sub"].map(lambda s: SUB[s][1])
prob.to_csv(DATA / "ehu_problem_inventory_2010_2026.csv", index=False)

# ----------------------------------------------------------------------------- theory questions
# Official list "Evaluación para el Acceso a la Universidad: Cuestiones teóricas" (UPV/EHU – Departamento de
# Educación; bilingual, 22 titles with a development guide each, also sent to correctors); provided by the
# coordinator on 19 Sep 2026: sources/exams_ehu_hist/ehu_theory_list_official.pdf. T-codes map to its numbering.
T = {
    "T04": (1, "Movimiento armónico simple. Ejemplos. Ecuación. Definición de las magnitudes. Ecuaciones de la velocidad y de la aceleración."),
    "T15": (2, "Movimiento ondulatorio en una dimensión. Ecuación. Definición de las magnitudes. Velocidad de propagación. Distinción entre ondas transversales y longitudinales."),
    "T09": (3, "Reflexión y refracción de ondas: concepto, índice de refracción, leyes… Conceptos de ángulo límite y reflexión total."),
    "T20": (4, "Ondas estacionarias. Definición y ejemplos."),
    "T08": (5, "Lupa. Descripción. Esquema de la formación de imágenes. Aumento."),
    "T21": (6, "Cámara fotográfica. Descripción. Esquema de la formación de imágenes."),
    "T14": (7, "El ojo humano. Descripción. Esquema de la formación de imágenes."),
    "T13": (8, "Defectos de la visión. Hipermetropía y miopía."),
    "T12": (9, "Ley de Gravitación Universal de Newton. Intensidad de campo. Campo creado por una masa puntual (o esférica). Ejemplo: el campo gravitatorio terrestre."),
    "T17": (10, "Campos de fuerza conservativos y no conservativos. Energía potencial gravitatoria. Potencial gravitatorio. Energía mecánica total. Principio de conservación de la energía."),
    "T02": (11, "Leyes de Kepler. Enunciados. Deducción de la 3ª Ley para órbitas circulares a partir de la Ley de Gravitación."),
    "T16": (12, "Líneas de fuerza y superficies equipotenciales en el campo gravitatorio creado por una masa puntual (o esférica)."),
    "T06": (13, "Ley de Coulomb. Intensidad de campo eléctrico. Campo electrostático creado por una carga puntual positiva y negativa; líneas de fuerza."),
    "T10": (14, "Fuerza ejercida dentro de un campo magnético uniforme: a) sobre una carga puntual en movimiento; b) sobre un conductor lineal de corriente."),
    "T11": (15, "Fuerzas entre corrientes eléctricas. Dos hilos rectos, paralelos e infinitos. Definición de amperio."),
    "T22": (16, "Campos magnéticos producidos por corrientes. Ley de Biot-Savart: a) corriente recta e infinita; b) corriente circular (espira)."),
    "T05": (17, "Ley de Faraday y Lenz para la inducción electromagnética. Valor de la fuerza electromotriz inducida. Sentido de la corriente."),
    "T19": (18, "Generador de corrientes alternas sinusoidales (alternador)."),
    "T03": (19, "Efecto fotoeléctrico. Descripción. Explicación cuántica. Teoría de Einstein. Frecuencia umbral. Trabajo de extracción."),
    "T01": (20, "Radiactividad natural. Desintegración radiactiva. Emisión de partículas alfa, beta y gamma. Leyes de Soddy y Fajans."),
    "T07": (21, "Fisión nuclear. Descripción y ejemplos. Bombas y centrales nucleares. Pérdida de masa. Ecuación de Einstein."),
    "T18": (22, "Fusión nuclear. Descripción y ejemplos. Bombas y posibles centrales nucleares. Pérdida de masa. Ecuación de Einstein."),
}
Q = [
    (2010, "ord", "A.C1", "T22"), (2010, "ord", "A.C2", "T06"), (2010, "ord", "B.C1", "T02"), (2010, "ord", "B.C2", "T07"),
    (2010, "extra", "A.C1", "T05"), (2010, "extra", "A.C2", "T15"), (2010, "extra", "B.C1", "T17"), (2010, "extra", "B.C2", "T01"),
    (2011, "ord", "A.C1", "T10"), (2011, "ord", "A.C2", "T08"), (2011, "ord", "B.C1", "T06"), (2011, "ord", "B.C2", "T01"),
    (2011, "extra", "A.C1", "T11"), (2011, "extra", "A.C2", "T06"), (2011, "extra", "B.C1", "T05"), (2011, "extra", "B.C2", "T03"),
    (2012, "ord", "A.C1", "T09"), (2012, "ord", "A.C2", "T07"), (2012, "ord", "B.C1", "T02"), (2012, "ord", "B.C2", "T03"),
    (2012, "extra", "A.C1", "T05"), (2012, "extra", "A.C2", "T01"), (2012, "extra", "B.C1", "T04"), (2012, "extra", "B.C2", "T06"),
    (2013, "ord", "A.C1", "T02"), (2013, "ord", "A.C2", "T07"), (2013, "ord", "B.C1", "T06"), (2013, "ord", "B.C2", "T04"),
    (2013, "extra", "A.C1", "T13"), (2013, "extra", "A.C2", "T05"), (2013, "extra", "B.C1", "T15"), (2013, "extra", "B.C2", "T03"),
    (2014, "ord", "A.C1", "T08"), (2014, "ord", "A.C2", "T11"), (2014, "ord", "B.C1", "T18"), (2014, "ord", "B.C2", "T12"),
    (2014, "extra", "A.C1", "T17"), (2014, "extra", "A.C2", "T04"), (2014, "extra", "B.C1", "T02"), (2014, "extra", "B.C2", "T01"),
    (2015, "ord", "A.C1", "T01"), (2015, "ord", "A.C2", "T19"), (2015, "ord", "B.C1", "T02"), (2015, "ord", "B.C2", "T14"),
    (2015, "extra", "A.C1", "T03"), (2015, "extra", "A.C2", "T12"), (2015, "extra", "B.C1", "T05"), (2015, "extra", "B.C2", "T04"),
    (2016, "ord", "A.C1", "T06"), (2016, "ord", "A.C2", "T07"), (2016, "ord", "B.C1", "T08"), (2016, "ord", "B.C2", "T12"),
    (2016, "extra", "A.C1", "T10"), (2016, "extra", "A.C2", "T03"), (2016, "extra", "B.C1", "T02"), (2016, "extra", "B.C2", "T01"),
    (2017, "ord", "A.C1", "T07"), (2017, "ord", "A.C2", "T11"), (2017, "ord", "B.C1", "T16"), (2017, "ord", "B.C2", "T09"),
    (2017, "extra", "A.C1", "T02"), (2017, "extra", "A.C2", "T14"), (2017, "extra", "B.C1", "T01"), (2017, "extra", "B.C2", "T06"),
    (2018, "ord", "A.C1", "T18"), (2018, "ord", "A.C2", "T17"), (2018, "ord", "B.C1", "T15"), (2018, "ord", "B.C2", "T05"),
    (2018, "extra", "A.C1", "T02"), (2018, "extra", "A.C2", "T01"), (2018, "extra", "B.C1", "T20"), (2018, "extra", "B.C2", "T10"),
    (2019, "ord", "A.C1", "T13"), (2019, "ord", "A.C2", "T03"), (2019, "ord", "B.C1", "T06"), (2019, "ord", "B.C2", "T19"),
    (2019, "extra", "A.C1", "T22"), (2019, "extra", "A.C2", "T20"),
    (2020, "ord", "B1", "T09"), (2020, "ord", "B2", "T02"), (2020, "ord", "B3", "T08"), (2020, "ord", "B4", "T16"),
    (2020, "extra", "B1", "T12"), (2020, "extra", "B2", "T18"), (2020, "extra", "B3", "T03"), (2020, "extra", "B4", "T14"),
    (2021, "ord", "B1", "T05"), (2021, "ord", "B2", "T13"), (2021, "ord", "B3", "T04"), (2021, "ord", "B4", "T01"),
    (2021, "extra", "B1", "T09"), (2021, "extra", "B2", "T21"), (2021, "extra", "B3", "T10"), (2021, "extra", "B4", "T03"),
    (2022, "ord", "B1", "T04"), (2022, "ord", "B2", "T20"), (2022, "ord", "B3", "T14"), (2022, "ord", "B4", "T16"),
    (2022, "extra", "B1", "T08"), (2022, "extra", "B2", "T11"), (2022, "extra", "B3", "T01"), (2022, "extra", "B4", "T15"),
    (2023, "ord", "B1", "T15"), (2023, "ord", "B2", "T17"), (2023, "ord", "B3", "T05"), (2023, "ord", "B4", "T07"),
    (2023, "extra", "B1", "T08"), (2023, "extra", "B2", "T11"), (2023, "extra", "B3", "T01"), (2023, "extra", "B4", "T13"),
    (2024, "ord", "B1", "T09"), (2024, "ord", "B2", "T10"), (2024, "ord", "B3", "T03"), (2024, "ord", "B4", "T01"),
    (2024, "extra", "B1", "T04"), (2024, "extra", "B2", "T02"), (2024, "extra", "B3", "T16"), (2024, "extra", "B4", "T19"),
]
theo = pd.DataFrame(Q, columns=["year", "sitting", "slot", "title_id"])
theo["official_no"] = theo.title_id.map(lambda k: T[k][0])
theo["title"] = theo.title_id.map(lambda k: T[k][1])
theo.to_csv(DATA / "ehu_theory_inventory.csv", index=False)

# ----------------------------------------------------------------------------- formats
FORMATS = pd.DataFrame([
    dict(period="2010–2019", label="Two whole options (A/B)", problems="2 × 3 pts", questions="2 × 2 pts (closed list of titles)",
         theory_pts=4, choice="choose one of two complete papers", n_items_offered=8, n_answered=4, optional_pct=100),
    dict(period="2020–2024", label="Four-of-eight (COVID format, kept to 2024)", problems="answer 2 of 4 (3 pts each)",
         questions="answer 2 of 4 (2 pts each, closed list)", theory_pts=4, choice="any 2 of 4 problems and any 2 of 4 questions",
         n_items_offered=8, n_answered=4, optional_pct=100),
    dict(period="2025", label="LOMLOE year 1", problems="4 × 2.5 pts; block A competencial and obligatory; B, C, D choose 1 of 2",
         questions="none (theory only through explanations inside problems)", theory_pts=0, choice="1 of 2 in three blocks",
         n_items_offered=7, n_answered=4, optional_pct=75),
    dict(period="2026", label="LOMLOE year 2", problems="4 × 2.5 pts; 1 and 2 competencial and obligatory; 3 and 4 choose a/b",
         questions="none", theory_pts=0, choice="1 of 2 in two blocks", n_items_offered=6, n_answered=4, optional_pct=50),
])
FORMATS.to_csv(DATA / "ehu_formats.csv", index=False)

# ----------------------------------------------------------------------------- selection premium simulation
rng = np.random.default_rng(7)
N = 200_000


def sim(sd_item: float, ability_mean=0.55, ability_sd=0.20):
    """Expected total score (0–10) under each format for the same population and item noise.

    Ability a ~ N(mean, sd) clipped to [0,1]; each item is scored as a fraction
    p = clip(a + e, 0, 1), e ~ N(0, sd_item); the paper score is the points-weighted sum of the
    items the student answers under the format's rule (choosing the best available items).
    """
    a = np.clip(rng.normal(ability_mean, ability_sd, N), 0, 1)

    def item(pts):
        return pts * np.clip(a + rng.normal(0, sd_item, N), 0, 1)

    out = {}
    # baseline: no choice, 4 items of 2.5
    out["no choice (4 × 2.5)"] = sum(item(2.5) for _ in range(4))
    # 2010–2019: option A = 2 problems (3) + 2 questions (2); option B same; choose the better total
    optA = item(3) + item(3) + item(2) + item(2)
    optB = item(3) + item(3) + item(2) + item(2)
    out["2010–19: better of two options"] = np.maximum(optA, optB)
    # 2020–2024: best 2 of 4 problems (3) + best 2 of 4 questions (2)
    pr = np.sort(np.stack([item(3) for _ in range(4)], 1), 1)[:, -2:].sum(1)
    qu = np.sort(np.stack([item(2) for _ in range(4)], 1), 1)[:, -2:].sum(1)
    out["2020–24: best 2 of 4 + best 2 of 4"] = pr + qu
    # 2025: obligatory 2.5 + three blocks best of two 2.5
    out["2025: 1 obligatory + 3 × best of 2"] = item(2.5) + sum(np.maximum(item(2.5), item(2.5)) for _ in range(3))
    # 2026: two obligatory + two blocks best of two
    out["2026: 2 obligatory + 2 × best of 2"] = item(2.5) + item(2.5) + sum(np.maximum(item(2.5), item(2.5)) for _ in range(2))
    return {k: float(v.mean()) for k, v in out.items()}


rows = []
for sd in (0.10, 0.20, 0.30):
    r = sim(sd)
    base = r["no choice (4 × 2.5)"]
    for k, v in r.items():
        rows.append(dict(item_sd=sd, format=k, expected_score=v, premium_vs_no_choice=v - base))
prem = pd.DataFrame(rows)
prem.to_csv(DATA / "ehu_selection_premium.csv", index=False)

# ----------------------------------------------------------------------------- tables
def md(df_, cols, headers, fmts):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for _, r in df_.iterrows():
        out.append("| " + " | ".join(f.format(r[c]) for c, f in zip(cols, fmts)) + " |")
    return "\n".join(out) + "\n"

(TABLES / "ehu_formats.md").write_text(md(FORMATS, ["period", "label", "problems", "questions", "choice", "optional_pct"],
                                         ["Years", "Format", "Problems", "Theory questions", "Choice", "Optional %"],
                                         ["{}", "{}", "{}", "{}", "{}", "{}"]))

# theory titles with counts (2012–2024 = the stable list) and all years
cnt_all = theo.groupby("title_id").size()
cnt_1224 = theo[theo.year.between(2012, 2024)].groupby("title_id").size()
tt = pd.DataFrame({"title_id": list(T.keys()), "no": [v[0] for v in T.values()], "title": [v[1] for v in T.values()]})
tt["n_2012_2024"] = tt.title_id.map(cnt_1224).fillna(0).astype(int)
tt["n_2010_2024"] = tt.title_id.map(cnt_all).fillna(0).astype(int)
tt = tt.sort_values("no")
(TABLES / "ehu_theory_titles.md").write_text(md(tt, ["no", "title", "n_2012_2024", "n_2010_2024"],
                                                ["No.", "Title in the official list (Spanish version, abridged)", "Times set 2012–2024", "Times set 2010–2024"],
                                                ["{}", "{}", "{}", "{}"]))

# problem sub-topic counts by period
prob["period"] = pd.cut(prob.year, [2009, 2019, 2024, 2025, 2026], labels=["2010–19", "2020–24", "2025", "2026"])
piv = prob.pivot_table(index="sub", columns="period", values="slot", aggfunc="count", fill_value=0, observed=False)
piv = piv.reindex(list(SUB.keys())).fillna(0).astype(int).reset_index()
piv["block"] = piv["sub"].map(lambda s: SUB[s][0]); piv["subtopic"] = piv["sub"].map(lambda s: SUB[s][1])
piv["total_2010_24"] = piv["2010–19"] + piv["2020–24"]
(TABLES / "ehu_problem_topics.md").write_text(md(piv, ["block", "subtopic", "2010–19", "2020–24", "2025", "2026"],
                                                  ["Block", "Problem sub-topic", "2010–19 (20 papers)", "2020–24 (10 papers)", "2025 (2)", "2026 (2)"],
                                                  ["{}", "{}", "{}", "{}", "{}", "{}"]))

# selection premium table
pp = prem.pivot(index="format", columns="item_sd", values="premium_vs_no_choice").reset_index()
order = ["no choice (4 × 2.5)", "2026: 2 obligatory + 2 × best of 2", "2025: 1 obligatory + 3 × best of 2",
         "2010–19: better of two options", "2020–24: best 2 of 4 + best 2 of 4"]
pp["o"] = pp["format"].map({k: i for i, k in enumerate(order)})
pp = pp.sort_values("o")
pp.columns = [str(c) for c in pp.columns]
(TABLES / "ehu_selection_premium.md").write_text(md(pp, ["format", "0.1", "0.2", "0.3"],
                                                     ["Format (selection rule)", "Premium, item SD 0.10", "Premium, item SD 0.20", "Premium, item SD 0.30"],
                                                     ["{}", "{:+.2f}", "{:+.2f}", "{:+.2f}"]))

# marking rules table (hand-made from the corrector documents)
MARK = pd.DataFrame([
    ("País Vasco 2012–2024", "no", "qualitative: 'se penalizará' missing units, purely mathematical developments, incoherent results; no amounts", "no", "no", "no"),
    ("País Vasco 2025", "no", "units mandatory in the final answer; significant figures and exponent notation 'penalised' (no amount); conceptual errors weigh more than calculation errors", "−0.1 from the 3rd error, cap 1 pt; syntax/coherence up to −0.5, total cap 1 pt", "no", "no"),
    ("País Vasco 2026", "yes", "−0.1 units; −0.1 repeated vector-symbol errors; −0.1 rounding/significant figures; grave errors (wrong equations, scalar/vector confusion) can void the section", "as 2025", "0.25-pt sub-items (a.1, a.2 …)", "yes (constants table on the paper)"),
    ("Canarias 2025 and 2026", "no", "full CRUE list: −0.1 units, vector symbol, prefixes, factor of 10, transcription, rounding; grave errors void the section", "not stated in the Física document", "sections of 1–1.5 pts", "no"),
    ("Comunitat Valenciana 2025 and 2026", "yes ('realiza primero el cálculo simbólico')", "60 % symbolic set-up and explanation / 40 % numerical result; units and significant figures worth +0.1", "linguistic criteria applied (general PAU rule)", "0.1-pt detail in the criteria", "no"),
    ("Cataluña 2025 and 2026", "no", "−0.25 per problem for unit errors; item-specific deductions (−0.1, −0.25) in the pauta", "linguistic correction stated", "0.25-pt detail", "no"),
    ("Madrid 2025 and 2026", "no", "'destreza en la obtención de resultados numéricos y el uso correcto de las unidades'; marks in multiples of 0.25 (2025) / 0.1 (2026)", "coherence, cohesion, spelling 'se evaluará'", "0.25 / 0.1", "no"),
    ("Asturias 2025 and 2026", "no", "−0.25 per section for a missing/incorrect unit of a calculated magnitude", "general PAU rule", "—", "yes (constants table on the paper)"),
    ("Andalucía 2025 and 2026", "no", "unit omission or misuse: at most −0.25 per exercise", "2026: −0.1 from the 3rd spelling error (Junta general rule)", "0.25 / 0.5 sub-sections", "no"),
    ("Extremadura 2025 and 2026", "no", "2025: unit errors up to −1 pt in the exam; 2026: −50 % of the section for a unit error, cap 1 pt", "−0.1 from the 3rd error, cap 1 pt; syntax/vocabulary up to −0.5 (same wording as EHU 2025)", "0.1–0.3 detail", "no"),
    ("Castilla-La Mancha 2026", "no", "not read (paper only)", "−0.25 per 3 faults, cap 1 pt (on the paper)", "—", "no"),
], columns=["paper", "symbolic_first", "units_and_error_rules", "language_rules", "granularity", "constants_table"])
MARK.to_csv(DATA / "marking_rules_2025_2026.csv", index=False)
(TABLES / "marking_rules.md").write_text(md(MARK, list(MARK.columns),
                                             ["Corrector document", "Symbolic-first rule", "Units and error rules", "Language rules", "Granularity", "Constants table"],
                                             ["{}"] * 6))

# ----------------------------------------------------------------------------- figures
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Colours come from the shared registry so a hue means the same thing in every
# figure of the study (ThesisFigures C1); styling is the shared module's job (E1).
from plot_style import C, apply_style

apply_style()

BLUE, ORANGE, AQUA, YELLOW = C["blue"], C["orange"], C["aqua"], C["yellow"]
MAGENTA, VIOLET, RED = C["magenta"], C["violet"], C["red"]
GREY = "#6b7280"

# Fig 13: sub-topic × year matrix of problems (ordinary + extraordinary pooled), counts 0–2+
years = list(range(2010, 2027))
subs = list(SUB.keys())
M = np.zeros((len(subs), len(years)))
for _, r in prob.iterrows():
    M[subs.index(r["sub"]), years.index(r.year)] += 1
fig, ax = plt.subplots(figsize=(12.5, 7.2))
cmap = ListedColormap(["#f3f4f6", "#9ec5f2", BLUE, "#123e78"])
im = ax.imshow(np.minimum(M, 3), cmap=cmap, vmin=0, vmax=3, aspect="auto")
ax.set_xticks(range(len(years)))
ax.set_xticklabels(years, rotation=0, fontsize=8.5)
ax.set_yticks(range(len(subs)))
ax.set_yticklabels([f"{s}  {SUB[s][1]}" for s in subs], fontsize=8.5)
for i, s in enumerate(subs):
    for j, y in enumerate(years):
        v = int(M[i, j])
        if v:
            ax.text(j, i, str(v), ha="center", va="center", fontsize=7.5, color="white" if v >= 2 else "#111")
# block separators
bounds = [i for i in range(1, len(subs)) if SUB[subs[i]][0] != SUB[subs[i - 1]][0]]
for b in bounds:
    ax.axhline(b - 0.5, color="white", lw=2.5)
ax.axvline(years.index(2025) - 0.5, color=RED, lw=1.5, ls="--")
ax.axvline(years.index(2020) - 0.5, color=GREY, lw=1, ls=":")
ax.text(years.index(2025) - 0.4, -0.9, "LOMLOE papers →", color=RED, fontsize=8.5)
ax.text(years.index(2020) - 0.4, -0.9, "4-of-8 format →", color=GREY, fontsize=8.5)
ax.set_title("EHU Física papers 2010–2026: number of problems set per sub-topic and year (ordinary + extraordinary sittings)",
             loc="left", fontsize=10.5, pad=18)
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
fig.text(0.01, 0.005, "Each year pools the June and July papers: 8 problems a year (4 per paper) in 2010–24, 14 (7 per paper) in 2025, 12 (6 per paper) in 2026; every option counted.\n"
         "Rows that never carried a problem before 2025: spherical mirrors (2025), standing waves (with sound levels, coded under W3) and radioactive decay (2026), the mass spectrometer (July 2026).",
         fontsize=7.5, color=GREY)
fig.tight_layout(rect=(0, 0.045, 1, 1))
fig.savefig(PLOTS / "fig13_ehu_topics.png", dpi=170)
fig.savefig(PLOTS / "fig13_ehu_topics.svg")

# Fig 14: series with format regimes and theory share
ser = pd.read_csv(DATA / "analysis" / "euskadi_fisica_series_2010_2026.csv")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6.4), sharex=True, gridspec_kw=dict(height_ratios=[3, 1.3]))
spans = [(2009.5, 2019.5, "#e8f0fb", "Two whole options A/B\n2 problems (3) + 2 theory questions (2)"),
         (2019.5, 2024.5, "#fff4e0", "Four-of-eight\nany 2 of 4 problems, any 2 of 4 questions"),
         (2024.5, 2025.5, "#fde4e4", "2025: 1 competencial\n+ 3 × (1 of 2); no theory"),
         (2025.5, 2026.5, "#f9c9c9", "2026: 2 competencial\n+ 2 × (a/b)")]
for k, (x0, x1, c, lab) in enumerate(spans):
    ax1.axvspan(x0, x1, color=c, lw=0)
    if k < 2:
        ax1.text((x0 + x1) / 2, 8.9, lab, ha="center", va="top", fontsize=7.8, color="#333")
ax1.text(2025.5, 8.9, "LOMLOE\n2025: 1 competencial\n+ 3 × (1 of 2); no theory\n2026: 2 competencial\n+ 2 × (a/b)", ha="center", va="top", fontsize=7.2, color="#7a1f1f")
ax1.plot(ser.year, ser["mean"], color=BLUE, lw=2, marker="o", ms=4)
for _, r in ser.iterrows():
    ax1.text(r.year, r["mean"] + 0.18, f"{r['mean']:.2f}", ha="center", fontsize=7.2, color="#222")
ax1.set_ylim(3, 9.2)
ax1.set_ylabel("Física mean, ordinary sitting")
ax1.set_title("The Basque Física mean 2010–2026 against the paper's format", loc="left", fontsize=10.5)
# lower panel: theory points and optional share
th = [4 if y <= 2024 else 0 for y in ser.year]
opt = [100 if y <= 2024 else (75 if y == 2025 else 50) for y in ser.year]
ax2.bar(ser.year - 0.2, th, 0.4, color=AQUA, label="points from closed-list theory questions")
ax2.set_ylabel("theory pts", color=AQUA)
ax2.set_ylim(0, 5)
ax2b = ax2.twinx()
ax2b.bar(ser.year + 0.2, opt, 0.4, color=YELLOW, label="optional share of the paper (%)")
ax2b.set_ylim(0, 110)
ax2b.set_ylabel("optional %", color="#b07a00")
ax2b.spines["top"].set_visible(False)
ax2.set_xticks(ser.year)
ax2.set_xlabel("year (ordinary sitting)")
h1, l1 = ax2.get_legend_handles_labels()
h2, l2 = ax2b.get_legend_handles_labels()
ax2.legend(h1 + h2, l1 + l2, loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=8, frameon=False, ncol=2)
fig.tight_layout()
fig.savefig(PLOTS / "fig14_ehu_formats_series.png", dpi=170)
fig.savefig(PLOTS / "fig14_ehu_formats_series.svg")

# Fig 15: selection premium
fig, ax = plt.subplots(figsize=(9, 4.2))
sub_ = prem[prem["format"] != "no choice (4 × 2.5)"]
labels = [k for k in order if k != "no choice (4 × 2.5)"]
x = np.arange(len(labels))
for i, sd in enumerate((0.10, 0.20, 0.30)):
    vals = [float(sub_[(sub_["format"] == k) & (sub_.item_sd == sd)].premium_vs_no_choice.iloc[0]) for k in labels]
    ax.bar(x + (i - 1) * 0.26, vals, 0.26, color=[YELLOW, ORANGE, RED][i], label=f"item-to-item SD {sd:.2f}")
    for xi, v in zip(x + (i - 1) * 0.26, vals):
        ax.text(xi, v + 0.02, f"{v:+.2f}", ha="center", fontsize=7.5)
ax.set_xticks(x)
ax.set_xticklabels([l.replace(": ", ":\n") for l in labels], fontsize=8.5)
ax.set_ylabel("expected gain over a paper with no choice (points /10)")
ax.set_title("Model: how much each EHU format adds to the expected score through choice alone", loc="left", fontsize=10.5)
ax.legend(frameon=False, fontsize=8.5)
fig.text(0.01, 0.005, "Simulation, 200 000 students: ability a ~ N(0.55, 0.20) clipped to [0,1]; each item scored as clip(a + e, 0, 1) × points with e ~ N(0, SD);\n"
         "the student answers the best items the rule allows. Same population and same items in every row; only the rule changes.", fontsize=7.3, color=GREY)
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig(PLOTS / "fig15_selection_premium.png", dpi=170)
fig.savefig(PLOTS / "fig15_selection_premium.svg")

summary = dict(
    n_papers=int(prob.groupby(["year", "sitting"]).ngroups),
    n_problems=int(len(prob)), n_questions=int(len(theo)),
    n_titles_2012_2024=int(cnt_1224.size), n_titles_all=int(cnt_all.size),
    modern_problems_2010_2024=prob[(prob.year <= 2024) & (prob.block == "Moderna")]["sub"].value_counts().to_dict(),
    subtopics_first_set_2025_26=[s for s in subs if M[subs.index(s), :years.index(2025)].sum() == 0 and M[subs.index(s), years.index(2025):].sum() > 0],
    subtopics_never=[s for s in subs if M[subs.index(s)].sum() == 0],
    premium=prem.to_dict(orient="records"),
)
(DATA / "ehu_history_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
print(json.dumps({k: v for k, v in summary.items() if k != "premium"}, indent=2, ensure_ascii=False))
print(pp.to_string(index=False))
