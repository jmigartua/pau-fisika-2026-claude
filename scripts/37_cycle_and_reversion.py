"""Is the wave in figure 37b a cycle? And what does the panel's memory say about 2027?

The coordinator looked at Cataluña's position against the field, 2015–2025, and saw a
cosine. The eye is right that there is a smooth rise and fall; the question is whether
eleven annual points can tell a cycle from a process with memory and no cycle at all.

Two things are computed, and the second matters more than the first.

1. A FALSE-ALARM PROBABILITY, against the right null. For a fixed period the sinusoid is
   linear in its coefficients, so the best fit over a period grid is exact and fast. The
   null is not white noise — using white noise here is the classic way to manufacture a
   cycle — but the memory the panel actually has, estimated from the panel itself.

   Choosing that null needs care, and the first attempt got it wrong. Pooling all
   communities without community intercepts gives an AR(1) coefficient of 0.61, but most
   of that is *between* communities: some sit above the field every year. Within a
   community, around its own level, the coefficient is 0.19 (0.30 after correcting the
   downward Nickell bias of a short dynamic panel). Since the sinusoid fit includes a
   constant, a community's own level is absorbed and cannot affect the fit, so the null
   that governs the *shape* is the within-community process, not the pooled one.

2. A LOOK-ELSEWHERE TEST. One series was examined because it looked wavy. The same fit
   is therefore run on all fifteen communities. If the wave were real and driven from
   outside, the periods would agree; and the series that prompted the question should
   stand out.

3. MEAN REVERSION, which is the part with consequences. A deviation from a community's
   own norm retains only a fifth to a third of itself the following year. Applied to
   Euskadi's 2026 deviation of −2.16 from its own norm, the panel's history expects
   most of it back in 2027 with no intervention at all — a trap for anyone who changes
   the paper and then reads the recovery as evidence that the change worked. It also
   yields the one pre-registered prediction in this dossier that a single future
   sitting can settle, at about 3.7 sigma.

A NOTE ON WHAT A DIFFERENCE CAN CONTAIN. The plotted quantity is a community minus the
field. Anything acting on every community at once — a national reform, a pandemic, a
cohort effect — is removed by that subtraction *by construction*. So whatever the wave
is, it cannot be a common external driver: it would have to be something specifically
Catalan with a nine-year clock.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from plot_style import C, INK, INK2, MUTED, apply_style, save as _save

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "analysis"
apply_style()
RNG = np.random.default_rng(20260922)
PGRID = np.linspace(2.2, 40, 600)
T = np.arange(11.0)
DES = [np.column_stack([np.ones(11), np.cos(2 * np.pi * T / P), np.sin(2 * np.pi * T / P)])
       for P in PGRID]
PINV = [np.linalg.pinv(X) for X in DES]


def best_sinusoid(y):
    """Largest R^2 over the period grid. Exact: linear in the coefficients."""
    tss = ((y - y.mean()) ** 2).sum()
    br, bp = -1.0, np.nan
    for X, Xp, P in zip(DES, PINV, PGRID):
        r = y - X @ (Xp @ y)
        ss = 1 - (r ** 2).sum() / tss
        if ss > br:
            br, bp = ss, P
    return br, bp


def ar1(dev, fixed_effects):
    xs, ys = [], []
    for c in dev.columns:
        s = dev[c].values
        if fixed_effects:
            s = s - s.mean()
        xs += list(s[:-1])
        ys += list(s[1:])
    lr = stats.linregress(xs, ys)
    resid = np.array(ys) - lr.slope * np.array(xs)
    return lr.slope, lr.stderr, resid.std(ddof=1), len(xs)


def simulate(phi, sigma, n, target_r2):
    hits, pers = 0, []
    for _ in range(n):
        z = np.empty(11)
        z[0] = RNG.normal(0, sigma / np.sqrt(1 - phi ** 2) if phi else sigma)
        for i in range(1, 11):
            z[i] = phi * z[i - 1] + RNG.normal(0, sigma)
        s, p = best_sinusoid(z)
        pers.append(p)
        hits += s >= target_r2
    return hits / n, float(np.median(pers))


def main() -> None:
    d = pd.read_csv(OUT / "regional_long_series.csv")
    m = d[d.source == "ministry"]
    w = (m.pivot_table(index="year", columns="ccaa", values="mean")
         .drop(columns=["Total"]).loc[2015:2025])
    w = w[w.columns[w.notna().sum() == 11]]
    field = w.mean(axis=1)
    dev = w.sub(field, axis=0)
    diff = (w["Cataluña"] - w.drop(columns=["Cataluña"]).mean(axis=1)).values

    r2, per = best_sinusoid(diff)
    phi_p, se_p, _, n_p = ar1(dev, False)
    phi_w, se_w, sig_w, n_w = ar1(dev, True)
    nickell = -(1 + phi_w) / (dev.shape[0] - 1)
    phi_bc = phi_w - nickell

    N = 3000
    fap = {}
    for lbl, ph in (("white noise", 0.0),
                    ("within-community, phi=%.2f" % phi_w, phi_w),
                    ("bias-corrected, phi=%.2f" % phi_bc, phi_bc),
                    ("pooled (wrong null), phi=%.2f" % phi_p, phi_p)):
        p, med = simulate(ph, sig_w, N, r2)
        fap[lbl] = {"false_alarm_p": round(p, 3), "median_period_from_noise": round(med, 1)}

    # ---- look-elsewhere: the same fit on every community
    look = {}
    for c in w.columns:
        s = (w[c] - w.drop(columns=[c]).mean(axis=1)).values
        rr, pp = best_sinusoid(s)
        look[c] = {"R2": round(rr, 3), "period": round(pp, 1)}
    pers_all = np.array([v["period"] for v in look.values()])
    r2_all = np.array([v["R2"] for v in look.values()])

    # ---- the 2027 pre-registration, in positions against the 2026 publishers
    pub = [c for c in d[(d.year == 2026) & (d.ccaa != "País Vasco")].ccaa if c in w.columns]
    pos_hist = w["País Vasco"] - w[pub].mean(axis=1)
    norm = float(pos_hist.loc[2015:2024].mean())
    y26 = d[d.year == 2026].set_index("ccaa")["mean"]
    pos26 = float(y26["País Vasco"] - y26[pub].mean())
    x26 = pos26 - norm
    rev = {"euskadi_norm_2015_2024": round(norm, 3), "euskadi_position_2025": round(float(pos_hist.loc[2025]), 3),
           "euskadi_position_2026": round(pos26, 3), "deviation_from_own_norm_2026": round(x26, 3),
           "field_2026_publishers": sorted(pub), "innovation_sd": round(sig_w, 3)}
    for lbl, ph in (("shock_phi_%.2f" % phi_w, phi_w), ("shock_phi_%.2f_bias_corrected" % phi_bc, phi_bc)):
        rev[lbl] = {"expected_2027_deviation": round(ph * x26, 2),
                    "ci95": [round(ph * x26 - 1.96 * sig_w, 2), round(ph * x26 + 1.96 * sig_w, 2)],
                    "implied_recovery": round(ph * x26 - x26, 2),
                    "half_life_years": round(float(np.log(0.5) / np.log(ph)), 2)}
    rev["level_change"] = {"expected_2027_deviation": round(x26, 2),
                           "ci95": [round(x26 - 1.96 * sig_w, 2), round(x26 + 1.96 * sig_w, 2)],
                           "implied_recovery": 0.0}
    rev["separation_sigma"] = round(abs(x26 - phi_w * x26) / sig_w, 2)

    res = {
        "catalunya_best_sinusoid": {"R2": round(r2, 3), "period_years": round(per, 1),
                                    "n_points": 11},
        "rayleigh_note": ("with an 11-year record the frequency resolution is 1/11 yr^-1, "
                          "so a period near 9 years cannot be distinguished from a trend "
                          "or from no cycle at all; three cycles would need ~27 years"),
        "ar1_pooled_no_fixed_effects": {"phi": round(phi_p, 3), "se": round(se_p, 3), "n": n_p,
                                        "note": "mostly between-community level differences"},
        "ar1_within_community": {"phi": round(phi_w, 3), "se": round(se_w, 3), "n": n_w,
                                 "innovation_sd": round(sig_w, 3),
                                 "nickell_bias": round(nickell, 3),
                                 "bias_corrected_phi": round(phi_bc, 3)},
        "false_alarm": fap,
        "look_elsewhere": look,
        "look_elsewhere_summary": {
            "n_communities": int(len(look)),
            "median_R2": round(float(np.median(r2_all)), 3),
            "n_above_0.80": int((r2_all >= 0.80).sum()),
            "catalunya_rank": int(1 + (r2_all > look["Cataluña"]["R2"]).sum()),
            "period_median": round(float(np.median(pers_all)), 1),
            "period_sd": round(float(pers_all.std(ddof=1)), 1),
            "verdict": ("periods do not agree, so no common driver; and the series that "
                        "prompted the question is not even the best fit"),
        },
        "pre_registered_2027": rev,
    }
    json.dump(res, open(OUT / "cycle_and_reversion.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))
    figure(look, diff, r2, per, pos_hist, pos26, norm, x26, phi_w, phi_bc, sig_w, fap)


def figure(look, diff, r2, per, pos_hist, pos26, norm, x26, phi, phibc, sig, fap):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.7),
                                 gridspec_kw=dict(wspace=0.30, width_ratios=[1.05, 1]))

    order = sorted(look, key=lambda c: look[c]["R2"])
    names = ["Euskadi" if c == "País Vasco" else c.split(" (")[0] for c in order]
    vals = [look[c]["R2"] for c in order]
    cols = [C["red"] if c == "País Vasco" else
            (C["violet"] if c == "Cataluña" else MUTED) for c in order]
    a1.barh(range(len(order)), vals, color=cols, height=0.72, zorder=2)
    for i, c in enumerate(order):
        a1.text(vals[i] + 0.012, i, "%.0f y" % look[c]["period"], va="center",
                fontsize=7.6, color=INK2)
    a1.set_yticks(range(len(order)))
    a1.set_yticklabels(names, fontsize=8.2)
    a1.set_xlim(0, 1.06)
    a1.set_xlabel("best sinusoid $R^2$ on 11 points")
    a1.set_title("a. Fit a cosine to every community, and\n     Aragón fits better than Cataluña", loc="left")
    a1.axvline(r2, color=C["violet"], lw=1.1, ls="--", zorder=3)
    a1.text(0.975, 0.025, "the periods run 2.5 to 40 years.\nA common external driver would\nimpose a common period.\nThese do not agree.",
            transform=a1.transAxes, fontsize=7.9, color=INK2, va="bottom", ha="right",
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=MUTED, lw=0.7))

    yrs = list(pos_hist.index) + [2026]
    vals = list(pos_hist.values) + [pos26]
    a2.axhline(norm, color=MUTED, lw=1.0, ls="--", zorder=1)
    a2.text(2014.8, 0.70, "Euskadi's own norm %+.2f" % norm, fontsize=8.2,
            color=INK2, ha="left")
    a2.plot(yrs, vals, "o-", color=INK, lw=1.6, ms=4.6, zorder=3)
    for ph, col, lab in ((phi, C["blue"], "a shock: reverts"),
                         (1.0, C["red"], "a level change: persists")):
        e = norm + ph * x26
        a2.errorbar([2027], [e], yerr=[1.96 * sig], fmt="s", ms=7, color=col,
                    capsize=5, lw=1.8, zorder=4)
        a2.annotate(lab, (2027, e), textcoords="offset points",
                    xytext=(-11, 36 if ph < 1 else -32), ha="right", fontsize=8.6,
                    color=col, fontweight="bold")
    a2.axvspan(2026.5, 2027.6, color=MUTED, alpha=0.14, zorder=0)
    a2.set_xlim(2014.4, 2027.9)
    a2.set_xticks(range(2015, 2028, 3))
    a2.set_ylabel("Euskadi $-$ field (marks)")
    a2.set_title("b. …and the one prediction a single\n     sitting can settle", loc="left")
    a2.text(0.03, 0.06, "separation %.1f$\\sigma$" % (abs(x26 - phi * x26) / sig),
            transform=a2.transAxes, fontsize=8.6, color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=MUTED, lw=0.7))

    fig.suptitle("A wave that eleven points cannot establish, and a reversion that 2027 will test")
    _save(fig, "fig38_cycle_and_reversion", ROOT / "plots")


if __name__ == "__main__":
    main()
