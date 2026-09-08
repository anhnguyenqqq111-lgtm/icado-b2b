#!/usr/bin/env python3
"""Extract a conservative, sitemap-checked plan for the 39 requested ICADO URLs."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "icado-sitemap-audit" / "ke-hoach-internal-link-toan-bo-91-bai.md"
SITEMAP = ROOT / "tools" / "icado-sitemap-audit" / "sitemap.xml"
OUT_MD = ROOT / "outputs" / "internal-link-plan-39-bai-gym-icado.md"
OUT_JSON = ROOT / "outputs" / "internal-link-plan-39-bai-gym-icado.json"

REQUESTED = [
    "cac-mau-ao-khoac-tap-gym-icado-phong-cach-cho-chang",
    "cac-mau-quan-short-tap-gym-nam-sieu-hop-cho-cardio",
    "cac-yeu-to-quan-trong-can-luu-y-khi-chon-trang-phuc-tap-gym",
    "cach-chon-size-ao-tap-gym-nu-chuan-nhat-nam-2024",
    "cach-phoi-do-tap-gym-nu-theo-dang-nguoi-dep-nhat",
    "cam-nang-chon-do-tap-gym-cho-nam-2024-ma-ban-khong-nen-bo-qua",
    "cap-nhat-nhanh-xu-huong-ao-tap-gym-nu-nam-2024",
    "chan-thuong-co-tay-khi-tap-gym",
    "checklist-cach-giat-do-the-thao-gym-tennis-pickleball-dung-cach",
    "do-tap-gym-nam-2024-nhung-mau-dep-nhat-dang-mua-nhat",
    "giat-quan-ao-tap-gym-dung-cach-de-bao-ve-suc-khoe",
    "ho-bien-ao-tap-gym-thanh-ao-da-nang-cho-moi-mon-the-thao",
    "icado-thuong-hieu-do-tap-gym-yoga-tennis-pickleball-hang-dau-tai-viet-nam",
    "kham-pha-xu-huong-mac-do-tap-gym-dao-pho-di-choi",
    "lay-si-quan-ao-gym-o-dau-chinh-sach-dai-ly-chiet-khau-cao-tai-icado",
    "loi-khuyen-tu-chuyen-gia-khi-chon-mua-ao-bra-tap-gym",
    "mach-ban-cac-meo-mac-do-tap-gym-nu-dep-nhat",
    "meo-chon-size-ao-tap-gym-nam-chuan-nhat-nam-2024",
    "meo-phoi-do-sieu-dep-cung-ao-tap-gym-nam-icado-2024",
    "mot-vai-tips-chon-do-bo-tap-gym-nu-cho-nang",
    "nguon-hang-gym-nu-dep-lay-si-von-it-loi-nhanh-khong-lo-ton-kho",
    "nguon-si-do-gym-nam-icado-chiet-khau-cao-thuong-hieu-uy-tin-hang-dau",
    "nhung-dieu-can-luu-y-khi-mua-quan-dui-gym-nu",
    "nhung-luu-y-quan-trong-khi-mua-quan-legging-gym-co-tui",
    "nhung-mau-ao-tank-top-gym-nam-nang-dong-va-lich-lam",
    "nhung-mau-quan-legging-co-tui-tien-loi-khi-tap-gym",
    "pickleball-do-nu-co-can-mua-moi-hay-tan-dung-do-tap-gym-yoga",
    "quan-ao-gym-thich-hop-chat-luong-cho-nguoi-tap-tai-nha",
    "tat-tan-tat-nhung-kieu-bra-tap-gym-dinh-cao-tai-icado",
    "top-10-mon-do-tap-gym-nam-khong-the-thieu-trong-tu-do-cua-chang",
    "top-10-set-do-tap-gym-nu-icado-hot-nhat-nam-2024",
    "top-10-thuong-hieu-do-tap-gym-xin-nhat-viet-nam",
    "top-3-mau-gang-tay-tap-gym-ben-dep-cho-gymer",
    "top-5-kieu-quan-tap-gym-nam-ban-chay-nhat-2024",
    "top-5-shop-do-tap-gym-da-nang-sieu-chat-luong",
    "top-6-mau-quan-dui-tap-gym-nam-hot-nhat-he-2024",
    "top-7-mau-ao-bra-gym-nu-pho-bien-nhat-nam-2024",
    "top-8-phu-kien-tap-gym-khong-the-thieu-cho-gymer",
    "top-nhung-mau-quan-tap-gym-nu-xinh-nhat-nam-2024",
]


def sitemap_urls() -> set[str]:
    root = ET.parse(SITEMAP).getroot()
    return {e.text.strip() for e in root.iter() if e.tag.endswith("loc") and e.text}


def sections(text: str):
    chunks = re.split(r"(?m)^### ", text)
    for chunk in chunks[1:]:
        source = re.search(r"\*\*Source URL\*\*: `([^`]+)`", chunk)
        if source:
            yield source.group(1), chunk


def parse_rows(source_url: str, chunk: str, valid_targets: set[str]):
    rows = []
    for line in chunk.splitlines():
        if not line.startswith("| ") or line.startswith("|---") or "Anchor text đề xuất" in line:
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0].startswith("**Commercial"):
            continue
        kind, anchor, target, reason, confidence = cells
        target = target.strip("`")
        if target not in valid_targets or target == source_url:
            continue
        rows.append({
            "source_url": source_url,
            "anchor_text": anchor,
            "target_url": target,
            "reason": reason,
            "confidence": confidence,
            "verification": "Target có trong sitemap cục bộ; anchor cần kiểm tra verbatim trong thân bài/CMS trước khi chèn.",
        })
    return rows


def main():
    valid = sitemap_urls()
    by_slug = {u.rstrip("/").rsplit("/", 1)[-1]: u for u in valid}
    requested_urls = [by_slug.get(slug, f"https://icado.vn/{slug}") for slug in REQUESTED]
    source_chunks = dict(sections(SOURCE.read_text(encoding="utf-8")))
    rows = []
    missing = []
    for source_url in requested_urls:
        if source_url not in source_chunks:
            missing.append(source_url)
            continue
        rows.extend(parse_rows(source_url, source_chunks[source_url], valid))

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    grouped = {}
    for row in rows:
        grouped.setdefault(row["source_url"], []).append(row)
    md = [
        "# Kế hoạch internal link ICADO – 39 bài gym",
        "",
        "- Ngày nghiên cứu: 28/08/2026",
        f"- Bài nguồn đã xử lý: {len(grouped)}/{len(requested_urls)}",
        f"- Đề xuất editorial link: {len(rows)}",
        "- Phạm vi đích: URL cùng domain, đối soát từ `tools/icado-sitemap-audit/sitemap.xml`.",
        "- Lưu ý xác minh: live access không ổn định trong môi trường nghiên cứu; anchor phải được tìm verbatim trong thân bài trước khi chèn. Không dùng title, menu, breadcrumb, related-post hoặc footer làm bằng chứng.",
        "",
    ]
    for source_url in requested_urls:
        items = grouped.get(source_url, [])
        md += [f"## {source_url}", "", "| Anchor text | Target URL | Context/reason | Confidence | Verification |", "|---|---|---|---|---|"]
        for row in items:
            md.append("| {anchor_text} | {target_url} | {reason} | {confidence} | {verification} |".format(**row))
        if not items:
            md.append("| — | — | Không đủ dữ liệu để đề xuất an toàn. | — | Chưa xác minh |")
        md.append("")
    if missing:
        md += ["## URL chưa tìm thấy trong bản kế hoạch nguồn", "", *[f"- {u}" for u in missing], ""]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"sources={len(grouped)} rows={len(rows)} missing={len(missing)}")


if __name__ == "__main__":
    main()
