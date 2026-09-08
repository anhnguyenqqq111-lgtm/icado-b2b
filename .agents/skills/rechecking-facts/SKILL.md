---
name: rechecking-facts
description: >
  Performs deep research to fact-check the generated article.
  Validates technical claims, pricing, specifications, and entities against authoritative sources.
  Triggers: fact check, recheck facts, verify claims, /recheck-facts
---

# Rechecking Facts (Deep Research)

## Purpose
To ensure 100% technical, legal, and commercial accuracy of the drafted SEO article (`article.md`) before final audit. This skill acts as a safeguard against AI hallucinations, ensuring that all claims, numbers, and specifications are verifiable.

## Process

### Phase 1: Claim Extraction

#### Entry Check
```
IF `article.md` exists:
    → Proceed to Extraction
ELSE:
    → Error: No article draft found to fact-check.
```

#### Action
1.  **Read** the `article.md` draft.
2.  **Extract verifiable claims**. Look specifically for:
    *   **Prices/Costs** (e.g., "Máy băm nhựa cũ có giá từ 50 - 100 triệu").
    *   **Technical Specifications** (e.g., "Động cơ Servo tiết kiệm 40% điện năng").
    *   **Legal/Regulatory References** (e.g., "Nghị định 15/2018/NĐ-CP").
    *   **Historical/Factual Statements** (e.g., "Công ty X thành lập năm Y").
    *   **Performance Metrics** (e.g., "Tăng năng suất 30%").

### Phase 2: Deep Research & Verification

**MANDATORY DEEP RESEARCH PROTOCOL**: You MUST NOT rely on your internal knowledge or simple `web search` snippets. 

#### Action
For each extracted claim, you MUST forcefully deploy the `browser tool` (incognito/private mode tab) to directly navigate standard sources and cross-reference facts cleanly without personalization bias.

1.  **Formulate precise queries**:
    *   Instruct the browser subagent to search `site:gov.vn "Nghị định 15/2018/NĐ-CP"` or `lãi suất techcombank mới nhất 2026`.
2.  **Evaluate Sources via Browser**:
    *   Command the subagent to click and read the actual text inside Gov articles, manufacturer PDFs, and official bank portals.
    *   Snippets are not enough to confirm deep parameters.
3.  **Compare**: Check the claim in `article.md` against the researched truth.

### Phase 3: Resolution & Correction

#### Action
1.  **Status Categories**:
    *   **✅ Verified**: The claim is accurate. No action needed.
    *   **⚠️ Needs Nuance**: The claim is mostly true but needs context (e.g., "Saves 40% energy" *should be* "Saves up to 40% energy under optimal conditions"). -> **Edit the article**.
    *   **❌ False/Hallucinated**: The claim is factually incorrect. -> **Edit the article** to correct the fact or remove the claim entirely.
2.  **Self-Correction**: Directly update `article.md` with the verified facts. Do not just leave a note; fix the text.

### Phase 4: Output Generation

Generate `fact-check-report.md`:

```markdown
# Fact-Check Report (Deep Research)

## 1. Verified Claims
- [Claim] - Source: [URL/Context File]

## 2. Corrections Made
- **Original**: [False Claim]
- **Corrected To**: [Verifiable Fact]
- **Source**: [URL/Context File]

## 3. Unverifiable Claims Removed
- [List any claims that were removed because they couldn't be proven]
```

## Self-Check (Read before finishing)

□ Did I actually use search tools or read context files to verify, or did I just guess?
  → You MUST perform actual verification.
□ Did I update the `article.md` file with the corrections?
  → The final outcome must be a corrected draft.
□ Are the sources cited authoritative?
  → Wikipedia is okay for general facts, but Gov/Manufacturer sites are required for regulations/specs.
