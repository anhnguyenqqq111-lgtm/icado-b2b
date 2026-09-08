# Kế hoạch audit và sửa nội dung Everlog

**Website:** [everlog.com.vn](https://everlog.com.vn/)  
**Phạm vi:** 15 URL trọng điểm gồm trang chủ, trang dịch vụ, bài blog và 5 bài Incoterms 2020.  
**Dữ liệu:** MCP Google Search Console, MCP GA4, rà soát nội dung live trên Everlog và nghiên cứu SERP đối thủ.  
**Khoảng thời gian dữ liệu GSC/GA4:** 08/06/2026–06/09/2026.  
**Mục đích:** Lập kế hoạch sửa nội dung và technical SEO; chưa chỉnh trực tiếp nội dung trên website.

## 1. Lưu ý về phương pháp

Đã thử mở SERP bằng Guest/Clean Session theo quy trình phân tích đối thủ. Môi trường hiện tại chặn Chrome Guest do lỗi quyền Crashpad, nên phần SERP được đối chiếu bằng live web search và mở trực tiếp các trang đối thủ truy cập được. Vì vậy, báo cáo dùng cụm **“đối thủ được quan sát trong SERP”**, không khẳng định thứ hạng tuyệt đối tại mọi thời điểm, thiết bị hoặc vị trí địa lý.

Các bài local trong workspace được dùng để kiểm tra outline, câu chữ và liên kết. Nội dung live trên `everlog.com.vn` được xem là phiên bản cần ưu tiên đối chiếu trước khi triển khai.

## 1.1. Keyword đã research và thứ hạng đối thủ trước phần phân tích

Đây là bảng SERP snapshot cần đọc trước khi vào phần đánh giá nội dung. **Vị trí đối thủ** là thứ tự kết quả được trả về trong lần tìm kiếm live ngày 06/09/2026; đây không phải thứ hạng cố định cho mọi người dùng. Vị trí có thể thay đổi theo địa điểm, thiết bị, lịch sử tìm kiếm, truy vấn chính xác và thời điểm crawl.

`GSC position` là vị trí trung bình 90 ngày của URL Everlog trong GSC. `SERP observed` là thứ tự quan sát được trong live web search. Khi công cụ không trả về đủ danh sách ổn định, mình ghi rõ `chưa xác nhận` thay vì tự suy đoán.

| Keyword đã research | GSC position của Everlog | SERP observed — đối thủ và vị trí | URL/đối chiếu |
|---|---:|---|---|
| `vận chuyển đường biển` | Everlog 7,2 | Interlink #1; Everlog xuất hiện #2 trong truy vấn tập trung; KVN #3 | [Interlink](https://interlink.com.vn/dich-vu-chi-tiet/van-chuyen-duong-bien/), [KVN](https://kvnlogistics.vn/vi/van-chuyen-duong-bien/) |
| `dịch vụ khai báo hải quan` | Trang hải quan 12,7 | IQ Logistics #1; HML #2; G.O.L #3; Everlog không xuất hiện trong nhóm kết quả trả về | [IQ](https://iql.com.vn/?tt-service=custom-brokerage), [HML](https://hml.com.vn/dich-vu/dich-vu-khai-bao-hai-quan/), [G.O.L](https://gol.vn/services/khai-bao-ho/) |
| `vận chuyển hàng lẻ` | Trang hàng lẻ 23,0; query cụ thể 44,1 | Simba #1; Kim Phú #2; Thông Tiến #3; Ascent #4 | [Simba](https://simbagroup.vn/van-chuyen-hang-le-lcl?aelang=vi), [Kim Phú](https://vantaikimphu.vn/dich-vu/van-chuyen-hang-le-hang-ghep-4.html), [Thông Tiến](https://thongtien.com/tin-tuc/van-chuyen-hang-le/) |
| `gom hàng LCL` | Query 19,7 | Kết quả thiên về bài giải thích LCL của FedEx/Kuehne+Nagel và các trang dịch vụ; thứ tự đối thủ không ổn định | [FedEx LCL](https://www.fedex.com/vi-vn/shipping/glossary/what-is-less-than-container-load-lcl.html), [Kuehne+Nagel LCL](https://www.kuehne-nagel.com/vn/services/sea-freight/lcl) |
| `các loại container thông dụng` | Bài container 16,3; hiện Crawled - currently not indexed | KVN #1; Anzen #2; Dido Inoxưởng #3; Topmoving #4; GSCVN #5; Everlog chưa hiển thị ổn định | [KVN](https://kvnlogistics.vn/vi/cac-loai-container-pho-bien-trong-van-tai-bien/), [Anzen](https://vantaianzen.vn/cac-loai-container/), [GSCVN](https://www.gscvn.com.vn/index.php/vi/tin-tuc/dac-diem-ky-thuat-container/90-phan-loai-container) |
| `cont FL` / `flat rack container` | Query `cont fl` 5,6 | KVN và các bài container chuyên dụng được quan sát; chưa có snapshot sạch đủ để chốt top 3 riêng cho `cont FL` | [KVN container](https://kvnlogistics.vn/vi/cac-loai-container-pho-bien-trong-van-tai-bien/), [PTN container chuyên dụng](https://ptnlogistics.com/container-chuyen-dung/) |
| `giá EXW là gì` | 8,2 | Thư viện Pháp luật #1; FedEx #2; GHN #3; Gateway #4; Everlog xuất hiện #5 | [Thư viện Pháp luật](https://thuvienphapluat.vn/phap-luat/gia-exw-la-gi-cach-tinh-gia-exw-cach-tinh-tri-gia-fob-tu-gia-exw-trong-xuat-nhap-khau-nhu-the-nao-45624-232412.html), [FedEx EXW](https://www.fedex.com/vi-vn/shipping/glossary/what-is-ex-exw.html), [Gateway EXW](https://gatewayexpress.vn/bai-viet/gia-xuat-xuong-la-gi/) |
| `phí EXW thuế suất bao nhiêu` | Query 8,1 | SERP không ổn định; các bài EXW giải thích thuế theo HS/nước nhập khẩu, không có “thuế suất EXW” cố định | Dùng [bài EXW Everlog](https://everlog.com.vn/gia-exw-la-gi-post2073.html) làm trang trả lời chính |
| `giá CFR là gì` | 64,7 | VM Style #1; Tuyền Logistics #2; Cộng đồng Logistics xuất hiện trong nhóm kết quả; Everlog chưa vào nhóm đầu | [VM Style](https://vmstyle.vn/hoi-dap/gia-cfr-la-gi/), [Tuyền Logistics](https://dichvuvantaibien.com/gia-cfr-la-gi/), [Cộng đồng Logistics](https://www.congdonglogistics.com/cfr-la-gi-gia-cfr-la-gi/) |
| `giá CIF là gì` | 18,0 | VietnamFinance, TSL và OHP được trả về; thứ tự top 3 không ổn định trong snapshot hiện tại | [VietnamFinance](https://vietnamfinance.vn/gia-cif-la-gi-incoterms-la-gi-d20314.html), [TSL CIF](https://tsl.com.vn/cif-la-gi/), [OHP CIF](https://www.ohp.vn/chi-tiet/tin-tuc/cif-la-gi-trong-xuat-nhap-khau/4649) |
| `giá DDP là gì` | 87,6 | TSL là đối thủ giải thích trực tiếp được quan sát; Everlog có kết quả live nhưng đang ở vị trí GSC rất thấp; top 3 không chốt được từ snapshot sạch | [TSL DDP](https://tsl.com.vn/ddp-la-gi/), [Everlog DDP](https://everlog.com.vn/gia-ddp-la-gi-post2075.html) |
| `giá FOB là gì` | 16,0 | Thư viện Pháp luật #1; Dữ liệu Pháp luật #2; Thư viện Pháp luật bài khác #3; VietnamBiz #4; GHN #5 | [Thư viện Pháp luật](https://thuvienphapluat.vn/phap-luat-doanh-nghiep/cau-hoi-thuong-gap/gia-fob-la-gi-gia-cif-la-gi-phan-biet-gia-cif-va-gia-fob-9344.html), [Dữ liệu Pháp luật](https://dulieuphapluat.vn/dinh-nghia/tri-gia-fob-8724.html), [GHN FOB](https://ghn.vn/blogs/thong-tin-giao-hang/fob-la-gi) |
| `W/M là gì`, `W/M là gì trong xuất nhập khẩu` | Bài trọng lượng 17,6; query 8,6 | Gateway và các trang calculator/giải thích chargeable weight được quan sát; chưa có thứ tự top 3 ổn định cho đúng biến thể Việt ngữ | [Gateway](https://gatewayexpress.vn/bai-viet/cach-tinh-cuoc-van-chuyen-quoc-te/), [Avenir calculator](https://www.avenir.vn/cong-cu/tinh-cuoc-container) |
| `chargeable weight là gì` | Query 68,6 | Gateway và các bài tính cước quốc tế là nhóm đối thủ nội dung; Everlog chưa có lợi thế thứ hạng | [Gateway](https://gatewayexpress.vn/bai-viet/cach-tinh-cuoc-van-chuyen-quoc-te/) |
| `thủ tục nhập khẩu thức ăn chó mèo` | 12,3 | 3W Logistics là đối thủ nội dung chính được mở và đối chiếu; snapshot SERP không trả về vị trí ổn định trong lần cuối | [3W Logistics](https://3w-logistics.com/vi/quy-trinh-thu-tuc-nhap-khau-thuc-an-cho-meo/), [Everlog](https://everlog.com.vn/thu-tuc-nhap-khau-thuc-an-cho-meo-post2038.html) |
| `tạm nhập tái xuất hàng triển lãm` | Bài triển lãm 8,0 | Cổng Dịch vụ công Quốc gia xuất hiện đầu; VietSupplyChain là đối thủ hướng dẫn chuyên sâu được quan sát; Everlog đang ở top 10 theo GSC | [Cổng DVC](https://dichvucong.gov.vn/p/home/dvc-chi-tiet-thu-tuc-nganh-doc.html?ma_thu_tuc=1.006468), [VietSupplyChain](https://vietsupplychain.com/tin-tuc/quy-trinh-tam-nhap-tai-xuat-hang-trien-lam/), [Everlog](https://everlog.com.vn/trung-bay-%E2%80%93-trien-lam-post1996.html) |

### Đối thủ đang viết những gì ở các vị trí đầu

- **Trang dịch vụ:** đối thủ không chỉ nói “giá tốt/chuyên nghiệp”; họ đưa rõ loại dịch vụ, tuyến, tải trọng hoặc nhóm hàng, thời gian dự kiến, quy trình, hồ sơ cần gửi, tracking và form báo giá. Ví dụ: [Prefer](https://prefer.com.vn/van-chuyen-duong-bien/) tách FCL, LCL, Breakbulk, door-to-door, hải quan và tracking; [Allship](https://logistic.allship.vn/dich-vu-hai-quan/) tách dịch vụ A–Z, hồ sơ, chi phí, quy trình và FAQ.
- **Bài thủ tục:** các bài mạnh thường có điều kiện áp dụng, checklist hồ sơ, quy trình từng bước, thuế/chi phí, rủi ro và câu hỏi thường gặp. [3W Logistics](https://3w-logistics.com/vi/quy-trinh-thu-tuc-nhap-khau-thuc-an-cho-meo/) là mẫu rõ cho nhóm thức ăn chó mèo.
- **Bài kỹ thuật:** đối thủ ưu tiên bảng thông số, ví dụ, cách chọn và cảnh báo sai số thực tế. [KVN](https://kvnlogistics.vn/vi/cac-loai-container-pho-bien-trong-van-tai-bien/) ghi rõ thông số container có thể khác theo hãng tàu/series.
- **Bài Incoterms:** các kết quả đầu trả lời rất sớm định nghĩa, chi phí, điểm chuyển rủi ro, trách nhiệm và một ví dụ; các bài dài hơn mới mở rộng sang so sánh, thuế và tình huống Việt Nam. [Thư viện Pháp luật về EXW](https://thuvienphapluat.vn/phap-luat/gia-exw-la-gi-cach-tinh-gia-exw-cach-tinh-tri-gia-fob-tu-gia-exw-trong-xuat-nhap-khau-nhu-the-nao-45624-232412.html) có lợi thế ở định nghĩa và công thức; [FedEx EXW](https://www.fedex.com/vi-vn/shipping/glossary/what-is-ex-exw.html) có lợi thế ở cách giải thích ngắn.

**Cách đọc bảng:** thứ hạng đối thủ chỉ là lớp dữ liệu đầu vào. Ý chính phía sau vẫn phải dựa trên GSC của Everlog, intent, chất lượng nội dung, độ tin cậy pháp lý và khả năng chuyển đổi; không copy cấu trúc hoặc chạy theo số chữ của một đối thủ đơn lẻ.

### 1.2. Quy trình SERP chuẩn cần dùng từ lần audit tiếp theo

Bảng trên là **SERP tham khảo từ live web search**, không phải dữ liệu SERP cá nhân hóa của tài khoản/máy bạn. Để khắc phục, cần dùng file export từ máy bạn làm nguồn xếp hạng chính:

1. Chạy rank-checker local bằng Puppeteer, không lấy thứ hạng từ câu trả lời của AI.
2. Cấu hình đúng địa điểm, ngôn ngữ, thiết bị và Google domain. File hiện có UULE mặc định `Tan Phu, Ho Chi Minh City, Vietnam`; cần đổi theo vị trí bạn muốn đo.
3. Chạy đúng keyword nguyên văn, mỗi keyword 2–3 lần ở cùng một cấu hình; lưu ngày/giờ và cấu hình.
4. Lấy top 5 URL organic, loại Everlog, quảng cáo, local pack, video, PAA và trang tag/category không cùng intent.
5. Gửi JSON/CSV kết quả vào workspace; bước phân tích đối thủ chỉ được dùng các URL này và phải giữ nguyên rank đã export.

#### Lệnh chạy công cụ có sẵn

```bash
cd /Users/t.anh/.gemini/antigravity-ide/scratch/goha-seo-main/tools/rank-checker
npm install
npm start
```

Sau đó mở `http://localhost:3000`, nhập project/domain/keywords và chạy check. Công cụ đã có chức năng trích xuất top competitor URLs, PAA và related searches.

Có thể chạy trực tiếp qua API local, không cần nhập keyword vào Google Sheet:

```bash
curl -X POST http://localhost:3000/api/checker/start \\
  -H 'Content-Type: application/json' \\
  -d '{
    "project": "Everest-Logistics",
    "domain": "everlog.com.vn",
    "keywords": [
      "vận chuyển đường biển",
      "dịch vụ khai báo hải quan",
      "vận chuyển hàng lẻ",
      "giá EXW là gì",
      "giá CFR là gì",
      "giá CIF là gì",
      "giá DDP là gì",
      "giá FOB là gì"
    ],
    "options": {
      "maxPages": 1,
      "chunkSize": 1,
      "uuleLocation": "Tan Phu, Ho Chi Minh City, Vietnam"
    }
  }'
```

Sau khi check xong, lấy dữ liệu SERP đã lưu:

```bash
curl http://localhost:3000/api/serp-data/Everest-Logistics > /tmp/everlog-serp.json
```

Nếu muốn khớp gần nhất với SERP bạn đang nhìn thấy, cần thống nhất thêm desktop/mobile, thành phố/quận, ngôn ngữ `vi-VN`, Google domain, SafeSearch và trạng thái đăng nhập. Không nên dùng `curl` trực tiếp vào trang Google để parse HTML vì thường gặp consent/CAPTCHA và markup không ổn định; Puppeteer local phù hợp hơn.

#### Quy tắc sử dụng rank sau khi có export local

- `Local SERP rank`: nguồn chính để ghi rank đối thủ trong báo cáo.
- `GSC average position`: nguồn chính để đánh giá vị trí Everlog trong 28/90 ngày.
- `AI/live web search`: chỉ dùng để tìm thêm URL/ý tưởng, không dùng để kết luận đối thủ đang đứng #1–#10.
- Nếu rank thay đổi giữa 3 lần chạy, ghi khoảng rank và thời điểm, ví dụ `#2–#4`, thay vì chọn một con số tùy ý.
- Nếu kết quả có quảng cáo, PAA hoặc local pack, ghi riêng SERP feature; không đánh nhầm chúng là organic rank.

#### Kết quả thử local ngày 06/09/2026

Đã cài dependency và chạy rank-checker với 16 keyword, location `Tan Phu, Ho Chi Minh City, Vietnam`, `maxPages=1`, `chunkSize=1`. Google trả về trang **“Hệ thống của chúng tôi đã phát hiện thấy lưu lượng truy cập bất thường”**; tool nhận diện được một số SERP feature nhưng nhiều kết quả organic trả `url: -`. Vì vậy, snapshot lần này **không được dùng để thay rank trong bảng**.

Để tiếp tục check mà vẫn đáng tin cậy, cần một trong các phương án sau:

- Chạy công cụ trên mạng/IP của bạn và gửi JSON/CSV; đây là phương án khớp SERP địa phương tốt nhất.
- Dùng SERP API có cấu hình location/device/language cố định; cần API key và chi phí dịch vụ.
- Gửi ảnh hoặc export kết quả từ Chrome đang dùng; đây là phương án duy nhất để khớp gần như nguyên trạng SERP cá nhân hóa của tài khoản bạn.

Không nên tiếp tục retry nhiều lần trên IP hiện tại vì có thể làm CAPTCHA kéo dài và làm dữ liệu rank sai lệch.

## 2. Tóm tắt cơ hội SEO từ GSC và GA4

| Nhóm | URL / tín hiệu | Nhận định |
|---|---|---|
| Cơ hội lớn nhất | `/dich-vu/tam-nhap-%E2%80%93-tai-xuat` — 627 impressions, 5 clicks, CTR 0,80%, vị trí 6,9 | Đã gần trang đầu nhưng title/URL/query chưa sạch; ưu tiên sửa để tăng CTR và bao phủ intent thủ tục. |
| Blog có thể kéo traffic | `/trung-bay-%E2%80%93-trien-lam-post1996.html` — 387 impressions, 11 clicks, vị trí 8,0 | Có tín hiệu tốt; cần mở rộng checklist, quy trình, deadline và CTA. |
| Khoảng trống chuyển đổi | `/hang-le-post1987.html` — 403 impressions, 4 clicks, vị trí 23,0 | Query “vận chuyển hàng lẻ” có 57 impressions nhưng đang ở vị trí 44,1; cần rewrite theo intent dịch vụ LCL. |
| Bài tính cước | Bài trọng lượng — 337 impressions, 2 clicks, vị trí 17,6 | Query `w/m là gì` có 41 impressions, vị trí 8,6; nên tách rõ W/M, chargeable weight và ví dụ tính. |
| Bài thủ tục có nhu cầu | Bài thức ăn chó mèo — 466 impressions, 4 clicks, vị trí 12,3 | Query “thủ tục nhập khẩu thức ăn chó mèo” có 34 impressions; cần làm rõ kiểm dịch, hồ sơ và quy trình. |
| Incoterms mạnh nhất | EXW — 213 impressions, 8 clicks, CTR 3,76%, vị trí 8,2 | Có thể tăng CTR bằng câu trả lời trực tiếp cho “giá EXW bao gồm gì/thuế suất bao nhiêu”. |
| Incoterms cần cứu | CIF — 161 impressions, 1 click, vị trí 18,0; FOB — 71 impressions, 1 click, vị trí 16,0 | Nội dung khá dài nhưng chưa khớp đủ query thực dụng và cần cải thiện snippet. |
| Incoterms chưa có lực | CFR — 6 impressions, vị trí 64,7; DDP — 5 impressions, vị trí 87,6 | Cần kiểm tra index, độ khớp title–H1–query và giảm phần diễn giải nặng tính quảng cáo. |
| Technical nghiêm trọng | `/cac-loai-container-thong-dung-post2035.html` — Crawled - currently not indexed | Không xóa bài. Sửa chất lượng, kiểm tra template, liên kết nội bộ và request indexing lại. |
| Chuyển đổi | GA4 ghi nhận 0 conversion trong snapshot | Mọi trang dịch vụ cần CTA có tracking: gọi điện, Zalo, form báo giá, click email và gửi form. |

### Query GSC nên dùng làm trục nội dung

| Cụm query | Tín hiệu | Trang đích nên giữ |
|---|---:|---|
| `logistics`, `công ty logistics` | 174 / 103 impressions; vị trí trang chủ 5,5 / 2,5 | Trang chủ |
| `vận chuyển hàng lẻ`, `gom hàng LCL` | 57 / 15 impressions | Trang hàng lẻ/LCL |
| `w/m là gì`, `w/m là gì trong xuất nhập khẩu` | 41 / 9 impressions | Bài tính cước/trọng lượng |
| `chargeable weight là gì` | 24 impressions | Bài tính cước/trọng lượng |
| `kiểm xưởng là gì` | 40 impressions; vị trí 7,3 | Bài kiểm xưởng; không nhập vào bài khác |
| `cont fl` | 39 impressions; vị trí 5,6 | Bài container |
| `thủ tục nhập khẩu thức ăn chó mèo` | 34 impressions; vị trí 26,6 | Bài thức ăn chó mèo |
| Các biến thể “tạm nhập tái xuất” | nhiều query 9–53 impressions, một số vị trí 3–9 | Trang dịch vụ tạm nhập/tái xuất và bài triển lãm; cần phân intent |
| `phí exw thuế suất bao nhiêu` | 10 impressions; vị trí 8,1 | Bài EXW; phải trả lời rõ đây không phải một “thuế suất EXW” cố định |

### GA4 cần dùng để quyết định nội dung

- Trang vận chuyển đường biển: 145 sessions, engagement rate 38,62%, bounce rate 61,38% — có traffic nhưng phần mở đầu/CTA chưa giữ người dùng tốt.
- Trang hải quan: 73 sessions, engagement rate 46,58% — cần đưa quy trình, hồ sơ và phạm vi phí lên sớm hơn.
- Trang vận tải nội địa: 40 sessions, engagement rate 42,50% — cần bổ sung tuyến, tải trọng, thời gian giao và bằng chứng năng lực.
- Trang chủ: 405 sessions, engagement rate 64,94%; tuy nhiên số liệu conversion đang bằng 0 — ưu tiên đo lường trước khi kết luận CTA không hiệu quả.
- Các bài EXW/CIF/DDP/FOB có sessions rất thấp; chưa đủ dữ liệu để đánh giá chất lượng hành vi riêng từng bài, nên dùng GSC và kiểm tra thứ hạng làm chỉ báo chính.

## 3. Các vấn đề technical toàn site cần xử lý trước

### P0 — Domain, canonical và liên kết nội bộ

1. Chọn một domain chuẩn. GSC đang dùng `https://everlog.com.vn/`, trong khi footer và nhiều bài local dẫn sang `everlog.vn`. Cần thống nhất một hostname cho canonical, sitemap, internal link, schema, email và CTA.
2. Kiểm tra redirect 301 giữa hai domain; không để cùng một nội dung index ở cả `everlog.com.vn` và `everlog.vn`.
3. Crawl toàn site để tìm link cũ hoặc sai slug. Bản nháp có các link như `/dich-vu/hai-quan/`, `/dich-vu/van-chuyen-quoc-te/`, trong khi URL live đang được GSC ghi nhận là `/dich-vu/dich-vu-hai-quan` và `/dich-vu/van-chuyen-duong-bien`. Nếu các link cũ không redirect 301, cần thay trực tiếp.
4. Xác nhận canonical tự trỏ, sitemap chỉ chứa URL chuẩn, hreflang không được tạo thừa nếu website chỉ có tiếng Việt.

### P0 — Index và spam parameter

1. Với bài container: kiểm tra `noindex`, robots, canonical, thin/duplicate content, liên kết nội bộ và rendering HTML; sau khi sửa gửi request indexing.
2. GA4 từng ghi nhận một landing URL `/tin-tuc?page=...` chứa chuỗi HTML/event handler đã encode. GSC chưa biết URL này và không crawl nó, nhưng cần xử lý như một cảnh báo bảo mật/parameter:
   - validate và encode giá trị `page` ở server;
   - chặn input HTML/JavaScript trong query parameter;
   - đặt canonical/noindex cho các trang lọc không có giá trị SEO;
   - rà soát log truy cập, WAF và template render danh sách tin.

### P1 — Template, schema và đo lường

1. Trang chủ hiển thị các bộ đếm “SỐ NĂM HOẠT ĐỘNG”, “NHÂN VIÊN”, “KHÁCH HÀNG” nhưng giá trị quan sát được bị trống. Hoặc nạp số liệu thật, hoặc bỏ block này.
2. Thêm Organization/LocalBusiness schema chỉ với thông tin có thể xác minh; dùng cùng tên, địa chỉ, điện thoại, domain.
3. FAQ schema chỉ dùng khi FAQ hiển thị thật trên trang và tuân thủ điều kiện của Google; không thêm schema chỉ để “làm đẹp” kết quả.
4. Thiết lập GA4 events và đánh dấu conversion cho `click_tel`, `click_zalo`, `submit_quote`, `click_email`, `click_whatsapp` nếu có. Gắn UTM cho các CTA trong bài blog.
5. Kiểm tra Core Web Vitals, ảnh hero, lazy-load ảnh dưới màn hình đầu tiên, alt ảnh, font và layout shift trên mobile.

## 4. Benchmark đối thủ theo nhóm intent

### 4.1. Dịch vụ đường biển

[Prefer Logistics](https://prefer.com.vn/van-chuyen-duong-bien/) tổ chức trang theo các module dễ chuyển đổi: FCL, LCL, Breakbulk, door-to-door, hải quan, tracking; tiếp theo là lợi thế dịch vụ, tuyến chính và form báo giá. Đây là cấu trúc nên học về độ rõ ràng, không sao chép câu chữ.

[Embassy Freight](https://new.embassyfreight.vn/vi/dich-vu/van-tai-duong-bien) nhấn vào FCL/LCL, door-to-door, chứng từ, thông quan và bằng chứng vận hành. [Hana Logistics](https://hanalogisticsvn.com/) cũng trình bày dịch vụ theo card, tuyến và phương tiện thay vì chỉ dùng đoạn giới thiệu dài.

**Khoảng trống của Everlog:** cần đưa loại hàng, tuyến, thời gian dự kiến, dữ liệu cần để báo giá và CTA lên trước phần diễn giải dài; đồng thời phải phân biệt rõ dịch vụ FCL, LCL, sea-air và trucking.

### 4.2. Dịch vụ hải quan

[Allship — Dịch vụ Hải quan](https://logistic.allship.vn/dich-vu-hai-quan/) có cấu trúc mạnh về chuyển đổi: promise rõ ở hero, dịch vụ A–Z, hồ sơ cần chuẩn bị, bảng phí/cấu trúc chi phí, nhóm khách hàng, quy trình 5 bước, FAQ và CTA. Các claim như thời gian 4–8 giờ, tỷ lệ luồng xanh hoặc số năm kinh nghiệm chỉ nên dùng khi Everlog có dữ liệu chứng minh tương đương.

[Interlink](https://interlink.com.vn/dich-vu-chi-tiet/van-chuyen-duong-bien/) và [NASA Customs](https://haiquannasa.com/dich-vu-hai-quan) cho thấy người dùng B2B thường tìm dịch vụ trọn gói, đại lý hải quan, giấy phép chuyên ngành, hoàn thuế và hỗ trợ từ A–Z.

**Khoảng trống của Everlog:** H1 hiện tại dài và có lỗi “khái báo”; cần chuyển lợi ích và checklist hồ sơ lên ngay sau hero.

### 4.3. Vận tải nội địa

SERP đối thủ như [Allship](https://logistic.allship.vn/dich-vu-van-chuyen-noi-dia/), [Protrans](https://protrans.com.vn/vi/dich-vu/van-tai-noi-dia) và [InterLOG](https://interlog.com.vn/dich-vu/van-tai-noi-dia/) đều nhấn vào tuyến, tải trọng/phương tiện, thời gian giao và khả năng door-to-door.

**Khoảng trống của Everlog:** phải biến trang thành trang dịch vụ có thể báo giá, không chỉ là bài giới thiệu chung.

### 4.4. Tạm nhập tái xuất và hàng triển lãm

[Nguồn Bộ Tài chính về thủ tục hàng hội chợ/triển lãm](https://dichvucong.mof.gov.vn/web/guest/dich-vu-cong-truc-tuyen) là nhóm nguồn cần dùng để kiểm tra căn cứ pháp lý, thời gian xử lý và lệ phí. [MISA AMIS](https://amis.misa.vn/) có nội dung giải thích khái niệm nhưng cần ưu tiên nguồn nhà nước khi chốt claim pháp lý.

**Khoảng trống của Everlog:** cần tách “dịch vụ tạm nhập tái xuất” và “hướng dẫn hàng triển lãm”, nhưng liên kết chặt bằng checklist chung: hàng gì, chiều nhập/xuất, hồ sơ, thời hạn, xử lý bán nội địa, vận chuyển tới địa điểm triển lãm.

### 4.5. Blog logistics và thủ tục

- [3W Logistics — nhập khẩu thức ăn chó mèo](https://3w-logistics.com/vi/quy-trinh-thu-tuc-nhap-khau-thuc-an-cho-meo/) bao phủ điều kiện pháp lý, HS, chứng từ, quy trình kiểm dịch/kiểm tra chất lượng, thuế, rủi ro và FAQ.
- [Gateway Express — cách tính cước](https://gatewayexpress.vn/bai-viet/cach-tinh-cuoc-van-chuyen-quoc-te/) tách gross weight, volumetric weight và chargeable weight, có công cụ tính; Everlog nên có ví dụ tương tự nhưng phải ghi rõ divisor thay đổi theo hãng/phương thức.
- [KVN Logistics — các loại container](https://kvnlogistics.vn/vi/cac-loai-container-pho-bien-trong-van-tai-bien/) nhấn mạnh loại cont, kích thước, tải trọng, cách chọn và cảnh báo thông số thay đổi theo hãng tàu/series.

### 4.6. Incoterms

[Thư viện Pháp luật — EXW](https://thuvienphapluat.vn/phap-luat/gia-exw-la-gi-cach-tinh-gia-exw-cach-tinh-tri-gia-fob-tu-gia-exw-trong-xuat-nhap-khau-nhu-the-nao-45624-232412.html) có lợi thế ở định nghĩa, công thức và liên hệ trị giá FOB. [FedEx — EXW](https://www.fedex.com/vi-vn/shipping/glossary/what-is-ex-exw.html) và [FedEx — CFR](https://www.fedex.com/vi-vn/shipping/glossary/what-is-cfr.html) trình bày ngắn, trả lời trực tiếp trách nhiệm các bên. [TSL — CIF](https://tsl.com.vn/cif-la-gi/) và [TCL Freight — FOB](https://tclfreight.com.vn/fob-la-gi/) là các mẫu nội dung thương mại dễ đọc.

**Khoảng trống của Everlog:** bản nháp chi tiết hơn nhiều đối thủ nhưng dễ bị “quá chuyên gia”: câu mở đầu dài, nhiều claim pháp lý chưa gắn nguồn tại chỗ, ví dụ chưa nhất quán và một số CTA/link dùng domain hoặc slug cũ.

### 4.7. Bước bổ sung: đo độ dài đối thủ rồi quyết định cắt và viết lại

Không đặt mục tiêu “dài hơn đối thủ” một cách máy móc. Google không xếp hạng chỉ vì số chữ. Độ dài cần đủ để giải quyết toàn bộ intent chính, nhưng phần thông tin hữu ích phải đứng trước phần mở rộng. Quy trình mới cho từng URL:

1. Lấy 3–5 kết quả organic cùng intent; loại phần menu, footer, quảng cáo, bình luận và block liên quan.
2. Ghi lại heading, chủ đề, bảng, checklist, ví dụ, FAQ, CTA và độ dài **nội dung chính hữu ích** của từng đối thủ.
3. Tính khoảng thấp–cao và trung vị tham khảo; không lấy một bài quá dài làm chuẩn duy nhất.
4. Đếm riêng bài Everlog: metadata, heading, nội dung chính, bảng, FAQ và CTA. Không cộng navigation/footer vào số chữ.
5. Đối chiếu theo 4 câu hỏi: Everlog có thiếu intent nào không? Có giải thích trùng không? Có đoạn dài nhưng không giúp người đọc ra quyết định không? Có claim nào cần cắt vì không chứng minh được không?
6. Chốt một trong ba hướng: **giữ độ dài và viết lại**, **rút gọn có chủ đích**, hoặc **mở rộng có điều kiện**.
7. Sau khi chốt phạm vi, viết lại theo thứ tự: câu trả lời trực tiếp → bảng/step-by-step → giải thích sâu → FAQ → CTA. Không kéo dài bài bằng keyword lặp.

#### Chuẩn độ dài đề xuất cho Everlog

Đây là **khoảng mục tiêu sau khi viết lại**, không phải cam kết thứ hạng. Khoảng này dựa trên độ phức tạp intent, cấu trúc đối thủ đã quan sát và lượng thông tin cần thiết cho người dùng B2B.

| Loại trang | Độ dài nội dung chính nên hướng tới | Nguyên tắc |
|---|---:|---|
| Trang dịch vụ đơn tuyến | 900–1.400 từ | Đủ dịch vụ, tuyến, quy trình, dữ liệu báo giá, FAQ và CTA; không biến thành bài giáo trình. |
| Trang dịch vụ hải quan | 1.200–1.800 từ | Cần thêm hồ sơ, nhóm dịch vụ, quy trình, phạm vi phí và trường hợp chuyên ngành. |
| Trang tạm nhập/tái xuất | 1.200–1.800 từ | Ưu tiên điều kiện, hồ sơ, thời hạn, quy trình và nhánh xử lý ngoại lệ. |
| Bài dịch vụ LCL | 1.400–2.000 từ | Phải giải thích LCL, cách tính, chi phí, quy trình và form báo giá. |
| Bài hướng dẫn thủ tục chuyên ngành | 1.800–2.600 từ | Dùng checklist và quy trình; mọi claim pháp lý phải được xác minh. |
| Bài kỹ thuật container/W/M | 1.400–2.200 từ | Bảng và ví dụ quan trọng hơn đoạn văn dài. |
| Bài giải thích Incoterms | 1.600–2.400 từ | Định nghĩa, cost/risk, trách nhiệm, ví dụ, so sánh và tình huống Việt Nam. |

#### Đánh giá độ dài bản nháp hiện tại

Số chữ dưới đây là số chữ của file `article.md`, đã gồm metadata, heading, bảng, CTA và liên kết Markdown; khi xuất bản cần đếm lại phần nội dung chính trên HTML.

| Bài | Số chữ file local | Mục tiêu sau sửa | Quyết định |
|---|---:|---:|---|
| Container | 3.673 | 1.800–2.200 | Rút gọn mạnh; giữ bảng thông số, loại cont, cách chọn và FL/OT; cắt phần ISO/cấu tạo lặp. |
| EXW | 3.124 | 1.800–2.300 | Rút gọn 20–35%; giữ định nghĩa, cost/risk, FCA/FOB, ví dụ và câu hỏi thuế. |
| CFR | 5.952 | 1.800–2.400 | Rút gọn mạnh; bỏ diễn giải lặp và ví dụ thuế chưa đủ căn cứ; ưu tiên câu trả lời trực tiếp. |
| CIF | 3.057 | 1.800–2.400 | Rút gọn có chọn lọc; nền nội dung tốt, đưa bảng/công thức/bảo hiểm lên đầu. |
| DDP | 6.074 | 2.000–2.600 | Rút gọn 40–55%; bỏ claim tuyệt đối và gom bảng chi phí/trách nhiệm. |
| FOB | 5.671 | 1.800–2.400 | Rút gọn mạnh; giữ công thức, on board, FOB–CIF–CFR–FCA và ví dụ. |
| Hàng triển lãm | 3.555 | 1.800–2.400 | Rút gọn phần dẫn; giữ checklist, timeline, hồ sơ và nhánh hàng bán nội địa. |

Các trang dịch vụ live cần đếm lại phần `<main>` sau khi loại template trước khi chốt cắt bao nhiêu chữ. Không lấy số chữ gồm menu/footer làm chuẩn.

#### Tiêu chí để quyết định cắt

- Cắt đoạn mở đầu mô tả ngành nếu chưa trả lời keyword trong 100–150 từ đầu.
- Cắt câu quảng cáo lặp như “chuyên nghiệp”, “tối ưu”, “nhanh chóng” nếu không đi kèm bằng chứng hoặc điều kiện áp dụng.
- Gộp các bảng trách nhiệm trùng nhau; mỗi bảng chỉ giữ một mục đích đọc.
- Cắt ví dụ thuế/phí có số liệu nhưng thiếu giả định, nguồn hoặc ngày áp dụng.
- Cắt nội dung mở rộng sang điều kiện Incoterms khác nếu chỉ lặp lại bài riêng; thay bằng đoạn tóm tắt và internal link.
- Không cắt checklist, công thức, điều kiện áp dụng, ngoại lệ pháp lý, FAQ có query hoặc CTA có khả năng chuyển đổi.

#### Format đầu ra sau khi viết lại từng bài

Mỗi bài cần có 4 bản ghi trước khi publish:

1. `Current`: số chữ, heading, intent đang đáp ứng, phần trùng/lặp.
2. `Cut`: đoạn hoặc H2 bị bỏ, lý do và vị trí.
3. `Add/Rewrite`: heading mới, đoạn cần viết lại, bảng/checklist/case cần thêm.
4. `Final`: target word count, title/H1/meta, internal links, CTA và các claim cần duyệt.

Bước này được áp dụng cho toàn bộ 15 URL trong phần 5; report hiện tại đã có hướng cắt/thêm cho từng URL, còn việc thay thế trực tiếp `article.md` chỉ thực hiện sau khi chốt bản rewrite và kiểm tra pháp lý.

## 5. Kế hoạch audit từng URL

| **URL** | **Status** | **Phân loại** | **Hình thức** | **Công việc audit** |
| ------------- | ---------- | ------------- | ------------- | ------------------- |
| [everlog.com.vn](https://everlog.com.vn/) | P1 – Nền tảng chuyển đổi | Trang chủ | Landing page doanh nghiệp | Làm rõ Everlog cung cấp gì trong 5 giây đầu; sắp xếp lại dịch vụ, tuyến, proof points và CTA; sửa counter trống; thống nhất domain; bổ sung schema và tracking conversion. |
| [/dich-vu/van-chuyen-duong-bien](https://everlog.com.vn/dich-vu/van-chuyen-duong-bien) | P1 – Traffic cao, engagement thấp | Dịch vụ | Landing page FCL/LCL | Đưa FCL/LCL, tuyến, quy trình, checklist báo giá và CTA lên đầu; thêm bảng so sánh, FAQ và transit time có điều kiện; sửa lỗi câu chữ và internal link. |
| [/dich-vu/dich-vu-hai-quan](https://everlog.com.vn/dich-vu/dich-vu-hai-quan) | P1 – Ý định chuyển đổi cao | Dịch vụ | Landing page khai báo hải quan | Rút gọn H1; bổ sung nhóm dịch vụ, checklist hồ sơ, quy trình, phạm vi phí và khu vực xử lý; xác minh claim thời gian/chi phí; thêm schema và tracking. |
| [/dich-vu/van-tai-noi-dia](https://everlog.com.vn/dich-vu/van-tai-noi-dia) | P2 – Vị trí tốt, độ phủ thấp | Dịch vụ | Landing page trucking | Bổ sung phương tiện, tải trọng, tuyến, thời gian giao, quy trình lấy/giao hàng và form báo giá; liên kết với đường biển, container và tracking CTA. |
| [/dich-vu/tam-nhap-%E2%80%93-tai-xuat](https://everlog.com.vn/dich-vu/tam-nhap-%E2%80%93-tai-xuat) | P0 – Cơ hội GSC lớn nhất | Dịch vụ | Landing page thủ tục | Đưa định nghĩa, trường hợp áp dụng, hồ sơ, quy trình và CTA lên đầu; phân biệt các hình thức tạm nhập/tái xuất; xác minh mã loại hình, thuế, thời hạn và căn cứ pháp lý. |
| [/trung-bay-%E2%80%93-trien-lam-post1996.html](https://everlog.com.vn/trung-bay-%E2%80%93-trien-lam-post1996.html) | P1 – Đã ở trang đầu | Blog thủ tục | Bài hướng dẫn chuyên ngành | Đưa checklist và CTA lên sớm; thêm timeline, hồ sơ, nhánh hàng bán/biếu tặng/tiêu hao và FAQ; xác minh mã loại hình, thuế, thời hạn và ngày cập nhật. |
| [/hang-le-post1987.html](https://everlog.com.vn/hang-le-post1987.html) | P0 – Impressions cao, query yếu | Blog dịch vụ | Bài dịch vụ LCL | Viết lại theo intent “vận chuyển hàng lẻ LCL”; bổ sung CFS, consolidation, cách tính W/M/CBM, chi phí, quy trình và form báo giá; tránh ngưỡng khối lượng tuyệt đối. |
| [/huong-dan-cach-tinh-trong-luong-trong-van-chuyen-duong-hang-khong-va-duong-bien-lcl-chi-tiet-post2057.html](https://everlog.com.vn/huong-dan-cach-tinh-trong-luong-trong-van-chuyen-duong-hang-khong-va-duong-bien-lcl-chi-tiet-post2057.html) | P1 – Query W/M có vị trí tốt | Blog kỹ thuật | Bài hướng dẫn tính cước | Tách rõ gross weight, volumetric weight, chargeable weight và W/M; đưa câu trả lời lên đầu; thêm bảng phương thức, ví dụ và cảnh báo divisor thay đổi theo carrier. |
| [/thu-tuc-nhap-khau-thuc-an-cho-meo-post2038.html](https://everlog.com.vn/thu-tuc-nhap-khau-thuc-an-cho-meo-post2038.html) | P1 – Gần top 10 | Blog thủ tục | Bài hướng dẫn nhập khẩu chuyên ngành | Làm rõ kiểm dịch/kiểm tra chuyên ngành, HS, hồ sơ và quy trình theo từng giai đoạn; thêm FAQ và CTA; xác minh HS, thuế, cơ quan quản lý và điều kiện sản phẩm. |
| [/cac-loai-container-thong-dung-post2035.html](https://everlog.com.vn/cac-loai-container-thong-dung-post2035.html) | P0 – Crawled, currently not indexed | Blog kỹ thuật | Bài tra cứu thông số | Kiểm tra noindex, canonical, robots, HTML render và internal link; đưa bảng loại cont lên đầu; bổ sung FL/FR, OT, reefer, tank, tare/payload và cảnh báo thông số theo hãng tàu; request indexing. |
| [/gia-exw-la-gi-post2073.html](https://everlog.com.vn/gia-exw-la-gi-post2073.html) | P1 – Đã có tín hiệu tốt | Incoterms 2020 | Bài giải thích điều kiện thương mại | Giữ định nghĩa và so sánh; đưa câu trả lời, bảng chi phí và điểm chuyển rủi ro lên đầu; giải thích “thuế suất EXW” không cố định; rà soát claim pháp lý và ví dụ minh họa. |
| [/gia-cfr-la-gi-post2074.html](https://everlog.com.vn/gia-cfr-la-gi-post2074.html) | P2 – Vị trí thấp | Incoterms 2020 | Bài giải thích điều kiện thương mại | Rewrite gọn theo định nghĩa, công thức, trách nhiệm và ví dụ; bổ sung CFR–FOB–CIF–CPT; sửa ký tự `q` đầu heading; xác minh trị giá hải quan, bảo hiểm và con số. |
| [/gia-cif-la-gi-post2071.html](https://everlog.com.vn/gia-cif-la-gi-post2071.html) | P1 – Có impressions, CTR thấp | Incoterms 2020 | Bài giải thích điều kiện thương mại | Đưa bảng CIF bao gồm/không bao gồm, công thức, bảo hiểm và điểm chuyển rủi ro lên đầu; thêm ví dụ số; phân biệt CIF/CIP và local charges; kiểm soát claim bảo hiểm. |
| [/gia-ddp-la-gi-post2075.html](https://everlog.com.vn/gia-ddp-la-gi-post2075.html) | P2 – Volume thấp, rủi ro pháp lý cao | Incoterms 2020 | Bài giải thích điều kiện thương mại | Rút gọn mạnh; làm rõ chi phí, DDP–DAP–DPU, chủ thể nhập khẩu và checklist hợp đồng; tránh claim tuyệt đối; xác minh Luật Hải quan, thuế và đại lý hải quan. |
| [/gia-fob-la-gi-post2068.html](https://everlog.com.vn/gia-fob-la-gi-post2068.html) | P1 – Cluster quan trọng | Incoterms 2020 | Bài giải thích điều kiện thương mại | Đưa công thức và bảng chi phí lên đầu; thêm ví dụ, phân biệt cảng bốc/dỡ và FOB–FCA; sửa diễn giải “qua mạn tàu”; rà soát trị giá hải quan và internal link. |

Quy ước:

- **Giữ:** nội dung có giá trị và phù hợp intent.
- **Di chuyển:** đưa phần quan trọng lên sớm hơn hoặc chuyển sang H2/H3 phù hợp.
- **Thêm:** nội dung còn thiếu so với query và SERP.
- **Cắt:** đoạn lặp, claim khó chứng minh, câu quảng cáo hoặc phần không phục vụ intent.
- **Xác minh:** claim pháp lý, thời gian, giá, mã loại hình, thuế suất và năng lực phải được duyệt trước khi xuất bản.

### 5.1. Trang chủ — logistics và công ty logistics

**URL:** [https://everlog.com.vn/](https://everlog.com.vn/)  
**GSC:** 3.177 impressions, 271 clicks, CTR 8,53%, vị trí 6,3. Query `logistics` có 174 impressions; `công ty logistics` có 103 impressions.  
**GA4:** 405 sessions, engagement rate 64,94%, 0 conversion trong snapshot.

**Mục tiêu:** Trang chủ phải trả lời trong 5 giây Everlog làm gì, phục vụ tuyến nào, cho loại khách hàng nào và liên hệ bằng cách nào.

**Giữ:** nhóm dịch vụ, logo đối tác, thông tin doanh nghiệp có thể xác minh và CTA.

**Di chuyển:** đưa 4–6 dịch vụ chính, khu vực/tuyến phục vụ, proof points và CTA báo giá ngay sau hero; đưa testimonial xuống sau phần năng lực.

**Thêm:**

- H1 có chủ thể và dịch vụ: `Công ty logistics và vận chuyển quốc tế trọn gói`.
- Một đoạn trả lời ngắn cho `Everlog cung cấp dịch vụ gì?`.
- Bảng dịch vụ: đường biển FCL/LCL, hải quan, vận tải nội địa, tạm nhập tái xuất, hàng triển lãm.
- Form báo giá với các trường tối thiểu: nơi đi, nơi đến, loại hàng, số kiện/trọng lượng/CBM, phương thức, thời gian dự kiến.
- Case/feedback có tên doanh nghiệp hoặc bối cảnh được phép công bố; nếu không có thì dùng quy trình và chứng từ mẫu thay cho lời khen chung.

**Cắt/sửa:** bỏ hoặc nạp số thật cho các counter đang trống; rút ngắn testimonial lặp ý; thống nhất toàn bộ link từ `everlog.vn` về domain chuẩn.

**Technical/measurement:** Organization/LocalBusiness schema; track click hotline, Zalo, email và submit form; kiểm tra title không chỉ nhắm “giải pháp chuyên nghiệp” mà có cụm `công ty logistics`.

**Ưu tiên:** P1 — nền tảng chuyển đổi và entity.

### 5.2. Dịch vụ vận chuyển đường biển

**URL:** [https://everlog.com.vn/dich-vu/van-chuyen-duong-bien](https://everlog.com.vn/dich-vu/van-chuyen-duong-bien)  
**GSC:** 116 impressions, 3 clicks, CTR 2,59%, vị trí 7,2.  
**GA4:** 145 sessions, engagement rate 38,62%, bounce rate 61,38%.

**Mục tiêu:** Chuyển từ trang giới thiệu dài thành landing page cho người cần báo giá FCL/LCL và lịch vận chuyển.

**Giữ:** FCL/LCL, door-to-door, sea-air, hàng quá khổ, tracking và các tuyến đang cung cấp thật.

**Di chuyển:** đưa 3 khối FCL/LCL/door-to-door và form báo giá lên trước phần giải thích tổng quan; đưa “cần cung cấp thông tin gì để báo giá” ngay trước CTA.

**Thêm:**

- Bảng so sánh FCL và LCL: khi dùng, đơn vị tính, thời gian, ưu/nhược điểm.
- Tuyến chính, cảng đi/cảng đến, lịch tàu và transit time theo dạng khoảng hoặc “cập nhật theo booking”; không hứa cố định nếu không có SLA.
- Quy trình 5 bước: nhận yêu cầu, tư vấn phương án, booking, chứng từ/thông quan, giao hàng/tracking.
- Checklist báo giá: tuyến, Incoterms, commodity, HS nếu có, gross weight, CBM, số kiện, loại cont, địa điểm lấy/giao.
- FAQ về local charges, demurrage/detention, bảo hiểm và hàng nguy hiểm.

**Cắt:** các đoạn lặp “nhanh chóng/giá tốt/chuyên nghiệp” không có bằng chứng; phần tuyến không có dịch vụ thực tế.

**Sửa câu chữ quan sát được:**

- `đang và đang có lượng hàng` → viết lại thành `doanh nghiệp có lô hàng cần vận chuyển`.
- `chúng tối` → `chúng tôi`.
- `quá kho` → kiểm tra ngữ cảnh, nhiều khả năng là `quá khổ`.
- `cập nhập` → `cập nhật`.
- `đơn cị` → `đơn vị`.
- `vui long` → `vui lòng`.
- `hằn tuần` → `hằng tuần`.

**Technical:** title/H1 nên có `vận chuyển đường biển quốc tế`, thêm breadcrumb và Service schema nếu template hỗ trợ. CTA cần event GA4.

**Ưu tiên:** P1 — traffic lớn, engagement thấp.

### 5.3. Dịch vụ khai hải quan

**URL:** [https://everlog.com.vn/dich-vu/dich-vu-hai-quan](https://everlog.com.vn/dich-vu/dich-vu-hai-quan)  
**GSC:** 30 impressions, 0 click, vị trí 12,7.  
**GA4:** 73 sessions, engagement rate 46,58%, bounce rate 53,42%.

**Mục tiêu:** Bắt query dịch vụ khai báo hải quan, đại lý hải quan, thông quan và kiểm tra chuyên ngành.

**Giữ:** phạm vi khai báo và CTA liên hệ.

**Di chuyển:** H1 hiện dài và khó đọc: `Dịch vụ khai hải quan trọn gói– Tư vấn dịch vụ hải quan chính xác tối ưu chi phí`. Tách thành H1 ngắn; đưa lợi ích, khu vực làm việc và hồ sơ cần gửi lên đầu.

**Thêm:**

- Các hạng mục: khai tờ khai, tư vấn HS/thuế, kiểm tra chuyên ngành, giấy phép, xử lý luồng vàng/đỏ, thông quan và giao nhận.
- Checklist hồ sơ: invoice, packing list, vận đơn, hợp đồng, C/O, giấy phép/chứng thư theo mặt hàng.
- Quy trình 5 bước giống benchmark Allship nhưng dùng quy trình thực tế của Everlog.
- Bảng “phí dịch vụ bao gồm/không bao gồm”; không công bố mức phí nếu chưa có bảng giá được duyệt.
- Nhóm hàng phục vụ và cảng/chi cục nhận xử lý.

**Cắt:** lời hứa “tối ưu chi phí” nếu không có cách đo; claim thời gian thông quan nếu không có điều kiện áp dụng.

**Sửa câu chữ:** `khái báo hải quan` → `khai báo hải quan`; rà soát `trọn gói–` thành `trọn gói –`.

**Technical:** title nên bắt đầu bằng `Dịch vụ khai báo hải quan`; thêm Service/FAQ phù hợp; event click hotline/Zalo/form.

**Ưu tiên:** P1 — dịch vụ có ý định chuyển đổi cao.

### 5.4. Dịch vụ vận tải nội địa

**URL:** [https://everlog.com.vn/dich-vu/van-tai-noi-dia](https://everlog.com.vn/dich-vu/van-tai-noi-dia)  
**GSC:** 21 impressions, 0 click, vị trí 5,4.  
**GA4:** 40 sessions, engagement rate 42,50%, bounce rate 57,50%.

**Mục tiêu:** Bao phủ vận chuyển nội địa, kéo container, trucking, giao nhận cảng–kho–nhà máy.

**Giữ:** dịch vụ và khu vực thật sự có thể phục vụ.

**Thêm:**

- Bảng phương tiện/tải trọng: đầu kéo cont, xe tải, xe thùng, xe tải cẩu nếu có.
- Tuyến chính: cảng, ICD, khu công nghiệp, tỉnh/thành; không ghi “toàn quốc” nếu chưa có mạng lưới chứng minh.
- Thời gian giao dự kiến theo tuyến; điều kiện ảnh hưởng: cấm tải, thời tiết, lịch cảng.
- Quy trình lấy hàng và giao hàng; giấy tờ cần cung cấp; xử lý hàng quá khổ/quá tải.
- Form báo giá chặng nội địa tách khỏi form đường biển.

**Cắt:** câu mô tả chung không có thông tin tuyến, xe hoặc quy trình.

**Technical:** title/H1 chứa `vận tải nội địa` và `kéo container`; liên kết hai chiều với trang đường biển và bài container; track submit quote.

**Ưu tiên:** P2 — vị trí tốt nhưng độ phủ thấp.

### 5.5. Dịch vụ tạm nhập – tái xuất

**URL:** [https://everlog.com.vn/dich-vu/tam-nhap-%E2%80%93-tai-xuat](https://everlog.com.vn/dich-vu/tam-nhap-%E2%80%93-tai-xuat)  
**GSC:** 627 impressions, 5 clicks, CTR 0,80%, vị trí 6,9. Nhiều query có lỗi gõ nhưng vẫn thể hiện nhu cầu thật.

**Mục tiêu:** Chiếm câu trả lời nhanh cho “tạm nhập tái xuất là gì”, sau đó chuyển đổi người có lô hàng cần làm thủ tục.

**Giữ:** dịch vụ, đối tượng hàng và các bước đang thực hiện thật.

**Di chuyển:** đưa định nghĩa, trường hợp áp dụng, hồ sơ và CTA lên trước phần giới thiệu dài.

**Thêm:**

- Phân biệt tạm nhập tái xuất, tạm xuất tái nhập và nhập khẩu để tiêu thụ nội địa.
- Bảng chiều hàng hóa, mục đích, hồ sơ, thời hạn và bước tái xuất.
- Quy trình từ tư vấn chứng từ đến vận chuyển, mở tờ khai, giao tại sự kiện/kho và tái xuất.
- Câu trả lời riêng cho thuế, thời hạn, gia hạn, hàng bán/chuyển tiêu thụ nội địa và xử lý quá hạn.
- Link đến bài hàng triển lãm như bài hướng dẫn chuyên sâu.

**Xác minh bắt buộc:** mọi mã loại hình, thời hạn miễn/hoãn thuế, lệ phí và căn cứ pháp lý phải kiểm tra theo quy định hiện hành trước khi xuất bản. Không mặc định mã G11/G21/A42 áp dụng cho mọi tình huống.

**Cắt:** các biến thể query lỗi gõ không cần đưa vào heading; chỉ dùng tự nhiên trong nội dung hoặc không dùng.

**Technical:** xem lại dấu gạch trong slug, title và canonical; redirect về slug chuẩn nếu có URL tương đương; FAQ hiển thị thật.

**Ưu tiên:** P0 — cơ hội GSC lớn nhất.

### 5.6. Tạm nhập tái xuất hàng hội chợ, triển lãm

**URL:** [https://everlog.com.vn/trung-bay-%E2%80%93-trien-lam-post1996.html](https://everlog.com.vn/trung-bay-%E2%80%93-trien-lam-post1996.html)  
**GSC:** 387 impressions, 11 clicks, CTR 2,84%, vị trí 8,0.

**Mục tiêu:** Bài hướng dẫn thủ tục chuyên biệt cho doanh nghiệp tham gia triển lãm.

**Giữ:** chủ đề hàng triển lãm và phần hồ sơ/quy trình đang có.

**Di chuyển:** đưa một bảng checklist “trước khi gửi hàng” lên đầu; đưa CTA dịch vụ sau bảng quy trình, không để tới cuối bài mới xuất hiện.

**Thêm:**

- Phân biệt đơn vị tổ chức sự kiện và doanh nghiệp tham gia gian hàng.
- Bảng tạm nhập hàng nước ngoài để triển lãm và tạm xuất hàng Việt Nam đi triển lãm.
- Timeline: trước sự kiện, khi hàng tới cửa khẩu, trong thời gian trưng bày, sau khi kết thúc.
- Checklist serial/model/số lượng/packing list/vận đơn/hợp đồng triển lãm và địa điểm giao.
- Nhánh xử lý hàng bán, hàng biếu tặng, hàng tiêu hao hoặc không tái xuất.
- FAQ về thời hạn, thuế, gia hạn, địa điểm mở tờ khai và vận chuyển tới venue.

**Xác minh bắt buộc:** mã loại hình G11/G21, A42, chính sách miễn thuế và thời hạn phải đối chiếu nguồn hải quan hiện hành; không dùng “mới nhất” trong title nếu chưa cập nhật ngày kiểm tra.

**Technical:** liên kết với trang dịch vụ tạm nhập–tái xuất, hải quan và vận chuyển đường biển/air; thêm `dateModified` đúng ngày sửa thật.

**Ưu tiên:** P1 — đã ở trang đầu, dễ tăng CTR.

### 5.7. Dịch vụ vận chuyển hàng lẻ LCL

**URL:** [https://everlog.com.vn/hang-le-post1987.html](https://everlog.com.vn/hang-le-post1987.html)  
**GSC:** 403 impressions, 4 clicks, CTR 0,99%, vị trí 23,0. Query `vận chuyển hàng lẻ` có 57 impressions, vị trí 44,1; `gom hàng LCL` có 15 impressions, vị trí 19,7.  
**GA4:** 5 sessions, engagement rate 40%.

**Mục tiêu:** Đánh đúng intent dịch vụ LCL, không để người dùng phải tự suy luận “hàng lẻ” là gì.

**Giữ:** dịch vụ LCL, quy trình nhận và giao hàng nếu có.

**Thêm:**

- H1: `Vận chuyển hàng lẻ LCL quốc tế: Quy trình và cách tính cước`.
- Giải thích LCL, CFS, consolidation và khác biệt với FCL.
- Khi nào nên chọn LCL; ngưỡng hàng chỉ là tham khảo, không đặt mốc cứng nếu chưa có policy giá.
- Cách tính theo W/M, CBM hoặc chargeable basis; ví dụ 1–2 lô hàng.
- Các chi phí có thể phát sinh: CFS, handling, chứng từ, local charges, trucking, hải quan, phụ phí mùa cao điểm.
- Quy trình booking–đóng ghép–khai báo–lấy hàng–giao hàng và thời gian dự kiến.
- Form báo giá có số kiện, kích thước từng kiện, gross weight, CBM, commodity và tuyến.

**Cắt:** phần mô tả chung về logistics không giúp chọn LCL; không dùng con số `100–200kg` như quy tắc tuyệt đối nếu không có bảng giá nội bộ.

**Technical:** liên kết đến bài W/M, bài container, dịch vụ đường biển và hải quan; canonical đúng URL; title chứa cả `hàng lẻ` và `LCL`.

**Ưu tiên:** P0 — impressions cao nhưng vị trí/query còn yếu.

### 5.8. Bài tính trọng lượng và cước

**URL:** [https://everlog.com.vn/huong-dan-cach-tinh-trong-luong-trong-van-chuyen-duong-hang-khong-va-duong-bien-lcl-chi-tiet-post2057.html](https://everlog.com.vn/huong-dan-cach-tinh-trong-luong-trong-van-chuyen-duong-hang-khong-va-duong-bien-lcl-chi-tiet-post2057.html)  
**GSC:** 337 impressions, 2 clicks, CTR 0,59%, vị trí 17,6. `w/m là gì` có 41 impressions, vị trí 8,6; `chargeable weight là gì` có 24 impressions, vị trí 68,6.

**Mục tiêu:** Tách rõ ba khái niệm mà người đọc thường trộn lẫn: gross weight, volumetric weight và chargeable weight/W/M.

**Giữ:** công thức và ví dụ đúng sau khi kiểm tra đơn vị.

**Di chuyển:** đưa câu trả lời ngắn cho `W/M là gì?` và `chargeable weight là gì?` ngay sau phần mở đầu; không bắt người đọc đi qua lý thuyết dài.

**Thêm:**

- Bảng phương thức: air, express, sea LCL, road; trọng lượng dùng để tính cước và đơn vị tương ứng.
- Ví dụ tách riêng: 1 kiện đường hàng không; lô LCL tính theo W/M; lô nhiều kiện lấy tổng.
- Cảnh báo divisor 5000/6000 hoặc quy tắc W/M có thể khác theo carrier, forwarder và bảng giá; không trình bày một divisor là chuẩn cho mọi trường hợp.
- Mẫu dữ liệu gửi để báo giá: kích thước dài–rộng–cao từng kiện, số kiện, gross weight, nơi đi/đến, commodity.

**Cắt:** đoạn mở đầu rộng về logistics; các công thức không ghi đơn vị hoặc không nêu điều kiện áp dụng.

**Technical:** sửa title/meta theo query thực tế; thêm bảng HTML dễ đọc trên mobile; liên kết sang LCL và đường biển; có thể thêm calculator sau khi kiểm tra logic.

**Ưu tiên:** P1 — query W/M đã có vị trí tốt, cần mở rộng sang chargeable weight.

### 5.9. Thủ tục nhập khẩu thức ăn chó mèo

**URL:** `https://everlog.com.vn/thu-tuc-nhap-khau-thuc-an-cho-meo-post2038.html`  
**GSC:** 466 impressions, 4 clicks, CTR 0,86%, vị trí 12,3. Query chính có 34 impressions, vị trí 26,6.  
**GA4:** 4 sessions, engagement rate 100% trong snapshot; mẫu nhỏ, chưa kết luận chất lượng.

**Mục tiêu:** Trả lời chính xác quy trình trước thông quan và điều kiện đưa sản phẩm ra thị trường.

**Giữ:** chủ đề HS, hồ sơ, thuế và dịch vụ hải quan.

**Di chuyển:** đưa cảnh báo “kiểm dịch/kiểm tra chuyên ngành và hồ sơ sản phẩm” lên phần mở đầu; sau đó mới đi vào HS và thuế.

**Thêm:**

- Phân biệt thức ăn cho chó/mèo với thực phẩm bổ sung, thuốc thú y hoặc sản phẩm có thành phần đặc biệt.
- Bảng hồ sơ theo giai đoạn: trước khi nhập, tại cửa khẩu, sau thông quan/đăng ký lưu hành nếu áp dụng.
- Quy trình rõ: kiểm tra điều kiện → xác định HS → hồ sơ chuyên ngành → vận chuyển → kiểm tra/lấy mẫu → khai hải quan → thông quan.
- FAQ về kiểm dịch, chứng nhận chất lượng, nhãn hàng hóa, hạn dùng, mẫu thử và lưu kho.
- CTA có yêu cầu gửi trước nhãn, thành phần, xuất xứ, invoice/packing list để tư vấn.

**Xác minh bắt buộc:** HS, thuế suất, cơ quan quản lý và yêu cầu đăng ký phải kiểm tra theo sản phẩm cụ thể và quy định tại thời điểm xuất bản; không dùng “mới nhất” nếu không có ngày rà soát.

**Cắt:** câu mở đầu chung chung về xu hướng thị trường; claim “thông quan nhanh” không có điều kiện.

**Technical:** title bắt đầu bằng `Thủ tục nhập khẩu thức ăn chó mèo`; liên kết tới khai hải quan, kiểm dịch, kiểm tra chuyên ngành và dịch vụ vận tải.

**Ưu tiên:** P1 — impressions cao, vị trí ngay ngoài top 10.

### 5.10. Các loại container thông dụng

**URL:** [https://everlog.com.vn/cac-loai-container-thong-dung-post2035.html](https://everlog.com.vn/cac-loai-container-thong-dung-post2035.html)  
**GSC:** 56 impressions, 0 click, vị trí 16,3; `cont fl` có 39 impressions, vị trí 5,6.  
**Indexing:** Crawled - currently not indexed; canonical, robots và fetch đều pass.

**Mục tiêu:** Đưa bài vào index và bao phủ nhu cầu tra cứu loại cont, kích thước, tải trọng, FL/OT/tank/reefer.

**Giữ:** phần ISO, bảng thông số, phân loại và cách đọc ký mã hiệu nếu số liệu được kiểm tra.

**Di chuyển:** đưa bảng loại cont và kích thước lên ngay sau định nghĩa; phần tiêu chuẩn ISO nên đứng sau câu trả lời thực dụng.

**Thêm:**

- Bảng 20DC, 40DC, 40HC, 45HC và các loại chuyên dụng; ghi rõ kích thước/tải trọng chỉ mang tính tham khảo theo hãng tàu/series.
- H3 riêng cho `flat rack (FR/FL)`, open top, reefer, tank, dry bulk và cont hàng nguy hiểm nếu có dịch vụ.
- Cách chọn theo loại hàng, CBM, chiều cao, khối lượng, tải trọng tuyến đường.
- Giải thích tare, payload, max gross, CSC/ISO và sự khác nhau giữa cont tiêu chuẩn và cont thực tế.
- Liên kết sang bài hàng lẻ, đường biển và vận tải nội địa.

**Cắt:** không cần mở rộng thành “12 loại” nếu Everlog chỉ muốn xử lý 7 loại; khi đó title phải ghi `7 loại container phổ biến`. Cắt phần cấu tạo quá chi tiết nếu không hỗ trợ quyết định chọn cont.

**Technical/index:** kiểm tra source HTML có đủ body hay chỉ render bằng JS; kiểm tra noindex và canonical; thêm internal link từ 3 bài đang có traffic; request indexing sau khi publish; kiểm tra ảnh/bảng trên mobile.

**Ưu tiên:** P0 technical + P2 content.

### 5.11. Giá EXW

**URL:** [https://everlog.com.vn/gia-exw-la-gi-post2073.html](https://everlog.com.vn/gia-exw-la-gi-post2073.html)  
**GSC:** 213 impressions, 8 clicks, CTR 3,76%, vị trí 8,2; query `phí exw thuế suất bao nhiêu` có 10 impressions, vị trí 8,1.

**Mục tiêu:** Giữ vị trí hiện tại, tăng CTR và giải quyết query thuế/phí thực dụng.

**Giữ:** định nghĩa EXW, điểm giao hàng, trách nhiệm, so sánh FCA/FOB và ví dụ.

**Di chuyển:** đưa câu trả lời 2–3 dòng cho `Giá EXW là gì?` và bảng “bên nào chịu chi phí từ đâu đến đâu” lên trước phần pháp lý.

**Thêm:**

- Hộp trả lời riêng: EXW không phải một mức thuế suất; tổng chi phí/thuế phụ thuộc hàng hóa, HS, nước nhập khẩu và các chặng phát sinh.
- Ví dụ bóc từ EXW đến FOB/CIF/DAP theo một lô giả định, ghi rõ giả định.
- Phần thực tế Việt Nam: ai thực hiện khai xuất khẩu, bốc hàng, lấy hàng tại xưởng; dùng ngôn ngữ “có thể cần phối hợp” thay vì tuyệt đối hóa.
- So sánh EXW–FCA–FOB theo phương thức vận tải và điểm chuyển rủi ro.

**Cắt/sửa:** các câu “người bán chưa làm thủ tục...” cần phân biệt nghĩa vụ theo Incoterms với yêu cầu pháp lý tại từng quốc gia; không đồng nhất giá EXW với trị giá tính thuế.

**Link:** đổi link `everlog.vn` và các slug cũ trong bản nháp về URL chuẩn sau khi xác nhận redirect.

**Xác minh:** căn cứ Thông tư 05/2018/TT-BCT, Incoterms 2020 và quy định xuất khẩu hiện hành; mọi ví dụ thuế phải ghi rõ chỉ là minh họa.

**Ưu tiên:** P1 — bài đã có tín hiệu tốt.

### 5.12. Giá CFR

**URL:** [https://everlog.com.vn/gia-cfr-la-gi-post2074.html](https://everlog.com.vn/gia-cfr-la-gi-post2074.html)  
**GSC:** 6 impressions, 0 click, vị trí 64,7.

**Mục tiêu:** Xây lại khả năng được hiểu và được index/rank cho query CFR cơ bản; không giữ cấu trúc quá nặng nếu chưa có traffic.

**Giữ:** hai điểm quan trọng: người bán trả cước tới cảng đích nhưng rủi ro chuyển khi hàng đã on board; CFR không bao gồm bảo hiểm.

**Di chuyển:** câu trả lời định nghĩa, công thức và bảng trách nhiệm lên đầu; phần pháp lý xuống sau ví dụ.

**Thêm:**

- Hộp trả lời `Giá CFR bao gồm gì và không bao gồm gì?`.
- Ví dụ `FOB + cước biển = CFR`, sau đó tách local charges, bảo hiểm và thuế nhập khẩu.
- Bảng CFR–FOB–CIF–CPT, đặc biệt phương thức vận tải và điểm chuyển rủi ro.
- Giải thích ranh giới giữa giá CFR trong hợp đồng và trị giá tính thuế; không cộng bảo hiểm giả định vào mọi trường hợp.
- Cảnh báo dùng FCA/CPT cho hàng container/multimodal khi phù hợp; viết theo hướng khuyến nghị, không biến thành quy tắc tuyệt đối.

**Cắt:** đoạn quảng cáo “chuyên gia thực chiến” lặp lại; ví dụ thuế có C/O/thuế suất nếu chưa kiểm chứng đầy đủ.

**Lỗi local rõ ràng:** file bản nháp bắt đầu bằng `q# Giá CFR...` — bỏ ký tự `q`, giữ lại heading Markdown hợp lệ.

**Xác minh:** Incoterms 2020, trị giá hải quan, bảo hiểm và quy tắc áp dụng cho container; rà soát toàn bộ con số trước publish.

**Ưu tiên:** P2 — cần rewrite sau EXW/CIF/FOB.

### 5.13. Giá CIF

**URL:** [https://everlog.com.vn/gia-cif-la-gi-post2071.html](https://everlog.com.vn/gia-cif-la-gi-post2071.html)  
**GSC:** 161 impressions, 1 click, CTR 0,62%, vị trí 18,0.  
**GA4:** 2 sessions; mẫu nhỏ.

**Mục tiêu:** Đưa bài từ vị trí 18 vào top 10 bằng snippet và cấu trúc trả lời trực tiếp.

**Giữ:** định nghĩa, công thức, bảo hiểm, bảng trách nhiệm, CIF–FOB–CIP, FAQ và liên kết cluster.

**Di chuyển:** đưa bảng `CIF bao gồm/không bao gồm`, điểm chuyển rủi ro và công thức lên 25% đầu bài.

**Thêm:**

- Hộp trả lời `Giá CIF = giá hàng + bảo hiểm + cước biển`; ghi rõ phạm vi đến cảng đích.
- Một ví dụ số ngắn, không trộn trị giá hợp đồng với trị giá tính thuế.
- Giải thích mức bảo hiểm theo điều khoản hợp đồng/chứng thư; claim “110%” phải ghi đúng bối cảnh và nguồn, không trình bày như mọi hợp đồng đều giống nhau.
- So sánh CIF và CIP theo phương thức vận tải, bảo hiểm và điểm giao.
- Bảng local charges đầu nhập do bên nào chịu theo hợp đồng thực tế.

**Cắt:** phần mở đầu và CTA có tính tự khen; gộp các đoạn lặp về “chuyên gia logistics”.

**Technical:** title/meta giữ keyword đầu câu; kiểm tra H1 chỉ có một; liên kết tới EXW/CFR/DDP/FOB bằng domain chuẩn; thêm FAQ hiển thị và schema nếu đủ điều kiện.

**Ưu tiên:** P1 — impressions đủ lớn, nội dung nền đã tốt.

### 5.14. Giá DDP

**URL:** [https://everlog.com.vn/gia-ddp-la-gi-post2075.html](https://everlog.com.vn/gia-ddp-la-gi-post2075.html)  
**GSC:** 5 impressions, 0 click, vị trí 87,6.  
**GA4:** 2 sessions; mẫu nhỏ.

**Mục tiêu:** Làm bài dễ hiểu và an toàn pháp lý hơn; không dùng độ dài thay cho độ tin cậy.

**Giữ:** định nghĩa, điểm giao, so sánh DDP/DAP/DPU/EXW/FOB và cảnh báo về nhập khẩu tại Việt Nam.

**Di chuyển:** đưa câu trả lời ngắn cho `DDP là gì?`, bảng ai chịu chi phí và ví dụ địa điểm giao lên đầu.

**Thêm:**

- Bảng 7 nhóm chi phí nhưng chỉ giữ các nhóm thật sự cần: hàng, xuất khẩu, vận tải quốc tế, nhập khẩu, thuế/phí, vận tải nội địa, giao cuối.
- DDP–DAP–DPU: ai làm thủ tục nhập khẩu, ai nộp thuế, ai dỡ hàng và điểm chuyển rủi ro.
- Checklist hợp đồng: địa chỉ giao cụ thể, loại thuế/phí đã bao gồm, chứng từ, người đứng tên nhập khẩu, xử lý local charges.
- Box “khi nào không nên dùng DDP” cho người bán không thể thực hiện thủ tục nhập khẩu hoặc không kiểm soát thuế/phí tại nước đến.

**Cắt/sửa:** tránh khẳng định tuyệt đối kiểu “người bán nước ngoài không thể tự đứng tên...” nếu chưa gắn căn cứ và ngoại lệ; viết thành “cần xác định chủ thể nhập khẩu hợp pháp tại Việt Nam và phương án đại diện phù hợp”. Không gọi DDP là luôn luôn “nhàn hạ” hoặc “all-in” nếu hợp đồng loại trừ khoản nào.

**Xác minh:** Luật Hải quan, quy định thuế và cơ chế đại lý hải quan tại thời điểm xuất bản; đây là bài có rủi ro pháp lý cao nhất trong nhóm.

**Ưu tiên:** P2 — volume hiện thấp, cần chỉnh accuracy trước khi mở rộng.

### 5.15. Giá FOB

**URL:** [https://everlog.com.vn/gia-fob-la-gi-post2068.html](https://everlog.com.vn/gia-fob-la-gi-post2068.html)  
**GSC:** 71 impressions, 1 click, CTR 1,41%, vị trí 16,0.  
**GA4:** 3 sessions; mẫu nhỏ.

**Mục tiêu:** Cải thiện query “FOB là gì/bao gồm gì” và hỗ trợ internal-link cluster với CIF/CFR/EXW.

**Giữ:** định nghĩa, công thức, phân chia trách nhiệm, so sánh FOB/CIF/CFR, trường hợp dùng FCA.

**Di chuyển:** đưa công thức và bảng FOB bao gồm/không bao gồm lên trước phần giải thích pháp lý.

**Thêm:**

- Ví dụ: giá hàng + vận chuyển nội địa + phí xuất khẩu + handling/xếp hàng = giá FOB theo giả định.
- Phân biệt cảng bốc hàng và cảng dỡ hàng.
- Cảnh báo FOB chỉ cho đường biển/thủy nội địa; hàng container giao cho carrier tại bãi có thể cần cân nhắc FCA.
- Tách phí do hợp đồng/booking quyết định khỏi chi phí mặc định.

**Cắt/sửa:** cụm `đã giao qua mạn tàu` trong phần diễn giải trị giá FOB cần rà soát, vì cách diễn đạt này dễ gây nhầm với quy tắc cũ; dùng “hàng đã được xếp lên tàu/on board” khi nói về Incoterms 2020. Không đồng nhất giá FOB thương mại với mọi cách tính trị giá hải quan.

**Link:** thay các link `everlog.vn`, `/dich-vu/hai-quan/`, `/dich-vu/van-chuyen-quoc-te/` sau khi xác nhận URL chuẩn.

**Ưu tiên:** P1 — cluster quan trọng, dễ hỗ trợ CIF/EXW.

## 6. Mapping nội dung để tránh cannibalization

| Intent | URL chính | URL hỗ trợ | Quy tắc |
|---|---|---|---|
| Vận chuyển đường biển | Trang dịch vụ đường biển | LCL, container, W/M, vận tải nội địa | Trang dịch vụ nhận query thương mại; bài blog giải thích khái niệm và trỏ về dịch vụ. |
| Vận chuyển hàng lẻ | Trang hàng lẻ/LCL | Bài W/M, container, đường biển | Không để bài W/M cạnh tranh với trang LCL cho query dịch vụ. |
| Tạm nhập tái xuất | Trang dịch vụ tạm nhập–tái xuất | Bài hàng triển lãm | Trang dịch vụ bán giải pháp; bài triển lãm xử lý use case cụ thể. |
| Hải quan | Trang khai hải quan | Bài thức ăn chó mèo, Incoterms | Bài chuyên ngành chỉ link về dịch vụ, không copy nguyên quy trình dịch vụ. |
| Container | Bài container | LCL, đường biển, trucking | Tập trung loại/size/FL/OT; không biến thành bài báo giá vận chuyển. |
| EXW/CFR/CIF/DDP/FOB | Mỗi bài một điều kiện | Các bài Incoterms còn lại | Mỗi bài có một intent chính; bảng so sánh chỉ tóm tắt và link sang bài chuyên biệt. |

## 7. Thứ tự triển khai đề xuất

### Sprint 0 — Technical và đo lường

1. Chốt domain chuẩn, redirect, canonical và sitemap.
2. Sửa link nội bộ sai domain/sai slug.
3. Điều tra parameter injection trong `/tin-tuc?page=`.
4. Sửa template counter trống, kiểm tra mobile/rendering.
5. Cấu hình GA4 conversion cho CTA.

### Sprint 1 — Trang có cơ hội rõ nhất

1. Tạm nhập–tái xuất.
2. Hàng lẻ/LCL.
3. Dịch vụ đường biển.
4. Bài triển lãm.
5. Thức ăn chó mèo.
6. Bài W/M/chargeable weight.

### Sprint 2 — Củng cố cluster và chuyển đổi

1. Trang hải quan.
2. Trang chủ.
3. Trang vận tải nội địa.
4. Container: sửa index trước, sau đó mở rộng nội dung.

### Sprint 3 — Incoterms

1. EXW, CIF, FOB.
2. CFR.
3. DDP sau khi hoàn tất review pháp lý.

## 8. Tiêu chí nghiệm thu sau khi sửa

- Mỗi URL chỉ có một H1, title/meta khớp intent và không lặp máy móc.
- Phần trả lời chính xuất hiện trong 100–150 từ đầu hoặc trong bảng/box đầu bài.
- Mỗi bài dịch vụ có CTA nhìn thấy trên mobile và event GA4 tương ứng.
- Mỗi bài blog có ít nhất 3 internal link ngữ cảnh tới trang dịch vụ hoặc bài cluster liên quan.
- Không còn link sang domain/slug cũ sau crawl.
- Không có lỗi chính tả trong title, H1, CTA, bảng và anchor text.
- Claim pháp lý, thuế, mã loại hình, thời gian, giá, tỷ lệ và năng lực đều có nguồn hoặc được đánh dấu cần duyệt.
- Bài container được index lại; kiểm tra bằng GSC URL Inspection sau publish.
- Sau 28–42 ngày, so sánh impressions, CTR, vị trí, query mới, engagement rate và số conversion theo từng URL.

## 9. Kết luận điều hành

Everlog không cần viết lại đồng loạt. Ưu tiên tạo tác động nhanh là sửa technical domain/index, sau đó rewrite các trang đã có impressions nhưng CTR hoặc vị trí yếu: tạm nhập–tái xuất, LCL, đường biển, hàng triển lãm, thức ăn chó mèo, W/M và EXW/CIF/FOB. Các bài Incoterms hiện có nền nội dung tốt nhưng cần rút gọn phần mở đầu, đưa câu trả lời lên đầu, làm rõ giả định tính phí và kiểm soát claim pháp lý.

## 10. Nguồn tham khảo đối thủ và pháp lý

- [Prefer Logistics — Vận chuyển đường biển](https://prefer.com.vn/van-chuyen-duong-bien/)
- [Allship — Dịch vụ Hải quan](https://logistic.allship.vn/dich-vu-hai-quan/)
- [3W Logistics — Thủ tục nhập khẩu thức ăn chó mèo](https://3w-logistics.com/vi/quy-trinh-thu-tuc-nhap-khau-thuc-an-cho-meo/)
- [Gateway Express — Cách tính cước vận chuyển quốc tế](https://gatewayexpress.vn/bai-viet/cach-tinh-cuoc-van-chuyen-quoc-te/)
- [KVN Logistics — Các loại container phổ biến](https://kvnlogistics.vn/vi/cac-loai-container-pho-bien-trong-van-tai-bien/)
- [Thư viện Pháp luật — Giá EXW và trị giá FOB](https://thuvienphapluat.vn/phap-luat/gia-exw-la-gi-cach-tinh-gia-exw-cach-tinh-tri-gia-fob-tu-gia-exw-trong-xuat-nhap-khau-nhu-the-nao-45624-232412.html)
- [FedEx — EXW](https://www.fedex.com/vi-vn/shipping/glossary/what-is-ex-exw.html)
- [FedEx — CFR](https://www.fedex.com/vi-vn/shipping/glossary/what-is-cfr.html)
- [TSL — CIF là gì](https://tsl.com.vn/cif-la-gi/)
- [TCL Freight — FOB là gì](https://tclfreight.com.vn/fob-la-gi/)
- [Cổng dịch vụ công Bộ Tài chính](https://dichvucong.mof.gov.vn/web/guest/dich-vu-cong-truc-tuyen)

**Ghi chú:** Các nguồn trên dùng để benchmark cấu trúc và kiểm tra hướng nghiên cứu. Trước khi publish, bộ phận chuyên môn cần duyệt lại mọi thông tin pháp lý, thuế, mã loại hình, thời hạn, phí và cam kết vận hành.
