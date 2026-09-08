# Premium Semantic SEO Outline Workflow (Everest Logistics)

Pipeline tự động tạo Outline nội dung chuẩn B2B Semantic SEO cho **Everest Logistics**.
Định dạng đầu ra BẮT BUỘC theo cấu trúc **Bảng (Table)** chuyên sâu.
Command: `/outline-everest [keyword chính] [keyword phụ 1] [keyword phụ 2] ...`

## Pipeline Steps

**[RULE 0 - MANDATORY] BẮT BUỘC SỬ DỤNG BROWSER & SO SÁNH ĐỐI THỦ ĐANG LIVE**:
- **Bắt buộc sử dụng `browser tool`** để tìm kiếm trên Google SERP thực tế và truy cập trực tiếp các URL của Top 3–5 đối thủ Logistics (Indochina Post, Ratraco, Vinalink...).
- **Trích xuất dữ liệu Live**: Quét toàn bộ DOM Headings (H1, H2, H3), nội dung bài viết, bảng cước, mã HS, quy trình hải quan.
- **So sánh đối chiếu trực tiếp**: Bắt buộc xuất ra `Competitor Analysis Table` kèm trích dẫn thực tế (Quotes) từ bài đối thủ.

**[PHASE 0] NẠP DỮ LIỆU THƯƠNG HIỆU**:
Trước khi tạo outline, Agent PHẢI nạp đầy đủ context từ các file:
1. `data/reference/persona-brand/Everest-Logistics/persona-everest-skill.md`
2. `data/reference/persona-brand/Everest-Logistics/central-entity-Everest-Logistics.md`
3. `.agent/skills/brands/everest-logistics/everest-outline-rules/SKILL.md`

---

### Phase 1: Keyword & Intent Mapping
**Skills sử dụng**: `keyword-strategy-mapping`, `keyword-expansion`
**Output Bắt buộc**: `Keyword Strategy Table` (Bảng phân tích từ khóa gồm: Main keyword, Keyword phụ, Google Suggest, LSI Keyword, PAA).

---

### Phase 2: Competitor Intelligence
**Skills sử dụng**: `competitor-outline-intelligence`
**Output Bắt buộc**: `Competitor Analysis Table` (Bảng phân tích đối thủ gồm 7 cột: `#`, `URL`, `Strengths`, `Weaknesses`, `What We Learn`, `Opportunity`, `Example` có quote live).

---

### Phase 3: Premium Outline Development
**Skills sử dụng**: `everest-outline-rules`, `generating-outlines-everest`, `internal-link-recommendation`
**Output Bắt buộc**: `Outline Candidate Table` (Bảng cấu trúc dàn ý gồm: `#`, `Heading`, `Why`, `Evidence`, `Content Direction`, `Content Format`, `Differentiation`, `So với bài hiện tại`). Nội dung các ô trình bày dạng gạch đầu dòng (bullet points).

---

### Phase 4: Quality Assurance (QA) & Formatting Audit
**Skills sử dụng**: `outline-quality-scoring`, `rechecking-facts`, `enforcing-zero-flair`, `everest-article-audit`
**Nhiệm vụ**: 
- Thẩm định độ chuẩn xác về Incoterms 2020, HS Code, thủ tục xuất nhập khẩu, kiểm tra từ sáo rỗng. Chấm điểm QA Score $\ge 80$.
- **Audit Formatting khi viết bài (`everest-article-audit`)**: Cấm bôi đậm (`**...**`) tràn lan giữa câu/đoạn; cấm dùng code block vẽ sơ đồ hộp ASCII art (`+----+`, `|...|`). Thay thế hoàn toàn bằng Bảng Markdown tiêu chuẩn.

---

### Ghi nhận & Xuất bản: 
- Xuất toàn bộ 3 Bảng ra file `clients/Everest-Logistics/brands/Everest-Logistics/keywords/[keyword-slug]/outline.md`.
- Khi triển khai `article.md`, bắt buộc chạy qua bước kiểm duyệt định dạng `everest-article-audit`.
- Thông báo kết quả cho user.

