import zipfile
import xml.etree.ElementTree as ET
import re

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

# Load raw data
raw_data = read_excel('key matcha.xlsx')
header = raw_data[0]
rows = raw_data[1:]

print(f"Header: {header}")
print(f"Total raw rows: {len(rows)}")

# Exclude list
exclude_terms = [
    'nhat', 'nhật', 'nhât', 'nhap', # Nhật / Nhật Bản
    'dai loan', 'đài loan', 'dai-loan', # Đài Loan
    'cozy',
    'han quoc', 'hàn quốc', 'korea',
    'trung quoc', 'trung quốc',
    'phuc long', 'phúc long', 'phuclong',
    'gongcha', 'gong cha',
    'neicha', 'neichatea',
    'meiko', 'meikotea',
    'matsuyuki', 'matsuba',
    'amiya', 'aiya', 'enso', 'ucc', 'ami', '1 tea', '1tea', 'master', 'king',
    'shopee', 'lazada', 'tiki', 'sendo', 'emart', 'coopmart', 'bachhoaxanh', 'bách hóa xanh', 'winmart', 'vinmart',
    # Beauty / Cosmetics
    'đắp mặt', 'dap mat', 'dưỡng da', 'duong da', 'trị mụn', 'tri mun', 'làm đẹp', 'lam dep', 'tắm trắng', 'tam trang', 'mặt nạ', 'mat na',
]

filtered_rows = []
excluded_count = 0
excluded_sample = []

for row in rows:
    if not row or len(row) < 1:
        continue
    keyword = row[0].strip()
    keyword_lower = keyword.lower()
    
    # Check if keyword contains any excluded terms
    exclude = False
    matched_term = ""
    for term in exclude_terms:
        if term in keyword_lower:
            exclude = True
            matched_term = term
            break
            
    if exclude:
        excluded_count += 1
        if len(excluded_sample) < 15:
            excluded_sample.append((keyword, matched_term))
    else:
        filtered_rows.append(row)

print(f"Filtered rows count: {len(filtered_rows)}")
print(f"Excluded rows count: {excluded_count}")
print(f"Excluded samples: {excluded_sample}")

# Print first 30 filtered keywords
print("\nFirst 30 filtered keywords:")
for i, r in enumerate(filtered_rows[:30]):
    print(f"{i+1}: {r}")
