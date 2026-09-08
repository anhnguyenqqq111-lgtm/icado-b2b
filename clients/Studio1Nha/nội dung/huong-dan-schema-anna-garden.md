# Dữ liệu crawl và hướng dẫn schema Anna Garden

## Dữ liệu đã crawl

| Trường | Giá trị |
|---|---|
| HTTP status | 200 |
| URL crawl | `https://studio1nha.vn/lamour/` |
| Canonical | `https://studio1nha.vn/lamour/` |
| Title | Phim Trường Anna Garden Quận 2 \| Bảng Giá & Concept \| Studio 1 nhà |
| Meta description | Chụp ảnh cưới lãng mạn như phim Hàn tại Phim trường Anna Garden Quận 2. Đặt lịch ngay hôm nay để nhận ưu đãi trọn gói cùng nhiều quà tặng hấp dẫn! |
| OG type | website |
| Ảnh đại diện | `https://studio1nha.vn/application/upload/products/551.JPG` |
| Kích thước ảnh | 1600 × 1067 px |
| Ngày xuất bản | 2023-06-11 |
| Ngày cập nhật | 2023-06-11 |
| Menu cha | `https://studio1nha.vn/phim-truong/` |
| Giá đang hiển thị chính | 6.900.000 VND |
| Điện thoại | 0967 211 002 |
| Zalo | 0837 887 727 |
| Địa chỉ Studio 1 Nhà | 111 Hồ Văn Huê, Phường 9, Phú Nhuận, TP.HCM |

## Loại schema đã dùng

- `WebPage`: mô tả landing page `/lamour/`.
- `Service`: thực thể chính là gói chụp ảnh cưới Anna Garden.
- `Offer`: giá 6.900.000 VND đang hiển thị ở tiêu đề gói và menu website.
- `ImageObject`: ảnh OG thực tế của trang.
- `BreadcrumbList`: Trang chủ → Phim trường → Anna Garden.
- `WebSite` và `LocalBusiness`/`ProfessionalService`: thông tin website và đơn vị cung cấp Studio 1 Nhà.

Không dùng `Article` vì đây là landing page dịch vụ. Không dùng `FAQPage` vì trang hiện không có cụm FAQ hiển thị.

## Cảnh báo dữ liệu cần xử lý

1. Phần đầu trang và menu ghi gói **6,9 triệu đồng**, nhưng cuối thân bài còn ghi **5,4 triệu đồng**. Schema tạm dùng 6,9 triệu đồng; owner cần xóa hoặc cập nhật giá cũ trên trang.
2. Title/meta và thân bài gọi Anna Garden là “Quận 2”, “dọc bờ sông Sài Gòn”; dữ liệu nghiên cứu khác trong project lại ghi Anna Garden tại Đồng Nai. Do chưa có nguồn chính thức thống nhất, schema không khai `Place.address`, `geo` hay bản đồ của phim trường.
3. Trang không có H1 trong HTML đã crawl; heading nội dung bắt đầu từ H2. Nên bổ sung một H1 duy nhất.
4. Trang đang khai `html lang="en-US"` và `og:locale="en_US"` dù nội dung là tiếng Việt. Nên đổi thành `vi-VN` và `vi_VN`.
5. Phần lớn ảnh gallery có `alt=""`. Cần bổ sung alt mô tả bối cảnh/concept thực tế.
6. Các ưu đãi quà tặng không có ngày hết hạn nên không được đưa vào `Offer`.

## Cách chèn

Bọc toàn bộ nội dung `schema-anna-garden.json` trong:

```html
<script type="application/ld+json">
...JSON-LD...
</script>
```

Sau khi chèn, kiểm tra lại bằng Schema Markup Validator. Google Rich Results Test có thể không hiển thị rich result riêng cho `Service`, nhưng schema vẫn giúp làm rõ thực thể, nhà cung cấp, giá và quan hệ trang.
