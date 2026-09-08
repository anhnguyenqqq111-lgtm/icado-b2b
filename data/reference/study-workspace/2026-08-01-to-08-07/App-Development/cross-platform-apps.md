# Cross-platform Apps

## Calendar app

`projects/calendar-app/app/` thể hiện một web app được đóng gói cho nhiều target:

```text
index.html + style.css + app.js
  ├─ PWA: manifest.json + sw.js
  ├─ Android/iOS: Capacitor + native projects
  └─ Desktop: Goha-Calendar-darwin-arm64
```

## Personal finance app

`projects/personal-finance/app/` sử dụng cùng pattern web/PWA/Capacitor, bổ sung cấu hình Vercel và desktop bundle FinTrack.

## Kiến thức cốt lõi

- Giữ web source là nguồn chuẩn và sinh `www/` bằng script.
- Chạy Capacitor sync sau khi cập nhật web bundle.
- Quản lý icon, manifest, native permissions và signing theo từng target.
- Phân biệt service-worker cache, web bundle cache và native build cache khi debug.
- Không chỉnh trực tiếp cả source lẫn bản copy trong `www/` vì sẽ tạo drift.

## Bài tập chẩn đoán

App mobile vẫn hiển thị code cũ sau khi sửa source. Kiểm tra theo thứ tự:

1. Source đã được lưu đúng chưa?
2. Script prepare có copy sang `www/` không?
3. Capacitor sync đã cập nhật native project chưa?
4. Native build có dùng cache cũ không?
5. Service worker hoặc app data có giữ asset cũ không?
