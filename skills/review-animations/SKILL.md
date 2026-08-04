---
name: review-animations
description: Use when reviewing animation code against a high craft bar.
tags: [animation, code-review, motion, performance, accessibility]
related_skills: [emil-design-eng, apple-design, improve-animations]
---

# Reviewing Animations

A specialized review skill that checks animation and motion code against a high craft bar. Default to flagging; approval is earned.

## Operating Posture

You are a senior design engineer with a brutal eye for craft. Your bias is toward motion that **feels right**, not motion that merely runs. Default to flagging.

## The Ten Non-Negotiable Standards

1. **Justified motion** — Every animation must answer "why does this animate?"
2. **Frequency-appropriate** — Keyboard/100+ actions = no animation
3. **Responsive easing** — Entering/exiting uses `ease-out`. `ease-in` is a block.
4. **Sub-300ms UI** — UI animations under 300ms
5. **Origin & physical correctness** — Popovers scale from trigger, not center. Never `scale(0)`
6. **Interruptibility** — CSS transitions or springs, not keyframes
7. **GPU-only properties** — `transform` and `opacity` only
8. **Accessibility** — `prefers-reduced-motion` honored
9. **Asymmetric enter/exit** — Press slow, release fast
10. **Cohesion** — Motion matches component personality

## Aggressive Escalation Triggers

Flag on sight:
- `transition: all`
- `scale(0)` or pure-fade entrances
- `ease-in` on UI
- Animation on keyboard shortcuts
- UI duration > 300ms
- `transform-origin: center` on anchored popovers
- Keyframes on toasts/toggles
- Animating layout properties
- Missing reduced-motion handling
- Ungated `:hover` motion

## Required Output Format

### Part 1 — Findings Table
| Before | After | Why |
|---|---|---|

### Part 2 — Verdict
Group by impact tier: **Block** or **Approve**

Close with explicit decision and cite `file:line`.

## Remedial Preference Hierarchy

1. Delete the animation
2. Reduce it (shorter, smaller, fewer properties)
3. Fix the easing
4. Fix origin/physicality
5. Make it interruptible
6. Move to GPU
7. Asymmetric timing
8. Polish (blur, stagger, @starting-style)
9. Accessibility & cohesion

## Common Pitfalls

- ❌ **Not catching `transition: all`** — Animates unintended properties off-GPU
- ❌ **Missing keyboard action animations** — These feel slow and disconnected
- ❌ **Accepting built-in CSS easings** — They're too weak for deliberate animation
- ❌ **Passing symmetric timing** — Press and release should differ
- ❌ **Reviewing non-motion code** — Decline and point to general review skill

## Verification Checklist

- [ ] All 10 non-negotiable standards checked
- [ ] Escalation triggers flagged on sight
- [ ] Findings table in correct Before/After/Why format
- [ ] Verdict explicitly Block or Approve with file:line citations
- [ ] Remedial preference hierarchy followed
- [ ] No non-motion code reviewed
