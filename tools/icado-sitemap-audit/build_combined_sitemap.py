from __future__ import annotations

import csv
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / "url-audit.csv"
NEWS = ROOT / "sitemap-tin-tuc.xml"
OUTPUT = ROOT / "sitemap-all.xml"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def main() -> None:
    urls: list[tuple[str, str]] = []
    seen: set[str] = set()

    with AUDIT.open(encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            url = row.get("url", "").strip()
            if (
                url
                and url not in seen
                and row.get("status") == "200"
                and row.get("indexable") == "True"
                and row.get("soft_404") != "True"
            ):
                seen.add(url)
                url_type = row.get("type", "")
                priority = "1.0" if url_type == "home" else "0.9" if url_type in {"category", "blog_category"} else "0.8" if url_type == "product" else "0.6"
                urls.append((url, priority))

    news_root = ET.parse(NEWS).getroot()
    for item in news_root:
        loc = item.find(f"{{{NS}}}loc")
        if loc is not None and loc.text and loc.text not in seen:
            seen.add(loc.text)
            urls.append((loc.text, "0.7"))

    ET.register_namespace("", NS)
    root = ET.Element(f"{{{NS}}}urlset")
    for url, priority in urls:
        item = ET.SubElement(root, f"{{{NS}}}url")
        ET.SubElement(item, f"{{{NS}}}loc").text = url
        ET.SubElement(item, f"{{{NS}}}priority").text = priority

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {len(urls)} unique URLs to {OUTPUT}")


if __name__ == "__main__":
    main()
