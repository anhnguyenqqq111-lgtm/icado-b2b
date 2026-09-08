# Kế hoạch SEO 6 tháng tổng hợp — MayMacCTH

**Ngày chốt:** 2026-08-03  
**Thị trường:** Hải Phòng  
**Conversion chính:** Form yêu cầu báo giá  
**Outcome cuối:** Qualified lead, đơn hàng, doanh thu và khách hàng đặt lại

---

## 1. Định hướng kinh doanh

SEO phải tạo ra khách hàng doanh nghiệp tại Hải Phòng có nhu cầu đặt may thật và khả năng đặt lại. Traffic, impression và thứ hạng là chỉ số dẫn đường, không phải outcome cuối.

### Chuỗi chuyển đổi

`Organic landing page → mở form → gửi form → lead hợp lệ → qualified lead → báo giá → đơn hàng → đặt lại`

### Nhóm dịch vụ ưu tiên

| Ưu tiên | Nhóm dịch vụ | Khách hàng | Cơ hội kinh doanh | CTA chính |
|---:|---|---|---|---|
| 1 | Đồng phục doanh nghiệp | SME, văn phòng, doanh nghiệp dịch vụ | Nhu cầu rộng; bổ sung theo nhân sự; làm mới định kỳ | Nhận báo giá và tư vấn mẫu |
| 2 | Đồng phục café, nhà hàng, khách sạn | Chủ cơ sở, chuỗi F&B, khách sạn | Nhiều vị trí sử dụng; thay mới và mở rộng điểm bán | Nhận thiết kế/mẫu và báo giá |
| 3 | Đồng phục bảo hộ lao động | Nhà máy, xưởng, nhà thầu, doanh nghiệp KCN | Đơn hàng lớn; cấp phát và thay thế định kỳ | Báo giá theo số lượng/tiêu chuẩn |

Áo lớp, áo nhóm, gia đình và các nhóm B2C không thuộc ưu tiên mở rộng SEO trong sáu tháng đầu. Chỉ giữ nội dung hiện có khi có giá trị kinh doanh hoặc hỗ trợ rõ ràng cho nhóm ưu tiên.

---

## 2. Định nghĩa conversion và lead

### Primary conversion

Form được gửi thành công và ghi nhận được nguồn organic, landing page, thời gian gửi và thông tin liên hệ.

### Lead hợp lệ

Form có tên và kênh liên hệ sử dụng được; không phải spam, tuyển dụng, nhà cung cấp hoặc yêu cầu ngoài phạm vi dịch vụ.

### Qualified lead — định nghĩa tạm thời

Sales xác nhận lead đáp ứng đủ ba điều kiện:

1. Là doanh nghiệp/cơ sở kinh doanh hoặc người đại diện mua hàng.
2. Địa điểm giao hàng hoặc phục vụ thuộc Hải Phòng.
3. Nhu cầu thuộc một trong ba nhóm ưu tiên và có ý định nhận tư vấn/báo giá.

Trước khi forecast doanh thu, Sales cần bổ sung MOQ, giá trị đơn tối thiểu, thời gian dự kiến mua và các trường hợp bị loại.

### Khách hàng đặt lại

Khách phát sinh đơn hàng mới sau đơn đầu tiên. CRM cần lưu ngày đơn đầu, ngày đơn lặp lại, nhóm sản phẩm và doanh thu từng đơn. Repeat rate được báo cáo theo cohort 90/180/365 ngày.

---

## 3. Thiết kế form và tracking

### Trường form đề xuất

- Họ tên và số điện thoại/Zalo.
- Tên doanh nghiệp/cơ sở.
- Nhóm nhu cầu.
- Số lượng dự kiến.
- Quận/huyện hoặc địa điểm giao hàng.
- Thời gian cần hàng.
- Yêu cầu về thiết kế, chất liệu hoặc tiêu chuẩn bảo hộ.

Không bắt buộc quá nhiều trường trước khi gửi. Các thông tin chuyên sâu có thể được Sales thu thập ở bước qualification.

### Sự kiện tối thiểu

- `form_start`: bắt đầu tương tác form.
- `generate_lead`: gửi form thành công.
- `form_error`: lỗi ngăn form được gửi.
- `click_phone`: nhấp gọi điện — conversion phụ.
- `click_zalo`: nhấp Zalo — conversion phụ.

CRM cần lưu source, medium, landing page, nhóm dịch vụ, qualification status, quote status, won/lost, doanh thu và repeat order.

---

## 4. Measurement plan và KPI tree

### KPI tree

`Repeat revenue ← đơn đặt lại ← đơn hàng ← báo giá thắng ← qualified lead ← form hợp lệ ← organic session ← click/impression/indexation`

### Bộ chỉ số

| Tầng | KPI | Nguồn | Tần suất | Owner |
|---|---|---|---|---|
| Business | Đơn hàng, doanh thu organic, đơn đặt lại, repeat revenue | CRM/kế toán | Tháng | Sales/Marketing |
| Sales | Qualified lead, báo giá, close rate, lý do mất | CRM | Tuần/tháng | Sales |
| Conversion | Form submit, completion rate, landing-page CVR | GA4/GTM | Tuần | Marketing Ops |
| Traffic quality | Organic sessions vào money pages, engagement | GA4 | Tuần/tháng | SEO |
| Visibility | Click, impression, CTR theo cluster/page | GSC | Tuần/tháng | SEO |
| Technical | Indexability, canonical, crawl errors, sitemap | Crawl/GSC | Tuần/tháng | SEO/Dev |

### Quy tắc KPI

- Thiết lập baseline ít nhất 28 ngày sau khi tracking được QA.
- Chưa cam kết số lead, traffic hay Top 3 khi chưa có GSC/GA4/CRM baseline.
- Tách branded/non-branded và báo cáo riêng ba cluster ưu tiên.
- Chỉ ghi nhận qualified lead khi Sales đã xác nhận trong CRM.
- Không dùng average position toàn site làm KPI chính.
- Không dùng điểm “unique content”, số backlink hoặc DA như KPI chất lượng độc lập.
- Review phải là review thật; không đặt mục tiêu tuyệt đối 5 sao.

### Công thức forecast

- `Form leads = organic money-page sessions × form CVR`.
- `Qualified leads = form leads × qualified rate`.
- `Won orders = qualified leads × quote rate × close rate`.
- `Revenue = won orders × AOV`.
- `Repeat revenue = khách đủ điều kiện đặt lại × repeat rate × repeat AOV`.

---

## 5. Roadmap triển khai sáu tháng

### Tháng 1 — Tracking, baseline và technical P0

**Điều kiện:** quyền CMS, GSC, GA4/GTM; CRM status; MOQ/AOV tạm thời.

**Công việc:**

- QA form trên mobile/desktop và thiết lập các sự kiện.
- Truyền source/medium, landing page và nhóm dịch vụ vào CRM.
- Crawl toàn site; lập URL inventory và quyết định index/noindex/301/canonical.
- Kiểm tra meta robots, X-Robots-Tag, robots.txt, sitemap và canonical.
- Xác minh lại lỗi `noindex`; recrawl và kiểm tra GSC URL Inspection sau sửa.
- Export GSC/GA4/CRM để lập baseline theo ba cluster.

**Bàn giao:** measurement spec, URL inventory, backlog P0/P1/P2 và baseline report.

**Done khi:** tracking test pass; P0 có owner/deadline; money pages trả 200, indexable và self-canonical; recrawl xác nhận.

### Tháng 2 — Money pages và conversion path

**Công việc:**

- Chọn URL primary duy nhất cho từng nhóm; xử lý cannibalization trước khi tạo URL mới.
- Refresh ba money pages với offer, phạm vi, quy trình, giá/giá từ hoặc cách báo giá, MOQ, thời gian, bảo hành, FAQ, proof và form.
- Bổ sung ảnh/case thật, title/meta/H1, internal links, breadcrumb và schema phù hợp.
- Tối ưu form, SLA phản hồi và thông tin bảo mật.

**Bàn giao:** ba money pages QA pass, content/asset gap list và internal-link map.

**Done khi:** mỗi trang có intent/CTA riêng, tracking pass, indexable và có tối thiểu ba contextual inbound links phù hợp.

### Tháng 3 — Cluster đồng phục doanh nghiệp

- Chọn subservice theo dữ liệu từ khóa, margin và năng lực thật.
- Xuất bản/refresh một hub và 2–4 supporting assets về báo giá, chất liệu, size, quy trình và case study.
- Tạo case study doanh nghiệp Hải Phòng với bài toán, số lượng, vật liệu/in-thêu, thời gian và kết quả.
- Liên kết supporting content với money page theo hành trình mua.

**KPI:** URL published/indexed, link coverage, non-brand click/impression và form theo cluster.

### Tháng 4 — Cluster café, nhà hàng, khách sạn

- Tách URL theo loại cơ sở/vị trí nhân viên chỉ khi SERP và asset chứng minh khác intent.
- Xây/refresh landing page theo các vị trí phục vụ, bếp, lễ tân và tạp dề.
- Nêu rõ vật liệu, giặt/bảo quản, khả năng bổ sung và thời gian sản xuất.
- Xuất bản case/portfolio thật và 2–4 supporting assets.
- Chạy CRO vòng một sau tối thiểu 28 ngày dữ liệu.

**KPI:** asset coverage, page CVR, qualified lead và lý do mất theo cluster.

### Tháng 5 — Cluster bảo hộ lao động và Local authority

- Xây/refresh money page theo ngành ứng dụng và yêu cầu kỹ thuật có thể chứng minh.
- Nêu rõ MOQ, mẫu duyệt, kiểm soát chất lượng, năng lực giao hàng và chu kỳ cấp phát.
- Tạo case study nhà máy/xưởng nếu được phép sử dụng.
- Xuất bản content về vật liệu và yêu cầu an toàn thực tế.
- Tối ưu GBP, NAP, review workflow và relevant local mentions.

**KPI:** qualified rate, quote rate, form theo cluster, review thật và relevant mentions.

### Tháng 6 — CRO, refresh và kế hoạch tiếp theo

- Đối chiếu GSC query–page; sửa CTR, intent mismatch, cannibalization và internal links.
- Chạy CRO vòng hai; lưu hypothesis, variant, thời gian và kết quả.
- Đối chiếu GA4 với CRM theo funnel form → qualified → quote → won.
- Phân tích cohort repeat nếu đủ dữ liệu; nếu chưa đủ, duy trì mốc 90/180/365 ngày.
- Chấm lại backlog theo `(Business impact × Demand × Confidence) / Effort`.

**Bàn giao:** growth report, funnel report, stop/start/continue và backlog quý tiếp theo.

---

## 6. KPI theo tháng

| Tháng | Trọng tâm | Leading KPI | Lagging KPI |
|---:|---|---|---|
| 1 | Tracking, technical, baseline | 100% test case pass; P0 có owner | Chưa đặt mục tiêu lead |
| 2 | Money pages | 100% completion/QA; đủ internal links | Baseline form và qualified lead |
| 3 | Đồng phục doanh nghiệp | Published/indexed/link coverage | Click và form theo cluster |
| 4 | F&B/khách sạn | QA, asset coverage, CRO test | Qualified lead và page CVR |
| 5 | Bảo hộ/Local authority | Relevant mentions/reviews thật | Qualified rate và quote rate |
| 6 | CRO/refresh | Test completion; backlog reprioritized | CVR, qualified lead và close rate |

---

## 7. RACI

| Workstream | Responsible | Accountable | Consulted |
|---|---|---|---|
| Technical/indexation | SEO + Dev | Marketing lead | CMS owner |
| Tracking/reporting | Marketing Ops | Marketing lead | Dev + Sales |
| Keyword/URL/content brief | SEO | Marketing lead | Sales/Operations |
| Content/asset | Content + Design | Marketing lead | SEO + Sales |
| Qualification/CRM/revenue | Sales | Sales lead | Marketing + Kế toán |
| GBP/review/mentions | Marketing/SEO | Marketing lead | CSKH/Sales |

---

## 8. Dữ liệu cần bổ sung

| Dữ liệu | Mục đích | Owner | Hạn đề xuất |
|---|---|---|---|
| GSC 16 tháng | Baseline, seasonality, query–URL map | SEO/website owner | Tuần 1 |
| GA4 tối thiểu 90 ngày | Landing page và conversion baseline | Marketing Ops | Tuần 1 |
| CRM/đơn hàng 6–12 tháng | Qualified rate, close rate, AOV, repeat rate | Sales/kế toán | Tuần 1 |
| MOQ và giá trị đơn tối thiểu | Chốt qualified lead | Sales/Operations | Tuần 1 |
| Năng lực sản xuất và SLA | Ưu tiên offer/công suất | Operations | Tuần 1 |
| Giá, quy trình, bảo hành | Hoàn thiện money pages | Sales/Operations | Tuần 2 |
| Case study, ảnh thật, review được phép dùng | Proof và CRO | Marketing/Sales | Tuần 2 |

---

## 9. Stop-the-line

- Money page mất index hoặc canonical sai.
- Form không gửi được, event không firing hoặc CRM mất nguồn/landing page.
- Deploy tạo 4xx/5xx, redirect loop hoặc robots/noindex sai.
- Nội dung dùng giá, thời gian, chứng nhận, review hoặc ảnh chưa được phê duyệt.

---

## 10. Quality gate trước triển khai

- [ ] Sales xác nhận MOQ, giá trị đơn tối thiểu và trường hợp loại lead.
- [ ] Form và CRM tracking đã QA end-to-end.
- [ ] Một intent có một URL primary.
- [ ] Ba money pages có offer, proof, CTA và owner.
- [ ] Mọi KPI có nguồn, thời gian và định nghĩa.
- [ ] Forecast tách rõ dữ liệu thực tế và giả định.
- [ ] Roadmap có dependency, owner và tiêu chí hoàn thành.

