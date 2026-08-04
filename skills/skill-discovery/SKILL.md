---
name: skill-discovery
description: "Use when discovering, designing, or developing skills."
category: software-development
tags: [skills, meta, discovery, design, development, best-practices]
---
# Skill Discovery — Design & Development Meta-Skill

A systematic approach to discovering, designing, developing, and managing skills.

## 1. When to Create a Skill

Create a skill when you've done something **3+ times** or it took **5+ tool calls** and would benefit from being repeatable. Specifically:

| Trigger | Example |
|---------|---------|
| Complex multi-step task succeeded | 7-phase Docker removal |
| Error overcome after iteration | Fixed `$var:` colon scope in PS7 |
| User corrected your approach | "Use flat string not array for ArgumentList" |
| Non-trivial workflow discovered | Multi-stage Docker builds with caching |
| Recurring task type | "Set up a new dev environment" |
| Configuration reference needed | "How to configure CMake on Windows" |

## 2. Skill Discovery Process

When faced with any task, systematically check:

```
1. skills_list() — browse all existing skills by category
2. skill_view(name) — load relevant skills
3. session_search("topic") — check past conversations for learned lessons
4. memory — check persistent notes about user/workflow preferences
```

### Discovery Heuristics

For ANY task the user asks about, ask:

- **Is this a recurring workflow?** (Git operations, Docker management, C++ builds)
- **Does it have a standard procedure?** (Setting up projects, debugging patterns)
- **Were there pitfalls I should remember?** (Encoding issues, UAC elevation, quoting)
- **Did the user correct me?** (That's a skill in waiting!)

### Category Mapping

Skills map to categories based on domain:

```
docker/          — Docker, Compose, Swarm, Buildx, containers
software-development/  — PS modules, build tools, WSL2, Windows tools
networking/      — DNS, firewall, VPN
mlops/           — ML training, model serving
productivity/    — Office documents, PDFs, spreadsheets
creative/        — ASCII art, diagrams, video
research/        — ArXiv, web scraping, blog monitoring
note-taking/     — Obsidian, note management
```

## 3. Skill Anatomy

Every skill has two mandatory parts:

### Frontmatter (YAML)

```yaml
---
name: skill-name-here       # lowercase-hyphens, max 64 chars
description: "Use when <trigger>. <one-line behavior>."  # MAX 60 CHARS!
category: software-development   # single category
tags: [tag1, tag2, tag3]    # discoverability tags
---
```

### Description Rules (CRITICAL)

Descriptions are truncated at 57 chars + "..." in the system prompt index.
They MUST follow this exact pattern:

```
"Use when <trigger condition>. <what it does briefly>."
```

Examples:
- ✅ `"Use when removing all Docker traces from Windows. 7-phase."` (56 chars)
- ✅ `"Use when building PS admin tools. BOM, UAC, PS5/7."` (55 chars)
- ✅ `"Use when managing container/image/volume/network lifecycles."` (60 chars)
- ❌ `"A production-grade, interactive PowerShell script for comprehensive Docker management..."` (too long)

### Body Structure

```markdown
# Title
Brief intro paragraph.

## Section (commands, patterns, reference)
```command
Actual code here
```

## Pitfalls
- Bullet list of gotchas
- Each one is a specific failure mode
```

## 4. Skill Design Principles

### 1. Trigger-First Naming
Name should immediately tell the agent when to load it:
- `docker-compose-patterns` → "Load when writing docker-compose.yml"
- `powershell-error-handling` → "Load when writing try/catch blocks"

### 2. Shallow But Wide
Cover the 80% case for each topic. Don't try to be a complete reference.
- Good: "Here are the 10 most common docker commands grouped by lifecycle"
- Bad: "Here is every Docker command and all 47 flags"

### 3. Exact Commands, Not Descriptions
Always provide copy-paste-ready code blocks:
- ✅ `docker stop $(docker ps -aq)` 
- ❌ "You should stop all containers using the docker stop command"

### 4. Pitfalls Section Is Mandatory
Every skill must end with `## Pitfalls` containing 3-10 bullet points.
These are the hard-won lessons that save time on the next attempt.

## 5. Writing Great Descriptions (≤60 chars)

The 60-char limit is strictly enforced. Use these patterns:

```
"Use when <noun>.<purpose>"
"Use when <verb>.<context>"
"Use when <task> via <tool>."
```

| Length | Description |
|--------|-------------|
| 60 | "Use when managing container/image/volume/network lifecycles." |
| 59 | "Use when orchestrating multi-service Docker environments." |
| 57 | "Use when removing all Docker traces from Windows. 7-phase." |
| 56 | "Use when debugging Docker network connectivity issues." |
| 53 | "Use when installing software via winget, choco, or scoop." |
| 50 | "Use when building C++ projects with CMake on Windows." |
| 48 | "Use when configuring Docker Desktop WSL2 backend on Windows." |

Check length before creating: `"Use when ...".Length`

## 6. Skill Lifecycle

```
DISCOVERY → DESIGN → CREATE → VALIDATE → USE → MAINTAIN → (UPDATE | MERGE | DELETE)
```

### CREATE
```powershell
skill_manage(action='create', name='my-skill', 
    content='# Full SKILL.md...', 
    category='software-development')
```

Or write directly:
```powershell
New-Item -Path "$env:LOCALAPPDATA\hermes\skills\<category>\<name>\SKILL.md"
```

### VALIDATE
After creating, verify:
1. `skills_list()` shows the skill with truncated description
2. `skill_view(name='my-skill')` loads the full content
3. The description starts with "Use when..." and is under 60 chars
4. The body has code examples and a pitfalls section

### UPDATE (PATCH)
When a skill has stale info:
```powershell
skill_manage(action='patch', name='my-skill',
    old_string='old wrong command',
    new_string='correct command')
```

### MERGE
When two skills overlap:
1. Create umbrella skill with consolidated content
2. Delete original skills with `absorbed_into='umbrella-skill'`

### DELETE
```powershell
skill_manage(action='delete', name='stale-skill',
    absorbed_into='')  # empty = prune, no forwarding
# OR
skill_manage(action='delete', name='old-skill',  
    absorbed_into='umbrella-skill')  # consolidating
```

## 7. Skill Discovery Checklist

When given ANY user task, run this checklist:

```
[ ] 1. Scan skills_list() for matching categories
[ ] 2. Load relevant skills with skill_view()
[ ] 3. Did skill cover the task?
      YES → follow it exactly
      NO → continue
[ ] 4. Is this a 5+ call / recurring workflow?
      YES → plan to create a skill after completion
      NO → just complete the task
[ ] 5. After completing task:
      [ ] Were there pitfalls? → add to skill
      [ ] Is this new? → create skill
      [ ] Was existing skill wrong? → patch it
[ ] 6. Ask user: "Save this as a skill?"
```

## 8. Advanced: Skill Development Patterns

### Mirroring the User's Workflow
If the user routinely does X, Y, Z together, wrap it in a skill:
```
"Use when setting up Docker + WSL2 + VS Code on a clean Windows machine."
```

### Error-to-Skill Pipeline
Every error you fix is a potential skill:
1. Hit error → fix error → document fix → create skill
2. Hit error again → load skill → fix in seconds

### Skill Chaining
Some tasks need multiple skills. Reference them:
```
See also: docker-wsl2-integration, docker-lifecycle-management
```

## 9. Testing Skills

After creating/updating a skill:

```powershell
# Verify it loads
skill_view(name='my-skill')

# Verify it appears in list
skills_list() | Where-Object { $_.name -match 'my-skill' }

# Follow the skill yourself to verify steps work
# If steps fail, patch immediately
```

## Pitfalls

- **Descriptions over 60 chars** are rejected by skill_manage
- **No `skills_list` call before acting** leads to duplicated effort
- **No pitfalls section** means the skill is incomplete
- **Outdated commands** (e.g., v1 docker-compose) slip in -- patch on discovery
- **Overly detailed skills** become reference docs, not quick-lookup procedures
- **Skipping the "ask user" step** creates skills nobody wants
- **Not checking for existing skills** before creating creates duplicates
