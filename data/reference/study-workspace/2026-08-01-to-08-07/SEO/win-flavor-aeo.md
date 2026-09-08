# WIN Flavor AEO Showcase — Học lại từ research đến article

> Mục tiêu: có thể giải thích AEO, tái tạo pipeline nội dung case study và kiểm tra tính đáng tin của từng claim.

## 1. Kết quả đã tạo

Một long-form case study tiếng Anh nhắm keyword **“AEO case study B2B”**, dùng WIN Flavor làm bằng chứng để giới thiệu năng lực AEO của GOHA. Bộ deliverable gồm:

| Tệp | Vai trò |
|---|---|
| `search-intent.md` | Xác định hybrid intent: informational + commercial investigation |
| `research.md` | Xây entity map, định nghĩa, benchmark, metric và implementation framework |
| `competitor-insights.md` | Tìm mẫu chung và content gap của bài đối thủ |
| `outline.md` | Chuyển insight thành cấu trúc 3.500 từ, 6 H2 + CTA |
| `article.md` | Bài hoàn chỉnh với metadata, key takeaways, bảng dữ liệu và CTA |

## 2. Mô hình tổng thể

```text
Search intent
   ↓ quyết định người đọc và loại nội dung
Semantic research ← competitor analysis
   ↓ quyết định entity, proof và differentiation
Strategic outline
   ↓ quyết định narrative + vị trí dữ liệu + CTA
Article
   ↓ cần kiểm chứng claim, schema và đo citation
Published AEO asset
```

## 3. Kiến thức cốt lõi

### AEO/GEO khác SEO ở mục tiêu đo lường

- SEO truyền thống tối ưu khả năng xếp hạng và nhận click.
- AEO/GEO tối ưu khả năng được answer engine trích xuất, nhắc đến và dẫn nguồn.
- Hai hệ không loại trừ nhau: authority, crawlability và topical depth của SEO vẫn là nền cho AI retrieval.

### Answer-first architecture

Mỗi section mở bằng câu trả lời 40–80 từ, heading gần với câu hỏi thật, bullet là câu hoàn chỉnh và dữ liệu nằm trong bảng. Mục đích là tạo các đoạn độc lập mà hệ thống retrieval có thể lấy đúng ngữ cảnh.

### Prompt testing là phép đo lặp lại

Protocol trong tài liệu yêu cầu giữ nguyên prompt, mở fresh context, ghi engine/mode/date/location, chạy tối thiểu ba lần và tách các tín hiệu: mention, citation, recommendation, cited URL, claim support, competitor sources.

### Case study phải nối tactic với business outcome

Narrative của bài đi theo trục: thay đổi hành vi tìm kiếm → framework AEO → cách triển khai → traffic/citation/conversion → công cụ đo → kế hoạch 90 ngày → dịch vụ GOHA.

## 4. Đi qua cách triển khai

### Bước 1 — Phân tích intent

- Mục đích: biết người tìm muốn học hay mua.
- Thực hiện: phân loại macro intent, 12 micro-intent, audience, SERP feature và content vehicle.
- Kết quả: chọn long-form case study 3.000–4.000 từ.
- Kiểm tra: mỗi H2 phải phục vụ ít nhất một micro-intent có độ liên quan cao.

### Bước 2 — Xây semantic research

- Mục đích: tránh một bài chỉ lặp keyword.
- Thực hiện: lập entity map, định nghĩa AEO/GEO/RAG, metric tiers, tools và keyword clusters.
- Kết quả: research brief có thể cấp dữ liệu cho outline.
- Kiểm tra: lần ngược từng bảng/claim về nguồn; claim thiếu nguồn phải đánh dấu.

### Bước 3 — Tìm content gap

- Mục đích: không sao chép cấu trúc đối thủ.
- Thực hiện: so sánh proof, depth, methodology, tool coverage và CTA.
- Kết quả: khác biệt dự kiến là dữ liệu WIN Flavor, góc nhìn exporter Việt Nam và prompt-testing framework.
- Kiểm tra: mỗi differentiator phải xuất hiện rõ trong outline.

### Bước 4 — Thiết kế outline

- Mục đích: khóa narrative trước khi viết.
- Thực hiện: map challenge → framework → playbook → results → tools → takeaways → service.
- Kết quả: 6 H2 chính, 18 H3, 10 bảng dự kiến và CTA.
- Kiểm tra: loại mọi section không giúp giải thích, chứng minh hoặc chuyển đổi.

### Bước 5 — Viết và kiểm chứng article

- Mục đích: tạo bài vừa học thuật, vừa có giá trị thương mại.
- Thực hiện: answer-first, tables, expert context, data blocks và CTA.
- Kết quả: bài tiếng Anh với slug `win-flavor-aeo-case-study-b2b`.
- Kiểm tra: kiểm tra title/meta, heading hierarchy, claim-source matrix, link, schema và readability.

## 5. Các quyết định đáng chú ý

| Quyết định | Bằng chứng | Đánh đổi |
|---|---|---|
| Chọn case study thay vì guide thuần | “case study” có micro-intent cao nhất trong `search-intent.md` | Đòi hỏi bằng chứng thật chặt hơn |
| Viết tiếng Anh | Nhắm B2B exporter và buyer quốc tế | Cần kiểm tra tone và thuật ngữ bản địa |
| Lead bằng conversion rate 2,85% | `research.md` coi đây là hero metric | Dễ gây mất tin cậy nếu không kèm GA4 evidence |
| Dùng Princeton GEO làm nền | Tạo academic authority | Phải dẫn đúng paper và không phóng đại kết quả |
| CTA về GOHA AEO service | Phù hợp commercial investigation | CTA quá mạnh có thể làm giảm tính trung lập |

## 6. Những claim cần xác minh trước khi publish

- 47% B2B buyers dùng AI cho vendor research và nguồn Forrester 2025.
- 60% Google searches là zero-click.
- AI referral chuyển đổi cao hơn organic 4–8 lần.
- Toàn bộ số WIN Flavor: 358 sessions, 312 users, 2,85%, +18,1%, +181,4%, 65,5%, 26,8%.
- Cách diễn giải các mức tăng từ Princeton GEO paper.
- Sự tồn tại và URL chính xác của landing page GOHA AEO.

## 7. Tiêu chí hoàn thành xuất bản

- Có source URL hoặc evidence nội bộ cho mọi số liệu.
- Tách rõ correlation và causation; không gán toàn bộ tăng trưởng cho AEO nếu dữ liệu chỉ là combined SEO + AEO.
- Có author/reviewer phù hợp E-E-A-T.
- Có Article/Organization schema; chỉ dùng FAQPage khi nội dung FAQ thật sự hiển thị.
- Prompt benchmark có file dữ liệu gốc để tái chạy.
