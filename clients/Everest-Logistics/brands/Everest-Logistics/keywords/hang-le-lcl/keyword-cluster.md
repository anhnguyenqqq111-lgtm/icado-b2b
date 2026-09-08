# Keyword cluster và internal-link map: vận chuyển hàng lẻ LCL

**Ngày nghiên cứu:** 07/09/2026  
**Nguồn dữ liệu chính:** MCP Google Search Console, live web search và các URL Everlog đã mở trực tiếp.  
**Trang trung tâm:** [Dịch vụ vận chuyển hàng lẻ LCL](https://everlog.com.vn/hang-le-post1987.html)

## 1. Dữ liệu query từ MCP GSC

Phạm vi MCP GSC: 90 ngày, từ 09/06/2026 đến 07/09/2026. URL có 155 impressions, 1 click và CTR trung bình 0,65% trong dữ liệu trả về.

| Query | Clicks | Impressions | CTR | Vị trí | Cluster |
|---|---:|---:|---:|---:|---|
| `vận chuyển hàng lẻ` | 0 | 58 | 0% | 43,6 | Commercial |
| `gom hàng là gì` | 0 | 30 | 0% | 28,9 | Informational |
| `dịch vụ LCL` | 0 | 10 | 0% | 33,6 | Commercial |
| `LCL` | 0 | 9 | 0% | 59,7 | Informational |
| `hàng lẻ` | 0 | 6 | 0% | 55,8 | Commercial |
| `đi via là gì` | 0 | 3 | 0% | 1,0 | Operational |
| `consolidator là gì` | 0 | 2 | 0% | 16,0 | Informational |
| `consol là gì` | 0 | 2 | 0% | 33,5 | Informational |
| `hàng consol là gì` | 0 | 2 | 0% | 32,5 | Informational |
| `lcl consol` | 0 | 2 | 0% | 22,5 | Informational |
| `LCL là gì` | 0 | 2 | 0% | 58,0 | Informational |
| `W/M là gì` | 0 | 2 | 0% | 55,0 | Operational |
| `consolidation là gì` | 0 | 1 | 0% | 41,0 | Informational |
| `hàng lẻ là gì` | 0 | 1 | 0% | 17,0 | Informational |

**Nhận định:** `đi via là gì` đã có vị trí 1 nhưng chỉ có 3 impressions. Không tách bài riêng ở thời điểm này; giữ nội dung direct/via trong trang trung tâm và dùng bài LCL làm điểm trả lời chính.

## 2. Cấu trúc cluster đề xuất

| Tầng | Cluster | Keyword chính | Intent | Trang đích | Vai trò |
|---|---|---|---|---|---|
| Pillar | Dịch vụ vận chuyển hàng lẻ LCL | `vận chuyển hàng lẻ`, `dịch vụ LCL`, `hàng lẻ` | Commercial | `/hang-le-post1987.html` | Trang trung tâm, nhận lead và giải thích dịch vụ. |
| Cluster 1 | Khái niệm LCL và gom hàng | `LCL là gì`, `hàng consol là gì`, `gom hàng là gì`, `consolidation là gì`, `consolidator là gì` | Informational | `/hang-le-post1987.html` trước mắt | Gom toàn bộ intent định nghĩa về trang trung tâm để tránh chia nhỏ khi dữ liệu còn thấp. |
| Cluster 2 | Cách tính cước LCL | `W/M là gì`, `RT`, `CBM`, `cách tính cước hàng LCL`, `trọng lượng quy đổi` | Operational / Commercial | `/huong-dan-cach-tinh-trong-luong-trong-van-chuyen-duong-hang-khong-va-duong-bien-lcl-chi-tiet-post2057.html` | Bài vệ tinh giải thích cách tính; link ngược về trang LCL để nhận báo giá. |
| Cluster 3 | Tuyến và lịch vận chuyển đường biển | `tuyến vận chuyển hàng LCL`, `LCL đi direct`, `LCL đi via`, `lịch tàu LCL` | Commercial | `/cac-tuyen-duong-van-chuyen-chinh-tai-everest-logistics-post2062.html` và `/dich-vu/van-chuyen-duong-bien` | Bài/landing page hỗ trợ quyết định tuyến; chỉ dùng tuyến và lịch đã xác nhận. |
| Cluster 4 | Hồ sơ và thông quan hàng LCL | `chứng từ gửi hàng LCL`, `tờ khai hàng LCL`, `hải quan hàng LCL` | Commercial / Do | `/dich-vu/dich-vu-hai-quan` | Liên kết dịch vụ hải quan khi bài LCL đề cập hồ sơ và thủ tục. |
| Cluster 5 | Lấy hàng và giao hàng nội địa | `vận chuyển LCL về kho`, `giao hàng LCL`, `vận tải nội địa hàng LCL` | Transactional | `/dich-vu/van-tai-noi-dia` | Chỉ liên kết khi nội dung nói đến chặng lấy/giao hàng. |

## 3. Internal-link plan đã xác nhận

| Source URL | Anchor text | Target URL | Context/reason | Confidence | Verification |
|---|---|---|---|---|---|
| `/hang-le-post1987.html` | `vận chuyển đường biển` | `https://everlog.com.vn/dich-vu/van-chuyen-duong-bien` | Đặt ở phần giải thích LCL là hình thức vận chuyển bằng đường biển. | Cao | Đã mở URL live; trang có mục LCL, FCL và cước đường biển. |
| `/hang-le-post1987.html` | `cách tính trọng lượng và cước LCL` | `https://everlog.com.vn/huong-dan-cach-tinh-trong-luong-trong-van-chuyen-duong-hang-khong-va-duong-bien-lcl-chi-tiet-post2057.html` | Đặt ở phần chi phí/W/M để chuyển người đọc sang bài tính cước chuyên sâu. | Cao | Đã mở URL live; bài có section tính cước đường biển LCL và RT. |
| `/hang-le-post1987.html` | `các tuyến đường vận chuyển chính` | `https://everlog.com.vn/cac-tuyen-duong-van-chuyen-chinh-tai-everest-logistics-post2062.html` | Đặt ở phần direct/via hoặc CTA khi người đọc cần xem tuyến. | Trung bình | URL live đã mở; cần kiểm tra lại tuyến LCL cụ thể trước khi publish link trong CMS. |
| `/hang-le-post1987.html` | `dịch vụ hải quan trọn gói` | `https://everlog.com.vn/dich-vu/dich-vu-hai-quan` | Đặt tại phần hồ sơ/tờ khai khi người đọc cần hỗ trợ thông quan. | Cao | Đã mở URL live; đúng intent dịch vụ hải quan. |
| `/hang-le-post1987.html` | `vận tải nội địa` | `https://everlog.com.vn/dich-vu/van-tai-noi-dia` | Đặt tại phần quy trình đưa hàng về kho hoặc giao hàng. | Trung bình | URL nằm trong cấu trúc dịch vụ Everlog; cần xác nhận nội dung live trước khi publish. |

## 4. Quy tắc triển khai cluster

- Giữ `/hang-le-post1987.html` làm trang trung tâm cho `vận chuyển hàng lẻ`, `dịch vụ LCL`, `gom hàng LCL` và các định nghĩa liên quan.
- Bài tính trọng lượng là cluster gần nhất để xử lý `W/M`, `RT`, `CBM` và cách tính cước; hai bài cần liên kết hai chiều.
- Trang vận chuyển đường biển là parent service; trang LCL liên kết lên parent bằng anchor mô tả rõ.
- Trang tuyến vận chuyển chỉ dùng để hỗ trợ quyết định tuyến; không đưa toàn bộ danh sách tuyến vào bài LCL nếu không phục vụ intent.
- Không tạo bài riêng cho `đi via là gì` ở thời điểm này vì dữ liệu mới chỉ có 3 impressions; tiếp tục theo dõi MCP GSC.
- Không dùng anchor chung như `xem thêm`, `tại đây` hoặc `bài viết` khi đã có anchor mô tả cụ thể.
- Kiểm tra canonical và redirect giữa `everlog.com.vn` và `everlog.vn` trước khi triển khai hàng loạt internal link.
