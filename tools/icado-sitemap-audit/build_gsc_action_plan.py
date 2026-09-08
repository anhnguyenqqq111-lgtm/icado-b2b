from __future__ import annotations

import concurrent.futures
import csv
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

import ssl
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parent
SOURCE = Path("/Users/t.anh/Downloads/https___icado.vn_-Coverage-Drilldown-2026-08-15.xlsx")
OUT = ROOT / "gsc-url-research.json"


def norm(value: str) -> str:
    value = unquote(value).lower().strip("/")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"^(san-pham|tag|category|chuyen-muc|tu-khoa-san-pham)/", "", value)
    value = re.sub(r"/(feed|page/\d+)$", "", value)
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def tokens(value: str) -> set[str]:
    stop = {"icado", "thoi", "trang", "san", "pham", "nu", "nam", "cao", "cap", "chinh", "hang"}
    return {x for x in norm(value).split("-") if len(x) > 1 and x not in stop}


def similarity(a: str, b: str) -> float:
    aa, bb = tokens(a), tokens(b)
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def read_gsc() -> list[dict]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    with zipfile.ZipFile(SOURCE) as zf:
        shared = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.findall(".//m:t", ns)) for si in root.findall("m:si", ns)]
        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        relmap = {r.attrib["Id"]: r.attrib["Target"] for r in rels}
        sheet = next(s for s in wb.findall(".//m:sheet", ns) if s.attrib["name"] == "Table")
        target = relmap[sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]]
        if not target.startswith("xl/"):
            target = "xl/" + target
        root = ET.fromstring(zf.read(target))
        data = []
        for r in root.findall(".//m:sheetData/m:row", ns)[1:]:
            values = {}
            for c in r.findall("m:c", ns):
                col = re.match(r"[A-Z]+", c.attrib["r"]).group()
                v = c.find("m:v", ns)
                value = "" if v is None else v.text or ""
                if c.attrib.get("t") == "s" and value:
                    value = shared[int(value)]
                values[col] = value
            if values.get("A"):
                data.append({"url": values["A"], "last_crawled": values.get("B", "")})
        return data


def read_current() -> list[dict]:
    with (ROOT / "url-audit.csv").open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("indexable") == "True" and r.get("status") == "200"]


def fetch(url: str) -> dict:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; ICADO-SEO-Audit/1.0)"})
        with urllib.request.urlopen(req, timeout=25, context=ssl.create_default_context()) as resp:
            body = resp.read(1_500_000).decode("utf-8", errors="ignore")
            title = ""
            m = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
            if m:
                title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
            robots = ""
            m = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)', body, re.I)
            if m:
                robots = m.group(1)
            return {"live_status": resp.status, "live_final_url": resp.geturl(), "live_title": title, "live_robots": robots}
    except urllib.error.HTTPError as exc:
        return {"live_status": exc.code, "live_final_url": exc.geturl(), "live_title": "", "live_robots": ""}
    except Exception as exc:
        return {"live_status": 0, "live_final_url": "", "live_title": "", "live_robots": "", "fetch_error": type(exc).__name__}


def classify(url: str) -> str:
    p = urlparse(url)
    path = p.path
    if path.startswith("/san-pham/"): return "legacy_product"
    if path.startswith("/tag/"): return "tag"
    if path.startswith("/tu-khoa-san-pham/"): return "product_tag"
    if path.startswith("/blocks/"): return "theme_block"
    if path.startswith("/category/"): return "legacy_category"
    if path.startswith("/chuyen-muc/"): return "legacy_section"
    if path.startswith("/author/"): return "author_archive"
    if path.startswith("/api/"): return "api"
    if path.startswith("/_next/"): return "next_asset"
    if "/feed/" in path or path.endswith("/feed"): return "feed"
    if re.search(r"/page/\d+/?$", path): return "pagination"
    if p.query: return "query_url"
    return "legacy_other"


def choose(row: dict, current: list[dict]) -> dict:
    url = row["url"]
    group = classify(url)
    path = urlparse(url).path
    oldslug = norm(path)
    candidates = []
    for c in current:
        score = similarity(oldslug, urlparse(c["url"]).path)
        if score:
            candidates.append((score, c["url"], c.get("type", ""), c.get("title", "")))
    candidates.sort(reverse=True)
    best = candidates[0] if candidates else (0.0, "", "", "")
    exact = next((c for c in current if norm(urlparse(c["url"]).path) == oldslug), None)
    old_codes = set(re.findall(r"\b(?:[a-z]{1,5}\d{1,5}|\d{4,6})\b", oldslug))
    code_matches = []
    for c in current:
        haystack = norm(urlparse(c["url"]).path + " " + c.get("title", ""))
        if old_codes and old_codes & set(re.findall(r"\b(?:[a-z]{1,5}\d{1,5}|\d{4,6})\b", haystack)):
            code_matches.append(c)
    live_status = row.get("live_status", 0)
    live_final = row.get("live_final_url", "")

    target = ""
    action = "KEEP_404"
    confidence = "High"
    reason = "URL đã trả 404 và không có trang mới tương đương; giữ 404, gỡ khỏi liên kết và sitemap."

    if group == "api":
        action, target, confidence = "KEEP_UTILITY_NO_INDEX", live_final, "High"
        reason = "Route đổi ngôn ngữ/API có đích hợp lệ; giữ chức năng, không đưa vào sitemap và có thể chặn crawl sau khi Google cập nhật."
    elif live_final and live_final.rstrip("/") != url.rstrip("/"):
        action, target, confidence = "KEEP_REDIRECT", live_final, "High"
        reason = "URL đang chuyển hướng tới đích liên quan; xác nhận redirect máy chủ là 301/308 và không tạo chuỗi chuyển hướng."
    elif live_status == 200 and any(c["url"].rstrip("/") == live_final.rstrip("/") for c in current):
        action, target, confidence = "KEEP_200", live_final, "High"
        reason = "URL hiện là trang indexable thuộc crawl/sitemap mới; giữ 200 và tối ưu indexability."
    elif live_status == 200 and row.get("live_title") == "Shop unavailable":
        action, confidence = "FIX_SOFT_404_TO_410", "High"
        reason = "URL trả 200 nhưng nội dung là 'Shop unavailable' (soft 404); đổi sang HTTP 410/404 thật."
    elif group in {"tag", "product_tag", "author_archive", "theme_block"} and live_status == 200:
        action, confidence = "REMOVE_AND_RETURN_410", "High"
        reason = "Trang archive/block mỏng vẫn trả 200; xóa khỏi liên kết/sitemap và trả 410. Chỉ giữ nếu có chiến lược landing page riêng."
    elif group in {"legacy_other", "legacy_category", "legacy_section"} and live_status == 200 and row.get("live_title"):
        action, target, confidence = "KEEP_200_OPTIMIZE", url.rstrip("/"), "Medium"
        reason = "URL có nội dung và tiêu đề thực; giữ 200, bổ sung canonical, internal link và đánh giá chất lượng trước khi yêu cầu index."
    elif group == "pagination" and live_status == 200:
        action, confidence = "KEEP_200_NO_SITEMAP", "Medium"
        reason = "Trang phân trang đang hoạt động; giữ 200 nếu có danh sách khác biệt, canonical tự tham chiếu và không đưa vào sitemap."
    elif group == "next_asset":
        action, confidence = "IGNORE_STATIC_ASSET", "High"
        reason = "Tài nguyên tĩnh Next.js không cần index; không đưa vào sitemap và không chặn toàn bộ /_next/static/."
    elif group == "query_url" and live_status == 200:
        action, confidence = "NOINDEX_CANONICAL", "High"
        reason = "URL tham số hệ thống đang trả 200; thêm noindex/canonical hoặc trả 404 nếu chức năng đã bỏ."
    elif group == "legacy_product" and exact:
        action, target = "301", exact["url"]
        reason = "Slug sản phẩm cũ khớp chính xác sản phẩm trên website mới."
    elif group == "legacy_product" and len(old_codes) == 1 and len(code_matches) == 1 and code_matches[0].get("type") == "product" and similarity(oldslug, code_matches[0]["url"]) >= 0.65:
        action, target, confidence = "301_REVIEW", code_matches[0]["url"], "Medium"
        reason = "Mã sản phẩm trong URL cũ khớp một sản phẩm mới; kiểm tra tên/SKU rồi triển khai 301."
    elif group == "legacy_product" and best[0] >= 0.72 and best[2] == "product":
        action, target, confidence = "301_REVIEW", best[1], "Medium"
        reason = f"Ứng viên sản phẩm mới tương đồng cao ({best[0]:.0%}); kiểm tra SKU/tên trước khi bật 301."
    elif group in {"legacy_category", "legacy_section", "tag", "product_tag"} and best[0] >= 0.78 and best[2] in {"category", "blog_category"}:
        action, target, confidence = "301_REVIEW", best[1], "Medium"
        reason = f"Có danh mục mới tương đồng cao ({best[0]:.0%}); duyệt thủ công trước khi 301."
    elif live_status == 200:
        action, confidence = "MANUAL_REVIEW_200", "Low"
        reason = "URL trả 200 nhưng không khớp sitemap/crawl mới; kiểm tra nội dung trước khi giữ, noindex hoặc trả 410."

    return {
        **row,
        "group": group,
        "recommended_action": action,
        "target_url": target,
        "confidence": confidence,
        "reason": reason,
        "best_candidate": best[1],
        "candidate_score": round(best[0], 3),
        "candidate_title": best[3],
    }


def main() -> None:
    rows = read_gsc()
    current = read_current()
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(fetch, (r["url"] for r in rows)))
    enriched = []
    for base, live in zip(rows, results):
        enriched.append(choose({**base, **live}, current))
    OUT.write_text(json.dumps({"rows": enriched, "current_urls": current}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"gsc_rows": len(rows), "current_urls": len(current), "output": str(OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
