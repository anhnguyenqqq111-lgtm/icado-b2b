#!/usr/bin/env python3
"""Crawl icado.vn and generate an indexable URL sitemap plus audit files."""

from __future__ import annotations

import csv
import html
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


BASE = "https://icado.vn/"
HOST = "icado.vn"
OUT = Path(__file__).resolve().parent
MAX_URLS = 10000
REQUEST_DELAY = 0.12
USER_AGENT = "ICADO-Sitemap-Audit/1.0 (+https://icado.vn/)"

EXCLUDED_PREFIXES = (
    "/api/",
    "/auth/",
    "/cart",
    "/checkout",
    "/account",
    "/tai-khoan",
    "/gio-hang",
    "/thanh-toan",
    "/_next/",
)
EXCLUDED_EXTENSIONS = (
    ".avif", ".css", ".gif", ".ico", ".jpeg", ".jpg", ".js", ".json",
    ".pdf", ".png", ".svg", ".webp", ".woff", ".woff2", ".xml", ".zip",
)
EXCLUDED_EXACT_PATHS = {
    "/ebook/nam",
    "/ebook/new",
    "/ebook/nu",
    "/ebook/phu-kien",
    "/ebook/the-thao",
}


@dataclass
class Page:
    url: str
    status: int = 0
    final_url: str = ""
    content_type: str = ""
    title: str = ""
    description: str = ""
    canonical: str = ""
    robots: str = ""
    h1_count: int = 0
    word_count: int = 0
    last_modified: str = ""
    error: str = ""
    links: set[str] = field(default_factory=set)

    @property
    def soft_404(self) -> bool:
        marker = f"{self.title} {self.description}".lower()
        return self.status == 200 and any(x in marker for x in ("404", "không tồn tại", "not found"))

    @property
    def indexable(self) -> bool:
        robots = self.robots.lower()
        canonical_ok = not self.canonical or normalize(self.canonical) == normalize(self.final_url or self.url)
        return (
            self.status == 200
            and self.content_type.startswith("text/html")
            and "noindex" not in robots
            and not self.soft_404
            and canonical_ok
        )


def normalize(raw: str, base: str = BASE) -> str | None:
    if not raw:
        return None
    raw = html.unescape(raw.strip())
    if raw.startswith(("mailto:", "tel:", "javascript:", "data:", "#")):
        return None
    absolute = urllib.parse.urljoin(base, raw)
    parts = urllib.parse.urlsplit(absolute)
    host = parts.netloc.lower().removeprefix("www.")
    if host != HOST or parts.scheme not in ("http", "https"):
        return None
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    lowered = path.lower()
    if lowered in EXCLUDED_EXACT_PATHS or lowered.startswith(EXCLUDED_PREFIXES) or lowered.endswith(EXCLUDED_EXTENSIONS):
        return None
    if path != "/":
        path = path.rstrip("/")
    # Query parameters create filter/sort/search duplicates on commerce sites.
    return urllib.parse.urlunsplit(("https", HOST, path, "", ""))


def attr(content: str, tag: str, name: str, value: str, wanted: str = "content") -> str:
    patterns = (
        rf"<{tag}\b(?=[^>]*\b{name}=[\"']{re.escape(value)}[\"'])[^>]*\b{wanted}=[\"']([^\"']*)[\"'][^>]*>",
        rf"<{tag}\b(?=[^>]*\b{wanted}=[\"']([^\"']*)[\"'])[^>]*\b{name}=[\"']{re.escape(value)}[\"'][^>]*>",
    )
    for pattern in patterns:
        match = re.search(pattern, content, re.I)
        if match:
            return html.unescape(match.group(1)).strip()
    return ""


def extract(content: str, url: str) -> tuple[dict[str, object], set[str]]:
    title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.I | re.S)
    title = re.sub(r"\s+", " ", html.unescape(title_match.group(1))).strip() if title_match else ""
    description = attr(content, "meta", "name", "description")
    robots = attr(content, "meta", "name", "robots")
    canonical = attr(content, "link", "rel", "canonical", "href")
    if canonical:
        canonical = normalize(canonical, url) or canonical
    h1_count = len(re.findall(r"<h1\b", content, re.I))
    body = re.sub(r"<(script|style|noscript)\b[^>]*>.*?</\1>", " ", content, flags=re.I | re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"\s+", " ", html.unescape(body)).strip()
    links: set[str] = set()
    for raw in re.findall(r"<a\b[^>]*\bhref=[\"']([^\"']+)[\"']", content, re.I):
        normalized = normalize(raw, url)
        if normalized:
            links.add(normalized)
    return {
        "title": title,
        "description": description,
        "robots": robots,
        "canonical": canonical,
        "h1_count": h1_count,
        "word_count": len(body.split()),
    }, links


def fetch(url: str) -> Page:
    page = Page(url=url)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            page.status = response.status
            page.final_url = normalize(response.geturl()) or response.geturl()
            page.content_type = response.headers.get_content_type()
            page.last_modified = response.headers.get("Last-Modified", "")
            if page.content_type.startswith("text/html"):
                content = response.read(8_000_000).decode("utf-8", "ignore")
                fields, page.links = extract(content, page.final_url or url)
                for key, value in fields.items():
                    setattr(page, key, value)
    except urllib.error.HTTPError as exc:
        page.status = exc.code
        page.final_url = normalize(exc.geturl()) or exc.geturl()
        page.error = str(exc)
    except Exception as exc:
        page.error = f"{type(exc).__name__}: {exc}"
    return page


def classify(url: str) -> str:
    path = urllib.parse.urlsplit(url).path.strip("/")
    if not path:
        return "home"
    first = path.split("/")[0]
    if first in {"tin-tuc", "blog", "kien-thuc"}:
        return "article" if path.count("/") else "article-index"
    if first == "ho-tro":
        return "policy"
    if first in {"gioi-thieu", "lien-he", "dai-ly", "hop-tac-kinh-doanh", "xuong-san-xuat"}:
        return "corporate"
    if first in {"chinh-sach-bao-hanh", "chinh-sach-doi-tra", "giao-hang-thanh-toan", "chinh-sach-bao-mat", "quy-che-hoat-dong", "huong-dan-mua-online"}:
        return "policy"
    if re.search(r"/(san-pham|product)/", f"/{path}/") or re.search(
        r"-icado-(?:at|ht|id|sa|lite|tpe|\d)[a-z0-9-]*$", path
    ):
        return "product"
    if path.count("/") >= 1:
        return "detail"
    return "category-or-landing"


def write_csv(pages: list[Page]) -> None:
    path = OUT / "url-audit.csv"
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["url", "type", "status", "final_url", "indexable", "soft_404", "canonical", "robots", "title", "title_length", "description", "description_length", "h1_count", "word_count", "last_modified", "error"])
        for p in sorted(pages, key=lambda x: x.url):
            writer.writerow([p.url, classify(p.url), p.status, p.final_url, p.indexable, p.soft_404, p.canonical, p.robots, p.title, len(p.title), p.description, len(p.description), p.h1_count, p.word_count, p.last_modified, p.error])


def write_sitemap(pages: list[Page]) -> None:
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    root = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
    today = datetime.now(timezone.utc).date().isoformat()
    for page in sorted((p for p in pages if p.indexable), key=lambda p: p.url):
        node = ET.SubElement(root, "{http://www.sitemaps.org/schemas/sitemap/0.9}url")
        ET.SubElement(node, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text = page.final_url or page.url
        ET.SubElement(node, "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod").text = today
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(OUT / "sitemap.xml", encoding="utf-8", xml_declaration=True)


def write_report(pages: list[Page], elapsed: float) -> None:
    statuses = Counter(p.status for p in pages)
    types = Counter(classify(p.url) for p in pages if p.indexable)
    indexable = [p for p in pages if p.indexable]
    missing_title = [p for p in indexable if not p.title]
    missing_desc = [p for p in indexable if not p.description]
    missing_h1 = [p for p in indexable if p.h1_count == 0]
    multi_h1 = [p for p in indexable if p.h1_count > 1]
    canonical_conflicts = [p for p in pages if p.canonical and normalize(p.canonical) != normalize(p.final_url or p.url)]
    missing_canonical = [p for p in indexable if not p.canonical]
    title_groups: dict[str, list[Page]] = {}
    for page in indexable:
        if page.title:
            title_groups.setdefault(page.title, []).append(page)
    duplicate_title_groups = {title: group for title, group in title_groups.items() if len(group) > 1}
    duplicate_title_urls = sum(len(group) for group in duplicate_title_groups.values())
    errors = [p for p in pages if p.error]

    def sample(items: list[Page], limit: int = 20) -> str:
        return "\n".join(f"- {p.url}" for p in items[:limit]) or "- Không có"

    report = f"""# ICADO crawl and sitemap audit

- Research date: {datetime.now().astimezone().isoformat(timespec='seconds')}
- Start URL: {BASE}
- Crawled URLs: {len(pages)}
- Indexable URLs in sitemap: {len(indexable)}
- Crawl duration: {elapsed:.1f} seconds
- Existing `/robots.txt` and sitemap endpoints: rendered as site HTML/soft 404 during initial inspection

## Indexable URLs by inferred type

{chr(10).join(f'- {key}: {value}' for key, value in sorted(types.items()))}

## HTTP status summary

{chr(10).join(f'- {key}: {value}' for key, value in sorted(statuses.items()))}

## Metadata findings

- Missing title: {len(missing_title)}
- Missing meta description: {len(missing_desc)}
- Missing H1: {len(missing_h1)}
- Multiple H1: {len(multi_h1)}
- Missing canonical: {len(missing_canonical)}
- Conflicting canonical: {len(canonical_conflicts)}
- URLs participating in duplicate-title groups: {duplicate_title_urls}
- Fetch errors: {len(errors)}

### Missing title samples

{sample(missing_title)}

### Missing description samples

{sample(missing_desc)}

### Missing H1 samples

{sample(missing_h1)}

### Conflicting canonical samples

{sample(canonical_conflicts)}

### Missing canonical samples

{sample(missing_canonical)}

### Duplicate title groups

{chr(10).join(f'- `{title}`: ' + ', '.join(p.url for p in group[:10]) for title, group in sorted(duplicate_title_groups.items())) or '- Không có'}

### Fetch error samples

{sample(errors)}

## Sitemap inclusion rules

Included only URLs that:

- returned HTTP 200;
- returned HTML;
- did not declare `noindex`;
- were not detected as soft 404;
- were self-canonical or had no canonical declaration;
- had no query parameters;
- were not auth, cart, checkout, account, API, static asset, PDF, or media URLs.

## Recommended deployment

1. Serve `sitemap.xml` at `https://icado.vn/sitemap.xml` with `application/xml`.
2. Add `Sitemap: https://icado.vn/sitemap.xml` to a real plain-text `robots.txt`.
3. Generate sitemap dynamically from active products/categories/articles so inventory changes are reflected automatically.
4. Use actual database `updated_at` values for `<lastmod>` instead of crawl date when implementing dynamically.
5. Keep filtered, sorted, searched, account, cart, and checkout URLs out of the sitemap.
"""
    (OUT / "AUDIT.md").write_text(report, encoding="utf-8")


def main() -> int:
    started = time.time()
    queue = deque([BASE])
    queued = {BASE}
    pages: list[Page] = []
    while queue and len(pages) < MAX_URLS:
        url = queue.popleft()
        page = fetch(url)
        pages.append(page)
        print(f"[{len(pages):04d}] {page.status or 'ERR'} {url} ({len(page.links)} links)", flush=True)
        for link in sorted(page.links):
            if link not in queued and len(queued) < MAX_URLS:
                queued.add(link)
                queue.append(link)
        time.sleep(REQUEST_DELAY)

    write_csv(pages)
    write_sitemap(pages)
    write_report(pages, time.time() - started)
    print(f"\nWrote {OUT / 'sitemap.xml'}")
    print(f"Wrote {OUT / 'url-audit.csv'}")
    print(f"Wrote {OUT / 'AUDIT.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
