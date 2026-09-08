# Practice Lab

## Phần A — Active recall

1. Vì sao AEO không thay thế SEO?
2. Nêu sáu tín hiệu cần ghi trong một lần prompt testing.
3. Pipeline của WIN Flavor đi qua năm artifact nào?
4. Vì sao sitemap Everest nên theo nhu cầu mua thay vì cấu trúc nội bộ?
5. Static prototype và Next.js implementation khác nhau ở đâu?
6. Vì sao `mtime` không phải lịch sử công việc đáng tin như Git commit?

## Phần B — Bài tập thay đổi

### Bài 1: Claim audit

Chọn 10 claim định lượng trong `article.md`. Tạo bảng gồm claim, nguồn đang ghi, bằng chứng gốc, trạng thái và wording an toàn hơn. Không cho publish khi evidence chưa đủ.

### Bài 2: Thiết kế lại một section

Chọn hero Everest. Viết:

- một H1 nói rõ đối tượng + giá trị;
- một supporting paragraph;
- một CTA chính và một CTA phụ;
- năm field cho quick quote;
- mobile layout ở 320px.

### Bài 3: Canonical cleanup plan

So sánh `projects/everest-logistics/site/`, `projects/everest-logistics/next-app/` và các bản trong `archive/everest-logistics-backups/`. Không xóa gì. Lập bảng hash/diff, đề xuất nguồn canonical, release folder và archive plan.

## Phần C — Bài tập chẩn đoán

1. ChatGPT mention rate tăng nhưng AI referral traffic không tăng. Hãy nêu ít nhất bốn giả thuyết và cách kiểm tra.
2. Form báo giá có nhiều lượt bắt đầu nhưng ít submit. Hãy phân biệt lỗi UX, lỗi validation, traffic intent và technical failure.
3. App mobile hiển thị code cũ dù source đã sửa. Hãy kiểm tra pipeline source → `www/` → Capacitor sync → native build → service-worker cache.
4. Workbook internal link có anchor không tồn tại trong bài nguồn. Hãy tìm tầng pipeline có thể gây lỗi.

<details>
<summary>Đáp án gợi ý</summary>

1. SEO tạo crawlability, authority và topical relevance; AEO dùng nền đó để tăng khả năng retrieval/citation.
2. Mention, citation, recommendation, cited URL, claim support và competitor sources; đồng thời lưu engine/mode/date/context.
3. `search-intent.md` → `research.md` + `competitor-insights.md` → `outline.md` → `article.md`.
4. Khách hàng tìm theo việc cần giải quyết; mental model nội bộ làm menu khó quét và giảm conversion.
5. Static nhanh và trực tiếp; Next.js tách component/data, phù hợp reuse và scale hơn.
6. `mtime` có thể đổi khi copy/extract/build và không cho biết tác giả, diff hay ý định.

Chẩn đoán mẫu: AI có thể mention nhưng không link; prompt set không đại diện volume; analytics mất referrer; citation nằm ở query ít nhu cầu; time lag; vị trí/engine khác nhau. Mỗi giả thuyết cần một phép đo riêng.

</details>
