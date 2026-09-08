---
name: generating-outlines-icado
description: >
  Generates a comprehensive Semantic SEO tabular outline for ICADO,
  focusing on D2C Sportswear, Gym/Yoga Ergonomics, Fabric Technology, and Direct Conversion.
---

# Generating Outlines for ICADO

Skill này lắp ráp và xuất bản Outline chuẩn Bảng (Table Format) cho **ICADO (Thời trang thể thao & Đồ tập Gym/Yoga)**.

## Các bước lắp ráp Outline:
1. **Nạp dữ liệu**: Đọc `icado-outline-rules`, kết quả cào đối thủ đồ tập và danh mục sản phẩm ICADO.
2. **Khởi tạo Header**:
   ```markdown
   # Outline: [Title Thời Trang Thể Thao / Đồ Tập Đẹp ≤ 60 chars]

   | Field | Value |
   |---|---|
   | Title | [Title Chuẩn SEO D2C Sportswear] |
   | Meta | [130-160 chars] |
   | KW chính/phụ | [Liệt kê] |
   | Target Audience | Gymer, Người tập Yoga/Pilates, Người chạy bộ, Tín đồ thời trang thể thao Athleisure |
   | Hard rules | Chuẩn xác thông số chất liệu co giãn 4 chiều, bảng size 3 vòng, công năng bộ môn |
   ```
3. **Lắp ráp 3 Bảng bắt buộc**:
   - `Keyword Strategy Table` (5 trường)
   - `Competitor Analysis Table` (7 cột có quote live)
   - `Outline Candidate Table` (8 cột, nội dung bullet phân tích chất liệu và phối đồ thể thao)
4. **Lồng ghép H2 Trải nghiệm đồ tập ICADO & Chữ ký chuẩn**.
5. **Kiểm tra QA Score** $\ge 80$.
