#!/usr/bin/env python3
import csv
import json
import re
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

SRC = Path('/Users/t.anh/Downloads/gapicado.xlsx')
OUT = Path('outputs/icado-keyword-clusters')

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def norm(value):
    value = unicodedata.normalize('NFD', str(value or '').lower())
    value = ''.join(c for c in value if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', value.replace('đ', 'd')).strip()


def read_first_sheet(path):
    with zipfile.ZipFile(path) as zf:
        shared = []
        if 'xl/sharedStrings.xml' in zf.namelist():
            root = ET.fromstring(zf.read('xl/sharedStrings.xml'))
            for si in root.findall('m:si', NS):
                shared.append(''.join(t.text or '' for t in si.iterfind('.//m:t', NS)))
        wb = ET.fromstring(zf.read('xl/workbook.xml'))
        rels = ET.fromstring(zf.read('xl/_rels/workbook.xml.rels'))
        relmap = {r.attrib['Id']: r.attrib['Target'] for r in rels}
        sheet = wb.find('m:sheets/m:sheet', NS)
        rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
        target = relmap[rid].lstrip('/')
        if not target.startswith('xl/'):
            target = 'xl/' + target
        root = ET.fromstring(zf.read(target))
        rows = []
        for row in root.findall('.//m:sheetData/m:row', NS):
            vals = {}
            for c in row.findall('m:c', NS):
                ref = c.attrib['r']
                col = re.match(r'[A-Z]+', ref).group()
                typ = c.attrib.get('t')
                v = c.find('m:v', NS)
                inline = c.find('m:is/m:t', NS)
                raw = inline.text if inline is not None else (v.text if v is not None else '')
                if typ == 's' and raw != '':
                    raw = shared[int(raw)]
                elif typ != 'str' and raw != '':
                    try:
                        raw = float(raw)
                        if raw.is_integer(): raw = int(raw)
                    except ValueError:
                        pass
                vals[col] = raw
            rows.append(vals)
        return rows


BRANDS = ['lining', 'li ning', 'yonex', 'mizuno', 'adidas', 'nike', 'puma', 'asics', 'beyono', 'liva', 'decathlon', 'fila', 'lacoste', 'lululemon', 'uniqlo', 'victor', 'kamito', 'joola', 'selkirk', 'head', 'babolat', 'wilson']
HARDWARE = ['vot ', 'vợt ', 'giay ', 'giày ', 'bong ', 'bóng ', 'luoi ', 'lưới ', 'cau long', 'cầu lông', 'bong ban', 'bóng bàn', 'bong ro', 'bóng rổ', 'bong chuyen', 'bóng chuyền', 'giay da bong', 'gậy golf', 'gay golf']
APPAREL = ['ao ', 'áo ', 'quan ', 'quần ', 'do tap', 'đồ tập', 'do the thao', 'đồ thể thao', 'trang phuc', 'trang phục', 'vay ', 'váy ', 'dam ', 'đầm ', 'legging', 'bra ', 'polo', 'short', 'set do', 'set đồ', 'bo do', 'bộ đồ', 'quan ao', 'quần áo', 'outfit', 'athleisure', 'sportswear', 'clothing']

PILLAR_RULES = [
    ('Pickleball', ['pickleball', 'pickle ball', 'pickleplay']),
    ('Gym & Training', ['gym', 'fitness', 'tap ta', 'tập tạ', 'workout', 'training', 'squat', 'deadlift', 'cardio']),
    ('Yoga & Pilates', ['yoga', 'pilates', 'aerobic', 'zumba']),
    ('Tennis & Running', ['tennis', 'tenniscore', 'chay bo', 'chạy bộ', 'running', 'marathon', 'jogging', 'trekking']),
    ('Công nghệ vải & form', ['vai ', 'vải ', 'chat lieu', 'chất liệu', 'polyester', 'spandex', 'nylon', 'cotton', 'co gian', 'co giãn', 'thoat mo hoi', 'thoát mồ hôi', 'khang khuan', 'kháng khuẩn', '4 kim 6 chi', '4 kim 6 chỉ', 'asian fit', 'aero-cool', 'aero-dry', 'form dang', 'form dáng']),
    ('Size, fit & chăm sóc', ['size', 'kich thuoc', 'kích thước', 'vong eo', 'vòng eo', 'vong hong', 'vòng hông', 'beo bung', 'béo bụng', 'map ', 'mập ', 'giat ', 'giặt ', 'bao quan', 'bảo quản', 'khu mui', 'khử mùi', 'nuoc xa', 'nước xả', 'bi hoi', 'bị hôi', 'mui mo hoi', 'mùi mồ hôi']),
    ('Athleisure & outfit', ['phoi do', 'phối đồ', 'outfit', 'athleisure', 'lookbook', 'phong cach', 'phong cách', 'mac dep', 'mặc đẹp', 'xu huong', 'xu hướng', 'capsule wardrobe', 'tenniscore']),
    ('B2B & đại lý', ['nguon si', 'nguồn sỉ', 'lay si', 'lấy sỉ', 'nhap si', 'nhập sỉ', 'si do', 'sỉ đồ', 'si quan', 'sỉ quần', 'si ao', 'sỉ áo', 'gia si', 'giá sỉ', 'nguon hang', 'nguồn hàng', 'dai ly', 'đại lý', 'mo shop', 'mở shop', 'kinh doanh do', 'kinh doanh quần', 'kinh doanh quan', 'kinh doanh ao', 'von mo', 'vốn mở', 'chiet khau', 'chiết khấu', 'ban buon', 'bán buôn', 'xuong may', 'xưởng may']),
]


def contains_any(text, needles):
    n = norm(text)
    return any(re.search(r'(?<!\w)' + re.escape(norm(x)) + r'(?!\w)', n) for x in needles if norm(x))


def choose_pillar(keyword):
    n = norm(keyword)
    hits = [(p, sum(bool(re.search(r'(?<!\w)' + re.escape(norm(x)) + r'(?!\w)', n)) for x in terms)) for p, terms in PILLAR_RULES]
    hits = [(p, s) for p, s in hits if s]
    if not hits:
        return ('Athleisure & outfit', 'Cần review') if contains_any(keyword, APPAREL) else ('Ngoài phạm vi plan', 'Loại')
    hits.sort(key=lambda x: x[1], reverse=True)
    pillar = hits[0][0]
    if pillar in ('Pickleball', 'Gym & Training', 'Yoga & Pilates', 'Tennis & Running') and not contains_any(keyword, APPAREL + ['mac gi', 'mặc gì', 'chat lieu', 'chất liệu', 'size', 'phoi do', 'phối đồ', 'outfit', 'phu kien', 'phụ kiện']):
        return pillar, 'Cần review'
    if pillar == 'Công nghệ vải & form' and not contains_any(keyword, APPAREL + ['the thao', 'thể thao', 'tap ', 'tập ', 'gym', 'yoga', 'pickleball', 'tennis', 'running']):
        return pillar, 'Loại'
    if pillar == 'Size, fit & chăm sóc' and not contains_any(keyword, APPAREL + ['the thao', 'thể thao', 'tap ', 'tập ', 'gym', 'yoga', 'pickleball', 'tennis', 'running']):
        return pillar, 'Loại'
    if pillar == 'Athleisure & outfit' and contains_any(keyword, ['jean', 'sneaker', 'giày', 'giay', 'mũ nồi', 'mu noi']) and not contains_any(keyword, ['đồ thể thao', 'do the thao', 'quần áo thể thao', 'quan ao the thao']):
        return pillar, 'Loại'
    return pillar, 'Giữ'


def choose_cluster(keyword, pillar):
    n = norm(keyword)
    if pillar == 'B2B & đại lý':
        if contains_any(n, ['nguon si','nguồn sỉ','nguon hang','nguồn hàng','lay si','lấy sỉ','nhap si','nhập sỉ','gia si','giá sỉ','xuong','xưởng','ban buon','bán buôn']): return 'Nguồn sỉ / nhà cung cấp'
        if contains_any(n, ['dai ly','đại lý','chinh sach','chính sách','chiet khau','chiết khấu']): return 'Đại lý / chính sách'
        return 'Mở shop / vốn / vận hành'
    patterns = [
        ('Nguồn sỉ / nhà cung cấp', ['nguon si', 'nguồn sỉ', 'nguon hang', 'nguồn hàng', 'xuong', 'xưởng', 'ban buon', 'bán buôn']),
        ('Mở shop / vốn / vận hành', ['mo shop', 'mở shop', 'von ', 'vốn ', 'kinh doanh', 'ton kho', 'tồn kho', 'gia ban', 'giá bán', 'loi nhuan', 'lợi nhuận']),
        ('Đại lý / chính sách', ['dai ly', 'đại lý', 'chinh sach', 'chính sách', 'chiet khau', 'chiết khấu']),
        ('Size và đo cơ thể', ['size', 'kich thuoc', 'kích thước', 'vong eo', 'vòng eo', 'vong hong', 'vòng hông', 'bang size', 'bảng size']),
        ('Giặt, khử mùi và bảo quản', ['giat', 'giặt', 'bao quan', 'bảo quản', 'khu mui', 'khử mùi', 'nuoc xa', 'nước xả', 'bi hoi', 'bị hôi', 'mui mo hoi', 'mùi mồ hôi']),
        ('Chất liệu và hiệu suất vải', ['vai ', 'vải ', 'chat lieu', 'chất liệu', 'polyester', 'spandex', 'nylon', 'cotton', 'co gian', 'co giãn', 'thoat mo hoi', 'thoát mồ hôi', 'khang khuan', 'kháng khuẩn', 'aero-']),
        ('Form dáng / công nghệ may', ['form', 'asian fit', '4 kim 6 chi', '4 kim 6 chỉ', 'duong may', 'đường may']),
        ('Phối đồ / outfit / lookbook', ['phoi do', 'phối đồ', 'outfit', 'lookbook', 'phong cach', 'phong cách', 'mac dep', 'mặc đẹp', 'capsule']),
        ('Xu hướng / Athleisure', ['athleisure', 'xu huong', 'xu hướng', 'tenniscore', 'mau do', 'màu đồ']),
        ('Chọn đồ nữ', [' nu', ' nữ', 'legging', 'bra', 'chan vay', 'chân váy', 'dam ', 'đầm ']),
        ('Chọn đồ nam', [' nam', 'nam ', 'quan short', 'quần short']),
        ('So sánh lựa chọn', ['hay ', 'hay là', 'khac ', 'khác ', 'so sanh', 'so sánh', 'nen chon', 'nên chọn']),
        ('Mặc gì / hướng dẫn chọn đồ', ['mac gi', 'mặc gì', 'chon do', 'chọn đồ', 'trang phuc', 'trang phục', 'do tap', 'đồ tập', 'quan ao', 'quần áo']),
        ('Phụ kiện trang phục', ['phu kien', 'phụ kiện', 'bang do', 'băng đô', 'vo ', 'vớ ', 'tat ', 'tất ']),
    ]
    for label, terms in patterns:
        if contains_any(n, terms): return label
    return {'Pickleball':'Kiến thức Pickleball hỗ trợ chọn đồ','Gym & Training':'Kiến thức Gym hỗ trợ chọn đồ','Yoga & Pilates':'Kiến thức Yoga/Pilates hỗ trợ chọn đồ','Tennis & Running':'Kiến thức Tennis/Running hỗ trợ chọn đồ','Công nghệ vải & form':'Kiến thức vật liệu thể thao','Size, fit & chăm sóc':'Fit và chăm sóc chung','Athleisure & outfit':'Trang phục thể thao ứng dụng','B2B & đại lý':'Kinh doanh đồ thể thao'}.get(pillar, 'Ngoài phạm vi')


def refined_intent(keyword, source_intent, cluster):
    n = norm(keyword)
    if cluster in ('Nguồn sỉ / nhà cung cấp', 'Đại lý / chính sách'): return 'B2B Lead Generation'
    if cluster == 'Mở shop / vốn / vận hành': return 'B2B Informational'
    if cluster == 'Size và đo cơ thể': return 'Size / Conversion support'
    if cluster == 'Giặt, khử mùi và bảo quản': return 'Care / Informational'
    if cluster in ('Phối đồ / outfit / lookbook', 'Xu hướng / Athleisure'): return 'Inspiration'
    if cluster == 'So sánh lựa chọn' or any(x in n for x in ['khac nhau', 'so sanh', 'hay ']): return 'Comparison'
    if any(x in n for x in ['gia ', 'mua ', 'ban ', 'chinh hang', 'shop ', 'o dau', 'ở đâu']): return 'Transactional'
    if any(x in n for x in ['la gi', 'là gì', 'tai sao', 'tại sao', 'cach ', 'cách ', 'co nen', 'có nên']): return 'Informational'
    if 'Commercial' in str(source_intent) or 'Transactional' in str(source_intent): return 'Commercial investigation'
    return 'Informational'


def main():
    rows = read_first_sheet(SRC)
    headers = {k: str(v) for k, v in rows[0].items()}
    out_rows = []
    seen = set()
    for r in rows[1:]:
        kw = str(r.get('A', '')).strip()
        if not kw or norm(kw) in seen: continue
        seen.add(norm(kw))
        pillar, decision = choose_pillar(kw)
        if contains_any(kw, BRANDS) and 'icado' not in norm(kw): decision = 'Loại'
        if contains_any(kw, HARDWARE) and not contains_any(kw, APPAREL): decision = 'Loại'
        low = kw.casefold()
        if any(x in low for x in ['vợt', 'giày', 'shoes', 'quấn cán', 'bóng bàn', 'cầu lông', 'bóng chuyền', 'bóng rổ']): decision = 'Loại'
        cluster = choose_cluster(kw, pillar)
        intent = refined_intent(kw, r.get('B', ''), cluster)
        volume = r.get('C', 0) or 0
        kd = r.get('D', 0) or 0
        priority = 'P0' if decision == 'Giữ' and volume >= 1000 and kd <= 45 else ('P1' if decision == 'Giữ' and volume >= 200 else ('P2' if decision == 'Giữ' else '—'))
        out_rows.append({
            'Keyword': kw, 'Intent nguồn': r.get('B',''), 'Volume': volume, 'KD': kd,
            'CPC': r.get('E',''), 'ICADO rank': r.get('G',''), 'ICADO page': r.get('K',''),
            'Quyết định': decision, 'Pillar': pillar, 'Cụm LSI / Search intent': cluster,
            'Intent chuẩn hóa': intent, 'Ưu tiên': priority,
        })
    out_rows.sort(key=lambda x: ({'Giữ':0,'Cần review':1,'Loại':2}[x['Quyết định']], x['Pillar'], x['Cụm LSI / Search intent'], -float(x['Volume'] or 0)))
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(out_rows[0])
    with (OUT/'icado_keyword_classification.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(out_rows)
    summary = defaultdict(lambda: {'keywords':0,'review':0,'volume':0,'review_volume':0,'clusters':Counter()})
    for x in out_rows:
        if x['Quyết định'] in ('Giữ','Cần review'):
            s=summary[x['Pillar']]
            if x['Quyết định']=='Giữ': s['keywords']+=1; s['volume']+=float(x['Volume'] or 0)
            else: s['review']+=1; s['review_volume']+=float(x['Volume'] or 0)
            s['clusters'][x['Cụm LSI / Search intent']]+=1
    with (OUT/'icado_pillar_summary.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['Pillar','Keyword giữ','Volume giữ','Keyword cần review','Volume cần review','Số cụm LSI'])
        for p,s in sorted(summary.items(), key=lambda kv:-(kv[1]['volume']+kv[1]['review_volume'])): w.writerow([p,s['keywords'],int(s['volume']),s['review'],int(s['review_volume']),len(s['clusters'])])
    with (OUT/'icado_lsi_clusters.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['Pillar','Cụm LSI / Search intent','Keyword giữ','Keyword cần review','Tổng volume ứng viên','Keyword chính','Keyword phụ'])
        groups=defaultdict(list)
        for x in out_rows:
            if x['Quyết định']!='Loại': groups[(x['Pillar'],x['Cụm LSI / Search intent'])].append(x)
        for (p,c),items in sorted(groups.items()):
            items.sort(key=lambda x:({'Giữ':0,'Cần review':1}[x['Quyết định']],-float(x['Volume'] or 0)))
            w.writerow([p,c,sum(x['Quyết định']=='Giữ' for x in items),sum(x['Quyết định']=='Cần review' for x in items),int(sum(float(x['Volume'] or 0) for x in items)),items[0]['Keyword'],' | '.join(x['Keyword'] for x in items[1:16])])
    audit={'source_rows':len(rows)-1,'unique_keywords':len(out_rows),'decisions':Counter(x['Quyết định'] for x in out_rows),'pillars':{p:{'keep':s['keywords'],'keep_volume':int(s['volume']),'review':s['review'],'review_volume':int(s['review_volume']),'clusters':dict(s['clusters'])} for p,s in summary.items()}}
    (OUT/'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
