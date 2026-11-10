# Going live: step-by-step activation

The code is complete. These are the switches only the account owner can flip.

## 1. GitHub Pages (free URL: https://123rahmat.github.io/NX/)
1. Repo → **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. **Settings → Environments → github-pages → Deployment branches**: allow `claude/sweet-wozniak-xg1vgp`. It is the only branch and the default.
3. **Actions** tab → "Deploy to GitHub Pages" → the latest run must be green. Re-run it with **Run workflow** if needed.
4. Account security: **Settings (profile) → Password and authentication → enable 2FA**.

## 2. Cloudflare (Worker `nx`)
1. dash.cloudflare.com → **Workers & Pages → nx → Settings → Build**: repo `123rahmat/NX`, branch `claude/sweet-wozniak-xg1vgp`. Build command can stay empty; `wrangler.jsonc` runs `scripts/cf-build.sh`.
2. **Deployments** → the latest build must say *Success*. Site: `https://nx.<your-subdomain>.workers.dev`.
3. When you own a domain: **nx → Settings → Domains & Routes → Add → Custom domain**, then run `python3 scripts/set_domain.py yourdomain.com`, rebuild, commit, push.
4. Free email on that domain: **Domain → Email → Email Routing** → forward `hello@yourdomain.com` to your Gmail.
5. Profile → **Authentication → enable 2FA**.

## 3. Contact form (straight to your Gmail, through your own Worker)
On the Cloudflare site, the form is sent by the `nx` Worker (`worker/index.js`) through Gmail SMTP. No outside service is involved.
1. Turn on **2-Step Verification** for your Google account (myaccount.google.com → Security).
2. Open **myaccount.google.com/apppasswords** → create an App Password called "Linqore website" → copy the 16 letters.
3. Cloudflare → **Workers & Pages → nx → Settings → Variables and Secrets → Add**:
   - `GMAIL_USER` (type **Secret**) = your Gmail address
   - `GMAIL_APP_PASSWORD` (type **Secret**) = the 16-letter App Password
4. Click **Deploy**, then send a test message from the live Cloudflare site's Contact page. It arrives in your Gmail from "Linqore website", and **Reply** goes to the visitor when they gave an email.

Backup: if the Worker can't send (secrets missing, Gmail down), and on the github.io copy, which has no server, the form uses FormSubmit instead. Click **Activate** once in FormSubmit's first email so that path also reaches you.

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
