---
name: visualizing-content
description: >
  Finds and inserts relevant images into an article.
  Analyzes content for visual opportunities, searches for images, and embeds them.
  Triggers: find images, add photos, visualize content, /visualize
---

# Visualizing Content Skill

## Purpose
This skill enhances text-heavy articles by identifying key visual opportunities, sourcing relevant professional images, and embedding them to improve reader engagement and SEO.

## Process

### Phase 1: Visual Opportunity Analysis

#### Entry Check
```
IF `article.md` exists:
    → Proceed to Analysis
ELSE
    → ASK user for the target article path.
```

#### Activity
1.  **Read** the `article.md` file.
2.  **Identify** 3-5 distinct sections that would benefit most from visual aid (e.g., complex processes, machinery, comparative tables, or key concepts).
3.  **Formulate** specific search queries for each identified section.
    *   *Constraint*: Queries must be specific to the industry (e.g., "industrial pvc dispensing machine", "food flavoring r&d lab").

### Phase 2: Image Sourcing & Generation

#### Entry Check
```
IF Visual Opportunities are identified:
    → Proceed to Source/Generate
ELSE
    → Return to Phase 1
```

#### Activity
1.  **Evaluate** the type of visual needed:
    *   *Real World/Specific Device*: Use `web search` to find real photos (e.g., "M&M's sorter machine").
    *   *Conceptual/Diagram/Illustration*: Use `generate_image` to create unique assets (e.g., "Diagram of in-line recycling process", "Comparison of plastic waste vs pellets").
    
2.  **Execution**:
    *   **Option A (Search)**: Use `web search` to find an image URL.
    *   **Option B (Generate)**: Use `generate_image` with a descriptive prompt. Save the image to the `assets/` folder (or appropriate path) and use the local path.
    
3.  **Selection**:
    *   *Priority*: High-quality generated images or authoritative sourced images.
    *   *Fallback*: If generation fails or search yields nothing, use the placeholder syntax.

### Phase 3: Content Integration

#### Entry Check
```
IF Images (Generated or Found) are ready:
    → Proceed to Insertion
```

#### Activity
1.  **Insert** the selected images into `article.md` at the identified locations.
    *   **Generated Image**: `![Alt Text](file:///absolute/path/to/generated_image.png)`
    *   **Sourced Image**: `![Alt Text](Image_URL)`
    *   *Placement*: Immediately after the relevant Header or Paragraph.
2.  **Verify** the file format is preserved.

## Self-Check (Read before finishing)

□ Did I find at least 3 relevant visual opportunities?
  → If not, look for abstract concepts that can be visualized (e.g., charts, icons).

□ Are the image sources appropriate for a B2B audience?
  → Avoid cartoony or low-quality stock verify.

□ Did I actually modify the `article.md` file?
  → The user expects the file to be updated, not just a list of links.

□ Is the Alt Text descriptive and SEO-friendly?
  → Ensure it describes the image and relates to the section topic.
