# Kế hoạch xử lý indexing sau migration — ICADO.vn

**Website:** https://icado.vn/  
**Bối cảnh:** Website vừa chuyển nền tảng/cấu trúc  
**Mục tiêu:** Bảo toàn tín hiệu SEO cũ, giúp Google nhận đúng URL mới và ưu tiên index các trang có giá trị kinh doanh.

## 1. Hiện trạng Google Search Console

| Nhóm trạng thái | Số URL | Mức ưu tiên | Nhận định ban đầu |
|---|---:|---:|---|
| Excluded by `noindex` tag | 2.786 | P1 | Có thể chủ yếu là filter, tìm kiếm, tài khoản hoặc URL kỹ thuật; cần phân loại trước khi sửa |
| Page with redirect | 1.105 | P2 | Thường bình thường sau migration nếu redirect đúng đích |
| Crawled – currently not indexed | 2.082 | **P0** | Nhóm cần phân tích sâu nhất vì Google đã crawl nhưng chưa chọn index |
| Duplicate without user-selected canonical | 55 | P1 | Thiếu hoặc xung đột tín hiệu canonical |
| Alternate page with proper canonical | 27 | P3 | Bình thường nếu canonical được khai báo đúng |
| Not found (404) | 22 | P1 | Cần kiểm tra traffic, backlink, internal link và URL thay thế |
| Blocked due to other 4xx issue | 2 | **P0** | Có thể liên quan 401, 403 hoặc 429; cần xử lý ngay nếu là URL SEO |
| Blocked by robots.txt | 1 | P1 | Cần xác định URL cần index hay URL kỹ thuật |
| Duplicate, Google chose different canonical | 3 | P1 | Tín hiệu canonical, sitemap và internal link có thể chưa thống nhất |
| Server error (5xx) | 0 | Theo dõi | Chưa phát hiện lỗi máy chủ trong báo cáo hiện tại |

> Lưu ý: Tổng số URL trong các nhóm loại trừ không đồng nghĩa với tổng số lỗi. URL redirect, `noindex` chủ động và alternate canonical có thể là trạng thái hợp lệ.

## 2. Nguyên tắc xử lý

1. Không request indexing hàng loạt khi chưa sửa nguyên nhân gốc.
2. Không redirect toàn bộ URL cũ hoặc URL 404 về trang chủ.
3. Sitemap chỉ chứa URL trả về `200`, được phép index và canonical về chính nó.
4. Internal link phải trỏ thẳng đến URL chuẩn cuối cùng, không đi qua redirect.
5. Mỗi URL indexable phải thống nhất các tín hiệu: HTTP status, canonical, sitemap, internal link, breadcrumb và schema.
6. Giữ redirect migration tối thiểu một năm; nên giữ lâu dài với URL còn backlink hoặc traffic.

## 3. Kế hoạch triển khai

### Giai đoạn 1 — Thu thập dữ liệu và phân loại URL

**Thời gian:** Ngày 1–2  
**Owner đề xuất:** SEO + Developer

#### Công việc

- Xuất toàn bộ URL của từng nhóm trạng thái từ Google Search Console.
- Xuất sitemap hiện tại và danh sách URL từ sitemap cũ nếu còn lưu.
- Crawl toàn website mới, bao gồm status code, canonical, robots meta, H1, title và độ sâu internal link.
- Thu thập danh sách URL cũ từ:
  - Sitemap cũ.
  - Google Analytics và Search Console trước migration.
  - Backlink có giá trị.
  - Crawl hoặc database website cũ.
- Gắn loại trang cho từng URL: sản phẩm, danh mục, thương hiệu, bài viết, landing page, filter, tìm kiếm, tài khoản hoặc URL kỹ thuật.
- Đánh dấu URL có click, impression, conversion hoặc backlink trước migration.

#### Đầu ra

- File URL inventory tổng.
- Bảng mapping URL cũ → URL mới.
- Danh sách URL P0/P1 theo giá trị kinh doanh.

#### Tiêu chí nghiệm thu

- 100% URL cũ quan trọng có phương án: giữ nguyên, redirect, canonical, `noindex`, 404 hoặc 410.
- Không có URL giá trị cao bị bỏ qua vì chỉ nhìn vào tổng số URL trong GSC.

### Giai đoạn 2 — Xử lý lỗi truy cập P0

**Thời gian:** Ngày 1–3  
**Owner đề xuất:** Developer/DevOps

#### Blocked due to other 4xx — 2 URL

- Xác định chính xác mã phản hồi: 401, 403, 429 hoặc mã khác.
- Kiểm tra CDN, firewall, WAF, rate limit và rule chống bot.
- Nếu URL cần SEO, đảm bảo Googlebot nhận nội dung và HTTP `200`.
- Nếu URL cần đăng nhập hoặc là tài nguyên riêng tư, giữ nguyên nhưng loại khỏi sitemap và internal link công khai.

#### Blocked by robots.txt — 1 URL

- Nếu là sản phẩm, danh mục, bài viết hoặc landing page cần index: bỏ rule chặn.
- Nếu là admin, cart, checkout, search hoặc khu vực kỹ thuật: giữ rule.
- Không vừa chặn robots.txt vừa kỳ vọng Google đọc `noindex` trên cùng URL.

#### Tiêu chí nghiệm thu

- Tất cả URL SEO quan trọng trả về `200` cho Googlebot.
- Không có URL indexable bị robots.txt hoặc WAF chặn nhầm.

### Giai đoạn 3 — Hoàn thiện redirect migration

**Thời gian:** Ngày 2–5  
**Owner đề xuất:** SEO lập mapping, Developer triển khai

#### Công việc

- Kiểm tra 1.105 URL trong nhóm “Page with redirect”.
- Mỗi URL cũ phải redirect `301` trực tiếp đến URL mới tương đương nhất.
- Loại redirect chain và redirect loop.
- Không redirect hàng loạt URL không liên quan về homepage.
- Chuẩn hóa HTTP/HTTPS, www/non-www, dấu `/`, chữ hoa/chữ thường và URL tham số.
- Cập nhật internal link, menu, breadcrumb, schema và canonical sang URL cuối.
- Loại toàn bộ URL redirect khỏi XML sitemap.
- Duy trì redirect ít nhất 12 tháng; ưu tiên giữ vô thời hạn với URL có backlink/traffic.

#### Mẫu đúng

```text
URL cũ → 301 → URL mới tương đương → 200
```

#### Mẫu cần tránh

```text
URL cũ → 301 → URL trung gian → 301 → URL mới
URL sản phẩm cũ → danh mục không tương đương → trang chủ
Nhiều URL không liên quan → trang chủ
```

#### Tiêu chí nghiệm thu

- Không có redirect loop.
- Không có chain quá một bước trong các URL nội bộ và URL migration quan trọng.
- 100% redirect đích trả về `200`, indexable và canonical về chính nó.

### Giai đoạn 4 — Audit 2.786 URL `noindex`

**Thời gian:** Ngày 3–7  
**Owner đề xuất:** SEO + Developer

#### Nhóm thường được giữ `noindex`

- Tìm kiếm nội bộ.
- Cart, checkout, tài khoản, wishlist và compare.
- URL lọc/sắp xếp không có chiến lược SEO riêng.
- URL tracking hoặc tham số phiên.
- Trang taxonomy rỗng hoặc không có giá trị tìm kiếm.

#### Nhóm cần gỡ `noindex` nếu phát hiện

- Sản phẩm đang kinh doanh.
- Danh mục sản phẩm chính.
- Trang thương hiệu cần SEO.
- Bài blog và landing page có nhu cầu tìm kiếm.
- Trang từng có traffic hoặc backlink trước migration.

#### Kiểm tra kỹ thuật

- Kiểm tra cả `<meta name="robots">` và HTTP `X-Robots-Tag`.
- Kiểm tra template hoặc plugin SEO có áp dụng `noindex` theo loại trang không.
- Không dùng `noindex` thay cho canonical khi mục tiêu là hợp nhất URL trùng lặp.
- URL giữ `noindex` phải được loại khỏi sitemap.

#### Tiêu chí nghiệm thu

- Không có trang sản phẩm, danh mục, thương hiệu, bài viết hoặc landing page quan trọng bị `noindex` ngoài ý muốn.
- 100% URL `noindex` trong sitemap được loại bỏ.

### Giai đoạn 5 — Xử lý canonical và duplicate

**Thời gian:** Ngày 4–7  
**Owner đề xuất:** SEO + Developer

#### Phạm vi

- 55 URL duplicate không có canonical do người dùng chọn.
- 3 URL Google chọn canonical khác khai báo.
- 27 alternate page có canonical đúng để xác nhận nhanh.

#### Công việc

- Mỗi URL chuẩn có self-referencing canonical.
- Phiên bản không cần tồn tại được redirect về URL chuẩn.
- Phiên bản cần tồn tại nhưng trùng nội dung dùng canonical nhất quán.
- Kiểm tra các biến thể:
  - HTTP/HTTPS.
  - www/non-www.
  - Có/không dấu `/`.
  - Chữ hoa/chữ thường.
  - URL có tham số.
  - Một sản phẩm xuất hiện dưới nhiều đường dẫn danh mục.
- Đảm bảo sitemap và internal link chỉ trỏ đến URL canonical.
- Không khai báo canonical khác nhau giữa HTML, HTTP header, sitemap hoặc hreflang.

#### Ma trận tín hiệu chuẩn

| Tín hiệu | Yêu cầu |
|---|---|
| HTTP redirect | Trỏ đến URL chuẩn |
| `rel="canonical"` | Trỏ đến URL chuẩn |
| XML sitemap | Chỉ chứa URL chuẩn |
| Internal link | Trỏ trực tiếp đến URL chuẩn |
| Breadcrumb/schema | Dùng URL chuẩn |
| hreflang nếu có | Trỏ đến URL chuẩn cùng ngôn ngữ tương ứng |

#### Tiêu chí nghiệm thu

- Tất cả tín hiệu canonical thống nhất.
- Không có URL non-canonical trong sitemap.
- Nhóm “Google chose different canonical” giảm sau lần crawl lại.

### Giai đoạn 6 — Xử lý 404 và URL bị loại bỏ

**Thời gian:** Ngày 4–6  
**Owner đề xuất:** SEO + Developer

#### Quy tắc quyết định

| Tình huống | Cách xử lý |
|---|---|
| Có trang mới tương đương | Redirect `301` |
| Nội dung đã hợp nhất vào trang liên quan | Redirect `301` đến trang hợp nhất |
| Sản phẩm dừng nhưng có model kế nhiệm tương đương | Cân nhắc `301` sau khi xác nhận intent |
| Không có trang thay thế phù hợp | Giữ `404` hoặc trả `410` |
| URL sai do internal link | Sửa internal link nguồn |
| URL rác do bot hoặc nhập sai | Giữ `404` |

#### Kiểm tra bắt buộc cho 22 URL

- Click và impression trước migration.
- Backlink và referral traffic.
- Internal link hiện tại.
- Có nằm trong sitemap cũ hoặc sitemap mới không.
- Có URL mới tương đương hay không.

#### Tiêu chí nghiệm thu

- Không còn URL 404 trong sitemap.
- Không còn internal link trỏ đến 404.
- URL có giá trị cũ được chuyển đến trang tương đương, không chuyển đại trà về trang chủ.

### Giai đoạn 7 — Xử lý 2.082 URL “Crawled – currently not indexed”

**Thời gian:** Tuần 2–4  
**Owner đề xuất:** SEO + Content + Developer

#### Bước 1: Phân loại theo template

- Sản phẩm.
- Danh mục.
- Thương hiệu.
- Bài viết.
- Landing page.
- URL filter/tham số hoặc URL kỹ thuật.

#### Bước 2: Ưu tiên theo giá trị

1. URL từng có click, impression, conversion hoặc backlink.
2. Danh mục và sản phẩm tạo doanh thu.
3. Landing page và bài viết phục vụ cluster chiến lược.
4. URL mỏng, trùng hoặc không có nhu cầu tìm kiếm.

#### Checklist trang sản phẩm

- Nội dung không sao chép nguyên mô tả nhà cung cấp.
- Có thông số, lợi ích, hướng dẫn chọn, hình ảnh và thông tin giao dịch hữu ích.
- Biến thể không tạo nhiều URL gần như giống nhau nếu không có nhu cầu tìm kiếm riêng.
- Sản phẩm hết hàng được xử lý theo chính sách nhất quán.
- Canonical đúng và URL có internal link từ danh mục.

#### Checklist trang danh mục

- Không rỗng và có đủ sản phẩm phù hợp.
- Title, H1 và mô tả không trùng với danh mục khác.
- Có nội dung hỗ trợ lựa chọn nhưng không lấn át danh sách sản phẩm.
- Có breadcrumb và internal link hợp lý.
- Không để filter URL cạnh tranh với danh mục chuẩn.

#### Checklist bài viết/landing page

- Đáp ứng intent cụ thể.
- Không cannibalization với bài hoặc trang dịch vụ khác.
- Có thông tin nguyên bản, cập nhật và đủ chiều sâu.
- Có internal link từ trang liên quan.
- Không nằm trong sitemap nếu nội dung không đủ giá trị index.

#### Hành động sau tối ưu

- Gửi lại sitemap đã làm sạch.
- Dùng URL Inspection và Request Indexing cho một nhóm URL quan trọng đại diện.
- Không request indexing đồng loạt 2.082 URL.
- Theo dõi theo template thay vì chỉ theo tổng số URL.

#### Tiêu chí nghiệm thu

- URL quan trọng chuyển dần sang indexed.
- Số URL indexable nhưng không có internal link giảm về 0.
- Sitemap không chứa URL mỏng, trùng, redirect, 404 hoặc `noindex`.

## 4. Kiểm tra XML sitemap

Mỗi URL trong sitemap phải đáp ứng đủ:

- HTTP `200`.
- Không bị robots.txt chặn.
- Không có `noindex`.
- Canonical về chính URL đó.
- Không redirect.
- Có nội dung và giá trị tìm kiếm thực tế.

Tách sitemap theo loại trang nếu website có quy mô lớn:

- Product sitemap.
- Category sitemap.
- Brand sitemap.
- Post sitemap.
- Page/landing-page sitemap.

## 5. Kiểm tra internal link sau migration

- Crawl toàn site để tìm link đến redirect, 404 và URL non-canonical.
- Sửa menu, footer, breadcrumb, bài viết và mô-đun sản phẩm liên quan.
- Bảo đảm danh mục và sản phẩm quan trọng không ở độ sâu click quá lớn.
- Ưu tiên internal link đến URL đang “Crawled – currently not indexed” nhưng có giá trị.
- Không tạo internal link đến URL filter/noindex nếu không phục vụ trải nghiệm người dùng.

## 6. Theo dõi và validation

### Hàng ngày trong 7 ngày đầu

- Lỗi 4xx/5xx mới.
- Khả năng truy cập của Googlebot.
- Redirect loop/chain.
- Trang quan trọng bị `noindex` hoặc canonical sai.
- Traffic và conversion trên landing page chính.

### Hàng tuần trong 4–8 tuần

- Số trang indexed theo từng sitemap/template.
- “Crawled – currently not indexed”.
- “Google chose different canonical”.
- Click, impression, CTR và position so với trước migration.
- Organic sessions và conversion.
- Crawl stats và log Googlebot nếu có quyền truy cập server.

### Khi nào dùng Validate Fix

- Chỉ dùng sau khi lỗi cùng nguyên nhân đã được sửa trên toàn bộ nhóm URL.
- Không Validate Fix cho trạng thái chủ động và hợp lệ như redirect đúng hoặc alternate canonical đúng.
- Với URL quan trọng, kiểm tra trực tiếp bằng URL Inspection trước khi validate cả nhóm.

## 7. Phân công đề xuất

| Vai trò | Trách nhiệm chính |
|---|---|
| SEO Lead | Phân loại URL, mapping migration, canonical, sitemap và ưu tiên kinh doanh |
| Developer | Redirect, status code, robots, meta robots, canonical template và sitemap |
| DevOps | CDN/WAF/firewall, 403/429, log server và ổn định hạ tầng |
| Content | Cải thiện sản phẩm, danh mục, bài viết và xử lý cannibalization |
| Analytics | So sánh traffic, conversion và landing page trước/sau migration |

## 8. Checklist nghiệm thu cuối

- [ ] URL quan trọng không bị `noindex` hoặc robots.txt chặn.
- [ ] Không có URL `4xx`, `5xx`, redirect hoặc non-canonical trong sitemap.
- [ ] URL cũ quan trọng redirect một bước đến trang mới tương đương.
- [ ] Không có redirect loop hoặc redirect hàng loạt về homepage.
- [ ] Canonical, sitemap, internal link, breadcrumb và schema thống nhất.
- [ ] Không còn internal link đến 404 hoặc URL redirect.
- [ ] Mỗi trang chuẩn có self-referencing canonical.
- [ ] Các sitemap mới đã được gửi trong Google Search Console.
- [ ] Đã kiểm tra mẫu URL bằng URL Inspection.
- [ ] Đã thiết lập báo cáo theo dõi ít nhất 8 tuần sau migration.

## 9. Kết luận ưu tiên

Thứ tự xử lý đề xuất cho ICADO:

1. **P0:** 2 URL bị 4xx và các URL quan trọng trong 2.082 URL đã crawl nhưng chưa index.
2. **P1:** Audit `noindex`, 404, robots.txt và các nhóm canonical xung đột.
3. **P2:** Làm sạch redirect, sitemap và internal link sau migration.
4. **P3:** Theo dõi alternate canonical hợp lệ và biến động tự nhiên trong vài tuần Google xử lý migration.

Không đánh giá kết quả migration chỉ bằng tổng số URL bị loại trừ. KPI chính là tỷ lệ index của URL có giá trị, khả năng phục hồi click/impression, organic sessions và conversion trên các trang kinh doanh quan trọng.

## Tài liệu tham chiếu

- [Google Search Central — Site moves and migrations](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)
- [Google Search Central — Canonicalization](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Google Search Central — Block indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing)
