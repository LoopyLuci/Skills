---
name: responsive-web-design-patterns
description: "Use when building responsive and mobile-first web designs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [responsive-design, mobile-first, CSS-grid, flexbox, media-queries, web-design]
    related_skills: [frontend-bootstrap, web-component-design, website-accessibility-audit, performance-budgeting]
---

# Responsive Web Design Patterns

Implementing responsive, mobile-first web design — from CSS Grid and Flexbox through responsive typography, images, and device testing.

## When to Use

- Building sites that work on all screen sizes
- Implementing mobile-first layouts
- Creating fluid grids with CSS Grid/Flexbox
- Optimizing for different devices

## Responsive Patterns

```python
RESPONSIVE_PATTERNS = {
    'mostly_fluid': 'Fluid grid with max-width container, columns stack on small screens',
    'column_drop': 'Full width → two columns → stacked as screen shrinks',
    'layout_shifter': 'Content reorders at breakpoints (sidebar moves)',
}

BREAKPOINTS = {
    'mobile': '320-480px', 'tablet': '481-768px',
    'desktop': '769-1200px', 'widescreen': '1201px+',
}
```

## Common Pitfalls

1. **Desktop-first instead of mobile-first** — compress up is easier than compress down
2. **Too many breakpoints** — 3-4 max; let content determine them
3. **No touch targets** — minimum 44×44px tap targets
4. **Desktop images on mobile** — serve responsive images with srcset

## Verification Checklist

- [ ] Mobile-first CSS (min-width media queries)
- [ ] Fluid images (max-width: 100%)
- [ ] Touch targets ≥ 44×44px
- [ ] Tested on real devices
- [ ] No horizontal scroll at any width
- [ ] Performance budget for mobile (<3s on 3G)
