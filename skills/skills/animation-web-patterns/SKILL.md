---
name: animation-web-patterns
description: "Use when implementing web animations and transitions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [animation, CSS-animations, Web-API, transitions, GSAP, motion]
    related_skills: [responsive-web-design-patterns, web-component-design, frontend-bootstrap, web-accessibility-practices]
---

# Web Animation Patterns

Implementing web animations — from CSS transitions and keyframes through Web Animations API, scroll-driven animations, and performance optimization.

## When to Use

- Adding UI animations for better user experience
- Implementing scroll-driven and intersection animations
- Building performant animations that don't jank
- Animating between routes and page transitions

## Animation Methods

```python
ANIMATION_METHODS = {
    'css_transitions': 'Declarative, GPU-accelerated, best for simple state changes',
    'css_keyframes': 'Multi-step animations, timing functions, can be GPU-accelerated',
    'web_animations_api': 'Programmatic control, better than JS setInterval, composable',
    'scroll_driven': 'Intersection Observer, Scroll Timeline — trigger on scroll position',
    'view_transitions': 'SPA route transitions between pages (Chrome 111+)',
}

# Web Animations API example
def animate_element(element, keyframes: List[Dict], duration: int = 300):
    import time
    anim = element.animate(keyframes, {
        'duration': duration, 'easing': 'ease-in-out',
        'fill': 'forwards'
    })
    return anim.finished  # Promise when done
```

## Common Pitfalls

1. **Animating layout properties** — animating width/height/top triggers layout; use transform + opacity
2. **No prefers-reduced-motion** — always respect user preference for reduced motion
3. **Too much animation** — overwhelming UI; use animation sparingly and purposefully
4. **Long durations** — animations >500ms feel slow; use 200-400ms for UI animations

## Verification Checklist

- [ ] Layout animations use transform (not width/height/top)
- [ ] prefers-reduced-motion respected
- [ ] Animation duration appropriate (200-400ms UI, 500-1000ms decorative)
- [ ] Animation curves feel natural (ease-out, cubic-bezier)
- [ ] No jank (60fps) — GPU-composited properties only
- [ ] Accessible: no flashing (epilepsy), motion respected
