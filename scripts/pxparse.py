"""Minimal, dependency-free PC-Axis (.px) parser.

Reads the keyword header (STUB, HEADING, VALUES) and the DATA block and returns a tidy
pandas DataFrame with one row per cell.  Written for the Ministry EPAU cubes
(px_pau_gen_materias_*.px); handles quoted multi-line values, "(.)"/"(..)" missing codes
and the ISO-8859-15 code page declared in the files.
"""
from __future__ import annotations

import itertools
import re
from pathlib import Path

import pandas as pd


def _split_top_level(s: str, sep: str = ",") -> list[str]:
    """Split on `sep` outside double quotes."""
    out, cur, inq = [], [], False
    for ch in s:
        if ch == '"':
            inq = not inq
            cur.append(ch)
        elif ch == sep and not inq:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur:
        out.append("".join(cur))
    return out


def _unquote_list(s: str) -> list[str]:
    items = _split_top_level(s.strip())
    return [i.strip().strip('"') for i in items if i.strip()]


def parse_px(path: str | Path, encoding: str = "ISO-8859-15") -> pd.DataFrame:
    text = Path(path).read_text(encoding=encoding, errors="replace")
    head, _, data = text.partition("DATA=")
    # header: KEY("dim")=value;  statements end with ';' outside quotes
    stmts, cur, inq = [], [], False
    for ch in head:
        if ch == '"':
            inq = not inq
        if ch == ";" and not inq:
            stmts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    kv: dict[str, str] = {}
    values: dict[str, list[str]] = {}
    for st in stmts:
        st = st.strip()
        if not st or "=" not in st:
            continue
        key, _, val = st.partition("=")
        key = key.strip()
        m = re.match(r'VALUES\("(.+)"\)', key)
        if m:
            values[m.group(1)] = _unquote_list(val)
        else:
            kv[key] = val.strip()
    stub = _unquote_list(kv.get("STUB", ""))
    heading = _unquote_list(kv.get("HEADING", ""))
    dims = stub + heading
    # data block: whitespace separated tokens; missing values like "." / ".." / "(.)"
    tokens = re.findall(r'"[^"]*"|[^\s;]+', data)
    vals: list[float | None] = []
    for t in tokens:
        t = t.strip('"')
        if t in ("", ";"):
            continue
        t = t.strip("()")
        if t in (".", "..", "...", "-"):
            vals.append(None)
        else:
            try:
                vals.append(float(t.replace(",", ".")))
            except ValueError:
                vals.append(None)
    sizes = [len(values[d]) for d in dims]
    n = 1
    for s in sizes:
        n *= s
    if len(vals) != n:
        raise ValueError(f"cell count mismatch: {len(vals)} values for {n} cells {dict(zip(dims, sizes))}")
    idx = pd.MultiIndex.from_product([values[d] for d in dims], names=dims)
    df = pd.DataFrame({"value": vals}, index=idx).reset_index()
    df.attrs["title"] = kv.get("TITLE", "").strip('"')
    df.attrs["creation_date"] = kv.get("CREATION-DATE", "").strip('"')
    return df


if __name__ == "__main__":
    import sys

    df = parse_px(sys.argv[1])
    print(df.attrs["title"], df.shape)
    for c in df.columns[:-1]:
        u = df[c].unique().tolist()
        print(f"  {c}: {len(u)} -> {u[:12]}")
