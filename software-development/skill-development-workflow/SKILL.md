---
name: skill-development-workflow
description: "Use when building authoring, testing, and iterating skills."
category: software-development
tags: [skills, development, authoring, testing, workflow]
---
# Skill Development Workflow

End-to-end process for authoring, testing, iterating, and deprecating skills.

## Authoring Flow

```
IDEA → SKETCH → DRAFT → VALIDATE → PUBLISH → ITERATE → (DEPRECATE | ARCHIVE)
```

### 1. IDEA — Identify the Gap
- Task took 5+ tool calls? → Skill candidate
- User corrected your approach? → Skill candidate
- Recurring configuration pattern? → Skill candidate

### 2. SKETCH — Outline
```markdown
# Title
<!-- 1-2 line description -->

## When to Use
<!-- 3-5 bullet conditions -->

## Steps
<!-- numbered steps with code -->

## Pitfalls
<!-- 3-8 failure modes -->
```

### 3. DRAFT — Write SKILL.md
Place under `%LOCALAPPDATA%\hermes\skills\<category>\<name>\SKILL.md`.
Category determines `skills_list(category=X)` grouping.

### 4. VALIDATE — Checklist
- [ ] Description starts with "Use when..." and is ≤60 chars
- [ ] Description ends with a period
- [ ] YAML frontmatter has name, description, category, tags
- [ ] Body has code examples (not just descriptions)
- [ ] Has pitfalls section
- [ ] Cross-references related skills

### 5. PUBLISH
```powershell
skill_manage(action='create', name='my-skill', 
    content='...', category='my-category')
```

### 6. ITERATE — Patch on Error
```powershell
skill_manage(action='patch', name='my-skill',
    old_string='wrong info',
    new_string='correct info')
```

### 7. DEPRECATE / ARCHIVE
```powershell
skill_manage(action='delete', name='old-skill',
    absorbed_into='new-skill')  # forward users
# or
skill_manage(action='delete', name='stale-skill',
    absorbed_into='')  # prune
```

## Pitfalls

- Don't publish without testing each code block
- Old skills silently degrade when tools/APIs change — audit quarterly
- Deleting a skill breaks cron jobs that reference it — deprecate first
- Descriptions truncated at 57 chars — lead with the trigger
- Category choice affects discovery — keep it consistent
