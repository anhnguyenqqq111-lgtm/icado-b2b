---
name: faq-research
description: >
  Nghiên cứu chuyên sâu để trích xuất 5-10 câu hỏi thường gặp (FAQ) chất lượng cao nhất cho một từ khóa,
  dựa trên Google People Also Ask (PAA), Search Suggestions và các nguồn forum/Reddit.
  Triggers: faq research, tìm faq, tìm câu hỏi thường gặp, /faq-research
---

# FAQ Research

## Purpose
Tách biệt nhiệm vụ đào sâu câu hỏi của người dùng (User Queries/FAQ) thành một module riêng. Thay vì chỉ gom từ khóa, skill này có nhiệm vụ truy vấn các kho tàng câu hỏi thực tế (đặc biệt là hộp People Also Ask của Google) để chọn ra những câu hỏi sát nhất với Intent, đóng góp trực tiếp vào mục FAQ của `outline.md`.

---

## Mandatory Inputs
- Keyword chính hoặc Chủ đề bài viết
- (Tùy chọn) `search-intent.md` để filter câu hỏi không liên quan

---

## Phase 1: Khai thác Nguồn Dữ liệu Thực tế

### 1.1 People Also Ask (PAA)
Sử dụng `web search` hoặc `browser tool` để tìm keyword chính trên Google.
- Tập trung vào hộp "Mọi người cũng hỏi" (People Also Ask).
- **Lưu ý kỹ thuật**: Có thể giả lập thao tác click vào các câu hỏi PAA để Google mở rộng thêm các câu hỏi ẩn sâu bên dưới. Ghi nhận toàn bộ.

### 1.2 Google Autocomplete (Dạng câu hỏi)
Thực hiện các lệnh tìm kiếm có tiền tố nghi vấn:
- `Tại sao [keyword]`
- `[keyword] là gì`
- `[keyword] giá bao nhiêu`
- `Có nên [keyword]`
- `[keyword] như thế nào`

### 1.3 Khai thác Forum/Social (Dành cho ngành ngách)
- Nếu là B2B hoặc kỹ thuật sâu: Thêm `site:reddit.com` hoặc `site:quora.com` sau keyword để xem người dùng thật đang hỏi gì.

---

## Phase 2: Lọc và Lựa chọn FAQ

Bạn sẽ thu thập được một danh sách thô (15-20 câu). Thực hiện bộ lọc sau để chọn ra **chính xác 5 câu tốt nhất** (theo chuẩn `hc-outline-rules`):

### Tiêu chí Loại bỏ (LOẠI NGAY):
- ❌ Câu hỏi đã được trả lời kỹ ở phần H2 chính của bài (tránh lặp nội dung).
- ❌ Câu hỏi mang tính địa phương hẹp (VD: "Mở thẻ ở chi nhánh Quận 1?").
- ❌ Câu hỏi đối thủ trực tiếp (VD: "FE Credit lãi suất bao nhiêu?").
- ❌ Câu hỏi quá rộng, không thể trả lời ngắn gọn trong 1-2 paragraph.

### Tiêu chí Ưu tiên (CHỌN LỌC):
- ✅ Đánh trúng nỗi lo sợ / thắc mắc phổ biến nhất (Pain points).
- ✅ Dạng câu hỏi Yes/No (VD: "Bị nợ xấu có vay được không?").
- ✅ Dạng câu hỏi liên quan đến chi phí / thời gian (VD: "Bao lâu thì nhận được tiền?").

---

## Phase 3: Soạn thảo Đáp án (Optional / Draft)

Nếu được yêu cầu, soạn thảo gợi ý đáp án ngắn gọn (chỉ 2-3 câu) cho mỗi FAQ đã chọn để định hướng cho writer:
- Đi thẳng vào vấn đề (Direct Answer).
- Không rườm rà "X xin trả lời câu hỏi của bạn".

---

## Output Format

Xuất ra file `faq-research-report.md` hoặc inject thẳng vào phần FAQ của `research.md` / `outline.md`:

```markdown
## 5 Câu hỏi FAQ Đề xuất (People Also Ask / Search Demand)

1. **[Câu hỏi 1]**
   > *Nguồn: Google PAA / Intent: [Trust/Cost/Process]*
   > Gợi ý trả lời: [Viết 1-2 câu đáp án cốt lõi]
   
2. **[Câu hỏi 2]**
   > *Nguồn: Autocomplete*
   > Gợi ý trả lời: [...]

... [Đủ 5 câu]
```

---

## Self-Check (Đọc trước khi hoàn thành)
- [ ] Có đúng 5 câu hỏi không? (Chuẩn outline Home Credit yêu cầu đúng 5 FAQ).
- [ ] Câu hỏi có phải là câu người dùng thật sự gõ không? (Đừng tự bịa ra câu hỏi với ngôn từ văn vẻ).
- [ ] Đã loại bỏ các câu hỏi quá chung chung (kiểu "X là gì" nếu H2 trên đã giải thích)?
