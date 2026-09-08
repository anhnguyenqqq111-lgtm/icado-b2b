---
name: keyword-expansion
description: >
  Mở rộng bộ từ khóa từ keyword chính sang các biến thể đuôi dài, autocomplete, PAA,
  và related searches. Phân loại theo Intent và ước lượng mức độ ưu tiên để chọn lọc đưa vào outline.
  Khác với extracting-keywords (đào sâu entity): skill này mở rộng bề ngang để không bỏ sót từ khóa.
  Triggers: keyword expansion, mở rộng từ khóa, long tail, PAA research, /expand-keywords
---

# Keyword Expansion — Home Credit Vietnam

## Purpose
Từ keyword chính và keyword phụ ban đầu (từ Planning), mở rộng thành bộ từ khóa đầy đủ theo 5 nguồn dữ liệu thực tế. Đầu ra là danh sách phân loại theo Intent và mức độ ưu tiên, sẵn sàng đưa vào Outline và tối ưu bài viết.

> **Phân biệt với `extracting-keywords`**:
> - `extracting-keywords` → Đào sâu Entity Graph (Ai/Cái gì liên quan đến keyword?)
> - `keyword-expansion` → Mở rộng bề ngang (Người ta tìm kiếm theo cách nào khác?)

---

## Mandatory Inputs

```
REQUIRED:
- Keyword chính [từ Planning]
- Keyword phụ ban đầu (nếu có) [từ Planning]

OPTIONAL (tăng độ chính xác):
- search-intent.md [để tránh chọn keyword lệch intent]
```

---

## Phase 1: Thu thập từ 5 nguồn thực tế

Thực hiện **tuần tự** từng nguồn, ghi nhận kết quả thô trước khi lọc:

### Nguồn 1: Google Autocomplete
Dùng `web search` hoặc `browser tool` với pattern:
```
"[keyword chính] "         → kéo danh sách gợi ý Google (A-Z variations)
"[keyword chính] là"
"[keyword chính] có"
"[keyword chính] bao nhiêu"
"[keyword chính] như thế nào"
"[keyword chính] ở đâu"
```
> Ghi nhận tất cả gợi ý xuất hiện — đây là bằng chứng người dùng thực sự tìm kiếm.

### Nguồn 2: People Also Ask (PAA)
Tìm kiếm keyword chính trên Google, thu thập toàn bộ câu hỏi trong hộp "People Also Ask":
- Ghi nhận CHÍNH XÁC câu hỏi (không paraphrase)
- PAA = tín hiệu intent mạnh nhất, ưu tiên cao cho FAQ section

### Nguồn 3: Related Searches (Tìm kiếm liên quan)
Cuộn xuống cuối trang Google SERP, lấy danh sách "Searches related to [keyword]":
- Thường là các long-tail và biến thể ngữ nghĩa phổ biến

### Nguồn 4: Competitor Heading Mining
Từ `competitors/*.md` (đã có từ analyzing-competitors), quét các H2/H3 chứa biến thể keyword:
- Cách đối thủ đặt heading = cách người dùng tìm kiếm thực tế
- Trích xuất thêm từ khóa chưa có trong Nguồn 1-3

### Nguồn 5: LSI Semantic Expansion (tùy chọn nâng cao)
Dùng `web search` với toán tử:
```
"[keyword chính]" định nghĩa
"[keyword chính]" cách tính
"[keyword chính]" so sánh
site:homecredit.vn "[keyword chính]"    ← Xem HCVN đã dùng từ khóa gì
```

---

## Phase 2: Lọc và Phân loại

### 2.1 Loại bỏ từ khóa không phù hợp

```
LOẠI:
❌ Từ khóa trùng hoàn toàn keyword chính (tautology)
❌ Từ khóa của đối thủ trực tiếp (VD: "vay Mcredit", "FE Credit lãi suất")
❌ Từ khóa địa lý quá cụ thể không liên quan (VD: "vay tiền Bắc Giang")
❌ Từ khóa search volume quá nhỏ và không có giá trị nội dung
❌ Từ khóa lệch hoàn toàn intent so với search-intent.md
```

### 2.2 Phân loại theo Intent và Độ ưu tiên

| Nhóm | Intent | Độ ưu tiên | Đưa vào đâu trong bài? |
|---|---|---|---|
| **KW Chính** | Primary | 🔴 Bắt buộc | Title, H1, Meta, H2 đầu tiên |
| **KW Phụ — Commercial** | Commercial / Compare | 🔴 Cao | H2 hoặc H3 chính, bảng so sánh |
| **KW Phụ — Informational** | Know / Know-Simple | 🟠 Trung bình | H3, nội dung đoạn văn, FAQ |
| **KW Đuôi dài — PAA** | Do / Know-Detailed | 🟠 Trung bình | FAQ section (5 câu), H3 phụ |
| **KW LSI / Biến thể** | Context signal | 🟡 Thấp | Rải trong nội dung, alt text |

### 2.3 Ước lượng mức độ ưu tiên

Chấm **Priority Score** cho từng keyword từ 1-5 dựa trên:
- **Relevance** (1-2): Mức độ liên quan trực tiếp đến topic
- **Searchability** (1-2): Có xuất hiện trong Autocomplete / PAA không?
- **HCVN fit** (1): Có thể lồng ghép tự nhiên vào bài tài chính không?

```
Priority 5 = Bắt buộc đưa vào outline
Priority 3-4 = Nên đưa, ưu tiên sau KW chính
Priority 1-2 = Dùng trong nội dung đoạn, không cần heading riêng
```

---

## Phase 3: Output

### Output File: Phần thêm vào `research.md`

Inject kết quả vào cuối `research.md` hiện có (hoặc tạo mới nếu chưa có):

```markdown
## Keyword Expansion Map

### KW Chính & Phụ Bắt buộc (Priority 4-5)
| Keyword | Nhóm | Intent | Priority | Ghi chú |
|---|---|---|---|---|
| [keyword chính] | Primary | [Intent] | 5 | Title + H1 + Meta |
| [kw phụ 1] | Commercial | Compare | 4 | H2 hoặc bảng |
| [kw phụ 2] | Informational | Know | 4 | H3 hoặc FAQ |

### KW Đuôi dài & PAA (Priority 2-3)
| Câu hỏi PAA / Long-tail | Nguồn | Priority | Đưa vào FAQ? |
|---|---|---|---|
| [câu hỏi PAA 1] | Google PAA | 3 | ✅ FAQ câu 1 |
| [câu hỏi PAA 2] | Google PAA | 3 | ✅ FAQ câu 2 |
| [long-tail 1] | Autocomplete | 2 | ⬜ Nội dung đoạn văn |

### KW LSI / Ngữ cảnh (Priority 1)
[biến thể 1], [biến thể 2], [biến thể 3]...
(Rải tự nhiên trong nội dung, không cần heading riêng)

### KW Loại bỏ (Rejected)
| Keyword | Lý do loại |
|---|---|
| [keyword X] | Lệch intent / Đối thủ trực tiếp / Volume quá nhỏ |
```

---

## Kết nối với các skill khác trong Pipeline

```
analyzing-search-intent  →  Cung cấp True Intent làm bộ lọc cho Phase 2
          ↓
keyword-expansion        →  Mở rộng bộ từ khóa theo 5 nguồn
          ↓
extracting-keywords      →  Đào sâu Entity Map và Knowledge Graph
          ↓
content-gap-analysis     →  Dùng KW expansion để kiểm tra đối thủ đã phủ gì
          ↓
generating-outlines-hc   →  Gán từng KW vào đúng vị trí trong outline
```

---

## Self-Check (Đọc trước khi chạy)

- [ ] Đã tìm kiếm ít nhất 6 pattern autocomplete khác nhau (không chỉ 1 pattern).
- [ ] Đã ghi nhận CHÍNH XÁC câu hỏi PAA — không paraphrase, không dịch.
- [ ] Đã kiểm tra từ khóa loại bỏ: không nhầm "từ khóa ít dùng" với "từ khóa lệch intent".
- [ ] Không đưa tên đối thủ tài chính (Mcredit, FE Credit, VPBank...) vào danh sách KW phụ.
- [ ] Priority Score được chấm logic, không phải tất cả đều Priority 5.
- [ ] Output inject vào `research.md` đúng format, không ghi đè nội dung cũ.
