---
name: generating-table-of-contents
description: >
  Generates a Table of Contents (Mục lục) anchor reference table for CMS copy-page workflows.
  Use when asked to tạo mục lục, generate TOC, or add anchor links to a bài viết for upload to WordPress/TinyMCE.
---

# Generating Table of Contents (TOC) - CMS Anchor Reference

Skill này tạo ra **bảng tham chiếu anchor** (Anchor Reference Table) phục vụ quy trình **copy page lên CMS** (WordPress, TinyMCE, Gutenberg).

---

## 1. Quy tắc đặt ID Anchor Link (Naming Convention)

ID cho mỗi mục được chuẩn hóa theo format:
`#[Số_Mục_Bỏ_Dấu_Chấm]_[Tên_Heading_Không_Dấu_Viết_Hoa_Chữ_Cái_Đầu_Nối_Gạch_Dưới]`

**Ví dụ quy đổi:**
- `1. Tiêu chí chọn vợt pickleball` → `#1_Tieu_chi_chon_vot_pickleball`
- `2.3. Vợt pickleball Joola` → `#23_Vot_pickleball_Joola`
- `5. Câu hỏi thường gặp (FAQ)` → `#5_Cau_hoi_thuong_gap_FAQ`

**Lưu ý bắt buộc:**
- Bỏ dấu chấm trong số mục: `2.3` → `23`
- Bỏ hoàn toàn dấu tiếng Việt
- Bỏ ký tự đặc biệt `()`, `:`, `-` trong tên
- Dùng gạch dưới `_` nối các từ, không dùng gạch ngang `-`

---

## 2. Deliverable: Bảng Anchor Reference

Output của skill là một **Markdown Table** với 2 cột:

```markdown
### Mục lục (Anchor Reference - Dán vào ô URL khi tạo link trên CMS)

| Tên mục (Text to display) | Anchor URL |
|---|---|
| 1. Tiêu chí chọn vợt pickleball chuẩn kỹ thuật cho nam và nữ | `#1_Tieu_chi_chon_vot_pickleball_chuan_ky_thuat_cho_nam_va_nu` |
| 1.1. Trọng lượng vợt và phân bổ lực cổ tay | `#11_Trong_luong_vot_va_phan_bo_luc_co_tay` |
| 2. Top 6 thương hiệu vợt pickleball đáng mua nhất 2026 | `#2_Top_6_thuong_hieu_vot_pickleball_dang_mua_nhat_2026` |
| 5. Câu hỏi thường gặp (FAQ) khi chọn vợt pickleball | `#5_Cau_hoi_thuong_gap_FAQ_khi_chon_vot_pickleball` |
```

**Tại sao dùng bảng tham chiếu thay vì hyperlink `[text](#anchor)`?**
- Khi copy từ Markdown Preview / VSCode IDE sang CMS, các link dạng `[text](#anchor)` bị IDE tự chèn tiền tố đường dẫn cục bộ (`vscode-resource.vscode-cdn.net/...#anchor`).
- Bảng tham chiếu chỉ chứa text thuần và anchor string dạng code, hoàn toàn an toàn khi copy.

---

## 3. Cách dùng trên CMS (WordPress / TinyMCE)

**Bước 1:** Trên trang bài viết CMS, bôi đen tên mục (ví dụ: `6. Câu hỏi thường gặp (FAQ) khi tập gym tại nhà`).

**Bước 2:** Nhấn nút **Insert/Edit Link** → hộp thoại Insert Link hiện ra.

**Bước 3:** Dán anchor URL từ cột phải của bảng vào ô **URL** (ví dụ: `#6_Cau_hoi_thuong_gap_FAQ_khi_tap_gym_tai_nha`).

**Bước 4:** Đặt **Open link in** → `Current window` → nhấn **Save**.

---

## 4. Gắn thẻ `id` vào Heading trong thân bài

Các thẻ Heading H2/H3 trong thân bài viết (`article.md`) phải sử dụng HTML tag kèm `id`:

```html
<h2 id="1_Tieu_chi_chon_vot_pickleball_chuan_ky_thuat_cho_nam_va_nu">1. Tiêu Chí Chọn Vợt Pickleball Chuẩn Kỹ Thuật Cho Nam Và Nữ</h2>

<h3 id="23_Vot_pickleball_Joola">2.3. Vợt Pickleball JOOLA - Tốc độ và độ xoáy dẫn đầu</h3>
```

---

## 5. Checklist Kiểm Tra
1. ✅ Không có dấu chấm trong tiền tố số (`23_` thay vì `2.3_`).
2. ✅ Không có dấu tiếng Việt và ký tự đặc biệt trong ID.
3. ✅ Mọi anchor URL trong bảng tham chiếu đều có thẻ Heading tương ứng mang đúng `id`.
4. ✅ Output là Markdown Table (không phải hyperlink `[text](url)`) để tránh lỗi vscode-cdn.
5. ✅ Chỉ liệt kê H2 và H3, bỏ qua H4/H5/H6.
