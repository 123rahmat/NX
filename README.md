# Nexora Digital website

Single-file static site (`index.html`) — no build step, no dependencies.

## Launch from GitHub
Pushing to `main` (or this branch) runs `.github/workflows/pages.yml` and publishes to GitHub Pages.
One-time: **Settings → Pages → Source: GitHub Actions**.
Site URL: `https://123rahmat.github.io/NX/`

## Contact form
Paste your email (or FormSubmit alias) into `<meta name="form-key">` in `index.html`.
Uses FormSubmit (free). First message triggers an activation email from FormSubmit: click it once. Do not edit the `<script>` block: it is locked by a CSP hash.
