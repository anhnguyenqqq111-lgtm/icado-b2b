---
name: seo-audit-research
description: Research, audit, and prioritize SEO pages using GA4, GSC, live browser review, and localized SERP competitors; produce an evidence-backed Markdown audit with exact rewrite, cut, add, and technical recommendations. Use when the user asks for SEO audit research, competitor analysis, high-impression keyword analysis, service-page improvement, or a final .md report.
---

# SEO Audit Research

Run a complete, evidence-backed SEO research and content-audit workflow for a supplied website. The default output is one Vietnamese Markdown report. The workflow is reusable across clients; never assume Everlog, a property, a date range, or a URL unless the user provides it or the connected data confirms it.

## Operating contract

- If the user asks for a plan first, produce only the scope, data sources, URL list, research method, deliverables, assumptions, and approval gate. Do not begin the substantive audit until the user approves or explicitly says to proceed.
- If the user says to proceed, execute the whole workflow in one pass when access permits.
- Use the user's exact output path when supplied. Otherwise use the workspace's canonical client/topic path or ask only when the destination materially affects the deliverable.
- Preserve Vietnamese diacritics and write in clear, practical Vietnamese unless another language is requested.
- Do not make CMS, code, redirect, metadata, or content changes unless the user separately authorizes implementation. The default deliverable is research and recommendations only.
- Never expose API keys, OAuth tokens, cookies, or private account data in the report or chat.
- Separate observed facts, inferred opportunities, and recommendations. Mark unavailable data instead of filling gaps with guesses.

## Record & Replay compatibility

This workflow is semantic-first and can be learned from a demonstrated UI session, but the recording must not hard-code the Everlog example. Convert demonstrated values into inputs:

```text
DOMAIN
TARGET_URLS
GA4_PROPERTY
GSC_PROPERTY
DATE_RANGE
COUNTRY
LANGUAGE
CITY_OR_LOCATION
DEVICE
SERP_PROVIDER
OUTPUT_PATH
```

For a recorded workflow, use stable semantic targets such as the GSC/GA4 property selector, query/page filter, date-range control, SERP provider's query and location fields, article URL, and Markdown output path. Avoid coordinate-only clicks when an accessible label, role, URL, or visible text target exists. Prefer MCP/API calls for GA4, GSC, and SERP retrieval; use UI replay for authentication-dependent navigation, visual inspection, and export verification.

The replay must verify each major state transition: the selected property matches the domain, filters/date range are visible, the returned SERP has parseable organic results, every requested URL was audited, and the Markdown file exists at the requested path. Replace credentials, cookies, API keys, and private account values with placeholders; never store them in a recording-derived skill.

## Required inputs and defaults

Collect or infer:

- Domain and country/language.
- Target URLs, or permission to discover the highest-priority pages.
- Business goal: leads, service enquiries, organic traffic, or another stated goal.
- Date range for GA4/GSC; default to the latest complete 3 months and state the exact dates.
- Output folder and filename; default to a single `.md` report.

For a request similar to the Everlog workflow, audit the supplied service/blog URLs plus the highest-opportunity pages discovered from GSC and GA4. Do not silently reduce the requested URL list.

## Phase 1: site, brand, and source-of-truth review

1. Read the workspace `AGENTS.md`, `README.md`, `workspace.toml`, the applicable brand persona/reference files, and any existing client workflow before researching.
2. Browse the live domain and each target URL. Record status, canonical URL, indexability signals when observable, title, meta description, H1, headings, visible copy, breadcrumbs, navigation, images/alt text, internal links, structured-data hints, dates, and conversion elements.
3. Check sitemap/robots and representative templates where accessible. Do not claim a sitewide technical defect from one page; label sample-based findings.
4. Preserve existing user work. Inspect `git status` before editing and do not overwrite unrelated or approved artifacts.

## Phase 2: GA4 and GSC via MCP

Use the connected GA4/GSC MCP tools when available. First identify the Google account's accessible GA4 accounts/properties and GSC properties; select the property matching the supplied domain and record the selected property ID/URL, timezone if available, date range, filters, and sampling/limitations.

### GA4 extraction

Retrieve, when permissions and connector support allow:

- landing-page performance: users, sessions, engaged sessions, engagement rate, average engagement time, key events/conversions, and revenue if relevant;
- organic acquisition segmented by landing page and source/medium;
- page views and engagement for target URLs;
- conversion paths or events relevant to service enquiries.

Use GA4 to prioritize pages with traffic but weak engagement/conversion, pages with meaningful conversions, and pages with growth potential. Do not treat traffic as proof of ranking.

### GSC extraction

Retrieve Search Analytics by query and page with clicks, impressions, CTR, and average position. At minimum produce:

- high-impression queries, sorted by impressions;
- queries with positions approximately 4–20 and low CTR as optimization candidates;
- queries generating impressions for each target URL;
- pages with high impressions but weak clicks/CTR;
- branded versus non-branded query notes where identifiable.

Use the exact GSC query/page filters and date range in the report. Treat average position as an aggregate metric, not a guaranteed live rank. Do not merge different properties or date ranges without labeling them.

## Phase 3: localized SERP and competitor research

Read [references/serp-sources.md](references/serp-sources.md) before collecting exact rankings or configuring a SERP provider.

When `google-serp-checker` is available, invoke `$google-serp-checker` automatically as the required SERP collection step; do not merely recommend it or wait for the user to call it separately. Feed it the GSC-derived queries and the user's target domain/URLs before beginning competitor-content analysis.

Use this sequence:

1. Build the query set from GSC high-impression queries, queries ranking approximately 4–20, and queries mapped to each requested URL. Add the supplied primary/secondary keywords when GSC is unavailable.
2. Call `google-serp-checker` with the query list, target domain/URLs, Vietnam/Vietnamese defaults when appropriate, city/location, desktop or mobile device, and top-10 depth unless the request specifies otherwise.
3. Validate that each response is a Google results page, not a consent/CAPTCHA/unusual-traffic page. Keep the returned `keyword | target domain | position | ranking URL | location | device | checked_at | status` evidence.
4. Use the returned organic ranking URLs and positions to select the top 3–5 relevant competitor pages for browser reading. Do not replace these URLs with AI-search results or an unverified web-search guess.

The SERP snapshot is a required preface to each article's competitor section. Before the analysis, state:

- the exact keyword/query researched;
- country, language, city/location, device, date, and personalization status;
- the source used and whether the result is live API data, browser observation, or a user-provided SERP;
- each selected competitor URL and its observed organic position.

`google-serp-checker` chooses a configured SERP API first, then a controlled browser fallback. Configure Vietnam, Vietnamese, the relevant city, and desktop/mobile explicitly; keep the same settings across comparisons. Record request timestamp and parameters. Parse only organic results for rank; exclude ads, map packs, PAA, featured snippets, video blocks, related searches, and the audited domain unless the report is specifically analyzing those features.

If `google-serp-checker` is unavailable, use its documented controlled-browser fallback only for a small query set and label the result as browser-observed. If Google blocks automation or returns CAPTCHA/unusual-traffic pages, do not present guessed rankings. Ask for a SERP export/screenshot or mark the competitor ranks unverified. AI search summaries are not evidence of an exact Google rank.

For each target article, inspect the top 3–5 relevant organic competitor pages, not merely the first three URLs. Capture:

- ranking position and URL;
- title, H1, H2/H3 structure, content type, search-intent coverage, and approximate visible word count;
- entities, definitions, examples, tables, visuals, FAQs, sources, author/business trust signals, schema hints, and conversion paths;
- content gaps, overused sections, weak explanations, and SERP features competitors satisfy.

Count comparable main-content words using the same exclusion rule for all pages. Report a range and median/typical competitor length, not a fake exact target. Recommend the shortest length that fully satisfies the intent and closes the gaps; never add words solely to hit a number.

## Phase 4: article-by-article audit

Audit every requested URL separately. For each one, compare GSC queries, GA4 behavior, the live article, and the localized SERP competitors. Address:

1. Intent and topical scope: what the searcher needs first, secondary intents, and whether the article answers them in the right order.
2. SERP alignment: title/H1 promise, competitor patterns, result type, snippets, and missing subtopics.
3. Content quality: factual clarity, definitions, examples, calculations/conditions, Vietnam/logistics context when relevant, freshness, source quality, E-E-A-T signals, and readability.
4. On-page SEO: title, meta description, H1, heading hierarchy, keyword/entity use, introduction, image alt text, anchor text, canonical, breadcrumbs, schema, and indexability signals.
5. UX and conversion: scannability, tables, mobile readability, CTA clarity, enquiry friction, related services, and contextual internal links.
6. Technical issues: status/redirects, robots/meta robots, canonical conflicts, duplicate/thin sections, broken links, image weight/dimensions when observable, Core Web Vitals only when measured, and structured-data validity only when tested. Distinguish page-level observations from issues requiring a sitewide crawl or dev access.

## Required rewrite decisions

Do not stop at generic advice. For every article, specify:

- what to keep and why;
- what to cut, with the section/paragraph and reason;
- what to rewrite, identifying the unclear wording and supplying a clearer direction or replacement wording when safe;
- what to add, the exact insertion point, heading level, purpose, entities/queries covered, and evidence needed;
- what to reorder, merge, or split;
- recommended title, H1, meta description, introduction/answer-first block, outline, FAQ/schema opportunities, CTA, and internal-link opportunities;
- recommended content length as a justified range based on comparable competitors and intent;
- priority, effort, owner (content/SEO/dev/design), and expected impact.

When a claim is financial, legal, regulatory, technical, price-sensitive, or otherwise time-sensitive, flag it for authoritative fact-checking and do not invent values. Retain citations or source notes during rewriting.

## Technical issue format

Use a table with:

| URL | Issue | Evidence | Severity | Fix | Owner | Validation |
|---|---|---|---|---|---|---|

Severity should be High/Medium/Low and reflect organic impact plus implementation risk. Include a sitewide issue only when supported by multiple samples, crawl data, or a connected technical tool.

## Markdown deliverable

Write one `.md` file unless the user requests separate files. Use this order:

1. Title, domain, research date, data period, scope, and executive summary.
2. Data-access and methodology notes, including GA4/GSC property identifiers, SERP source, location/device, and limitations.
3. GSC high-impression keyword table and GA4 page/opportunity table.
4. Prioritized audit list, including the rationale for the top 10 pages when that was requested.
5. Competitor SERP preface and article audit for each URL, one article at a time.
6. Technical issue table.
7. Consolidated content plan: quick wins, 30-day, 60-day, and 90-day actions; dependencies and measurement plan.
8. Appendix containing raw query/page evidence, competitor URLs/ranks/word-count method, internal-link map, and unverified items.

Use tables for metrics and issue tracking, bullets for recommendations, and explicit labels such as `Observed`, `Inferred`, `Recommended`, and `Unverified`. Include the report's exact file path in the final response.

## Quality gate before handoff

Verify that:

- every requested URL has its own audit;
- `google-serp-checker` was automatically used for the SERP step when available, and its query/rank evidence is preserved;
- every competitor section begins with keyword, SERP parameters, source, rank, and word-count comparison;
- high-impression GSC queries are tied to page/action recommendations;
- GA4 and GSC date ranges and properties are stated;
- recommendations say where to cut/add/rewrite, not only what topic to cover;
- technical claims are scoped to available evidence;
- no API credentials or unsupported rankings are included;
- the Markdown file opens correctly and contains no placeholder text;
- if workspace canonical artifacts were changed, update the appropriate `topic.toml` and run the workspace validator. For a standalone report, do not create duplicate topic artifacts just to satisfy this skill.
