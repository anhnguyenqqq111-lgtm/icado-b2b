# Kế hoạch SEO 6 tháng — MayMacCTH

**Phạm vi:** `maymaccth.com`, thị trường Hải Phòng  
**Thời gian đề xuất:** Tháng 8/2026–Tháng 1/2027  
**Mục tiêu kinh doanh:** tăng qualified lead qua form báo giá và tạo khách hàng doanh nghiệp có khả năng đặt lại.  
**Nguồn hiện có:** tài liệu nghiên cứu nội bộ, bộ từ khóa và các file crawl/keyword trong thư mục dự án. Các số audit URL cần được xác minh lại bằng crawl mới, GSC, GA4 và CRM trong tháng 1.

## 1. Tóm tắt điều hành

MayMacCTH cần tập trung SEO vào ba nhóm tạo doanh thu và có khả năng mua lại tại Hải Phòng:

1. Đồng phục doanh nghiệp.
2. Đồng phục café, nhà hàng và khách sạn.
3. Đồng phục bảo hộ lao động.

Chiến lược sáu tháng là **xác minh và dọn nền tảng → chuẩn hóa trang tiền → xây ba topic cluster ưu tiên → tăng local trust và bằng chứng thật → tối ưu theo qualified lead, đơn hàng và repeat revenue**.

Ưu tiên 90 ngày đầu:

1. Xác minh lỗi index/noindex, hoàn thiện tracking form và thiết lập baseline GSC–GA4–CRM.
2. Chốt một URL primary cho từng nhóm dịch vụ; hoàn thiện offer, proof, FAQ, internal links và CTA báo giá.
3. Xây cụm đồng phục doanh nghiệp trước, sau đó mở rộng F&B/khách sạn và bảo hộ lao động.

Traffic, impression và thứ hạng là chỉ số dẫn đường. Outcome cuối là:

`Organic landing page → form hợp lệ → qualified lead → báo giá → đơn hàng → đặt lại`

## 2. Kết quả audit URL

Audit hiện tại mới là nhận định ban đầu, chưa có bảng URL inventory đã xác minh. Không dùng các nhận định sau làm số liệu nghiệm thu cho đến khi crawl lại.

| Hạng mục | Phát hiện hiện có | Mức ưu tiên | Hành động |
|---|---|---|---|
| Indexability | Tài liệu cũ ghi nhận meta `robots/googlebot noindex` trên các trang | P0 | Kiểm tra HTML render, source, X-Robots-Tag, robots.txt và GSC URL Inspection; chỉ sửa sau khi xác nhận |
| Sitemap/canonical | Chưa có decision map theo từng URL | P0 | Crawl toàn site; chỉ giữ URL 200, canonical, indexable trong sitemap |
| Title/meta | Trang chủ và một số trang được mô tả là title/meta ngắn hoặc chung chung | P1 | Xuất dữ liệu crawl; viết lại trước cho money pages |
| H1 | Tài liệu cũ ghi nhận thiếu H1 ở trang chủ/template | P1 | Mỗi trang indexable có đúng một H1 theo intent |
| Hình ảnh | Có nhận định ảnh thiếu alt và dung lượng lớn | P1 | Phân biệt ảnh nội dung/ảnh trang trí; tối ưu WebP/AVIF, kích thước và alt tự nhiên |
| Mobile/UX | Menu mobile và đường chuyển đổi cần kiểm tra | P1 | Test trên thiết bị thật; ưu tiên form, CTA, tốc độ và khả năng đọc |
| Conversion tracking | Chưa có bằng chứng form → GA4 → CRM hoạt động end-to-end | P0 | Thiết lập và QA `form_start`, `generate_lead`, `form_error` |
| Baseline | Chưa có GSC/GA4/CRM baseline thống nhất | P0 | Lấy GSC 16 tháng, GA4 ≥90 ngày và CRM 6–12 tháng |

### Việc cần xử lý ngay

- Kiểm tra trực tiếp lỗi `noindex`; không gỡ hàng loạt theo nhận định cũ nếu chưa xác nhận từng template.
- Lập master URL inventory: URL, status, type, indexability, canonical, sitemap, business value, decision và owner.
- Phân loại URL theo `keep/refresh/merge/301/noindex/404-410/investigate`.
- Chỉ đóng ticket khi recrawl và GSC xác nhận đúng trạng thái.
- QA form trên mobile/desktop và kiểm tra lead có đủ source, landing page, service group trong CRM.

## 3. Nhóm URL ưu tiên

Các URL dưới đây là cấu trúc đề xuất; cần đối chiếu với URL đang tồn tại trước khi tạo mới.

### Nhóm A — Trang doanh thu, xử lý tháng 1–2

- Trang chủ — định vị xưởng may đồng phục B2B tại Hải Phòng.
- `/may-dong-phuc-doanh-nghiep/` — đồng phục doanh nghiệp.
- `/may-dong-phuc-nha-hang-khach-san/` — đồng phục café, nhà hàng, khách sạn.
- `/may-dong-phuc-bao-ho-lao-dong/` — đồng phục bảo hộ lao động.
- `/may-dong-phuc-tai-hai-phong/` — local hub nếu intent khác rõ với trang chủ.
- Trang quy trình/báo giá/cam kết chất lượng — supporting conversion asset, không tự động tạo URL SEO riêng nếu trùng intent.

Mỗi money page cần có: H1 theo intent; title/meta; offer; nhóm sản phẩm; chất liệu; MOQ; giá từ hoặc cách báo giá; quy trình; thời gian; chính sách/bảo hành; portfolio/case thật; FAQ; form báo giá; call/Zalo phụ; breadcrumb; internal links và schema phù hợp nội dung hiển thị.

### Nhóm B — Subservice và commercial content, xử lý tháng 2–4

- Đồng phục polo công ty và sơ mi/văn phòng.
- Đồng phục quán café, nhà hàng, khách sạn theo vị trí sử dụng.
- Đồng phục/tạp dề nhân viên phục vụ, bếp và lễ tân.
- Đồng phục công nhân, kỹ sư và bảo hộ theo ngành ứng dụng.
- Trang báo giá, chất liệu, size và quy trình khi có intent riêng trên SERP.

Chỉ tạo URL riêng khi có search intent và nội dung/offer khác biệt. Các biến thể gần nhau được giải quyết bằng section/FAQ thay vì một URL cho mỗi từ khóa.

### Nhóm C — Content hỗ trợ, xử lý tháng 3–5

- Hướng dẫn chọn chất liệu, size, in/thêu và bảo quản.
- Checklist đặt may, duyệt mẫu, nghiệm thu và đặt bổ sung.
- Case study khách hàng tại Hải Phòng.
- Nội dung theo nhu cầu KCN, F&B và doanh nghiệp địa phương.

Blog phải liên kết theo ngữ cảnh tới money page; không thay thế landing page dịch vụ.

## 4. Nghiên cứu cạnh tranh công khai

Đây là danh sách đối thủ/benchmark từ tài liệu nội bộ; cần rà soát SERP cho 20–50 keyword tiền trước khi chốt competitor matrix.

| Nhóm | Đơn vị | Điểm cần kiểm chứng | Hướng đáp trả của MayMacCTH |
|---|---|---|---|
| Local Hải Phòng | Đồng phục Trọng Tấn | Local landing pages, xưởng/ảnh thật, độ phủ keyword địa phương | Cạnh tranh bằng proof thật, báo giá/quy trình rõ, tốc độ tư vấn và case Hải Phòng |
| Local Hải Phòng | Đồng phục Phố Cảng / Đồng phục 3 Miền | Uy tín địa phương, Zalo và nhóm bảo hộ/công sở | Chuẩn hóa service architecture, form qualification và content theo intent mua |
| Toàn quốc | Đồng phục Hải Anh | Độ phủ danh mục/content, thương hiệu mạnh | Không cạnh tranh bằng số lượng; tập trung local service, case, MOQ, SLA và khả năng bổ sung |
| Benchmark ngành | Gạo House và các website chuyên biệt | UX, landing page, catalog và social proof | Dùng portfolio thật, form ngắn, điều khoản rõ và internal links theo hành trình mua |

### Khoảng trống cần khai thác

1. Trang báo giá minh bạch: yếu tố ảnh hưởng giá, MOQ, mẫu duyệt và chi phí phát sinh.
2. Dịch vụ phục vụ Hải Phòng: thời gian tư vấn/giao mẫu, khu vực phục vụ và case địa phương.
3. Proof content: ảnh xưởng, quy trình, case, chất liệu, kiểm soát chất lượng và khả năng đặt bổ sung.
4. Nội dung ra quyết định: chọn vải, in hay thêu, size, timeline, nghiệm thu và bảo hành.

## 5. Chiến lược keyword và content pillar

### Pillar 1 — Đồng phục doanh nghiệp

- Intent thương mại: may đồng phục doanh nghiệp, đồng phục công ty, áo polo công ty, đồng phục văn phòng tại Hải Phòng.
- Intent hỗ trợ mua: báo giá, MOQ, chất liệu, bảng size, phối màu, in/thêu logo và quy trình.
- URL đích: money page đồng phục doanh nghiệp và các subservice có intent riêng.

### Pillar 2 — Café, nhà hàng và khách sạn

- Intent thương mại: may đồng phục quán café, nhà hàng, khách sạn, tạp dề, đồng phục phục vụ/bếp/lễ tân.
- Intent hỗ trợ mua: chọn kiểu theo vị trí, chất liệu dễ giặt, phối nhận diện, số lượng và đặt bổ sung.
- URL đích: hub F&B/khách sạn và landing page con khi đủ dữ liệu.

### Pillar 3 — Bảo hộ lao động

- Intent thương mại: may đồng phục bảo hộ lao động, đồng phục công nhân/kỹ sư, xưởng may bảo hộ Hải Phòng.
- Intent hỗ trợ mua: chọn vải, phản quang, độ bền, tiêu chuẩn áp dụng, mẫu duyệt và kiểm soát chất lượng.
- URL đích: money page bảo hộ và các trang ngành ứng dụng có khác biệt thật.

### Pillar 4 — Local SEO Hải Phòng

- Intent: xưởng may đồng phục Hải Phòng, may đồng phục tại Hải Phòng và truy vấn gắn khu vực/KCN có demand thật.
- Asset: địa chỉ/NAP, Google Business Profile, ảnh xưởng/đội ngũ, review, case và đối tác địa phương.
- Không tạo hàng loạt location page nếu không có nội dung và năng lực phục vụ khác biệt.

### Pillar 5 — Quy trình, chất liệu và hậu mãi

- Intent hỗ trợ mua/retention: quy trình đặt may, chọn vải, bảng size, in/thêu, bảo quản, nghiệm thu và đặt bổ sung.
- Vai trò: nuôi dưỡng lead và tăng khả năng đặt lại; CTA theo đúng giai đoạn.

## 6. Roadmap 6 tháng

| Tháng | Mục tiêu | Công việc | Deliverables |
|---|---|---|---|
| 1 | Xác minh nền tảng và baseline | QA form/GA4/CRM; crawl site; kiểm tra noindex/robots/canonical/sitemap; URL decision map; lấy GSC/GA4/CRM baseline | Business brief, measurement spec, URL inventory, backlog P0/P1/P2, baseline report |
| 2 | Chuẩn hóa trang doanh thu | Chốt một URL primary cho ba nhóm; tối ưu offer, H1/title/meta, pricing/MOQ, proof, FAQ, form, schema và internal links | 3 money pages QA/indexable; landing-page template; internal-link map |
| 3 | Xây cluster đồng phục doanh nghiệp | Hoàn thiện hub/subservice; 2–4 supporting assets; 1 case study Hải Phòng; liên kết về money page | Cluster doanh nghiệp hoạt động; ≥3 contextual inbound links/page; content tracker |
| 4 | Xây cluster F&B/khách sạn | Landing page theo intent; portfolio/case; 2–4 supporting assets; CRO vòng 1 sau ≥28 ngày dữ liệu | Cluster F&B/khách sạn; case/portfolio; báo cáo CRO vòng 1 |
| 5 | Xây cluster bảo hộ và local authority | Money page bảo hộ; content vật liệu/yêu cầu kỹ thuật; case; GBP/NAP/review flow; outreach địa phương | Cluster bảo hộ; relevant mentions/reviews; local/authority log |
| 6 | Tối ưu theo dữ liệu và CRO | GSC query–page review; CTR/cannibalization/internal links; CRO vòng 2; đối chiếu GA4–CRM; phân tích repeat cohort; reprioritize | Báo cáo sáu tháng, funnel report, refresh list, CRO backlog, kế hoạch quý tiếp theo |

## 7. Lịch content đề xuất

Lịch cuối cùng phải được đối chiếu với keyword-to-URL map; không xuất bản mới nếu đã có URL đúng intent cần refresh.

| Tháng | Nội dung | Intent | URL đích chính |
|---|---|---|---|
| 3 | Báo giá may đồng phục doanh nghiệp phụ thuộc những yếu tố nào? | Commercial investigation | Trang đồng phục doanh nghiệp |
| 3 | Chọn áo polo hay sơ mi làm đồng phục công ty | Comparison | Trang doanh nghiệp/polo/sơ mi |
| 3 | Bảng size đồng phục doanh nghiệp và quy trình chốt size | Commercial investigation | Trang đồng phục doanh nghiệp |
| 3 | Case study: đồng phục doanh nghiệp tại Hải Phòng | Proof/conversion | Trang đồng phục doanh nghiệp |
| 4 | Chọn đồng phục cho từng vị trí trong quán café/nhà hàng | Commercial investigation | Trang F&B/khách sạn |
| 4 | Tạp dề, áo phục vụ và đồng phục bếp: chọn chất liệu nào? | Comparison | Trang F&B/khách sạn |
| 4 | Checklist đặt đồng phục khi mở quán hoặc chi nhánh mới | Commercial investigation | Trang F&B/khách sạn |
| 4 | Case study: bộ đồng phục F&B tại Hải Phòng | Proof/conversion | Trang F&B/khách sạn |
| 5 | Chọn vải may đồng phục bảo hộ theo môi trường làm việc | Commercial investigation | Trang bảo hộ lao động |
| 5 | In hay thêu logo trên đồng phục công nhân? | Comparison | Trang bảo hộ lao động |
| 5 | Quy trình duyệt mẫu và nghiệm thu đơn bảo hộ số lượng lớn | Commercial investigation | Trang bảo hộ lao động |
| 5 | Hướng dẫn bảo quản và đặt bổ sung đồng phục đúng màu/chất liệu | Retention | Money page liên quan |

Mỗi nội dung cần có một primary keyword, intent, URL đích, CTA, 3–5 internal links, asset thật, owner và tiêu chí QA/indexation.

## 8. KPI và cách đo

Chốt mục tiêu tuyệt đối sau khi có ít nhất 28 ngày baseline và Sales cập nhật CRM đầy đủ.

| Nhóm KPI | Mục tiêu định hướng | Nguồn và cách đo |
|---|---|---|
| Form tracking | 100% test case pass, không mất source/landing page | GA4 DebugView + CRM test |
| Technical P0 | 100% ticket P0 được recrawl xác nhận | Crawl + GSC + ticket log |
| Money pages | 100% ba trang ưu tiên QA/indexable/tracking pass | Crawl + content/landing tracker |
| Organic form leads | Tăng so với baseline theo từng cluster | GA4 + CRM |
| Organic qualified leads | Tăng so với baseline; chỉ tính Sales xác nhận | CRM |
| Qualified/quote/close rate | Theo dõi và cải thiện sau baseline | CRM |
| Repeat order/revenue | Báo cáo cohort 90/180/365 ngày khi đủ dữ liệu | CRM/kế toán |
| Non-brand clicks | Tăng theo ba cluster, không dùng total domain đơn lẻ | GSC query/page |
| Landing-page CVR | Cải thiện qua hai vòng CRO | GA4, so trước–sau ≥28 ngày |
| Content/case | 12 content assets, gồm tối thiểu 2 case thật trong tháng 3–5 | Editorial tracker; chỉ tính URL QA/indexable |
| Local/authority | Relevant mentions và review thật | GBP + outreach log |

### Định nghĩa vận hành

- **Primary conversion:** form gửi thành công.
- **Lead hợp lệ:** thông tin liên hệ dùng được; không phải spam/tuyển dụng/nhà cung cấp.
- **Qualified lead:** đại diện doanh nghiệp/cơ sở; phục vụ tại Hải Phòng; thuộc ba nhóm ưu tiên; có ý định nhận tư vấn/báo giá.
- **Repeat customer:** khách phát sinh đơn hàng mới sau đơn đầu tiên.
- **Forecast:** `sessions × form CVR × qualified rate × quote rate × close rate × AOV`.

## 9. Theo dõi vận hành

### Nhịp vận hành

- **Hàng tuần:** index health, lỗi crawl, form tracking, ticket P0/P1, content QA, qualified lead và phản hồi Sales.
- **Hai tuần:** sprint SEO–Content–Dev–Sales; cập nhật owner, deadline, dependency và blocker.
- **Hàng tháng:** GSC query/page, performance theo cluster, CVR, CRM funnel, GBP/review, outreach và content progress.
- **Hàng quý:** cannibalization, refresh, repeat cohort, năng lực sản xuất và reprioritize theo business value.

### Tracker bắt buộc

| Nhóm | Trường cần theo dõi | Tiêu chí đóng |
|---|---|---|
| URL decision | URL, type, issue, decision, destination, reason, priority, owner, due date, QA | Recrawl/GSC xác nhận |
| Technical | Issue, evidence, recommendation, owner, deploy date, recrawl result | Không đóng chỉ vì đã deploy |
| Landing page | Intent, keyword, URL, offer, proof, CTA, assets, tracking, QA/index status | Tất cả mục bắt buộc pass |
| Content | Cluster, keyword, intent, URL đích, CTA, links, asset, owner, publish/index status | SEO + brand + asset owner sign-off |
| Lead/revenue | Ngày, landing page, service, source, qualification, quote, won/lost, revenue, repeat | Sales cập nhật đủ trạng thái |
| Authority/local | Target, relevance, pitch/asset, status, live URL/mention, date, owner | Chỉ tính link/mention/review thật |

### Quy tắc báo động

| Tín hiệu | Ngưỡng | Hành động |
|---|---|---|
| Money page mất index/canonical sai | Phát hiện bất kỳ | Ticket P0; kiểm tra robots, status, canonical, sitemap và internal links |
| Form/event/CRM source lỗi | Phát hiện bất kỳ | Dừng đánh giá KPI; sửa và test end-to-end trong 48 giờ |
| Organic clicks giảm | >20% WoW sau khi loại trừ mùa vụ | Kiểm tra query/page, index status, deploy và SERP |
| CVR giảm | >25% MoM trong khi traffic ổn định | Kiểm tra form, mobile UX, CTA, offer và phản hồi Sales |
| Impressions cao, CTR thấp | Thấp hơn baseline cluster sau ≥28 ngày | Test title/meta và bổ sung proof/FAQ phù hợp |

## 10. Nguồn tham khảo

### Nguồn dự án

- Các file `01–07` và `research_log.md` trong thư mục MayMacCTH.
- Các workbook keyword/crawl trong thư mục MayMacCTH; cần ghi snapshot và định nghĩa cột khi sử dụng.

### Đối thủ/benchmark cần xác minh

- MayMacCTH: https://maymaccth.com/
- Đồng phục Trọng Tấn: https://dongphuctrongtan.com/
- Đồng phục Phố Cảng: https://dongphucphocang.com/
- Đồng phục 3 Miền: https://dongphuc3mien.vn/
- Đồng phục Hải Anh: https://dongphuchaianh.vn/
- Gạo House: https://gaohouse.vn/

### Tài liệu Google

- Robots meta tag: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- Canonicalization: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Sitemap: https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
- Structured data policies: https://developers.google.com/search/docs/appearance/structured-data/sd-policies

