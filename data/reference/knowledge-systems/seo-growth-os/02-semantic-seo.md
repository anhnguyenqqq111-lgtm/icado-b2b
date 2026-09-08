# 02. Semantic SEO: playbook triển khai từ dữ liệu đến topical authority

## 0. Semantic SEO là gì trong hệ thống này?

Semantic SEO là cách tổ chức website để người dùng, search engine và answer engine hiểu cùng một hệ thống:

```text
Entity → thuộc tính → quan hệ → nhu cầu → truy vấn → nội dung → bằng chứng → hành động
```

Không tối ưu bằng cách gom thật nhiều từ đồng nghĩa. Một hệ thống semantic tốt phải trả lời được bốn câu hỏi:

1. Doanh nghiệp nói về chủ đề nào và có quyền nói ở khía cạnh nào?
2. Người dùng đang cố hoàn thành công việc gì ở mỗi giai đoạn?
3. Trang nào là nguồn trả lời chính cho từng nhóm nhu cầu?
4. Bằng chứng nào làm câu trả lời đáng tin và dẫn tới chuyển đổi?

## 1. Đầu vào và đầu ra bắt buộc

### Đầu vào

Trước khi nghiên cứu keyword, thu thập tối thiểu:

| Nhóm dữ liệu | Cần lấy | Nguồn nội bộ phù hợp |
|---|---|---|
| Business | mục tiêu doanh thu, biên lợi nhuận, thị trường, năng lực cung ứng | business brief, CRM, Sales/Operations |
| Audience | segment, role, job-to-be-done, nỗi sợ, tiêu chí mua | persona, phỏng vấn Sales, lost reason |
| Offer | sản phẩm/dịch vụ, điều kiện, giá, SLA, giới hạn | product/service owner |
| Search | query, SERP, GSC, competitor pages, PAA | GSC, SERP, competitor research |
| Authority | tác giả, case, chứng chỉ, ảnh thật, dữ liệu, đối tác | brand reference, source register |
| Technical | URL inventory, indexation, canonical, template, internal links | crawl, GSC, CMS/dev |

### Đầu ra

Một project semantic hoàn chỉnh cần có:

1. Entity map và relationship map.
2. Query map có intent, funnel stage, priority và target URL.
3. Topical map: pillar, sub-pillar, cluster, money page, proof asset.
4. Content brief cho từng URL.
5. Internal-link map và orphan-page report.
6. Claim/evidence matrix.
7. Publish QA và measurement plan.

## 2. Quy trình 10 bước

### Bước 1 - Chốt business boundary

Viết một câu định vị theo mẫu:

`[Brand] giúp [segment] giải quyết [job/problem] bằng [offer/capability] tại [market], với [proof/constraint].`

Sau đó tạo bảng boundary:

| Câu hỏi | Ví dụ cần chốt |
|---|---|
| Phục vụ ai? | SME, R&D, procurement, khách du lịch, người vay |
| Phục vụ ở đâu? | Hải Phòng, Việt Nam, quốc tế |
| Cung cấp gì? | sản phẩm, dịch vụ, tư vấn, công cụ |
| Không cung cấp gì? | loại đơn, khu vực, tiêu chuẩn ngoài năng lực |
| Kết quả kinh doanh? | quote, sample, booking, application, repeat order |

Nếu chưa chốt boundary, không mở rộng topical map. Chủ đề rộng nhưng không liên quan dễ tạo traffic không có giá trị và làm loãng topical focus.

### Bước 2 - Lập entity inventory

#### 2.1. Thu thập entity

Tìm entity từ năm lớp dữ liệu:

1. First-party: product catalog, CRM, SOP, sales call, FAQ, case.
2. SERP: autocomplete, PAA, related searches, knowledge panel, image refinements.
3. Competitor: heading, filter, comparison criteria, terminology, missing proof.
4. Industry: tiêu chuẩn, hiệp hội, cơ quan quản lý, báo cáo, tài liệu kỹ thuật.
5. Community: câu hỏi thực tế trên forum, comment, YouTube, social hoặc support ticket.

#### 2.2. Phân loại entity

| Loại | Cần ghi | Câu hỏi kiểm tra |
|---|---|---|
| Organization/brand | tên, vai trò, thị trường | Ai có năng lực thật? |
| Person/role | người dùng, người ảnh hưởng, người duyệt | Ai tìm, ai dùng, ai trả tiền? |
| Place | địa bàn, tuyến, khu vực, local modifier | Địa điểm làm thay đổi nhu cầu thế nào? |
| Product/service | loại, biến thể, use case | Cung cấp gì và giới hạn gì? |
| Concept | định nghĩa, tiêu chuẩn, thuật ngữ liên quan | Người mới cần hiểu khái niệm nào? |
| Attribute | giá, kích thước, vật liệu, tính năng, điều kiện | Thuộc tính nào ảnh hưởng quyết định? |
| Process | bước, hồ sơ, thời gian, SLA | Khách cần làm gì tiếp theo? |
| Evidence | case, ảnh, dữ liệu, review, chứng chỉ | Claim nào có bằng chứng gốc? |
| Time/event | năm, mùa vụ, cập nhật, chu kỳ mua | Claim nào cần refresh? |

#### 2.3. Ghi relationship

Không chỉ lập danh sách entity. Ghi quan hệ bằng động từ rõ ràng:

| Quan hệ | Ví dụ |
|---|---|
| is-a | Semantic SEO là một phương pháp SEO |
| part-of | entity extraction là một phần của semantic research |
| used-for | schema giúp mô tả loại nội dung |
| serves | dịch vụ phục vụ một segment/khu vực |
| requires | quy trình yêu cầu hồ sơ/điều kiện |
| compared-with | sản phẩm A so với B theo tiêu chí X |
| proven-by | claim được chứng minh bằng case/dataset |
| leads-to | bài giải thích dẫn tới trang giải pháp |

#### 2.4. Entity score

Chấm 0–3 cho mỗi entity:

`Relevance × Business value × Evidence strength × Freshness`.

Entity điểm cao phải xuất hiện ở trang phù hợp; entity điểm thấp chỉ giữ khi giúp hiểu chủ đề hoặc phục vụ một query cụ thể. Không đưa mọi entity vào mọi bài.

### Bước 3 - Phân tích search intent

Tách ba lớp intent:

1. **Macro intent**: informational, commercial investigation, transactional, navigational.
2. **Micro-intent**: definition, process, comparison, cost, problem/fix, local, provider, eligibility, risk, maintenance.
3. **Journey state**: problem aware, solution aware, provider aware, decision, retention.

| Tín hiệu query | Micro-intent | Trang nên dùng |
|---|---|---|
| là gì, nghĩa là gì | definition | glossary/guide hoặc pillar |
| cách, quy trình, thủ tục | process | how-to/checklist |
| so sánh, vs, nên chọn | comparison | comparison/selector |
| giá, chi phí, báo giá | cost/decision | pricing/service/product |
| lỗi, không hoạt động, khắc phục | problem/fix | troubleshooting/support |
| ở đâu, gần đây, tại [địa phương] | local/provider | local landing/provider page |
| mua, đặt, đăng ký, nhận tư vấn | transactional | money page/form |

#### Cách xác nhận intent bằng SERP

Với mỗi query chính:

1. Ghi ngày, quốc gia, ngôn ngữ, thiết bị và location.
2. Ghi loại kết quả: product page, guide, video, local pack, forum, PAA, AI feature.
3. Lấy 5–10 kết quả đầu và phân loại mục đích thực tế của từng URL.
4. Ghi format, độ sâu, proof, CTA và gap của kết quả hiện có.
5. Chọn intent chiếm ưu thế; ghi intent phụ nếu SERP mixed.
6. Nếu một query có hai intent không thể phục vụ tốt trên cùng URL, tách URL hoặc chọn một intent theo business priority.

Không dùng volume để phủ quyết SERP intent. Query volume cao nhưng sai intent thường tạo traffic kém chất lượng.

### Bước 4 - Thu thập và phân cụm query

#### 4.1. Nguồn query

- GSC: query thật, URL đang nhận impression/click, CTR thấp, query chưa có URL tốt.
- SERP: autocomplete, PAA, related search, filters, image/video refinements.
- Website/CRM: site search, form question, sales objection, lost reason, support ticket.
- Competitor: heading, navigation, glossary, comparison, category/filter.
- Industry/community: thuật ngữ chuyên môn và cách khách hàng nói đời thường.

#### 4.2. Chuẩn hóa

Trước khi cluster, chuẩn hóa:

- viết thường, bỏ khoảng trắng thừa và ký tự không cần thiết;
- giữ lại biến thể địa phương, ngôn ngữ và spelling nếu có intent khác;
- tách brand/non-brand, product/service, question/commercial;
- đánh dấu query có năm, giá, quy định hoặc thông số để fact-check/refresh;
- không gộp hai query chỉ vì có cùng từ khóa nếu khác job-to-be-done.

#### 4.3. Cluster theo facet trước, theo keyword sau

```text
Topic
├── Definition: là gì, ý nghĩa, phân loại
├── Process: cách làm, quy trình, thủ tục
├── Problem: lỗi, rủi ro, xử lý
├── Comparison: A vs B, ưu nhược điểm, nên chọn
├── Cost: giá, chi phí, ROI, ngân sách
├── Use case: theo ngành, đối tượng, địa điểm
├── Provider: nhà cung cấp, dịch vụ, báo giá
└── Retention: bảo trì, sử dụng, mua lại, nâng cấp
```

Một cluster chỉ nên có một **dominant intent** và một **target URL**. Query phụ cùng câu trả lời có thể nằm chung; query cần format, proof hoặc CTA khác nên tách trang.

#### 4.4. Query map thực thi

| Query | Facet | Macro intent | Micro-intent | Journey | SERP format | Target URL | Priority | Evidence |
|---|---|---|---|---|---|---|---|---|
| [query] | [facet] | [type] | [type] | [stage] | [format] | [/url] | P1/P2/P3 | [source] |

Priority có thể tính:

`Priority = Business fit × Intent strength × Evidence opportunity × SERP opportunity ÷ Effort`.

Chấm 1–5; ghi lý do, không trình bày điểm như dữ liệu khách quan tuyệt đối.

### Bước 5 - Thiết kế topical map và URL ownership

#### 5.1. Chọn pillar

Pillar là trang bao quát một chủ đề có vai trò kinh doanh hoặc authority rõ ràng. Nó không nhất thiết là query có volume cao nhất.

Pillar tốt có:

- định nghĩa và phạm vi;
- các nhóm entity/thuộc tính chính;
- điều hướng tới cluster;
- liên kết tới solution/money page;
- proof và author phù hợp;
- lý do để được cập nhật định kỳ.

#### 5.2. Chọn cluster

Tạo cluster khi có ít nhất một điều kiện:

- query có intent khác pillar;
- cần format khác, ví dụ calculator, comparison, local page;
- có audience/use case khác;
- cần proof hoặc CTA riêng;
- nội dung quá dài khiến người dùng khó hoàn thành task;
- có giá trị business đủ lớn để đo riêng.

Không tạo cluster chỉ vì thêm một keyword gần nghĩa.

#### 5.3. URL ownership matrix

| URL | Vai trò | Intent chính | Query sở hữu | Entity chính | CTA | KPI | Canonical decision |
|---|---|---|---|---|---|---|---|
| /topic/ | pillar | broad informational | nhóm definition | topic/entity | xem cluster | visibility/assisted | canonical |
| /topic/problem/ | problem cluster | informational | lỗi/rủi ro | problem/process | xem giải pháp | engaged/key event | độc lập |
| /service/ | money page | transactional | provider/price | brand/offer | quote/contact | qualified lead | độc lập |

### Bước 6 - Thiết kế content brief và information gain

#### 6.1. Brief tối thiểu

```markdown
Business role:
Target audience/role:
Job-to-be-done:
Primary query + dominant intent:
Secondary queries:
Entities and relationships:
Questions to answer:
Original evidence/data:
Competitive gap:
Required sections:
Internal links in/out:
CTA and qualification:
Primary/guardrail KPI:
Owner/reviewer/freshness date:
```

#### 6.2. Viết theo information gain

Mỗi bài cần thêm ít nhất một lớp giá trị mà đối thủ chưa làm tốt:

- dữ liệu first-party hoặc quy trình quan sát được;
- ví dụ theo thị trường/ngành/ngữ cảnh cụ thể;
- decision criteria và giới hạn áp dụng;
- bảng so sánh có nguồn;
- template, calculator, checklist hoặc diagnostic;
- góc nhìn chuyên gia có author và trách nhiệm rõ.

Không coi độ dài, số keyword hoặc paraphrase đối thủ là information gain.

#### 6.3. Cấu trúc answer-first

```text
H1 = topic + audience/outcome
Mở bài = trả lời intent chính + phạm vi + điều kiện
Key takeaway = 3–7 kết luận có thể kiểm tra
H2 = các facet/micro-intent lớn
H3 = thuộc tính, quy trình, ví dụ, ngoại lệ
Proof block = source/case/data/author
Decision block = khi nào nên/không nên chọn
CTA = hành động kế tiếp đúng funnel stage
```

### Bước 7 - Xây internal-link graph

#### 7.1. Ba hướng link

```text
Pillar → cluster: điều hướng xuống chi tiết
Cluster → pillar: trả người đọc về bức tranh tổng thể
Cluster ↔ cluster: nối các bước liên quan trong cùng journey
Content → money page: chuyển từ hiểu vấn đề sang giải pháp
Proof → money page: chuyển từ tin tưởng sang hành động
```

#### 7.2. Quy tắc chọn link

Mỗi link phải trả lời: “Người đọc vừa đọc đoạn này sẽ cần biết gì tiếp theo?”

Kiểm tra:

- anchor tồn tại nguyên văn trong nội dung;
- anchor mô tả đúng destination, không tối ưu quá đà;
- destination bổ sung ý nghĩa cho context;
- không tự link về chính trang hiện tại;
- không lặp destination/anchor quá mức;
- page quan trọng có cả link in và link out;
- link được gắn vào câu có chủ đề liên quan, không gom thành danh sách cuối bài.

#### 7.3. Link plan

| Source URL | Exact anchor/context | Destination | Relation | Funnel movement | Priority | Validation |
|---|---|---|---|---|---|---|

Đối với pipeline tự động, tách rõ suggestion, validation và editorial approval. Không publish hàng loạt nếu chưa kiểm tra anchor, relevance, status code và diversity.

### Bước 8 - Triển khai on-page và technical semantics

#### On-page

- title/H1 nói rõ entity, task hoặc outcome;
- heading phản ánh query facet, không đặt heading chỉ để chứa keyword;
- đoạn đầu trả lời câu hỏi chính;
- bảng dùng cho so sánh, thông số, điều kiện;
- hình ảnh có alt mô tả đúng nội dung, không nhồi keyword;
- author, reviewer, date, source và update note hiển thị khi phù hợp;
- CTA và related links theo journey.

#### Technical

- một URL có một vai trò/canonical rõ;
- crawlable, indexable, status code và sitemap đúng;
- breadcrumb/structured data mô tả đúng nội dung hiển thị;
- HTML semantic, heading hierarchy và link có thể đọc được;
- không dùng schema để khai báo điều không có trên trang;
- kiểm tra mobile, tốc độ, accessibility và form event;
- xử lý duplicate, faceted navigation, pagination, redirects và orphan pages.

Technical semantics làm công cụ hiểu nội dung dễ hơn; không thay thế nội dung, authority hoặc proof.

### Bước 9 - QA semantic trước publish

#### Coverage checklist

- [ ] Intent chính được trả lời ngay đầu bài.
- [ ] Các entity chính và quan hệ quan trọng đã có.
- [ ] Có thuộc tính, điều kiện, ngoại lệ và giới hạn.
- [ ] Mỗi H2 tương ứng một câu hỏi/facet, không trùng với URL khác.
- [ ] Có information gain cụ thể.
- [ ] Query phụ xuất hiện tự nhiên trong phần giải thích phù hợp.
- [ ] Claim định lượng có source, scope, date và owner.
- [ ] Brand/service/CTA đúng capability reference.

#### Architecture checklist

- [ ] URL có owner và dominant intent.
- [ ] Có link pillar ↔ cluster.
- [ ] Có link tới money page hoặc next action khi phù hợp.
- [ ] Không orphan, cannibalization hoặc redirect chain chưa xử lý.
- [ ] Internal-link anchor/context/destination đã validate.

#### Experience checklist

- [ ] Format đúng SERP và task người dùng.
- [ ] Có bảng/checklist/calculator/visual nếu task cần.
- [ ] CTA vừa với funnel stage.
- [ ] Mobile, readability, accessibility và form hoạt động.

### Bước 10 - Đo lường và refresh

Theo dõi theo URL, cluster và intent, không chỉ tổng domain:

| Giai đoạn | Tín hiệu | Quyết định |
|---|---|---|
| 0–28 ngày | index, crawl, impressions, query coverage | lỗi kỹ thuật hoặc mismatch ban đầu |
| 29–90 ngày | clicks, CTR, ranking distribution, engagement | title/format/intent/internal links |
| 90+ ngày | key events, qualified lead, quote/win, assisted path | giữ, mở rộng, CRO hoặc dừng |
| Theo quý | query drift, SERP change, claim freshness, cannibalization | consolidate, split, refresh, redirect |

#### Refresh trigger

- query mới xuất hiện nhưng bài chưa trả lời;
- impression tăng nhưng CTR thấp;
- click tăng nhưng engagement/lead thấp;
- SERP format thay đổi;
- giá, luật, thông số, tên sản phẩm hoặc địa điểm thay đổi;
- competitor có proof/góc nhìn mới;
- claim thiếu nguồn hoặc đã quá hạn xác minh.

Refresh phải ghi rõ: thay đổi gì, vì sao, nguồn nào, ngày nào, KPI nào sẽ quan sát. Chỉ đổi ngày publish mà không cải thiện nội dung không phải refresh.

## 3. Ví dụ rút gọn: cluster B2B may đồng phục

```text
Business outcome: qualified quote tại Hải Phòng
  → Pillar: đồng phục doanh nghiệp
      → Cluster: chọn chất liệu theo môi trường làm việc
      → Cluster: đồng phục cho nhà máy/KCN
      → Cluster: quy trình đặt may và duyệt mẫu
      → Money page: nhận may đồng phục doanh nghiệp Hải Phòng
      → Proof: ảnh mẫu, năng lực, case đã xác minh
```

Mỗi cluster có role khác nhau: bài chất liệu giải thích và hỗ trợ quyết định; bài KCN giải quyết use case/local; quy trình giảm risk; money page nhận brief và qualification. Không gộp tất cả vào một bài dài nếu người đọc cần hành động và bằng chứng khác nhau.

## 4. Các lỗi thường gặp

| Lỗi | Nguyên nhân | Cách sửa |
|---|---|---|
| Gọi danh sách keyword là semantic map | chưa có entity/relationship/URL owner | thêm entity map và journey |
| Mỗi biến thể query tạo một bài | nhầm coverage với số lượng | cluster theo intent/facet |
| Pillar quá rộng, không có next action | ưu tiên volume hơn business | thêm boundary, proof, CTA và cluster |
| Bài có đủ keyword nhưng không có proof | content-first, thiếu capability data | tạo evidence matrix và reviewer |
| Internal link hàng loạt | tối ưu số link | kiểm tra context, anchor và destination |
| Traffic tăng nhưng lead giảm | sai audience/offer hoặc form friction | nối GSC → GA4 → CRM và diagnosis theo funnel |
| Có nhiều AI mention nhưng không có citation | prompt sample nhỏ hoặc content thiếu evidence | tách metric, cải thiện source/claim/structure và đo lại |

## 5. Bộ artifact nên lưu cho mỗi topic

```text
topic.toml
├── search-intent.md          # SERP, macro/micro intent, format
├── research.md               # entities, query map, sources, gaps
├── competitor-insights.md    # structure, proof, differentiation
├── outline.md                # hierarchy, sections, CTA, links
├── fact-check-report.md      # claim/source/status nếu workflow yêu cầu
├── article.md                # nội dung triển khai
└── audit-report.md           # semantic, technical, UX, conversion QA
```

Knowledge OS là lớp phương pháp chung; các topic vẫn phải tuân thủ `workspace.toml`, brand reference và workflow tương ứng.

## 6. Template kiểm tra nhanh trước khi bắt đầu

```markdown
Topic:
Audience/role:
Business goal:
Target market/location:
Offer/capability boundary:
Primary entity:
Top 5 supporting entities:
Dominant intent:
Journey stage:
Target URL:
Pillar or cluster:
Information gain:
Required evidence:
Primary CTA:
Primary KPI:
Reviewer:
Refresh date:
```
