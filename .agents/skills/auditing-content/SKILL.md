---
name: auditing-content
description: >
  Validates SEO article quality against Outline and Research data.
  Ensures structural compliance, entity coverage, and search intent alignment.
  Triggers: audit content, check article, review draft, /audit-content
---

# Auditing Content

## Purpose
Ensures consistency and quality of the generated article (`article.md`) by cross-referencing it with the Outline (`outline.md`) and Research Data (`research.md`).

## Process

### Phase 1: Input Validation

#### Entry Check
```
IF files exist (article.md AND outline.md AND research.md):
    → Proceed to Phase 2
ELSE:
    → Identify missing file.
    → Ask user to provide or generate the missing artifact.
```

#### Optional Context Check
```
IF `search-intent.md` exists:
    → Load as Intent Baseline.
IF brand context files exist:
    → Activate Phase 3.5 (Brand Audit)
```

### Phase 2: Structural Verification (Outline vs Article)

#### Actions
For each section in `outline.md`:
1.  **Check Existence**: Is the corresponding heading present in `article.md`?
2.  **Evaluate Coverage**: Does the content reflect the outline's intent?
3.  **Note Discrepancies**: Missing sub-headings or "drifted" topics.

#### Output: Structure Check
```markdown
### 1. Structural Audit
| Outline Section | Article Match | Status | Notes |
|-----------------|---------------|--------|-------|
| [H2 Heading] | [Existing H2] | ✅/❌ | [Note coverage quality] |
```

### Phase 3: Semantic Verification (Research vs Article)

#### Actions
For entities in `research.md` (and `search-intent.md` if available):
1.  **Scan Usage**: Are key entities mentioned in `article.md`?
2.  **Context Check**: Are they used naturally?
3.  **Intent Check**:
    *   *Primary Source*: Check against `search-intent.md` (Micro-Intent: Know/Do/Go).
    *   *Secondary Source*: Check against `research.md` clusters (Info/Comm/Trans).
    *   **Verify**: Does the content answer the specific "User Motivation"?

#### Output: Semantic Check
```markdown
### 2. Semantic Audit
- **Primary Entities Used**: [List found]
- **Missing Entities**: [List missing vital entities]
- **Intent Alignment**: [Score 1-10] (Based on `search-intent.md`)
```

### Phase 3.1: Brand-aware compliance checks

#### Actions
You MUST programmatically (using script or strict counting) verify the following:
1. **Keyword coverage**: Confirm that the primary query and relevant secondary queries are answered naturally; apply a numeric density only when the brand standard specifies one.
2. **Readability**: Apply the sentence and paragraph limits from the matching brand standard. If none exists, flag only text that is materially hard to scan.
3. **Typography**: Check headings and formatting against the matching brand standard instead of imposing one house style globally.
4. **Link Rules**: Validate links against the matching brand's approved internal-link source. Do not require Home Credit links or CTA blocks for another brand.
5. **Explanations & Clarity**: Flag wording that is inaccurate, ambiguous, or needlessly ornate; preserve legitimate domain terminology and necessary definitions.

#### Output: Hard Rules Check
```markdown
### 3. Hard Rules Audit
- **Main KW Density**: [Measured %] (Pass/Fail)
- **Formatting Constraint**: [Paragraph length check] (Pass/Fail)
- **Signature CTA**: [Present/Missing link]
- **Explanations & Clarity Audit**: [Pass/Fail] (Checked for metaphors, parenthetical definitions, and common terms over-explanation)
```

### Phase 3.2: Home Credit Strict Audit Checklist (Brand Logic)
Nếu bài viết thuộc dự án Home Credit, bạn **BẮT BUỘC PASS 100%** bộ tiêu chí sau trước khi giao bài:
- [ ] H2 không được đặt dưới dạng câu hỏi trơ trọi. Giọng văn phải Serious & Expert (không từ lóng, hoa mỹ).
- [ ] SEO Metadata: Meta Description phải có CTA chứa bối cảnh thương hiệu (VD: "Tìm hiểu tại thư viện Home Credit ngay"), cấm dùng CTA cụt lủn.
- [ ] Bảng biểu (Tables): Xác nhận mọi bảng biểu (Bảng giá/Thông số) phải có tính diễn giải. Bảng Trả góp mô phỏng dòng tiền CHỈ CÓ 4 CỘT thuần toán học.
- [ ] Điểm chạm Brief: Các yêu cầu bổ sung riêng của khách (Sapo/Kết bài) có bị bỏ quên không?
- [ ] Sapo Logic: Đoạn mở bài đi trực diện từ Pain point -> Solution chưa? Tuyệt đối vắng mặt các Câu Hỏi Tu Từ ("Vậy X là gì?").
- [ ] Fluff & Filler: Quét sạch câu cảm thán. Diệt từ vựng "đao to búa lớn" (sóng gió, tuyệt tác, điều phối dư địa...).
- [ ] Formatting Text: Câu <= 25 chữ, đoạn <= 3 dòng. Danh sách liệt kê nếu có dấu `.` ở tận cùng câu (ngoại trừ dòng chốt cuối cùng) -> LẬP TỨC XÓA BỎ.
- [ ] Bullet Formatting (Descriptive): Các list có dấu `:` bắt buộc In đậm vế trước, và Viết hoa chữ đầu tiên của vế sau.
- [ ] Keywords & Links: Điểm danh đủ mặt các KW phụ. Mọi dịch vụ được nhắc đến trong đoạn Service Matching H2 phải cắm Link Exact Match.
- [ ] Service Matching Prompts: Mục quảng bá dịch vụ đã gộp đủ 3 tầng H3 (Điều kiện & Thủ tục, Các bước thực hiện, Bảng dự toán) chưa.

### Phase 3.5: Brand & Context Validation (Conditional)

#### Actions
*Only runs if context files are present.*
1.  **Vertical Check**: Does it stick to the domain defined in `source-context`?
2.  **Entity Check**: Are contact details/services consistent with `central-entity`?
3.  **Voice Check**: Does it sound like the defined persona?

### Phase 4: Reporting & Recommendations

#### Output Generation
Generate `audit-report.md`:
1.  **Summary Score** (1-10)
2.  **Critical Issues List**
3.  **Actionable Recommendations** (Specific additions, not generic advice)

## Self-Check (Read before auditing)

□ Did I actually read the content of all 3 files?
  → Don't guess based on filenames.

□ Am I being fair about heading variations?
  → If "Introduction" became "Getting Started", that's a match if content aligns.

□ Is the Semantic Check strict on "Entities"?
  → Ensure key terms from research are actually present contextually.

□ Are recommendations actionable?
  → "Add a paragraph about X in section Y" > "Make it better".
