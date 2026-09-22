"""One mechanical measure of examined reasoning in the Catalan papers, 2010–2025.

Why this exists. The dossier can say that the Basque paper converted and that the
Catalan paper was already converted, but until now it could not say so on a single
measure: the nine-community coding counts *competency-coded share of marks* on two
years, and the Catalan history script counted a Catalan verb list. Neither travels.

This script applies the same operational definition to both archives across
seventeen years: **what share of a paper's items require the candidate to justify,
explain, reason, evaluate, interpret or say why**, as against computing, stating or
describing. It is deliberately crude and deliberately mechanical, so that it is
reproducible and so that its failures are visible.

THE BASQUE ARCHIVE IS NOT MEASURED HERE, and that is a result of this script rather
than an omission. The same splitter applied to the Basque papers returns 7, 8, 10, 11,
11, 12, 11, 11, 12, 11 items for 2010–2019 and 5 to 8 thereafter, against the 8, 8, 7
and 6 items those papers are known to offer (`data/ehu_formats.csv`). The text layer
of the Basque PDFs does not parse into items reliably — some years yield only the
theory titles, some duplicate a problem under two renderings of a degree symbol — so a
year-by-year Basque series on this measure would be an artefact of extraction. The
Basque side of the comparison therefore uses the hand coding of competency-carried
marks, which is a different measure and is labelled as such wherever the two are set
side by side.

Three corrections were needed and are recorded because the first version of this
measure produced a false finding without them:

  1. NOUNS. 'los valores de la frecuencia' matched a bare /valor/ stem, and
     'Explicación cuántica' — a theory *title*, i.e. something to recall — matched
     a bare /explic/ stem. Both are excluded by requiring inflected verb forms at
     word boundaries. Uncorrected, they put the 2024 Basque paper at 37.5 % when
     its true value is far lower, which would have manufactured an instrument
     change in the one year the dossier says the instrument did not move.
  2. DUPLICATES. Some extractions repeat an item (the same problem appears twice
     in the text layer). Items are de-duplicated on their normalised first 200
     characters before counting.
  3. THEORY TITLES. A Basque 'C' item is a recall title, not a demand. Titles are
     detected by the absence of any second-person or usted imperative and are
     counted as items but never as demand.

LIMITATION. A verb list is not a reading. It cannot see a demand phrased without
one of these verbs, and it cannot tell a token justification from a real one. It is
used here for one purpose only — dating a change within each archive on a rule that
does not know which year it is looking at.
"""
import io
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EHU = ROOT / "sources" / "exams_ehu_hist"
CAT = ROOT / "data" / "catalunya"
OUT = ROOT / "data" / "analysis"

# Inflected verb forms only, at word boundaries. Imperative (tú), imperative
# (usted/subjunctive), infinitive, and the adverb 'razonadamente'.
ES = re.compile(
    r"\b(?:justifica|justifique|justificar|justificad|justificando"
    r"|razona|razone|razonar|razonad|razonadamente"
    r"|explica|explique|explicar|explicad"
    r"|valora|valore|valorar|valorad"
    r"|comenta|comente|comentar|comentad"
    r"|argumenta|argumente|argumentar"
    r"|interpreta|interprete|interpretar"
    r"|discute|discuta|discutir"
    r"|juzga|juzgue"
    r"|por qu[ée])\b", re.I)

# Catalan PAU uses the 2nd-person plural imperative throughout, which is
# unambiguous: these forms are not nouns.
CA = re.compile(
    r"\b(?:justifiqueu|raoneu|expliqueu|valoreu|comenteu|argumenteu"
    r"|interpreteu|discutiu|jutgeu|per qu[eè])\b", re.I)

EHU_SPLIT = re.compile(
    r"\n\s*(?:[PC]\s*\d+\s*[\.\)\s]|[AB]\.\s*\d+\s*\.?\-"
    r"|\d+\.\s+Problema,\s*BLOQUE)", re.I)
CAT_SPLIT_OLD = re.compile(r"\n\s*P\d\)")
CAT_SPLIT_NEW = re.compile(r"\n\s*Exercici\s*\d")

# A recall title has no imperative addressed to the candidate anywhere in it.
ADDRESS = re.compile(
    r"\b(?:calcula|calcule|calcular|determina|determine|determinar|halla|halle"
    r"|hallar|obt[eé]n|obtenga|obtener|indica|indique|indicar|escribe|escriba"
    r"|dibuja|dibuje|representa|represente|deduce|deduzca|demuestra|demuestre"
    r"|justifica|justifique|razona|razone|explica|explique|valora|valore"
    r"|comenta|comente|eval[uú]a|eval[uú]e|estima|estime|compara|compare"
    r"|\?|calculeu|determineu|trobeu|indiqueu|dibuixeu|expliqueu|justifiqueu)",
    re.I)


def _items(text: str, splitter: re.Pattern) -> list[str]:
    parts = splitter.split(text)[1:]
    out, seen = [], set()
    for p in parts:
        p = re.sub(r"\s+", " ", p).strip()
        if len(p) < 120:
            continue
        key = p[:200].lower()
        if key in seen:                      # correction 2: duplicate extraction
            continue
        seen.add(key)
        out.append(p)
    return out


def measure(text: str, splitter: re.Pattern, demand: re.Pattern) -> dict:
    items = _items(text, splitter)
    titles = [p for p in items if not ADDRESS.search(p)]
    k = sum(1 for p in items if demand.search(p) and ADDRESS.search(p))
    return {"items": len(items), "titles": len(titles), "with_demand": k,
            "demand_pct": round(100 * k / len(items), 1) if items else None}


def main() -> None:
    rows = []
    for y in range(2005, 2026):
        f = CAT / f"{y}.txt"
        if f.exists():
            t = io.open(f, encoding="utf-8", errors="ignore").read()
            sp = CAT_SPLIT_NEW if y >= 2025 else CAT_SPLIT_OLD
            r = measure(t, sp, CA)
            if r["items"]:
                rows.append({"system": "Cataluña", "year": y, **r})

    d = pd.DataFrame(rows)
    d.to_csv(OUT / "demand_history_two_systems.csv", index=False)

    print(d.to_string(index=False))

    summary = {}
    for sysname in ("Cataluña",):
        s = d[d.system == sysname].set_index("year").demand_pct
        summary[sysname] = {
            "2010_2019_mean": round(float(s.loc[2010:2019].mean()), 1),
            "2010_2019_sd": round(float(s.loc[2010:2019].std(ddof=1)), 1),
            "2010_2019_max": float(s.loc[2010:2019].max()),
            "2020_2023_mean": round(float(s.loc[2020:2023].mean()), 1),
            "2024": float(s.loc[2024]),
            "last_two": [float(v) for v in s.loc[2025:].values],
        }
    json.dump(summary, open(OUT / "demand_history_two_systems.json", "w"),
              indent=1, ensure_ascii=False)
    print()
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
