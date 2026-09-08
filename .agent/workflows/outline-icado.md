# Premium Semantic SEO Outline Workflow (ICADO)

Pipeline tự động tạo Outline nội dung chuẩn D2C Sportswear cho **ICADO (Thời trang thể thao & Đồ tập cao cấp)**.
Định dạng đầu ra BẮT BUỘC theo cấu trúc **Bảng (Table)** chuyên sâu.
Command: `/outline-icado [keyword chính] [keyword phụ 1] [keyword phụ 2] ...`

## Pipeline Steps

**[RULE 0 - MANDATORY] BẮT BUỘC SỬ DỤNG BROWSER & SO SÁNH ĐỐI THỦ ĐANG LIVE**:
- **Bắt buộc sử dụng `browser tool`** để tìm kiếm trên Google SERP thực tế và truy cập trực tiếp các URL của Top 3–5 đối thủ đồ tập thể thao (Coolmate, Olaben, Decathlon...).
- **Trích xuất dữ liệu Live**: Quét toàn bộ DOM Headings (H1, H2, H3), thông số chất liệu vải, bảng chọn size, phối đồ tập gym/yoga/chạy bộ.
- **So sánh đối chiếu trực tiếp**: Bắt buộc xuất ra `Competitor Analysis Table` kèm trích dẫn thực tế (Quotes) từ bài đối thủ.

**[PHASE 0] NẠP DỮ LIỆU THƯƠNG HIỆU**:
Trước khi tạo outline, Agent PHẢI nạp đầy đủ context từ các file:
1. `data/reference/persona-brand/ICADO/persona-icado-skill.md`
2. `data/reference/persona-brand/ICADO/central-entity-ICADO.md`
3. `.agent/skills/brands/icado/icado-outline-rules/SKILL.md`

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
**Skills sử dụng**: `icado-outline-rules`, `generating-outlines-icado`, `internal-link-recommendation`
**Output Bắt buộc**: `Outline Candidate Table` (8 cột, nội dung diễn giải định dạng gạch đầu dòng bullet points chuyên sâu về công năng vận động và thẩm mỹ thời trang).

---

### Phase 4: Quality Assurance (QA)
**Skills sử dụng**: `outline-quality-scoring`, `rechecking-facts`, `enforcing-zero-flair`
**Nhiệm vụ**: Thẩm định độ chính xác các thông số chất liệu co giãn 4 chiều, bảng size 3 vòng, tính khoa học của bài viết. Chấm điểm QA Score $\ge 80$.

---

### Ghi nhận & Xuất bản: 
- Xuất toàn bộ 3 Bảng ra file `clients/General-B2B/brands/ICADO/keywords/[keyword-slug]/outline.md`.
- Thông báo kết quả cho user.
