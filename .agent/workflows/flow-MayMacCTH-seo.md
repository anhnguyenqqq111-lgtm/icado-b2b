# May Mặc CTH — Full B2B Local SEO & Content Workflow Pipeline

Workflow sản xuất nội dung chuyên sâu cho **May Mặc CTH — Xưởng may đồng phục Hải Phòng** (maymaccth.com) chuẩn hóa theo kiến trúc FigJam 3 Cấp độ (3-Level Architecture) kết hợp Cổng kiểm soát chất lượng (Gates & Feedback Loops).

**Lệnh kích hoạt:** `/flow-MayMacCTH-seo [keyword chính] [keyword phụ 1] [keyword phụ 2] ...`

---

## 1. LEVEL 1: HIGH-LEVEL WORKFLOW (WHAT) — 8 ĐẦU VIỆC LỚN

Sơ đồ luồng tổng thể 8 Workstreams và đầu ra tương ứng:

```mermaid
graph LR
    classDef workstream fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#fff;
    classDef output fill:#1f2937,stroke:#6b7280,stroke-width:1px,color:#93c5fd;

    W1["01. PLANNING<br><i>Xác định dòng sản phẩm may, chất liệu, tệp B2B KCN</i>"]:::workstream
    W2["02. RESEARCH<br><i>Thu thập thông số vải, bảng size, giá đối thủ</i>"]:::workstream
    W3["03. CONTENT STRATEGY<br><i>Tìm khoảng trống kỹ thuật, góc giá xưởng & Local KCN</i>"]:::workstream
    W4["04. OUTLINE DEV<br><i>Xây dựng cấu trúc outline, bảng size, bảng giá xưởng</i>"]:::workstream
    W5["05. OUTLINE QA<br><i>Kiểm tra chuẩn xác thông số dệt may & tín hiệu Local</i>"]:::workstream
    W6["06. CLIENT APPROVAL<br><i>Gửi outline xưởng duyệt, nhận feedback, khóa outline</i>"]:::workstream
    W7["07. ARTICLE WRITING<br><i>Viết bài B2B xưởng may thực chiến, tư vấn may mẫu</i>"]:::workstream
    W8["08. ARTICLE QA & PUBLISH<br><i>Fact-check bảng giá/size, tối ưu Local & xuất bản</i>"]:::workstream

    O1["📄 B2B Manufacturing Brief"]:::output
    O2["📦 Fabric & Competitor Bundle"]:::output
    O3["📐 Local & Pricing Strategy"]:::output
    O4["📑 CTH Outline Candidate"]:::output
    O5["📊 QA Report & Score"]:::output
    O6["🔒 Approved Outline (Locked)"]:::output
    O7["📝 B2B Article Draft"]:::output
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

    G1{"Planning Gate<br>Xác nhận loại áo & tệp khách B2B?"}:::gate
    G2{"Research Gate<br>Dữ liệu vải & bảng size đầy đủ?"}:::gate
    G3{"Strategy Gate<br>Lợi thế giá xưởng & Local rõ ràng?"}:::gate
    G4{"Outline Gate<br>Bảng dàn ý đạt chuẩn 8 cột bullet?"}:::gate
    G5{"QA Gate<br>Score ≥ 80 & Thông số vải chuẩn?"}:::gate
    G6{"Approval Gate<br>Xưởng duyệt & Khóa dàn ý?"}:::gate
    G7{"Writing Gate<br>Viết chuẩn xác 100% cấu trúc đã khóa?"}:::gate
    G8{"Final Gate<br>Fact-check size/giá & Local PASS?"}:::gate

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
    G6 -- "Đổi dòng vải/chiến lược" --> S3

    S7 --> G7
    G7 -- Yes --> S8["08. Article QA & Publish"]:::step
    G7 -- "Lệch outline" --> S7

    S8 --> G8
    G8 -- "PASS (100%)" --> DONE["🚀 Xuất bản (Publish)"]:::pass
    G8 -- "Chưa đạt chuẩn" --> S7
```

---

## 3. LEVEL 2: LOW-LEVEL WORKFLOW (HOW) — CHI TIẾT TỪNG ĐẦU VIỆC

### 01. PLANNING
*   **1.1 Xác định sản phẩm**: Áo thun polo đồng phục, áo sơ mi công sở, đồ bảo hộ lao động nhà máy, đồng phục nhà hàng/spa, áo khoác gió.
*   **1.2 Xác định đối tượng**: Doanh nghiệp tại các KCN Hải Phòng (VSIP, Đình Vũ, Tràng Duệ, Nomura...), các cơ quan trường học tại miền Bắc.
*   **1.3 Output**: Lưu `Planning context` trong `research.md` tại `clients/MayMacCTH/brands/MayMacCTH/keywords/[keyword-slug]/`.

### 02. RESEARCH
*   **2.1 Search Intent**: So sánh chất liệu vải, tra cứu bảng giá may sỉ, bảng size chuẩn, cách bảo quản hình in/thêu.
*   **2.2 Keyword Expansion**: Bộ từ khóa kèm định vị địa phương (Hải Phòng, Miền Bắc, KCN) và từ khóa chất liệu (Cotton 65/35, Poly Thái, Kaki Pangrim...).
*   **2.3 Competitor Intelligence**: Cào live DOM Top 3-5 xưởng may đối thủ qua `browser tool`.
*   **2.4 Output**: `Keyword Strategy Table` & `Competitor Analysis Table`.

### 03. CONTENT STRATEGY
*   **3.1 Content Gap**: Khắc phục các bài viết đối thủ thiếu bảng thông số vải rõ ràng hoặc giấu bảng giá xưởng.
*   **3.2 Local & USP**: Định vị May Mặc CTH có xưởng sản xuất trực tiếp tại Hải Phòng, hỗ trợ gửi mẫu vải tận nơi miễn phí.
*   **3.3 Output**: Phần `Content strategy` trong `research.md`.

### 04. OUTLINE DEVELOPMENT
*   **4.1 Cấu trúc chuẩn 5-6 H2**:
    1. Tổng quan phân khúc & tiêu chuẩn sản phẩm đồng phục.
    2. Bảng so sánh chi tiết các chất liệu vải may phù hợp nhất.
    3. Bảng thông số chọn size áo chuẩn form người Việt.
    4. Bảng báo giá may tận xưởng & các yếu tố ảnh hưởng đến giá thành.
    5. Xưởng May Đồng Phục CTH — Địa chỉ may uy tín tại Hải Phòng.
    6. FAQ 5 câu hỏi thường gặp.
*   **4.2 Output**: `Outline Candidate Table` trong `outline.md`.

### 05. OUTLINE QA
*   **5.1 Fabric & Local QA**: Thẩm định tên gọi chất liệu, tỷ lệ dệt, mật độ từ khóa Local Hải Phòng.
*   **5.2 Outline Scoring**: Chấm điểm outline ($\ge 80$).
*   **5.3 Output**: `outline-qa-report.md`.

### 06. DUYỆT & KHÓA DÀN Ý (APPROVAL)
*   **6.1 Gửi xưởng**: Trình duyệt dàn ý với ban quản lý xưởng may CTH.
*   **6.2 Khóa outline**: Lock cấu trúc trước khi viết bài.

### 07. ARTICLE WRITING
*   **7.1 Viết bài B2B**: Triển khai toàn văn bài viết (1600 - 2200 từ), lồng ghép bảng biểu và hướng dẫn chọn mẫu vải trực quan.
*   **7.2 Output**: `article.md`.

### 08. ARTICLE QA & PUBLISH
*   **8.1 Fact-check & Publish**: Kiểm tra số đo bảng size, công thức báo giá may sỉ, bàn giao bài viết cho CMS May Mặc CTH.

---

## 4. LEVEL 3: EXECUTION (SKILLS, RULES & DATABASES)

### 🛠️ Skills Thực thi
1. `maymaccth-outline-rules`
2. `generating-outlines-maymaccth`
3. `keyword-strategy-mapping` & `keyword-expansion`
4. `competitor-outline-intelligence`
5. `rechecking-facts` & `auditing-content`
6. `outline-quality-scoring` & `client-approval-gate`
7. `writing-semantic-content`

### 🏛️ Foundation & References
*   **Content Rules**: `data/reference/persona-brand/MayMacCTH/content-rules.md`
*   **Central Entity**: `data/reference/persona-brand/MayMacCTH/central-entity-MayMacCTH.md`
*   **Topic Clusters**: `data/reference/persona-brand/MayMacCTH/topic-clusters.md`
*   **Internal Links**: `data/reference/persona-brand/MayMacCTH/internal-links.md`
