"""Did Cataluña's change of examining model move its mean? An event study with an
honest power statement — and the answer is a bound, not a coefficient.

The question, asked by the coordinator: Cataluña converted to a competency style at
some point; if the conversion cost marks, the size of that cost is the closest thing
available to an external estimate of what a conversion costs, and it might be carried
across to Euskadi with caution.

Three steps.

1. DATE THE CHANGE from the papers. `35_demand_history.py` applies one mechanical
   rule to sixteen Catalan papers. The 2010s sit at 17.7 % of items carrying a
   justification demand (sd 10.9); 2020–2023 sit at 50.0 %. The step is at 2020.

2. MEASURE THE MEAN AGAINST THE FIELD, so that national shocks difference out, using
   the sixteen communities with a complete 2015–2025 Ministry series. 2020 and 2021
   are excluded throughout: they are the COVID sittings, in which every community's
   mean rose, and they are also the first two years of the new Catalan style, so they
   confound the thing being measured with the thing being controlled for.

3. STATE THE POWER BEFORE THE RESULT. With five pre years and four post years and a
   pre-period sd of 0.78, the smallest shift this design can detect at 80 % power is
   1.26 marks. Any estimate smaller than that is a number the design cannot resolve,
   and saying so is the point of computing it.
"""
import json
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from plot_style import C, INK, INK2, MUTED, apply_style, save as _save

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "analysis"
apply_style()

PRE = [2015, 2016, 2017, 2018, 2019]
COVID = [2020, 2021]
POST = [2022, 2023, 2024, 2025]


def main() -> None:
    d = pd.read_csv(OUT / "regional_long_series.csv")
    d = d[d.source == "ministry"]
    w = d.pivot_table(index="year", columns="ccaa", values="mean")
    full = w.columns[w.notna().sum() == 11]
    w = w[full]
    cat = w["Cataluña"]
    field = w.drop(columns=["Cataluña"]).mean(axis=1)
    diff = cat - field

    shift = diff[POST].mean() - diff[PRE].mean()
    t, p = stats.ttest_ind(diff[POST], diff[PRE], equal_var=False)

    vals = diff[PRE + POST].values
    obs = vals[5:].mean() - vals[:5].mean()
    hits = tot = 0
    for c in combinations(range(9), 4):
        m = np.zeros(9, bool)
        m[list(c)] = True
        tot += 1
        if abs(vals[m].mean() - vals[~m].mean()) >= abs(obs):
            hits += 1

    sp = np.sqrt((diff[PRE].var(ddof=1) + diff[POST].var(ddof=1)) / 2)
    mde = 2.9 * sp * np.sqrt(1 / len(PRE) + 1 / len(POST))

    res = {
        "field_n": int(len(full) - 1),
        "gap_pre_2015_2019": round(float(diff[PRE].mean()), 3),
        "gap_post_2022_2025": round(float(diff[POST].mean()), 3),
        "shift": round(float(shift), 3),
        "welch_t": round(float(t), 3), "welch_p": round(float(p), 3),
        "permutation_p": round(hits / tot, 3), "permutation_n": tot,
        "pooled_sd": round(float(sp), 3),
        "mde_80pct_power": round(float(mde), 2),
        "yoy_sd_of_gap": round(float(diff.diff().dropna().std(ddof=1)), 3),
        "largest_yoy_swing_no_model_change": round(float(diff.diff().loc[2017]), 3),
        "decomposition": {
            "catalunya_own_mean_change": round(float(cat[POST].mean() - cat[PRE].mean()), 3),
            "field_change": round(float(field[POST].mean() - field[PRE].mean()), 3),
            "share_of_gap_shift_that_is_the_field_rising":
                round(float(-(field[POST].mean() - field[PRE].mean()) / shift), 3),
        },
        "robustness": {},
    }
    for lbl, py in (("drop 2018", [2015, 2016, 2017, 2019]),
                    ("drop 2016 and 2018", [2015, 2017, 2019])):
        tt, pp = stats.ttest_ind(diff[POST], diff[py], equal_var=False)
        res["robustness"][lbl] = {"shift": round(float(diff[POST].mean() - diff[py].mean()), 3),
                                  "p": round(float(pp), 3)}
    res["robustness"]["medians"] = {
        "shift": round(float(diff[POST].median() - diff[PRE].median()), 3)}
    json.dump(res, open(OUT / "catalunya_event.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))

    # ---------------------------------------------------------------- figure
    dem = pd.read_csv(OUT / "demand_history_two_systems.csv").set_index("year")
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.0, 6.6), sharex=True,
                                 gridspec_kw=dict(hspace=0.30, height_ratios=[1, 1.15]))

    s = dem.loc[2010:2025, "demand_pct"]
    a1.bar(s.index, s.values, color=[C["violet"] if y >= 2020 else MUTED for y in s.index],
           width=0.72, zorder=2)
    a1.axhline(17.7, xmax=0.615, color=INK2, lw=1.3, ls="--", zorder=3)
    a1.axhline(50.0, xmin=0.615, xmax=0.87, color=C["violet"], lw=1.3, ls="--", zorder=3)
    a1.text(2009.4, 76, "2010–2019   mean 17.7 %, sd 10.9", fontsize=8.6, color=INK2,
            va="top", ha="left")
    a1.text(2009.4, 68, "2020–2023   mean 50.0 %", fontsize=8.6, color=C["violet"],
            va="top", ha="left", fontweight="bold")
    a1.annotate("never zero: the lowest\nCatalan year is 6.2 %", (2017.6, 6.2),
                textcoords="offset points", xytext=(0, 30), fontsize=8.2, color=INK2,
                ha="center", arrowprops=dict(arrowstyle="-", lw=0.8, color=MUTED))
    a1.set_ylabel("items demanding\njustification (%)")
    a1.set_title("a. The Catalan paper: one mechanical measure, sixteen years",
                 loc="left")
    a1.set_ylim(0, 80)

    a2.axhline(0, color=MUTED, lw=0.9, ls="--", zorder=1)
    a2.plot(diff.index, diff.values, "o-", color=INK, lw=1.6, ms=5, zorder=3)
    for ys, lab, col, dx, dy, ha in (
            (PRE, "2015–19  %+.2f" % diff[PRE].mean(), INK2, -0.55, 0.10, "right"),
            (POST, "2022–25  %+.2f" % diff[POST].mean(), C["violet"], -0.55, 0.19, "center")):
        a2.hlines(diff[ys].mean(), min(ys) - 0.42, max(ys) + 0.42, color=col, lw=3.2,
                  zorder=4)
        xa = (min(ys) + dx if ha == "right" else
              (np.mean(ys) if ha == "center" else max(ys) + dx))
        a2.text(xa, diff[ys].mean() + dy, lab, ha=ha, va="center", fontsize=9,
                color=col, fontweight="bold")
    a2.axvspan(2019.5, 2021.5, color=MUTED, alpha=0.17, zorder=0)
    a2.annotate("COVID\nsittings\nexcluded", (2020.5, -0.62), ha="center",
                fontsize=8.2, color=INK2)
    a2.annotate("shift $%+.2f$ — Welch $p=%.2f$, exact $p=%.2f$\n"
                "smallest shift detectable here: %.2f"
                % (shift, p, hits / tot, mde),
                (2012.4, -0.42), fontsize=8.8, color=INK, ha="center",
                bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=MUTED, lw=0.8))
    a2.set_ylabel("Cataluña $-$ field\n(marks)")
    a2.set_xlabel("")
    a2.set_title("b. …and what it did to the mean, against the fifteen-community field",
                 loc="left")
    a2.set_xlim(2008.8, 2026.4)
    a2.set_xticks(range(2010, 2027, 2))

    fig.suptitle("A conversion that can be dated, and a cost that cannot be measured")
    _save(fig, "fig37_catalunya_event", ROOT / "plots")


if __name__ == "__main__":
    main()
