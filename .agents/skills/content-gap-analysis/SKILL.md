---
name: content-gap-analysis
description: >
  Phân tích khoảng trống nội dung (Content Gap) và kiểm tra khả năng triệt tiêu từ khóa nội bộ (Keyword Cannibalization).
  So sánh coverage của HCVN với đối thủ để tìm lợi thế. Rà soát kho 180+ bài hiện có để ngăn trùng lặp.
  Triggers: content gap, phân tích khoảng trống, cannibalization check, trùng từ khóa, /gap-analysis
---

# Content Gap Analysis & Cannibalization Check — Home Credit Vietnam

## Purpose
Thực hiện 2 nhiệm vụ song song trước khi xây dựng outline:
1. **Content Gap Analysis**: Xác định những gì đối thủ đã viết mà HCVN chưa phủ → tạo lợi thế cạnh tranh.
2. **Cannibalization Check**: Xác định bài viết nào trong kho 180+ bài của HCVN đang cạnh tranh cùng từ khóa mục tiêu → quyết định viết mới hay cập nhật bài cũ.

---

## Mandatory Inputs

```
REQUIRED:
- Keyword chính + danh sách keyword phụ [từ Planning]
- competitor-insights.md [từ analyzing-competitors]
- competitors/competitor_[N]_*.md (ít nhất 3 file) [từ analyzing-competitors]

OPTIONAL (tăng độ chính xác):
- research.md [từ extracting-keywords]
- search-intent.md [từ analyzing-search-intent]
```

---

## Phase 1: Cannibalization Check (CHẠY TRƯỚC — Quyết định "Viết mới hay Cập nhật?")

> **Lý do chạy trước**: Nếu phát hiện bài trùng → dừng sản xuất bài mới, chuyển sang cập nhật bài cũ. Tránh lãng phí nguồn lực.

### 1.1 Scan kho bài hiện có

Thực hiện theo thứ tự:

**Bước 1 — Tìm folder trùng slug**:
```bash
ls clients/Home-Credit/brands/Home-Credit/keywords/ | grep -i "[keyword-slug]"
```

**Bước 2 — Tìm theo từ khóa chính trong Title của tất cả outline.md**:
```bash
grep -r -l "[keyword chính]" clients/Home-Credit/brands/Home-Credit/keywords/*/outline.md 2>/dev/null
grep -r -l "[keyword chính]" clients/Home-Credit/brands/Home-Credit/keywords/*/article.md 2>/dev/null
```

**Bước 3 — Tìm theo các từ khóa phụ quan trọng** (lặp lại Bước 2 cho từng KW phụ).

### 1.2 Phân loại kết quả Cannibalization

```
KẾT QUẢ A: Không tìm thấy bài trùng
    → Verdict: "No Cannibalization — Safe to create new article"
    → Ghi nhận vào gap-analysis-report.md
    → Tiếp tục Phase 2

KẾT QUẢ B: Tìm thấy 1 bài trùng có article.md hoàn chỉnh
    → Mở bài đó, đọc Title + H2 structure
    → Verdict: "Cannibalization Risk — Recommend Update instead of Create"
    → Báo cáo cho user: bài trùng là [URL/slug], nội dung trùng ở [danh sách heading]
    → DỪNG workflow, hỏi user: "Cập nhật bài cũ hay vẫn tạo bài mới với góc nhìn khác biệt?"

KẾT QUẢ C: Tìm thấy bài trùng nhưng chỉ có outline.md, không có article.md
    → Verdict: "Partial Cannibalization — Bài cũ chưa hoàn chỉnh"
    → Gợi ý: Xem xét hoàn thiện bài cũ thay vì tạo bài mới
    → Hỏi user quyết định

KẾT QUẢ D: Tìm thấy nhiều bài có keyword phụ trùng nhau
    → Ghi nhận tất cả vào báo cáo, phân tích mức độ trùng lặp
    → Nếu < 30% overlap: Safe to proceed
    → Nếu >= 30% overlap: Cảnh báo, đề xuất hợp nhất hoặc phân biệt rõ angle
```

---

## Phase 2: Content Gap Analysis (So sánh đối thủ vs HCVN)

### 2.1 Xây dựng Ma trận Coverage

Từ dữ liệu trong `competitor-insights.md` và `competitors/*.md`, tạo bảng ma trận:

```markdown
| Topic / Subtopic | Đối thủ 1 | Đối thủ 2 | Đối thủ 3 | HCVN (Bài cũ nếu có) | Gap? |
|---|---|---|---|---|---|
| [Chủ đề A] | ✅ H2 | ✅ H2 | ✅ H3 | ❌ | 🔴 CRITICAL GAP |
| [Chủ đề B] | ✅ H2 | ❌ | ✅ H2 | ✅ outline | ⚠️ PARTIAL |
| [Chủ đề C] | ❌ | ❌ | ❌ | ❌ | 🟢 OPPORTUNITY |
```

**Phân loại Gap**:
- 🔴 **CRITICAL GAP**: Đối thủ có (≥ 2/3), HCVN không có → Bắt buộc đưa vào bài.
- ⚠️ **PARTIAL GAP**: Đối thủ có nhưng chưa đi sâu, HCVN có thể đi sâu hơn → Ưu tiên cao.
- 🟢 **UNIQUE OPPORTUNITY**: Không ai viết → Tạo lợi thế độc quyền, kiểm tra search demand trước.
- ⬜ **SKIP**: Đối thủ có nhưng không phù hợp góc nhìn HCVN.

### 2.2 Phân tích Depth Gap (Độ sâu)

Không chỉ so sánh "có / không có" — còn phân tích **đối thủ viết nông mà HCVN có thể đi sâu hơn**:

| Hạng mục kiểm tra | Câu hỏi cần trả lời |
|---|---|
| **Số liệu định lượng** | Đối thủ có % / VNĐ / ngày cụ thể không, hay chỉ mô tả mơ hồ? |
| **Ví dụ thực tế** | Đối thủ có case study, ví dụ tính toán không, hay chỉ lý thuyết? |
| **Bảng biểu** | Đối thủ có bảng so sánh không, hay chỉ liệt kê đơn giản? |
| **FAQ thực tế** | Đối thủ có trả lời đúng câu hỏi người dùng thực sự hỏi không? |
| **Cập nhật** | Thông tin đối thủ có lỗi thời (> 6 tháng) không? HCVN có thể cập nhật mới hơn? |

### 2.3 Xác định HCVN Unique Angle

Dựa trên kết quả Gap Analysis, xác định **góc nhìn độc quyền của HCVN** mà đối thủ không có:

```
HCVN Unique Advantages (Kiểm tra lần lượt):
✅ Cung cấp bảng tính toán trả góp cụ thể (không có đối thủ nào làm đủ tốt)
✅ Góc nhìn từ phía người dùng vay tiêu dùng thực tế (không phải ngân hàng hay tài chính vĩ mô)
✅ Tích hợp giải pháp tài chính trực tiếp (không chỉ tư vấn thuần lý thuyết)
✅ Số liệu mới nhất từ dịch vụ HCVN (giải ngân trong X giờ, lãi suất Y%...)
```

---

## Phase 3: Synthesis — Tạo Briefing cho Outline

Tổng hợp kết quả 2 Phase thành **Content Strategy Briefing** để truyền sang `04. Outline Development`:

```markdown
## Content Gap & Cannibalization Briefing — [Keyword]

### ✅ Cannibalization Status
- Verdict: [No Cannibalization / Risk / Partial]
- Bài liên quan trong kho: [Slug/URL nếu có]
- Quyết định: [Viết mới / Cập nhật bài cũ]

### 🔴 Critical Gaps (Bắt buộc đưa vào outline)
1. [Topic A] — Tất cả đối thủ có, HCVN chưa phủ
2. [Topic B] — Đối thủ đề cập sơ sài, HCVN cần đi sâu hơn với [số liệu cụ thể]

### 🟢 Unique Opportunities (Lợi thế độc quyền HCVN)
1. [Bảng tính toán trả góp tháng với lãi suất HC]
2. [Thông tin cập nhật mới nhất: chương trình X, điều kiện Y]

### ⬜ Topics to SKIP (Không phù hợp angle HCVN)
1. [Topic X] — Quá kỹ thuật / Không liên quan dịch vụ HC

### 📌 Recommended HCVN Angle
[Một câu mô tả góc nhìn độc quyền: VD: "Góc nhìn người mua thực tế, tập trung vào bảng tính toán tài chính và điều kiện trả góp linh hoạt qua Home Credit"]
```

---

## Output Files

1. **`gap-analysis-report.md`** — Báo cáo đầy đủ Content Gap Matrix + Cannibalization result.
2. **Nội dung inject vào `research.md`** — Phần `## Content Gap` thêm vào cuối file research hiện có (nếu research.md đã tồn tại).

---

## Decision Tree — Tóm tắt Logic

```
START
│
├── [Cannibalization Check]
│   ├── Bài trùng đã có article.md → STOP, báo user, hỏi quyết định
│   ├── Bài trùng chỉ có outline.md → WARN, gợi ý hoàn thiện cũ
│   └── Không trùng → PROCEED
│
└── [Content Gap Analysis]
    ├── Xác định Critical Gaps (🔴) → Mandatory topics cho outline
    ├── Xác định Depth Gaps (⚠️) → Priority topics
    ├── Xác định Opportunities (🟢) → HCVN unique angle
    └── Output: gap-analysis-report.md + Content Strategy Briefing
```

---

## Self-Check (Đọc trước khi chạy)

- [ ] Đã chạy grep với ít nhất 3 biến thể từ khóa (keyword chính, dạng viết tắt, dạng đồng nghĩa phổ biến).
- [ ] Đã đọc heading structure của ít nhất 3 file competitor trước khi lập ma trận.
- [ ] Không gán "CRITICAL GAP" cho topic chỉ có 1/3 đối thủ viết — cần ít nhất 2/3.
- [ ] Đã kiểm tra bài trùng theo cả slug folder lẫn nội dung Title/H2, không chỉ tên thư mục.
- [ ] Content Strategy Briefing đủ cụ thể để outliner có thể dùng trực tiếp, không mơ hồ.
