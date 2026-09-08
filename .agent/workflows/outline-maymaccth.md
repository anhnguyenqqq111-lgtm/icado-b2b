# Premium Semantic SEO Outline Workflow (May Mặc CTH)

Pipeline tự động tạo Outline nội dung chuẩn B2B Local SEO cho **May Mặc CTH — Xưởng may đồng phục Hải Phòng**.
Định dạng đầu ra BẮT BUỘC theo cấu trúc **Bảng (Table)** chuyên sâu.
Command: `/outline-maymaccth [keyword chính] [keyword phụ 1] [keyword phụ 2] ...`

## Pipeline Steps

**[RULE 0 - MANDATORY] BẮT BUỘC SỬ DỤNG BROWSER & SO SÁNH ĐỐI THỦ ĐANG LIVE**:
- **Bắt buộc sử dụng `browser tool`** để tìm kiếm trên Google SERP thực tế và truy cập trực tiếp các URL của Top 3–5 xưởng may đối thủ (Đồng Phục Bốn Mùa, Hải Anh, Ong Vàng...).
- **Trích xuất dữ liệu Live**: Quét toàn bộ DOM Headings (H1, H2, H3), nội dung bài viết, bảng giá may, phân loại chất liệu vải, bảng chọn size.
- **So sánh đối chiếu trực tiếp**: Bắt buộc xuất ra `Competitor Analysis Table` kèm trích dẫn thực tế (Quotes) từ bài đối thủ.

**[PHASE 0] NẠP DỮ LIỆU THƯƠNG HIỆU**:
Trước khi tạo outline, Agent PHẢI nạp đầy đủ context từ các file:
1. `data/reference/persona-brand/MayMacCTH/content-rules.md`
2. `data/reference/persona-brand/MayMacCTH/central-entity-MayMacCTH.md`
3. `.agent/skills/brands/maymaccth/maymaccth-outline-rules/SKILL.md`

---

### Phase 1: Keyword & Intent Mapping
**Skills sử dụng**: `keyword-strategy-mapping`, `keyword-expansion`
**Output Bắt buộc**: `Keyword Strategy Table` (5 trường: Main keyword, Keyword phụ, Google Suggest, LSI Keyword, PAA).

---

### Phase 2: Competitor Intelligence
**Skills sử dụng**: `competitor-outline-intelligence`
**Output Bắt buộc**: `Competitor Analysis Table` (7 cột có quote live trích từ bài đối thủ).

---

### Phase 3: Premium Outline Development
**Skills sử dụng**: `maymaccth-outline-rules`, `generating-outlines-maymaccth`, `internal-link-recommendation`
**Output Bắt buộc**: `Outline Candidate Table` (8 cột, nội dung diễn giải định dạng gạch đầu dòng bullet points chuyên sâu về chất liệu và kỹ thuật may).

---

### Phase 4: Quality Assurance (QA)
**Skills sử dụng**: `outline-quality-scoring`, `rechecking-facts`, `enforcing-zero-flair`
**Nhiệm vụ**: Thẩm định độ chính xác thông số kỹ thuật vải (GSM, co giãn 2c/4c), bảng chọn size, tín hiệu địa phương Hải Phòng. Chấm điểm QA Score $\ge 80$.

---

### Ghi nhận & Xuất bản: 
- Xuất toàn bộ 3 Bảng ra file `clients/MayMacCTH/brands/MayMacCTH/keywords/[keyword-slug]/outline.md`.
- Thông báo kết quả cho user.
