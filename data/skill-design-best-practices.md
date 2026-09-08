# Claude Skill Design Best Practices

A comprehensive guide for creating effective AI skills that produce consistent, high-quality outputs. This guide combines official Anthropic specifications with battle-tested techniques from real-world skill development.

---

## Table of Contents

1. [What is a Skill?](#what-is-a-skill)
2. [Core Specification](#core-specification)
3. [Design Mindset](#design-mindset)
4. [The "Tease" Technique](#the-tease-technique)
5. [Self-Check Pattern](#self-check-pattern)
6. [Progressive Disclosure](#progressive-disclosure)
7. [Skill Patterns](#skill-patterns)
8. [Common Mistakes](#common-mistakes)
9. [Platform Considerations](#platform-considerations)
10. [Quick Reference](#quick-reference)

---

## What is a Skill?

A **skill** is a structured instruction set that guides AI behavior for a specific, repeatable task. Think of it as a playbook that transforms implicit knowledge into explicit, executable workflows.

**Skills ARE:**
- Reusable frameworks for repeated tasks
- Decision logic encoded in conditional flows
- Quality guardrails built into process
- Modular capabilities that can be combined

**Skills are NOT:**
- One-off prompts
- Generic instructions
- Tool tutorials

> **Mental Model:** Building a skill is like creating an onboarding guide for a highly capable but overconfident new hire. They're smart enough to figure things out—but sometimes too confident to follow instructions carefully.

---

## Core Specification

### The SKILL.md File

Every Claude Skill requires a `SKILL.md` file combining YAML frontmatter with Markdown instructions.

**⚠️ CRITICAL: File name is case-sensitive.**

| File Name | Status |
|-----------|--------|
| `SKILL.md` | ✅ **Correct** — Only this exact name works |
| `skill.md` | ❌ Will NOT be recognized |
| `Skill.md` | ❌ Will NOT be recognized |
| `SKILL.MD` | ❌ Will NOT be recognized |

### Required Frontmatter

```yaml
---
name: your-skill-name
description: >
  Brief description of what this Skill does and when to use it.
  Include trigger phrases that help Claude recognize when to activate.
---
```

**Name requirements:**
- Maximum 64 characters
- Only lowercase letters, numbers, and hyphens
- Cannot contain "anthropic" or "claude"
- Convention: Use gerund form (`processing-pdfs`, `analyzing-data`)

**Description formula:**
```
[What it does] + [When to use it] + [Trigger phrases]
```

**Weak description:**
```
This skill helps with documents.
```

**Strong description:**
```
Discover implicit workflows and convert them to explicit process maps.
Outputs: workflow diagram + skills list + orchestration plan.
Triggers: analyze my workflow, help me understand my process, /workflow
```

### Folder Structure

```
skill-name/
├── SKILL.md              # Required: Core instructions (CASE-SENSITIVE!)
├── references/           # Optional: Detailed docs, examples
│   ├── patterns.md
│   └── examples.md
├── scripts/              # Optional: Executable Python/Bash
│   └── validate.py
└── assets/               # Optional: Templates, resources
    └── template.docx
```

---

## Design Mindset

### The Overconfident Expert Problem

AI models (especially capable ones) tend to:
- Skip instructions they consider "obvious"
- Jump to solutions before gathering context
- Ignore guardrails when confident about approach

This isn't a bug—it's emergent behavior from training on expert-level content. Your skill design must account for this.

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Tease, don't command** | Make AI *need* to read instructions to proceed |
| **Encode decisions** | Use IF/THEN logic, not linear steps |
| **Build in checkpoints** | Force pauses before major transitions |
| **Constrain choices** | Too many options = paralysis or shortcuts |

---

## The "Tease" Technique

**Problem:** Direct commands get skipped by confident models.

**Solution:** Structure information so AI must read it to complete the task.

### Before vs After

| ❌ Direct Command | ✅ Tease Technique |
|-------------------|-------------------|
| "Ask the user: What is your goal?" | "User's goal is required before Phase 2. If not provided → gather it first." |
| "Follow these 5 steps in order" | "Phase 2 requires output from Phase 1. Check: do you have [X]?" |
| "Use this template for output" | "Output format depends on user context. See conditions below." |

### Implementation Pattern

Instead of:
```markdown
## Step 1: Ask Questions
Ask the user these questions:
1. What is your goal?
2. Who is your audience?
3. What format do you need?
```

Write:
```markdown
## Phase 1: Discovery

### Entry Conditions
```
IF user has not provided goal + audience + format:
    → Gather missing information (one question at a time)
    → Do not proceed until all three are confirmed

IF user has provided all three:
    → Proceed to Phase 2
```

### Questions to Gather (if needed)
| Need | Question |
|------|----------|
| Goal | "What outcome are you trying to achieve?" |
| Audience | "Who will consume this output?" |
| Format | "What format works best for your use case?" |
```

The AI must read the conditions to know what to do, rather than seeing "ask questions" and assuming it knows what that means.

### Placeholder Technique

Use generic placeholders in examples instead of realistic content:

```markdown
## File Naming Convention

Pattern: `{feature-name}-{type}.{ext}`

Examples:
- `user-auth-component.tsx`
- `payment-service.ts`
- `order-validator.py`
```

This teaches the AI the *pattern* rather than giving it specific examples it might copy inappropriately.

---

## Self-Check Pattern

Add a checklist at the end of your skill that the AI reads before responding.

### Template

```markdown
## Self-Check (Read before every response)

□ Have I gathered enough context?
  → If missing info: ask, don't assume

□ Am I asking one question at a time?
  → Multiple questions overwhelm users

□ Did I confirm before moving to next phase?
  → Never skip confirmation steps

□ Is my output actionable?
  → Theory without action = wasted effort

□ Does tone match brand voice?
  → [Insert specific tone guidelines]

□ Am I over-engineering?
  → Simple solution > comprehensive solution
```

### Why This Works

1. **Recency bias**: Information at the end of context gets more attention
2. **Explicit criteria**: Gives AI specific things to verify
3. **Prevents drift**: Long conversations lose track of guidelines
4. **Self-correction**: AI catches its own mistakes before responding

---

## Progressive Disclosure

Claude Skills use a three-tier loading system that minimizes token consumption:

| Level | When Loaded | Token Cost | Content |
|-------|-------------|------------|---------|
| **Level 1** | Always at startup | ~100 tokens | `name` and `description` only |
| **Level 2** | When skill triggers | <5k tokens | SKILL.md body |
| **Level 3** | As needed | Unlimited | Reference files, scripts |

### Design Implications

**Keep SKILL.md lean:**
- 500 lines maximum recommended
- Core logic and flow only
- Move detailed examples to `references/`

**Use references for:**
- Detailed templates
- Extended examples
- Edge case handling
- API documentation

**Use scripts for:**
- Deterministic operations
- Validation routines
- Data transformations
- File processing

### Example Structure

```
workflow-architect/
├── SKILL.md                    # ~300 lines: Core flow + conditions
└── references/
    ├── demo-case.md            # Full example conversation
    ├── scoring-framework.md    # Detailed evaluation criteria
    └── templates/
        └── output-formats.md   # Output structure templates
```

---

## Skill Patterns

### Pattern 1: Discovery Workflow

For skills that need to extract information before acting.

```markdown
## Phase 1: Discovery

### Entry Check
```
IF user provided: [specific context needed]
    → Proceed to Phase 2
ELSE
    → Gather missing information below
```

### Information Needed
| Item | How to Gather |
|------|---------------|
| Goal | "What are you trying to achieve?" |
| Context | "Tell me about [relevant background]" |
| Constraints | "Any limitations I should know about?" |

### Transition Criteria
All items gathered + user confirmed → Phase 2
```

### Pattern 2: Evaluation Framework

For skills that need to assess or score inputs.

```markdown
## Evaluation Framework

### Scoring Criteria

| Criterion | Question | Score 0-3 |
|-----------|----------|-----------|
| Frequency | How often does this repeat? | |
| Consistency | Is there a clear pattern? | |
| Automation | Can AI handle this? | |
| Time | How long does it take? | |
| Impact | How important is the output? | |

### Scoring Guide
- 0 = Not at all
- 1 = Slightly
- 2 = Moderately
- 3 = Highly

### Thresholds
- Score ≥ 12: High priority
- Score 8-11: Medium priority
- Score < 8: Low priority
```

### Pattern 3: Iterative Refinement

For skills that need multiple passes.

```markdown
## Refinement Process

### Pass 1: Draft
- Generate initial output based on inputs
- Focus on structure and completeness
- Note areas of uncertainty

### Pass 2: Review
```
FOR each section:
    Check against criteria in Self-Check
    IF issues found:
        Note issue
        Revise section
        Re-check
```

### Pass 3: Polish
- Verify tone and voice
- Ensure actionability
- Confirm with user before finalizing
```

### Pattern 4: Conditional Branching

For skills with multiple paths based on context.

```markdown
## Process Flow

### Route Selection
```
IF user is [Persona A]:
    → Use Template A
    → Focus on [specific aspects]
    → Output format: [format A]

IF user is [Persona B]:
    → Use Template B
    → Focus on [different aspects]
    → Output format: [format B]

IF unclear:
    → Ask: "Which describes you better: [A description] or [B description]?"
```

### Human Checkpoints
Mark points where human review is required:
- After [major step]: Review [what] because [why]
- Before [critical step]: Confirm [what] because [why]
```

### Pattern 5: Self-Learning

For skills that improve based on user feedback.

```markdown
## Self-Learning

### File lưu patterns
> `references/learned-patterns.md` — Skill tự động cập nhật

### Khi nào ghi nhận
```
SAU KHI output, NẾU user chỉnh sửa:
    → Phân tích: User thay đổi gì?
    → Ghi vào references/learned-patterns.md

Format:
| Date | Pattern | Context | Action |
|------|---------|---------|--------|
```

### Trước khi execute
```
LUÔN đọc references/learned-patterns.md (nếu có)

NẾU có patterns relevant:
    → Apply vào output
    → Mention: "Đã apply preferences: [X]"

NẾU conflict với yêu cầu hiện tại:
    → Hỏi: "Lần trước bạn prefer [X], lần này vẫn vậy?"
```

### User controls
```
NẾU user nói "reset preferences":
    → Xóa learned-patterns.md
    → Confirm: "Đã reset, sẽ học lại từ đầu"

NẾU user nói "show preferences":
    → Hiển thị nội dung learned-patterns.md
```
```

**Why Self-Learning Works:**
- Skills become personalized over time
- Reduces repetitive corrections
- User feels "understood" by the skill
- Creates stickiness — switching to another tool means losing learned preferences

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| **Wrong file casing** | Skill not discovered | Must be exactly `SKILL.md` |
| **Vague descriptions** | Unreliable triggering | Include specific triggers and boundaries |
| **Direct commands** | Instructions get skipped | Use tease technique with conditions |
| **No self-check** | Quality drift over conversation | Add checklist at end |
| **Context bloat** | Token exhaustion | Split into reference files |
| **Linear steps** | AI skips ahead | Use conditional logic |
| **No confirmation points** | Wrong outputs go unnoticed | Force pauses before transitions |
| **Too many options** | Decision paralysis | Provide defaults with escape hatches |
| **Assumed knowledge** | AI makes up details | Explicitly state what to gather |
| **Deep nesting** | Navigation confusion | Keep references one level deep |

---

## Platform Considerations

| Platform | Pre-built Skills | Custom Skills | Network | Packages |
|----------|------------------|---------------|---------|----------|
| **Claude.ai** | ✓ | ✓ (ZIP upload) | Varies | npm, PyPI |
| **Claude API** | ✓ | ✓ (`/v1/skills`) | **No** | Pre-installed |
| **Claude Code** | ✗ | ✓ (filesystem) | Full | Local |

### Claude.ai Deployment
- Upload as ZIP file via Settings → Capabilities → Skills
- Skills appear in skill selector for conversations

### Claude Code Deployment
```bash
# Personal skills (all projects)
~/.claude/skills/your-skill/SKILL.md

# Project skills (this project only)
.claude/skills/your-skill/SKILL.md
```

### API Deployment
Requires beta headers:
- `code-execution-2025-08-25`
- `skills-2025-10-02`
- `files-api-2025-04-14`

---

## Quick Reference

### File Naming

| Item | Rule | Example |
|------|------|---------|
| Main file | Exactly `SKILL.md` | ✅ `SKILL.md` ❌ `skill.md` |
| Folder | Lowercase + hyphens | ✅ `my-skill` ❌ `MySkill` |
| Scripts | Lowercase + underscores | ✅ `validate_data.py` |
| References | Lowercase + hyphens | ✅ `api-reference.md` |

### Technical Limits

| Constraint | Limit |
|------------|-------|
| SKILL.md length | 500 lines recommended |
| Name length | 64 characters |
| Description length | 1,024 characters |
| Skills per API request | 8 maximum |

### Description Formula

```
[Action verb] + [specific task] + [output type].
[When to use trigger].
Triggers: [comma-separated phrases]
```

### Starter Template

```markdown
---
name: your-skill-name
description: >
  [What it does in one sentence].
  [When to use it].
  Triggers: [trigger phrase 1], [trigger phrase 2], /command
---

# Skill Name

## Purpose
[One paragraph explaining the problem this skill solves]

## Process

### Phase 1: [Name]

#### Entry Check
```
IF [condition]:
    → Proceed to Phase 2
ELSE
    → [Gather what's needed]
```

#### Actions
[What to do in this phase]

### Phase 2: [Name]
[Continue pattern...]

## Self-Check (Read before every response)

□ [Checkpoint 1]
□ [Checkpoint 2]
□ [Checkpoint 3]
```

---

## Resources

**Official Documentation:**
- Overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Best Practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code Skills: https://code.claude.com/docs/en/skills

**Repositories:**
- Official Skills: https://github.com/anthropics/skills
- Community Collection: https://github.com/travisvn/awesome-claude-skills

**Open Standard:**
- Agent Skills Specification: https://agentskills.io

---

*Version 1.0 — January 2026*
