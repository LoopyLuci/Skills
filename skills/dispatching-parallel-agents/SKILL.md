---
name: dispatching-parallel-agents
description: Use when dispatching subagents for parallel independent tasks
tags: [subagents, parallel, delegation, testing]
related_skills: [subagent-driven-development, executing-plans]
---

# Dispatching Parallel Agents

## Overview

You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They should never inherit your session's context or history — you construct exactly what they need.

**Core principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

## When to Use

- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:** Failures are related (fix one might fix others), need to understand full system state, or agents would interfere with each other.

## The Pattern

### 1. Identify Independent Domains
Group failures by what's broken — each domain should be independent.

### 2. Create Focused Agent Tasks
Each agent gets: specific scope, clear goal, constraints, expected output.

### 3. Dispatch in Parallel
Issue all subagent dispatches in the same response — they run in parallel.

### 4. Review and Integrate
When agents return: read summaries, verify fixes don't conflict, run full test suite.

## Code Example: Good Agent Prompt

```
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:

1. "should abort tool with partial output capture"
2. "should handle mixed completed and aborted tools"
3. "should properly track pendingToolCount"

These are timing/race condition issues. Your task:
1. Read the test file and understand what each test verifies
2. Identify root cause - timing issues or actual bugs?
3. Fix by replacing arbitrary timeouts with event-based waiting

Do NOT just increase timeouts - find the real issue.
Return: Summary of what you found and what you fixed.
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too broad scope ("Fix all the tests") | Scope to one file or subsystem per agent |
| No context provided | Always include error messages and test names |
| No constraints given | Specify "Do NOT change production code" or similar |
| Vague output expectations | Request specific output format: "Return summary of root cause and changes" |
| Dispatching related failures together | Investigate related failures together first — fixing one might fix others |

## Verification Checklist

- [ ] Verified tasks are truly independent (no shared state)
- [ ] Each agent has focused scope (one file/subsystem)
- [ ] Each agent has clear goal and constraints
- [ ] All dispatches issued in same response for parallel execution
- [ ] Reviewed each agent's summary upon return
- [ ] Checked for conflicts between agent changes
- [ ] Ran full test suite after integration
