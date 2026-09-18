# Deploy the site to GitHub Pages

The rendered site is copied to `docs/` (with a `.nojekyll` marker) so GitHub Pages can serve it from the `main` branch.
Run these on the Mac, from this folder, with the GitHub CLI signed in (`gh auth login` once):

```bash
cd "/Users/User/Desktop/2026/20260701/20260706_pau_fisika_analysis/claude_analysis_2026-09-18"
gh repo create pau-fisika-2026 --public --source=. --remote=origin --push
gh api -X POST repos/jmigartua/pau-fisika-2026/pages -f 'source[branch]=main' -f 'source[path]=/docs'
```

The site will be at https://jmigartua.github.io/pau-fisika-2026/ within a minute or two
(replace `jmigartua` if your GitHub user name is different; use `--private` instead of `--public` if you prefer,
Pages on a private repo needs a paid plan).

After any re-render (`quarto render`), refresh the served copy and push:

```bash
rm -rf docs && cp -R _site docs && touch docs/.nojekyll
git add -A && git commit -m "Update site" && git push
```

Without the GitHub CLI: create an empty repository on github.com, then
`git remote add origin https://github.com/<user>/pau-fisika-2026.git && git push -u origin main`,
and in the repository's Settings → Pages choose "Deploy from a branch", branch `main`, folder `/docs`.
