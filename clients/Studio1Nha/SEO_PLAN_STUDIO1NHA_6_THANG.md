# Kế hoạch SEO 6 tháng — Studio 1 Nhà

**Thời gian đề xuất:** Tháng 8/2026–Tháng 1/2027  
**Mục tiêu kinh doanh:** tăng organic qualified leads cho các gói chụp ảnh cưới tại TP.HCM, chụp phim trường, ngoại cảnh và dịch vụ ngày cưới.  
**Nguồn phân tích:** crawl `studio1nha.xlsx` (2.388 URL; 90 HTML) và rà soát SERP ngày 02/08/2026.

## 1. Tóm tắt chiến lược

Studio 1 Nhà có lợi thế rõ ràng về phim trường riêng, concept Hàn Quốc và danh mục điểm chụp ngoại cảnh (Hồ Cốc, Đà Lạt, Vĩnh Hy, Phú Quý). SEO cần chuyển từ trạng thái **nhiều URL và nội dung rải rác** sang **cụm trang dịch vụ có ý định mua cao**; nội dung thông tin đóng vai trò thu hút–nuôi dưỡng và dẫn khách về trang gói/đặt lịch.

Ưu tiên theo thứ tự:

1. Sửa khả năng crawl/index và tín hiệu on-page tại các trang dịch vụ.
2. Xây cụm landing page theo nhu cầu–địa điểm–concept, kèm bảng giá, portfolio thật, FAQ và CTA đặt lịch.
3. Dùng content hướng dẫn/so sánh để phủ phễu tìm kiếm sớm; liên kết nội bộ có chủ đích về trang tiền.
4. Tăng Local SEO, review, E-E-A-T và digital PR/liên kết liên quan ngành cưới.

## 2. Hiện trạng website từ file crawl

| Hạng mục | Phát hiện | Mức ưu tiên | Hành động |
|---|---:|---|---|
| Quy mô crawl | 2.388 URL, trong đó 90 HTML và phần còn lại chủ yếu là ảnh/tài nguyên | — | Tách dashboard KPI HTML/indexable khỏi asset để theo dõi đúng |
| Indexability HTML | 40 indexable; 36 canonical; 9 noindex; 5 client-error | P0 | Rà soát canonical/noindex theo từng template; chỉ giữ URL chuẩn có ý định tìm kiếm |
| HTTP lỗi | 4 URL 404 ảnh và 1 URL 400 (`/ho-coc/src=`) | P0 | Sửa link nguồn; thay ảnh hoặc 301 khi có trang đích tương ứng |
| H1 | 44/90 HTML không có H1 | P0 | Mỗi trang indexable có đúng 1 H1 bám chủ đề/ý định tìm kiếm |
| Title | 5 thiếu; 10 quá ngắn; 52 dài trên 60 ký tự | P1 | Viết lại theo mẫu: dịch vụ + khác biệt + địa điểm + thương hiệu khi còn chỗ |
| Meta description | 5 thiếu; 38 ngắn dưới 70; 21 dài trên 160 | P1 | Viết description độc nhất, nêu concept/giá từ/CTA; giữ khoảng 120–155 ký tự |
| Ảnh thiếu alt | 85/90 HTML có ảnh thiếu alt (thường 1–2 ảnh/trang) | P1 | Audit ảnh décor vs ảnh nội dung; thêm alt mô tả cho ảnh portfolio, để alt rỗng cho ảnh thuần trang trí |
| Hiệu năng server | 14 HTML phản hồi trên 1.000 ms | P1 | Benchmark hosting, cache, WebP/AVIF, lazy-load, CDN; đo lại Core Web Vitals thực tế |
| Phân mảnh URL | Có cặp URL slash/non-slash và `//category/...` | P0 | Ép redirect 301 nhất quán, self-canonical, chuẩn hóa internal link và sitemap |

**Lưu ý:** 36 URL canonical và 9 noindex không mặc nhiên là lỗi. Cần xác nhận mục đích từng URL trước khi đổi, đặc biệt với trang lọc, trang đích cũ hoặc tài nguyên. Crawl này không có dữ liệu Google Search Console, backlink hay Core Web Vitals; các KPI bên dưới là khung thiết lập baseline trong tháng đầu.

## 3. Bối cảnh ngành hàng và đối thủ

### Nhu cầu tìm kiếm cần sở hữu

| Cụm ý định | Vai trò | Trang đích/chủ đề ưu tiên |
|---|---|---|
| `chụp ảnh cưới tphcm`, `studio chụp ảnh cưới đẹp tphcm` | Head term, thương mại | Trang dịch vụ trụ cột: chụp ảnh cưới TP.HCM |
| `chụp ảnh cưới trọn gói`, `bảng giá chụp ảnh cưới` | Quyết định/so sánh giá | Bảng giá minh bạch, phạm vi gói, add-on, FAQ |
| `chụp ảnh cưới phim trường tphcm` | Commercial niche | Landing page phim trường + từng phim trường/concept |
| `chụp ảnh cưới ngoại cảnh`, `Hồ Cốc`, `Đà Lạt`, `Vĩnh Hy`, `Phú Quý` | Destination-led | Bộ landing page địa điểm có portfolio, lịch trình, chi phí, mùa đẹp |
| `chụp ảnh cưới Hàn Quốc`, `concept ảnh cưới Hàn Quốc` | Style-led | Hub concept Hàn Quốc; portfolio theo vibe/trang phục |
| `quay phim chụp ảnh phóng sự cưới`, `combo ngày cưới` | Cross-sell, high value | Trang dịch vụ ngày cưới, case study và gói combo |
| `kinh nghiệm chụp ảnh cưới`, `nên chọn studio hay trọn gói` | Informational | Bài tư vấn liên kết đến trang gói và form đặt lịch |

### Đối thủ SEO trực tiếp cần theo dõi

| Nhóm | Đơn vị | Điểm quan sát trên SERP | Hướng đáp trả của Studio 1 Nhà |
|---|---|---|---|
| Studio wedding chuyên biệt | Oliva Wedding | Phủ trang chủ và content về phong cách/phim trường | Tạo trang concept + portfolio thật, tối ưu rich content/FAQ |
| Studio wedding chuyên biệt | Jovian Studio | Có trang chuyên sâu truy vấn phim trường | Thắng theo local intent + landing page phim trường, giá, lịch chụp và case thật |
| Giá và gói trọn gói | Aloha Studio | Có landing page bảng giá/chụp cưới với mức giá hiển thị | Đưa mức giá từ, inclusions/exclusions, FAQ và CTA tư vấn trên trang tiền |
| Thương hiệu/portfolio đa dịch vụ | Lavender Studio | Phủ nhiều phân khúc ảnh và nhiều địa phương | Tập trung khác biệt TP.HCM + phim trường riêng + concept trẻ thay vì cạnh tranh độ rộng |
| Giá rẻ/local | Ahihi Studio, Lão Trư Studio | Nhắm nhu cầu chụp cưới TP.HCM/ngoại cảnh | Nêu proof: ekip, review, quy trình, số album, hậu trường và portfolio theo nhu cầu |

Đây là shortlist từ kết quả tìm kiếm, không phải báo cáo thị phần. Hàng tháng cần chụp SERP 20–30 từ khóa tiền để cập nhật đối thủ thực tế theo từng cụm.

## 4. Kiến trúc nội dung và liên kết nội bộ mục tiêu

```text
Chụp ảnh cưới TP.HCM (pillar / money page)
├── Chụp ảnh cưới trọn gói & Bảng giá
├── Chụp ảnh cưới phim trường
│   ├── Sunny/Paris Garden, Vũ Garden, L'Amour, Long Island...
│   └── Concept Hàn Quốc
├── Chụp ảnh cưới ngoại cảnh
│   ├── Hồ Cốc / Vũng Tàu
│   ├── Đà Lạt
│   ├── Vĩnh Hy / Hang Rái
│   └── Phú Quý
├── Quay phim & phóng sự cưới / Combo ngày cưới
└── Trang phục, makeup, đặt lịch

Blog hướng dẫn / so sánh / checklist → liên kết ngữ cảnh về đúng landing page dịch vụ
```

Nguyên tắc: một URL chính cho mỗi ý định; mỗi landing page có 3–6 internal links vào từ bài blog/portfolio liên quan; ưu tiên anchor mô tả tự nhiên, không lặp máy móc. Không tạo bài mới nếu đã có URL cùng mục đích mà chỉ cần nâng cấp/redirect.

## 5. Roadmap triển khai 6 tháng

| Tháng | Mục tiêu | Việc triển khai trọng tâm | Deliverables | KPI kiểm soát |
|---|---|---|---|---|
| **T1 — Nền tảng & đo lường** | Loại bỏ rào cản index/crawl, có baseline | Kết nối/kiểm tra GSC, GA4, GBP; mapping 90 HTML; xử lý 404/400, slash/non-slash, `//`; audit canonical/noindex/robots/sitemap; bổ sung H1/title/meta ở 15 URL có giá trị cao; audit alt; đo CWV | Technical backlog đã đóng P0; keyword map 30–50 KW; dashboard baseline | Indexed valid; crawl errors; branded/non-branded clicks; CWV; leads organic |
| **T2 — Trang tiền & local conversion** | Biến trang dịch vụ thành landing page chuyển đổi | Tối ưu/viết lại 5 trang: TP.HCM, trọn gói/bảng giá, phim trường, ngoại cảnh, phóng sự/combo; thêm bảng giá từ, portfolio, quy trình, FAQ schema, CTA/book lịch, review; chuẩn hóa NAP và Google Business Profile | 5 landing pages hoàn chỉnh; 1 template FAQ; conversion tracking form/call/Zalo | Impressions & CTR trang tiền; organic leads; GBP calls/directions; index status |
| **T3 — Cụm phim trường & concept** | Tăng topical authority ở lợi thế khác biệt | Nâng cấp hub phim trường; tối ưu 4 trang phim trường/concept có nhu cầu; 4 bài hỗ trợ: chọn phim trường, concept Hàn Quốc, checklist chụp, so sánh studio/ngoại cảnh; thêm album thực tế có alt/caption | 1 hub + 4 landing/sub-pages + 4 bài; internal-link map v1 | Top 20/top 10 KW phim trường/concept; CTR; engagement/lead assist |
| **T4 — Cụm ngoại cảnh & địa điểm** | Chiếm long-tail có ý định mua cao | Nâng cấp 4 trang: Hồ Cốc/Vũng Tàu, Đà Lạt, Vĩnh Hy, Phú Quý; mỗi trang có lịch trình, mùa đẹp, chi phí, di chuyển, gallery, FAQ; 4 bài information dựa trên nhu cầu thực; PR/collab với venue/wedding vendors | 4 landing pages + 4 bài + 3–5 referring domains liên quan | Top 10 long-tail địa điểm; organic sessions cluster; RD chất lượng; lead theo destination |
| **T5 — E-E-A-T & mở rộng demand capture** | Tăng độ tin cậy, bao phủ giai đoạn cân nhắc | Case study 6 cặp đôi (brief → concept → ảnh → review); trang đội ngũ/quy trình/chính sách; 4 bài so sánh giá/gói/thời gian chuẩn bị; review generation flow sau bàn giao; audit CWV lần 2 | 6 case studies, 4 bài, trust block/sitewide; SOP xin review | Review volume/rating; assisted conversions; ranking trung bình money KW; CWV improvement |
| **T6 — Tối ưu & scale** | Chuyển tăng trưởng thành hệ thống lặp | GSC content refresh: sửa trang có impression cao CTR thấp; merge/redirect cannibalized pages; refresh bảng giá/portfolio; link reclamation/PR; A/B CTA và form; kế hoạch quý tiếp theo theo gap KW | SEO report 6 tháng; content refresh batch; Q2 backlog ưu tiên | Organic qualified leads vs baseline; conversion rate; top 3/10 share; revenue attribution |

## 6. Backlog nội dung ưu tiên

### Landing/service pages (tối ưu trước khi viết mới)

1. `https://studio1nha.vn/` — định vị “chụp ảnh cưới TP.HCM”; bổ sung H1 rõ ràng và CTA.
2. `/bang-gia-chup-anh-cuoi-tai-tphcm/` hoặc chọn một URL chuẩn cho cụm giá; đưa bảng gói, mục bao gồm/không gồm, FAQ.
3. `/phim-truong/` — xác nhận canonical, trở thành hub có các lựa chọn phim trường.
4. `/ngoai-canh/` — thêm metadata đúng độ dài và điều hướng theo địa điểm.
5. `/dich-vu-quay-phim-chup-anh-phong-su-cuoi/` + `/gia-quay-phim-chup-anh-phong-su-cuoi/` — quyết định quan hệ pillar/supporting để tránh chồng lấn.
6. `/chup-hinh-cuoi-ngoai-canh/`, `/chup-hinh-cuoi-da-lat/`, `/chup-anh-cuoi-han-quoc/`, `/phim-truong-vu-garden/` — kiểm tra canonical và hợp nhất với trang cũ nếu cùng intent.

### Bài/blog mới (đề xuất 12 bài, triển khai 2 bài/tháng từ T3)

| Cụm | Tiêu đề gợi ý | CTA đích |
|---|---|---|
| Giá | Bảng giá chụp ảnh cưới trọn gói TP.HCM: gồm gì, phát sinh gì? | Bảng giá/gói trọn gói |
| So sánh | Chụp studio, phim trường hay ngoại cảnh: chọn theo ngân sách và phong cách | Phim trường + ngoại cảnh |
| Chuẩn bị | Checklist chụp ảnh cưới trước 3 tháng cho cặp đôi lần đầu | Đặt lịch |
| Concept | 10 concept ảnh cưới Hàn Quốc hợp cô dâu Việt | Concept Hàn Quốc |
| Phim trường | Kinh nghiệm chọn phim trường chụp cưới ở TP.HCM | Hub phim trường |
| Ngoại cảnh | Chụp ảnh cưới Hồ Cốc: chi phí, lịch trình 1 ngày, mùa đẹp | Hồ Cốc |
| Ngoại cảnh | Chụp ảnh cưới Đà Lạt: 7 bối cảnh và budget cần chuẩn bị | Đà Lạt |
| Ngoại cảnh | Chụp ảnh cưới Vĩnh Hy – Hang Rái: kinh nghiệm di chuyển và concept phù hợp | Vĩnh Hy |
| Ngày cưới | Chụp phóng sự cưới khác gì chụp truyền thống? | Phóng sự cưới |
| Trang phục | Thuê váy cưới/vest: cách chọn theo dáng người và concept | Trang phục |
| Makeup | Makeup cô dâu đi chụp: thử trước bao lâu và cần lưu ý gì? | Makeup + đặt lịch |
| Proof | Case study: từ moodboard đến album tại [phim trường/địa điểm] | Gói liên quan |

## 7. KPI và cách đo

Không đặt con số tăng trưởng tuyệt đối trước khi có baseline GSC/GA4 và dữ liệu CRM. Chốt mục tiêu trong tuần 2 của T1 theo 4 nhóm sau:

| Tầng KPI | Chỉ số | Mục tiêu định hướng 6 tháng |
|---|---|---|
| Visibility | Impressions non-brand, số KW Top 10/Top 3 cho 30–50 từ khóa | Tăng đều; ưu tiên Top 10/Top 3 của trang tiền và long-tail địa điểm |
| Traffic quality | Organic sessions vào landing page, CTR, engaged sessions | Tăng traffic vào trang dịch vụ nhanh hơn blog thuần thông tin |
| Conversion | Form submit, click gọi, click Zalo, đặt lịch từ organic; CVR | Theo dõi theo landing page và cụm dịch vụ, không chỉ tổng site |
| Business | Qualified lead, booking, doanh thu/revenue attribution | CRM gắn UTM/source=organic; báo cáo theo gói và địa điểm |

Nhịp báo cáo: weekly technical/production; monthly GSC+GA4+GBP; quarterly đánh giá keyword gap, conversion và ngân sách content/PR.

## 8. Điều kiện để đạt kế hoạch

- Có quyền GSC, GA4, Google Business Profile, CMS và dữ liệu lead/booking.
- Xác nhận danh sách gói, mức giá từ, địa điểm đang vận hành, quy trình và phạm vi dịch vụ để nội dung chính xác.
- Ekip cung cấp tối thiểu 1 album/case thật mỗi tuần, review khách đã đồng ý và hình ảnh có quyền sử dụng.
- Dev hỗ trợ sprint T1: redirect, canonical/noindex, sitemap, tốc độ và tracking.
- Không dùng backlink số lượng lớn/không liên quan; ưu tiên đối tác phim trường, venue, wedding planner, báo/chuyên trang cưới và vendor địa phương.

## 9. Việc cần làm ngay trong 10 ngày đầu

1. Lấy export GSC 16 tháng và GA4 90 ngày; thiết lập baseline theo URL/service.
2. Chọn URL chuẩn cho title/slash/canonical conflict; xử lý 5 URL lỗi trước.
3. Tạo danh sách 15 URL money page và sửa H1/title/meta/CTA theo brief chung.
4. Xác minh conversion event cho form, call, Zalo, đặt lịch và đẩy vào CRM.
5. Chốt outline + asset list cho 5 landing pages T2 và lịch sản xuất T3.
