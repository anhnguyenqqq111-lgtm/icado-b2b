# SERP source protocol

Use this reference when exact localized competitor rankings are needed.

## Preferred source order

1. Invoke the workspace `google-serp-checker` skill; it selects the configured SERP API or controlled browser path.
2. Within that skill, use a configured Bright Data SERP API with a fixed Vietnam location, language, device, and timestamp.
3. Use the workspace `tools/rank-checker`, if it can return organic results without CAPTCHA.
4. Use a clean/incognito browser session, labeled as browser-observed.
5. Use a user-provided export or screenshot, labeled as user-provided.

Never use an AI-generated search summary as proof of an exact Google rank.

## Bright Data setup

The product page may advertise a free monthly request allowance and pay-as-you-go pricing; eligibility and quota are controlled by the user's Bright Data dashboard and may change. Do not promise free usage in the report without checking the account dashboard.

The API key must stay in a local environment variable. Do not paste it into chat, Markdown, source code, shell history when avoidable, or Git.

Example request pattern:

```bash
export BRIGHTDATA_API_KEY="API_KEY_CUA_BAN"
export BRIGHTDATA_ZONE="TEN_ZONE_CUA_BAN"

curl --request POST \
  --url https://api.brightdata.com/request \
  --header "Authorization: Bearer $BRIGHTDATA_API_KEY" \
  --header "Content-Type: application/json" \
  --data "{
    \"zone\": \"$BRIGHTDATA_ZONE\",
    \"url\": \"https://www.google.com/search?q=QUERY_ENCODED&hl=vi&gl=vn&brd_json=1\",
    \"format\": \"raw\",
    \"method\": \"GET\",
    \"country\": \"vn\"
  }"
```

Use the actual zone name created in the dashboard. Prefer the Bright Data Playground to set city, language, search type, pagination, and mobile/desktop parameters when the query-string syntax is unclear.

## SERP evidence record

For every query, store or report:

```text
query:
timestamp:
country:
language:
city_or_location:
device:
personalization:
provider:
request_parameters:
organic_results:
```

Rank is the 1-based position within the filtered organic-results list. Exclude ads, map packs, PAA, featured snippets, video blocks, related searches, and the audited domain from competitor-rank calculations.

## Failure handling

If the response is empty, blocked, contains CAPTCHA/unusual-traffic content, or cannot be parsed reliably:

- do not infer competitor URLs or ranks;
- report the failure and the exact source attempted;
- use a different permitted source or request a user export;
- mark affected rows `Unverified`.
