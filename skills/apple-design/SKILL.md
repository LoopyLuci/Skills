---
name: apple-design
description: Use when building gesture-driven or Apple-style interfaces.
tags: [apple, ui-design, animation, gestures, spring-physics]
related_skills: [animation-vocabulary, frontend-design, emil-design-eng]
---

# Apple Design

How Apple builds interfaces that feel like an extension of you — translated for the web platform.

## The Core Idea

> "When we align the interface to the way we think and move, something magical happens — it stops feeling like a computer and starts feeling like a seamless extension of us."

## 1. Response — Kill Latency

- **Respond on pointer-down, not on release** — Highlight on touch-down instantly
- **Feedback must be continuous** *during* the interaction, not just at the end

```css
.button:active {
  transform: scale(0.97);
  transition: transform 100ms ease-out;
}
```

## 2. Direct Manipulation — 1:1 Tracking

```js
el.addEventListener('pointerdown', (e) => {
  el.setPointerCapture(e.pointerId);
  const grabOffset = e.clientY - el.getBoundingClientRect().top;
  // Track position + timestamp history for velocity
});
```

## 3. Interruptibility

Every animation must be interruptible and redirectable at any moment. Always animate from the *current* value, never the target value.

## 4. Use Springs

```js
import { animate } from 'motion';

// Critically damped (no overshoot)
animate(el, { y: 0 }, { type: 'spring', bounce: 0, duration: 0.4 });

// With bounce for momentum interactions
animate(el, { y: target }, { type: 'spring', bounce: 0.2, duration: 0.4 });
```

| Interaction | Damping | Response |
|---|---|---|
| Move/reposition | 1.0 | 0.4 |
| Rotation | 0.8 | 0.4 |
| Drawer/sheet | 0.8 | 0.3 |

## 5. Velocity Handoff

Pass pointer release velocity as spring initial velocity:
```
relativeVelocity = gestureVelocity / (targetValue − currentValue)
```

## 6. Momentum Projection

```js
function project(initialVelocity, decelerationRate = 0.998) {
  return (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate);
}
const projectedEndpoint = currentPosition + project(releaseVelocity);
```

## 7. Spatial Consistency

- Enter and exit along the same path
- Anchor interactions to their source (transform-origin)

## 8. Rubber-Banding

```js
function rubberband(overshoot, dimension, constant = 0.55) {
  return (overshoot * dimension * constant) / (dimension + constant * Math.abs(overshoot));
}
```

## 9. Accessibility

```css
@media (prefers-reduced-motion: reduce) {
  .sheet { transition: opacity 200ms ease; transform: none !important; }
}
```

## Common Pitfalls

- ❌ **Animating on pointer-up only** — Respond on pointer-down
- ❌ **CSS transitions for gesture-driven motion** — Springs are interruptible
- ❌ **Hard stops at boundaries** — Use rubber-banding instead
- ❌ **Ignoring reduced motion** — Always provide accessible alternatives

## Verification Checklist

- [ ] Feedback fires on pointer-down (instant)
- [ ] Springs used for gesture-driven animations
- [ ] Interruptibility: animation can be redirected mid-flight
- [ ] Velocity handed off from gesture to animation
- [ ] Rubber-banding at scroll/drag boundaries
- [ ] `prefers-reduced-motion` handling implemented
- [ ] `transform-origin` set correctly for anchored elements
