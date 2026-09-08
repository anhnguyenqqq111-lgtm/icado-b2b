import zipfile
import xml.etree.ElementTree as ET

def read_excel(file_path):
    with zipfile.ZipFile(file_path, 'r') as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings_xml = z.read('xl/sharedStrings.xml')
            root = ET.fromstring(strings_xml)
            ns = ''
            if '}' in root.tag:
                ns = root.tag.split('}')[0] + '}'
            for si in root.findall(f'{ns}si'):
                t = si.find(f'{ns}t')
                if t is not None and t.text is not None:
                    strings.append(t.text)
                else:
                    text = "".join([rt.text for rt in si.findall(f'.//{ns}t') if rt.text])
                    strings.append(text)

        sheet_xml = z.read('xl/worksheets/sheet1.xml')
        root = ET.fromstring(sheet_xml)
        ns = ''
        if '}' in root.tag:
            ns = root.tag.split('}')[0] + '}'
        
        data = []
        for row in root.findall(f'.//{ns}row'):
            row_data = []
            for c in row.findall(f'{ns}c'):
                v = c.find(f'{ns}v')
                val = ""
                if v is not None:
                    val = v.text
                    if c.get('t') == 's': # shared string
                        val = strings[int(val)]
                row_data.append(val)
            if any(row_data):
                data.append(row_data)
        
        return data

raw_data = read_excel('key matcha.xlsx')
rows = raw_data[1:]

non_matcha = []
for row in rows:
    if not row: continue
    kw = row[0].strip().lower()
    # check if it contains matcha-related terms
    matcha_related = ['matcha', 'trà', 'tra', 'chè', 'che', 'oolong', 'ô long', 'green', 'hương', 'huong']
    if not any(x in kw for x in matcha_related):
        non_matcha.append(row[0])

print(f"Total non-matcha keywords: {len(non_matcha)}")
print("Samples:")
for x in non_matcha[:30]:
    print(x)
