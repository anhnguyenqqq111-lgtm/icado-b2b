import csv
import re
from collections import defaultdict
from pathlib import Path


INPUT = Path('outputs/goha-gsc-queries-2026-03-08-to-2026-09-08.csv')
OUTPUT = Path('outputs/goha-search-intent-content-groups-2026-03-08-to-2026-09-08.md')
MAPPING_OUTPUT = Path('outputs/goha-search-intent-keyword-mapping-2026-03-08-to-2026-09-08.csv')


GROUPS = [
    ('GOHA và thương hiệu liên quan', 'Brand/Navigational', 'Website', 'goha', ['go ha', 'goha news', 'goha media', 'goha shipping', 'goha mmo']),
    ('Từ điển SEO và digital marketing', 'Informational', 'Quick Answer', 'thuật ngữ SEO', ['thuật ngữ seo', 'digital marketing là gì', 'marketing là gì']),
    ('Bài tổng hợp truy vấn SEO cần làm sạch', 'Operational', 'Data Cleanup', 'kiểm tra và làm sạch query SEO', ['query rác SEO', 'SEO query cleanup', 'search footprint']),
    ('Công cụ SEO và phần mềm SEO', 'Commercial Investigation', 'Selection', 'công cụ seo', ['seo tools', 'phần mềm seo', 'seo software', 'seo tool']),
    ('Google Search Console', 'Informational', 'Instructional', 'hướng dẫn sử dụng Google Search Console', ['google search console', 'gsc là gì', 'đăng ký google search console']),
    ('Nghiên cứu từ khóa', 'Informational', 'Instructional', 'nghiên cứu từ khóa SEO', ['keyword research', 'từ khóa seo', 'search volume', 'long tail keyword']),
    ('Search intent và chiến lược nội dung', 'Informational', 'Detailed Explanation', 'search intent là gì', ['search intent', 'chiến lược nội dung', 'content strategy', 'content marketing']),
    ('SEO on-page, off-page và technical SEO', 'Informational', 'Detailed Explanation', 'technical SEO là gì', ['onpage seo', 'offpage seo', 'technical seo', 'seo on page', 'seo off page']),
    ('Page speed và Core Web Vitals', 'Informational', 'Instructional', 'tối ưu tốc độ website', ['page speed', 'core web vitals', 'web vitals', 'tốc độ website']),
    ('Voice search SEO', 'Informational', 'Detailed Explanation', 'voice search SEO là gì', ['voice search', 'voice search optimization']),
    ('Google Ads và quảng cáo tìm kiếm', 'Commercial Investigation', 'Selection', 'quảng cáo Google là gì', ['google ads', 'quảng cáo google', 'google advertising', 'search ads']),
    ('Social media marketing', 'Informational', 'Detailed Explanation', 'social media marketing là gì', ['social media marketing', 'facebook marketing', 'zalo marketing', 'fanpage']),
    ('Performance marketing', 'Informational', 'Detailed Explanation', 'performance marketing là gì', ['performance marketing', 'ads ecommerce', 'ecommerce ads']),
    ('Thiết kế và tối ưu website', 'Informational', 'Instructional', 'tối ưu website chuẩn SEO', ['thiết kế website', 'website chuẩn seo', 'tối ưu website', 'website design']),
    ('Chăm sóc và bảo trì website', 'Commercial', 'Service Booking', 'dịch vụ chăm sóc website', ['chăm sóc web', 'bảo trì website', 'website maintenance']),
    ('GA4, Analytics và đo lường SEO', 'Informational', 'Instructional', 'Google Analytics cho SEO', ['google analytics', 'ga4', 'analytics seo', 'looker studio']),
    ('Dịch vụ SEO tổng thể', 'Commercial', 'Service Booking', 'dịch vụ seo',
     ['dịch vụ seo ai', 'công ty seo', 'agency seo', 'seo service', 'seo website chuyên nghiệp', 'báo giá seo']),
    ('Dịch vụ SEO Google Maps / Local SEO', 'Commercial', 'Local Discovery', 'dịch vụ seo google map',
     ['dịch vụ seo map', 'seo google map', 'seo google maps', 'local seo service', 'seo địa phương']),
    ('Dịch vụ GEO/AEO cho AI search', 'Commercial', 'Service Booking', 'dịch vụ geo',
     ['dịch vụ aeo', 'dịch vụ geo tphcm', 'geo ai seo expert', 'seo ai agency']),
    ('Dịch vụ marketing theo ngành', 'Commercial', 'Service Booking', 'dịch vụ marketing theo ngành',
     ['dịch vụ marketing logistics', 'dịch vụ marketing giáo dục', 'dịch vụ marketing f&b', 'b2b marketing agency']),
    ('Dịch vụ quảng cáo Google Maps', 'Commercial', 'Service Booking', 'dịch vụ quảng cáo google map',
     ['quảng cáo google map', 'phí dịch vụ quảng cáo google map', 'giá quảng cáo google map']),
    ('SEO là gì và nền tảng SEO', 'Informational', 'Detailed Explanation', 'seo là gì',
     ['seo là gì', 'seo là gì vậy', 'search engine optimization là gì', 'seo basics']),
    ('SEO AI là gì và cách triển khai', 'Informational', 'Detailed Explanation', 'seo ai là gì',
     ['seo ai', 'ai seo', 'seo cho ai', 'seo ai overview', 'seo ai google']),
    ('AEO là gì', 'Informational', 'Detailed Explanation', 'aeo là gì',
     ['aeo', 'answer engine optimization', 'aeo seo']),
    ('GEO là gì', 'Informational', 'Detailed Explanation', 'geo là gì',
     ['geo', 'generative engine optimization', 'geo marketing']),
    ('So sánh SEO, AEO và GEO', 'Commercial Investigation', 'Comparison', 'seo vs geo vs aeo',
     ['aeo vs seo', 'geo vs aeo', 'aeo và seo', 'seo và geo', 'so sánh seo aeo geo']),
    ('Topical authority và topical map', 'Informational', 'Detailed Explanation', 'topical authority là gì',
     ['topical authority', 'topical map là gì', 'topical map seo', 'seo topical map', 'topical mapping']),
    ('Entity SEO và Social Entity', 'Informational', 'Detailed Explanation', 'entity seo là gì',
     ['entity là gì', 'social entity', 'social entity là gì', 'backlink entity là gì', 'dịch vụ entity social']),
    ('Backlink trong SEO', 'Informational', 'Detailed Explanation', 'backlink là gì',
     ['backlink', 'backlink seo là gì', 'backlink trong seo là gì', 'backlinks là gì', 'backlink chất lượng']),
    ('Hướng dẫn xây dựng backlink', 'Informational', 'Instructional', 'xây dựng backlink',
     ['đi backlink', 'đặt backlink', 'backlink như thế nào', 'link building', 'backlink cho website']),
    ('Canonical URL và canonical tag', 'Informational', 'Detailed Explanation', 'canonical là gì',
     ['canonical', 'canonical url là gì', 'canonical tag là gì', 'seo canonical']),
    ('Schema markup cho SEO và AI search', 'Informational', 'Instructional', 'schema markup cho ai search',
     ['schema markup', 'các loại schema', 'faq schema là gì', 'schema seo']),
    ('Hướng dẫn SEO Google Maps', 'Informational', 'Instructional', 'cách seo google map',
     ['hướng dẫn seo google map', 'seo map là gì', 'google maps seo', 'seo google maps']),
    ('Website không lên top Google', 'Informational', 'Instructional', 'website không lên top google',
     ['web không lên top', 'tại sao website không lên top', 'website bị tụt hạng', 'website không có traffic']),
    ('Thuật toán và cập nhật Google', 'Informational', 'Freshness/News', 'thuật toán google là gì',
     ['thuật toán google', 'google cập nhật thuật toán', 'google update thuật toán', 'thuật toán mới nhất của google']),
    ('Xu hướng SEO năm 2026', 'Informational', 'Predictive/Trend', 'xu hướng seo 2026',
     ['seo 2026', 'google seo update 2026', 'xu hướng seo', 'seo trend']),
    ('SEO B2B', 'Informational', 'Detailed Explanation', 'seo b2b là gì',
     ['seo b2b', 'b2b seo', 'b2b content marketing', 'b2b và b2c']),
    ('Marketing logistics', 'Informational', 'Detailed Explanation', 'marketing logistics là gì',
     ['marketing logistics', 'digital marketing in logistics', 'marketing logistic']),
    ('E-commerce và quảng cáo e-commerce', 'Informational', 'Detailed Explanation', 'ecommerce là gì',
     ['ecommerce', 'e-commerce', 'ecommerce advertising', 'ecommerce ads', 'thiết kế website ecommerce']),
    ('SEO social và social entity', 'Informational', 'Instructional', 'seo social là gì',
     ['seo social', 'social seo', 'backlink social', 'seo website bằng social entity']),
    ('SEO YouTube', 'Informational', 'Instructional', 'seo youtube là gì',
     ['seo youtube', 'cách seo youtube', 'seo đề xuất youtube', 'youtube seo agency']),
    ('Vibe coding và WordPress', 'Informational', 'Instructional', 'vibe code wordpress',
     ['wordpress vibe coding', 'vibe coding wordpress', 'tối ưu wordpress cho ai search']),
]


def norm(s):
    s = s.lower().strip()
    s = re.sub(r'\s+', ' ', s)
    return s


def classify(query):
    q = norm(query)
    # Preserve navigational/noise separately; these must not become content pages.
    if q in {'goha', 'goha mmo', 'goha media', 'goha news', 'goha shipping', 'go ha', 'site:goha.vn'}:
        return 'GOHA và thương hiệu liên quan'
    if any(x in q for x in ['tiki ', 'seotraffic.top', 'powered by wordpress', 'submit a question', 'filetype:', 'copyright', 'image>', 'which companies does this snippet']):
        return 'Bài tổng hợp truy vấn SEO cần làm sạch'
    # Comparisons have their own page even if they contain an informational entity.
    if any(x in q for x in [' vs ', ' so sánh ', ' và ', ' hay ', 'versus']):
        if any(x in q for x in ['seo', 'aeo', 'geo', 'b2b', 'b2c']):
            return 'So sánh SEO, AEO và GEO' if any(x in q for x in ['aeo', 'geo']) else 'SEO B2B'
    # Explicit local/service modifiers stay commercial and are not mixed with guides.
    if any(x in q for x in ['quảng cáo google map', 'quảng cáo google maps', 'quảng cáo gmap']):
        return 'Dịch vụ quảng cáo Google Maps'
    if any(x in q for x in ['dịch vụ', 'dich vu', 'công ty ', 'agency', 'báo giá', 'gia dich vu', 'giá dịch vụ', 'phí dịch vụ', 'supplier', 'near me']):
        if 'google map' in q or 'google maps' in q or 'seo map' in q:
            return 'Dịch vụ SEO Google Maps / Local SEO'
        if any(x in q for x in ['geo', 'aeo', 'ai seo', 'seo ai']):
            return 'Dịch vụ GEO/AEO cho AI search'
        if any(x in q for x in ['marketing logistics', 'marketing giáo dục', 'marketing f&b', 'b2b marketing']):
            return 'Dịch vụ marketing theo ngành'
        return 'Dịch vụ SEO tổng thể'
    # Instructional modifiers are separated from definitions.
    if any(x in q for x in ['cách ', 'hướng dẫn', 'làm thế nào', 'như thế nào', 'how to', 'checklist', 'không lên top', 'không có traffic']):
        if 'google map' in q or 'google maps' in q or 'seo map' in q:
            return 'Hướng dẫn SEO Google Maps'
        if 'backlink' in q or 'link building' in q or 'đi link' in q:
            return 'Hướng dẫn xây dựng backlink'
        if 'youtube' in q:
            return 'SEO YouTube'
        if 'wordpress' in q or 'vibe code' in q:
            return 'Vibe coding và WordPress'
        if 'website' in q and any(x in q for x in ['không lên top', 'không có traffic']):
            return 'Website không lên top Google'
    if any(x in q for x in ['cập nhật', 'update', 'mới nhất', 'xu hướng', 'trend', 'năm 2026']):
        return 'Xu hướng SEO năm 2026' if ('2026' in q or 'xu hướng' in q or 'trend' in q) else 'Thuật toán và cập nhật Google'
    # Technical entities must not be absorbed into generic SEO.
    if any(x in q for x in ['search console', 'gsc là gì', 'đăng ký google search console']):
        return 'Google Search Console'
    if any(x in q for x in ['keyword research', 'search volume', 'long tail keyword', 'nghiên cứu từ khóa']):
        return 'Nghiên cứu từ khóa'
    if 'search intent' in q or 'chiến lược nội dung' in q or 'content strategy' in q:
        return 'Search intent và chiến lược nội dung'
    if any(x in q for x in ['onpage seo', 'on-page seo', 'offpage seo', 'off-page seo', 'technical seo']):
        return 'SEO on-page, off-page và technical SEO'
    if any(x in q for x in ['page speed', 'core web vitals', 'web vitals', 'tốc độ website']):
        return 'Page speed và Core Web Vitals'
    if 'voice search' in q:
        return 'Voice search SEO'
    if any(x in q for x in ['google ads', 'quảng cáo google', 'google advertising', 'search ads']):
        return 'Google Ads và quảng cáo tìm kiếm'
    if any(x in q for x in ['social media', 'facebook marketing', 'zalo marketing', 'fanpage']):
        return 'Social media marketing'
    if any(x in q for x in ['performance marketing', 'ads ecommerce', 'ecommerce ads']):
        return 'Performance marketing'
    if any(x in q for x in ['thiết kế website', 'website chuẩn seo', 'tối ưu website', 'website design']):
        return 'Thiết kế và tối ưu website'
    if any(x in q for x in ['chăm sóc web', 'chăm sóc website', 'bảo trì website', 'website maintenance']):
        return 'Chăm sóc và bảo trì website'
    if any(x in q for x in ['google analytics', 'ga4', 'analytics seo', 'looker studio']):
        return 'GA4, Analytics và đo lường SEO'
    if any(x in q for x in ['công cụ seo', 'seo tools', 'phần mềm seo', 'seo software', 'seo tool']):
        return 'Công cụ SEO và phần mềm SEO'
    if 'canonical' in q:
        return 'Canonical URL và canonical tag'
    if 'schema' in q:
        return 'Schema markup cho SEO và AI search'
    if 'backlink' in q or 'link building' in q:
        return 'Backlink trong SEO'
    if 'entity' in q or 'social entity' in q:
        return 'Entity SEO và Social Entity'
    if 'topical' in q:
        return 'Topical authority và topical map'
    if 'seo' in q and any(x in q for x in ['vs', 'aeo', 'geo']):
        return 'So sánh SEO, AEO và GEO'
    if 'aeo' in q:
        return 'AEO là gì'
    if 'geo' in q:
        return 'GEO là gì'
    if 'seo ai' in q or 'ai seo' in q or 'seo cho ai' in q:
        return 'SEO AI là gì và cách triển khai'
    if 'b2b' in q or 'b2c' in q:
        return 'SEO B2B'
    if 'logistics' in q or 'logistic' in q:
        return 'Marketing logistics'
    if 'ecommerce' in q or 'e-commerce' in q:
        return 'E-commerce và quảng cáo e-commerce'
    if 'youtube' in q:
        return 'SEO YouTube'
    if 'wordpress' in q or 'vibe code' in q:
        return 'Vibe coding và WordPress'
    if q == 'seo' or q.startswith('seo ') or 'seo là gì' in q:
        return 'SEO là gì và nền tảng SEO'
    return 'Từ điển SEO và digital marketing'


def main():
    rows = list(csv.DictReader(INPUT.open(encoding='utf-8')))
    grouped = defaultdict(list)
    for row in rows:
        row['intent_group'] = classify(row['query'])
        grouped[row['intent_group']].append(row)
    with MAPPING_OUTPUT.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['query', 'article_group', 'article_idea', 'intent', 'micro_intent', 'clicks', 'impressions', 'ctr', 'position'])
        writer.writeheader()
        meta_by_name = {x[0]: x for x in GROUPS}
        writer.writerows({
            'query': row['query'],
            'article_group': row['intent_group'],
            'article_idea': meta_by_name[row['intent_group']][0],
            'intent': meta_by_name[row['intent_group']][1],
            'micro_intent': meta_by_name[row['intent_group']][2],
            **{k: row[k] for k in ['clicks', 'impressions', 'ctr', 'position']},
        } for row in rows)
    rank = {name: i for i, (name, *_rest) in enumerate(GROUPS)}
    order = sorted(grouped, key=lambda x: (rank.get(x, 999), -sum(int(r['impressions']) for r in grouped[x])))
    def vi(n):
        return f'{n:,}'.replace(',', '.')

    lines = [
        '# GOHA — nhóm bài theo search intent', '',
        '- Website/property: `https://goha.vn/`',
        '- Dữ liệu: GSC query-level, Web, 08/03/2026–08/09/2026',
        '- Nguyên tắc: mỗi bài chỉ có **một macro-intent và một micro-intent chính**; keyword gần nghĩa được gom làm biến thể/H2/FAQ, không tạo bài riêng.',
        '- Mỗi query đều được gán một `article_group`, `article_idea`, macro-intent và micro-intent.',
        '- Với query brand/footprint/rác, idea được ghi nhận để đánh giá đầy đủ nhưng không khuyến nghị xuất bản thành bài SEO độc lập.', '',
        f'- Bảng mapping đầy đủ: [goha-search-intent-keyword-mapping-2026-03-08-to-2026-09-08.csv](goha-search-intent-keyword-mapping-2026-03-08-to-2026-09-08.csv) — mỗi query xuất hiện đúng một lần.', '',
        '## Tóm tắt', '',
        f'- Tổng query đã phân nhóm: **{vi(len(rows))}**',
        f'- Nhóm bài/landing page/idea: **{len(order)}**',
        f'- Query đã được gán bài/idea: **{vi(len(rows))}/{vi(len(rows))}**', '',
        '## Cụm bài viết đề xuất', '',
        '| # | Bài viết/URL intent | Macro-intent | Micro-intent | Keyword chính | Query phụ tiêu biểu | Impressions | Clicks |',
        '|---:|---|---|---|---|---|---:|---:|',
    ]
    n = 0
    for name in order:
        meta = next((x for x in GROUPS if x[0] == name), None)
        if not meta:
            continue
        n += 1
        rows2 = sorted(grouped[name], key=lambda x: int(x['impressions']), reverse=True)
        imps = sum(int(x['impressions']) for x in rows2)
        clicks = sum(int(x['clicks']) for x in rows2)
        examples = '; '.join(x['query'] for x in rows2[:6])
        lines.append(f'| {n} | {meta[0]} | {meta[1]} | {meta[2]} | `{meta[3]}` | {examples} | {vi(imps)} | {vi(clicks)} |')
    lines += ['', '## Quy tắc gom và chống cannibalization', '']
    for name in order:
        if name.startswith('Không tạo bài'):
            continue
        rows2 = sorted(grouped[name], key=lambda x: int(x['impressions']), reverse=True)
        lines.append(f'### {name}')
        lines.append('')
        lines.append('- Chỉ nên dùng một URL chính cho intent này; các query còn lại làm keyword phụ, H2 hoặc FAQ.')
        lines.append('- Toàn bộ query trong cụm:')
        lines.append('')
        for r in rows2:
            lines.append(f"  - `{r['query']}` — {r['impressions']} impressions, {r['clicks']} clicks, vị trí {r['position']}")
        lines.append('')
    lines += ['## Lưu ý khi triển khai', '', '- Nhóm `GOHA và thương hiệu liên quan` phù hợp với trang thương hiệu/landing page, không phải bài blog.', '- Nhóm `Bài tổng hợp truy vấn SEO cần làm sạch` và các query có dấu hiệu footprint/rác chỉ là idea kiểm tra dữ liệu; không nên xuất bản thành bài chỉ để nhắm keyword.', '- Các query còn lại có thể dùng làm keyword chính/phụ, H2 hoặc FAQ trong article group tương ứng.', '']
    for name in order:
        xs = grouped[name]
        if name in {'GOHA và thương hiệu liên quan', 'Bài tổng hợp truy vấn SEO cần làm sạch'}:
            lines.append(f'- **{name}**: {vi(len(xs))} query, {vi(sum(int(x["impressions"]) for x in xs))} impressions. Ví dụ: ' + '; '.join(x['query'] for x in sorted(xs, key=lambda x: int(x['impressions']), reverse=True)[:12]))
    OUTPUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
