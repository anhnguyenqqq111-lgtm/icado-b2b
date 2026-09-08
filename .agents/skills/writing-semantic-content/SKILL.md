---
name: writing-semantic-content
description: >
  Guides the writing process for Semantic SEO content, focusing on entity injection and search intent depth.
  Triggers: write article, viet bai, viet content, /write-content
---

# Writing Semantic Content

## Purpose
Guides the drafting of content that is optimized for **Semantic Search** and **Search Intent**, ensuring adherence to the standard outline structure for maximum Topical Authority.

## Process

### Phase 1: Preparation (Context & Strategy)

#### Entry Check
```
IF Outline exists AND Entities are defined:
    → Proceed to Phase 2
ELSE:
    → Stop. Require Outline and Entity list before writing.
```

#### Core Context
Define before writing:
1.  **Role**: Pillar Page (Broad) vs Cluster Page (Specific).
2.  **Audience**: Level of expertise required.
3.  **Tone & Benchmark**: Read and analyze the golden standard sample article located in `data/reference/persona-brand/[Brand]/standards/` to absorb the exact voice, flow, sentence length, and structure before drafting. Use this sample as a benchmark to compare with the completed article.

### Phase 2: Entity Injection System

#### Requirement
Instead of keyword stuffing, use the **Entity System**:
*   **Primary Entity**: Mention in Title, H1, Intro (First 100 words), and Conclusion.
*   **Related Entities**: Inject naturally into relevant H2/H3 sections.
    *   *Person*: Mention experts for credibility.
    *   *Concept*: Define terms clearly.

### Phase 3: Drafting (The 6-Part Standard)

Follow the structure strictly:

**I. Intro (Sapo)**: 
*   **Direct & Affirmative**: State exactly what the entity/topic is and its main value proposition immediately in the first sentence (e.g., "X là loại tài sản/khoản vay phổ biến, được quan tâm bởi ưu điểm Y...").
*   **NO Rhetorical Questions**: NEVER write assumptions or conversational questions aimed at the reader (e.g., "Bạn có biết X là gì không?", "Vậy X khác Y như thế nào?", "Mức giá mới nhất là bao nhiêu? Chúng ta cùng tìm hiểu..."). This cheapens the authority of the content.
*   **Hook + Value**: Integrate the main keywords naturally into these objective statements.
**II. Body**:
*   Break down into **Query Clusters** (H2s).
*   **Rule**: Each section must answer a specific user question (What, How, Which).
**III. Expansion**: Compare (Vs) or Warn (Mistakes).
**IV. FAQ**: Short, snippet-optimized answers.
**V. Conclusion**: Recap + Internal Links.

#### Writing Rules (Crucial)
1.  **Sentence Case Headings**: Only capitalize the **first letter** of the sentence and **proper nouns**.
    *   **Bad**: "Cách Làm Bánh Tiramisu Ngon" (Title Case - English Style).
    *   **Good**: "Cách làm bánh tiramisu ngon" (Sentence Case - Vietnamese Style).
    *   **Strict Rule**: Never capitalize every word in a heading.
2.  **H3 Subheading Enforcement (No Walls of Text)**: 
    *   If an H2 section is longer than 200-300 words or covers multiple distinct points (e.g., benefits, factors, risks), you **MUST** break it down into `###` (H3) subheadings. 
    *   Do not write 4-5 long paragraphs consecutively under a single H2. Use H3s to label each specific point (e.g., `### 1. Công suất động cơ`, `### 2. Chất liệu dao băm`).
5.  **NO Nested Bullets**: Do not nest lists deeper than 1 level. Keep it flat.
6.  **Bullet List Formatting (Critical)**: When creating a descriptive bullet list with a colon (:), you MUST bold the text before the colon and MUST capitalize the first letter of the word immediately following the colon (e.g., `- **Giá vàng:** Khi giá tăng...`, DO NOT write `- **Giá vàng:** khi giá...`).
4.  **Length**: Follow the approved outline and the matching brand standard. Do not pad an article to meet an arbitrary word count.
5.  **Language**: Write in 100% Vietnamese. Do NOT use English words unless they are unavoidable technical terms (check with User first) or standard abbreviations (e.g., ISO, HACCP). Translate terms like "Labeling" to "Ghi nhãn".
6.  **Professional Tone**: No "Hey guys", no empty adjectives ("very", "extremely").
7.  **Short Paragraph Rule (UX & Readability)**:
    *   **Strict Limit**: Single paragraphs should NOT exceed **4 lines** in the editor.
    *   **Action**: Break down complex ideas into 2-3 shorter paragraphs or use bullet points to avoid "walls of text" that discourage readers.
8.  **No Metaphors & Direct Explanations (Strict Clarity)**:
    *   **No Metaphors**: Do NOT use metaphorical or figurative language to describe business or technical concepts. Explain them simply and directly for the reader.
    *   **No Parentheses or Quotes for Definitions**: Minimize the use of parentheses `()` or quotation marks `""` to define or translate terms. Explain them directly in the flow of the text (e.g., instead of writing "chỉ mục (indexing)", write "chỉ mục là quá trình...").
    *   **Common Terms**: If a term is already widely known (e.g., SEO, Website, Google, AI), do not explain or define it at all to keep the text concise.
9.  **Keyword use**:
    *   Cover the primary query and the relevant secondary queries naturally.
    *   Use entities from `research.md` where they improve the answer; do not insert a term solely to satisfy a count.
    *   Apply a numeric density target only when the matching brand standard explicitly requires one.

### Phase 4: Self-Correction

As you write, check:
*   **Entity Density**: Are we talking about the *concepts* or just the keyword?
*   **Contextual Linking**: Do anchors describe the destination? Use the matching brand's approved internal-link source when one exists.
*   **Terminology**: Use standard industry terms (e.g., "Standard Document", "Manual") instead of metaphors.

## Self-Check (Read before outputting)

□ Does the draft follow the approved scope and brand-specific length guidance?
  → Expand only when a section remains incomplete for the reader's intent.

□ Are headings in Sentence case (no Title Case)?
  → Check every H2 and H3.

□ Did I avoid numbering the headings?
  → "Introduction", not "1. Introduction".

□ Are entities mentioned naturally?
  → Don't force them; if an entity doesn't fit, don't use it.
