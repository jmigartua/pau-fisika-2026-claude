# Deploy the site to GitHub Pages

The rendered site is copied to `docs/` (with a `.nojekyll` marker) so GitHub Pages can serve it from the `main` branch.
This is the Claude-side analysis; the Codex-side companion study lives at
https://github.com/jmigartua/pau-fisika-2026-codex.

The repository already exists and Pages is already configured, so the creation step below is kept only
for rebuilding from scratch:

```bash
cd "/Users/User/Desktop/2026/20260701/20260706_pau_fisika_analysis/claude_analysis_2026-09-18"
gh repo create pau-fisika-2026-claude --public --source=. --remote=origin --push
gh api -X POST repos/jmigartua/pau-fisika-2026-claude/pages -f 'source[branch]=main' -f 'source[path]=/docs'
```

The site is at https://jmigartua.github.io/pau-fisika-2026-claude/.

## After any re-render

```bash
quarto render                 # the 13 website pages -> _site/
quarto render onepage.qmd     # the standalone single-page edition -> onepage.html
rm -rf docs && cp -R _site docs
cp onepage.html docs/onepage.html
touch docs/.nojekyll
git add -A && git commit -m "Update site" && git push
```

Both render lines matter. `onepage.qmd` is deliberately **not** in the project render list in `_quarto.yml` —
it is a self-contained `embed-resources: true` edition of the whole report, not a page of the website, so it
renders to `onepage.html` in the project root and has to be copied into `docs/` by hand. Skipping that copy
silently drops https://jmigartua.github.io/pau-fisika-2026-claude/onepage.html from the published site.

## Theme

`styles.scss` is a single stylesheet serving both colour schemes, adapted from the Codex-side site so the two
studies share one layout, typography and structure. Only the palette differs: UPV/EHU's corporate identity
manual specifies Pantone Process Black and white as the sole corporate colours, so black and white carry text,
headings and surfaces, and the single accent is the institutional blue EHU uses on ehu.eus — `#0066b3`, with
`#004980` for links and a lightened `#4da3e8` in dark mode. The accent appears only where the layout needs
one: active navigation item, active TOC entry, link hover, and key-figure numerals.
