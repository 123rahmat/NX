# Nexwire website

Single-file static site (`index.html`) — no build step, no dependencies.

## Launch from GitHub
Pushing to `main` (or this branch) runs `.github/workflows/pages.yml` and publishes to GitHub Pages.
One-time: **Settings → Pages → Source: GitHub Actions**.
Site URL: `https://123rahmat.github.io/NX/`

## Contact form
Paste your email (or FormSubmit alias) into `<meta name="form-key">` in `index.html`.
Uses FormSubmit (free). First message triggers an activation email from FormSubmit: click it once. Do not edit the `<script>` block: it is locked by a CSP hash.

## Service pages (SEO)
`web-development/`, `embedded-systems/`, `iot-solutions/`, `mobile-apps/`, `projects/` and `sitemap.xml`
are generated static HTML. Edit content in `scripts/build_pages.py`, then run:

    python3 scripts/build_pages.py .

## Moving to your own domain later
1. Buy the domain and point its DNS at GitHub Pages (A records 185.199.108.153, .109.153, .110.153, .111.153; `www` CNAME to `123rahmat.github.io`).
2. Run `python3 scripts/set_domain.py https://yourdomain.com/`, then commit and push.
3. Settings -> Pages -> Custom domain: enter the domain, tick Enforce HTTPS.
4. In Google Search Console add the new domain and use Settings -> Change of address.
