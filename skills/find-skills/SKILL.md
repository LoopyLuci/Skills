---
name: find-skills
description: Use when searching for agent skills to extend capabilities
tags: [skills, discovery, search, agent-capabilities]
related_skills: [skill-discovery, skill-catalog-navigation, skills-repo-publishing]
---

# Find Skills

Helps you discover and install agent skills from the open agent skills ecosystem.

## When to Use This Skill

Use when the user:
- Asks "how do I do X" where X might have an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem.

**Key commands:**
- `npx skills find [query] [--owner <owner>]` — Search for skills
- `npx skills add <package>` — Install a skill
- `npx skills update` — Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need
Identify the domain (React, testing, design) and specific task.

### Step 2: Check the Leaderboard First
Check skills.sh leaderboard before running CLI search.

### Step 3: Search for Skills
```bash
npx skills find react performance
npx skills find pr review
npx skills find changelog
```

### Step 4: Verify Quality Before Recommending
- Check install count (prefer 1K+ installs)
- Source reputation (official sources more trustworthy)
- GitHub stars (skepticism under 100 stars)

### Step 5: Present Options
Show name, description, install count, and install command.

### Step 6: Offer to Install
```bash
npx skills add <owner/repo@skill> -g -y
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Recommending without verifying | Always check install count and source reputation |
| Searching too broadly | Use specific keywords for better results |
| Not checking skills.sh first | Leaderboard has pre-vetted options |
| Installing untrusted sources | Verify source before installing |

## Verification Checklist

- [ ] Understood user's specific need
- [ ] Checked skills.sh leaderboard first
- [ ] Searched with specific keywords
- [ ] Verified skill quality (installs, source reputation)
- [ ] Presented install command to user
- [ ] Installed only after user approval
