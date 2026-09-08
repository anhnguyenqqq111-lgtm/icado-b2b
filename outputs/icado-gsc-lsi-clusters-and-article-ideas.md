# ICADO — Gom query GSC thành LSI và ý tưởng bài

- Nguồn: query exact từ GSC server `gscNew`, property `https://icado.vn/`.
- Kỳ dữ liệu: `2025-09-08`–`2026-09-07`.
- Phạm vi đầu vào: 4.386 query liên quan, có impression và average position `> 10`.
- Mỗi query được gán một cụm primary intent duy nhất để làm cơ sở quy hoạch URL. Một LSI có thể được nhắc lại tự nhiên trong các bài liên quan.

## Bản đồ cụm LSI

| Cụm LSI | Query | Impressions | Keyword trụ cột | Ý tưởng bài chính | Vai trò | Ưu tiên |
|---|---:|---:|---|---|---|---|
| B2B — sỉ, đại lý & kinh doanh | 64 | 4.742 | sỉ đồ thể thao | Nguồn hàng đồ thể thao sỉ: tiêu chí chọn nhà cung cấp và chính sách đại lý | B2B hub riêng | P0 |
| Local, shop & transactional | 425 | 20.745 | shop đồ thể thao | Mua đồ thể thao chính hãng ở đâu? Tiêu chí chọn shop theo môn tập | Landing/local support | P1 |
| Chăm sóc & bảo quản | 8 | 64 | cách giặt đồ thể thao | Cách giặt và bảo quản đồ thể thao để không mùi, không bai dão, bền form | Evergreen how-to | P1 |
| Size, fit & dáng người | 42 | 1.045 | size đồ thể thao | Cách đo và chọn size đồ thể thao nam nữ: bảng đo eo, hông, ngực và chiều dài | Hub hỗ trợ chuyển đổi | P0 |
| Chất liệu & công nghệ vải | 177 | 3.085 | chất liệu đồ thể thao | Polyester, spandex hay cotton: chọn chất liệu đồ thể thao theo môn tập | Knowledge pillar | P1 |
| Pickleball — giày, vợt, bóng & phụ kiện | 278 | 28.650 | thiết bị pickleball | Checklist thiết bị pickleball cho người mới: vợt, bóng, giày và phụ kiện | Cụm comparison / commercial | P0 |
| Pickleball — trang phục | 388 | 23.049 | đồ tập pickleball | Mặc gì chơi pickleball? Cách chọn trang phục theo giới tính, cường độ và thời tiết | Pillar + guide chọn đồ | P0 |
| Gym — đồ tập, legging & bra | 339 | 53.681 | đồ tập gym | Cách chọn đồ tập gym nam nữ: áo, quần, bra, legging và độ hỗ trợ | Pillar commercial investigation | P0 |
| Yoga & Pilates — trang phục | 122 | 19.735 | đồ tập yoga | Tập yoga nên mặc gì? Cách chọn áo, quần và chất liệu theo động tác | Pillar + guide chọn đồ | P0 |
| Tennis & chạy bộ — trang phục | 141 | 14.079 | đồ tennis và chạy bộ | Trang phục tennis và chạy bộ khác nhau thế nào? Cách chọn theo chuyển động | Comparison + guide | P1 |
| Outfit & athleisure | 39 | 1.765 | phối đồ thể thao | Athleisure là gì? 7 cách phối đồ thể thao từ phòng tập đến đi chơi | Inspiration cluster | P1 |
| Kiến thức gym, yoga & fitness | 1.144 | 23.334 | kiến thức gym yoga cho người mới | Gym, yoga và fitness cho người mới: chọn bộ môn, lịch tập và trang phục phù hợp | TOFU knowledge hub | P2 |
| Sportswear tổng quát — cần review | 1.219 | 58.843 | đồ thể thao | Rà soát thủ công trước khi tạo nội dung; không tự động tạo bài cho query không đủ topical fit | Review | P3 |

## LSI exact và idea theo cụm

### B2B — sỉ, đại lý & kinh doanh
- **Keyword trụ cột:** `sỉ đồ thể thao`
- **LSI semantic mở rộng:** sỉ quần áo thể thao, sỉ đồ tập gym, nguồn hàng pickleball, đại lý đồ thể thao, nhập sỉ đồ gym
- **Bài đề xuất:** **Nguồn hàng đồ thể thao sỉ: tiêu chí chọn nhà cung cấp và chính sách đại lý**
- **Dạng triển khai:** B2B hub riêng; ưu tiên P0.
- **Query exact tiêu biểu từ GSC:**
  - `bán đồ gym` — 745 impressions; vị trí TB 21.4
  - `shop bán đồ thể thao` — 420 impressions; vị trí TB 44.3
  - `mở shop bán đồ thể thao` — 281 impressions; vị trí TB 22.2
  - `sỉ quần áo thể thao` — 270 impressions; vị trí TB 21.1
  - `bán đồ thể thao` — 266 impressions; vị trí TB 45.4
  - `shop bán đồ thể thao nữ` — 258 impressions; vị trí TB 18.1
  - `bán sỉ đồ thể thao` — 238 impressions; vị trí TB 28.9
  - `bán đồ thể thao nữ` — 235 impressions; vị trí TB 23.3
  - `sỉ đồ bộ thể thao` — 175 impressions; vị trí TB 60.6
  - `shop bán đồ thể thao giá rẻ` — 167 impressions; vị trí TB 48.3
  - `kinh nghiệm mở shop quần áo nam​` — 163 impressions; vị trí TB 71.5
  - `kinh nghiệm mở shop quần áo nữ​` — 158 impressions; vị trí TB 65.2
  - `shop bán đồ tập gym gần đây` — 104 impressions; vị trí TB 12.0
  - `kinh nghiệm mở shop quần áo online​` — 95 impressions; vị trí TB 90.0
  - `chuyên bán đồ thể thao` — 91 impressions; vị trí TB 64.1
  - `sỉ đồ thể thao` — 90 impressions; vị trí TB 36.2
  - `trang web bán đồ thể thao` — 81 impressions; vị trí TB 52.0
  - `bán đồ thể thao online` — 73 impressions; vị trí TB 63.0
  - `shop bán đồ pickleball` — 64 impressions; vị trí TB 10.3
  - `bán đồ thể thao nam` — 63 impressions; vị trí TB 71.0
  - `shop bán đồ thể thao đà nẵng` — 61 impressions; vị trí TB 18.3
  - `bán đồ thể thao đà nẵng` — 60 impressions; vị trí TB 23.3
  - `mở shop quần áo cần những gì` — 51 impressions; vị trí TB 10.2
  - `shop bán đồ pickleball ở tphcm` — 48 impressions; vị trí TB 11.1
  - `nhập hàng pickleball` — 43 impressions; vị trí TB 54.7
  - `shop bán đồ tập gym` — 34 impressions; vị trí TB 12.1
  - `sỉ túi xách thể thao` — 34 impressions; vị trí TB 94.1
  - `quản lý cửa hàng bán đồ thể thao` — 32 impressions; vị trí TB 32.3
  - `cửa hàng bán đồ pickleball` — 26 impressions; vị trí TB 21.4
  - `bán đồ pickleball` — 25 impressions; vị trí TB 30.6

### Local, shop & transactional
- **Keyword trụ cột:** `shop đồ thể thao`
- **LSI semantic mở rộng:** shop đồ thể thao, shop đồ gym, shop đồ yoga, shop pickleball, đồ thể thao chính hãng, mua ở đâu
- **Bài đề xuất:** **Mua đồ thể thao chính hãng ở đâu? Tiêu chí chọn shop theo môn tập**
- **Dạng triển khai:** Landing/local support; ưu tiên P1.
- **Query exact tiêu biểu từ GSC:**
  - `mua vợt pickleball ở đâu` — 1.014 impressions; vị trí TB 10.2
  - `nên mua bóng pickleball loại nào` — 697 impressions; vị trí TB 15.4
  - `shop vợt pickleball` — 548 impressions; vị trí TB 14.9
  - `nên mua vợt pickleball hãng nào` — 517 impressions; vị trí TB 15.8
  - `mua vợt pickleball` — 469 impressions; vị trí TB 37.3
  - `người mới chơi pickleball cần mua gì` — 454 impressions; vị trí TB 42.7
  - `shop pickleball` — 403 impressions; vị trí TB 12.8
  - `địa chỉ bán vợt pickleball` — 396 impressions; vị trí TB 19.0
  - `mua vợt pickleball ở đâu uy tín` — 382 impressions; vị trí TB 11.3
  - `mua vợt pickleball chính hãng ở đâu` — 376 impressions; vị trí TB 13.2
  - `shop đồ tập gym nam` — 368 impressions; vị trí TB 13.4
  - `nên mua vợt pickleball nào` — 339 impressions; vị trí TB 12.6
  - `chọn mua bóng pickleball` — 332 impressions; vị trí TB 23.1
  - `quần thể thao nam chính hãng` — 328 impressions; vị trí TB 13.4
  - `quần short thể thao nam chính hãng` — 315 impressions; vị trí TB 37.5
  - `shop đồ tập gym nữ` — 301 impressions; vị trí TB 10.6
  - `mua vợt pickleball uy tín` — 289 impressions; vị trí TB 12.2
  - `địa chỉ mua vợt pickleball uy tín` — 271 impressions; vị trí TB 15.5
  - `nên mua vợt pickleball ở đâu` — 261 impressions; vị trí TB 14.6
  - `nơi mua vợt pickleball uy tín` — 257 impressions; vị trí TB 17.0
  - `pickleball shop` — 252 impressions; vị trí TB 10.3
  - `shop bán vợt pickleball` — 251 impressions; vị trí TB 10.6
  - `chỗ mua vợt pickleball` — 250 impressions; vị trí TB 11.5
  - `vợt pickleball chính hãng` — 250 impressions; vị trí TB 28.5
  - `mua vợt pickleball uy tín ở đâu` — 235 impressions; vị trí TB 12.0
  - `mua vợt pickleball ở đâu chính hãng` — 231 impressions; vị trí TB 15.5
  - `nên mua vợt pickleball loại nào` — 229 impressions; vị trí TB 17.4
  - `shop mua vợt pickleball` — 229 impressions; vị trí TB 12.7
  - `bóng pickleball chính hãng` — 224 impressions; vị trí TB 14.8
  - `địa điểm mua vợt pickleball` — 223 impressions; vị trí TB 19.0

### Chăm sóc & bảo quản
- **Keyword trụ cột:** `cách giặt đồ thể thao`
- **LSI semantic mở rộng:** giặt đồ thể thao, giặt legging, giặt polyester, khử mùi đồ tập, bảo quản đồ yoga, nước giặt đồ thể thao
- **Bài đề xuất:** **Cách giặt và bảo quản đồ thể thao để không mùi, không bai dão, bền form**
- **Dạng triển khai:** Evergreen how-to; ưu tiên P1.
- **Query exact tiêu biểu từ GSC:**
  - `thảm tập yoga có giặt được không` — 31 impressions; vị trí TB 50.7
  - `cách giặt thảm yoga` — 12 impressions; vị trí TB 65.8
  - `cách giặt quần short thể thao nữ` — 11 impressions; vị trí TB 13.5
  - `cách giặt quần legging` — 5 impressions; vị trí TB 18.8
  - `cách giặt vải polyester` — 2 impressions; vị trí TB 76.0
  - `giặt vải polyester` — 1 impressions; vị trí TB 86.0
  - `nước giặt quần áo` — 1 impressions; vị trí TB 87.0
  - `quần áo có mùi sau khi giặt` — 1 impressions; vị trí TB 46.0

### Size, fit & dáng người
- **Keyword trụ cột:** `size đồ thể thao`
- **LSI semantic mở rộng:** bảng size đồ thể thao, size quần legging, size áo bra, size đồ pickleball, Asian Fit, form đồ thể thao
- **Bài đề xuất:** **Cách đo và chọn size đồ thể thao nam nữ: bảng đo eo, hông, ngực và chiều dài**
- **Dạng triển khai:** Hub hỗ trợ chuyển đổi; ưu tiên P0.
- **Query exact tiêu biểu từ GSC:**
  - `cách chọn giày pickleball theo form chân` — 459 impressions; vị trí TB 47.8
  - `size đồ thể thao nữ` — 115 impressions; vị trí TB 28.7
  - `size áo thể thao nữ` — 74 impressions; vị trí TB 39.7
  - `chọn size cán vợt pickleball` — 47 impressions; vị trí TB 50.4
  - `bảng size áo thể thao nữ` — 46 impressions; vị trí TB 31.8
  - `size đồ thể thao nam` — 44 impressions; vị trí TB 32.8
  - `bảng size quần áo thể thao nữ` — 43 impressions; vị trí TB 35.0
  - `bảng size đồ thể thao nam` — 38 impressions; vị trí TB 52.4
  - `bảng size quần áo thể thao nam` — 30 impressions; vị trí TB 52.9
  - `quần legging chạy bộ nữ cạp cao` — 21 impressions; vị trí TB 13.1
  - `bài tập yoga cho vòng eo thon gọn` — 16 impressions; vị trí TB 42.3
  - `quần legging nữ cạp cao` — 12 impressions; vị trí TB 26.2
  - `bảng size quần legging` — 9 impressions; vị trí TB 55.0
  - `size quần legging nữ` — 9 impressions; vị trí TB 63.8
  - `quan the thao nam cao cap` — 8 impressions; vị trí TB 30.6
  - `size áo thể dục` — 8 impressions; vị trí TB 64.0
  - `size áo thể thao nam` — 8 impressions; vị trí TB 37.0
  - `chọn size áo thể thao nam` — 6 impressions; vị trí TB 29.0
  - `quần áo tập gym nữ size lớn` — 6 impressions; vị trí TB 26.3
  - `10 bài tập yoga giúp vòng eo săn chắc` — 5 impressions; vị trí TB 36.4
  - `bảng size áo thể thao nam` — 5 impressions; vị trí TB 49.4
  - `size đồ thể thao` — 4 impressions; vị trí TB 71.8
  - `áo bra tập gym big size` — 4 impressions; vị trí TB 20.0
  - `quần legging cạp cao` — 3 impressions; vị trí TB 55.0
  - `size quần thể thao nam` — 3 impressions; vị trí TB 82.7
  - `chọn size quần thể thao nam` — 2 impressions; vị trí TB 45.5
  - `cách chọn quần legging nữ theo dáng người` — 2 impressions; vị trí TB 19.0
  - `size quần legging` — 2 impressions; vị trí TB 92.0
  - `size áo thể thao` — 2 impressions; vị trí TB 84.5
  - `váy tennis nữ màu trắng size s` — 2 impressions; vị trí TB 15.5

### Chất liệu & công nghệ vải
- **Keyword trụ cột:** `chất liệu đồ thể thao`
- **LSI semantic mở rộng:** polyester spandex, vải co giãn 4 chiều, vải thoát mồ hôi, quick dry, Aero-Cool, Aero-Dry, Asian Fit
- **Bài đề xuất:** **Polyester, spandex hay cotton: chọn chất liệu đồ thể thao theo môn tập**
- **Dạng triển khai:** Knowledge pillar; ưu tiên P1.
- **Query exact tiêu biểu từ GSC:**
  - `vợt pickleball chất liệu nào tốt` — 248 impressions; vị trí TB 59.1
  - `vải polyester` — 240 impressions; vị trí TB 63.9
  - `bóng pickleball làm bằng chất liệu gì` — 223 impressions; vị trí TB 44.6
  - `bóng pickleball chất liệu gì` — 208 impressions; vị trí TB 29.1
  - `quả bóng pickleball làm bằng chất liệu gì` — 206 impressions; vị trí TB 41.3
  - `spandex là gì` — 163 impressions; vị trí TB 55.1
  - `chấn thương vai khi tập gym` — 142 impressions; vị trí TB 13.7
  - `vải spandex` — 95 impressions; vị trí TB 16.5
  - `áo bra tập aerobic` — 69 impressions; vị trí TB 41.1
  - `so sánh vải polyester và cotton` — 65 impressions; vị trí TB 29.5
  - `polyester là gì` — 64 impressions; vị trí TB 68.3
  - `chất liệu spandex` — 56 impressions; vị trí TB 15.3
  - `vải polyester là gì` — 56 impressions; vị trí TB 62.6
  - `chất liệu thun lạnh` — 55 impressions; vị trí TB 11.9
  - `spandex` — 51 impressions; vị trí TB 60.8
  - `vợt pickleball được làm bằng chất liệu gì` — 36 impressions; vị trí TB 87.3
  - `các bài tập vai gym` — 34 impressions; vị trí TB 62.1
  - `vải polyester có nóng không` — 34 impressions; vị trí TB 50.2
  - `chất vải polyester có nóng không` — 33 impressions; vị trí TB 82.2
  - `tập vai gym` — 33 impressions; vị trí TB 57.7
  - `vải đồ bơi mặc tập gym được k` — 33 impressions; vị trí TB 11.8
  - `polyester` — 31 impressions; vị trí TB 35.5
  - `vải may đồ thể thao` — 29 impressions; vị trí TB 28.9
  - `vải polyester mặc có nóng không` — 26 impressions; vị trí TB 65.3
  - `áo khoác thể thao nữ vải dù` — 26 impressions; vị trí TB 22.1
  - `các bài tập vai ở phòng gym` — 25 impressions; vị trí TB 58.5
  - `vải cotton spandex` — 25 impressions; vị trí TB 13.4
  - `vải polyester có mát không` — 25 impressions; vị trí TB 81.4
  - `chất liệu polyester có nóng không` — 23 impressions; vị trí TB 80.9
  - `quần polyester` — 23 impressions; vị trí TB 76.1

### Pickleball — giày, vợt, bóng & phụ kiện
- **Keyword trụ cột:** `thiết bị pickleball`
- **LSI semantic mở rộng:** giày pickleball, vợt pickleball, bóng pickleball, túi vợt pickleball, phụ kiện pickleball, chọn size cán vợt
- **Bài đề xuất:** **Checklist thiết bị pickleball cho người mới: vợt, bóng, giày và phụ kiện**
- **Dạng triển khai:** Cụm comparison / commercial; ưu tiên P0.
- **Query exact tiêu biểu từ GSC:**
  - `top vợt pickleball 2025` — 976 impressions; vị trí TB 11.8
  - `top vợt pickleball` — 896 impressions; vị trí TB 14.7
  - `giày pickleball nữ` — 815 impressions; vị trí TB 12.0
  - `giày pickleball nam` — 650 impressions; vị trí TB 10.3
  - `top hãng vợt pickleball` — 627 impressions; vị trí TB 11.0
  - `giày pickleball là gì` — 597 impressions; vị trí TB 43.6
  - `top 5 vợt pickleball tốt nhất hiện nay` — 589 impressions; vị trí TB 10.8
  - `hãng vợt pickleball tốt nhất hiện nay` — 571 impressions; vị trí TB 11.3
  - `top vợt pickleball tốt nhất hiện nay` — 566 impressions; vị trí TB 10.1
  - `nữ nên đánh vợt pickleball nào` — 562 impressions; vị trí TB 10.6
  - `top vợt pickleball cho người mới chơi` — 544 impressions; vị trí TB 29.6
  - `các loại bóng pickleball` — 523 impressions; vị trí TB 12.6
  - `bóng pickleball chuẩn thi đấu` — 489 impressions; vị trí TB 14.7
  - `top 10 vợt pickleball tốt nhất hiện nay` — 488 impressions; vị trí TB 15.7
  - `top 5 vợt pickleball` — 479 impressions; vị trí TB 11.5
  - `chọn bóng pickleball` — 474 impressions; vị trí TB 18.5
  - `cách chọn vợt pickleball cho người mới` — 471 impressions; vị trí TB 31.0
  - `bóng pickleball loại nào tốt` — 469 impressions; vị trí TB 17.1
  - `top những cây vợt pickleball` — 458 impressions; vị trí TB 10.6
  - `cách chọn bóng pickleball` — 434 impressions; vị trí TB 21.9
  - `bán vợt pickleball` — 431 impressions; vị trí TB 15.4
  - `bóng pickleball 26 lỗ và 40 lỗ khác nhau thế nào` — 428 impressions; vị trí TB 30.0
  - `vợt pickleball tốt` — 426 impressions; vị trí TB 17.3
  - `vợt pickleball nào tốt` — 415 impressions; vị trí TB 10.6
  - `bóng thi đấu pickleball franklin` — 410 impressions; vị trí TB 35.3
  - `bóng pickleball chuẩn` — 407 impressions; vị trí TB 29.7
  - `nên chọn bóng pickleball loại nào` — 386 impressions; vị trí TB 12.6
  - `hãng vợt pickleball` — 373 impressions; vị trí TB 16.6
  - `top vợt pickleball dưới 2 triệu` — 371 impressions; vị trí TB 53.9
  - `kích thước bóng pickleball` — 363 impressions; vị trí TB 36.5

### Pickleball — trang phục
- **Keyword trụ cột:** `đồ tập pickleball`
- **LSI semantic mở rộng:** áo pickleball, quần pickleball, váy pickleball, set đồ pickleball, trang phục pickleball nữ/nam, vải chơi pickleball, outfit pickleball
- **Bài đề xuất:** **Mặc gì chơi pickleball? Cách chọn trang phục theo giới tính, cường độ và thời tiết**
- **Dạng triển khai:** Pillar + guide chọn đồ; ưu tiên P0.
- **Query exact tiêu biểu từ GSC:**
  - `áo pickleball` — 7.211 impressions; vị trí TB 34.9
  - `quần áo pickleball nữ` — 1.890 impressions; vị trí TB 19.8
  - `đồ pickleball nữ` — 1.281 impressions; vị trí TB 12.0
  - `đồ tập pickleball` — 1.158 impressions; vị trí TB 13.4
  - `quần áo pickleball nam` — 726 impressions; vị trí TB 24.2
  - `giầy pickleball` — 692 impressions; vị trí TB 15.3
  - `checklist đồ mang đi sân pickleball` — 619 impressions; vị trí TB 38.3
  - `váy pickleball nữ` — 544 impressions; vị trí TB 10.6
  - `quần pickleball nam` — 522 impressions; vị trí TB 10.7
  - `lỗi thường gặp khi chơi pickleball` — 473 impressions; vị trí TB 23.4
  - `đồ pickleball nam` — 451 impressions; vị trí TB 11.3
  - `áo pickleball nữ` — 355 impressions; vị trí TB 23.2
  - `quần áo pickleball` — 313 impressions; vị trí TB 36.4
  - `áo pickleball nam` — 310 impressions; vị trí TB 12.7
  - `psc pickleball club hồ chí minh` — 271 impressions; vị trí TB 11.0
  - `trang phục pickleball` — 266 impressions; vị trí TB 42.9
  - `bộ quần áo pickleball nữ` — 243 impressions; vị trí TB 10.2
  - `váy pickleball` — 174 impressions; vị trí TB 12.2
  - `đánh pickleball mặc đồ gì` — 173 impressions; vị trí TB 13.6
  - `đồng phục pickleball` — 144 impressions; vị trí TB 25.0
  - `đồ pickleball` — 129 impressions; vị trí TB 16.5
  - `pickleball` — 126 impressions; vị trí TB 13.4
  - `sân pickleball gần đây` — 121 impressions; vị trí TB 22.4
  - `quần áo đánh pickleball nữ` — 113 impressions; vị trí TB 11.4
  - `thời trang pickleball nữ` — 102 impressions; vị trí TB 10.3
  - `bộ quần áo pickleball` — 94 impressions; vị trí TB 39.5
  - `quần áo thể thao pickleball` — 94 impressions; vị trí TB 55.9
  - `đồ tập pickleball nam` — 92 impressions; vị trí TB 17.0
  - `sân pickleball` — 92 impressions; vị trí TB 55.4
  - `mẫu áo pickleball đẹp` — 90 impressions; vị trí TB 13.1

### Gym — đồ tập, legging & bra
- **Keyword trụ cột:** `đồ tập gym`
- **LSI semantic mở rộng:** đồ tập gym nữ/nam, quần tập gym, áo tập gym, legging tập gym, bra thể thao, tank top gym, set đồ gym
- **Bài đề xuất:** **Cách chọn đồ tập gym nam nữ: áo, quần, bra, legging và độ hỗ trợ**
- **Dạng triển khai:** Pillar commercial investigation; ưu tiên P0.
- **Query exact tiêu biểu từ GSC:**
  - `quần tập gym nữ` — 4.382 impressions; vị trí TB 13.2
  - `đồ tập gym nữ` — 4.245 impressions; vị trí TB 10.5
  - `áo bra thể thao` — 3.215 impressions; vị trí TB 11.5
  - `đồ tập gym nam` — 2.921 impressions; vị trí TB 14.4
  - `áo tập gym nữ` — 1.886 impressions; vị trí TB 10.3
  - `quần tập gym` — 1.866 impressions; vị trí TB 14.8
  - `bao tay tập gym` — 1.298 impressions; vị trí TB 28.5
  - `áo tập gym` — 1.281 impressions; vị trí TB 12.3
  - `bra thể thao` — 1.157 impressions; vị trí TB 13.3
  - `áo gym nữ` — 1.106 impressions; vị trí TB 18.3
  - `đồ tập gym cho nam` — 1.102 impressions; vị trí TB 20.4
  - `đồ gym` — 1.029 impressions; vị trí TB 13.0
  - `áo tập gym nam` — 998 impressions; vị trí TB 12.3
  - `bộ quần áo tập gym nam` — 992 impressions; vị trí TB 15.5
  - `áo gym nam` — 825 impressions; vị trí TB 20.8
  - `đồ tập gym nữ ngắn` — 793 impressions; vị trí TB 14.4
  - `quần tập gym nam` — 719 impressions; vị trí TB 29.7
  - `quần áo tập gym nam` — 708 impressions; vị trí TB 10.7
  - `bộ đồ tập gym nữ` — 679 impressions; vị trí TB 22.8
  - `đồ bộ tập gym nữ` — 639 impressions; vị trí TB 20.7
  - `đồ gym nam` — 627 impressions; vị trí TB 12.7
  - `áo ba lỗ tập gym nam` — 591 impressions; vị trí TB 13.0
  - `bộ đồ tập gym nam` — 541 impressions; vị trí TB 13.6
  - `quần áo tập gym nữ hàng hiệu` — 499 impressions; vị trí TB 15.0
  - `bra thể thao nữ` — 488 impressions; vị trí TB 13.0
  - `set đồ tập gym nam` — 441 impressions; vị trí TB 13.2
  - `quần tập gym nam cao cấp` — 427 impressions; vị trí TB 10.4
  - `áo bra tập gym` — 423 impressions; vị trí TB 19.7
  - `áo ba lỗ nam tập gym` — 411 impressions; vị trí TB 19.8
  - `set đồ tập gym` — 405 impressions; vị trí TB 12.4

### Yoga & Pilates — trang phục
- **Keyword trụ cột:** `đồ tập yoga`
- **LSI semantic mở rộng:** đồ tập yoga, quần áo yoga, áo tập yoga, đồ yoga nữ/nam, bra yoga, đồ tập pilates, size đồ yoga
- **Bài đề xuất:** **Tập yoga nên mặc gì? Cách chọn áo, quần và chất liệu theo động tác**
- **Dạng triển khai:** Pillar + guide chọn đồ; ưu tiên P0.
- **Query exact tiêu biểu từ GSC:**
  - `đồ tập yoga` — 5.791 impressions; vị trí TB 11.7
  - `áo tập yoga` — 1.747 impressions; vị trí TB 14.9
  - `đồ tập yoga cho nam` — 1.690 impressions; vị trí TB 18.0
  - `quần áo tập yoga` — 1.532 impressions; vị trí TB 14.6
  - `bra yoga` — 1.166 impressions; vị trí TB 16.7
  - `quần áo tập yoga hàng hiệu` — 664 impressions; vị trí TB 12.1
  - `đồ yoga` — 625 impressions; vị trí TB 10.3
  - `đồ yoga nữ` — 535 impressions; vị trí TB 13.0
  - `quần áo yoga nữ` — 472 impressions; vị trí TB 12.7
  - `đồ tập yoga kín đáo` — 336 impressions; vị trí TB 21.9
  - `đồ tập yoga cao cấp` — 327 impressions; vị trí TB 11.0
  - `đồ yoga nữ đẹp` — 278 impressions; vị trí TB 21.3
  - `quần áo yoga` — 273 impressions; vị trí TB 14.0
  - `do tap yoga` — 250 impressions; vị trí TB 12.7
  - `trang phục tập yoga cho nữ` — 242 impressions; vị trí TB 10.4
  - `áo ngực tập yoga` — 200 impressions; vị trí TB 28.9
  - `do yoga` — 194 impressions; vị trí TB 17.6
  - `áo quần tập yoga` — 188 impressions; vị trí TB 11.1
  - `áo yoga` — 184 impressions; vị trí TB 11.2
  - `bộ đồ yoga` — 183 impressions; vị trí TB 11.2
  - `đồ tập yoga tốt` — 174 impressions; vị trí TB 30.1
  - `quần áo tập yoga nữ hàng hiệu` — 168 impressions; vị trí TB 15.6
  - `set đồ tập yoga` — 144 impressions; vị trí TB 10.9
  - `đồ yoga đẹp` — 137 impressions; vị trí TB 11.6
  - `áo tập yoga đẹp` — 135 impressions; vị trí TB 10.9
  - `quần áo tập yoga nam` — 130 impressions; vị trí TB 13.4
  - `áo tập yoga dài tay` — 130 impressions; vị trí TB 14.3
  - `đồ tập yoga đà nẵng` — 122 impressions; vị trí TB 10.6
  - `mặc đồ tập yoga đẹp` — 122 impressions; vị trí TB 41.1
  - `áo tập yoga có tay` — 115 impressions; vị trí TB 15.9

### Tennis & chạy bộ — trang phục
- **Keyword trụ cột:** `đồ tennis và chạy bộ`
- **LSI semantic mở rộng:** đồ tennis nữ/nam, áo tennis, quần tennis, quần áo chạy bộ, áo chạy bộ, legging chạy bộ
- **Bài đề xuất:** **Trang phục tennis và chạy bộ khác nhau thế nào? Cách chọn theo chuyển động**
- **Dạng triển khai:** Comparison + guide; ưu tiên P1.
- **Query exact tiêu biểu từ GSC:**
  - `quần tennis nam` — 1.944 impressions; vị trí TB 17.2
  - `quần chạy bộ nữ` — 1.223 impressions; vị trí TB 31.4
  - `đồ tập tennis nữ` — 1.215 impressions; vị trí TB 21.2
  - `quần áo chạy bộ nữ` — 1.191 impressions; vị trí TB 16.9
  - `quần áo tennis nam` — 833 impressions; vị trí TB 35.4
  - `trang phục chạy bộ nữ` — 742 impressions; vị trí TB 22.3
  - `áo tennis` — 602 impressions; vị trí TB 29.2
  - `đồ tennis nữ` — 491 impressions; vị trí TB 16.0
  - `đồ tennis nam` — 473 impressions; vị trí TB 24.5
  - `quần chạy bộ jogger uniqlo` — 443 impressions; vị trí TB 40.0
  - `ao tennis` — 328 impressions; vị trí TB 11.8
  - `quần áo chạy bộ` — 311 impressions; vị trí TB 27.7
  - `đồ chạy bộ` — 299 impressions; vị trí TB 29.2
  - `quần short chạy bộ nữ` — 268 impressions; vị trí TB 31.8
  - `đồ tennis` — 232 impressions; vị trí TB 12.0
  - `quần áo chạy bộ nam` — 194 impressions; vị trí TB 29.6
  - `áo tennis nữ` — 194 impressions; vị trí TB 30.3
  - `đồ chạy bộ nữ` — 182 impressions; vị trí TB 23.9
  - `set đồ chạy bộ` — 147 impressions; vị trí TB 33.8
  - `áo chạy bộ nam` — 141 impressions; vị trí TB 49.0
  - `quần áo tennis` — 138 impressions; vị trí TB 42.3
  - `quần áo chạy bộ cho nam` — 137 impressions; vị trí TB 23.4
  - `quần tennis` — 118 impressions; vị trí TB 23.6
  - `đồ chạy bộ cho nam` — 115 impressions; vị trí TB 35.5
  - `quần áo tennis nữ` — 111 impressions; vị trí TB 29.2
  - `bộ đồ chạy bộ nữ` — 109 impressions; vị trí TB 32.7
  - `set đồ chạy bộ nam` — 106 impressions; vị trí TB 39.5
  - `bộ quần áo chạy bộ nam` — 99 impressions; vị trí TB 42.0
  - `áo ngực chạy bộ` — 90 impressions; vị trí TB 47.3
  - `bộ đồ chạy bộ nam` — 82 impressions; vị trí TB 39.8

### Outfit & athleisure
- **Keyword trụ cột:** `phối đồ thể thao`
- **LSI semantic mở rộng:** athleisure, phối đồ thể thao nữ/nam, outfit pickleball, outfit gym, phối áo polo, phối chân váy thể thao
- **Bài đề xuất:** **Athleisure là gì? 7 cách phối đồ thể thao từ phòng tập đến đi chơi**
- **Dạng triển khai:** Inspiration cluster; ưu tiên P1.
- **Query exact tiêu biểu từ GSC:**
  - `thời trang quần thun thể thao` — 615 impressions; vị trí TB 16.8
  - `thời trang legging` — 398 impressions; vị trí TB 25.3
  - `thời trang thể thao` — 125 impressions; vị trí TB 21.2
  - `thời trang thể thao nữ` — 113 impressions; vị trí TB 28.4
  - `thời trang yoga` — 98 impressions; vị trí TB 26.1
  - `thương hiệu thời trang thể thao nổi tiếng` — 59 impressions; vị trí TB 48.6
  - `thời trang gym cho nam` — 58 impressions; vị trí TB 28.1
  - `quần thể thao nam thời trang` — 53 impressions; vị trí TB 14.1
  - `thời trang gym cho nữ` — 43 impressions; vị trí TB 21.1
  - `quần áo thể thao thời trang` — 30 impressions; vị trí TB 15.6
  - `quần nam thời trang thể thao` — 23 impressions; vị trí TB 13.9
  - `quần thể thao thời trang` — 23 impressions; vị trí TB 20.9
  - `thương hiệu thời trang thể thao nổi tiếng thị trường` — 21 impressions; vị trí TB 15.3
  - `thời trang gym` — 17 impressions; vị trí TB 18.7
  - `cách phối đồ thể thao nữ` — 12 impressions; vị trí TB 59.5
  - `athleisure là gì` — 9 impressions; vị trí TB 47.3
  - `thương hiệu thời trang thể thao` — 8 impressions; vị trí TB 14.9
  - `phối đồ thể thao nam` — 7 impressions; vị trí TB 53.0
  - `phối đồ áo khoác thể thao nam` — 7 impressions; vị trí TB 62.4
  - `thời trang thể thao nam` — 6 impressions; vị trí TB 42.5
  - `các hãng thời trang thể thao` — 5 impressions; vị trí TB 19.8
  - `thương hiệu thời trang thể thao việt nam` — 5 impressions; vị trí TB 18.8
  - `phối đồ thể thao nữ` — 4 impressions; vị trí TB 60.5
  - `phối đồ với quần legging lửng` — 4 impressions; vị trí TB 81.0
  - `phối đồ thể thao` — 3 impressions; vị trí TB 76.3
  - `các hãng thời trang thể thao việt nam` — 2 impressions; vị trí TB 44.0
  - `phối đồ với quần legging` — 2 impressions; vị trí TB 90.5
  - `phối đồ với quần legging dài` — 2 impressions; vị trí TB 95.5
  - `phối đồ với quần thể thao` — 2 impressions; vị trí TB 85.0
  - `phối đồ với quần thể thao nữ` — 2 impressions; vị trí TB 36.5

### Kiến thức gym, yoga & fitness
- **Keyword trụ cột:** `kiến thức gym yoga cho người mới`
- **LSI semantic mở rộng:** gymer là gì, fitness là gì, bài tập gym, lịch tập gym, yoga là gì, tư thế yoga, cardio, bodybuilding
- **Bài đề xuất:** **Gym, yoga và fitness cho người mới: chọn bộ môn, lịch tập và trang phục phù hợp**
- **Dạng triển khai:** TOFU knowledge hub; ưu tiên P2.
- **Query exact tiêu biểu từ GSC:**
  - `vinyasa yoga là gì` — 1.974 impressions; vị trí TB 10.5
  - `yoga là gì` — 761 impressions; vị trí TB 11.0
  - `trang phục tập gym nam` — 651 impressions; vị trí TB 30.2
  - `bộ tập gym nữ` — 632 impressions; vị trí TB 22.2
  - `yoga stretch là gì` — 607 impressions; vị trí TB 11.8
  - `trang phục tập gym` — 582 impressions; vị trí TB 10.3
  - `tập fitness là gì` — 430 impressions; vị trí TB 10.3
  - `yoga therapy` — 370 impressions; vị trí TB 21.3
  - `yoga hatha là gì` — 346 impressions; vị trí TB 10.1
  - `khăn trải thảm yoga loại nào tốt` — 329 impressions; vị trí TB 30.1
  - `yoga cho bà bầu 3 tháng giữa` — 326 impressions; vị trí TB 12.5
  - `tập gym tại nhà` — 310 impressions; vị trí TB 30.1
  - `hướng dẫn tập gym tại nhà` — 307 impressions; vị trí TB 20.9
  - `lịch tập gym cho người mới` — 304 impressions; vị trí TB 15.4
  - `yoga cho bà bầu 3 tháng đầu` — 301 impressions; vị trí TB 13.3
  - `lịch tập gym cho người mới bắt đầu` — 296 impressions; vị trí TB 15.5
  - `app tập gym` — 278 impressions; vị trí TB 13.2
  - `app tập gym free` — 264 impressions; vị trí TB 11.8
  - `túi tập gym` — 258 impressions; vị trí TB 37.8
  - `aerial yoga` — 256 impressions; vị trí TB 10.6
  - `thảm yoga định tuyến` — 235 impressions; vị trí TB 15.3
  - `lợi ích của yoga` — 220 impressions; vị trí TB 10.1
  - `app tập gym cho nam` — 211 impressions; vị trí TB 10.7
  - `dụng cụ tập gym` — 197 impressions; vị trí TB 45.4
  - `lịch tập gym` — 191 impressions; vị trí TB 32.2
  - `yoga cho mẹ bầu 3 tháng đầu` — 190 impressions; vị trí TB 10.2
  - `kích thước thảm yoga` — 180 impressions; vị trí TB 11.5
  - `yoga vinyasa là gì` — 172 impressions; vị trí TB 11.1
  - `hatha dynamic yoga là gì` — 163 impressions; vị trí TB 13.0
  - `fitness la gi` — 154 impressions; vị trí TB 10.1

### Sportswear tổng quát — cần review
- **Keyword trụ cột:** `đồ thể thao`
- **LSI semantic mở rộng:** đồ thể thao, quần áo thể thao, trang phục vận động
- **Bài đề xuất:** **Rà soát thủ công trước khi tạo nội dung; không tự động tạo bài cho query không đủ topical fit**
- **Dạng triển khai:** Review; ưu tiên P3.
- **Query exact tiêu biểu từ GSC:**
  - `áo thể thao nữ` — 3.000 impressions; vị trí TB 14.8
  - `quần áo thể thao nữ` — 2.933 impressions; vị trí TB 13.5
  - `áo thể thao chất lượng` — 2.777 impressions; vị trí TB 50.0
  - `áo ngực thể thao` — 2.497 impressions; vị trí TB 27.7
  - `đồ thể thao` — 2.211 impressions; vị trí TB 11.0
  - `quần dài thể thao nam` — 1.937 impressions; vị trí TB 10.9
  - `legging` — 1.931 impressions; vị trí TB 21.2
  - `quần leggings` — 1.635 impressions; vị trí TB 14.5
  - `áo khoác thể thao nam` — 1.465 impressions; vị trí TB 32.9
  - `quần short thể thao nữ` — 1.238 impressions; vị trí TB 12.9
  - `áo khoác thể thao nữ` — 1.234 impressions; vị trí TB 25.0
  - `đồ tập thể dục` — 1.192 impressions; vị trí TB 22.4
  - `áo khoác thể thao` — 1.154 impressions; vị trí TB 36.0
  - `quần dài thể thao` — 1.118 impressions; vị trí TB 13.3
  - `quần tập thể dục nữ` — 1.056 impressions; vị trí TB 10.2
  - `quần leggings nữ` — 985 impressions; vị trí TB 17.3
  - `quần ôm legging` — 897 impressions; vị trí TB 14.1
  - `quần legging dài` — 861 impressions; vị trí TB 12.9
  - `trang phục gym nam` — 722 impressions; vị trí TB 22.0
  - `bra` — 520 impressions; vị trí TB 19.0
  - `đồ thể thao nam` — 456 impressions; vị trí TB 34.9
  - `áo thun thể thao` — 451 impressions; vị trí TB 22.2
  - `áo thể thao` — 449 impressions; vị trí TB 20.2
  - `quần thun thể thao nam` — 445 impressions; vị trí TB 15.4
  - `quần jogger nam thể thao` — 401 impressions; vị trí TB 11.6
  - `đồ tập thể dục nam` — 389 impressions; vị trí TB 13.5
  - `quần thể thao dài cho nam` — 386 impressions; vị trí TB 10.8
  - `dây nhảy thể dục` — 386 impressions; vị trí TB 20.2
  - `đồ thể thao nữ cao cấp` — 374 impressions; vị trí TB 17.0
  - `đồ tập thể thao nam` — 360 impressions; vị trí TB 13.4

## Quy tắc chống cannibalization

- Một URL chỉ nhận một intent chính: chọn đồ, kiến thức bộ môn, comparison, local hoặc B2B.
- Không tách bài riêng cho biến thể số ít/số nhiều, lỗi chính tả hoặc query chỉ khác `nữ/nam` nếu nội dung có thể xử lý trong cùng guide.
- Cụm trang phục nên dẫn về category ICADO; cụm giá, mua, shop và sản phẩm cụ thể cần phân định với `thegioidotap.vn`.
- Cụm B2B/sỉ cần hub và CTA riêng, không trộn vào blog D2C.
- Query 1–5 impressions giữ làm FAQ/H3/semantic variant, không tạo URL độc lập.
