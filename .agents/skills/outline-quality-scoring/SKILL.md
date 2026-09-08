---
name: outline-quality-scoring
description: Score a brand-neutral SEO outline against its research, search intent, factual readiness, and stated brand rules. Use before outline approval for brands without a dedicated rubric.
---

# Outline quality scoring

Use this scorecard only when the brand does not provide its own approved outline rubric. Read the relevant brand rules before scoring.

## Inputs

- `outline.md` is required.
- Read `search-intent.md` and `research.md` when present.
- Read the matching brand persona, content rules, and internal-link reference when they exist.

## Scorecard (100 points)

| Criterion | Points | Pass condition |
|---|---:|---|
| Intent alignment | 20 | Title, H1, and section order answer the documented primary intent |
| Entity and topic coverage | 20 | Required entities and decision criteria are covered without overlapping headings |
| Evidence and factual readiness | 20 | Claims, prices, specifications, regulations, and examples are sourced or explicitly marked for verification |
| Structure and usefulness | 15 | Sections form a coherent reader journey; tables and FAQ are used only where useful |
| Brand fit and conversion logic | 15 | Tone, CTA, service/product mentions, and internal links match the brand references |
| Metadata and formatting | 10 | Metadata is usable and headings follow the selected brand style |

## Decision

- Pass at 80/100 or the higher threshold specified by the brand.
- A score below 80 returns the outline to revision with concrete fixes by heading.
- Do not impose Home Credit signatures, service-matching rules, font blocks, word counts, or internal-link ratios on another brand.

## Output

Write `outline-qa-report.md` with the score, evidence, failed criteria, and prioritized edits. Keep it as a supporting QA artifact; the canonical outline remains `outline.md`.
