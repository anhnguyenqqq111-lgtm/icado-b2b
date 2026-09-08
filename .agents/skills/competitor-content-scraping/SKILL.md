---
name: competitor-content-scraping
description: >
  Scrape and extract DOM structure (H1, H2, H3) and core content from specific competitor URLs.
  Tách biệt logic cào dữ liệu thành một module độc lập, có khả năng xử lý anti-bot bằng browser tool.
  Triggers: scrape url, cào dữ liệu đối thủ, dom extract, /scrape-competitor
---

# Competitor Content Scraping

## Purpose
Tập trung chuyên sâu vào nhiệm vụ kỹ thuật: truy cập một URL đối thủ cụ thể, vượt qua các rào cản kỹ thuật (anti-bot, pop-up, lazy-load), và trích xuất chính xác cấu trúc DOM (H1, H2, H3) cùng nội dung cốt lõi. Skill này đóng vai trò là "công cụ thu thập" cho `analyzing-competitors` hoặc bất kỳ workflow nào cần cào dữ liệu sạch.

---

## Mandatory Inputs
- URL đích cần cào dữ liệu
- Chế độ cào: "Headings Only" (chỉ lấy cấu trúc DOM) hoặc "Full Content" (lấy cả nội dung text)

---

## Phase 1: Thử nghiệm truy cập tĩnh (Static Fetch)

### 1.1 Sử dụng `web page extraction`
- Thử cào dữ liệu nhanh bằng tool `web page extraction`.
- **Kiểm tra kết quả**: 
  - Nếu trả về HTML chuẩn có chứa nội dung bài viết $\rightarrow$ Chuyển sang Phase 3.
  - Nếu trả về lỗi 403, 404 giả, Cloudflare block, màn hình Captcha, hoặc HTML trống (do CSR/React/Vue render client-side) $\rightarrow$ Thất bại, chuyển sang Phase 2.

---

## Phase 2: Truy cập động qua Browser Subagent (Dynamic Fetch)

Nếu Phase 1 thất bại, BẮT BUỘC sử dụng `browser tool` để giả lập người dùng thật:

### 2.1 Cấu hình Subagent
- **Task**: "Truy cập URL `[URL]`. Đợi trang load hoàn toàn. Cuộn từ từ xuống cuối trang để trigger toàn bộ nội dung lazy-load. Đọc cấu trúc DOM (H1, H2, H3) và trích xuất. Trả về kết quả dưới dạng Markdown."
- **Xử lý Pop-up**: Subagent phải tự động tìm và click đóng (X) các pop-up quảng cáo, newsletter che màn hình.

---

## Phase 3: Xử lý và Trích xuất Dữ liệu

### 3.1 Extract DOM Headings (Cấu trúc H1-H3)
- Quét toàn bộ thẻ tiêu đề.
- **Giữ nguyên 100% text gốc**, tuyệt đối không dịch thuật, không tóm tắt, không viết lại.
- Thể hiện tính phân cấp (Hierarchy) rõ ràng.

### 3.2 Lọc rác (Noise Filtering)
- Bỏ qua các H2/H3 thuộc Sidebar (Bài viết mới, Danh mục).
- Bỏ qua các H2/H3 thuộc Footer (Thông tin liên hệ, Chính sách bảo mật).
- Chỉ giữ lại các heading nằm trong block nội dung bài viết chính (`<article>`, `<div class="content">`, v.v.).

---

## Phase 4: Output File

Lưu kết quả vào thư mục `competitors/` với định dạng chuẩn:

```markdown
# DOM Scrape: [Tên trang web / Brand]
> Nguồn: `[URL gốc]`
> Thời gian cào: [DD/MM/YYYY]

## Cấu trúc Heading Gốc
- **H1**: [Text]
  - **H2**: [Text]
    - **H3**: [Text]
  - **H2**: [Text]

## Nhận xét kỹ thuật
- [Ví dụ: Bài viết sử dụng nhiều bảng biểu so sánh]
- [Ví dụ: Có module tính toán tài chính]
```

---

## Self-Check (Đọc trước khi thực hiện)
- [ ] Nếu dùng `web page extraction` thấy toàn code JS mà không có text → Phải chuyển ngay sang `browser tool`.
- [ ] Đã cuộn trang (scroll) chưa? Nhiều trang B2B/Tài chính lazy-load text ở nửa dưới.
- [ ] Output có dính heading của Footer không? (Ví dụ: "Về chúng tôi", "Chính sách") → Bắt buộc xóa bỏ các heading rác này.
