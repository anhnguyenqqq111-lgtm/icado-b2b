---
name: analyzing-search-intent
description: >
  Deeply analyzes search intent using a 12-type Semantic Micro-Intent framework.
  Provides specific content format recommendations and SERP feature predictions.
  Triggers: analyze intent, search intent analysis, check user intent, /analyze-intent
---

# Analyzing Search Intent (Semantic NLP)

## Purpose
To move beyond basic "Info/Trans" labeling and provide a granular 12-point micro-intent analysis of what the user actually wants, integrated with Entity attributes.

## Mandatory References
*   `semantic-reference.md`: The latest Semantic SEO Micro-Intents Framework (12 categories) and Entity-Intent relationship. (MUST READ before classification).
*   `references/intent-definitions.md`: Core definitions.

## Process

### Phase 1: Deep SERP & Intent Discovery
**CRITICAL PROTOCOL**: You MUST use the `browser tool` to:
1. Search the keyword on Google.
2. Analyze the actual SERP visual layout and the attributes targeted by competitors.

### Phase 2: Classification Details
Using the framework from `semantic-reference.md`:
1.  **Identify Macro-Intent**: Informational, Commercial, Transactional.
2.  **Identify Micro-Intent**: Which of the 12 micro-actions is required? (e.g., Quick Answer, Comparison, Local Discovery).
3.  **Entity-Intent Relationship**: What specific Attribute of the Entity is the user searching for?

### Phase 3: Content Mapping
Recommend the exact Content Vehicle (e.g., Encyclopedic Guide, Compare Table, PDP) needed to satisfy the micro-intent.

### Phase 4: Output Generation
Generate an Intent Report in markdown outlining the primary intent, micro-intents, related entities, and recommended content layout.
