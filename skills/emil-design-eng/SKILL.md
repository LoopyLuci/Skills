---
name: emil-design-eng
description: Use when applying Emil Kowalski's animation philosophy.
tags: [animation, ui-design, css, motion, frontend]
related_skills: [apple-design, animation-vocabulary, review-animations]
---

# Design Engineering

Emil Kowalski's philosophy on UI polish, component design, and animation decisions.

## Core Philosophy

### Taste is trained, not innate
Good taste is a trained instinct. Study why the best interfaces feel the way they do. Reverse engineer animations. Inspect interactions.

### Unseen details compound
Most details users never consciously notice. That is the point. The aggregate of invisible correctness creates interfaces people love without knowing why.

### Beauty is leverage
People select tools based on the overall experience. Good defaults and good animations are real differentiators.

## The Animation Decision Framework

### 1. Should this animate at all?
| Frequency | Decision |
|---|---|
| 100+ times/day | No animation. Ever. |
| Tens of times/day | Remove or drastically reduce |
| Occasional | Standard animation |
| Rare/first-time | Can add delight |

### 2. What is the purpose?
Valid: spatial consistency, state indication, explanation, feedback, preventing jarring changes.

### 3. What easing?
- Entering/exiting → ease-out
- Moving/morphing on screen → ease-in-out
- Hover/color change → ease
- Constant motion → linear

### 4. How fast?
| Element | Duration |
|---|---|
| Button press | 100-160ms |
| Tooltips | 125-200ms |
| Dropdowns | 150-250ms |
| Modals/drawers | 200-500ms |

## Component Building Principles

### Buttons must feel responsive
```css
.button { transition: transform 160ms ease-out; }
.button:active { transform: scale(0.97); }
```

### Never animate from scale(0)
```css
/* Bad */
.entering { transform: scale(0); }

/* Good */
.entering { transform: scale(0.95); opacity: 0; }
```

### Make popovers origin-aware
```css
.popover { transform-origin: var(--transform-origin); }
```

### Use CSS transitions over keyframes
CSS transitions can be interrupted mid-animation. Keyframes restart from zero.

### Use blur to mask imperfect transitions
```css
.button-content.transitioning {
  filter: blur(2px);
  opacity: 0.7;
}
```

### Custom Easing Curves
```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
```

## Performance Rules
- Only animate `transform` and `opacity`
- CSS variables on parent trigger recalc on all children
- Framer Motion `x`/`y`/`scale` are NOT hardware accelerated

## Common Pitfalls

- ❌ **Animating keyboard actions** — These are 100+/day, never animate
- ❌ **Built-in CSS easings** — Too weak; always use custom cubic-beziers
- ❌ **`ease-in` on UI elements** — Feels sluggish, delays initial movement
- ❌ **Sharing Framer Motion option objects** — They mutate in place

## Verification Checklist

- [ ] Frequency check applied before adding animation
- [ ] Easing uses custom cubic-bezier curves (not built-ins)
- [ ] Duration under 300ms for UI animations
- [ ] `transform-origin` set correctly for trigger-anchored elements
- [ ] No `scale(0)` entries anywhere
- [ ] CSS transitions used (not keyframes) for interruptible UI
- [ ] `prefers-reduced-motion` handled
- [ ] Hover animations gated behind `@media (hover: hover)`
