# Going live: step-by-step activation

The code is complete. These are the switches only the account owner can flip.

## 1. GitHub Pages (free URL: https://123rahmat.github.io/NX/)
1. Repo → **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. **Settings → Environments → github-pages → Deployment branches**: allow `claude/sweet-wozniak-xg1vgp` (or `main` once merged).
3. **Actions** tab → "Deploy to GitHub Pages" → the latest run must be green. Re-run it with **Run workflow** if needed.
4. Optional: merge the branch into `main` so `main` is the source of truth.
5. Account security: **Settings (profile) → Password and authentication → enable 2FA**.

## 2. Cloudflare (Worker `nx`)
1. dash.cloudflare.com → **Workers & Pages → nx → Settings → Build**: repo `123rahmat/NX`, branch `claude/sweet-wozniak-xg1vgp` (or `main`). Build command can stay empty; `wrangler.jsonc` runs `scripts/cf-build.sh`.
2. **Deployments** → the latest build must say *Success*. Site: `https://nx.<your-subdomain>.workers.dev`.
3. When you own a domain: **nx → Settings → Domains & Routes → Add → Custom domain**, then run `python3 scripts/set_domain.py yourdomain.com`, rebuild, commit, push.
4. Free email on that domain: **Domain → Email → Email Routing** → forward `hello@yourdomain.com` to your Gmail.
5. Profile → **Authentication → enable 2FA**.

## 3. Contact form (FormSubmit)
1. Open the live site → Contact → send a test message.
2. Open the "Activate Form" email from FormSubmit in your Gmail and click **Activate**.
3. FormSubmit then mails you a random alias. Put it in `FORM_TO` in `scripts/build_site.py`, rebuild (`python3 scripts/build_site.py`), commit and push. This hides your email from the page source.

## 4. Google
1. search.google.com/search-console → **Add property (URL prefix)** with the live URL → verify (HTML tag or DNS for a domain).
2. **Sitemaps** → submit `sitemap.xml`.
3. business.google.com → create a **Business Profile** with the same name, phone and city as the site.

## 5. After every change
```bash
python3 scripts/build_site.py
```
```bash
git add -A && git commit -m "Update site" && git push
```
Both GitHub Pages and Cloudflare redeploy automatically.
