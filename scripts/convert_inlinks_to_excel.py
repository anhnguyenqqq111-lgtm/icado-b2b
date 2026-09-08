import os
import re
import zipfile

def parse_heritage_combined_md(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = text.split("## ")
    data = []

    for sec in sections[1:]:
        lines = sec.strip().split("\n")
        title = lines[0].strip()
        source_url = ""
        links = []

        for line in lines:
            line_str = line.strip()
            if line_str.startswith("Nguồn:") or line_str.startswith("- Nguồn:"):
                source_url = line_str.replace("Nguồn:", "").replace("- Nguồn:", "").strip()
            elif "|" in line_str and not line_str.startswith("| Anchor text") and not line_str.startswith("|---"):
                parts = [p.strip() for p in line_str.split("|")[1:-1]]
                if len(parts) >= 2:
                    anchor = parts[0]
                    dest_url = parts[1]
                    if anchor and dest_url and dest_url.startswith("http"):
                        links.append((anchor, dest_url))
        
        # If source_url wasn't found via "Nguồn:", try extracting url from title if title has markdown link
        if not source_url:
            m = re.search(r'\((https?://[^\)]+)\)', title)
            if m:
                source_url = m.group(1)

        if source_url:
            data.append({
                "title": title,
                "source_url": source_url,
                "links": links
            })
    return data

def parse_report_85_md(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = text.split("### ")
    data = []

    for sec in sections[1:]:
        lines = sec.strip().split("\n")
        header = lines[0].strip()
        
        m_source = re.search(r'\[(.*?)\]\((https?://[^\)]+)\)', header)
        if not m_source:
            continue
        title = m_source.group(1)
        source_url = m_source.group(2)
        
        links = []
        for line in lines[1:]:
            line_str = line.strip()
            if "➔" in line_str or "Anchor:" in line_str:
                # e.g.: * https://... ➔ **Anchor:** `...`
                dest_m = re.search(r'(https?://[^\s]+)', line_str)
                anc_m = re.search(r'Anchor:\s*[`"*\s]*(.*?)[`"*\s]*$', line_str)
                if dest_m and anc_m:
                    dest_url = dest_m.group(1)
                    anchor = anc_m.group(1).strip("`* ")
                    links.append((anchor, dest_url))

        data.append({
            "title": title,
            "source_url": source_url,
            "links": links
        })
    return data

def build_xlsx(output_path, sheets_dict):
    """
    sheets_dict = {
        "SheetName": {
            "headers": ["URL Nguồn", "Inlink", "Anchor"],
            "rows": [ [cell1, cell2, cell3], ... ]
        }
    }
    """
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        # 1. Content Types
        override_sheets = ""
        for i in range(1, len(sheets_dict) + 1):
            override_sheets += f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>\n'
        
        content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  {override_sheets}
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""
        z.writestr("[Content_Types].xml", content_types)

        # 2. _rels/.rels
        rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""
        z.writestr("_rels/.rels", rels)

        # 3. xl/_rels/workbook.xml.rels
        sheet_rels = ""
        for i in range(1, len(sheets_dict) + 1):
            sheet_rels += f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>\n'
        sheet_rels += f'<Relationship Id="rId{len(sheets_dict)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>\n'

        wb_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
{sheet_rels}
</Relationships>"""
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)

        # 4. xl/workbook.xml
        sheets_xml = ""
        for i, sheet_name in enumerate(sheets_dict.keys(), 1):
            sheets_xml += f'<sheet name="{sheet_name}" sheetId="{i}" r:id="rId{i}"/>\n'

        workbook = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    {sheets_xml}
  </sheets>
</workbook>"""
        z.writestr("xl/workbook.xml", workbook)

        # 5. xl/styles.xml
        styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFF"/><name val="Calibri"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="1F4E78"/><bgColor indexed="64"/></fill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/></border>
    <border>
      <left style="thin"><color rgb="D9D9D9"/></left>
      <right style="thin"><color rgb="D9D9D9"/></right>
      <top style="thin"><color rgb="D9D9D9"/></top>
      <bottom style="thin"><color rgb="D9D9D9"/></bottom>
    </border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>
  </cellXfs>
</styleSheet>"""
        z.writestr("xl/styles.xml", styles)

        # 6. xl/worksheets/sheet{i}.xml
        for sheet_idx, (sheet_name, content) in enumerate(sheets_dict.items(), 1):
            headers = content["headers"]
            rows = content["rows"]

            sheet_rows = []
            # Header
            h_cells = []
            for col_idx, h in enumerate(headers, 1):
                col_letter = chr(64 + col_idx)
                h_cells.append(f'<c r="{col_letter}1" t="inlineStr" s="1"><is><t>{h}</t></is></c>')
            sheet_rows.append(f'<row r="1" ht="28" customHeight="1">{"".join(h_cells)}</row>')

            # Rows
            for r_idx, row in enumerate(rows, 2):
                cells = []
                for c_idx, val in enumerate(row, 1):
                    col_letter = chr(64 + c_idx)
                    escaped_val = str(val).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    cells.append(f'<c r="{col_letter}{r_idx}" t="inlineStr" s="2"><is><t xml:space="preserve">{escaped_val}</t></is></c>')
                sheet_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')

            sheet_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <cols>
    <col min="1" max="1" width="55" customWidth="1"/>
    <col min="2" max="2" width="70" customWidth="1"/>
    <col min="3" max="3" width="45" customWidth="1"/>
  </cols>
  <sheetData>
    {"".join(sheet_rows)}
  </sheetData>
</worksheet>"""
            z.writestr(f"xl/worksheets/sheet{sheet_idx}.xml", sheet_xml)

def convert_md_to_excel():
    base_dir = "/Users/t.anh/.gemini/antigravity-ide/scratch/goha-seo-main"
    combined_md = os.path.join(base_dir, "heritage-internal-links-combined.md")
    report_85_md = "/Users/t.anh/.gemini/antigravity-ide/scratch/TuanAnh-MKT-Planing/report_85_links_perfect.md"

    # Process heritage-internal-links-combined.md (547 articles)
    if os.path.exists(combined_md):
        data = parse_heritage_combined_md(combined_md)
        print(f"Loaded {len(data)} articles from {combined_md}")

        # Format 1: 3 inlinks grouped per cell (1 row per Source URL)
        rows_grouped = []
        rows_split = []

        for item in data:
            src_url = item["source_url"]
            links = item["links"] # list of (anchor, dest_url)
            
            # Limit to 3 inlinks or take up to 3 inlinks
            top_links = links[:3]

            # Grouped strings
            dest_urls_str = "\n".join([l[1] for l in top_links])
            anchors_str = "\n".join([l[0] for l in top_links])

            rows_grouped.append([src_url, dest_urls_str, anchors_str])

            # Split rows (1 row per inlink)
            for anc, dest in links:
                rows_split.append([src_url, dest, anc])

        sheets = {
            "Inlinks (3 inlink 1 ô)": {
                "headers": ["URL Nguồn", "Inlink", "Anchor"],
                "rows": rows_grouped
            },
            "Inlinks Chi Tiết (Tách Dòng)": {
                "headers": ["URL Nguồn", "Inlink", "Anchor"],
                "rows": rows_split
            }
        }

        output_xlsx = os.path.join(base_dir, "heritage-internal-links-547.xlsx")
        build_xlsx(output_xlsx, sheets)
        print(f"Generated Excel: {output_xlsx}")

        # Also write CSV for convenience
        output_csv = os.path.join(base_dir, "heritage-internal-links-547-grouped.csv")
        with open(output_csv, "w", encoding="utf-8-sig") as f:
            f.write("URL Nguồn,Inlink,Anchor\n")
            for r in rows_grouped:
                u_src = '"' + r[0].replace('"', '""') + '"'
                u_dest = '"' + r[1].replace('"', '""') + '"'
                u_anc = '"' + r[2].replace('"', '""') + '"'
                f.write(f"{u_src},{u_dest},{u_anc}\n")
        print(f"Generated CSV: {output_csv}")

    # Process report_85_links_perfect.md if exists
    if os.path.exists(report_85_md):
        data85 = parse_report_85_md(report_85_md)
        print(f"Loaded {len(data85)} articles from {report_85_md}")

        rows_grouped = []
        rows_split = []

        for item in data85:
            src_url = item["source_url"]
            links = item["links"][:3]
            dest_urls_str = "\n".join([l[1] for l in links])
            anchors_str = "\n".join([l[0] for l in links])

            rows_grouped.append([src_url, dest_urls_str, anchors_str])
            for anc, dest in item["links"]:
                rows_split.append([src_url, dest, anc])

        sheets85 = {
            "Inlinks (3 inlink 1 ô)": {
                "headers": ["URL Nguồn", "Inlink", "Anchor"],
                "rows": rows_grouped
            },
            "Inlinks Chi Tiết (Tách Dòng)": {
                "headers": ["URL Nguồn", "Inlink", "Anchor"],
                "rows": rows_split
            }
        }

        output_xlsx85 = os.path.join("/Users/t.anh/.gemini/antigravity-ide/scratch/TuanAnh-MKT-Planing", "report_85_links_inlinks.xlsx")
        build_xlsx(output_xlsx85, sheets85)
        print(f"Generated Excel: {output_xlsx85}")

if __name__ == "__main__":
    convert_md_to_excel()
