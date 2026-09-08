---
name: everest-article-audit
description: >
  Final audit gate and formatting rules for Everest Logistics articles.
  Enforces lead-in bolding for structured lists while banning inline overbolding,
  strips broken ASCII-art diagrams/code-boxes, bans LaTeX math syntax,
  and validates clean mobile-friendly Markdown formatting before publication.
---

# Everest Logistics Article Final Audit Skill

## Mục đích
Skill này là **bước kiểm duyệt bắt buộc (Final Audit Gate)** cuối cùng trước khi xuất bản bất kỳ bài viết nào cho thương hiệu **Everest Logistics**.

---

## 1. Quy tắc 1: Chuẩn hóa Bôi đậm (Lead-in Bold vs Inline Overbolding)

### ✅ ĐƯỢC PHÉP & BẮT BUỘC: In đậm Nhãn Đầu Dòng (Lead-in Bolding)
* Khi trình bày các danh sách gạch đầu dòng (bullet points) hoặc danh sách có cấu trúc (như Key Takeaways, checklist, các bước, ưu/nhược điểm, tình huống/giải pháp), **bắt buộc in đậm phần nhãn/tiêu đề đầu dòng kèm dấu hai chấm**:
  * Ví dụ đúng: `* **Giá DDP (Delivered Duty Paid - Giao hàng đã nộp thuế):** Là điều kiện giao hàng trọn gói...`
  * Ví dụ đúng: `* **Nghĩa vụ tối đa (Maximum Obligation):** DDP đặt nghĩa vụ và rủi ro lớn nhất...`
  * Ví dụ đúng: `* **Điểm chuyển giao rủi ro:** Rủi ro chuyển sang Người mua tại kho đích...`
  * Ví dụ đúng: `* **Hậu quả:** Rủi ro đã chuyển sang Người mua ngay từ khi...`
  * Ví dụ đúng: `* **Giải pháp phòng ngừa:** Doanh nghiệp phải yêu cầu Người bán...`

### ❌ CẤM: Bôi đậm rải rác giữa câu văn (Inline Overbolding)
* Tuyệt đối không bôi đậm rải rác các cụm từ ngữ, từ khóa ngẫu nhiên nằm ở giữa câu văn (ví dụ sai: `...rủi ro lại kết thúc ngay tại **cảng bốc hàng (Port of Loading)** khi hàng được xếp an toàn...`).
* Toàn bộ phần nội dung diễn giải sau nhãn đầu dòng phải là **văn bản thường (Normal Text)**, liền mạch, tự nhiên và chuyên nghiệp.

---

## 2. Quy tắc 2: CẤM Bảng vẽ ASCII / Sơ đồ Text-Art trong Code Block

### ❌ Lỗi nghiêm trọng:
* Sử dụng code block (```` ``` ````) để vẽ sơ đồ hộp, bảng ASCII art bằng các ký tự `+---+`, `|...|`, `====>`.
* Các khối ASCII art này **bị vỡ layout hoàn toàn trên giao diện mobile và web responsive**, tạo trải nghiệm người dùng rất xấu.

### ✅ Quy chuẩn chuẩn mực:
* **Thay thế 100% bằng Bảng Markdown tiêu chuẩn (Standard Markdown Table)** với các cột được căn chỉnh rõ ràng.
* Hoặc sử dụng cấu trúc danh sách có thứ tự / gạch đầu dòng phân cấp rõ ràng.

---

## 3. Quy tắc 3: CẤM Dùng cú pháp LaTeX Math (`$...$`, `$$...$$`) cho công thức

### ❌ Lỗi nghiêm trọng:
* Dùng ký hiệu LaTeX `$$ \text{Giá CFR} = \text{Giá FOB} + ... $$` hoặc `$FOB + F$`.
* Trình hiển thị Markdown/CMS không hỗ trợ tiếng Việt có dấu trong LaTeX, dẫn đến việc chữ tiếng Việt bị bung tách từng ký tự và dấu thanh (ví dụ lỗi: `Gi a ˊ CFR = Gi a ˊ FOB...`).

### ✅ Quy chuẩn chuẩn mực:
* **Viết công thức bằng văn bản thuần (Plain Text) rõ ràng**, đặt trên dòng riêng hoặc dùng dấu gạch đầu dòng:
  * Ví dụ đúng: `Công thức: Giá CFR = Giá FOB + Cước vận tải biển quốc tế (Freight)`
  * Viết tắt: `CFR = FOB + F`
* Trong các bảng tính toán ví dụ: Viết phép tính trực tiếp bằng số và chữ bình thường (ví dụ: `FOB + F = 35.000 + 850 = 35.850 USD`).

---

## 4. Checklist Audit hoàn tất trước khi xuất bản

1. [ ] **Chuẩn hóa Bôi đậm:** Đảm bảo tất cả các bullet points quan trọng đều có in đậm nhãn đầu dòng (`* **Nhãn:** Nội dung`); gỡ bỏ toàn bộ việc bôi đậm vụn vặt ở giữa câu văn.
2. [ ] **Quét ASCII Art:** Đảm bảo không còn bất kỳ khối `+----+` text art nào trong code block. Mọi sơ đồ phải được chuyển đổi sang bảng Markdown hoặc văn bản phân cấp.
3. [ ] **Quét LaTeX Math:** Đảm bảo không còn bất kỳ ký tự `$`, `$$`, `\text{}` nào trong công thức và bảng tính.
4. [ ] **Bảng biểu chuẩn:** Mọi bảng so sánh, checklist chi phí, phân chia trách nhiệm đều dùng cú pháp Markdown table `| Cột 1 | Cột 2 |`.
5. [ ] **Khung E-E-A-T & Chữ ký:** Đảm bảo đủ thông tin người kiểm duyệt chuyên môn (Mr. Ryan Vỹ), ngày cập nhật, căn cứ pháp lý và chữ ký thương hiệu Everest Logistics ở cuối bài.
