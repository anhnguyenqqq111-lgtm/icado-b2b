#!/usr/bin/env python3
"""Crawl maymaccth.com public sitemaps and export categories/products."""

from __future__ import annotations

import csv
import html
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse


BASE = "https://maymaccth.com"
UA = "Mozilla/5.0 (compatible; catalog-audit/1.0)"
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
OUT = WORKSPACE_ROOT / "clients" / "MayMacCTH" / "research" / "maymaccth-crawl"


def fetch(url: str, attempts: int = 3) -> str:
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as response:
                return response.read().decode("utf-8", "replace")
        except Exception:
            if attempt == attempts - 1:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("unreachable")


def sitemap_urls(url: str) -> list[str]:
    root = ET.fromstring(fetch(url))
    return [node.text.strip() for node in root.findall("{*}url/{*}loc") if node.text]


def clean(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def first_match(page: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, page, re.I | re.S)
        if match:
            value = clean(match.group(1))
            if value:
                return value
    return ""


def page_record(url: str) -> dict[str, str]:
    page = fetch(url)
    name = first_match(page, [
        r'<h1[^>]*>(.*?)</h1>',
        r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']',
        r'<title[^>]*>(.*?)</title>',
    ])
    canonical = first_match(page, [
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']',
        r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\'](.*?)["\']',
    ])
    slug = urlparse(url).path.rstrip("/").split("/")[-1]
    return {"name": name, "slug": slug, "url": canonical or url, "status": "ok"}


def sitemap_record(url: str) -> dict[str, str]:
    slug = urlparse(url).path.rstrip("/").split("/")[-1]
    return {"name": slug.replace("-", " "), "slug": slug, "url": url, "status": "sitemap"}


def crawl_many(urls: list[str]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(page_record, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                records.append(future.result())
            except Exception as exc:
                slug = urlparse(url).path.rstrip("/").split("/")[-1]
                records.append({"name": "", "slug": slug, "url": url, "status": f"error: {exc}"})
    return sorted(records, key=lambda row: (row["name"].casefold(), row["slug"]))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["name", "slug", "url", "status"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    category_urls = sitemap_urls(f"{BASE}/product-categories.xml")
    product_urls: list[str] = []
    sitemap = ET.fromstring(fetch(f"{BASE}/sitemap.xml"))
    product_maps = [
        node.text.strip()
        for node in sitemap.findall("{*}sitemap/{*}loc")
        if node.text and re.search(r"/products-.*\.xml$", node.text)
    ]
    for product_map in product_maps:
        product_urls.extend(sitemap_urls(product_map))

    category_urls = sorted(set(category_urls))
    product_urls = sorted(set(product_urls))
    fetch_titles = "--fetch-titles" in sys.argv
    categories = crawl_many(category_urls) if fetch_titles else [sitemap_record(url) for url in category_urls]
    products = crawl_many(product_urls) if fetch_titles else [sitemap_record(url) for url in product_urls]
    categories.sort(key=lambda row: row["slug"])
    products.sort(key=lambda row: row["slug"])

    OUT.mkdir(exist_ok=True)
    write_csv(OUT / "categories.csv", categories)
    write_csv(OUT / "products.csv", products)

    with (OUT / "README.md").open("w", encoding="utf-8") as handle:
        handle.write("# Crawl maymaccth.com\n\n")
        handle.write(f"- Danh mục: {len(categories)}\n")
        handle.write(f"- Sản phẩm: {len(products)}\n")
        handle.write(f"- Chế độ: {'Tên H1 từ từng trang' if fetch_titles else 'URL/slug chuẩn từ sitemap'}\n")
        handle.write(f"- Lỗi danh mục: {sum(r['status'].startswith('error:') for r in categories)}\n")
        handle.write(f"- Lỗi sản phẩm: {sum(r['status'].startswith('error:') for r in products)}\n")
        handle.write("- Nguồn: sitemap.xml, product-categories.xml và toàn bộ products-*.xml được sitemap khai báo.\n")

    print(f"categories={len(categories)} products={len(products)}")
    print(f"category_errors={sum(r['status'].startswith('error:') for r in categories)} product_errors={sum(r['status'].startswith('error:') for r in products)}")


if __name__ == "__main__":
    main()
