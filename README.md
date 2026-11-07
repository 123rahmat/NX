# Nexora Digital website

Single-file static site (`index.html`) — no build step, no dependencies.

## Launch from GitHub
Pushing to `main` (or this branch) runs `.github/workflows/pages.yml` and publishes to GitHub Pages.
One-time: **Settings → Pages → Source: GitHub Actions**.
Site URL: `https://123rahmat.github.io/NX/`

## Contact form
Paste your Web3Forms access key into `<meta name="form-key" content="">` in `index.html`.
Do not edit the `<script>` block: it is locked by a CSP hash.
