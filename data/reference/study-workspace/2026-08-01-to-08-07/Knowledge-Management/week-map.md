# Bản đồ công việc tuần 01–07/08/2026

## Kết quả quan sát được

Tuần này tạo ra bốn dòng năng lực lớn:

1. **SEO/AEO content system:** nghiên cứu intent, entity, đối thủ, outline và bài case study WIN Flavor; nhiều cụm bài Home Credit và May Mặc CTH.
2. **Thiết kế và triển khai web:** kế hoạch UX/SEO, information architecture, design system, website tĩnh và bản Next.js cho Everest Logistics.
3. **Ứng dụng đa nền tảng:** Calendar và Personal Finance sử dụng web stack, PWA và Capacitor để đóng gói Android/iOS.
4. **SEO operations/tooling:** nghiên cứu internal link Heritage, xuất CSV/XLSX, phân nhóm keyword và tạo skill ghi lại kiến thức AI.

## Timeline dựa trên bằng chứng tệp

| Mốc quan sát | Nhóm công việc | Artifact tiêu biểu | Điều học được |
|---|---|---|---|
| 01–06/08 | SEO/content production | `clients/Home-Credit/`, `clients/MayMacCTH/` | Quy trình sản xuất nội dung theo cụm và persona |
| 06/08 | Everest web | `clients/Everest-Logistics/`, `projects/everest-logistics/` | Chuyển SEO research thành IA, component và trang chuyển đổi |
| 06–07/08 | Mobile apps | `projects/calendar-app/`, `projects/personal-finance/` | Dùng một web codebase cho PWA + Capacitor + desktop bundle |
| 07/08 | Internal links | `heritage-internal-links-547.xlsx`, `convert_inlinks_to_excel.py`, `scripts/build_heritage_internal_links.py` | Tự động hóa crawl, scoring, anchor selection và workbook |
| 07/08 17:30–17:54 | WIN Flavor AEO | 5 tệp trong `clients/General-B2B/keywords/GOHA/win-flavor-aeo-showcase/` | Pipeline search intent → research → competitor gap → outline → article |
| 07/08 20:36 | Knowledge capture | `.agent/skills/learn-ai-output/` | Biến output của AI thành tài liệu học chủ động |

## Luồng công việc tổng thể

```text
Research dữ liệu
  → phân loại intent/entity
  → thiết kế kiến trúc nội dung hoặc sản phẩm
  → tạo artifact (article/web/app/tool)
  → kiểm tra và đóng gói
  → document để học lại
```

## Điểm mạnh lặp lại

- Bắt đầu bằng cấu trúc và tiêu chí thay vì viết ngay.
- Dùng dữ liệu bảng cho nội dung B2B và quyết định SEO.
- Chuyển một thiết kế thành nhiều bề mặt: static site, Next.js, PWA, mobile.
- Tự động hóa các thao tác lặp lại bằng Python/JavaScript.

## Rủi ro cần sửa trong tuần sau

- Nhiều bản sao Everest (`site 2` đến `site 6`) làm mờ đâu là nguồn chuẩn.
- Phần lớn công việc chưa được Git theo dõi nên khó xem diff hoặc phục hồi lịch sử.
- Một số con số AEO/industry benchmark chưa kèm nguồn gốc có thể kiểm chứng ngay trong workspace.
- Artifact build và source đang nằm cùng cấp, làm nhiễu khi rà công việc theo thời gian.

## Cách tái tạo tuần này có kiểm soát

1. Tạo branch hoặc repository rõ ràng cho mỗi project.
2. Chốt source-of-truth trước khi tạo bản sao hoặc file zip.
3. Commit theo milestone: research, architecture, implementation, QA, docs.
4. Lưu nguồn dữ liệu và bằng chứng cạnh claim quan trọng.
5. Cuối ngày cập nhật study workspace bằng diff thay vì dựa vào `mtime`.
