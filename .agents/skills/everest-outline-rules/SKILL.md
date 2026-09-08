---
name: everest-outline-rules
description: >
  Contains core business rules, logistics constraints, Freight/Customs Service Matching,
  and Outline Consolidation for Everest Logistics. Must be applied before outline generation.
---

# Everest Logistics Outline Rules

## 0. Rule 0: Bắt buộc sử dụng Browser & So sánh đối thủ đang Live (Hard Requirement)
- ✅ **LIVE EXTRACTION**: Bắt buộc sử dụng trình duyệt (`browser tool`) để search Google live và cào trực tiếp cấu trúc Headings (H1, H2, H3), nội dung bài viết, bảng biểu cước, quy trình thủ tục từ Top 3–5 đối thủ Logistics (Indochina Post, Ratraco, T&M Forwarding, Vinalink...).
- ❌ **CẤM DỮ LIỆU ẢO**: Tuyệt đối không phán đoán đối thủ hoặc bịa đặt trích dẫn quy định hải quan. Cột `Example` trong Bảng Phân Tích Đối Thủ bắt buộc phải chứa trích dẫn ngắn (quote) lấy trực tiếp từ bài đối thủ.
- ✅ **AUDIT SO SÁNH**: Trong cột `So với bài hiện tại` của Bảng Cấu Trúc Outline, bắt buộc đối chiếu chi tiết từng Heading xem bài cũ đã có, cần giữ nguyên, cần tinh chỉnh hay là phần mới hoàn toàn.

### 0.1. Schema bảng bắt buộc
- **Keyword Strategy Table:** luôn phải có đủ các trường `Main keyword`, `Keyword phụ`, `Google Suggest`, `LSI Keyword`, `PAA`.
- **Competitor Analysis Table:** luôn phải có đủ các cột `#`, `URL`, `Strengths`, `Weaknesses`, `What We Learn`, `Opportunity`, `Example`.
- **Outline Candidate Table:** luôn phải có đủ các cột `#`, `Heading`, `Why`, `Evidence`, `Content Direction`, `Content Format`, `Differentiation`, `So với bài hiện tại`. Nội dung diễn giải bắt buộc viết dạng gạch đầu dòng (bullet points).

## 1. Writing Style & Logistics Constraints
- ✅ **BẮT BUỘC THAM KHẢO BRAND PERSONA**: Tra cứu kỹ `data/reference/persona-brand/Everest-Logistics/persona-everest-skill.md` và `central-entity-Everest-Logistics.md`.
- ❌ **KHÔNG** dùng từ sáo rỗng, hoa mỹ rẻ tiền. Văn phong logistics phải chuyên nghiệp, chính xác về thuật ngữ (Incoterms 2020, Bill of Lading, HS Code, C/O, CFS/CY...).
- ❌ **KHÔNG** đưa cam kết viển vông như "thông quan 100% không cần kiểm tra", "cước rẻ nhất thế giới".
- ✅ **ĐỘ DÀI TIÊU CHUẨN:** Outline hướng tới bài viết B2B chuyên sâu (1800 - 2500 từ), phân bổ bảng biểu so sánh cước, quy trình từng bước và checklist chứng từ.

## 2. Lead Generation & Service Matching
Xác định keyword liên quan đến dịch vụ nào của Everest Logistics:
- Vận tải đường biển quốc tế (FCL/LCL)
- Vận tải hàng không (Air Freight)
- Khai thuê hải quan & tư vấn thuế xuất nhập khẩu
- Dịch vụ kho bãi CFS, bonded warehouse, phân phối nội địa
- Ủy thác xuất nhập khẩu trọn gói

**Nguyên tắc lồng ghép H2 Service**:
Thêm 1 H2 thúc đẩy liên hệ / nhận báo giá dịch vụ Everest Logistics trước Kết bài:
- `## [Số]. Giải pháp [Tên Dịch Vụ] tối ưu chi phí & thời gian tại Everest Logistics`
- Phân nhánh 3 H3 con:
  - `### [Số].1. Năng lực mạng lưới & cam kết vận hành của Everest Logistics`
  - `### [Số].2. Quy trình tiếp nhận & báo giá minh bạch`
  - `### [Số].3. Bảng biểu phí tham khảo & chính sách hỗ trợ doanh nghiệp XNK`

## 3. Outline Consolidation Pattern
- **Gộp heading**: Gộp các ý nhỏ thành H3 trong một H2 lớn. Duy trì **5 đến 6 H2 chính**.
- **FAQ**: Đẩy các câu hỏi ngắn (mã HS, thuế suất, thời gian transit, chứng từ đi kèm) xuống FAQ. FAQ **CÓ ĐÚNG 5 CÂU HỎI**.
- **Bảng biểu bắt buộc**: Bảng so sánh phương thức (FCL vs LCL, Air vs Sea), bảng chi phí phát sinh, bảng checklist hồ sơ hải quan.

## 4. Chữ ký thương hiệu Everest Logistics
Ở cuối cùng của outline, gắn chữ ký chuẩn:
```markdown
*Everest Logistics — Đối tác giao nhận vận tải quốc tế và giải pháp chuỗi cung ứng toàn cầu chuyên nghiệp. Hotline: (+84) ... | Email: info@everestlogs.com | Website: everestlogs.com*
```
