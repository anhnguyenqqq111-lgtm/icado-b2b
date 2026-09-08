import json, zipfile, xml.etree.ElementTree as ET
from filter_seo_keywords import classify, NS, SRC

with zipfile.ZipFile(SRC, 'r') as z:
    ss=ET.fromstring(z.read('xl/sharedStrings.xml'))
    strings=[''.join(t.itertext()) for t in ss.findall(f'.//{{{NS}}}si')]
    root=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    rows=[['Keywords','Search Volume (Average)','Trend','Top of Page Bid (Low Range) (INR)','Top of Page Bid (High Range) (INR)','Competition','Dịch vụ SEO','Funnel','Cụm chủ đề','Ưu tiên']]
    for row in root.findall(f'.//{{{NS}}}sheetData/{{{NS}}}row'):
        cells={}
        for c in row.findall(f'{{{NS}}}c'):
            v=c.find(f'{{{NS}}}v')
            if v is None: continue
            val=v.text or ''
            if c.attrib.get('t')=='s': val=strings[int(val)]
            cells[c.attrib['r'].rstrip('0123456789')]=val
        if not cells.get('A') or cells['A']=='Keywords': continue
        result=classify(cells['A'])
        if not result: continue
        service,funnel,cluster,priority=result
        rows.append([cells.get(c,'') for c in 'ABCDEF']+[service,funnel,cluster,priority])
print(json.dumps(rows, ensure_ascii=False))
