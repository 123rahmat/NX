"""Switch the whole site to a new address in one step.

Usage (from the repo root):
    python3 scripts/set_domain.py https://nexwire.com/

Rewrites every canonical, Open Graph, schema and sitemap URL, regenerates the
service pages and writes the CNAME file GitHub Pages needs for a custom domain.
Run it once, commit and push. Old github.io links then redirect to the new domain.
"""
import pathlib, re, subprocess, sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG = ROOT / "scripts" / "build_site.py"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    new = sys.argv[1].strip()
    u = urlparse(new)
    if u.scheme != "https" or not u.netloc or u.params or u.query or u.fragment:
        sys.exit("Give a full https address, for example https://nexwire.com/")
    new = f"https://{u.netloc.lower()}{u.path.rstrip('/')}/"

    old = re.search(r'^BASE = "([^"]+)"', CONFIG.read_text(), re.M).group(1)
    if old == new:
        sys.exit(f"Already using {new}")

    changed = []
    for f in ROOT.rglob("*"):
        if f.is_dir() or ".git" in f.parts or f.suffix not in {".html", ".xml", ".txt", ".py", ".md"}:
            continue
        text = f.read_text()
        if old in text:
            f.write_text(text.replace(old, new))
            changed.append(str(f.relative_to(ROOT)))

    cname = ROOT / "CNAME"
    if u.path.strip("/"):
        cname.unlink(missing_ok=True)  # a sub-path address is not a custom domain
    else:
        cname.write_text(u.netloc.lower() + "\n")

    subprocess.run([sys.executable, str(CONFIG)], check=True)
    print(f"{old} -> {new}")
    print("Updated:", ", ".join(sorted(changed)))
    print("Next: commit and push, then set the same domain in Settings -> Pages -> Custom domain and tick Enforce HTTPS.")


if __name__ == "__main__":
    main()
