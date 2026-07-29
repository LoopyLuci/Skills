---
name: website-accessibility-audit
description: "Use when auditing site accessibility. WCAG, a11y."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [accessibility, a11y, wcag, compliance, inclusive-design]
    related_skills: [website-architecture-planner, landing-page-builder]
---

# Website Accessibility Audit

## Overview
Comprehensive accessibility audit: automated checks (contrast, ARIA, keyboard nav, focus indicators, form labels), manual testing guidance, WCAG 2.2 conformance levels (A/AA/AAA), remediation prioritization, and compliance reporting.

## When to Use
- "Make my website accessible"
- "Run a WCAG compliance check"
- "Check my site for accessibility issues"

## WCAG 2.2 Conformance Levels
| Level | Requirement | Target |
|-------|-------------|--------|
| A | Minimum accessibility — must pass for basic use | Legal minimum in many jurisdictions |
| AA | Acceptable for most users — all new sites should target | Industry standard, ADA compliance |
| AAA | Highest level — best effort only (rarely possible site-wide) | Luxury goal, not practical for all content |

## Automated Checks (use axe DevTools, Lighthouse, or WAVE)

### Color & Contrast
- [ ] Text-to-background contrast ratio ≥ 4.5:1 (AA normal text) / ≥ 3:1 (AA large text)
- [ ] Non-text content (icons, charts) contrast ≥ 3:1
- [ ] Focus indicator contrast (visible keyboard focus) ≥ 3:1
- [ ] No information conveyed by color alone (red = error only)
- Tool: `web_extract` the page, then check inline styles for color usage. Better: use axe-cli.

### Keyboard Navigation
- [ ] All interactive elements reachable with Tab key
- [ ] Tab order follows visual order (logical DOM order)
- [ ] Focus is visible on every interactive element
- [ ] No keyboard traps (can Tab in and Tab out)
- [ ] Skip navigation link present (first focusable element)

### Images & Media
- [ ] All `<img>` have meaningful alt text (or `alt=""` for decorative)
- [ ] Complex images (charts, infographics) have long descriptions
- [ ] Video content has captions (pre-recorded) / transcripts (audio)
- [ ] No auto-playing video/audio (or has a pause mechanism)

### Forms & Input
- [ ] Every input has a visible `<label>` (not placeholder-only)
- [ ] Error messages are associated with inputs via `aria-describedby`
- [ ] Required fields indicated visually AND programmatically (`required` or `aria-required`)
- [ ] Autocomplete attributes on common fields (`name`, `email`, `address`)

### ARIA
- [ ] ARIA landmarks used (`<nav>`, `<main>`, `<footer>`, `<aside>`)
- [ ] ARIA is not used to fix bad HTML (fix the HTML first)
- [ ] ARIA roles, states, and properties are valid and correctly applied
- [ ] Dynamic content has `aria-live` regions (polite for most updates)

## Manual Testing (do at least 2)
1. **Screen reader test**: Navigate the page with VoiceOver (macOS) or NVDA (Windows) using only keyboard
2. **Zoom test**: Zoom to 200% — no content should be cut off or overlapping
3. **Reduced motion**: Enable "Reduce motion" in OS — animations should pause or simplify
4. **High contrast mode**: Windows High Contrast Mode — all information must still be visible
5. **No CSS test**: Disable CSS — content must be readable in logical order

## Remediation Prioritization
| Priority | Impact | Example | Timeline |
|----------|--------|---------|----------|
| 🔴 Critical | Blocks access entirely | No alt text on essential images, keyboard trap | Immediate |
| 🟡 High | Severe usability barrier | Low contrast text, missing form labels | Within 1 week |
| 🔵 Medium | Frustrating but workable | Missing skip nav, auto-playing video | Within 1 month |
| ⚪ Low | Nice-to-have | AAA contrast on decorative elements, ARIA optimizations | Next sprint |

## Common Pitfalls
1. **Relying only on automated tools** — automated checks catch ~30% of issues. Manual testing is essential.
2. **Placeholder-only labels** — placeholder text disappears on input; use real `<label>` elements
3. **ARIA overuse** — "ARIA is for when HTML is wrong" — fix HTML first, ARIA only as supplement
4. **Focus style removal** — `outline: none` without replacement is the #1 keyboard accessibility failure
5. **Accessibility as a one-time fix** — audit with every major feature release

## Verification Checklist
- [ ] Automated scan completed (Lighthouse/axe/WAVE)
- [ ] Contrast ratios checked (all text 4.5:1+ AA)
- [ ] Keyboard navigation tested (Tab through entire page)
- [ ] Alt text on all meaningful images, `alt=""` on decorative
- [ ] Form labels present and associated
- [ ] ARIA landmarks in place
- [ ] Manual test performed (screen reader + zoom 200%)
- [ ] Issues prioritized (critical→high→medium→low)
- [ ] Report generated with specific remediation steps