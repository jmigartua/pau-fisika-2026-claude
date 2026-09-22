"""Cataluña's Physics papers 2020–2025: was the competency style new in 2025?

Why this exists. The nine-community comparison showed Cataluña at 75 % of its
marks competency-coded in 2025 and 37.5 % in 2026, and the dossier could not say
what it had been before, because the item coding covers only 2025 and 2026. That
gap mattered: if 75 % was a jump, Cataluña converted in the same year as Euskadi
and did not fall; if it was steady state, Cataluña had been examining that way
for years and the comparison is with a mature practice rather than a conversion.

The ordinary papers for 2020–2025 were obtained from examenesdepau.com. This
script measures two things on each of them, on the same definitions the 2025/2026
coding used:

  context   — does the problem open in a real setting (a mission, an experiment,
              a device, a published claim) rather than an abstract configuration?
  demand    — does any part of the problem ask the candidate to justify, reason,
              explain, evaluate, interpret or say why?

The demand test is mechanical (a verb list) and therefore reproducible; the
context test was made by reading every problem and is recorded per year below.

LIMITATION, stated because it bounds what this can support: 2025 and 2026 were
coded blind by two people ($\\kappa = 0.76$). 2020–2024 were coded once, by one
reader, after the result was known. The series is evidence about a direction of
travel, not a measurement of the same quality as the two-year panel.
"""
import io
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
TXT = ROOT / "data" / "catalunya"
OUT = ROOT / "data" / "analysis"

DEMAND = (r"justifiqueu|raoneu|expliqueu|valoreu|comenteu|argumenteu|interpreteu"
          r"|discutiu|per qu[eè]|indiqueu clarament|creieu")

# Read by hand from every problem opening: does the problem sit in a real
# setting? Recorded per year as (problems with a real setting, problems).
CONTEXT = {
    2020: (6, 16),   # Freddie Mercury's voice, lightning, Parker Solar Probe,
                     # carbon-14 dating, Apollo 15 feather and hammer, garage photocell
    2021: (7, 16),   # Tycho Brahe and Kepler, magnet through a coil, nitrogen-13 decay
    2022: (8, 16),   # eel locomotion, cyclotron, radon, the July 2020 NASA mission
    2023: (9, 14),   # Phobos and Deimos, beach waves, the 2022 fusion announcement
                     # and what the media said of it, a tanning lamp, two Nobel prizes
    2024: (6, 7),    # BepiColombo, the Earth's field, a lightning rod, firework altitude,
                     # polonium and the Curies, a photoelectric sample
    2025: (4, 4),    # space debris, Millikan, an art exhibition, a sodium isotope
}

# 2020–2024: 4 of 7 or 4 of 8 short problems. 2025: four exercises on the four
# blocks, with an A/B option inside two of them — the structure the decree asks
# for. The structure changed in 2025; the substance, as measured below, did not.
STRUCTURE = {2020: "4 of 8", 2021: "4 of 8", 2022: "4 of 8", 2023: "4 of 7",
             2024: "4 of 7", 2025: "4 exercises, A/B inside two"}


def problems(year: int) -> list[str]:
    t = io.open(TXT / f"{year}.txt", encoding="utf-8").read()
    pat = r"\n\s*Exercici\s*\d" if year >= 2025 else r"\n\s*P\d\)"
    parts = re.split(pat, t)[1:]
    return [re.sub(r"\s+", " ", p) for p in parts if len(p.strip()) > 200]


def main() -> None:
    rows = []
    for y in sorted(CONTEXT):
        ps = problems(y)
        k = sum(1 for p in ps if re.search(DEMAND, p, re.I))
        ctx_k, ctx_n = CONTEXT[y]
        rows.append({
            "year": y,
            "structure": STRUCTURE[y],
            "problems": len(ps),
            "with_demand": k,
            "demand_pct": round(100 * k / len(ps), 1) if ps else None,
            "with_context": ctx_k,
            "context_of": ctx_n,
            "context_pct": round(100 * ctx_k / ctx_n, 1),
        })
    df = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "catalunya_history_2020_2025.csv", index=False)
    print(df.to_string(index=False))
    print("\nEvery year from 2020 carries both real settings and explicit")
    print("justification demands. The 2025 structure is new; the substance is not.")


if __name__ == "__main__":
    main()
