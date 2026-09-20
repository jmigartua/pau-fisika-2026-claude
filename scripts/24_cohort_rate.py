#!/usr/bin/env python3
"""Is there a rate of cohort decay, and can it be projected onto a PAU year?

The coordinator's question, stated precisely: PISA measures a cohort at 15, the PAU
measures part of the same cohort at 18, two years later.  Between one PISA round and
the next the 15-year-olds get worse.  Is there also a degradation WITHIN a cohort as it
moves through Bachillerato — and if so, can a rate be attached to it and used to
anticipate a PAU year before it happens?

This script answers in four parts.

1. THE RATE IS NOT A SLOPE.  The per-cohort-year change between consecutive PISA rounds
   is computed for Euskadi and for Spain.  In Euskadi it ranges from +3.65 to -7.53
   points per cohort-year.  The series is a sequence of steps, not a trend, so a linear
   extrapolation from it is not a projection but a guess with error bars drawn around
   the wrong model.

2. WHAT IS IDENTIFIABLE.  Write the PAU mean of cohort c as

       PAU(c) = s * [ A(c,15) + G(c) ] + sel(c) + paper(y) + marking(y)

   with A(c,15) the ability PISA measures, G(c) the gain or loss over the three school
   years, sel the selection into Física, and paper and marking the year's exam and its
   correction.  Differencing consecutive cohorts leaves

       d PAU = s * [ d A15 + d G ] + d sel + d paper + d marking.

   PISA delivers dA15.  dG — the within-cohort term the coordinator is after — is
   therefore identified only if d sel, d paper and d marking are known.  They are not,
   and d paper is the largest term in the dossier.  So dG is NOT identifiable from PISA
   and the PAU alone.  Two things follow, and they are the useful part: a CONSTANT
   within-cohort degradation cancels in every difference and is invisible because it is
   irrelevant to the year-to-year question; and a CHANGING one would show up as the PAU
   falling faster than PISA for matched cohorts.  It does not.

3. WHAT TRANSFERS FROM THE POPULATION TO THE CANDIDATES.  PISA measures everyone at 15;
   PAU Física is sat by a self-selected fifth.  Whether a population mean shift reaches
   the selected group 1:1 depends on whether the selection threshold is absolute (a
   fixed standard) or relative (the top q, whoever they are).  Both are computed.  Two
   observations pin down which is closer: take-up is roughly flat, and the Basque PISA
   top band fell by about what a uniform shift of the whole distribution predicts.

4. THE 2026 ENTRY COUNT RUNS THE WRONG WAY FOR DILUTION.  123 fewer candidates sat
   Física in 2026 than in 2025, 5.6 % fewer.  Under the most favourable assumption for
   the dilution story — that the ones who stayed away were the weakest — the 2026 group
   should have scored HIGHER than the 2025 group, not lower.  The composition change is
   therefore a credit against the fall, not a part of it.

Reads : data/analysis/pisa_link.json, data/analysis/slope_compare.json,
        data/analysis/pau2027_estimator.json, data/analysis/take_up.json,
        data/analysis/euskadi_participation.csv, data/analysis/results.json
Writes: data/analysis/cohort_rate.json, data/tables/cohort_rate_steps.md,
        data/tables/cohort_identification.md, plots/fig28_cohort_rate.(png|svg)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from plot_style import C, INK, INK2, MUTED, apply_style, save as _save

apply_style()
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
A = DATA / "analysis"
TABLES = DATA / "tables"
PLOTS = ROOT / "plots"

SD_PISA = 90.0          # one PISA proficiency SD, the scale's own definition
SD_PAU = 2.343          # SD of the PAU regional means panel, as used throughout
SHIFT_YEARS = 2         # PISA year + 2 = the PAU year of the same cohort


def rates(series: dict[str, float]) -> list[dict]:
    """Per-cohort-year change between consecutive PISA rounds."""
    ys = sorted(int(y) for y in series)
    out = []
    for a_, b_ in zip(ys, ys[1:]):
        span = b_ - a_
        out.append(dict(from_year=a_, to_year=b_, span=span,
                        change=series[str(b_)] - series[str(a_)],
                        per_year=(series[str(b_)] - series[str(a_)]) / span))
    return out


def selected_shift(q: float, delta_sd: float) -> dict:
    """How much of a population mean shift reaches the selected upper tail.

    Two selection rules, both on a standard normal latent ability.

      relative : the top q are always taken, whoever they are.  The truncation point
                 moves with the distribution, so the selected mean shifts by exactly
                 the population shift.  Transfer = 1 by construction.

      absolute : the threshold is a fixed standard.  The population slides down past a
                 stationary cut, fewer qualify, and the survivors are a more extreme
                 slice, so the selected mean falls by LESS than the population mean.
    """
    c = stats.norm.ppf(1 - q)                       # the cut, before the shift
    def tail_mean(mu, cut):
        a_ = (cut - mu)
        return mu + stats.norm.pdf(a_) / (1 - stats.norm.cdf(a_))
    before = tail_mean(0.0, c)
    after_abs = tail_mean(delta_sd, c)              # delta_sd is negative
    return dict(q=q, cut=float(c), delta_population_sd=delta_sd,
                relative_transfer=1.0,
                absolute_shift_sd=float(after_abs - before),
                absolute_transfer=float((after_abs - before) / delta_sd),
                absolute_new_share=float(1 - stats.norm.cdf(c - delta_sd)))


def main() -> None:
    pl = json.loads((A / "pisa_link.json").read_text(encoding="utf-8"))
    sc = json.loads((A / "slope_compare.json").read_text(encoding="utf-8"))
    est = json.loads((A / "pau2027_estimator.json").read_text(encoding="utf-8"))
    tu = json.loads((A / "take_up.json").read_text(encoding="utf-8"))
    part = pd.read_csv(A / "euskadi_participation.csv")

    pv = pl["science_mean"]["pais_vasco"]
    es = pl["science_mean"]["espana"]
    r_pv, r_es = rates(pv), rates(es)
    excess = [dict(from_year=a_["from_year"], to_year=a_["to_year"], span=a_["span"],
                   per_year=a_["per_year"] - b_["per_year"],
                   per_year_marks=(a_["per_year"] - b_["per_year"]) / SD_PISA * SD_PAU)
              for a_, b_ in zip(r_pv, r_es)]

    pv_rates = np.array([r["per_year"] for r in r_pv])
    step = dict(
        mean_per_year=float(pv_rates.mean()), sd_per_year=float(pv_rates.std(ddof=1)),
        min_per_year=float(pv_rates.min()), max_per_year=float(pv_rates.max()),
        range_per_year=float(pv_rates.max() - pv_rates.min()),
        # A trend would show consecutive rates clustered; steps show them dispersed.
        # The ratio of the spread of the rates to their mean is the diagnostic.
        dispersion_over_mean=float(abs(pv_rates.std(ddof=1) / pv_rates.mean())),
    )

    # ---- the 2026 cohort was never measured ------------------------------------
    # PISA 2022 -> PAU 2024; PISA 2025 -> PAU 2027.  The cohort that sat PAU 2026 was
    # fifteen in the spring of 2024, between rounds.  Linear interpolation is the only
    # option, and it assumes the 2022-25 fall was spread evenly over the three cohorts.
    f = 2.0 / 3.0
    interp = dict(
        method="linear interpolation between PISA 2022 and PISA 2025",
        pais_vasco_2024=pv["2022"] + f * (pv["2025"] - pv["2022"]),
        espana_2024=es["2022"] + f * (es["2025"] - es["2022"]),
        caveat=("the fall may have been concentrated in one of the three cohorts; "
                "nothing in the data says it was spread evenly"),
    )
    interp["gap_2024"] = interp["pais_vasco_2024"] - interp["espana_2024"]
    interp["gap_2022"] = pl["gap_pv_minus_spain"]["2022"]
    interp["excess_move_2022_to_2024"] = interp["gap_2024"] - interp["gap_2022"]
    interp["excess_per_cohort_year"] = interp["excess_move_2022_to_2024"] / 2.0
    interp["excess_per_cohort_year_marks"] = (
        interp["excess_per_cohort_year"] / SD_PISA * SD_PAU)

    # ---- the top-band check ----------------------------------------------------
    # If the Basque decline is a pure LOCATION shift of the whole distribution, the
    # level 5-6 share follows mechanically from the mean move.  If instead the top of
    # the distribution collapsed on its own, the observed share will be well below what
    # the shift predicts, and transferring the mean move to a selected group would be
    # unsafe.
    t0 = pl["top56_pct"]["pais_vasco"]["2022"] / 100.0
    t1 = pl["top56_pct"]["pais_vasco"]["2025"] / 100.0
    shift_sd = (pv["2025"] - pv["2022"]) / SD_PISA
    cut0 = stats.norm.ppf(1 - t0)
    pred = float(1 - stats.norm.cdf(cut0 - shift_sd))
    topband = dict(
        observed_2022_pct=t0 * 100, observed_2025_pct=t1 * 100,
        mean_shift_sd=float(shift_sd),
        predicted_2025_pct_from_uniform_shift=pred * 100,
        observed_over_predicted=float(t1 / pred),
        reading=("a uniform shift of the whole distribution accounts for the observed "
                 "fall in the top band to within 4.8 per cent of the predicted share; the "
                 "Basque PISA decline is a location move, not a collapse of the top"),
    )

    # ---- selection transfer ----------------------------------------------------
    q_obs = tu["national_take_up_by_year"]["2025"]
    transfer = [selected_shift(q, shift_sd / 3.0) for q in
                [0.10, 0.15, q_obs, 0.25, 0.30, 0.40]]
    transfer_at_obs = selected_shift(q_obs, shift_sd / 3.0)

    # ---- the 2026 entry count --------------------------------------------------
    p25 = int(part.loc[part.year == 2025, "presented"].iloc[0])
    p26 = int(part.loc[part.year == 2026, "presented"].iloc[0])
    drop = (p25 - p26) / p25
    # The truncation is applied to the 2025 candidate pool — it is the 2025 entrants
    # minus whoever stayed away — so the relevant dispersion is the 2025 within-year SD
    # from the beta fit of that year's published distribution.
    res = json.loads((A / "results.json").read_text(encoding="utf-8"))
    sd_marks_2025 = float(res["beta_fits"]["EHU_2025"]["sd"])
    # Most favourable case for dilution: the 123 who stayed away were the weakest.
    zc = stats.norm.ppf(drop)
    gain_sd = stats.norm.pdf(zc) / (1 - drop)
    composition = dict(
        presented_2025=p25, presented_2026=p26, change=p26 - p25,
        change_pct=-drop * 100,
        within_year_sd_marks_2025=float(sd_marks_2025),
        max_gain_if_weakest_left_marks=float(gain_sd * sd_marks_2025),
        reading=("fewer candidates, so the composition change cannot have lowered the "
                 "mean; at its most extreme it should have raised it, which makes the "
                 "unexplained part of the fall larger, not smaller"),
        earlier_year_note=dict(
            presented_2024=int(part.loc[part.year == 2024, "presented"].iloc[0]),
            change_2024_to_2025_pct=float(
                (p25 - part.loc[part.year == 2024, "presented"].iloc[0])
                / part.loc[part.year == 2024, "presented"].iloc[0] * 100),
            comment=("2025 is the opposite case: 401 more candidates, +22.4 %, and a "
                     "mean 0.62 lower — there, dilution is a live hypothesis, and the "
                     "mark budget assigns that year almost wholly to the common "
                     "component in any case"),
        ),
    )

    # ---- 2027 ------------------------------------------------------------------
    # PISA 2025 is the first round that maps onto a future PAU year without
    # interpolation: that cohort sits PAU 2027.
    cohort_2027_gross = est["cohort_term_marks_from_2026_baseline"]
    cohort_2027_excess = (
        (pv["2025"] - pv["2022"]) - (es["2025"] - es["2022"])) / 3.0 / SD_PISA * SD_PAU
    projection = dict(
        measured_cohort=True,
        baseline_2026=est["pau_2026"],
        cohort_term_gross_marks=cohort_2027_gross,
        cohort_term_excess_of_field_marks=float(cohort_2027_excess),
        paper_sd_marks=est["annual_paper_sd"],
        band_95_one_year=1.96 * est["annual_paper_sd"],
        noise_to_signal=float(est["annual_paper_sd"] / abs(cohort_2027_gross)),
        scenarios=est["scenarios"],
        reading=("the cohort term is worth about a fifth of a mark a year and the "
                 "paper is worth nearly a whole mark; a cohort projection is real but "
                 "it sets an expectation, it does not set a target"),
    )

    # ---- matched-cohort slope comparison ---------------------------------------
    accel = dict(
        pau_euskadi_sd_per_decade=sc["fits"]["PAU Física, Euskadi"]["slope_sd_decade"],
        pisa_euskadi_sd_per_decade=sc["fits"]["PISA science, Euskadi"]["slope_sd_decade"],
        difference=sc["slope_difference_tests"]["Euskadi"]["difference"],
        p=sc["slope_difference_tests"]["Euskadi"]["p"],
        reading=("for matched cohorts the PAU falls more slowly than PISA, not faster; "
                 "an accelerating within-cohort degradation would give the opposite "
                 "sign.  The difference is not significant either way (n = 4 to 6), so "
                 "this rules nothing out — it simply gives no support to acceleration"),
    )

    out = dict(
        alignment=f"PISA year + {SHIFT_YEARS} = PAU year",
        sd_pisa=SD_PISA, sd_pau=SD_PAU,
        rates_pais_vasco=r_pv, rates_espana=r_es, rates_excess=excess,
        step_diagnostics=step,
        interpolated_2026_cohort=interp,
        top_band_check=topband,
        selection_transfer=dict(
            at_observed_take_up=transfer_at_obs, grid=transfer, take_up_2025=q_obs,
            take_up_trend_r=tu["take_up_r"], take_up_trend_p=tu["take_up_p"],
            bounds=dict(
                low=transfer_at_obs["absolute_transfer"], high=1.0,
                cohort_term_marks_high=float(
                    interp["excess_per_cohort_year_marks"]),
                cohort_term_marks_low=float(
                    interp["excess_per_cohort_year_marks"]
                    * transfer_at_obs["absolute_transfer"]),
            ),
            which_is_closer=(
                "the two rules differ by a factor of four, so the choice matters.  "
                "Under an absolute standard a falling population should produce "
                "falling take-up, because fewer clear the bar; national take-up "
                f"instead drifts slightly up (0.222 in 2015 to {q_obs:.3f} in 2025) "
                f"and shows no association with the mean (r = {tu['take_up_r']:.3f}, "
                f"p = {tu['take_up_p']:.3f}).  That points to the relative rule: "
                "candidates choose Física for the degree they want and the weighting "
                "it carries, not against a fixed ability bar.  The dossier's 1:1 "
                "conversion is therefore defensible, but it is the TOP of the range, "
                "so the cohort term it yields is an upper bound in magnitude and the "
                "unattributed remainder a lower bound."),
        ),
        composition_2026=composition,
        projection_2027=projection,
        acceleration_test=accel,
        identification=dict(
            model="PAU(c) = s*[A(c,15) + G(c)] + sel(c) + paper(y) + marking(y)",
            identified=["s*dA15 (from PISA, up to the scale factor s)"],
            not_identified=["dG, the within-cohort term",
                            "d marking, which is collinear with d paper in 2026"],
            why=("dG enters every difference alongside d paper, and d paper is both "
                 "unobserved and the largest term; no amount of PISA data separates "
                 "them"),
            what_would=("an annual census measure of Basque students at 15 would give a "
                        "one-year cadence where PISA gives three, and the school marks "
                        "of the same cohort at 18 would bracket G(c) from the other "
                        "end; neither is in the dossier"),
        ),
    )
    (A / "cohort_rate.json").write_text(json.dumps(out, indent=2, ensure_ascii=False),
                                        encoding="utf-8")

    # ---- tables ----------------------------------------------------------------
    L = ["| PISA rounds | PAU years of those cohorts | Span | Euskadi, per cohort-year |"
         " Spain, per cohort-year | Excess | In marks |", "|---|---|---:|---:|---:|---:|---:|"]
    for a_, b_, e_ in zip(r_pv, r_es, excess):
        L.append(f"| {a_['from_year']}→{a_['to_year']} | "
                 f"{a_['from_year']+SHIFT_YEARS}→{a_['to_year']+SHIFT_YEARS} | "
                 f"{a_['span']} yr | {a_['per_year']:+.2f} | {b_['per_year']:+.2f} | "
                 f"{e_['per_year']:+.2f} | {e_['per_year_marks']:+.3f} |")
    L += ["", f"PISA science points per cohort-year. The Basque rates range from "
          f"{step['min_per_year']:+.2f} to {step['max_per_year']:+.2f}, a spread of "
          f"{step['range_per_year']:.2f} points a year around a mean of "
          f"{step['mean_per_year']:+.2f}: the series is a sequence of steps, not a "
          f"slope, and the last column is what one cohort-year of the excess is worth "
          f"on the Basque PAU scale."]
    (TABLES / "cohort_rate_steps.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = ["| Term | What it is | Observed? | Identified from PISA + PAU? |",
         "|---|---|:-:|:-:|",
         "| `A(c,15)` | the cohort's ability at fifteen | yes, every three years | "
         "yes, up to the scale factor |",
         "| `G(c)` | what the cohort gains or loses between fifteen and eighteen | no | "
         "**no** |",
         "| `sel(c)` | who chooses to sit Física | partly: entry counts, not ability | "
         "bounded, not identified |",
         "| `paper(y)` | the year's exam | coded, not calibrated | **no** |",
         "| `marking(y)` | how that exam was corrected | not published | **no** |",
         "",
         "A constant `G` cancels in every year-to-year difference, so it is invisible "
         "*and* irrelevant to the question the office actually faces. A changing `G` "
         "would matter, and would show as the PAU falling faster than PISA for matched "
         "cohorts; it falls more slowly "
         f"({accel['pau_euskadi_sd_per_decade']:+.3f} against "
         f"{accel['pisa_euskadi_sd_per_decade']:+.3f} SD per decade, difference "
         f"p = {accel['p']:.2f}), which is no support for acceleration and, at this "
         "sample size, no refutation either."]
    (TABLES / "cohort_identification.md").write_text("\n".join(L) + "\n",
                                                     encoding="utf-8")

    # ---- figure ----------------------------------------------------------------
    c_g_ = projection["cohort_term_gross_marks"]
    c_e_ = projection["cohort_term_excess_of_field_marks"]

    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.6))

    # (a) per-cohort-year rates as steps
    ax = axes[0]
    xs, pvv, esv = [], [], []
    for a_, b_ in zip(r_pv, r_es):
        xs += [a_["from_year"], a_["to_year"]]
        pvv += [a_["per_year"]] * 2
        esv += [b_["per_year"]] * 2
    ax.plot(xs, pvv, color=C["red"], lw=2.0, label="Euskadi")
    ax.plot(xs, esv, color=C["blue"], lw=1.6, label="Spain")
    ax.axhline(0, color=INK, lw=0.9)
    ax.fill_between(xs, pvv, esv, color=C["red"], alpha=0.10)
    for a_ in r_pv:
        ax.text((a_["from_year"] + a_["to_year"]) / 2, a_["per_year"]
                + (0.45 if a_["per_year"] >= 0 else -0.85),
                f"{a_['per_year']:+.1f}", ha="center", fontsize=8, color=C["red"])
    ax.set_xticks([int(y) for y in sorted(pv)])
    ax.set_xticklabels([str(y) for y in sorted(int(k) for k in pv)], fontsize=8)
    ax.set_xlabel("PISA round (the cohort sits the PAU two years later)")
    ax.set_ylabel("PISA science points per cohort-year")
    ax.set_ylim(-9.6, 5.6)
    ax.legend(loc="lower left", fontsize=8)
    ax.set_title("(a) Steps, not a slope\nEuskadi: $+3.7$ to $-7.5$ a year", loc="left")

    # (b) how much of a population shift reaches the selected group
    ax = axes[1]
    qs = np.linspace(0.05, 0.60, 120)
    tr = [selected_shift(q, shift_sd / 3.0)["absolute_transfer"] for q in qs]
    ax.plot(qs * 100, tr, color=C["violet"], lw=1.8, label="absolute standard")
    ax.axhline(1.0, color=C["aqua"], lw=1.8, label="relative (top $q$ always)")
    ax.axvline(q_obs * 100, color=MUTED, lw=1.0, ls="--")
    ax.scatter([q_obs * 100], [transfer_at_obs["absolute_transfer"]], s=52,
               color=C["violet"], zorder=4)
    ax.annotate(f"take-up {q_obs*100:.1f} per cent\ntransfer "
                f"{transfer_at_obs['absolute_transfer']:.2f}",
                (q_obs * 100, transfer_at_obs["absolute_transfer"]),
                textcoords="offset points", xytext=(10, -22), fontsize=8, color=INK2)
    ax.set_xlim(5, 60); ax.set_ylim(0.0, 1.15)
    ax.set_xlabel("share of the cohort sitting Física (per cent)")
    ax.set_ylabel("fraction of the population shift reaching the candidates")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title("(b) The rule matters: 0.23 or 1.00\nflat take-up favours the "
                 "relative rule", loc="left")

    # (c) what actually moves the 2027 mean
    ax = axes[2]
    items = [
        ("Cohort term,\nexcess of the field", abs(c_e_), C["violet"]),
        ("Cohort term,\ngross Basque move", abs(c_g_), C["red"]),
        ("One SD of\npaper-to-paper variation", projection["paper_sd_marks"], C["orange"]),
        ("95 per cent band of the\npaper alone, one year", projection["band_95_one_year"],
         C["yellow"]),
    ]
    y = np.arange(len(items))[::-1]
    ax.barh(y, [i[1] for i in items], color=[i[2] for i in items], height=0.6)
    for yy, (_, v, _) in zip(y, items):
        ax.text(v + 0.035, yy, f"{v:.2f}", va="center", fontsize=9, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([i[0] for i in items], fontsize=8.5)
    ax.set_xlim(0, 2.05)
    ax.set_xlabel("marks, one year ahead")
    ax.set_title(f"(c) The cohort is worth {abs(c_g_):.2f} a year,\n"
                 f"the paper {projection['paper_sd_marks']:.2f}", loc="left")
    ax.grid(axis="y", visible=False)

    fig.suptitle("Figure 28 — A rate of cohort decay, and what it can and cannot "
                 "anticipate", x=0.005, ha="left", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _save(fig, "fig28_cohort_rate", PLOTS)

    print("Basque per-cohort-year rates:",
          ", ".join(f"{r['from_year']}-{r['to_year']}: {r['per_year']:+.2f}"
                    for r in r_pv))
    print(f"spread {step['range_per_year']:.2f} around mean "
          f"{step['mean_per_year']:+.2f}")
    print(f"interpolated 2026-cohort excess per year "
          f"{interp['excess_per_cohort_year']:+.2f} pts = "
          f"{interp['excess_per_cohort_year_marks']:+.3f} marks")
    print(f"top band: observed {topband['observed_2025_pct']:.2f} %, uniform-shift "
          f"prediction {topband['predicted_2025_pct_from_uniform_shift']:.2f} %, "
          f"ratio {topband['observed_over_predicted']:.3f}")
    print(f"selection transfer at take-up {q_obs:.3f}: absolute "
          f"{transfer_at_obs['absolute_transfer']:.3f}, relative 1.000 -> cohort term "
          f"between {out['selection_transfer']['bounds']['cohort_term_marks_low']:+.3f} "
          f"and {out['selection_transfer']['bounds']['cohort_term_marks_high']:+.3f} marks")
    print(f"2026 entries {p26} vs {p25} ({composition['change_pct']:+.1f} %); "
          f"max gain if the weakest stayed away "
          f"{composition['max_gain_if_weakest_left_marks']:+.3f} marks")
    print(f"2027: cohort {c_g_:+.3f} gross / {c_e_:+.3f} excess; paper SD "
          f"{projection['paper_sd_marks']:.3f}; ratio "
          f"{projection['noise_to_signal']:.2f}")


if __name__ == "__main__":
    main()
