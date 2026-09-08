# 03. AI search, AIO, AEO và GEO

## 1. Cách gọi trong hệ thống

- **AI search**: lớp tìm kiếm có khả năng tổng hợp/cá nhân hóa câu trả lời.
- **AIO**: AI Overviews hoặc cách gọi nội bộ cho tối ưu hiện diện trong AI-generated answers.
- **AEO**: Answer Engine Optimization, tối ưu để câu trả lời có thể được lấy/trích xuất.
- **GEO**: Generative Engine Optimization, tối ưu khả năng hiện diện, được nhắc và được trích dẫn trong output của generative engine.

Đây là các nhãn vận hành, không nên xem như một ranking factor riêng. Google nói best practice SEO vẫn là nền tảng cho AI features, và khuyến nghị nội dung độc đáo, hữu ích, people-first; không có “hack” đảm bảo xuất hiện.

## 2. Mô hình visibility

```text
Access/crawl/index
  → retrieval eligibility
  → source selection
  → citation/mention
  → answer absorption
  → click/brand search
  → lead/revenue
```

Mỗi tầng có thể rơi rụng. Được nhắc không đồng nghĩa được trích dẫn; được trích dẫn không đồng nghĩa có click; có click không đồng nghĩa có doanh thu.

## 3. Answer-first architecture

Mỗi section nên có:

1. Heading gần cách người dùng hỏi.
2. Câu trả lời ngắn, rõ điều kiện áp dụng.
3. Giải thích và bằng chứng.
4. Bảng/bullet có cấu trúc khi cần so sánh.
5. Link tới nguồn gốc hoặc trang chuyên sâu.
6. CTA tương ứng với intent, không ép bán ở TOFU.

Đây là khả năng đọc và tái sử dụng thông tin, không phải công thức đảm bảo citation.

## 4. Evidence graph

Với mỗi claim quan trọng, lưu:

| Field | Ý nghĩa |
|---|---|
| Claim | phát biểu cần bảo vệ |
| Source | URL/file/dataset gốc |
| Scope | thị trường, thời gian, đối tượng |
| Evidence type | first-party, official, academic, observed |
| Owner | người chịu trách nhiệm xác minh |
| Last verified | ngày kiểm tra |
| Confidence | high/medium/low |
| Safe wording | cách diễn đạt không vượt quá bằng chứng |

## 5. Prompt benchmark

Giữ nguyên prompt set, engine/model/mode, location, language, date và fresh context. Chạy lặp tối thiểu 3 lần; ghi:

`mention`, `recommendation`, `citation`, `cited URL`, `claim support`, `competitor source`, `answer accuracy`, `click/referral nếu có`.

Không lấy một lần prompt làm market share. So sánh theo cùng query set và báo cáo confidence/limitations.

## 6. Đo lường và diễn giải

| Metric | Có thể nói | Không được suy ra |
|---|---|---|
| Mention rate | thương hiệu xuất hiện trong mẫu prompt | toàn bộ thị trường biết thương hiệu |
| Citation rate | URL được dẫn trong mẫu prompt | URL tạo traffic/doanh thu |
| AI referral | lượt truy cập có nguồn AI được nhận diện | toàn bộ ảnh hưởng của AI |
| Assisted conversion | điểm chạm AI trước key event | AI là nguyên nhân duy nhất |
| Claim support | câu trả lời dùng đúng bằng chứng | nội dung đã luôn chính xác |

## 7. Guardrails

- Không bịa review, case, số liệu, credential hoặc claim “được AI ưu tiên”.
- Không tạo hàng loạt trang mỏng bằng AI. Google cảnh báo scaled content không thêm giá trị có thể vi phạm spam policy.
- Không dùng `llms.txt`, schema hoặc FAQ như lời hứa ranking/citation; chỉ triển khai khi có use case và nội dung hiển thị phù hợp.
- Cập nhật prompt benchmark theo quý và khi engine thay đổi đáng kể.
