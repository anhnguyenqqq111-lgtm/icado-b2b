# Thiết kế website Everest Logistics — Strategy đến implementation

> Mục tiêu: hiểu cách chuyển nghiên cứu SEO và nhu cầu B2B thành information architecture, design system và website có khả năng tạo lead.

## 1. Bài toán thiết kế

Website không chỉ giới thiệu công ty mà phải giúp khách B2B nhanh chóng:

- xác định đúng dịch vụ;
- biết cần chuẩn bị thông tin/chứng từ gì;
- hiểu quy trình, chi phí và rủi ro;
- tin vào năng lực thực tế;
- gửi một yêu cầu báo giá đủ điều kiện.

## 2. Kiến trúc quyết định

```text
Business goal: qualified leads
  ├─ User need: phương thức vận chuyển
  ├─ User need: thủ tục cần xử lý
  ├─ User need: loại hàng đặc biệt
  ├─ User need: tuyến vận chuyển
  └─ User need: dịch vụ trọn gói
        ↓
Information architecture
        ↓
Page templates + components + CTA system
        ↓
Static prototype / Next.js implementation
```

## 3. Các nguyên tắc có thể tái sử dụng

### Navigation theo mental model khách hàng

Menu cấp một giữ 6–7 nhóm. Mega menu gom theo nhu cầu mua, không bê nguyên cơ cấu nghiệp vụ nội bộ. Trang kiến thức và trang dịch vụ có intent khác nhau nên không dùng chung vai trò.

### Evidence before decoration

Ưu tiên ảnh dự án thật, tuyến thật, chứng chỉ, case study và KPI đã xác minh. Không dùng số giả, logo khách hàng chưa được phép hoặc testimonial không đúng vai trò.

### CTA theo cấp độ cam kết

- Chính: Nhận báo giá, Trao đổi với chuyên viên.
- Phụ: Xem quy trình, Chuẩn bị thông tin, Xem dự án, Gọi/Zalo.
- Mỗi section chỉ có một hành động trội để giảm cạnh tranh chú ý.

### Form là một phần của service design

Form nhanh thu thập điểm đi, điểm đến, loại hàng, phương thức và số điện thoại. Form chi tiết cần conditional fields theo dịch vụ; mục tiêu là tạo lead có đủ dữ liệu để sales phản hồi.

### Design system phục vụ triển khai

Prototype tĩnh trong `projects/everest-logistics/site/` dùng `assets/site.css`, `assets/site.js`, `design-system.html`; bản Next.js trong `projects/everest-logistics/next-app/` tách `Header`, `HeroSlider`, `ContactForm`, `Footer` và data trong `lib/services.js`. Đây là chuyển đổi từ page-specific markup sang component reuse.

## 4. Hai hướng implementation

| Hướng | Điểm mạnh | Rủi ro | Dùng khi |
|---|---|---|---|
| Static HTML/CSS/JS | Nhanh, dễ demo, ít dependency | Trùng layout giữa nhiều trang, khó quản trị nội dung | Prototype hoặc site nhỏ |
| Next.js component | Reuse tốt, route/data rõ, dễ mở rộng | Cần build/runtime và quy ước code | Website sản xuất hoặc nhiều template |

## 5. Quy trình tái tạo

1. Audit site và dữ liệu keyword; tách commercial intent khỏi informational intent.
2. Xác minh dịch vụ/tuyến/loại hàng doanh nghiệp thật sự cung cấp.
3. Viết sitemap và page inventory theo P0/P1/P2.
4. Thiết kế conversion journey trước wireframe trang chủ.
5. Tạo token cho màu, type, spacing, radius và breakpoint.
6. Tạo component states: default, hover, focus, error, success, loading.
7. Prototype trang chủ + landing page dịch vụ + form báo giá trên mobile/desktop.
8. Chọn source-of-truth và triển khai static hoặc Next.js.
9. Kiểm tra accessibility, responsive, form validation, analytics event và SEO technical.

## 6. Lỗi cấu trúc hiện tại cần tránh

- Các bản sao trước đó đã được đưa vào archive; `projects/everest-logistics/` hiện là vị trí project rõ nhất nhưng vẫn cần xác nhận canonical bằng diff/hash.
- Có cả zip, build output và source trong cùng workspace; nên tách `src/`, `dist/`, `releases/`.
- Cần kiểm tra xem `projects/everest-logistics/next-app/` hay `site/` là hướng bàn giao cuối.
- Service pages placeholder ngắn chưa đủ nội dung production.
- Dữ liệu năng lực và contact phải được phía Everest xác minh trước publish.

## 7. Checklist QA web

- Menu và keyboard navigation hoạt động ở 320px, tablet và desktop.
- Màu chữ đạt WCAG AA, focus state nhìn thấy rõ.
- Form có label, error copy, success state và chống submit lặp.
- CTA call/Zalo/form được gắn analytics event.
- Một URL có một H1; canonical, metadata, robots và sitemap đúng.
- Không có placeholder hotline, testimonial hoặc business metric.
