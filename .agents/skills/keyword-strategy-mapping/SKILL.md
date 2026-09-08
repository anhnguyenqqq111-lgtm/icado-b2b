---
name: keyword-strategy-mapping
description: >
  Sử dụng trình duyệt (browser tool) để cào dữ liệu SERP thực tế. 
  Gom nhóm từ khóa và xuất ra định dạng Keyword Strategy Table.
  Triggers: keyword strategy, lập bảng từ khóa outline
---

# Keyword Strategy Mapping (Tabular Format)

## Purpose
Skill này thay thế các skill research cũ trong luồng `outline-hc`. Nhiệm vụ cốt lõi là BẮT BUỘC dùng trình duyệt giả lập để cào dữ liệu Google SERP đang live (tránh dữ liệu ảo), sau đó đúc kết thành Bảng Chiến lược Từ khóa (`Keyword Strategy Table`).

---

## 🛑 QUY TẮC BẮT BUỘC (LIVE RESEARCH)
1. Tuyệt đối **KHÔNG** tự bịa (hallucinate) từ khóa dựa trên kiến thức cũ.
2. **BẮT BUỘC sử dụng `browser tool`** để thực hiện tìm kiếm từ khóa chính trên Google. 
3. Mọi dữ liệu (Google Suggest, PAA, LSI) phải là dữ liệu thực tế đang hiển thị (Live on SERP) tại thời điểm cào.

---

## Phase 1: Live SERP Extraction
Sử dụng `browser tool` thực hiện task sau:
1. Mở trang Google Search.
2. Gõ từ khóa chính (Main Keyword).
3. Đợi trang load và thu thập:
   - Các gợi ý tự động xổ xuống khi gõ (Google Suggest).
   - Danh sách "Mọi người cũng hỏi" (People Also Ask - PAA). Cuộn và click mở vài câu để lấy đủ lượng PAA.
   - Các từ khóa liên quan ở cuối trang (Related Searches / LSI).

## Phase 2: Format & Output
Sau khi lấy được dữ liệu LIVE, hãy sắp xếp và xuất ra Markdown Table chính xác như sau:

```markdown
### 1. Bảng Phân Tích Từ Khóa (Keyword Strategy Table)

| Loại từ khóa | Chi tiết |
| :--- | :--- |
| **Main keyword** | [Từ khóa chính] |
| **Keyword phụ** | - [Từ 1]<br>- [Từ 2]<br>- [Từ 3] |
| **Google Suggest** | - [Gợi ý 1]<br>- [Gợi ý 2] |
| **LSI Keyword** | - [LSI 1]<br>- [LSI 2] |
| **PAA** | - [PAA 1]<br>- [PAA 2]<br>- [PAA 3] |
```

`Main keyword`, `Keyword phụ`, `Google Suggest`, `LSI Keyword` và `PAA` là 5 trường bắt buộc. Nếu chưa xác minh được giá trị, để trống hoặc ghi `Chưa xác minh`; không tự suy đoán.

**Lưu ý định dạng**:
- Sử dụng thẻ `<br>` hoặc danh sách gạch đầu dòng `- ` để ngắt dòng bên trong ô bảng giúp dễ đọc.
