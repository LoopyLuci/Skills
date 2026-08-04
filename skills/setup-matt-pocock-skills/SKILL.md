---
name: setup-matt-pocock-skills
description: Use when setting up Matt Pocock skills in a new workspace or project
tags: [setup, onboarding, configuration, matt-pocock, workspace]
related_skills: [writing-great-skills, ask-matt, wayfinder]
---

# Setup Matt Pocock Skills

Configure a new workspace with the full Matt Pocock skillset: issue trackers, domain files, triage labels, and cross-skill integration.

## Setup Steps

### 1. Check for existing domain files
Look for CONTEXT.md, UBIQUITOUS_LANGUAGE.md, and existing ADRs before creating new ones.

### 2. Configure issue tracker
Setup the issue tracker configuration for the project. Create docs/agents/issue-tracker.md with the appropriate commands for the issue tracker being used (GitHub, GitLab, or local file-based).

### 3. Configure triage labels
If using GitHub or GitLab, configure triage labels for classifying issues.

### 4. Verify cross-skill integration
Ensure that skills reference correct paths and domain files are readable by dependent skills.

## Common Pitfalls

- **Missing issue-tracker configuration**: The issue tracker setup is critical for skills like code-review and to-tickets. Do not skip this step.
- **Not checking for existing domain files**: Always check for existing CONTEXT.md, ADRs, or UBIQUITOUS_LANGUAGE.md before creating new ones.
- **Forgetting cross-skill references**: Other skills reference the outputs of this setup (domain files, issue tracker docs). Verify they resolve correctly.

## Verification Checklist

- [ ] Issue tracker configured (docs/agents/issue-tracker.md exists)
- [ ] Domain files checked for existing content
- [ ] Triage labels configured if applicable
- [ ] Cross-skill references verified
