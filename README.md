# Linqore website

Static multi-page site for Linqore (embedded systems, IoT, web and mobile apps).
Live: https://123rahmat.github.io/NX/ (GitHub Pages) and the Cloudflare Worker `nx`.

## Structure
| Path | Purpose |
|---|---|
| `scripts/content.json` | All text: services, projects, FAQ, legal |
| `scripts/build_site.py` | Builds every page, `sitemap.xml`, `robots.txt` and `404.html` |
| `assets/site.css`, `assets/site.js` | Shared design and behaviour (menu, hero animation, filters, contact form) |
| `assets/logo.svg` | Header and footer logo (from the brand pack) |
| `fonts/` | Self-hosted IBM Plex (SIL Open Font License) |
| `brand/` | Logo and brand pack; never published |

Rebuild after any content or design change, then commit:

    python3 scripts/build_site.py

## Publishing
Full go-live checklist (GitHub, Cloudflare, form, Google, domain): see [DEPLOYMENT.md](DEPLOYMENT.md).

- **GitHub Pages:** `.github/workflows/pages.yml` runs security checks and publishes public files on every push.
- **Cloudflare:** `wrangler.jsonc` runs `scripts/cf-build.sh`, which copies only public files to `public/`; `_headers` adds security headers.

## Contact form
On Cloudflare, `worker/index.js` sends it straight to Gmail over SMTP (secrets `GMAIL_USER`, `GMAIL_APP_PASSWORD`).
On GitHub Pages, or if that fails, it falls back to FormSubmit (`FORM_TO`). Setup: [DEPLOYMENT.md](DEPLOYMENT.md#3-contact-form-straight-to-your-gmail-through-your-own-worker).

## Custom domain
After buying a domain and pointing it at the host:

    python3 scripts/set_domain.py https://yourdomain.com/

## Security
Strict Content-Security-Policy on every page (scripts only from this site, no inline code), security headers on
Cloudflare, least-privilege deploy workflow with actions pinned to exact commits, and Dependabot updates.
