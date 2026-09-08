# Everest & D2C/SME SEO Workspace Instructions

## Workspace Purpose

This repository is an independent monorepo for:

- SEO research, outlines, and content production for:
  - **Everest Logistics** (B2B freight, customs clearance, international freight forwarding).
  - **ICADO** (D2C activewear, gym, yoga, and running sportswear).
  - **May Mặc CTH** (B2B uniform manufacturing, fabric specs, local SEO Hải Phòng).
  - **Studio 1 Nhà** (Wedding photography, bridal makeup, pre-wedding visual concepts).
- Brand personas, writing standards, and shared reference data.
- Independent web application: `projects/everest-logistics` (Next.js freight & customs portal).
- Reusable rank checking and SEO reporting tools.

Do not treat the repository root as a single npm application.

## Source of Truth

Before changing workspace structure or topic metadata, read:

1. `README.md` for the workspace architecture.
2. `workspace.toml` for canonical paths, workflows, and required artifacts.
3. `scripts/workspace.py` for validation and governance behavior.
4. The relevant brand references under `data/reference/persona-brand/`.
5. The relevant workflow under `.agent/workflows/` or skill under `.agents/skills/`.

## Workspace Layout

- `clients/`: Canonical client and SEO topic work (`Everest-Logistics`, `ICADO`, `MayMacCTH`, `Studio1Nha`).
- `data/reference/`: Shared brand personas, standards, and research.
- `projects/`: Independent application source code (`everest-logistics`).
- `tools/`: Reusable tools such as rank checking and GSC dashboards.
- `scripts/`: Workspace-wide automation.
- `outputs/`: Generated reports, GSC plans, and keyword clusters.
- `archive/`: External archive index; archive payloads are not stored in Git.
- `tests/`: Workspace governance tests.

## Canonical SEO Topic Structure

The canonical topic path is:

`clients/<client>/brands/<brand>/keywords/<slug>/`

Each topic must contain `topic.toml`.

Canonical topic artifacts are:

- `search-intent.md`
- `research.md`
- `competitor-insights.md`
- `outline.md`
- `fact-check-report.md`
- `article.md`
- `audit-report.md`

## Validation

Run:

```bash
python3 scripts/workspace.py validate
python3 -m unittest discover -s tests
```
