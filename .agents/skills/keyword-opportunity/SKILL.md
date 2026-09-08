---
name: keyword-opportunity
description: Find and prioritize SEO keyword opportunities from Google Search Console, optionally validate landing-page relevance with GA4, and export a full-period table with blog/content ideas. Use when the user asks for keyword opportunity, high-impression queries, keywords outside Top 10, or blog keyword expansion from first-party search data.
---

# Keyword Opportunity

## Purpose

Identify queries that already generate Google impressions but have room to grow, then separate genuine content opportunities from conversion terms, noise, unrelated queries, and duplicate URL signals.

The default output is a Vietnamese Markdown report. Do not edit CMS content, metadata, redirects, or code unless the user separately asks for implementation.

## Required inputs

- Website/domain and one or more seed terms. Preserve the user's spelling and language.
- Exact GSC property. Always call mcp__gscOther__list_properties first and select the property matching the supplied website.
- Date period. If the user says “1 năm”, use the GSC 365-day window and record the exact returned start/end dates. At the current date, GSC may have a 1–3 day freshness lag; record the latest date with non-zero data.
- Business context: product/service, blog-only, or both. If not stated, return both labels and do not silently treat every query as a conversion term.

GA4 is optional. If a matching GA4 property is unavailable, state that clearly and do not infer conversions or engagement from GSC.

## GSC extraction

Use the connected GSC MCP tools:

1. Retrieve query-level Search Analytics for the seed term using dimensions: query, Web search, and the full requested period.
2. Retrieve dimensions: query,date for the same filter to measure frequency and ranking stability.
3. Retrieve dimensions: query,page only for page mapping. Use query-level data for the authoritative query totals.
4. When a query-page result contains URL fragments (#section), do not sum fragment rows as separate query volume; explain that fragments are mapping signals.

For multiple seed terms, run one query for each seed, merge exact duplicates, and retain the seed/source column.

Record these fields:

| Field | Meaning |
|---|---|
| query | Exact GSC query |
| clicks | GSC clicks |
| impressions | GSC impressions |
| ctr | GSC CTR |
| position | GSC average position |
| active_days | Number of dates with an impression |
| top10_share | Share of impression from dates with position <= 10 |
| page | Best mapped URL when page data is available |

## Default opportunity rules

Apply the following rules unless the user gives different thresholds:

- impressions >= 1.
- average position > 10 for “outside Top 10”. A position of exactly 10.0 is not outside Top 10.
- The query is semantically related to the stated product/service or can naturally support its topical authority.
- For a blog-only request, exclude direct conversion terms such as buy, price, supplier, shop, where to buy, request a quote, wholesale, and equivalent local-language variants. Keep informational product education, comparison, process, use case, and FAQ queries.
- Exclude obvious unrelated brands, people, locations, health/beauty claims, image/file searches, quiz fragments, and accidental query noise. Document the exclusion logic; do not hide the raw count.

## Ranking stability

Use the daily report, not a single live SERP check, to evaluate instability:

- active_days <= 90 indicates sparse/episodic visibility within the full year.
- top10_share < 0.50 indicates most impressions occurred outside Top 10.
- Mark a query as unstable when either condition is true, and show both metrics in the report.

Do not claim that a page “disappeared” solely because its aggregate position is high. Say “GSC shows sparse or unstable visibility” and cite the active-day/top-10-share evidence.

## Content opportunity and blog ideas

For each retained query, assign:

- intent: informational, comparison, process/how-to, application/use case, product education, or commercial;
- opportunity type: new blog, expand existing article, optimize existing page, internal-link support, or reject;
- one concise blog idea that answers the query without turning the title into a sales CTA;
- a cluster label so close variants become one article rather than cannibalizing pages.

Typical clusters include:

- definition/origin: “what is matcha”, ingredients, tea plant, production;
- comparison: matcha versus green tea, Japan versus Taiwan, grades/types;
- sensory quality: taste, bitterness, umami, fishy smell, color;
- processing: production, grinding, storage, expiry;
- F&B applications: latte, milk tea, cocktail, bottled drinks, bakery, RTD;
- flavor ingredients: matcha flavor, flavouring, powder, natural flavor.

Do not generate a separate article for every spelling variant or query with only 1–5 impressions; use those as H3, FAQ, or semantic variants.

## Output

Unless another path is requested, create:

outputs/<domain-slug>-<seed>-keyword-opportunities-full-year.md

The report must contain:

1. Website, GSC property, exact period, freshness note, and business scope.
2. Methodology and explicit thresholds.
3. Summary counts: total seed queries, outside-Top-10 queries, retained opportunities, total impressions.
4. Full retained table with query, blog idea, clicks, impressions, CTR, average position, active days, Top-10 share, intent, and mapped page when available.
5. Rejected/noise categories with counts and examples.
6. Recommended content clusters and priorities.
7. Limitations: GSC average position is aggregate, not a guaranteed live rank; GA4 limitations; incomplete recent days.

Use Vietnamese diacritics when writing Vietnamese output. Preserve exact query text in the keyword column.

## Quality gate

Before handoff, verify:

- the selected GSC property matches the website;
- the report covers the requested full period;
- the latest non-zero GSC date is stated;
- query-level totals were not inflated by URL fragments;
- every retained keyword has at least one impression;
- every retained keyword satisfies the stated relevance and stability rules;
- direct conversion terms are excluded when the user requests blog ideas;
- raw counts and exclusions are transparent;
- no GA4 metric or conversion claim is fabricated;
- the generated Markdown file exists and has the expected row count.
