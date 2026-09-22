"""Shared figure style for the whole study (ThesisFigures rule E1).

Every figure in the website is produced by a script in `scripts/` that imports
this module; no script defines its own rcParams or colours. Rule IDs below
refer to the ThesisFigures rulebook.

All figure text is typeset by LaTeX (T1). That is the one behavioural change
from the pre-LaTeX pipeline — the underlying computation of every figure is
untouched.

Requires a working LaTeX installation with `dvipng` on PATH. Verify with:

    python3 -c "import matplotlib; matplotlib.use('Agg'); \
        from matplotlib import rcParams; rcParams['text.usetex']=True; \
        import matplotlib.pyplot as plt; f,a=plt.subplots(); a.set_title(r'$x$'); \
        f.savefig('/tmp/_t.png'); print('usetex ok')"
"""
from __future__ import annotations

import re
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import rcParams  # noqa: E402

# --------------------------------------------------------------------------
# T2 — one knob for text scale.
# These figures are displayed on the web, not reduced for print: an 8.4 in
# canvas is served into a 720 px body column, a reduction of roughly 0.9x. So
# BASE sits near the on-page body size rather than being inflated the way a
# print figure included at 0.65\linewidth would need.
# --------------------------------------------------------------------------
BASE = 10.0

# --------------------------------------------------------------------------
# C1 — central colour registry. One meaning, one colour, across all 15 figures.
# Values carried over unchanged from the pre-LaTeX pipeline so the figures keep
# the palette the chapters already describe in prose.
# --------------------------------------------------------------------------
C = dict(
    blue="#2a78d6",
    orange="#eb6834",
    aqua="#1baf7a",
    yellow="#eda100",
    magenta="#e87ba4",
    green="#008300",
    violet="#4a3aa7",
    red="#e34948",
)

INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8983"
GRID = "#e6e5e1"
SURF = "#fcfcfb"

# --------------------------------------------------------------------------
# T3/T4 — LaTeX escaping.
#
# The data behind these figures is Spanish and Basque: region and subject names
# carry accents and enyes, and a great many labels quote percentages. Under
# usetex an unescaped "%" opens a LaTeX comment and silently swallows the rest
# of the label — "Euskadi 39.8 % pass" renders as "Euskadi 39.8". That failure
# is invisible in the output, so escaping is installed as a guard over
# matplotlib's text layer rather than left to each call site (see
# install_latex_text_guard).
#
# Accented characters need no escaping: the preamble loads utf8 inputenc with
# T1 fontenc and Latin Modern, which typesets them directly.
# --------------------------------------------------------------------------
_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

# Unicode mapped to LaTeX. The list is not speculative: it is every non-ASCII
# character that occurs in the plotting scripts or in the analysis CSVs whose
# values reach a label, enumerated with
#
#     python3 -c "...scan scripts/*.py and data/**/*.csv for ord(ch) > 127..."
#
# Accented Latin-1 (á é í ó ú ü à ò ñ ª º ¿ ·) is deliberately absent: utf8
# inputenc with T1 fontenc typesets those directly, and mapping them would
# only risk mangling the region names. Greek and mathematical symbols must be
# mapped — LaTeX rejects them outright in text mode ("Unicode character Δ not
# set up for use with LaTeX"), which aborts the whole figure.
_UNICODE = {
    # mathematical operators and relations
    "→": r"$\rightarrow$",
    "←": r"$\leftarrow$",
    "≤": r"$\leq$",
    "≥": r"$\geq$",
    "±": r"$\pm$",
    "×": r"$\times$",
    "≈": r"$\approx$",
    "−": r"$-$",       # U+2212, already a true minus
    "°": r"$^\circ$",
    "µ": r"$\mu$",     # U+00B5 micro sign
    # punctuation
    "–": "--",          # en dash
    "—": "---",         # em dash
    "…": r"\ldots{}",
    "’": "'",
    "‘": "'",
    "“": "``",
    "”": "''",
    # Greek: lower case
    "α": r"$\alpha$", "β": r"$\beta$", "γ": r"$\gamma$", "δ": r"$\delta$",
    "ε": r"$\varepsilon$", "ζ": r"$\zeta$", "η": r"$\eta$", "θ": r"$\theta$",
    "ι": r"$\iota$", "κ": r"$\kappa$", "λ": r"$\lambda$", "μ": r"$\mu$",
    "ν": r"$\nu$", "ξ": r"$\xi$", "π": r"$\pi$", "ρ": r"$\rho$",
    "σ": r"$\sigma$", "τ": r"$\tau$", "υ": r"$\upsilon$", "φ": r"$\varphi$",
    "χ": r"$\chi$", "ψ": r"$\psi$", "ω": r"$\omega$",
    # Greek: upper case
    "Γ": r"$\Gamma$", "Δ": r"$\Delta$", "Θ": r"$\Theta$", "Λ": r"$\Lambda$",
    "Ξ": r"$\Xi$", "Π": r"$\Pi$", "Σ": r"$\Sigma$", "Φ": r"$\Phi$",
    "Ψ": r"$\Psi$", "Ω": r"$\Omega$",
}

_MATH_SEGMENT = re.compile(r"(?<!\\)(\$.*?(?<!\\)\$)", re.DOTALL)

# T4 — a signed number written as plain ASCII ("-0.82", "+1.13") renders in
# text mode with a hyphen, which is shorter and sits lower than a real minus,
# so a column of signed labels looks ragged. Promote the sign to math mode, but
# only when it actually is a sign: the lookbehind keeps the hyphens inside
# "Castilla-La Mancha", "year-to-year" and "2010-19" as hyphens.
# The excluded "-" in the lookbehind protects the "--" that an en dash becomes:
# without it "2015–2025" would come out as "2015-$-$2025".
_SIGNED_NUMBER = re.compile(r"(?<![\w.\-])([+-])(?=[.,]?\d)")
_SIGN_MATH = {"-": r"$-$", "+": r"$+$"}


class _Raw(str):
    """A string that is already valid LaTeX and must not be escaped again.

    Needed because the text guard below escapes everything on its way into a
    Text object, which would turn a deliberate `\\textbf{...}` into a literal
    backslash. Marking the string with this type lets it through untouched.
    """


def latex_safe(text: str) -> str:
    """Escape a label for usetex, leaving any `$...$` math segments intact.

    Splitting on math segments matters: a script that deliberately writes
    r"mean $\\bar{x}$" must keep its braces, while the surrounding prose still
    needs its percent signs and underscores escaped.
    """
    if isinstance(text, _Raw):
        return str(text)
    if not isinstance(text, str) or not text:
        return text
    out = []
    for i, part in enumerate(_MATH_SEGMENT.split(text)):
        if i % 2:                      # odd parts are the math segments
            out.append(part)
            continue
        for ch, rep in _ESCAPES.items():
            part = part.replace(ch, rep)
        for ch, rep in _UNICODE.items():
            part = part.replace(ch, rep)
        part = _SIGNED_NUMBER.sub(lambda m: _SIGN_MATH[m.group(1)], part)
        out.append(part)
    return "".join(out)


def install_latex_text_guard() -> None:
    """Route every string matplotlib turns into figure text through latex_safe.

    Patching `Text.set_text` covers titles, axis labels, tick labels, legend
    entries, annotations and bare `ax.text` calls in one place, so a label added
    later cannot reintroduce the silent-percent bug. Strings already carrying a
    `$...$` segment keep that segment verbatim.
    """
    from matplotlib.axes import Axes
    from matplotlib.text import Text

    if getattr(Text, "_latex_guard_installed", False):
        return
    original = Text.set_text

    def guarded(self, s):
        # Idempotence matters: matplotlib re-sets a Text's own string during
        # draw (title repositioning does this), so escaping unconditionally
        # would turn "\%" into "\textbackslash{}\%" on the way to the file
        # while the figure looked correct right after set_title. Remembering
        # what we last produced for this object makes a second pass a no-op.
        if isinstance(s, _Raw):
            self._latex_escaped = str(s)
        elif isinstance(s, str) and s != getattr(self, "_latex_escaped", None):
            s = latex_safe(s)
            self._latex_escaped = s
        return original(self, s)

    Text.set_text = guarded

    # The pre-LaTeX pipeline set semibold titles through rcParams. matplotlib's
    # fontweight does nothing for usetex text — weight has to come from LaTeX —
    # so titles are wrapped here instead, which keeps every existing
    # `ax.set_title(...)` call site unchanged.
    original_title = Axes.set_title

    def bold_title(self, label, *args, **kwargs):
        if isinstance(label, str) and not isinstance(label, _Raw):
            # Each line must be wrapped on its own: matplotlib splits multi-line
            # text on "\n" and hands each line to LaTeX as a separate document,
            # so a `\textbf{` opened on one line and closed on the next aborts
            # the run with an unmatched brace.
            label = _Raw(
                "\n".join(
                    r"\textbf{" + latex_safe(line) + "}" for line in label.split("\n")
                )
            )
        return original_title(self, label, *args, **kwargs)

    Axes.set_title = bold_title
    Text._latex_guard_installed = True


def apply_style() -> None:
    """T1/T2 — install the LaTeX text stack and the shared rcParams."""
    rcParams.update(
        {
            # T1: real LaTeX for every piece of figure text.
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": ["Latin Modern Roman", "Computer Modern Roman"],
            "text.latex.preamble": (
                r"\usepackage[utf8]{inputenc}"
                r"\usepackage[T1]{fontenc}"
                r"\usepackage{lmodern}"
                r"\usepackage{amsmath}"
                r"\usepackage{textcomp}"
            ),
            # T2: every size derives from BASE.
            "font.size": BASE,
            "axes.labelsize": BASE,
            "axes.titlesize": BASE + 1,
            "xtick.labelsize": BASE - 1.5,
            "ytick.labelsize": BASE - 1.5,
            "legend.fontsize": BASE - 1.5,
            # Appearance carried over unchanged from the pre-LaTeX pipeline.
            "axes.edgecolor": GRID,
            "axes.labelcolor": INK2,
            "xtick.color": INK2,
            "ytick.color": INK2,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlecolor": INK,
            "figure.facecolor": SURF,
            "axes.facecolor": SURF,
            "legend.frameon": False,
            "savefig.facecolor": SURF,
        }
    )
    install_latex_text_guard()


def bf(text: str) -> str:
    """Bold any label under usetex (titles are bolded automatically already)."""
    return _Raw(r"\textbf{" + latex_safe(text) + "}")


def phantom_minus(values, decimals=2):
    """G2 — tick labels whose digits align across signed and unsigned axes.

    Non-negative labels carry an invisible minus so a column of numbers does not
    shift horizontally when one of them turns negative.
    """
    return [
        rf"$-{abs(v):.{decimals}f}$" if v < 0 else rf"$\phantom{{-}}{v:.{decimals}f}$"
        for v in values
    ]


# --------------------------------------------------------------------- language
# R1 · the Spanish briefing and synthesis carried English figures. Rather than
# fork every plotting script, each script runs twice: once as it always has,
# and once with PAU_LANG=es, which (a) makes `T()` return the Spanish string
# and (b) makes `save()` write to <name>_es. The figure code is untouched apart
# from wrapping its display strings in T(), so the two versions cannot drift in
# anything but wording. The glossary lives in scripts/es_strings.py; a string
# with no entry falls through unchanged, which is what we want for numerals,
# community names and file paths.
LANG = os.environ.get("PAU_LANG", "en")

# --------------------------------------------------------------------- paper mode
# The paper needs the same figures at page proportions. Reimplementing them would
# let the two sets drift apart, so the panel code is shared verbatim and only the
# *layout* changes: PAU_PAPER=1 makes `panels3()` return a 2-over-1 arrangement at
# text-column width instead of the dossier's 1x3 strip, and `save()` writes into
# plots/paper/ under a paper-numbered name. Nothing that computes a number is
# touched, so a panel cannot say one thing in the dossier and another in the paper.
PAPER = os.environ.get("PAU_PAPER", "") not in ("", "0")

# A4 with the paper's own margins leaves ~163mm of text; 6.5in is that, near enough.
PAGE_W = 6.5

# Paper figure numbers, keyed by the dossier name the script already passes to save().
PAPER_NAMES = {
    "fig25_decomposition": "fig04_locus",          # panels a+b only
    "fig26_subject_decomposition": "fig05_subjects",
    "fig27_comparability": "fig06_reform_intensity",
    "fig30_penalty_regime": "fig07_marking_regime",
    "fig29_statement_budget": "fig09_statements",
    "fig33_field_sensitivity": "fig10_field_sensitivity",
    "fig36_competency_path": "fig11_competency_path",
    "fig37_catalunya_event": "fig12_catalunya_event",
    "fig38_cycle_and_reversion": "fig13_reversion",
}


def panels3(w, h, height_ratios=(1.0, 0.92), hspace=0.46, wspace=0.34):
    """Three panels: a 1x3 strip for the dossier, 2-over-1 for the page.

    Callers unpack `axes[0], axes[1], axes[2]` exactly as before.
    """
    import matplotlib.pyplot as _plt
    if not PAPER:
        return _plt.subplots(1, 3, figsize=(w, h))
    fig = _plt.figure(figsize=(PAGE_W, PAGE_W * 0.98))
    gs = fig.add_gridspec(2, 2, height_ratios=list(height_ratios),
                          hspace=hspace, wspace=wspace)
    # a dossier panel was w/3 wide; a paper panel is PAGE_W/2
    fig._pau_scale = (PAGE_W / 2.0) / (w / 3.0)
    return fig, [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]),
                 fig.add_subplot(gs[1, :])]

# The figures the Spanish documents actually include. A script run with
# PAU_LANG=es writes only these, so no _es file can exist with English in it.
ES_FIGURES = {
    "fig01_euskadi_series",
    "fig03_regions_2026_vs_2025",
    "fig10_school_vs_pau",
    "fig23_pau2027",
    "fig25_decomposition",
    "fig26_subject_decomposition",
    "fig28_cohort_rate",
    "fig29_statement_budget",
    # paper-mode names, needed in Spanish for the coordination deck
    "fig04_locus",
    "fig08_attribution_budget",
    "fig33_field_sensitivity",
    "fig34_budget_no_catalunya",
    "fig36_competency_path",
    "fig37_catalunya_event",
    "fig38_cycle_and_reversion",
}


def T(s):
    """English display string -> the language this run is producing."""
    if LANG == "en":
        return s
    from es_strings import ES
    return ES.get(s, s)


def save(fig, name, outdir: Path, dpi=200):
    """Emit PNG (raster, for the website) and SVG (vector) under one name.

    E2: the filenames are exactly the ones the chapters include, so the site
    renders unchanged after regeneration. Under PAU_LANG=es the name gains an
    `_es` suffix, unless the caller has already supplied one.
    """
    if PAPER:
        # The panel code sets its type sizes in points for a wide dossier figure.
        # Dropped into a text-column-width page figure those points are unchanged
        # while the panels are narrower, so the labels grow relative to the plot and
        # collide. Every text artist is therefore rescaled by exactly the factor the
        # panel shrank by, which keeps the type-to-data ratio the panel was designed
        # with. The running head is dropped: the paper's caption carries it.
        import matplotlib.text as _mtext
        k = getattr(fig, "_pau_scale", 0.70)
        if fig._suptitle is not None:
            fig._suptitle.set_visible(False)
        for t in fig.findobj(_mtext.Text):
            try:
                t.set_fontsize(t.get_fontsize() * k)
            except Exception:
                pass
        # Axis labels written for a wide panel overrun a narrow one and collide with
        # the neighbour's. They are wrapped rather than shortened, so the paper and
        # the dossier still say the same words.
        import textwrap as _tw
        for ax in fig.get_axes():
            for setter, getter in ((ax.set_xlabel, ax.get_xlabel),
                                   (ax.set_ylabel, ax.get_ylabel)):
                t = getter()
                if len(t) > 44 and "\n" not in t:
                    setter(_tw.fill(t, width=42))
        fig.set_constrained_layout(False)
        name = PAPER_NAMES.get(name, name)
        outdir = outdir.parent / "plots" / "paper" if outdir.name != "plots" else outdir / "paper"
    if LANG == "es":
        base = name[:-3] if name.endswith("_es") else name
        if base not in ES_FIGURES:
            # Not used by any Spanish document: writing an _es copy with English
            # text in it would be worse than not writing one at all.
            plt.close(fig)
            return
        name = base + "_es"
    outdir.mkdir(exist_ok=True)
    fig.savefig(outdir / f"{name}.png", dpi=dpi, bbox_inches="tight")
    fig.savefig(outdir / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)
    print("saved", name)
