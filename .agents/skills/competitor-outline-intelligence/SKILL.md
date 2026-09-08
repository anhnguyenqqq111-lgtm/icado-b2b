---
name: competitor-outline-intelligence
description: >
  Sử dụng trình duyệt (browser tool) truy cập trực tiếp bài viết đối thủ. 
  Phân tích cấu trúc và xuất ra định dạng Competitor Analysis Table.
  Triggers: competitor outline, phân tích cấu trúc đối thủ dạng bảng
---

# Competitor Outline Intelligence (Tabular Format)

## Purpose
Skill này thay thế việc cào nội dung đơn thuần. Nhiệm vụ là BẮT BUỘC dùng trình duyệt giả lập để truy cập các URL đối thủ đang live, đọc nội dung thực tế (ngay cả phần bị che hoặc lazy-load), sau đó tổng hợp thành Bảng Phân Tích Đối thủ (`Competitor Analysis Table`) phục vụ lên Outline.

---

## 🛑 QUY TẮC BẮT BUỘC (LIVE RESEARCH)
1. Tuyệt đối **KHÔNG** đánh giá đối thủ dựa trên URL hoặc trí nhớ ảo.
2. **BẮT BUỘC sử dụng `browser tool`** để truy cập trực tiếp từng URL trong Top 5 SERP.
3. Phải đọc cấu trúc thẻ Heading (H2, H3), Bảng biểu (Table), FAQ thực tế đang hiển thị trên bài viết của đối thủ.

---

## Phase 1: Live Competitor Extraction
Với mỗi URL đối thủ:
1. Dùng `browser tool` truy cập URL.
2. Scroll để load toàn bộ trang.
3. Ghi nhận cấu trúc Heading (H2/H3), cách họ trình bày bảng biểu, ví dụ minh họa và có mục FAQ không.
4. Đánh giá Điểm mạnh (Strengths) và Điểm yếu/Thiếu sót (Weaknesses) của cấu trúc đó.

## Phase 2: Format & Output
Sau khi phân tích Top 5 đối thủ, xuất kết quả ra Markdown Table chính xác như sau:

```markdown
### 2. Bảng Phân Tích Đối Thủ (Competitor Analysis Table)

| # | URL | Strengths | Weaknesses | What We Learn | Opportunity | Example |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | domain.com | [Điểm mạnh 1] | [Điểm yếu 1] | [Bài học] | [Cơ hội cho bài HC] | "[Trích dẫn thực tế]" |
| 2 | domain2.com | ... | ... | ... | ... | ... |
| 3 | domain3.com | ... | ... | ... | ... | ... |
```

**Lưu ý**: Cột `Example` bắt buộc phải chứa một trích dẫn ngắn (quote) LẤY TRỰC TIẾP TỪ BÀI ĐỐI THỦ để minh chứng cho việc đã cào dữ liệu thực tế.

Schema cứng của bảng gồm đủ 7 cột: `#`, `URL`, `Strengths`, `Weaknesses`, `What We Learn`, `Opportunity`, `Example`. Nếu một cột chưa có giá trị, để trống hoặc ghi `Chưa xác minh`; không được bỏ cột hoặc bịa dữ liệu.
