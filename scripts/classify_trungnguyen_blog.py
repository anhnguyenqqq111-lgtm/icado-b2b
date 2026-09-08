#!/usr/bin/env python3
"""Classify Trung Nguyen TNT blog titles into the approved news categories."""

from __future__ import annotations

import re
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

SOURCE = Path("/Users/t.anh/Downloads/page_titles_all.xlsx")
OUT = Path("outputs/trung-nguyen-blog-classification")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

CATS = {
    "Băng tải PVC": ("bang-tai-pvc", "Băng tải PVC, dây băng tải PVC và hệ thống vận chuyển", "Băng tải PVC", "https://trungnguyentw.com/may-moc-phu-tro-nganh-nhua/bang-tai/"),
    "Cánh tay robot": ("canh-tay-robot", "Robot gắp sản phẩm và tự động hóa nhà máy nhựa", "Cánh tay robot", "https://trungnguyentw.com/canh-tay-robot/"),
    "Chiller giải nhiệt gió và chiller giải nhiệt nước": ("chiller-gio-va-nuoc", "Chiller, làm lạnh khuôn và hệ thống giải nhiệt", "Chiller công nghiệp", "https://trungnguyentw.com/chiller-cong-nghiep/"),
    "Cụm gia nhiệt hồng ngoại FIR": ("cum-gia-nhiet-hong-ngoai-fir", "Gia nhiệt hồng ngoại xa và tiết kiệm năng lượng", "Cụm gia nhiệt hồng ngoại FIR", "https://trungnguyentw.com/"),
    "Máy băm, nghiền nhựa": ("may-bam-nghien-nhua", "Băm nghiền, dao nghiền và tái chế phế liệu nhựa", "Máy băm nghiền nhựa", "https://trungnguyentw.com/may-moc-phu-tro-nganh-nhua/may-bam-may-nghien/"),
    "Máy chấm keo PVC sản xuất nhãn mác, đế giày": ("may-cham-keo-pvc", "Máy chấm keo và sản xuất sản phẩm PVC mềm", "Máy chấm keo PVC", "https://trungnguyentw.com/may-cham-keo-pvc-tu-dong/"),
    "Máy gia nhiệt": ("may-gia-nhiet", "Gia nhiệt và kiểm soát nhiệt độ khuôn", "Máy điều khiển nhiệt độ khuôn", "https://trungnguyentw.com/may-moc-phu-tro-nganh-nhua/may-dieu-khien-nhiet-do-khuon/"),
    "Máy hút liệu": ("may-hut-lieu", "Hút liệu, cấp liệu chân không và vận chuyển hạt nhựa", "Máy hút liệu tự động", "https://trungnguyentw.com/may-moc-phu-tro-nganh-nhua/may-hut-lieu-tu-dong/"),
    "Máy sấy nhựa": ("may-say-nhua", "Sấy, hút ẩm và kiểm soát độ ẩm hạt nhựa", "Máy sấy nhựa", "https://trungnguyentw.com/may-moc-phu-tro-nganh-nhua/may-say/"),
    "Máy trộn nhựa": ("may-tron-nhua", "Trộn hạt, trộn màu và phối liệu nhựa", "Máy trộn nhựa", "https://trungnguyentw.com/may-moc-phu-tro-nganh-nhua/may-tron-nhua/"),
    "Sàng rung công nghiệp": ("sang-rung", "Sàng rung và phân loại kích thước nguyên liệu", "Sàng rung công nghiệp", "https://trungnguyentw.com/may-moc-phu-tro-nganh-nhua/sang-rung/"),
    "Tin tức thị trường ngành nhựa": ("tin-tuc-thi-truong", "Thị trường, chính sách và xu hướng ngành nhựa", "Traffic Only", "https://trungnguyentw.com/tin-tuc/"),
    "Tổng quan về nhựa": ("tong-quan-ve-nhua", "Vật liệu polymer, tính chất và quy trình sản xuất nhựa", "Sản phẩm/thiết bị phù hợp theo vật liệu", "https://trungnguyentw.com/may-moc-phu-tro-nganh-nhua/"),
    "Dịch vụ bảo trì, bảo dưỡng, sửa chữa": ("dich-vu-bao-tri-bao-duong-sua-chua", "Dịch vụ kỹ thuật, bảo trì và sửa chữa tại nhà máy", "Dịch vụ bảo trì, sửa chữa", "https://trungnguyentw.com/dich-vu-bao-tri-bao-duong-sua-chua-bang-tai-nhua/"),
    "Tin tức": ("tin-tuc", "Tin doanh nghiệp hoặc chủ đề công nghiệp tổng hợp", "Traffic Only", "https://trungnguyentw.com/tin-tuc/"),
    "Need Manual Review": ("", "Không đủ dữ liệu để xác định chủ đề trung tâm", "Traffic Only", ""),
}

OPPS = {
    "Băng tải PVC": ["giá băng tải PVC theo mét", "cách chọn độ dày dây băng tải PVC", "băng tải PVC cho máy ép nhựa", "lỗi lệch băng tải và cách chỉnh"],
    "Cánh tay robot": ["robot gắp nhựa phù hợp máy ép bao nhiêu tấn", "giá robot 3 trục máy ép nhựa", "so sánh robot 3 trục và 5 trục", "hoàn vốn robot gắp sản phẩm"],
    "Chiller giải nhiệt gió và chiller giải nhiệt nước": ["cách tính công suất chiller cho máy ép nhựa", "giá chiller công nghiệp theo HP", "chiller gió hay nước cho nhà máy nhựa", "lỗi áp suất cao chiller"],
    "Cụm gia nhiệt hồng ngoại FIR": ["gia nhiệt FIR tiết kiệm bao nhiêu điện", "so sánh FIR và điện trở vòng", "giá cụm gia nhiệt hồng ngoại máy ép nhựa", "cách chọn công suất FIR"],
    "Máy băm, nghiền nhựa": ["máy nghiền phù hợp từng loại phế liệu", "giá máy băm nhựa theo công suất", "cách chọn dao máy nghiền nhựa", "máy nghiền chậm hay nhanh"],
    "Máy chấm keo PVC sản xuất nhãn mác, đế giày": ["giá máy chấm keo PVC tự động", "chi phí dây chuyền làm nhãn PVC", "máy chấm keo PVC bao nhiêu màu", "khuôn làm logo PVC theo yêu cầu"],
    "Máy gia nhiệt": ["cách chọn máy nhiệt độ khuôn nước hay dầu", "giá máy điều khiển nhiệt độ khuôn", "cách tính công suất gia nhiệt khuôn", "lỗi quá nhiệt máy nhiệt độ khuôn"],
    "Máy hút liệu": ["cách chọn máy hút liệu theo khoảng cách", "giá máy hút liệu tự động", "máy hút liệu 1 pha hay 3 pha", "thiết kế hệ thống cấp liệu trung tâm"],
    "Máy sấy nhựa": ["bảng nhiệt độ sấy từng loại nhựa", "cách chọn phễu sấy theo công suất", "giá máy sấy hút ẩm nhựa", "so sánh phễu sấy và máy sấy 3 trong 1"],
    "Máy trộn nhựa": ["cách chọn máy trộn đứng hay ngang", "giá máy trộn nhựa theo kg", "thời gian trộn hạt nhựa tối ưu", "máy trộn màu cho từng loại nhựa"],
    "Sàng rung công nghiệp": ["cách chọn kích thước lưới sàng", "giá sàng rung công nghiệp", "sàng rung cho hạt nhựa tái chế", "lỗi sàng rung yếu"],
    "Tin tức thị trường ngành nhựa": ["giá hạt nhựa mới nhất", "xu hướng ngành nhựa Việt Nam", "thị trường nhựa tái chế", "quy định EPR ngành nhựa"],
    "Tổng quan về nhựa": ["cách nhận biết từng loại nhựa", "nhiệt độ gia công các loại nhựa", "chọn máy theo vật liệu PP PE PET", "quy trình tái chế nhựa công nghiệp"],
    "Dịch vụ bảo trì, bảo dưỡng, sửa chữa": ["báo giá bảo trì máy ngành nhựa", "hợp đồng bảo trì nhà máy nhựa", "sửa máy ngành nhựa tại nhà máy", "checklist bảo dưỡng máy phụ trợ"],
    "Tin tức": ["giải pháp tự động hóa nhà máy nhựa", "nâng cấp dây chuyền sản xuất nhựa", "case study tối ưu năng suất nhà máy"],
    "Need Manual Review": ["cần đọc H1, meta description và nội dung trước khi nghiên cứu keyword"],
}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn")).strip()


def read_rows():
    with zipfile.ZipFile(SOURCE) as z:
        root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    rows = []
    for row in root.findall(".//m:row", NS)[1:]:
        d = {}
        for c in row.findall("m:c", NS):
            col = re.match(r"[A-Z]+", c.get("r", "")).group()
            if c.get("t") == "inlineStr":
                val = "".join(t.text or "" for t in c.findall(".//m:t", NS))
            else:
                v = c.find("m:v", NS)
                val = v.text if v is not None else ""
            d[col] = val
        rows.append({"url": d.get("A", ""), "title": d.get("C", ""), "indexability": d.get("F", "")})
    return rows


STATIC = {"", "tin-tuc", "gioi-thieu", "lien-he", "faq", "du-an-da-hoan-thanh", "may-moc-phu-tro-nganh-nhua", "linh-kien-nganh-nhua", "canh-tay-robot", "chiller-cong-nghiep", "phoi-chai-pet", "ban-thao-tac-cong-nghiep", "may-cham-keo-pvc-tu-dong"}


def is_blog(row):
    u = row["url"]
    if not u or "/san-pham/" in u or "/du-an/" in u or "/page/" in u:
        return False
    path = re.sub(r"https?://[^/]+/?", "", u).strip("/")
    if path in STATIC or path.startswith("may-moc-phu-tro-nganh-nhua/") or path.startswith("linh-kien-nganh-nhua/"):
        return False
    return True


def contains(t, *terms):
    return any(fold(x) in t for x in terms)


def classify(title, url):
    t = fold(title + " " + url)
    if contains(t, "dich vu", "nhan sua", "bao gia sua", "hop dong bao tri", "bao tri bao duong sua chua"):
        cat = "Dịch vụ bảo trì, bảo dưỡng, sửa chữa"
    elif contains(t, "hong ngoai fir", "gia nhiet fir", "far infrared"):
        cat = "Cụm gia nhiệt hồng ngoại FIR"
    elif contains(t, "cham keo pvc", "nho giot pvc", "nhan mac pvc", "logo pvc", "moc khoa pvc", "de giay pvc", "keo pvc"):
        cat = "Máy chấm keo PVC sản xuất nhãn mác, đế giày"
    elif contains(t, "canh tay robot", "robot gap", "robot may ep", "robot cong nghiep", "tu dong hoa"):
        cat = "Cánh tay robot"
    elif contains(t, "chiller", "thap giai nhiet", "giai nhiet gio", "giai nhiet nuoc", "lam lanh khuon", "he thong lam lanh"):
        cat = "Chiller giải nhiệt gió và chiller giải nhiệt nước"
    elif contains(t, "may bam", "may nghien", "may xay nhua", "dao may bam", "dao nghien", "bam nghien"):
        cat = "Máy băm, nghiền nhựa"
    elif contains(t, "bang tai pvc", "day bang tai", "bang tai nhua", "bang tai cong nghiep", "bang tai"):
        cat = "Băng tải PVC"
    elif contains(t, "may hut lieu", "hut lieu", "cap lieu", "pheu hut", "van hut", "bom hut lieu"):
        cat = "Máy hút liệu"
    elif contains(t, "may say", "pheu say", "tu say", "say nhua", "say hat", "hut am", "do am hat nhua"):
        cat = "Máy sấy nhựa"
    elif contains(t, "may tron", "tron nhua", "tron hat", "tron mau", "phoi tron", "sai lech ty le mau"):
        cat = "Máy trộn nhựa"
    elif contains(t, "sang rung", "luoi sang", "may sang", "phan loai hat"):
        cat = "Sàng rung công nghiệp"
    elif contains(t, "nhiet do khuon", "may gia nhiet", "bo gia nhiet", "gia nhiet khuon", "dieu nhiet khuon", "kiem soat nhiet do"):
        cat = "Máy gia nhiệt"
    elif contains(t, "gia hat nhua", "thi truong nhua", "xuat nhap khau nhua", "hoi cho", "trien lam", "chinh sach", "epr", "xu huong nganh nhua", "kinh doanh nganh nhua"):
        cat = "Tin tức thị trường ngành nhựa"
    elif contains(t, "nhua la gi", "hat nhua", "nhua nguyen sinh", "nhua tai sinh", "nhua tai che", "phe lieu nhua", "polymer", "nhua pvc", "nhua pp", "nhua pe", "nhua pet", "nhua abs", "nhua pc", "khuon ep nhua", "ep phun nhua", "quy trinh san xuat nhua"):
        cat = "Tổng quan về nhựa"
    elif contains(t, "trung nguyen tnt", "nha may nhua", "nganh nhua", "may moc cong nghiep"):
        cat = "Tin tức"
    else:
        cat = "Need Manual Review"

    confidence = "High" if cat not in {"Tin tức", "Need Manual Review"} else ("Medium" if cat == "Tin tức" else "Manual Review")
    intent = "Transactional" if contains(t, "bao gia", "mua", "dia chi", "nha cung cap", "dich vu", "sua chua") else ("Commercial Investigation" if contains(t, "so sanh", "top", "nen", "lua chon", "cach chon", "co nen", "gia ") else "Informational")
    action = "Cần kiểm tra thủ công" if cat == "Need Manual Review" else ("Tối ưu lại intent" if cat == "Tin tức" else "Bổ sung internal link")
    page_opp = "Đọc nội dung và tạo bài bổ trợ theo intent" if cat == "Need Manual Review" else f"Bài hỗ trợ: {OPPS[cat][0]}"
    internal = "Need Manual Review" if cat == "Need Manual Review" else f"Bài viết → {CATS[cat][2]} → landing page"
    cannibal = "Rà soát bài cùng cluster và hợp nhất nếu trùng intent" if cat != "Need Manual Review" else "Chưa đánh giá được khi thiếu nội dung"
    reason = ("Title/URL không cung cấp đủ tín hiệu để khớp chắc chắn với 14 category được phép." if cat == "Need Manual Review" else f"Chủ đề trung tâm và thực thể chính khớp trực tiếp với phạm vi của category {cat}.")
    return cat, confidence, intent, action, reason, page_opp, internal, cannibal


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def main():
    all_rows = read_rows()
    rows = [r for r in all_rows if is_blog(r)]
    results = []
    grouped = defaultdict(list)
    for r in rows:
        cat, conf, intent, action, reason, page_opp, internal, cannibal = classify(r["title"], r["url"])
        slug, topic, product, landing = CATS[cat]
        item = {**r, "cat": cat, "slug": slug, "topic": topic, "intent": intent, "confidence": conf, "reason": reason, "product": product, "landing": landing, "opps": "; ".join(OPPS[cat][:4]), "page_opp": page_opp, "internal": internal, "cannibal": cannibal, "action": action}
        results.append(item)
        grouped[cat].append(item)

    OUT.mkdir(parents=True, exist_ok=True)
    report = ["# Phân loại bài viết Trung Nguyên TNT", "", f"Nguồn: `{SOURCE}` · Tổng bài blog nhận diện: **{len(results)}**.", "", "> Lưu ý: file nguồn chỉ có URL và Title, không có H1/meta/nội dung. Confidence phản ánh giới hạn dữ liệu này.", "", "| URL | Title | Chủ đề chính | Category | Slug | User Intent | Sản phẩm/Dịch vụ liên quan | Keyword Opportunity | Page Opportunity | Internal Link | Cannibalization | Hành động |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in results:
        prod = x["product"] + (f" — {x['landing']}" if x["landing"] else "")
        report.append("| " + " | ".join(esc(v) for v in [x["url"], x["title"], x["topic"], x["cat"], x["slug"], x["intent"], prod, x["opps"], x["page_opp"], x["internal"], x["cannibal"], x["action"]]) + " |")
    (OUT / "01-phan-loai-bai-viet.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    topical = ["# Topical Map và Content Opportunity", "", f"Phân tích từ **{len(results)}** bài blog nhận diện trong `{SOURCE.name}`.", ""]
    for cat in CATS:
        if cat == "Need Manual Review" and not grouped[cat]:
            continue
        items = grouped[cat]
        topical += [f"## {cat}", "", f"- Slug: `{CATS[cat][0] or 'N/A'}`", f"- Số bài hiện có: **{len(items)}**", f"- Topic cluster: {CATS[cat][1]}", f"- Landing page: {CATS[cat][3] or 'Cần xác định sau khi đọc nội dung'}", "", "### Bài viết hiện có", ""]
        topical += [f"- [{x['title']}]({x['url']}) — {x['intent']} / {x['confidence']}" for x in items]
        topical += ["", "### Nội dung còn thiếu và keyword opportunity", ""]
        for i, kw in enumerate(OPPS[cat], 1):
            scores = [5, 5 if i < 3 else 4, 5 if i < 3 else 4, 5, 5, 5 if i < 3 else 4]
            total = sum(scores)
            priority = "A" if total >= 24 else "B" if total >= 18 else "C"
            topical.append(f"- **{kw}** — Product Relevance {scores[0]}/5; Intent {scores[1]}/5; Conversion {scores[2]}/5; Authority {scores[3]}/5; Internal link {scores[4]}/5; Ưu tiên {scores[5]}/5; **Tổng {total}/30 — Priority {priority}**.")
        topical += ["", "### Internal linking", "", f"- Các bài trong cluster nên liên kết chéo theo ngữ cảnh và trỏ về: {CATS[cat][3] or 'landing page phù hợp sau khi review'}.", f"- Anchor ưu tiên: `{CATS[cat][2]}` và biến thể theo vấn đề/công suất/ứng dụng; tránh lặp exact-match trên mọi bài.", ""]
    (OUT / "02-topical-map-content-gap.md").write_text("\n".join(topical) + "\n", encoding="utf-8")

    vault_cat = Path("outputs/trung-nguyen-topical-map-vault/02 - Category")
    vault_cat.mkdir(parents=True, exist_ok=True)
    for cat, meta in CATS.items():
        if cat == "Need Manual Review":
            continue
        slug, topic, product, landing = meta
        items = grouped[cat]
        lines = ["---", "type: topical-map", f'category: "{cat}"', f'slug: "{slug}"', "status: active", "---", "", f"# [[{cat}]]", "", "## Pillar Page", "", f"- Trang hiện có: {landing}", f"- Trang đề xuất: {landing}", "- Search Intent: Informational + Commercial Investigation", f"- Trang sản phẩm/dịch vụ liên quan: {product}", "", "## Existing Content", "", "| Page | Primary Keyword | Intent | Cluster | Product Link |", "|---|---|---|---|---|"]
        for x in items:
            lines.append(f"| [{esc(x['title'])}]({x['url']}) | {esc(x['topic'])} | {x['intent']} | {esc(x['topic'])} | {landing} |")
        opps = OPPS[cat]
        while len(opps) < 4:
            opps = opps + ["Bổ sung nội dung theo intent còn thiếu"]
        lines += ["", "## Topic Clusters", "", "### Cluster: Kiến thức nền", "", f"- Chủ đề: {topic}", "- Trang cần tạo: là gì, cấu tạo, nguyên lý, ứng dụng", "", "### Cluster: Lựa chọn và so sánh", "", f"- Trang cần tạo: {opps[0]}; {opps[1]}", "", "### Cluster: Vận hành và kỹ thuật", "", f"- Trang cần tạo: {opps[2]}", "", "### Cluster: Sự cố và bảo trì", "", f"- Trang cần tạo: {opps[3]}", "", "### Cluster: Giá và mua hàng", "", f"- Landing page: {landing}", "", "## Keyword Opportunities", "", "| Keyword | Intent | Page Type | Product Relevance | Conversion | Total Score | Priority |", "|---|---|---|---:|---:|---:|---|"]
        for i, kw in enumerate(OPPS[cat], 1):
            score = 30 if i < 3 else 27
            lines.append(f"| {kw} | {'Commercial Investigation' if i < 3 else 'Informational'} | Supporting article | 5 | {5 if i < 3 else 4} | {score} | {'A' if score >= 24 else 'B'} |")
        lines += ["", "## Page Opportunities", ""]
        for kw in opps[:2]:
            lines += [f"### [[{kw}]]", "", f"- Primary keyword: {kw}", f"- Category: {cat}", "- Search Intent: Commercial Investigation", "- Funnel Stage: MOFU/BOFU", "- Page Type: Supporting article", "- User Problem: Người mua cần chọn đúng thiết bị/công suất/giải pháp.", f"- Product liên quan: {product}", "- Nội dung cần có: tiêu chí chọn, thông số, so sánh, chi phí, FAQ.", "- CTA: Nhận tư vấn và báo giá", f"- Internal link đến: {landing}", "- Internal link từ: các bài hiện có trong cluster", "- Priority: A", ""]
        lines += ["## Content Gaps", "", "- Chưa đủ coverage cho intent lựa chọn theo công suất và bài báo giá.", "- Cần bổ sung bài lỗi thường gặp, bảo trì và so sánh.", "", "## Cannibalization Risks", "", f"- Có {len(items)} bài cùng cluster; cần rà soát các bài có title gần nhau trước khi xuất bản thêm.", "- Hành động: giữ một bài hub cho mỗi intent, gộp hoặc redirect bài trùng.", "", "## Internal Link Map", "", f"- [[Bài hỗ trợ]] → [[{cat}]]", f"- [[Bài informational]] → {landing}", "- [[Bài lỗi kỹ thuật]] → [[Dịch vụ bảo trì, bảo dưỡng, sửa chữa]]", ""]
        (vault_cat / f"Topical Map - {cat}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    summary = ["category\tcount\thigh\tmedium\tmanual"]
    for cat, items in grouped.items():
        summary.append("\t".join(map(str, [cat, len(items), sum(x["confidence"] == "High" for x in items), sum(x["confidence"] == "Medium" for x in items), sum(x["confidence"] == "Manual Review" for x in items)])))
    (OUT / "summary.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")

    # Import the non-blog URL classes into the Obsidian vault as auditable notes.
    vault_root = Path("outputs/trung-nguyen-topical-map-vault")
    existing_urls = set()
    for note in vault_root.rglob("*.md"):
        try:
            txt = note.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        existing_urls.update(re.findall(r'^url:\s*["\']([^"\']+)', txt, flags=re.M))
    buckets = {"product": [], "category": [], "project": []}
    for r in all_rows:
        u = r["url"]
        if u in existing_urls or "/page/" in u and "/tin-tuc/" not in u and "/may-moc-phu-tro-nganh-nhua/" not in u and "/linh-kien-nganh-nhua/" not in u and "/du-an-da-hoan-thanh/" not in u:
            pass
        if "/san-pham/" in u:
            buckets["product"].append(r)
        elif "/du-an/" in u:
            buckets["project"].append(r)
        elif ("/tin-tuc/" in u or "/may-moc-phu-tro-nganh-nhua/" in u or "/linh-kien-nganh-nhua/" in u) or u.rstrip("/").endswith(("/may-moc-phu-tro-nganh-nhua", "/linh-kien-nganh-nhua", "/canh-tay-robot", "/chiller-cong-nghiep", "/phoi-chai-pet", "/ban-thao-tac-cong-nghiep")):
            buckets["category"].append(r)
    target_dirs = {"product": vault_root / "03 - Product", "category": vault_root / "02 - Category", "project": vault_root / "05 - Project"}
    imported = {}
    for kind, entries in buckets.items():
        target_dirs[kind].mkdir(parents=True, exist_ok=True)
        made = 0
        for r in entries:
            if r["url"] in existing_urls:
                continue
            path_part = re.sub(r"https?://[^/]+/?", "", r["url"]).strip("/")
            slug = re.sub(r"[^a-z0-9]+", "-", fold(path_part)).strip("-") or "trang"
            if "/page/" in r["url"]:
                slug += "-page-" + r["url"].rstrip("/").split("/page/")[-1]
            note_path = target_dirs[kind] / f"{slug}.md"
            n = 2
            while note_path.exists():
                note_path = target_dirs[kind] / f"{slug}-{n}.md"
                n += 1
            page_type = {"product": "product", "category": "category", "project": "project"}[kind]
            note = ["---", f'title: "{r["title"].replace(chr(34), chr(39))}"', f'url: "{r["url"]}"', f"page_type: {page_type}", 'source: "page_titles_all.xlsx"', f'indexability: "{r["indexability"]}"', "status: existing", "---", "", f"# {r['title']}", "", f"- URL: {r['url']}", f"- Loại trang: `{page_type}`", "- Ghi chú: Chưa có H1/meta/nội dung trong file nguồn; cần crawl nội dung để hoàn thiện mapping.", ""]
            note_path.write_text("\n".join(note), encoding="utf-8")
            made += 1
        imported[kind] = {"source": len(entries), "created": made, "existing": len(entries) - made}
    (OUT / "nonblog-import-summary.md").write_text("# Import non-blog vào Obsidian\n\n" + "\n".join(f"- {k}: {v['source']} URL; tạo mới {v['created']}; đã có {v['existing']}" for k, v in imported.items()) + "\n", encoding="utf-8")
    print(f"Wrote {len(results)} rows to {OUT}")


if __name__ == "__main__":
    main()
