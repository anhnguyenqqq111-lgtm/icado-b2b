# ICADO — Full D2C Sportswear Content Workflow Pipeline

Workflow sản xuất nội dung chuyên sâu cho **ICADO — Thời Trang Thể Thao & Đồ Tập Gym / Yoga Cao Cấp** (icado.vn) chuẩn hóa theo kiến trúc FigJam 3 Cấp độ (3-Level Architecture) kết hợp Cổng kiểm soát chất lượng (Gates & Feedback Loops).

**Lệnh kích hoạt:** `/flow-ICADO-seo [keyword chính] [keyword phụ 1] [keyword phụ 2] ...`

---

## 1. LEVEL 1: HIGH-LEVEL WORKFLOW (WHAT) — 8 ĐẦU VIỆC LỚN

Sơ đồ luồng tổng thể 8 Workstreams và đầu ra tương ứng:

```mermaid
graph LR
    classDef workstream fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#fff;
    classDef output fill:#1f2937,stroke:#6b7280,stroke-width:1px,color:#93c5fd;

    W1["01. PLANNING<br><i>Xác định bộ môn tập, dòng đồ tập, tệp khách D2C</i>"]:::workstream
    W2["02. RESEARCH<br><i>Thu thập thông số vải co giãn, form dáng, đối thủ</i>"]:::workstream
    W3["03. CONTENT STRATEGY<br><i>Tìm góc tiếp cận tôn dáng, công năng vận động & size</i>"]:::workstream
    W4["04. OUTLINE DEV<br><i>Xây dựng cấu trúc outline, bảng size 3 vòng, FAQ</i>"]:::workstream
    W5["05. OUTLINE QA<br><i>Kiểm tra tính khoa học của chuyển động & chất liệu</i>"]:::workstream
    W6["06. CLIENT APPROVAL<br><i>Gửi Brand Manager duyệt, nhận feedback, khóa outline</i>"]:::workstream
    W7["07. ARTICLE WRITING<br><i>Viết bài thời trang thể thao truyền cảm hứng, chuẩn SEO</i>"]:::workstream
    W8["08. ARTICLE QA & PUBLISH<br><i>Fact-check chất liệu, link sản phẩm & xuất bản</i>"]:::workstream

    O1["📄 Sportswear Brief"]:::output
    O2["📦 Fabric & Fit Research Bundle"]:::output
    O3["📐 Ergonomics & Style Strategy"]:::output
    O4["📑 ICADO Outline Candidate"]:::output
    O5["📊 QA Report & Score"]:::output
    O6["🔒 Approved Outline (Locked)"]:::output
    O7["📝 Sportswear Article Draft"]:::output
    O8["🚀 Published Article"]:::output

    W1 --> O1 --> W2
    W2 --> O2 --> W3
    W3 --> O3 --> W4
    W4 --> O4 --> W5
    W5 --> O5 --> W6
    W6 --> O6 --> W7
    W7 --> O7 --> W8
    W8 --> O8
```

---

## 2. GATES & FEEDBACK LOOPS (CỔNG KIỂM SOÁT CHẤT LƯỢNG)

```mermaid
graph TD
    classDef gate fill:#7f1d1d,stroke:#ef4444,stroke-width:2px,color:#fff;
    classDef step fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#fff;
    classDef pass fill:#065f46,stroke:#10b981,stroke-width:2px,color:#fff;

    G1{"Planning Gate<br>Xác nhận bộ môn & phân khúc đồ tập?"}:::gate
    G2{"Research Gate<br>Dữ liệu chất liệu & bảng size đầy đủ?"}:::gate
    G3{"Strategy Gate<br>Điểm khác biệt form dáng ICADO rõ ràng?"}:::gate
    G4{"Outline Gate<br>Bảng dàn ý đạt chuẩn 8 cột bullet?"}:::gate
    G5{"QA Gate<br>Score ≥ 80 & Tính khoa học vận động chuẩn?"}:::gate
    G6{"Approval Gate<br>Brand Manager duyệt & Khóa dàn ý?"}:::gate
    G7{"Writing Gate<br>Viết chuẩn xác 100% cấu trúc đã khóa?"}:::gate
    G8{"Final Gate<br>Fact-check chất liệu/size 100% PASS?"}:::gate

    S1["01. Planning"]:::step --> G1
    G1 -- Yes --> S2["02. Research"]:::step
    G1 -- No --> S1

    S2 --> G2
    G2 -- Yes --> S3["03. Content Strategy"]:::step
    G2 -- No --> S2

    S3 --> G3
    G3 -- Yes --> S4["04. Outline Development"]:::step
    G3 -- No --> S3

    S4 --> G4
    G4 -- Yes --> S5["05. Outline QA"]:::step
    G4 -- No --> S4

    S5 --> G5
    G5 -- "PASS (≥80)" --> S6["06. Client Approval"]:::step
    G5 -- "FAIL (<80)" --> S4

    S6 --> G6
    G6 -- "Approved & Locked" --> S7["07. Article Writing"]:::step
    G6 -- "Cần sửa cấu trúc" --> S4
    G6 -- "Đổi bộ môn/concept" --> S3

    S7 --> G7
    G7 -- Yes --> S8["08. Article QA & Publish"]:::step
    G7 -- "Lệch phong cách" --> S7

    S8 --> G8
    G8 -- "PASS (100%)" --> DONE["🚀 Xuất bản (Publish)"]:::pass
    G8 -- "Chưa đạt chuẩn" --> S7
```

---

## 3. LEVEL 2: LOW-LEVEL WORKFLOW (HOW) — CHI TIẾT TỪNG ĐẦU VIỆC

### 01. PLANNING
*   **1.1 Xác định dòng đồ tập**: Đồ tập Gym (quần legging, áo bra, áo tanktop nam/nữ), Đồ tập Yoga/Pilates liền thân, Quần áo chạy bộ cản gió/thoát mồ hôi, Trang phục Athleisure dạo phố.
*   **1.2 Xác định đối tượng**: Tín đồ tập thể hình, huấn luyện viên Gym/Yoga, phụ nữ yêu thích vóc dáng khỏe khoắn, người chạy bộ.
*   **1.3 Output**: Lưu `Planning context` trong `research.md` tại `clients/General-B2B/brands/ICADO/keywords/[keyword-slug]/`.

### 02. RESEARCH
*   **2.1 Search Intent**: So sánh chất liệu đồ tập (Nylon Spandex vs Poly Spandex), cách chọn size đồ tập ôm sát không ngấn mỡ, cách phối đồ đi tập đẹp, cách giặt giữ form.
*   **2.2 Keyword Expansion**: Trích xuất bộ từ khóa công năng (co giãn 4 chiều, cạp cao giấu bụng, nâng mông quả đào, chống lộ viền tam giác).
*   **2.3 Competitor Intelligence**: Cào live DOM Top 3-5 thương hiệu đối thủ qua `browser tool`.
*   **2.4 Output**: `Keyword Strategy Table` & `Competitor Analysis Table`.

### 03. CONTENT STRATEGY
*   **3.1 Content Gap**: Khắc phục các bài viết đối thủ chỉ bán hàng thuần túy mà thiếu kiến thức về giải phẫu học cơ thể và chuyển động cơ bắp khi tập.
*   **3.2 ICADO USP**: Form dáng thiết kế riêng cho tỷ lệ người Việt, đường may flatlock chống cọ xát, công nghệ dệt định hình vóc dáng.
*   **3.3 Output**: Phần `Content strategy` trong `research.md`.

### 04. OUTLINE DEVELOPMENT
*   **4.1 Cấu trúc chuẩn 5-6 H2**:
    1. Tiêu chí lựa chọn đồ tập chuyên dụng cho từng bộ môn thể thao.
    2. Phân tích chất liệu vải dệt công nghệ cao & Bảng so sánh độ bền co giãn.
    3. Bảng chọn size đồ tập chuẩn xác theo số đo 3 vòng và cân nặng.
    4. Gợi ý phối đồ tập thể thao sành điệu & Cách bảo quản đồ tập không bai dão.
    5. ICADO — Thương hiệu đồ tập Gym/Yoga chuẩn form tôn dáng.
    6. FAQ 5 câu hỏi thường gặp.
*   **4.2 Output**: `Outline Candidate Table` trong `outline.md`.

### 05. OUTLINE QA
*   **5.1 Sportswear Ergonomics QA**: Thẩm định độ chính xác các thuật ngữ thể thao và giải pháp cơ học chuyển động.
*   **5.2 Outline Scoring**: Chấm điểm outline ($\ge 80$).
*   **5.3 Output**: `outline-qa-report.md`.

### 06. DUYỆT & KHÓA DÀN Ý (APPROVAL)
*   **6.1 Gửi Brand Team**: Trình duyệt dàn ý với nhóm quản lý nhãn hàng ICADO.
*   **6.2 Khóa outline**: Lock cấu trúc trước khi viết bài.

### 07. ARTICLE WRITING
*   **7.1 Viết bài D2C Sportswear**: Triển khai toàn văn bài viết (1500 - 1800 từ) tràn đầy cảm hứng vận động, hướng dẫn trực quan.
*   **7.2 Tạo Mục lục tự động (TOC & Anchor Links)**: Sử dụng skill `generating-table-of-contents` để tạo khối Mục Lục có liên kết Anchor (`#number_PascalCase_Underscore`) và tự động gắn thuộc tính `id="..."` vào các thẻ Heading H2/H3 tương ứng.
*   **7.3 Output**: `article.md`.

### 08. ARTICLE QA & PUBLISH
*   **8.1 Fact-check & Publish**: Kiểm tra số đo bảng size, tính hoạt động của các liên kết anchor mục lục và xuất bản bài viết lên blog ICADO.

---

## 4. LEVEL 3: EXECUTION (SKILLS, RULES & DATABASES)

### 🛠️ Skills Thực thi
1. `icado-outline-rules`
2. `generating-outlines-icado`
3. `keyword-strategy-mapping` & `keyword-expansion`
4. `competitor-outline-intelligence`
5. `generating-table-of-contents` (Tạo mục lục & gắn Anchor IDs)
6. `research-internal-links` (Nghiên cứu & chèn liên kết nội bộ)
7. `rechecking-facts` & `auditing-content`
8. `outline-quality-scoring` & `client-approval-gate`
9. `writing-semantic-content`

### 🏛️ Foundation & References
*   **Persona**: `data/reference/persona-brand/ICADO/persona-icado-skill.md`
*   **Central Entity**: `data/reference/persona-brand/ICADO/central-entity-ICADO.md`
*   **Source Context**: `data/reference/persona-brand/ICADO/source-context-ICADO.md`
