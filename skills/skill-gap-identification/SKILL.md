---
name: skill-gap-identification
description: Detect when a skill is missing and request or create one.
---

# Skill Gap Identification

**Trigger**: Use when you're about to do a task from scratch and realize no skill covers it, or when you struggle through something that should have been automated.

## Gap Detection Patterns

```markdown
Notice these signals:

SIGNAL 1: "I've done this before but there's no skill"
  → You wrote similar code twice → skill gap
  
SIGNAL 2: "I'm looking up the same docs again"
  → You keep searching for the same commands → skill gap
  
SIGNAL 3: "I keep making the same mistake"
  → You hit the same pitfalls repeatedly → skill gap
  
SIGNAL 4: "This took longer than it should"
  → A 5-minute task took 30 minutes → skill gap

SIGNAL 5: "The user corrected me on this before"
  → Memory says user corrected this approach → skill gap
```

## Gap Assessment

```markdown
Potential gap detected: "<topic>"
        │
   ┌────▼────────────┐
   │ Does a skill    │
   │ exist but I     │──YES──► Load it now, no gap
   │ missed it?      │
   └────┬────────────┘
        │ NO
   ┌────▼─────────────┐
   │ Is this a        │
   │ one-off task?    │──YES──► No gap needed, one-off
   │ (won't repeat)   │
   └────┬─────────────┘
        │ NO
   ┌────▼─────────────┐
   │ Is this a        │
   │ ~5 step process  │──YES──► Skill needed, propose creation
   │ with clear steps?│
   └────┬─────────────┘
        │ NO
   ┌────▼─────────────┐
   │ Too complex or   │──YES──► Decompose into sub-skills
   │ too simple?      │
   └────┬─────────────┘
        │ UNCLEAR
   └──► Note for later
```

## Gap Documentation Template

```markdown
When you identify a gap, document it:

GAP REPORT
──────────
Topic:       <what the skill would cover>
Trigger:     "Use when <specific situation>"
Steps count: <how many steps typically involved>
Frequency:   <daily/weekly/monthly — how often you'd use it>
Commands:    <key commands or tools involved>
Pitfalls:    <common mistakes you know about>
---

Then propose creation: "I don't have a skill for this yet.
Should I create one?"
```

## Real-World Gap Analysis

```markdown
TASK: "Deploy a Redis cluster with sentinel"
──────────────────────────────────────────

EXISTING SKILLS SCAN:
  redis-caching-patterns        → cache usage, not deployment
  dockerfile-optimization       → Docker build, not Redis config
  kubernetes-deployment         → general k8s, not Redis-specific
  
GAP: No skill for "Redis deployment and configuration"
  
GAP REPORT:
  Topic:    Redis cluster deployment
  Trigger:  "Use when deploying Redis with sentinel or cluster mode"
  Steps:    ~8 (install, configure master, configure replicas,
            set up sentinels, test failover, monitor)
  Commands: redis-cli, redis-sentinel, redis.conf
  Pitfalls: Network partitions, split-brain, memory limits

PROPOSAL: Create skill "redis-cluster-deployment"?
```

## When to Propose vs. When to Auto-Create

```markdown
PROPOSE to the user (ask permission):
- Complex domain you're not fully confident in
- Task the user specifically asked about
- First time encountering the need

AUTO-CREATE (with confirmation):
- You've completed a 5+ step task successfully
- You hit and resolved errors during the task
- The process had clear, repeatable steps
- You know the pitfalls from first-hand experience

Use /learn for fast skill creation from source material:
  /learn how I just set up Redis clustering
```

## Pitfalls
- **Over-identification**: Not every 2-step process needs a skill — reserve for complex/repeated tasks
- **Skill overlap**: Proposed skill might overlap 80% with an existing skill — consider patching instead
- **Scope creep**: A gap report that covers 3 different domains should be 3 skills, not 1
- **Premature creation**: Creating a skill after doing something once — wait until you've repeated it

## Verification
```markdown
After creating a skill for a gap:
- Does it cover the gap you identified?
- Does it include the pitfalls you learned?
- Has using it saved time on the next similar task?
```
