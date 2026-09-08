from __future__ import annotations

import collections
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = ROOT.parent.parent
DATA = json.loads((ROOT / "gsc-url-research.json").read_text(encoding="utf-8"))
OUT_DIR = WORKSPACE_ROOT / "outputs" / "icado-gsc-action-plan"
OUT = OUT_DIR / "ICADO-GSC-1000-URL-Action-Plan.xlsx"


def col_letter(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def cell(ref: str, value, style: int = 0) -> str:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{ref}" s="{style}"><v>{value}</v></c>'
    text = "" if value is None else str(value)
    return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{escape(text)}</t></is></c>'


def worksheet(rows, widths, freeze="A2", auto_filter=True, row_styles=None):
    max_col = max((len(r) for r in rows), default=1)
    max_row = len(rows)
    sheet_rows = []
    for ri, row in enumerate(rows, 1):
        cells = []
        for ci, value in enumerate(row, 1):
            style = 1 if ri == 1 else 2
            if row_styles and ri > 1:
                style = row_styles.get(str(row[0]), 2)
            cells.append(cell(f"{col_letter(ci)}{ri}", value, style))
        height = ' ht="34" customHeight="1"' if ri == 1 else ''
        sheet_rows.append(f'<row r="{ri}"{height}>{"".join(cells)}</row>')
    cols = "".join(f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths, 1))
    pane = f'<pane ySplit="1" topLeftCell="{freeze}" activePane="bottomLeft" state="frozen"/>' if freeze else ""
    filt = f'<autoFilter ref="A1:{col_letter(max_col)}{max_row}"/>' if auto_filter and max_row else ""
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetViews><sheetView workbookViewId="0">{pane}</sheetView></sheetViews>
  <sheetFormatPr defaultRowHeight="18"/>
  <cols>{cols}</cols>
  <sheetData>{''.join(sheet_rows)}</sheetData>
  {filt}
  <pageMargins left="0.25" right="0.25" top="0.5" bottom="0.5" header="0.2" footer="0.2"/>
</worksheet>'''


def build():
    rows = DATA["rows"]
    current = DATA["current_urls"]
    actions = collections.Counter(r["recommended_action"] for r in rows)
    groups = collections.Counter(r["group"] for r in rows)
    statuses = collections.Counter(r["live_status"] for r in rows)
    summary = [
        ["ICADO – GSC 1.000 URL Action Plan", "Giá trị", "Ghi chú"],
        ["Ngày kiểm tra", "2026-08-15", "Đối chiếu trực tiếp icado.vn và dữ liệu crawl/sitemap hiện có"],
        ["URL mẫu GSC", len(rows), "Sheet URL Action Plan"],
        ["URL indexable đã crawl", len(current), "Sheet Current Indexable"],
        ["Live HTTP 404", statuses[404], "Đa số có thể giữ 404 nếu không có trang thay thế"],
        ["Live HTTP 200", statuses[200], "Bao gồm trang thật, archive và soft 404"],
        ["Soft 404 'Shop unavailable'", sum(r["live_title"] == "Shop unavailable" for r in rows), "Phải đổi từ 200 sang 404/410"],
        ["URL có target đề xuất", sum(bool(r["target_url"]) for r in rows), "301/redirect/giữ URL"],
        [],
        ["Phân bổ hành động", "Số URL", "Ý nghĩa"],
    ]
    action_notes = {
        "KEEP_404": "Giữ HTTP 404; không redirect về trang chủ",
        "FIX_SOFT_404_TO_410": "Sửa phản hồi 200 lỗi thành 410/404 thật",
        "REMOVE_AND_RETURN_410": "Xóa archive/block mỏng và trả 410",
        "KEEP_200_OPTIMIZE": "Giữ nội dung thật, sửa canonical/internal link/content",
        "KEEP_200_NO_SITEMAP": "Giữ phân trang hoạt động nhưng không cho vào sitemap",
        "KEEP_REDIRECT": "Giữ redirect liên quan; xác nhận 301/308",
        "KEEP_UTILITY_NO_INDEX": "Giữ route chức năng, không lập chỉ mục",
        "IGNORE_STATIC_ASSET": "Tài nguyên tĩnh; không cần hành động index",
        "NOINDEX_CANONICAL": "URL tham số: noindex và canonical",
        "301": "Redirect chính xác tới URL mới",
        "301_REVIEW": "Duyệt thủ công SKU/chủ đề trước khi bật 301",
        "KEEP_200": "URL đã thuộc tập indexable hiện tại",
        "MANUAL_REVIEW_200": "Trang 200 chưa khớp dữ liệu hiện tại; kiểm tra thủ công",
    }
    for action, count in actions.most_common():
        summary.append([action, count, action_notes.get(action, "")])
    summary += [[], ["Nhóm URL", "Số URL", "Ưu tiên"]]
    for group, count in groups.most_common():
        priority = "P1" if group in {"legacy_product", "theme_block"} else "P2" if group in {"tag", "product_tag", "legacy_category"} else "P3"
        summary.append([group, count, priority])

    headers = ["ID", "Old URL", "Last crawled (GSC)", "Group", "Live status", "Live final URL", "Live title", "Live robots", "Recommended action", "Target URL", "Confidence", "Reason", "Best candidate", "Candidate score", "Candidate title", "Implementation status", "Owner", "Notes", "Checked at", "Research sources"]
    plan = [headers]
    for i, r in enumerate(rows, 1):
        plan.append([
            i, r["url"], r["last_crawled"], r["group"], r["live_status"], r["live_final_url"], r["live_title"], r["live_robots"],
            r["recommended_action"], r["target_url"], r["confidence"], r["reason"], r["best_candidate"], r["candidate_score"], r["candidate_title"],
            "Pending", "", "", "2026-08-15", "GSC export; live HTTP check; tools/icado-sitemap-audit/url-audit.csv"
        ])

    current_rows = [["URL", "Type", "HTTP status", "Canonical", "Title", "Description", "H1 count", "Word count", "Source"]]
    for r in current:
        current_rows.append([r["url"], r["type"], r["status"], r["canonical"], r["title"], r["description"], r["h1_count"], r["word_count"], "tools/icado-sitemap-audit/url-audit.csv"])

    rules = [
        ["Rule", "When", "Action", "Do not do"],
        ["Relevant replacement", "Old URL has same product/article/category", "301/308 one-to-one", "Do not redirect unrelated URLs to homepage"],
        ["Removed permanently", "No equivalent new URL", "Keep 404 or return 410", "Do not robots-block before Google sees 404/410"],
        ["Soft 404", "HTTP 200 with error/Shop unavailable", "Return real 404/410", "Do not keep HTTP 200"],
        ["Thin archive", "Tag/author/block with no search value", "Remove internal links/sitemap; 410", "Do not mass-index archives"],
        ["Functional utility", "API, locale switch, account/cart", "Keep functional; no sitemap; noindex/robots as appropriate", "robots.txt is not security"],
        ["Static assets", "CSS/JS/font under /_next/static", "Allow rendering; exclude from sitemap", "Do not block all /_next/"],
        ["Sources", "Google documentation", "https://developers.google.com/search/docs/crawling-indexing/robots/intro", ""],
        ["Sources", "Google documentation", "https://developers.google.com/search/docs/crawling-indexing/block-indexing", ""],
        ["Sources", "Google documentation", "https://developers.google.com/crawling/docs/troubleshooting/http-status-codes", ""],
    ]

    sheets = [
        ("Executive Summary", worksheet(summary, [38, 18, 72], freeze="A2", auto_filter=False)),
        ("URL Action Plan", worksheet(plan, [8, 55, 22, 20, 12, 55, 48, 18, 27, 55, 14, 72, 55, 15, 48, 20, 18, 35, 16, 55])),
        ("Current Indexable", worksheet(current_rows, [55, 18, 12, 55, 48, 65, 12, 14, 40])),
        ("Decision Rules", worksheet(rules, [26, 55, 70, 55], freeze="A2", auto_filter=False)),
    ]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>' + ''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(sheets)+1)) + '</Types>')
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><bookViews><workbookView/></bookViews><sheets>' + ''.join(f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>' for i,(name,_) in enumerate(sheets,1)) + '</sheets><calcPr calcId="191029" fullCalcOnLoad="1"/></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,len(sheets)+1)) + f'<Relationship Id="rId{len(sheets)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
        z.writestr("xl/styles.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="10"/><name val="Aptos"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="10"/><name val="Aptos Display"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF17365D"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>''')
        for i, (_, xml) in enumerate(sheets, 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", xml)
    print(OUT)


if __name__ == "__main__":
    build()
