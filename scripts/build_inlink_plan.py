import csv
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


SOURCE = Path('/Users/t.anh/Downloads/Bai-viet-Export-2026-August-05-0708/bundle\\/Bai-viet-Export-2026-August-05-0708.csv')
OUT = Path('outputs/heritage-inlink-plan/rows.json')


def normalize(text):
    text = urllib_unquote(text).lower().replace('đ', 'd')
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', ' ', text).strip()


def urllib_unquote(text):
    from urllib.parse import unquote
    return unquote(text or '')


STOP = set(normalize('''va cua cho tai la o ve voi mot nhung cac tu tren trong noi theo qua den day nay
    kham pha trai nghiem hanh trinh diem den du lich viet nam dep net ve mien chuyen dieu ky uc
    giua cung nhin ngam nghe thay mot ngay noi chon dat tro lai''').split())

# Nhóm địa danh bao gồm tỉnh/thành và các điểm đến thường được dùng thay tên tỉnh.
PLACE_GROUPS = {
    'hanoi': 'ha noi ho guom hoan kiem tay ho ba vi son tay duong lam bat trang soc son',
    'hochiminh': 'sai gon ho chi minh can gio cu chi thu duc',
    'hue': 'hue thua thien phu xuan tam giang lang co bach ma',
    'danang': 'da nang son tra ngu hanh son ba na hai van',
    'quangnam': 'quang nam hoi an my son cu lao cham tam ky',
    'quangninh': 'quang ninh ha long yen tu co to van don mong cai bai tu long',
    'ninhbinh': 'ninh binh trang an tam coc bai dinh cuc phuong hoa lu',
    'laocai': 'lao cai sa pa sapa fansipan bat xat y ty bac ha',
    'hagiang': 'ha giang dong van meo vac ma pi leng hoang su phi',
    'dienbien': 'dien bien muong phang a pa chai',
    'sonla': 'son la moc chau ta xua quynh nhai',
    'hoabinh': 'hoa binh mai chau da bac',
    'yenbai': 'yen bai mu cang chai tram tau thac ba',
    'caobang': 'cao bang ban gioc trung khanh pac bo',
    'backan': 'bac kan ba be',
    'langson': 'lang son mau son dong dang',
    'phutho': 'phu tho hung vuong den hung',
    'thanhhoa': 'thanh hoa sam son pu luong lam kinh thanh nha ho',
    'nghean': 'nghe an vinh cua lo nam dan pu mat',
    'hatinh': 'ha tinh thien cam huong son',
    'quangbinh': 'quang binh phong nha ke bang son doong nhat le',
    'quangtri': 'quang tri con co khe sanh vinh moc',
    'quangngai': 'quang ngai ly son sa huynh',
    'binhdinh': 'binh dinh quy nhon ky co eo gio tay son',
    'phuyen': 'phu yen tuy hoa ganh da dia mui dien',
    'khanhhoa': 'khanh hoa nha trang cam ranh van phong hon mun',
    'ninhthuan': 'ninh thuan phan rang vinh hy nui chua',
    'binhthuan': 'binh thuan phan thiet mui ne phu quy',
    'lamdong': 'lam dong da lat bao loc langbiang tuyen lam',
    'daklak': 'dak lak daklak buon ma thuot lak yok don',
    'gialai': 'gia lai pleiku bien ho chu dang ya',
    'kontum': 'kon tum mang den ngoc linh',
    'daknong': 'dak nong ta dung',
    'cantho': 'can tho cai rang phong dien',
    'angiang': 'an giang chau doc bay nui tra su',
    'kiengiang': 'kien giang phu quoc ha tien nam du rach gia',
    'camau': 'ca mau dat mui u minh',
    'baclieu': 'bac lieu',
    'soctrang': 'soc trang',
    'bentre': 'ben tre',
    'tiengiang': 'tien giang my tho cai be',
    'vinhlong': 'vinh long mang thit',
    'dongthap': 'dong thap sa dec tram chim',
    'tayninh': 'tay ninh ba den',
    'vungtau': 'vung tau ba ria con dao ho tram long hai',
    'dongnai': 'dong nai nam cat tien tri an',
    'binhduong': 'binh duong thu dau mot',
    'haiphong': 'hai phong cat ba do son lan ha',
}

THEMES = {
    'bien_dao': 'bien dao vinh bai tam cat song lan bien hoang hon binh minh san ho',
    'nui_trekking': 'nui deo trekking leo nui rung thac hang dong cao nguyen may dinh',
    'di_san_lich_su': 'di san lich su thanh co den chua lang mo hoang cung bao tang chien truong co do',
    'van_hoa_le_hoi': 'van hoa le hoi phong tuc dan toc lang nghe am thuc cho phien tet',
    'sinh_thai': 'sinh thai vuon quoc gia thien nhien rung ngap man chim hoa ho dong vat',
    'do_thi': 'thanh pho pho co kien truc cafe dem pho di bo',
    'nghi_duong': 'resort nghi duong khach san wellness suoi khoang golf',
    'mua_hoa': 'hoa mua xuan sen sung mai dao ban phuong do',
}


def phrase_terms(groups):
    result = {}
    for key, value in groups.items():
        words = normalize(value).split()
        result[key] = set(words) | {' '.join(words[i:i+2]) for i in range(len(words)-1)}
    return result


PLACE_TERMS = phrase_terms(PLACE_GROUPS)
THEME_TERMS = phrase_terms(THEMES)


def features(row):
    text = normalize(f"{row['Title']} {row['Permalink']}")
    words = [w for w in text.split() if len(w) > 2 and w not in STOP and not w.isdigit()]
    grams = words + [' '.join(words[i:i+2]) for i in range(len(words)-1)]
    found_places = {k for k, terms in PLACE_TERMS.items() if any(term in f' {text} ' for term in terms if len(term) > 3)}
    found_themes = {k for k, terms in THEME_TERMS.items() if any(term in f' {text} ' for term in terms if len(term) > 3)}
    return text, Counter(grams), found_places, found_themes


with SOURCE.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))

docs = [features(r) for r in rows]
df = Counter()
for _, counts, _, _ in docs:
    df.update(counts.keys())
n = len(rows)

vectors = []
norms = []
for _, counts, _, _ in docs:
    vec = {t: (1 + math.log(c)) * math.log((n + 1) / (df[t] + 1)) for t, c in counts.items()}
    vectors.append(vec)
    norms.append(math.sqrt(sum(v * v for v in vec.values())) or 1)

place_index = defaultdict(list)
theme_index = defaultdict(list)
for i, (_, _, places, themes) in enumerate(docs):
    for key in places:
        place_index[key].append(i)
    for key in themes:
        theme_index[key].append(i)


def score(i, j):
    vi, vj = vectors[i], vectors[j]
    if len(vi) > len(vj):
        vi, vj = vj, vi
    cosine = sum(v * vj.get(t, 0) for t, v in vi.items()) / (norms[i] * norms[j])
    places_i, places_j = docs[i][2], docs[j][2]
    themes_i, themes_j = docs[i][3], docs[j][3]
    same_place = len(places_i & places_j)
    same_theme = len(themes_i & themes_j)
    return cosine + 1.8 * same_place + 0.55 * same_theme


recommendations = []
for i in range(n):
    candidates = set()
    for key in docs[i][2]:
        candidates.update(place_index[key])
    for key in docs[i][3]:
        candidates.update(theme_index[key])
    # Bổ sung toàn bộ tập để các tiêu đề văn chương vẫn luôn có phương án.
    candidates.update(range(n))
    candidates.discard(i)
    ranked = sorted(candidates, key=lambda j: (-score(i, j), abs(i-j), int(rows[j]['ID'])))
    # Sáu gợi ý tạo dư địa triển khai, nhưng ngưỡng chất lượng bắt buộc là tối thiểu bốn.
    recommendations.append([rows[j]['ID'] for j in ranked[:6]])

output_rows = [['ID', 'Title', 'Permalink', 'Inlink đề xuất']]
for row, recs in zip(rows, recommendations):
    output_rows.append([row['ID'], row['Title'], row['Permalink'], ', '.join(recs)])

assert len(output_rows) == n + 1
assert all(len(x.split(', ')) >= 4 for x in (r[3] for r in output_rows[1:]))
assert all(r[0] not in r[3].split(', ') for r in output_rows[1:])

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(output_rows, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'articles': n, 'min_links': min(len(r[3].split(', ')) for r in output_rows[1:]), 'output': str(OUT)}, ensure_ascii=False))
