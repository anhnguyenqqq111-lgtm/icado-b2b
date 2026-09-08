import copy, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from filter_seo_keywords import classify, NS, SRC

TMP=SRC.with_name(SRC.stem+' - patched.tmp.xlsx')

def inline_cell(ref, value):
    c=ET.Element(f'{{{NS}}}c', {'r':ref, 't':'inlineStr'})
    isel=ET.SubElement(c,f'{{{NS}}}is'); t=ET.SubElement(isel,f'{{{NS}}}t'); t.text=value
    return c

with zipfile.ZipFile(SRC,'r') as zin:
    ss=ET.fromstring(zin.read('xl/sharedStrings.xml'))
    strings=[''.join(t.itertext()) for t in ss.findall(f'.//{{{NS}}}si')]
    root=ET.fromstring(zin.read('xl/worksheets/sheet1.xml'))
    for row in root.findall(f'.//{{{NS}}}sheetData/{{{NS}}}row'):
        rn=int(row.attrib['r'])
        if rn<=1600: continue
        kwcell=row.find(f"{{{NS}}}c[@r='A{rn}']")
        if kwcell is None: continue
        v=kwcell.find(f'{{{NS}}}v')
        if v is None: continue
        kw=strings[int(v.text)] if kwcell.attrib.get('t')=='s' else (v.text or '')
        result=classify(kw)
        vals=['LOẠI','','',''] if not result else list(result)
        for col,val in zip('GHIJ',vals):
            if row.find(f"{{{NS}}}c[@r='{col}{rn}']") is None:
                row.append(inline_cell(f'{col}{rn}',val))
    sheet_xml=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(TMP,'w',zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            zout.writestr(item, sheet_xml if item.filename=='xl/worksheets/sheet1.xml' else zin.read(item.filename))
TMP.replace(SRC)
print('patched rows 1601-1720')
