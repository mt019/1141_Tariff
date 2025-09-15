#!/usr/bin/env python3
import argparse
import time
from pathlib import Path
from typing import List, Tuple

import re


def load_site_url(config_path: Path) -> str:
    text = config_path.read_text(encoding="utf-8")
    m = re.search(r"^\s*site_url\s*:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text, re.MULTILINE)
    site_url = (m.group(1).strip() if m else "")
    if not site_url:
        raise ValueError("site_url missing in mkdocs config")
    if not site_url.endswith("/"):
        site_url += "/"
    return site_url


def collect_urls(site_dir: Path, site_url: str) -> List[Tuple[str, str]]:
    urls: List[Tuple[str, str]] = []
    for p in site_dir.rglob("*.html"):
        rel = p.relative_to(site_dir).as_posix()
        if rel == "404.html" or rel.startswith("search/"):
            continue
        if rel.endswith("/index.html"):
            loc = site_url + rel[: -len("index.html")]
        elif rel == "index.html":
            loc = site_url
        else:
            loc = site_url + rel
        lastmod = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(p.stat().st_mtime))
        urls.append((loc, lastmod))
    return urls


def write_sitemap(site_dir: Path, urls: List[Tuple[str, str]]):
    site_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">",
    ]
    for loc, lastmod in sorted(urls):
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (site_dir / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Generate sitemap.xml for MkDocs output")
    ap.add_argument("--config", default="mkdocs/mkdocs.yml", help="Path to mkdocs.yml")
    ap.add_argument("--site-dir", default="mkdocs/site", help="Built site directory")
    args = ap.parse_args()

    config_path = Path(args.config)
    site_dir = Path(args.site_dir)

    site_url = load_site_url(config_path)
    urls = collect_urls(site_dir, site_url)
    write_sitemap(site_dir, urls)
    print(f"sitemap.xml generated at {site_dir}/sitemap.xml with {len(urls)} URLs")


if __name__ == "__main__":
    main()
