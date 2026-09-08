# Kế hoạch SEO 6 tháng — ICADO

**Phạm vi:** icado.vn  
**Nguồn audit:** `icado.xlsx`, crawl 277 URL.  
**Thời điểm lập kế hoạch:** 02/08/2026

## 1. Tóm tắt điều hành

ICADO có nền tảng để tăng trưởng SEO ở các nhóm sản phẩm Gym, Yoga, Pickleball, Tennis và thời trang thể thao nam/nữ. Tuy nhiên, cần xử lý vệ sinh kỹ thuật và chuẩn hóa các trang doanh thu trước khi mở rộng content.

Ưu tiên 90 ngày đầu:

1. Xử lý URL lỗi/không còn giá trị và các redirect nội bộ.
2. Hoàn chỉnh on-page cho danh mục, trang sản phẩm và các trang đích theo môn thể thao.
3. Xây dựng cụm nội dung có intent mua hàng; liên kết nội bộ về danh mục và sản phẩm.

## 2. Kết quả audit URL

| Hạng mục | Kết quả | Hàm ý SEO |
|---|---:|---|
| Tổng URL crawl | 277 | Bao gồm HTML và tài nguyên tĩnh |
| URL HTML | 231 | Phạm vi cần quản trị index |
| URL HTML indexable | 53 | Tập trung tối ưu trước |
| URL `200 + noindex` | 62 | Nhiều URL trả trang `Not found`; cần 301, 410 hoặc khôi phục |
| Redirect `307` | 115 | Đều thuộc `/api/locale`; cần bỏ khỏi internal links/sitemap crawlable |
| Trang indexable thiếu H1 | 37/53 | Mất tín hiệu topical relevance |
| Trang indexable dưới 300 từ | 40/53 | Thiếu ngữ cảnh để cạnh tranh truy vấn thương mại/thông tin |
| Trang indexable có title trùng | 18 | Giảm khả năng phân biệt intent và CTR |
| Trang indexable có ảnh thiếu alt | 8 | Bỏ lỡ tín hiệu image SEO/accessibility |
| Trang indexable phản hồi trên 400 ms | 8 | Cần kiểm tra Core Web Vitals thực tế |

### Việc cần xử lý ngay

- Lập bảng quyết định cho 62 URL `200 + noindex`:
  - **Có trang/sản phẩm thay thế:** 301 trực tiếp đến URL gần nhất về intent.
  - **Sản phẩm hết vĩnh viễn, không có thay thế:** trả 410 hoặc 404 thực sự; xóa khỏi sitemap, menu và internal links.
  - **Sản phẩm còn bán:** khôi phục nội dung, indexability, canonical và structured data.
- Không để URL `/api/locale?to=en&next=...` xuất hiện trong sitemap XML hoặc link điều hướng crawlable.
- Kiểm tra các đường dẫn `/auth/` có xuất hiện trong index/sitemap; đặt `noindex, follow` nếu không mang intent tìm kiếm.
- Chuẩn hóa title, meta, một H1 duy nhất, breadcrumb và canonical cho toàn bộ category/PDP ưu tiên.

## 3. Nhóm URL ưu tiên

### Nhóm A — Trang doanh thu, xử lý tháng 1–2

- `/pickleball`
- `/gym`
- `/yoga`
- `/do-the-thao`
- `/do-the-thao-nu`
- `/do-the-thao-nam`
- `/tham-tap-yoga`

Mỗi trang cần có: H1 theo intent, title 45–60 ký tự, meta 120–155 ký tự, mô tả danh mục hữu ích 300–500 từ, FAQ, liên kết tới subcategory/PDP, block size/benefit/chất liệu và Breadcrumb schema.

### Nhóm B — Product page, xử lý tháng 2–3

- Các SKU đang index được nhưng mô tả trùng/lỏng.
- Các URL sản phẩm trả `200 + noindex + Not found` như áo polo, legging, bra, quần short, thảm yoga, túi và vớ.

Template PDP cần gồm: mô tả riêng theo sản phẩm, thuộc tính/chất liệu, size chart, hướng dẫn bảo quản, FAQ, review, ảnh có alt mô tả, Product + Offer + Review schema và sản phẩm liên quan theo môn thể thao.

### Nhóm C — Content cũ, xử lý tháng 3–4

Các bài yoga/gym có khoảng 138–151 từ, thiếu H1 hoặc chỉ một internal link cần được làm mới/ghép cụm. Ví dụ: bài tập yoga tại nhà, hít thở yoga, tập gym kết hợp yoga, đồ tập gym nữ kín đáo.

## 4. Nghiên cứu cạnh tranh công khai

Đây là đánh giá về định vị, cấu trúc danh mục và content có thể quan sát công khai; không phải dữ liệu traffic/backlink trả phí.

| Thương hiệu | Điểm quan sát | Hàm ý cho ICADO |
|---|---|---|
| Beyono | Phủ danh mục theo môn: pickleball, bóng chuyền, cầu lông, chạy bộ; có cả sản phẩm và tin tức | ICADO cần rõ hub theo môn và bộ lọc/landing page theo nhu cầu, không chỉ phân loại giới tính |
| Chillax Sport | Định vị pickleball dành riêng cho phụ nữ, kết nối cộng đồng và phong cách sống | ICADO nên khai thác sâu chủ đề Pickleball nữ: outfit, size, chất liệu, sân/CLB, giải đấu |
| TEZO | Mạnh về giá/khuyến mại, breadth thời trang nữ và bài hướng dẫn lựa chọn đồ tập | ICADO nên cạnh tranh bằng chuyên môn môn thể thao, chất liệu, form dáng, review và nội dung sử dụng thực tế thay vì chỉ giảm giá |
| Decathlon/Nike/Adidas/Uniqlo | Dẫn dắt kỳ vọng người dùng về danh mục chuyên biệt, công nghệ vải và lựa chọn theo hoạt động | Trang category/PDP của ICADO phải giải thích lợi ích sản phẩm theo môn, cường độ vận động và điều kiện sử dụng |

Lưu ý: Thegioidotap là hệ thống sở hữu/phân phối ICADO, không coi là đối thủ. Cần quản trị giữa hai website để tránh trùng lặp/cannibalization: phân định vai trò URL, canonical hoặc nội dung khác biệt rõ ràng.

## 5. Chiến lược keyword và content pillar

### Pillar 1: Pickleball

- Intent thương mại: đồ pickleball nữ, đồ pickleball nam, váy pickleball, áo pickleball, quần/váy tennis pickleball, phụ kiện pickleball.
- Intent hỗ trợ mua: mặc gì chơi pickleball, chọn size váy/áo pickleball, vải nào phù hợp chơi pickleball, outfit pickleball nữ.
- Tài sản khác biệt: BST Pickleplay, đối tác sân/CLB và nội dung cộng đồng.

### Pillar 2: Gym & Training

- Intent thương mại: đồ tập gym nữ, áo bra thể thao, legging nữ, áo gym nam, quần short gym nam.
- Intent hỗ trợ mua: cách chọn đồ tập gym theo dáng, size legging, đồ gym nữ kín đáo, chất liệu không lộ/không bí.

### Pillar 3: Yoga

- Intent thương mại: đồ tập yoga nữ, quần yoga, thảm yoga, túi đựng thảm yoga.
- Intent hỗ trợ mua: cách chọn thảm yoga theo độ dày, chọn đồ yoga cho người mới, cách vệ sinh/bảo quản thảm.

### Pillar 4: Tennis & Active lifestyle

- Intent thương mại: đồ tennis nữ/nam, váy thể thao, áo polo thể thao, phụ kiện thể thao.
- Intent hỗ trợ mua: trang phục tennis, phối đồ thể thao đi chơi, cách bảo quản vải thể thao.

### Pillar 5: B2B/đại lý (tách khỏi D2C)

- Intent: sỉ đồ thể thao, nguồn hàng đồ tập, đại lý đồ thể thao, quần áo thể thao giá sỉ.
- Không dùng các bài B2B để điều hướng mạnh vào trang D2C; thiết kế hub và CTA riêng cho khách đại lý.

## 6. Roadmap 6 tháng

| Tháng | Mục tiêu | Công việc | Deliverables |
|---|---|---|---|
| 1 | Làm sạch nền tảng | Cài/kiểm tra GSC, GA4, dashboard; quyết định 301/410/khôi phục cho 62 URL noindex; sitemap/robots/canonical; bỏ locale redirects; audit CWV | Redirect map, sitemap sạch, baseline KPI, backlog kỹ thuật |
| 2 | Tăng chất lượng trang doanh thu | Tối ưu homepage và 7 URL Nhóm A; H1/title/meta; copy category, FAQ, breadcrumb; schema Organization/WebSite/Breadcrumb | 7 landing pages chuẩn on-page, template category |
| 3 | Chuyển hóa PDP & liên kết | Sửa 20 PDP ưu tiên; ảnh alt, Product/Offer schema, size/FAQ/reviews; tạo module related products; internal-link map | 20 PDP hoàn chỉnh, 30+ internal links ngữ cảnh |
| 4 | Xây topical authority | Xuất bản 6 bài content pillar; refresh 2 bài cũ; mỗi bài có CTA theo intent, link về hub/category/PDP | 8 URL content cải thiện/xuất bản, 4 topic clusters |
| 5 | Xây uy tín & local/community | Digital PR/UGC với sân/CLB/HLV; local SEO cho cửa hàng/đại lý; tách hub B2B sỉ; xử lý mention không link | 5–8 referring domains phù hợp, 3 trang local/partner, 1 B2B hub |
| 6 | Tối ưu theo dữ liệu & CRO | GSC query/page review; refresh URL impression cao CTR thấp; test title/meta; tối ưu FAQ/schema; audit conversion journey từ organic | Báo cáo tăng trưởng, danh sách refresh 90 ngày tiếp theo, CRO backlog |

## 7. Lịch content đề xuất

| Tháng | Nội dung | Mục tiêu | URL đích chính |
|---|---|---|---|
| 3 | Cách chọn đồ pickleball nữ theo dáng và cường độ chơi | Commercial investigation | `/pickleball` |
| 3 | Đồ pickleball nam: checklist trang phục, chất liệu và size | Commercial investigation | `/pickleball` |
| 4 | Chọn đồ tập gym nữ: bra, legging, áo và cách chọn size | Commercial investigation | `/gym`, `/do-the-thao-nu` |
| 4 | Đồ yoga cho người mới: chọn trang phục và thảm theo nhu cầu | Commercial investigation | `/yoga`, `/tham-tap-yoga` |
| 4 | Thảm yoga 6mm, 8mm hay 10mm: chọn theo bài tập và thể trạng | Commercial investigation | `/tham-tap-yoga` |
| 5 | Trang phục tennis/pickleball: khác nhau ở đâu, chọn gì cho người mới | Comparison | `/tennis`, `/pickleball` |
| 5 | Cách giặt và bảo quản đồ thể thao để bền form, không mùi | Informational + retention | Category/PDP liên quan |
| 5 | Outfit thể thao nữ: 7 cách phối từ phòng tập đến đi chơi | Inspiration | `/do-the-thao-nu` |

## 8. KPI và cách đo

Chốt số mục tiêu tuyệt đối sau khi có baseline 28 ngày đầu từ GSC/GA4. Mục tiêu định hướng sau 6 tháng:

| Nhóm KPI | Mục tiêu định hướng | Nguồn |
|---|---:|---|
| Organic clicks | +25–35% so với baseline | Google Search Console |
| Organic conversions/revenue | +15% so với baseline | GA4/e-commerce platform |
| Trang category có H1/title/meta chuẩn | 100% URL Nhóm A | Crawl hàng tháng |
| URL `Not found` trong sitemap | 0 | Sitemap + crawl |
| Content xuất bản/làm mới | 8 URL trong tháng 3–5 | Editorial tracker |
| Referring domains phù hợp | 5–8 domain mới | Ahrefs/Semrush/manual log |
| CTR nhóm URL ưu tiên | Cải thiện theo từng query/page | GSC |

## 9. Theo dõi vận hành

- **Hàng tuần:** index coverage, lỗi 404/5xx, đơn organic, URL/sản phẩm mới.
- **Hàng tháng:** crawl kỹ thuật, GSC query/page, CTR, positions, content publishing, links, conversion rate.
- **Hàng quý:** rà soát cannibalization với Thegioidotap, refresh content cũ, thông tin giá/hàng tồn, schema và CWV.

## 10. Nguồn tham khảo đối thủ

- Beyono: https://www.beyono.vn/
- Chillax Sport: https://chillaxsport.vn/gioi-thieu
- TEZO danh mục nữ: https://tezo.vn/collections/thoi-trang-nu
- TEZO bài so sánh đồ tập: https://tezo.vn/blogs/tin-thoi-trang/top-6-thuong-hieu-do-tap-quoc-te-gia-phai-chang-phu-hop-choi-pickleb
- VnExpress về ICADO Pickleplay: https://vnexpress.net/hoa-hau-kieu-duy-lam-dai-dien-bo-suu-tap-icado-pickleplay-4860788.html

