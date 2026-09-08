---
name: enforcing-zero-flair
description: >
  Enforces the Zero-Flair policy. Strips all hyperbolic AI 'word salad' and ensures strict formatting (bullet points, tables, signatures).
  Use this before finalizing or auditing any Home Credit article.
  Triggers: check word salad, enforce zero flair, audit flair, /zero-flair
---

# Enforcing Zero-Flair (Anti-Word-Salad Protocol)

## Purpose
AI models naturally default to hyperbolic "word salad" (e.g., "tuyệt tác", "đỉnh cao", "điều phối lương bổng", "tiết kiệm sinh sản") when generating financial or technical content. This skill acts as a strict filter to forcefully replace these hallucinations with cold, objective, S-V-O Vietnamese. It also validates structural hard-rules.

## Phase 1: Text Blacklist & Phrasing Check

```
IF the text contains any of the forbidden terms below:
    → REWRITE the entire sentence objectively.
    → DO NOT just swap one word; fix the tone.
```

### Forbidden Vocabulary (Blacklist)

| Category | Banned Words | Replacement Concept |
|---|---|---|
| Praising | siêu phẩm, tuyệt tác, bom tấn, đỉnh cao, hoàn hảo | thiết bị, mẫu xe, dòng máy, sản phẩm |
| Robotic/Jargon | tĩnh lặng, cỗ máy liên thông, chứng thực xếp hạng | kính nhám, chuẩn bảo vệ, đạt chuẩn |
| Pseudo-Finance | điều phối lương bổng, dư địa đầu tư, tiết kiệm sinh sản, bảng mô phỏng dòng tiền, biến số giá thành, chu kỳ vay tín dụng | phân bổ thu nhập, tiết kiệm chi tiêu, số tiền thanh toán, bảng thanh toán trả góp, giá xe thực tế, thời gian vay |
| Filler | điểm nổi trội đáng báo giá, sự biến động nổi bật | thay đổi lớn nhất, điểm đáng chú ý |
| Vague Marketing | phù hợp mục tiêu, sở hữu bảo hành gốc, đặc điểm lựa chọn, lợi ích tối ưu, không gian hiển thị, vùng khuyết tối ưu khu vực, giá bán lẻ khối động cơ, sức hút dịch vụ tài chính, đánh dấu ranh giới rõ rệt, tối ưu chi phí cho từng đối tượng | phù hợp cho ai?, đối tượng sử dụng, kích hoạt bảo hành chính hãng, màn hình, tai thỏ, xe phân khối, lợi ích khi vay, ưu điểm gói vay, phân cấp rõ ràng, mức giá phù hợp |

## Phase 2: Zero-Flair Execution

```
WHEN the check is complete:
    → RETURN the corrected Markdown text.
    → POINT OUT any major word-salad phrases that were eliminated.
```

## Self-Check (Read before every response)

□ Are there any leftover hyperbolic adjectives like "hoàn hảo", "tuyệt đỉnh", "sinh sản"?
  → Rewrite to be painfully boring and objective. Disable all LLM persona creativity.
□ Did I avoid metaphorical or figurative language to explain terms?
  → Explain concepts simply and directly without metaphors.
□ Did I avoid using parentheses `()` or quotes `""` to explain or translate terms?
  → Explain directly in the sentence flow (e.g., replace "chỉ mục (indexing)" with direct context).
□ Did I avoid over-explaining common terms (SEO, AI, Website, etc.)?
  → Do not explain or define terms that are already highly popular.
□ Did I put a period at the end of bullet points (except the final one)?
  → Remove them immediately.
□ Does every bulleted list have an introductory sentence?
  → Ensure there is at least one introductory/transition sentence (e.g., "Dưới đây là một số lợi ích tiêu biểu:") before starting ANY bullet point list `-`. NEVER jump directly from a Heading (H2/H3) into a bullet point list without a leading sentence.
□ Does every descriptive bullet point follow the "Bold Prefix + Capitalized Suffix" rule?
  → For lists formatted with a colon, the text before the colon MUST be bolded, and the first letter immediately following the colon MUST be capitalized. Example: `- **Giá vàng:** Khi giá tăng...` (NOT `- **Giá vàng:** khi giá tăng...`).
