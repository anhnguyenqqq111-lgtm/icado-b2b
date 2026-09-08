---
name: analyzing-semantic-seo
description: >
  Analyzes and creates a comprehensive Semantic SEO strategy for a website or topic.
  Focuses on Entity extraction, Search Intent mapping, and Content Hierarchy.
  Triggers: semantic seo, phân tích seo, tạo content map, entity analysis, /semantic-seo
---

# Analyzing Semantic SEO

## Purpose
Creates a holistic SEO strategy based on Semantic Search principles—answering ALL questions related to a topic and organizing them into a coherent hierarchy (Pillar/Cluster).

## Process

### Phase 1: Discovery

#### Entry Check
```
IF User provided (Topic/Keyword AND Audience AND Goal):
    → Proceed to Phase 2
ELSE:
    → Gather missing context.
```

#### Information Needed
*   **Topic**: Main keyword?
*   **URL**: Existing website?
*   **Goal**: Rank? Authority? Content Hub?

### Phase 2: Entity Extraction

#### Actions
1.  **List Entities**: Person, Organization, Location, Concept, Time.
2.  **Map Relationships**: How do they connect?
3.  **Output**: Entity Map.

### Phase 3: Query Research

#### Actions
1.  **Generate Clusters**:
    *   *What* (Definition)
    *   *How* (Process)
    *   *Why* (Explanation)
    *   *Comparison* (Vs)
    *   *Best/Top* (Ranking)
2.  **Map Intent**: Informational, Commercial, Transactional, Navigational.

### Phase 4: Content Hierarchy

#### Actions
Define the site structure:
1.  **Pillar Page**: Validates the core topic.
2.  **Cluster Pages**: Supporting articles for specific query clusters.
3.  **Linking**:
    *   Pillar → Clusters (Downward)
    *   Clusters → Pillar (Upward)
    *   Cluster ↔ Cluster (Horizontal)

### Phase 5: Output Generation

Generate specific deliverables based on goal.
*   See `references/output-templates.md` for formats.

## Self-Check (Read before outputting)

□ Did I extract all entity types?
  → Person, Org, Place, Concept, Time.

□ Does the hierarchy make sense?
  → A broad "What is" question is usually Pillar; "How to fix specific error" is Cluster.

□ Is the linking strategy circular?
  → Ensure no orphan pages; everything links back to the pillar.

## References
*   `references/entity-patterns.md`: Detailed Entity Extraction patterns.
*   `references/query-research.md`: Methodology for finding queries.
*   `references/output-templates.md`: Templates for final deliverables.
