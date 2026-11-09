#!/usr/bin/env bash
# Cloudflare Pages build: copy only the public website files into ./public
set -euo pipefail
rm -rf public && mkdir public
for item in index.html 404.html robots.txt sitemap.xml site.webmanifest og-image.png _headers assets fonts \
            services web-development embedded-systems iot-solutions mobile-apps projects about contact privacy terms; do
  cp -R "$item" public/
done
echo "Published files:"; find public -type f | sort
