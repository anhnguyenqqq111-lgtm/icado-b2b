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

# Load raw data
raw_data = read_excel('key matcha.xlsx')
rows = raw_data[1:]

exclude_terms = [
    'nhat', 'nhật', 'nhât', 'nhap',
    'dai loan', 'đài loan', 'dai-loan',
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
    'đắp mặt', 'dap mat', 'dưỡng da', 'duong da', 'trị mụn', 'tri mun', 'làm đẹp', 'lam dep', 'tắm trắng', 'tam trang', 'mặt nạ', 'mat na',
]

groups = {
    'Bột matcha giá sỉ / B2B': [],
    'Mua bột matcha ở đâu': [],
    'Bột matcha nguyên chất': [],
    'Bột matcha - Câu hỏi': [],
    'Pha chế & Ứng dụng F&B': [],
    'Bột matcha khác': []
}

for row in rows:
    if not row or len(row) < 1:
        continue
    keyword = row[0].strip()
    keyword_lower = keyword.lower()
    
    # Check exclude list
    exclude = False
    for term in exclude_terms:
        if term in keyword_lower:
            exclude = True
            break
    if exclude:
        continue
        
    # Classification rules
    # 1. B2B & Wholesale
    b2b_keywords = ['sỉ', 'si', 'cung cấp', 'cung cap', 'nhà phân phối', 'nha phan phoi', 'nhà cung cấp', 'nha cung cap', 
                    'phân phối', 'phan phoi', 'bán buôn', 'ban buon', 'nhập khẩu', 'nhap khau', 'công ty', 'cong ty', 'bán sỉ', 'ban si']
    is_b2b = any(x in keyword_lower for x in b2b_keywords)
    
    # 2. Where to buy
    buy_keywords = ['mua ở đâu', 'mua o dau', 'mua bột', 'mua bot', 'mua matcha', 'địa chỉ', 'dia chi', 'tphcm', 'hà nội', 'ha noi', 
                    'quận', 'quan', 'siêu thị', 'sieu thi', 'cửa hàng', 'cua hang', 'nơi bán', 'noi ban', 'bán bột', 'ban bot', 'bán matcha', 'ban matcha']
    is_buy = any(x in keyword_lower for x in buy_keywords)
    
    # 3. Pure/Quality
    pure_keywords = ['nguyên chất', 'nguyen chat', 'organic', 'cao cấp', 'cao cap', 'xịn', 'xin', 'real', 'nguyên bản', 'uy tín', 'chất lượng', 'chat luong', 'ngon']
    is_pure = any(x in keyword_lower for x in pure_keywords)
    
    # 4. Questions/Benefits
    question_keywords = ['gì', 'gi', 'sao', 'thế nào', 'the nao', 'tác dụng', 'tac dung', 'công dụng', 'cong dung', 'giảm cân', 'giam can', 
                         'calo', 'calories', 'tốt không', 'tot khong', 'caffeine', 'bao nhiêu', 'bao nhieu', 'được không', 'duoc khong', 
                         'tác hại', 'tac hai', 'uống mỗi ngày', 'uong moi ngay', 'hạn sử dụng', 'han su dung', 'bảo quản', 'bao quan', 'lưu ý', 'luu y']
    is_question = any(x in keyword_lower for x in question_keywords)
    
    # 5. Recipe / F&B
    recipe_keywords = ['pha', 'làm bánh', 'lam banh', 'làm kem', 'lam kem', 'trà sữa', 'tra sua', 'đá xay', 'da xay', 'latte', 
                       'công thức', 'cong thuc', 'cách làm', 'cach lam', 'chế biến', 'che bien', 'nấu', 'nau', 'pha chế', 'pha che', 
                       'uống', 'uong', 'ăn', 'an', 'bánh', 'banh', 'kem', 'chè', 'che', 'thạch', 'thach', 'rau câu', 'rau cau', 'pudding', 'sữa', 'sua']
    is_recipe = any(x in keyword_lower for x in recipe_keywords)
    
    if is_b2b:
        groups['Bột matcha giá sỉ / B2B'].append(row)
    elif is_buy:
        groups['Mua bột matcha ở đâu'].append(row)
    elif is_pure:
        groups['Bột matcha nguyên chất'].append(row)
    elif is_question:
        groups['Bột matcha - Câu hỏi'].append(row)
    elif is_recipe:
        groups['Pha chế & Ứng dụng F&B'].append(row)
    else:
        groups['Bột matcha khác'].append(row)

# Print other group items
print("Group 'Bột matcha khác' samples:")
for row in groups['Bột matcha khác'][:100]:
    print(row[0])
