from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = ROOT.parent.parent
SOURCE = WORKSPACE_ROOT / "clients" / "General-B2B" / "brands" / "ICADO" / "research" / "icado-tin-tuc-urls.txt"
OUTPUT = ROOT / "sitemap-tin-tuc.xml"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
NEWS_PRIORITY = "0.7"


def main() -> None:
    urls = []
    seen = set()
    for raw in SOURCE.read_text(encoding="utf-8").splitlines():
        url = raw.strip()
        if not url or url in seen:
            continue
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != "icado.vn" or not parsed.path.startswith("/tin-tuc/"):
            raise ValueError(f"URL ngoài phạm vi sitemap tin tức: {url}")
        seen.add(url)
        urls.append(url)

    ET.register_namespace("", NS)
    root = ET.Element(f"{{{NS}}}urlset")
    for url in urls:
        item = ET.SubElement(root, f"{{{NS}}}url")
        ET.SubElement(item, f"{{{NS}}}loc").text = url
        ET.SubElement(item, f"{{{NS}}}priority").text = NEWS_PRIORITY

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {len(urls)} URLs to {OUTPUT}")


if __name__ == "__main__":
    main()
