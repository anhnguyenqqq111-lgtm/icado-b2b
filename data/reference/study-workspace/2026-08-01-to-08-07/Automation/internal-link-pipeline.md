# Internal-link Automation Pipeline

## Kết quả trong tuần

Pipeline Heritage tạo các report Markdown/JSON/CSV và workbook như `heritage-internal-links-547.xlsx`, kết hợp những script thu thập nội dung, tính độ liên quan, chọn anchor và xuất dữ liệu.

## Luồng xử lý

```text
Sitemap/workbook URLs
  → fetch + cache pages
  → clean and normalize text
  → score topical similarity
  → locate an exact anchor in source content
  → enforce destination/diversity rules
  → export review plan
  → validate row count, URLs and duplicates
```

## Nguyên tắc chất lượng

- Anchor phải tồn tại nguyên văn trong bài nguồn.
- Destination phải thực sự bổ sung ý nghĩa cho ngữ cảnh quanh anchor.
- Không link một trang về chính nó.
- Tránh lặp destination và anchor quá mức.
- Tách suggestion tự động khỏi approval biên tập.
- Cache giúp tái chạy nhanh nhưng phải có cơ chế refresh.

## Các tầng có thể gây lỗi

| Triệu chứng | Tầng cần kiểm tra |
|---|---|
| Anchor không tồn tại | HTML cleaning, normalization hoặc surface matching |
| Trang đích không liên quan | Feature extraction và similarity score |
| Link lặp dày | Diversity constraints |
| Workbook hỏng | XML escaping, sheet relations và archive integrity |
| Nội dung cũ | Cache invalidation |

## Bài tập

Lấy ngẫu nhiên 20 dòng trong workbook. Kiểm tra anchor tồn tại, context relevance, URL status và destination diversity; ghi precision trước khi triển khai hàng loạt.
