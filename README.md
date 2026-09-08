# Everest & D2C/SME SEO Workspace

Workspace chuyên biệt quản lý SEO, content marketing, personas, và applications cho nhóm khách hàng Logistics & SME / D2C:

- **Everest Logistics**: Vận tải biển, hàng không, thủ tục hải quan, Next.js logistics web app.
- **ICADO**: Thời trang thể thao nam/nữ, gym, yoga, đồ chạy bộ.
- **May Mặc CTH**: May đo đồng phục công sở, áo polo, bảo hộ lao động Hải Phòng.
- **Studio 1 Nhà**: Dịch vụ chụp ảnh cưới, trọn gói studio, phim trường TP.HCM.

## Cấu trúc thư mục

```
├── .agent/               # Workflows tự động hóa SEO
├── .agents/skills/       # Bộ skills chuyên sâu theo nhãn hàng & kỹ năng dùng chung
├── clients/              # Dữ liệu khách hàng, từ khóa & bài viết
│   ├── Everest-Logistics/
│   ├── ICADO/
│   ├── MayMacCTH/
│   └── Studio1Nha/
├── data/reference/       # Persona, tiêu chuẩn chất lượng từng nhãn hàng
├── outputs/              # Báo cáo audit, calendar, kế hoạch internal link
├── projects/             # Source code dự án web app (everest-logistics)
├── scripts/              # Automation scripts
└── tools/                # Rank checker, keyword tooling
```

## Kiểm tra Workspace

```bash
python3 scripts/workspace.py validate
python3 -m unittest discover -s tests
```
