---
name: workflow-automation-skill
description: "Automation: identify tasks, design, implement."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [automation, workflow, scripts, efficiency, meta]
    related_skills: [ai-agent-integration-workflow, skill-audit-and-gap-analysis, freelance-business-operations]
---

# Workflow Automation Skill

## Overview
Meta-skill for identifying, designing, and implementing automations in Hermes. Spot repetitive tasks, design the automation, choose the right tool (cron job, script, Hermes skill, delegate), implement, test, and document.

## When to Use
- Automating a repetitive manual task
- Creating a script for a weekly workflow
- Setting up a scheduled (cron) job
- Building a Hermes skill for a triggered workflow
- Deciding whether to automate vs keep manual
- Documenting an automation for reuse

## Body

### 1. Automation Decision Tree

```
Is this task repetitive?
├── No → Skip (do manually)
└── Yes → How often?
    ├── One-time batch → Write script (terminal or execute_code)
    ├── Scheduled (daily/weekly/monthly) → cron job (cronjob tool)
    ├── Triggered by user intent → Hermes skill (skill_manage create)
    └── Complex multi-step reasoning → delegate_task (parallel subagents)
```

### 2. Automation Types & Tools

| Type | Tool | Best For | When |
|------|------|----------|------|
| **One-shot script** | terminal or execute_code | Import/export, transform, batch process | Now |
| **Scheduled task** | cronjob tool | Daily reports, data collection, monitoring | Recurring |
| **Agent workflow** | Hermes skill | Semantic trigger → structured output | User-requested |
| **Parallel processing** | delegate_task | N independent subtasks concurrently | Complex projects |
| **File watcher** | cron + script | Generate report when file changes | Data pipelines |

### 3. Workflow Detection Checklist

Ask these 5 questions. If YES to 3+, it's automatable:

1. Do you do this more than once a month?
2. Does it follow the same steps each time?
3. Are the inputs predictable (format, location)?
4. Is the output well-defined (report, file, notification)?
5. Does it take more than 5 minutes to do manually?

### 4. Automation Implementation Template

**Step 1 — Define the workflow:**
```yaml
task: "Name"
trigger: "Time-based | File-change | User request"
input: "Data source, format, location"
steps:
  - "1. Collect"
  - "2. Transform"
  - "3. Generate"
  - "4. Deliver"
output: "Report, file, notification, dashboard update"
frequency: "One-time | Daily | Weekly | Monthly"
```

**Step 2 — Choose tool:**
- Data collection → `web_extract` + `terminal` (curl)
- Data processing → `execute_code` (Python/pandas)
- Output generation → `pdf`, `xlsx`, `docx`, or markdown
- Delivery → Email (himalaya skill), webhook (curl), file save

**Step 3 — Build & test:**
- Write the script or skill content
- Run in dry-run mode first (no delivery, just verify output)
- Check error paths (what if API fails? file not found?)

**Step 4 — Deploy & monitor:**
- For cron: `cronjob(action='create', schedule=..., prompt=..., script=...)`
- For skills: `skill_manage(action='create', name=..., content=...)`
- Check first 3 runs for correctness

**Step 5 — Document:**
- Comment header in scripts with purpose, inputs, outputs
- If a skill, ensure description is accurate and tags are set

### 5. Error Handling Patterns

```python
# Pattern: try/except with notification
try:
    result = perform_automation()
    notify("Success", result)
except Exception as e:
    notify("FAILED", str(e))
    # Don't leave the system in a broken state
    rollback()
```

**Always include:**
- What happens on API failure
- What happens on missing input
- What happens on partial data
- Notification (success AND failure)
- Idempotency (running twice produces same result)

### 6. Automation Anti-Patterns

- **Automating a broken workflow**: Make sure the manual process works before automating it.
- **No error handling**: The automation will fail eventually. Handle it gracefully.
- **Over-automating**: Tasks with frequent exceptions are better manual.
- **No documentation**: A script without comments is a puzzle 6 months later.
- **Silent failures**: User discovers the problem before you do. Always notify on failure.
- **No idempotency**: Running twice should not produce duplicate results or errors.

## Common Pitfalls

- **Automating too early**: Make sure the manual process is stable and well-understood first.
- **Choosing the wrong tool**: One-shot task → cron job wastes resources. Recurring task → one-shot script is unsustainable.
- **No rollback plan**: If the automation fails midway, the system should not be left in an inconsistent state.
- **Hardcoded values**: Every hardcoded path, API key, or email address is a maintenance trap. Use config files or env vars.
- **Forgetting to monitor**: Automations drift. Check first 3 runs, then sample monthly.

## Verification Checklist

- [ ] Task passes the automation test (repetitive, predictable, defined output)
- [ ] Tool selected (script/cron/skill/delegate) with rationale
- [ ] Implementation built and tested in dry-run mode
- [ ] Error handling for all failure modes (API, input, partial data)
- [ ] Notification on success AND failure
- [ ] Documented (comments, skill description, tag)
- [ ] First 3 runs monitored for correctness
- [ ] Rollback/remediation plan documented