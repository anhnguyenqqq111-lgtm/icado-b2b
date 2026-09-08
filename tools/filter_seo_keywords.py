import copy
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

SRC = Path('/Users/t.anh/Downloads/Keyword Tool Export - Keyword Suggestions - chống thấm.xlsx')
BACKUP = SRC.with_name(SRC.stem + ' - backup-original.xlsx')
TMP = SRC.with_name(SRC.stem + ' - seo-filtered.tmp.xlsx')
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
RNS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKGNS = 'http://schemas.openxmlformats.org/package/2006/relationships'
ET.register_namespace('', NS)
ET.register_namespace('r', RNS)

BRANDS = ['sika', 'kova', 'taiko', 'việt tín', 'viet tín', 'viettel', 'housef', 'house f',
          'xaydungancu', 'an cư', 'tkxdgroup', 'daiphathome', 'daiphathouse', 'megahome',
          'cokhixaydung', 'housedesign', 'housenhome']
NON_SERVICE = ['văn khấn', 'mâm cúng', 'bài cúng', 'cúng sửa', 'ngày tốt', 'mơ thấy',
                'nằm mơ', 'đánh số', 'phong thủy', 'hướng nhà', 'lễ động thổ', 'đám ma']
PRODUCT_ONLY = ['sơn ', 'keo ', 'băng keo', 'màng ', 'lưới ', 'nhựa đường', 'ga chống',
                 'vật liệu', 'phụ gia', 'hóa chất', 'xi măng', 'chất chống', 'tấm chống',
                 'giấy dầu', 'miếng dán', 'cao su chống', 'màng pe', 'màng hdpe']
HCM = ['hcm', 'tp hcm', 'tphcm', 'hồ chí minh', 'ho chi minh', 'sài gòn', 'saigon',
       'thủ đức', 'thu duc', 'quận 1', 'quận 2', 'quận 3', 'quận 4', 'quận 5', 'quận 6',
       'quận 7', 'quận 8', 'quận 9', 'quận 10', 'quận 11', 'quận 12', 'tân bình', 'tân phú',
       'bình thạnh', 'gò vấp', 'phú nhuận', 'bình tân', 'hóc môn', 'củ chi', 'nhà bè',
       'bình chánh', 'dĩ an', 'thuận an', 'bình dương', 'đồng nai']
OTHER_LOC = ['hà nội', 'hải phòng', 'đà nẵng', 'nha trang', 'cần thơ', 'quy nhơn',
             'quảng ninh', 'thanh hóa', 'nghệ an', 'nam định', 'thái nguyên', 'buôn ma thuột',
             'đồng xoài', 'bình phước', 'quảng ngãi', 'vinh', 'hải dương', 'thái bình',
             'phú quốc', 'long an', 'tiền giang', 'bà rịa', 'vũng tàu']


def classify(keyword):
    k = keyword.lower().strip()
    if any(x in k for x in BRANDS + NON_SERVICE):
        return None
    has_hcm = any(x in k for x in HCM)
    if 'chống thấm' in k:
        if any(x in k for x in PRODUCT_ONLY):
            return None
        if any(x in k for x in OTHER_LOC) and not has_hcm:
            return None
        service = 'Chống thấm'
    elif 'xây nhà' in k or 'xây dựng nhà' in k:
        if any(x in k for x in OTHER_LOC) and not has_hcm:
            return None
        service = 'Xây nhà HCM'
    elif 'sửa nhà' in k or 'sửa chữa nhà' in k or 'cải tạo nhà' in k:
        if any(x in k for x in OTHER_LOC) and not has_hcm:
            return None
        service = 'Sửa nhà HCM'
    else:
        return None

    bofu = ['dịch vụ', 'công ty', 'đơn vị', 'thợ', 'thi công', 'nhận', 'báo giá',
            'bảng giá', 'chi phí', 'giá ', 'giá', 'trọn gói', 'uy tín', 'chuyên nghiệp',
            'gọi', 'thuê', 'tư vấn', 'đăng ký']
    tofu = ['là gì', 'cách', 'quy trình', 'nguyên nhân', 'tại sao', 'khi nào', 'hướng dẫn',
            'kinh nghiệm', 'mẫu', 'tiêu chuẩn', 'có nên', 'bao gồm', 'nên', 'ý tưởng']
    if any(x in k for x in bofu):
        funnel = 'BOFU'
    elif any(x in k for x in tofu):
        funnel = 'TOFU'
    else:
        funnel = 'MOFU'

    if service == 'Chống thấm':
        if any(x in k for x in ['sân thượng', 'nhà vệ sinh', 'tường', 'trần', 'mái', 'ban công', 'sàn']):
            cluster = 'Theo hạng mục'
        elif any(x in k for x in ['giá', 'chi phí', 'báo giá', 'đơn giá']):
            cluster = 'Giá và chi phí'
        else:
            cluster = 'Dịch vụ tổng quát'
    elif service == 'Xây nhà HCM':
        if 'trọn gói' in k: cluster = 'Xây nhà trọn gói'
        elif 'cấp 4' in k: cluster = 'Xây nhà cấp 4'
        elif any(x in k for x in ['giá', 'chi phí', 'báo giá', 'đơn giá']): cluster = 'Giá và chi phí'
        else: cluster = 'Dịch vụ tổng quát'
    else:
        if 'trọn gói' in k: cluster = 'Sửa nhà trọn gói'
        elif 'cấp 4' in k: cluster = 'Sửa nhà cấp 4'
        elif any(x in k for x in ['giá', 'chi phí', 'báo giá', 'đơn giá']): cluster = 'Giá và chi phí'
        else: cluster = 'Dịch vụ tổng quát'
    priority = 'Cao' if funnel == 'BOFU' else ('Trung bình' if funnel == 'MOFU' else 'Thấp')
    return service, funnel, cluster, priority


def col_ref(cell_ref):
    return re.sub(r'\d+', '', cell_ref)


def make_cell(ref, value, style=None, numeric=False):
    attrs = {'r': ref}
    if style is not None:
        attrs['s'] = style
    if numeric:
        c = ET.Element(f'{{{NS}}}c', attrs)
        v = ET.SubElement(c, f'{{{NS}}}v')
        v.text = '' if value is None else str(value)
        return c
    c = ET.Element(f'{{{NS}}}c', {**attrs, 't': 'inlineStr'})
    isel = ET.SubElement(c, f'{{{NS}}}is')
    t = ET.SubElement(isel, f'{{{NS}}}t')
    t.text = '' if value is None else str(value)
    return c


def main():
    with zipfile.ZipFile(SRC, 'r') as zin:
        shared = ET.fromstring(zin.read('xl/sharedStrings.xml'))
        strings = [''.join(t.itertext()) for t in shared.findall(f'.//{{{NS}}}si')]
        sheet = ET.fromstring(zin.read('xl/worksheets/sheet1.xml'))
        rows = []
        for row in sheet.findall(f'.//{{{NS}}}sheetData/{{{NS}}}row'):
            cells = {}
            for cell in row.findall(f'{{{NS}}}c'):
                v = cell.find(f'{{{NS}}}v')
                if v is None: continue
                value = v.text or ''
                if cell.attrib.get('t') == 's': value = strings[int(value)]
                cells[col_ref(cell.attrib['r'])] = (value, cell.attrib.get('s'), cell.attrib.get('t') != 's' and cell.attrib.get('t') != 'str')
            if cells.get('A') and cells['A'][0] != 'Keywords':
                result = classify(cells['A'][0])
                if result:
                    rows.append((cells, result))

        out_sheet = ET.Element(f'{{{NS}}}worksheet')
        ET.SubElement(out_sheet, f'{{{NS}}}sheetPr')
        ET.SubElement(out_sheet, f'{{{NS}}}dimension', {'ref': f'A1:J{len(rows)+1}'})
        views = ET.SubElement(out_sheet, f'{{{NS}}}sheetViews')
        ET.SubElement(views, f'{{{NS}}}sheetView', {'workbookViewId': '0'})
        ET.SubElement(out_sheet, f'{{{NS}}}sheetFormatPr', {'defaultRowHeight': '15'})
        data = ET.SubElement(out_sheet, f'{{{NS}}}sheetData')
        headers = ['Keywords', 'Search Volume (Average)', 'Trend', 'Top of Page Bid (Low Range) (INR)', 'Top of Page Bid (High Range) (INR)', 'Competition', 'Dịch vụ', 'Funnel', 'Cụm chủ đề', 'Ưu tiên']
        hrow = ET.SubElement(data, f'{{{NS}}}row', {'r': '1'})
        for i, h in enumerate(headers):
            col = chr(65+i)
            hrow.append(make_cell(f'{col}1', h, '1'))
        for idx, (cells, result) in enumerate(rows, start=2):
            row = ET.SubElement(data, f'{{{NS}}}row', {'r': str(idx)})
            for col in 'ABCDEF':
                if col in cells:
                    value, style, numeric = cells[col]
                    row.append(make_cell(f'{col}{idx}', value, style, numeric and col != 'A'))
            service, funnel, cluster, priority = result
            for col, value in zip('GHIJ', [service, funnel, cluster, priority]):
                row.append(make_cell(f'{col}{idx}', value, '1'))
        ET.SubElement(out_sheet, f'{{{NS}}}autoFilter', {'ref': f'A1:J{len(rows)+1}'})
        ET.SubElement(out_sheet, f'{{{NS}}}sheetProtection', {'selectLockedCells': '0', 'selectUnlockedCells': '0'})
        sheet_xml = ET.tostring(out_sheet, encoding='utf-8', xml_declaration=True)

        wb = ET.fromstring(zin.read('xl/workbook.xml'))
        sheets = wb.find(f'{{{NS}}}sheets')
        sheets.append(ET.Element(f'{{{NS}}}sheet', {'name': 'SEO Filtered', 'sheetId': '2', f'{{{RNS}}}id': 'rId5'}))
        wb_xml = ET.tostring(wb, encoding='utf-8', xml_declaration=True)
        rels = ET.fromstring(zin.read('xl/_rels/workbook.xml.rels'))
        rels.append(ET.Element(f'{{{PKGNS}}}Relationship', {'Id': 'rId5', 'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet', 'Target': 'worksheets/sheet2.xml'}))
        rels_xml = ET.tostring(rels, encoding='utf-8', xml_declaration=True)
        types = ET.fromstring(zin.read('[Content_Types].xml'))
        types.append(ET.Element('{http://schemas.openxmlformats.org/package/2006/content-types}Override', {'PartName': '/xl/worksheets/sheet2.xml', 'ContentType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'}))
        types_xml = ET.tostring(types, encoding='utf-8', xml_declaration=True)

        if not BACKUP.exists(): shutil.copy2(SRC, BACKUP)
        with zipfile.ZipFile(TMP, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                payload = zin.read(item.filename)
                if item.filename == 'xl/workbook.xml': payload = wb_xml
                elif item.filename == 'xl/_rels/workbook.xml.rels': payload = rels_xml
                elif item.filename == '[Content_Types].xml': payload = types_xml
                zout.writestr(item, payload)
            zout.writestr('xl/worksheets/sheet2.xml', sheet_xml)
    TMP.replace(SRC)
    print(f'Kept {len(rows)} keywords in SEO Filtered; original backed up at {BACKUP}')


if __name__ == '__main__':
    main()
