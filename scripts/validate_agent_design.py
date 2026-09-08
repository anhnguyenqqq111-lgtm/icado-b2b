#!/usr/bin/env python3
"""Validate local SEO flows and skills for broken contracts and duplicate sources."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / ".agent"
SKILLS = AGENT / "skills"
DEPRECATED_TOOLS = ("browser_subagent", "search_web", "web_search", "read_url_content", "view_file")
LEGACY_ALIASES = {
    "analyzing-competitors": "common/analyzing-competitors",
    "analyzing-search-intent": "common/analyzing-search-intent",
    "auditing-content": "common/auditing-content",
    "client-approval-gate": "common/client-approval-gate",
    "competitor-content-scraping": "common/competitor-content-scraping",
    "competitor-outline-intelligence": "common/competitor-outline-intelligence",
    "content-gap-analysis": "common/content-gap-analysis",
    "enforcing-zero-flair": "common/enforcing-zero-flair",
    "extracting-keywords": "common/extracting-keywords",
    "faq-research": "common/faq-research",
    "generating-outlines-home-credit": "brands/home-credit/generating-outlines-home-credit",
    "generating-tabular-outline-hc": "brands/home-credit/generating-tabular-outline-hc",
    "hc-outline-rules": "brands/home-credit/hc-outline-rules",
    "home-credit-content": "brands/home-credit/home-credit-content",
    "internal-link-recommendation": "common/internal-link-recommendation",
    "keyword-expansion": "common/keyword-expansion",
    "keyword-strategy-mapping": "common/keyword-strategy-mapping",
    "outline-quality-scoring": "common/outline-quality-scoring",
    "rechecking-facts": "common/rechecking-facts",
    "research-internal-links": "common/research-internal-links",
    "verifying-financial-logic": "brands/home-credit/verifying-financial-logic",
    "writing-semantic-content": "common/writing-semantic-content",
}
PATH_RE = re.compile(r"`((?:data|clients|\.agent|tools)/[^`]+)`")


def is_dynamic(path: str) -> bool:
    return any(marker in path for marker in ("<", "[", "*"))


def main() -> int:
    errors: list[str] = []
    markdown = sorted(AGENT.rglob("*.md"))
    for path in sorted(SKILLS.rglob("SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"empty skill: {path.relative_to(ROOT)}")
            continue
        if not text.startswith("---\n"):
            errors.append(f"missing frontmatter: {path.relative_to(ROOT)}")
            continue
        _, _, remainder = text.partition("---\n")
        frontmatter, marker, _ = remainder.partition("---\n")
        if not marker or not re.search(r"^name:\s*[^\s]+", frontmatter, re.MULTILINE):
            errors.append(f"invalid skill name: {path.relative_to(ROOT)}")
        if not marker or not re.search(r"^description:\s*.+", frontmatter, re.MULTILINE):
            errors.append(f"missing skill description: {path.relative_to(ROOT)}")

    for path in markdown:
        text = path.read_text(encoding="utf-8")
        for tool in DEPRECATED_TOOLS:
            if tool in text:
                errors.append(f"deprecated tool token `{tool}`: {path.relative_to(ROOT)}")
        for reference in PATH_RE.findall(text):
            reference = reference.rstrip(".,:;)")
            if not is_dynamic(reference) and not (ROOT / reference).exists():
                errors.append(f"missing reference `{reference}`: {path.relative_to(ROOT)}")

    for alias, canonical in LEGACY_ALIASES.items():
        alias_path = SKILLS / alias
        if not alias_path.is_symlink() or alias_path.resolve() != (SKILLS / canonical).resolve():
            errors.append(f"legacy alias must link to {canonical}: {alias_path.relative_to(ROOT)}")

    if errors:
        print("\n".join(f"ERROR {item}" for item in errors))
        return 1
    print(f"OK: {len(markdown)} flow/skill Markdown files validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
