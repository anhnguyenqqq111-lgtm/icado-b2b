import zipfile
import xml.etree.ElementTree as ET

def read_excel(file_path):
    with zipfile.ZipFile(file_path, 'r') as z:
        # Get shared strings
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings_xml = z.read('xl/sharedStrings.xml')
            root = ET.fromstring(strings_xml)
            # handle namespaces
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

        # Get sheet data
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

try:
    data = read_excel('key matcha.xlsx')
    print(f"Total rows read: {len(data)}")
    with open('all_keywords.txt', 'w', encoding='utf-8') as f:
        for i, row in enumerate(data):
            f.write(" | ".join([str(x) for x in row]) + "\n")
    print("Done writing to all_keywords.txt")
except Exception as e:
    print("Error:", e)
