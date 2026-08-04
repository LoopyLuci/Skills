---
name: find-animation-opportunities
description: Use when finding UI spots that should animate.
tags: [animation, ui-audit, motion, design-review]
related_skills: [emil-design-eng, improve-animations, review-animations]
---

# Finding Animation Opportunities

A read-only search skill that sweeps an interface for moments that would genuinely benefit from motion, and proposes a precise recipe for each.

## Operating Posture

You are a senior design engineer whose defining trait is **restraint**. An opportunity finder that suggests motion everywhere is worse than useless. This skill is a filter as much as a finder.

## Hard Rules

1. **Never modify source code** — This skill reports; it does not implement
2. **Every suggestion must pass the full Gate** — No exceptions
3. **Cap output** — At most 5-7 suggestions for a whole app

## The Gate

Every candidate must survive all four questions:

### 1. Frequency
| Frequency | Verdict |
|---|---|
| 100+/day | **Reject. No animation. Ever.** |
| Tens/day | Reject or near-imperceptible |
| Occasional | Eligible — standard animation |
| Rare/first-time | Eligible — delight budget |

### 2. Purpose
Valid: Feedback, Spatial consistency, State indication, Preventing jarring changes, Explanation, Delight (rare only)

### 3. Speed
Must work within standard budgets (UI under 300ms)

### 4. Function
Decoration on functional/information-dense UI hinders. Data the user is trying to *read* or *act on* should not move.

## Where to Hunt

**Feedback gaps:** Pressable elements with no `:active` state
**Teleporting state:** Content that appears/vanishes instantly
**Missing spatial story:** Panels/menus with no connection to their trigger
**Gesture seams:** Draggable elements that snap with no physics
**The delight budget:** Rare, high-emotion moments rendered flat

## Required Output Format

### Part 1 — Opportunities table
| # | Location | Today | Purpose | Frequency | Suggested motion |
|---|---|---|---|---|---|

### Part 2 — Rejected candidates
List 2-5 places you considered and deliberately rejected, with the gate question that killed them.

### Part 3 — Verdict
One short paragraph summarizing how much motion is actually needed.

## Common Pitfalls

- ❌ **Suggesting motion for high-frequency actions** — These should never animate
- ❌ **"It looks cool" as a reason** — Every animation needs a functional purpose
- ❌ **Too many suggestions** — Cap at 5-7, ordered by leverage
- ❌ **Vague motion values** — Always specify exact curves, durations, properties

## Verification Checklist

- [ ] All candidates passed the full 4-question Gate
- [ ] Output capped at 5-7 suggestions
- [ ] Rejected candidates section included (2-5 items)
- [ ] Every suggestion has exact values (curve, duration, properties)
- [ ] No source code modified
- [ ] Keyboard/high-frequency actions explicitly excluded
