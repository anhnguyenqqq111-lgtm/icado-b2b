---
name: research-internal-links
description: Research, select, and validate contextual internal-link opportunities for any website or SEO project. Use when Codex is asked to đi internal link/inlink, find anchor text already present in source articles, map several anchors per page to relevant pages on the same site, audit proposed internal links, or deliver an insertion-ready CSV/Markdown link plan.
---

# Research Internal Links

Build an evidence-backed internal-link plan without inventing anchor text.

## Inputs

Collect or infer:

- Site/domain and source article URLs.
- Requested anchors per article; default to 3.
- Language, exclusions, and output format; default to Markdown plus CSV when a file is useful.
- Whether the user wants recommendations only or authorized CMS/file edits.

Proceed with safe defaults when details are omitted. Browse because live pages, indexes, and URLs are time-sensitive.

## Workflow

1. Fetch each source page and isolate the article body. Exclude navigation, breadcrumbs, author/date boilerplate, tags, captions, related-post blocks, comments, and footer.
2. Preserve a normalized plain-text copy of the body while retaining the exact displayed spelling of candidate anchors.
3. Discover relevant destination pages from the same canonical domain using, in order:
   - site sitemap or CMS index;
   - site search or public CMS API;
   - search engine queries restricted with `site:`.
4. Match destinations by topical hierarchy:
   - same named entity, place, person, object, or event;
   - same subtopic or user intent;
   - broader parent topic only when no direct match exists.
5. Select the requested number of anchors per source. Require every anchor to occur verbatim in the isolated body. Prefer descriptive noun phrases of 2–8 words over generic words.
6. Use distinct destination URLs within a source article unless the user explicitly permits duplicates. Never link a page to itself.
7. Check each destination is live, canonical, indexable when detectable, in the requested language, and on the allowed domain. Avoid tag, category, search, attachment, PDF, login, and redirect URLs unless explicitly requested.
8. Avoid placing overlapping anchors in the same occurrence, repeated exact-match anchors, or links crowded into one paragraph. Recommend the first contextually strong occurrence, not automatically the first textual occurrence.
9. Score or label topical confidence. Replace low-confidence links when a closer destination exists.
10. Validate the completed plan. For JSON plans, run `scripts/validate_link_plan.py`. Treat its body extraction as a safety check and manually inspect failures because themes vary.

## Quality rules

- Do not rewrite a sentence merely to manufacture an anchor unless the user authorizes copy edits.
- Do not claim an anchor is present based only on a title, caption, tag, menu, or related-post card.
- Do not use anchors such as “xem thêm”, “tại đây”, or “bài viết” when a descriptive phrase exists.
- Keep target relevance explainable in one short sentence.
- Prefer evergreen editorial pages over commercial or news pages when both satisfy the same intent.
- Flag thin coverage instead of forcing the requested quota.
- If live access is blocked, clearly label unverified rows; never present them as verified.

## Deliverable

Return one row per proposed link with:

| Source URL | Anchor text | Target URL | Context/reason | Confidence | Verification |
|---|---|---|---|---|---|

Group rows by source article for readability. State the research date and any inaccessible pages. If editing is authorized and credentials/tools are available, insert links and then re-fetch or render the page to verify them.

For machine validation, prepare JSON as documented in `references/plan-schema.md`.
