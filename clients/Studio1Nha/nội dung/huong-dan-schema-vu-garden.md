# Dữ liệu crawl và hướng dẫn schema Vũ Garden

## Dữ liệu đã crawl

| Trường | Giá trị |
|---|---|
| Thời điểm crawl | 2026-08-16 (Asia/Ho_Chi_Minh) |
| HTTP status | 200 |
| URL crawl | `https://studio1nha.vn/vu-garden/` |
| Canonical | `https://studio1nha.vn/vu-garden/` |
| Title | Chụp Ảnh Cưới Phim Trường Vũ Garden Lãng Mạn \| Studio 1 Nhà |
| Meta description | Dịch vụ chụp ảnh cưới trọn gói tại phim trường Vũ Garden từ Studio 1 Nhà. Ekip chuyên nghiệp hỗ trợ trọn gói concept, trang phục, makeup và tạo dáng tự nhiên. |
| OG type | website |
| Ảnh đại diện | `https://studio1nha.vn/application/upload/products/245.jpg` |
| Kích thước ảnh | 1600 × 1067 px |
| URL ảnh sản phẩm tìm thấy | 83 URL |
| Ngày xuất bản trong meta | 2022-10-05 |
| Ngày cập nhật trong meta | 2023-04-06 |
| H1 | Phim trường Vũ Garden – Khu vườn châu Âu lãng mạn cho album cưới |
| Menu cha | `https://studio1nha.vn/phim-truong/` |
| Gói Ruby đang hiển thị | 8.900.000 VND |
| Gói Luxury đang hiển thị | 12.900.000 VND |
| Điện thoại | 0967 211 002 |
| Zalo | 0837 887 727 |
| Địa chỉ Studio 1 Nhà | 111–113 Hồ Văn Huê, Phường 9, Phú Nhuận, TP.HCM |
| Địa chỉ Vũ Garden | 117 đường Nguyễn Du, phường An Phú, TP. Thuận An, Bình Dương |

## Loại schema đã dùng

- `WebPage`: mô tả landing page `/vu-garden/` và liên kết các thực thể trên trang.
- `Service`: thực thể chính là dịch vụ chụp ảnh cưới Vũ Garden của Studio 1 Nhà.
- Hai `Offer`: phản ánh đúng hai gói Ruby 8.900.000 VND và Luxury 12.900.000 VND đang hiển thị.
- `Place`: mô tả phim trường Vũ Garden và địa chỉ tại Thuận An, Bình Dương.
- `ImageObject`: dùng đúng ảnh OG thực tế, kích thước 1600 × 1067 px.
- `BreadcrumbList`: Trang chủ → Phim trường → Vũ Garden.
- `WebSite` và `LocalBusiness`/`ProfessionalService`: website và đơn vị cung cấp Studio 1 Nhà.

Không dùng `Article` hoặc `FAQPage` để giữ đúng format schema của bốn trang phim trường mẫu. `Service` là main entity của `WebPage`. Các thuộc tính trong schema chỉ lấy từ metadata, nội dung, bảng giá, thông tin liên hệ và URL ảnh xuất hiện trong HTML đã crawl.

## Lỗi schema hiện tại cần thay thế

Trang Vũ Garden đang chứa một block JSON-LD của **Long Island**. Block này có các lỗi:

1. Toàn bộ `@id`, URL, tên dịch vụ, `Place` và breadcrumb đều trỏ đến `/long-island/`.
2. Có các placeholder chưa thay như `URL_LOGO_THỰC_TẾ`, `URL_FACEBOOK_THỰC_TẾ`, `URL_ẢNH_LONG_ISLAND_1`.
3. Schema cũ khai giá 8.900.000 VND nhưng không phản ánh gói Luxury 12.900.000 VND đang hiển thị.
4. Schema cũ không mô tả địa chỉ Vũ Garden hoặc ảnh đại diện thật của trang.

Phải **xóa/thay thế hoàn toàn** block schema Long Island hiện tại. Không chèn schema mới bên cạnh block sai vì bot tìm kiếm vẫn có thể đọc cả hai graph và nhận dữ liệu mâu thuẫn.

## Cảnh báo dữ liệu cần xử lý

1. Meta `article:modified_time` và `og:updated_time` vẫn là `2023-04-06` dù thân bài đã được cập nhật. Schema giữ nguyên `dateModified: 2023-04-06` vì yêu cầu chỉ sử dụng dữ liệu đang có trên web. Khi metadata được sửa, cần cập nhật lại schema theo cùng ngày.
2. Trang đang khai `html lang="en-US"` và `og:locale="en_US"` dù nội dung là tiếng Việt. Nên đổi thành `vi-VN` và `vi_VN`.
3. Bảng giá vé phim trường không xuất hiện trong HTML sau lần crawl này, dù có trong bản nội dung nguồn. Nếu chủ đích đăng phần giá vé, cần kiểm tra lại trình soạn thảo hoặc cache trang.
4. Heading “Khu rừng cổ tích” không xuất hiện trong danh sách heading HTML dù đoạn nội dung mô tả vẫn còn. Nên kiểm tra lại thẻ H3 của mục này.

## Cách chèn

1. Mở phần quản trị schema/head code của trang `/vu-garden/`.
2. Tìm block `<script type="application/ld+json">` đang chứa dữ liệu Long Island.
3. Xóa toàn bộ block đó.
4. Bọc nội dung file `schema-vu-garden.json` trong:

```html
<script type="application/ld+json">
...JSON-LD trong schema-vu-garden.json...
</script>
```

5. Xóa cache website/CDN rồi crawl lại source HTML để chắc chắn chỉ còn schema Vũ Garden.
6. Kiểm tra bằng Schema Markup Validator. Google Rich Results Test có thể không hiển thị rich result riêng cho `Service`, nhưng dữ liệu vẫn giúp máy tìm kiếm hiểu quan hệ giữa trang, dịch vụ, địa điểm và báo giá.

## Checklist sau khi triển khai

- Không còn chuỗi `long-island` hoặc `URL_*_THỰC_TẾ` trong source `/vu-garden/`.
- Tất cả URL và `@id` Vũ Garden dùng HTTPS, cùng canonical có dấu `/` cuối.
- Giá Ruby và Luxury trong schema khớp bảng giá nhìn thấy trên trang.
- `dateModified` trong schema khớp `article:modified_time` đang có trên web.
- JSON-LD parse hợp lệ và không có lỗi bắt buộc trong Schema Markup Validator.
