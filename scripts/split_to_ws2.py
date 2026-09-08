#!/usr/bin/env python3
"""Script to set up Workspace 2 and separate projects from Workspace 1."""

import os
import shutil
from pathlib import Path

WS1 = Path("/Users/t.anh/.gemini/antigravity-ide/scratch/goha-seo-main").resolve()
WS2 = Path("/Users/t.anh/.gemini/antigravity-ide/scratch/goha-seo-ws2").resolve()

print(f"Source (WS1): {WS1}")
print(f"Destination (WS2): {WS2}")

WS2.mkdir(parents=True, exist_ok=True)

def copy_item(src: Path, dst: Path):
    if not src.exists():
        print(f"Skipping non-existent: {src}")
        return
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, symlinks=True)
        print(f"Copied dir: {src.relative_to(WS1)} -> {dst}")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied file: {src.relative_to(WS1)} -> {dst}")

# 1. Base files & tools
base_items = [
    "scripts",
    "tests",
    "tools",
    ".gitignore",
    ".gitattributes",
    "codex-cli-guide.md",
    "data/ai_writing_blacklist.md",
    "data/skill-design-best-practices.md",
    "data/reference/knowledge-systems",
    "data/reference/study-workspace",
]

for item in base_items:
    copy_item(WS1 / item, WS2 / item)

# 2. Clients for WS2
copy_item(WS1 / "clients/Everest-Logistics", WS2 / "clients/Everest-Logistics")
copy_item(WS1 / "clients/MayMacCTH", WS2 / "clients/MayMacCTH")
copy_item(WS1 / "clients/Studio1Nha", WS2 / "clients/Studio1Nha")

# ICADO: Migrate into clean clients/ICADO
icado_target = WS2 / "clients/ICADO/brands/ICADO"
icado_target.parent.mkdir(parents=True, exist_ok=True)
copy_item(WS1 / "clients/General-B2B/brands/ICADO", icado_target)
if (WS1 / "clients/General-B2B/icado_seo").exists():
    copy_item(WS1 / "clients/General-B2B/icado_seo", WS2 / "clients/ICADO/icado_seo")

# 3. Personas for WS2
ws2_personas = ["Everest-Logistics", "ICADO", "MayMacCTH", "Studio1Nha"]
for p in ws2_personas:
    copy_item(WS1 / "data/reference/persona-brand" / p, WS2 / "data/reference/persona-brand" / p)

# 4. Projects & archives for WS2
copy_item(WS1 / "projects/everest-logistics", WS2 / "projects/everest-logistics")
for extra_root in ["everest-logistics-next 2", "everest-logistics-next 3", "everest-logistics-site 2.zip"]:
    copy_item(WS1 / extra_root, WS2 / extra_root)

# 5. Workflows for WS2
ws2_workflows = [
    "flow-everest-seo.md",
    "outline-everest.md",
    "flow-ICADO-seo.md",
    "outline-icado.md",
    "flow-MayMacCTH-seo.md",
    "outline-maymaccth.md",
    "flow-studio1nha-seo.md",
    "outline-studio1nha.md",
    "semantic-seo.md",
]
(WS2 / ".agent/workflows").mkdir(parents=True, exist_ok=True)
for wf in ws2_workflows:
    copy_item(WS1 / ".agent/workflows" / wf, WS2 / ".agent/workflows" / wf)

# 6. Skills for WS2 (.agents/skills)
ws2_brand_skills = [
    "everest-article-audit",
    "everest-outline-rules",
    "generating-outlines-everest",
    "generating-outlines-icado",
    "icado-outline-rules",
    "generating-outlines-maymaccth",
    "maymaccth-outline-rules",
    "generating-outlines-studio1nha",
    "studio1nha-outline-rules",
]

shared_skills = [
    "analyzing-competitors",
    "analyzing-search-intent",
    "analyzing-semantic-seo",
    "auditing-content",
    "client-approval-gate",
    "competitor-content-scraping",
    "competitor-outline-intelligence",
    "content-gap-analysis",
    "enforcing-zero-flair",
    "extracting-keywords",
    "faq-research",
    "generating-outlines",
    "generating-table-of-contents",
    "keyword-expansion",
    "keyword-opportunity",
    "keyword-strategy-mapping",
    "learn-ai-output",
    "outline-quality-scoring",
    "rechecking-facts",
    "research-internal-links",
    "seo-audit-research",
    "visualizing-content",
    "writing-semantic-content",
]

(WS2 / ".agents/skills").mkdir(parents=True, exist_ok=True)
for sk in ws2_brand_skills + shared_skills:
    copy_item(WS1 / ".agents/skills" / sk, WS2 / ".agents/skills" / sk)

# 7. Outputs for WS2
(WS2 / "outputs").mkdir(parents=True, exist_ok=True)
for p in (WS1 / "outputs").iterdir():
    name = p.name.lower()
    if any(k in name for k in ["everlog", "icado", "studio1nha"]):
        copy_item(p, WS2 / "outputs" / p.name)

print("\n--- Workspace 2 file copy completed successfully ---")
