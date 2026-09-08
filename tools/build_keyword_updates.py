import json, sys, zipfile, xml.etree.ElementTree as ET
from filter_seo_keywords import classify, NS, SRC

with zipfile.ZipFile(SRC, 'r') as z:
    ss=ET.fromstring(z.read('xl/sharedStrings.xml'))
    strings=[''.join(t.itertext()) for t in ss.findall(f'.//{{{NS}}}si')]
    root=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    updates=[
        {'cell':'G1','value':'Dịch vụ SEO'},
        {'cell':'H1','value':'Funnel'},
        {'cell':'I1','value':'Cụm chủ đề'},
        {'cell':'J1','value':'Ưu tiên'},
    ]
    for row in root.findall(f'.//{{{NS}}}sheetData/{{{NS}}}row'):
        rn=row.attrib['r']; kw=None
        for c in row.findall(f'{{{NS}}}c'):
            if c.attrib['r'].startswith('A'):
                v=c.find(f'{{{NS}}}v')
                if v is not None:
                    kw=strings[int(v.text)] if c.attrib.get('t')=='s' else (v.text or '')
                break
        if not kw or kw=='Keywords': continue
        result=classify(kw)
        if result:
            service,funnel,cluster,priority=result
            values=[service,funnel,cluster,priority]
        else:
            values=['LOẠI','','','']
        for col,val in zip('GHIJ',values): updates.append({'cell':f'{col}{rn}','value':val})
batch_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
start = batch_index * 80
end = start + 80
print(json.dumps(updates[start:end], ensure_ascii=False))
