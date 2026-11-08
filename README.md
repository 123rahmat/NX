# Nexwire website

Static multi-page site published by GitHub Actions to GitHub Pages:
https://linqore.com/

## Structure
- `scripts/content.json`: all text (services, projects, FAQ, legal). Edit content here.
- `scripts/build_site.py`: builds every page, `sitemap.xml` and `robots.txt`.
- `assets/site.css`, `assets/site.js`: shared design and behaviour (menu, hero animation, filters, contact form).
- `fonts/`: self-hosted IBM Plex (SIL Open Font License, see `fonts/OFL.txt`).

After editing content or the generator, rebuild and commit:

    python3 scripts/build_site.py

## Contact form
Sent through FormSubmit to the address in `FORM_TO` in `scripts/build_site.py`.
The first message triggers an activation email from FormSubmit: click it once.
Then replace the email in `FORM_TO` with the random alias FormSubmit gives you and rebuild,
so your address is not visible in the page.

## Security
- Strict Content-Security-Policy on every page: scripts only from this site, no inline code,
  network requests only to FormSubmit, no plugins, no embedding in other sites.
- Deploy workflow: least-privilege permissions, actions pinned to exact commits, a check that
  fails the deploy if a page lacks the security policy or a secret is committed.
  Only public files are published (no `scripts/`, `README.md` or `.github/`).
- Dependabot keeps the pinned actions updated.

## Moving to your own domain later
1. Buy the domain and point its DNS at GitHub Pages (A records 185.199.108.153, .109.153, .110.153, .111.153; `www` CNAME to `123rahmat.github.io`).
2. Run `python3 scripts/set_domain.py https://yourdomain.com/`, then commit and push.
3. Settings -> Pages -> Custom domain: enter the domain, tick Enforce HTTPS.
4. In Google Search Console add the new domain and use Settings -> Change of address.
