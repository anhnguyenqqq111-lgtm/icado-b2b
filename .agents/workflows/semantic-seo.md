---
description: Automated Semantic SEO Content Creation Process (Research -> Outline -> Article)
---

# Semantic SEO Workflow

This workflow automates the creation of high-quality SEO content based on the Semantic SEO methodology.

**Command:** `/semantic-seo [keyword]`

**Global Quality Rules:**
7. **Sapo Rules**: Sapo MUST naturally contain the primary keyword and at least one secondary keyword in the first 3 sentences.
8. **No AI Flair Words**: CẤM SỬ DỤNG từ ngữ hoa mỹ do AI tự chế (ví dụ: vòng tuần hoàn, luân hồi, trầm trọng, lấp liếm, hứa hẹn, cỗ máy, siêu việt). Keep tone 100% Serious & Expert.
9. **Structured CTA**: The service promotion block (Lead Generation) MUST strictly contain structured H3s explaining Conditions, Procedures, Steps, and Benefits distinctly.
10. **Grammar & Word Count**: Ưu tiên cao nhất cho văn phong tự nhiên đúng ngữ pháp tiếng Việt. Tuyệt đối không ép chữ hay gọt văn bản một cách máy móc gây tối nghĩa chỉ để lách qua hệ đếm Word Count hay Keyword Density.
11. **Keyword Density (Premium SEO)**: Mật độ Keyword lý tưởng là ~1.4% (dao động 1.0-1.4%). Không cố ép vòng mật độ lên mức 1.5-2% nếu điều đó làm phá vỡ cấu trúc lập luận tự nhiên của chuyên gia.
12. **Markdown Tables**: Khi làm các nội dung trình bày về "Bảng tính", "So sánh", hay "Ưu nhược điểm" thì BẮT BUỘC dùng định dạng Markdown Table chuẩn (`| Cột 1 | Cột 2 |`). CẤM dùng gạch đầu dòng (bullet lists) thay thế.**
1. **Content Freshness**: MUST use `web search` to verify the latest information, regulations, and industry data before writing. Always reference the most current sources. Never rely on outdated information.
2. **No Emoji**: Articles must NOT contain any emoji characters (⭐, ⚠️, 🔥, etc.). Use text labels like **(MỚI)**, **Lưu ý**, **Quan trọng** instead.
3. **No Em Dash**: Never use em dash (—) in articles. Always use short dash (-) instead.
4. **Key Takeaways**: Every article MUST include a `[key_takeaways]...[/key_takeaways]` shortcode block after the intro paragraph (before the first image). Contains 5-7 bullet points summarizing the most important facts. MUST have a blank line before `[/key_takeaways]`.
5. **No Brand Prefix in Expert Remarks**: Blockquote expert remarks must NOT be prefixed with brand name. The blockquote stands alone as objective expert insight.
6. **Keyword Density**: The **primary keyword** MUST appear **5-10 times** in the article body (excluding metadata table), scaled by content length. All **secondary keywords** and **semantic/LSI keywords** from `research.md` MUST also appear at least once naturally in the article. Verify keyword presence during the Audit phase.

## 1. Preparation
- **Input**: User provides a target keyword.
- **Action**: Create a designated folder for the keyword.
   > `clients/General-B2B/brands/General-B2B/keywords/[keyword-slug]`

## 2. Phase 1: Semantic Research & Intent Discovery
- **Action**: Use `web search` to analyze current Google SERP features (Snippet, PAA, Local Pack) to confirm Micro-Intent.
- **Skill**: `.agent/skills/common/analyzing-search-intent/SKILL.md` (to document intent)
- **Skill**: `.agent/skills/common/extracting-keywords/SKILL.md` (to build entity map)
- **Optimization**: Use search operators like `"[keyword]"` for exact volume context and `site:.vn` for localized entities.
- **Output**: `research.md`
- **Goal**: Analyze Entity Map, Query Clusters, and User Intent with real-time data.

## 3. Phase 2: Content Outline
- **Skill**: `.agent/skills/common/generating-outlines/SKILL.md`
- **Input**: `research.md` (now containing real-time search data)
- **Output**: `outline.md`
- **Goal**: Create a structured outline with Header, Hook, Body, Semantic Expansion, and FAQ.

## 4. Phase 3: Content Writing
- **Skill**: `.agent/skills/common/writing-semantic-content/SKILL.md`
- **Input**: `research.md` + `outline.md`
- **Output**: `article.md`
- **MANDATORY**: The article MUST start with an **SEO Metadata Table** before the H1 heading. Use this exact format (use short dashes `-`/`--` for outline hierarchy, never em dashes):

```markdown
| | |
|---|---|
| **Keyword chính** | [primary keyword] |
| **Keyword phụ** | [secondary keyword 1] |
| | [secondary keyword 2] |
| | ... |
| **Slug** | [keyword-slug] |
| **Meta title** | [optimized title with keyword + freshness year] |
| **Meta description** | [compelling 155-char description with keyword] |
| **Outline** | H1: [title] |
| | - H2: [section] |
| | -- H3: [subsection] |
| | ... |

---
```
- **Goal**: Draft the complete article following the 6-part Semantic SEO structure.

## 5. Phase 4: Fact-Checking & Deep Research (Optimized)
- **Skill**: `.agent/skills/common/rechecking-facts/SKILL.md`
- **Action**: Use `web search` with **Advanced Operators**:
    - `site:[competitor_url] [claim]` to verify claims.
    - `"[technical_spec]"` to find official data sheets.
    - `lang:vi` or `lang:en` for specific source validation.
- **Input**: `article.md`
- **Output**: `fact-check-report.md` (and corrected `article.md`)
- **Goal**: Safeguard against AI hallucinations. Verify all technical claims against authoritative sources.

## 6. Phase 5: Zero-Flair Audit
- **Skill**: `.agent/skills/common/enforcing-zero-flair/SKILL.md`
- **Action**: BẮT BUỘC gọi lệnh `/zero-flair` để tiêu diệt các từ ngữ sáo rỗng, đao to búa lớn do AI tự bịa ra trước khi xem xét bài viết hoàn thiện.
- **Input**: `article.md`

## 7. Final Output
- Notify user that the process is complete.
- Provide paths to all artifacts: `research.md`, `outline.md`, `fact-check-report.md`, `article.md`.

---
