# Link-plan JSON schema

Use a JSON array. Each item represents one proposed internal link:

```json
[
  {
    "source_url": "https://example.com/source/",
    "anchor_text": "exact phrase already in the article",
    "target_url": "https://example.com/target/"
  }
]
```

Optional fields such as `reason`, `confidence`, `source_title`, and `target_title` are preserved by downstream workflows but ignored by the validator.

Run:

```bash
python3 scripts/validate_link_plan.py plan.json
```

The validator checks required fields, same-domain status, self-links, duplicate source-target pairs, HTTP reachability, and whether the exact anchor occurs in the likely article body. Exit code is nonzero when any row fails.
