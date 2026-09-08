---
name: client-approval-gate
description: >
  Quy trình chuẩn hóa bàn giao outline, log feedback từ khách hàng, phân loại chỉnh sửa
  (Minor / Major / Reject), cập nhật outline theo góp ý, và khóa outline (Freeze) trước
  khi chuyển sang giai đoạn viết bài.
  Triggers: gửi outline, client approval, duyệt outline, khóa outline, /approve-outline
---

# Client Approval Gate — Home Credit Vietnam

## Purpose
Đây là **Cổng chuyển tiếp quan trọng nhất** trong pipeline HCVN: quản lý quá trình bàn giao outline cho khách hàng, tiếp nhận phản hồi, phân loại và xử lý góp ý, rồi khóa outline (Freeze) để bàn giao cho writer. Không có giai đoạn này, writer có thể viết bài trên nền outline chưa được duyệt.

> **Điều kiện tiên quyết**: Outline phải đạt ≥ 80 điểm từ `outline-quality-scoring` trước khi vào gate này.

---

## Mandatory Inputs

```
REQUIRED:
- outline.md [đã pass outline-quality-scoring ≥ 80 điểm]
- outline-qa-report.md [từ outline-quality-scoring]
- Keyword chính + topic của bài [từ Planning]

OPTIONAL:
- Tên khách hàng / người duyệt [để cá nhân hóa bản giao nộp]
- Deadline phản hồi [nếu có]
```

---

## Phase 1: Chuẩn bị Gói Bàn Giao (Delivery Package)

### 1.1 Kiểm tra điều kiện vào gate

```
IF outline-qa-report.md tồn tại AND score >= 80:
    → PROCEED to Phase 2
ELIF outline-qa-report.md không tồn tại:
    → STOP. Yêu cầu chạy outline-quality-scoring trước.
ELIF score < 80:
    → STOP. Trả outline về Phase 04 (Outline Development) để sửa.
    → Liệt kê lỗi cần sửa từ outline-qa-report.md
```

### 1.2 Tạo Delivery Summary cho khách hàng

Tạo file `approval/delivery-summary.md` trong folder keyword:

```markdown
# Bàn giao Outline — [Keyword Chính]
> Ngày bàn giao: [DD/MM/YYYY]
> QA Score: [X]/100 ✅

## Tóm tắt bài viết
- **Keyword chính**: [keyword]
- **Keyword phụ**: [list]
- **Góc nhìn bài viết**: [1 câu mô tả angle]
- **Độ dài dự kiến**: [1600–1800 từ]
- **Định dạng**: [Toplist / How-to Guide / Comparison / FAQ-heavy]

## Cấu trúc Outline
[Copy toàn bộ danh sách H1 → H2 → H3 từ outline.md, không kèm nội dung gợi ý]

## Dịch vụ HC tích hợp
[Tên dịch vụ + CTA heading đã thiết kế]

## 5 Câu hỏi FAQ
1. [Câu hỏi 1]
2. [Câu hỏi 2]
3. [Câu hỏi 3]
4. [Câu hỏi 4]
5. [Câu hỏi 5]

## Internal Link Plan
[Bảng 3–5 link từ internal-link-recommendation]

## Yêu cầu phản hồi
Vui lòng phản hồi theo format:
- ✅ DUYỆT: [Heading] — Giữ nguyên
- ✏️ SỬA NHỎ: [Heading cũ] → [Heading mới / góp ý]
- 🔄 SỬA LỚN: [Mô tả thay đổi cấu trúc / hướng bài]
- ❌ TỪ CHỐI: [Lý do]

> Deadline phản hồi: [Ngày/Giờ nếu có]
```

---

## Phase 2: Tiếp nhận và Phân loại Feedback

### 2.1 Phân loại phản hồi theo 4 loại

| Loại | Dấu hiệu nhận biết | Xử lý | Ảnh hưởng đến workflow |
|---|---|---|---|
| **✅ APPROVED** | "Duyệt", "OK", "OK hết", không có góp ý sửa | Chuyển sang Phase 3 (Freeze) | Tiến thẳng đến viết bài |
| **✏️ MINOR** | Sửa từ ngữ heading, đổi 1-2 câu FAQ, thêm/bớt 1 H3 | Sửa trực tiếp trong outline.md, không xây lại cấu trúc | Sửa xong → Freeze ngay |
| **🔄 MAJOR** | Đổi góc nhìn bài, thêm/xóa toàn bộ H2, thay dịch vụ match, đổi định dạng bài | Trả về Phase 04 (Outline Dev) + Phase 03 (Strategy) nếu cần | Cần chạy lại outline-quality-scoring sau khi sửa |
| **❌ REJECT** | Từ chối toàn bộ, yêu cầu làm lại từ đầu | Escalate, họp để làm rõ yêu cầu | Restart từ Phase 01 hoặc 03 |

### 2.2 Log feedback vào file

Tạo `approval/feedback-log.md`:

```markdown
# Feedback Log — [Keyword]
> Nhận phản hồi ngày: [DD/MM/YYYY HH:MM]
> Người phản hồi: [Tên nếu có]

## Phân loại tổng thể: [APPROVED / MINOR / MAJOR / REJECT]

## Chi tiết góp ý

| # | Loại | Phần bị góp ý | Nội dung góp ý | Trạng thái xử lý |
|---|---|---|---|---|
| 1 | ✏️ MINOR | H2: [Heading cũ] | Đổi thành: [Heading mới] | ⬜ Chưa xử lý |
| 2 | 🔄 MAJOR | Dịch vụ match | Đổi từ [A] sang [B] | ⬜ Chưa xử lý |

## Ghi chú thêm
[Bất kỳ context hay yêu cầu bổ sung nào từ khách]
```

---

## Phase 3: Xử lý chỉnh sửa

### 3.1 Xử lý MINOR

Với mỗi góp ý MINOR, sửa trực tiếp trong `outline.md`:
1. Cập nhật đúng heading / FAQ / cấu trúc theo góp ý
2. Đánh dấu trong `feedback-log.md`: `✅ Đã xử lý`
3. **Không cần chạy lại outline-quality-scoring** nếu chỉ sửa từ ngữ
4. Thông báo cho khách: "Đã cập nhật theo góp ý, outline sẵn sàng khóa"

### 3.2 Xử lý MAJOR

1. Ghi rõ scope thay đổi trong `feedback-log.md`
2. **Trả outline về Phase 04** với briefing cụ thể:
   ```
   MAJOR REVISION REQUIRED:
   - Đổi từ [Angle A] sang [Angle B]
   - Thêm H2 về [Topic X], xóa H2 về [Topic Y]
   - Đổi Service Match từ [Service A] sang [Service B]
   → Phải chạy lại outline-quality-scoring sau khi rebuild
   ```
3. Sau khi rebuild và re-score ≥ 80 → Gửi lại khách (vòng 2)

### 3.3 Giới hạn vòng lặp (Loop Breaker)

```
IF revision_round > 2:
    → ESCALATE: Cảnh báo "Outline đã qua 2 vòng chỉnh sửa MAJOR"
    → Đề xuất họp làm rõ yêu cầu trước khi tiếp tục
    → Không tự động tiếp tục vòng 3
```

---

## Phase 4: Khóa Outline (Outline Freeze)

Khi khách hàng xác nhận APPROVED (hoặc sau khi sửa MINOR):

### 4.1 Tạo Frozen Outline

Tạo file `approval/outline-FROZEN.md` — bản sao y nguyên của `outline.md` tại thời điểm được duyệt:

```markdown
# FROZEN OUTLINE — [Keyword Chính]
> Trạng thái: 🔒 LOCKED
> Ngày khóa: [DD/MM/YYYY HH:MM]
> Người duyệt: [Tên]
> QA Score lần cuối: [X]/100
> Version: v[N] (Vòng duyệt thứ N)

---
[Toàn bộ nội dung outline.md tại thời điểm được duyệt]
```

### 4.2 Cập nhật metadata trong `topic.toml` (nếu file tồn tại)

```toml
# Thêm hoặc cập nhật metadata approval:
outline_status = "FROZEN"
outline_frozen_date = "YYYY-MM-DD"
approval_round = N
```

### 4.3 Thông báo bàn giao cho writer

```markdown
## ✅ Outline Approved & Frozen — [Keyword]

Writer nhận bàn giao:
- 📄 Outline đã khóa: approval/outline-FROZEN.md
- 📊 QA Report: outline-qa-report.md
- 🔗 Internal Link Plan: (trong outline-FROZEN.md phần cuối)
- 📌 Angle bài: [1 câu mô tả]

⚠️ QUAN TRỌNG cho Writer:
- Bám sát 100% cấu trúc H2/H3 trong outline đã khóa
- Không tự thêm/bớt/đổi heading mà không có phê duyệt
- Nếu phát hiện vấn đề khi viết → báo lại trước, không tự sửa cấu trúc
```

---

## Folder Structure sau khi hoàn thành Gate

```
clients/Home-Credit/brands/Home-Credit/keywords/[keyword-slug]/
├── search-intent.md
├── research.md
├── competitors/
│   └── competitor_[N]_*.md
├── gap-analysis-report.md
├── outline.md                    ← Bản làm việc (có thể bị edit)
├── outline-qa-report.md          ← Kết quả chấm điểm
├── approval/
│   ├── delivery-summary.md       ← Gói bàn giao cho khách
│   ├── feedback-log.md           ← Log toàn bộ phản hồi
│   └── outline-FROZEN.md        ← Bản khóa, bất biến
└── topic.toml                    ← Cập nhật approval metadata; chỉ đổi `status` theo workflow contract
```

---

## Decision Flow tổng thể

```
[Đầu vào: outline.md đạt ≥ 80 điểm]
         ↓
    Phase 1: Tạo delivery-summary.md
         ↓
    [Gửi cho khách hàng]
         ↓
    Phase 2: Nhận feedback → Phân loại
    ├── APPROVED → Phase 4 (Freeze)
    ├── MINOR    → Phase 3.1 → Phase 4 (Freeze)
    ├── MAJOR    → Phase 3.2 → Trả về Phase 04 Outline Dev
    │              → Re-score → Gửi lại (Round 2)
    │              → Nếu Round > 2 → ESCALATE
    └── REJECT   → ESCALATE (Họp làm rõ yêu cầu)
         ↓
    Phase 4: outline-FROZEN.md + Thông báo writer
         ↓
    [Chuyển sang 07. Article Writing]
```

---

## Self-Check (Đọc trước khi chạy)

- [ ] Đã xác nhận outline-qa-report.md tồn tại và score ≥ 80 trước khi vào gate.
- [ ] delivery-summary.md chỉ chứa **cấu trúc heading** — không copy toàn bộ nội dung gợi ý vào.
- [ ] feedback-log.md ghi nhận đầy đủ từng góp ý với trạng thái xử lý.
- [ ] outline-FROZEN.md là bản copy y nguyên `outline.md` tại thời điểm duyệt — không chỉnh sửa sau khi đã freeze.
- [ ] Không tự ý chuyển sang viết bài khi chưa có outline-FROZEN.md.
- [ ] Không tự coi "im lặng" hay "không có phản hồi" là APPROVED — phải có xác nhận tường minh.
