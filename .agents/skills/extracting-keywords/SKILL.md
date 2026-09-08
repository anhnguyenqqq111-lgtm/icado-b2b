---
name: extracting-keywords
description: >
  Extracts entities and constructs a semantic query map for a given keyword.
  Triggers: extract keywords, entity research, semantic analysis, /extract-keywords
---

# Extracting Keywords & Entities

## Purpose
Analyze a main keyword to extract relevant entities (Person, Org, Concept, etc.) and build a cluster of supporting queries/keywords to establish topical authority.

## Process

### Phase 1: Input Validation

#### Entry Check
```
IF target keyword is provided:
    → Proceed to Phase 2
ELSE:
    → Ask: "What is the main keyword or topic you want to analyze?"
```

### Phase 2: Entity Extraction

#### Actions
Simulate knowledge graph lookup to identify entities related to the **Main Keyword**.

**Categories to Find:**
1.  **Person**: Experts, Authors, Influencers.
2.  **Organization**: Companies, Brands, Tools.
3.  **Location**: Geographically relevant interactions.
4.  **Concept**: Defined theories, laws, frameworks.
5.  **Time/Event**: Key dates, history.

*Constraint*: Organize into Primary (High Relevance) and Secondary (Medium Relevance).

### Phase 3: Query & Keyword Research

#### Actions
Generate supporting keywords and cluster them by **User Intent**.

**Sources:**
*   Autocomplete / People Also Ask (PAA)
*   LSI / Related Searches

**Clusters:**
*   **Informational**: Definition, How-to, Guide.
*   **Commercial**: Best, Review, Top, Vs.
*   **Transactional**: Price, Buy, Service.

### Phase 4: Output Generation

Produce a Markdown report matching this template:

```markdown
# Semantic Analysis: [Main Keyword]

## 1. Entity Interpretation
| Category | Entities (Examples) | Relevance |
| :--- | :--- | :--- |
| **Person** | ... | ... |
| ... | ... | ... |

## 2. Keyword Clusters

### Cluster A: [Topic Facet, e.g., Definitions]
*   **Intent**: Informational
*   **Keywords**: [List keys]

### Cluster B: [Topic Facet, e.g., Comparison]
*   **Intent**: Commercial
*   **Keywords**: [List keys]

## 3. Strategic Recommendations
*   [Brief notes on usage]
```

## Self-Check (Read before outputting)

□ Did I categorize entities correctly?
  → Ensure a "Tool" isn't listed as a "Concept".

□ Do the clusters make semantic sense?
  → "How to" queries should be separate from "Best X" queries.

□ Are the specific entities relevant to the *User's* topic?
  → Don't hallucinate generic entities; use specific ones for the niche.
