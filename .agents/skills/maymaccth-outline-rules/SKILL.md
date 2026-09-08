---
name: maymaccth-outline-rules
description: >
  Contains core B2B uniform manufacturing rules, fabric technical specifications,
  Haiphong local SEO signals, and Outline Consolidation for May Mặc CTH.
---

# May Mặc CTH Outline Rules

## 0. Rule 0: Bắt buộc sử dụng Browser & So sánh đối thủ đang Live (Hard Requirement)
- ✅ **LIVE EXTRACTION**: Bắt buộc dùng trình duyệt (`browser tool`) để search Google live và cào trực tiếp cấu trúc Headings (H1, H2, H3), bảng giá may, chất liệu vải từ Top 3–5 xưởng may đồng phục (Đồng Phục Bốn Mùa, Đồng Phục Hải Anh, Ong Vàng, May Mặc Song Phú...).
- ❌ **CẤM DỮ LIỆU ẢO**: Tuyệt đối không phán đoán đối thủ hoặc bịa đặt bảng giá may, bảng size. Cột `Example` trong Bảng Phân Tích Đối Thủ bắt buộc có quote live.
- ✅ **AUDIT SO SÁNH**: Đối chiếu chi tiết từng Heading so với bài viết hiện có của CTH.

### 0.1. Schema bảng bắt buộc
- **Keyword Strategy Table:** `Main keyword`, `Keyword phụ`, `Google Suggest`, `LSI Keyword`, `PAA`.
- **Competitor Analysis Table:** `#`, `URL`, `Strengths`, `Weaknesses`, `What We Learn`, `Opportunity`, `Example`.
- **Outline Candidate Table:** `#`, `Heading`, `Why`, `Evidence`, `Content Direction`, `Content Format`, `Differentiation`, `So với bài hiện tại`. Nội dung diễn giải bắt buộc viết dạng gạch đầu dòng (bullet points).

## 1. Writing Style & Manufacturing Constraints
- ✅ **BẮT BUỘC THAM KHẢO DỮ LIỆU XƯỞNG**: Tra cứu `data/reference/persona-brand/MayMacCTH/content-rules.md` và `central-entity-MayMacCTH.md`.
- ✅ **TÍN HIỆU LOCAL SEO HẢI PHÒNG & MIỀN BẮC**: Lồng ghép tự nhiên các khu công nghiệp trọng điểm (KCN VSIP Hải Phòng, KCN Đình Vũ, KCN Tràng Duệ, KCN Nomura, KCN Nam Sách, KCN Phố Nối...).
- ❌ **KHÔNG** dùng các từ chung chung mơ hồ ("vải tốt nhất"). Phải nêu rõ tên loại vải (CVC 65/35, Cotton 100% 4 chiều, Vải cá sấu Poly Thái, Vải Kaki Pangrim Hàn Quốc, Vải Lon, Kate Silk...).
- ✅ **BẢNG BIỂU BẮT BUỘC:** 
  1. Bảng so sánh ưu nhược điểm & độ bền các loại vải.
  2. Bảng thông số chọn size chuẩn người Việt (S, M, L, XL, XXL, 3XL).
  3. Bảng báo giá may theo số lượng (10 - 50 áo, 50 - 200 áo, >500 áo).

## 2. Lead Generation & CTH Service Promotion
Lồng ghép 1 H2 thúc đẩy nhận mẫu vải & báo giá trực tiếp từ xưởng May Mặc CTH trước Kết bài:
- `## [Số]. Xưởng may [Sản phẩm đồng phục] uy tín, giá tận xưởng tại Hải Phòng — May Mặc CTH`
- 3 H3 gợi ý:
  - `### [Số].1. Năng lực xưởng may trực tiếp & công nghệ in thêu hiện đại`
  - `### [Số].2. Quy trình đặt may & chính sách gửi mẫu vải miễn phí tận nơi`
  - `### [Số].3. Bảng báo giá may sỉ & cam kết bảo hành đường kim mũi chỉ`

## 3. Outline Consolidation Pattern
- **Gộp heading**: Duy trì **5 đến 6 H2 chính**.
- **FAQ**: Đẩy các thắc mắc (thời gian may mẫu, số lượng tối thiểu, giặt ủi bảo quản) xuống FAQ **ĐÚNG 5 CÂU**.
- **Chữ ký May Mặc CTH**:
```markdown
*May Mặc CTH — Xưởng may đồng phục công ty, bảo hộ lao động, áo polo doanh nghiệp uy tín hàng đầu Hải Phòng và miền Bắc. Hotline/Zalo: 0988.xxx.xxx | Xưởng: TP. Hải Phòng | Website: maymaccth.com*
```
