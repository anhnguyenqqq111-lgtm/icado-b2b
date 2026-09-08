# Audit triển khai landing page vận chuyển đường biển

## Phạm vi

- URL: `https://everlog.com.vn/dich-vu/van-chuyen-duong-bien`
- Ưu tiên: P1
- Dữ liệu đầu vào: 116 impressions, 3 clicks, CTR 2,59%, vị trí 7,2; 145 sessions, engagement rate 38,62%, bounce rate 61,38%.
- Mục tiêu: đưa người có nhu cầu FCL/LCL tới form báo giá và thông tin lịch tàu.

## Đã triển khai

- Đổi title/H1 sang “Vận chuyển đường biển quốc tế FCL/LCL” và thêm breadcrumb.
- Thêm Service schema với URL canonical của trang.
- Đưa 3 lựa chọn FCL, LCL, door-to-door/sea-air và form báo giá lên trước phần giải thích.
- Form có họ tên, doanh nghiệp, điện thoại, email, POL/nơi lấy, POD/nơi giao và thông tin commodity, HS, gross weight, CBM, số kiện, loại cont, Incoterms, thời gian.
- Thêm bảng FCL/LCL, tuyến/cảng/transit time theo khoảng hoặc cập nhật theo booking.
- Thêm quy trình 5 bước, checklist ngay trước CTA và 5 FAQ về local charges, demurrage/detention, bảo hiểm, hàng nguy hiểm, lịch tàu.
- Loại bỏ claim không có bằng chứng và không đưa thêm tuyến ngoài phạm vi đã được cung cấp.
- Form phát event GA4 `generate_lead` khi `window.gtag` tồn tại.
- Sau khi đối chiếu bản gốc, giới hạn lại thông số: FCL 20’/40’, LCL dưới 10 tấn và dưới 15 CBM; không mở rộng danh mục container, loại hàng hoặc năng lực ngoài nội dung nguồn.

## Cần xác nhận trước khi publish

- Cập nhật danh sách tuyến, cảng và khoảng transit time từ đội vận hành tại thời điểm booking.
- Nối form demo với CRM/API và kiểm tra event trong GA4 DebugView.
- Xác nhận template production có render schema và breadcrumb; kiểm tra canonical/redirect nếu website production khác app demo.
- Xác nhận người kiểm duyệt chuyên môn và ngày cập nhật trên CMS.

## Kiểm tra

- `git diff --check`: cần chạy sau khi hoàn tất thay đổi.
- `npm run build`: chưa chạy được vì package chưa có `node_modules` (`next: command not found`).
