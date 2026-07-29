---
name: skill-audit-and-gap-analysis
description: "Skill audit: review, find gaps, draft skills."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, audit, gap-analysis, meta, curation]
    related_skills: [workflow-automation-skill, hermes-agent-skill-authoring]
---

# Skill Audit & Gap Analysis

## Overview
Meta-skill for maintaining Hermes skill library health. Reviews existing skills against project needs and user workflows, identifies gaps, suggests new skills with priority scoring, and generates SKILL.md drafts for promising candidates.

## When to Use
- Auditing your current skill library for coverage
- Identifying gaps between available skills and your workflows
- Prioritizing which new skills to create first
- Drafting SKILL.md for high-priority skill candidates
- Pruning redundant or rarely-used skills
- Reviewing skill health (outdated commands, stale workflows)

## Body

### 1. Step 1: Inventory Current Skills

Use `skills_list()` to catalog all existing skills. Categorize each:

| Category | Definition | Action |
|----------|------------|--------|
| **Active** | Used frequently in sessions | Keep, maintain |
| **Rarely used** | Loaded but never triggered | Consider pruning or merging |
| **Outdated** | Stale commands, obsolete workflows | Patch or rewrite |
| **Overlapping** | Multiple skills covering the same ground | Merge into one, delete others |

### 2. Step 2: Map User Workflows

Ask the user or infer from session history about recurring tasks:
- "What do you spend the most time on?"
- "What repetitive tasks do you wish were automated?"
- "What's a task where output is inconsistent?"
- Look at recent sessions for patterns (session_search)

**Workflow capture template:**
```yaml
workflow:
  name: "Weekly reporting"
  frequency: "Every Monday"
  steps: ["Pull data from API", "Transform in Python", "Generate PDF", "Email to team"]
  existing_skill: false  # false = gap!
```

### 3. Step 3: Identify Gap Categories

| Gap Type | Description | Example |
|----------|-------------|---------|
| **Domain gap** | Entire field not covered | No real estate skills for an investor user |
| **Depth gap** | Skill exists but lacks depth | SEO skill missing technical SEO |
| **Integration gap** | Skills don't compose | Blogging skill doesn't trigger repurposing |
| **Platform gap** | Covers web only, misses mobile | Social media skill ignores TikTok |
| **Audience gap** | Wrong audience assumed | Marketing skill for B2C when user is B2B |
| **Automation gap** | Manual workflow with no skill | User runs 10 terminal commands weekly |

### 4. Step 4: Prioritize Gaps

Score each candidate on 3 axes (1–5):

| Criterion | 1 | 2 | 3 | 4 | 5 |
|-----------|---|---|---|---|---|
| **Frequency** | Yearly | Quarterly | Monthly | Weekly | Daily |
| **Impact** | Marginal | Minor | Moderate | Significant | Transformative |
| **Effort** | 10+ hours | 6–9h | 3–5h | 1–2h | <1h |

**Priority Score = (Frequency × Impact) / Effort**

- Score ≥ 5: Build immediately
- Score 3–4: Build soon
- Score < 3: Defer or skip

### 5. Step 5: Draft SKILL.md for Top Candidates

For each high-priority candidate, create:

**Frontmatter:**
```yaml
---
name: skill-name
description: "Use when <trigger>. <one-line behavior.>"  # Max 60 chars total
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tag1, tag2, tag3]
    related_skills: [existing-skill-1, existing-skill-2]
---
```

**Body structure:** Overview → When to Use → Workflow/Steps (numbered, with exact commands) → Common Pitfalls → Verification Checklist.

### 6. Cleanup: Pruning & Merging

**When to prune a skill:**
- Not triggered in 30+ sessions
- Content is fully covered by another skill
- Workflow is now handled by built-in tools
- Auth credentials/API keys no longer valid

**When to merge:**
- Multiple skills share >50% of triggers
- Skills are subtypes of a larger domain

Use `skill_manage(action='delete', name='...', absorbed_into='umbrella-skill')` to delete with forwarding.

## Common Pitfalls

- **Auditing without asking the user**: The user knows their workflow best. Always ask about recurring tasks.
- **Creating skills no one will use**: Every skill has a maintenance cost (system prompt budget). Create only for high-frequency triggers.
- **Skipping effort estimation**: A huge-impact skill that takes 20 hours should be planned, not rushed.
- **Ignoring existing skills**: Extending a skill is usually better than creating a sibling.
- **Skill debt**: New skills bloat the system prompt index. Prune unused or redundant skills.

## Verification Checklist

- [ ] Complete inventory of existing skills via skills_list()
- [ ] User workflows mapped (ask user or infer from history)
- [ ] Gap categories identified (domain/depth/integration/platform/audience/automation)
- [ ] 5+ candidate gaps scored (Frequency × Impact / Effort)
- [ ] Top 3 candidates have SKILL.md frontmatter drafted
- [ ] Redundant/outdated skills identified for pruning or merging
- [ ] User shown the plan and asked for feedback before creation