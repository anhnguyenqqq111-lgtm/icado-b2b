from __future__ import annotations

import csv
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / "url-audit.csv"
INDEXABLE_SITEMAP = ROOT / "sitemap-indexable.xml"
NEWS_SITEMAP = ROOT / "sitemap-tin-tuc.xml"
SITEMAP_INDEX = ROOT / "sitemap-index.xml"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


PRIORITY_BY_TYPE = {
    "home": "1.0",
    "category": "0.9",
    "blog_category": "0.9",
    "product": "0.8",
    "article": "0.7",
    "page": "0.6",
}


def write_xml(root: ET.Element, output: Path) -> None:
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(output, encoding="utf-8", xml_declaration=True)


def build_indexable_sitemap() -> int:
    urls = []
    seen = set()
    with AUDIT.open(encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            url = row.get("url", "").strip()
            if (
                not url
                or url in seen
                or row.get("status") != "200"
                or row.get("indexable") != "True"
                or row.get("soft_404") == "True"
            ):
                continue
            seen.add(url)
            urls.append((url, row.get("type", "")))

    root = ET.Element(f"{{{NS}}}urlset")
    for url, url_type in urls:
        item = ET.SubElement(root, f"{{{NS}}}url")
        ET.SubElement(item, f"{{{NS}}}loc").text = url
        ET.SubElement(item, f"{{{NS}}}priority").text = PRIORITY_BY_TYPE.get(url_type, "0.6")
    write_xml(root, INDEXABLE_SITEMAP)
    return len(urls)


def build_index() -> None:
    root = ET.Element(f"{{{NS}}}sitemapindex")
    for location in (
        "https://icado.vn/sitemap-indexable.xml",
        "https://icado.vn/sitemap-tin-tuc.xml",
    ):
        item = ET.SubElement(root, f"{{{NS}}}sitemap")
        ET.SubElement(item, f"{{{NS}}}loc").text = location
    write_xml(root, SITEMAP_INDEX)


def main() -> None:
    if not NEWS_SITEMAP.exists():
        raise FileNotFoundError("Hãy tạo sitemap-tin-tuc.xml trước")
    count = build_indexable_sitemap()
    build_index()
    print(f"Indexable URLs: {count}")
    print(f"Created: {INDEXABLE_SITEMAP}")
    print(f"Created: {SITEMAP_INDEX}")


if __name__ == "__main__":
    ET.register_namespace("", NS)
    main()
