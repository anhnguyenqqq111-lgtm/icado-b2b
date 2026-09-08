# 📊 Rank Dashboard — Keyword Ranking Tracker

Công cụ check ranking keyword trên Google Search, tích hợp Google Sheets.

## Tính năng

- ✅ Check ranking keyword tự động với Puppeteer
- ✅ Tích hợp Google Sheets (đọc project, keywords + ghi kết quả)
- ✅ CAPTCHA detection + auto-solver (audio)
- ✅ WARP VPN integration (auto reset sau 5 CAPTCHA liên tiếp)
- ✅ Resume từ chỗ dừng (bỏ qua keywords đã check trong 72h)
- ✅ SERP Feature Detection (Featured Snippet, PAA, Video, Knowledge Panel...)
- ✅ Rank Drop Alerts (cảnh báo keyword tụt ≥5 vị trí)
- ✅ CSV Export
- ✅ Schedule auto-check (6h/12h/24h/3 ngày/1 tuần)
- ✅ AI Insights (Gemini API)
- ✅ Wipe History

## Cài đặt

```bash
npm install
```

## Cấu hình

1. **Google Sheets OAuth**: Đặt `credentials.json` vào thư mục gốc
2. **Settings**: Sửa `settings.json`:
   ```json
   {
     "GOOGLE_SHEET_ID": "your-sheet-id",
     "UULE_CODE": "Ho Chi Minh City"
   }
   ```
3. **Gemini AI** (tùy chọn): Thêm API keys vào `.env`:
   ```
   GEMINI_API_KEY_1=your-key
   ```

## Chạy

```bash
npm start
```

Truy cập: **http://localhost:3000**

Hoặc click `start-dashboard.bat`

## Cấu trúc Google Sheet

Sheet cần có 2 tab:
- **Project**: Cột `DỰ ÁN` + `Domain`
- **Keyword_KPI**: Cột `DỰ ÁN` + `Keywords`

Kết quả ranking sẽ được ghi vào tab riêng theo tên project.
