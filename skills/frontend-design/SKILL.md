---
name: frontend-design
description: Use when designing UI with distinctive visual identity.
tags: [ui-design, frontend, typography, visual-design, web-design]
related_skills: [brand-guidelines, theme-factory, animation-vocabulary]
---

# Frontend Design

Approach this as the design lead at a small studio. Every design choice should be deliberate and specific to the brief — never a templated default.

## Ground It in the Subject

Before designing, name: the concrete subject, its audience, and the page's single job. The subject's own world is where distinctive choices come from.

## Design Principles

### Hero as Thesis
Open with the most characteristic thing in the subject's world.

### Typography Carries Personality
- Pair display and body faces deliberately
- Set a clear type scale with intentional weights
- Make type treatment a memorable part of the design

### Structure Is Information
- Structural devices should encode something true about content
- Only use numbered markers if order carries information

### Leverage Motion Deliberately
- One orchestrated moment beats scattered effects
- Sometimes less is more

## Process: Brainstorm → Plan → Critique → Build

### Pass 1: Design Plan
Create a compact token system:
- **Color**: 4-6 named hex values
- **Type**: 2+ roles (display, body, utility)
- **Layout**: Prose descriptions + ASCII wireframes
- **Signature**: One unique element the page is remembered by

### Pass 2: Review and Build
Review the plan against the brief. Revise generic defaults. Only after confirming uniqueness should you write code.

## Code Example: CSS Token System

```css
:root {
  --color-bg: #f8f6f2;
  --color-text: #1a1a2e;
  --color-accent: #e07a5f;
  --font-display: 'Lora', Georgia, serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --text-hero: clamp(3rem, 8vw, 6rem);
  --text-body: 1rem;
}
```

## Common Pitfalls

- ❌ **Using default AI looks** (cream+terracotta, near-black+acid green, broadsheet)
- ❌ **Centering body text** — Left-align paragraphs and lists
- ❌ **Inter font by default** — Choose typefaces specific to the brief
- ❌ **No responsive design** — Must work down to mobile

## Verification Checklist

- [ ] Design plan has hex colors, type roles, layout concept
- [ ] No generic defaults used without intent
- [ ] Typography pairing is specific to the brief
- [ ] Copy uses active voice, plain language
- [ ] Responsive down to mobile
- [ ] Keyboard focus is visible
- [ ] `prefers-reduced-motion` respected
