---
name: web-accessibility-practices
description: "Use when implementing web accessibility (WCAG) standards."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [accessibility, a11y, WCAG, ARIA, screen-reader, inclusive-design]
    related_skills: [responsive-web-design-patterns, web-component-design, website-accessibility-audit, frontend-bootstrap]
---

# Web Accessibility Practices

Implementing web accessibility (WCAG) standards — from semantic HTML and ARIA through keyboard navigation, color contrast, screen reader compatibility, and testing.

## When to Use

- Ensuring web content is accessible to users with disabilities
- Meeting WCAG 2.1 AA compliance requirements
- Improving SEO through semantic HTML
- Building inclusive web applications

## Accessibility Principles

```python
A11Y_PRINCIPLES = {
    'perceivable': 'Content available to senses — alt text, captions, adaptable presentation',
    'operable': 'Interface works for all input methods — keyboard, voice, switch',
    'understandable': 'Content and interface are clear — readable text, predictable behavior',
    'robust': 'Compatible with current and future assistive technologies',
}

def check_color_contrast(foreground: str, background: str, size: str = 'normal') -> float:
    """Calculate WCAG contrast ratio (minimum 4.5:1 for normal text)."""
    def hex_to_luminance(hex_color):
        rgb = [int(hex_color[i:i+2], 16) / 255.0 for i in (1, 3, 5)]
        return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    
    l1 = hex_to_luminance(foreground) + 0.05
    l2 = hex_to_luminance(background) + 0.05
    ratio = max(l1, l2) / min(l1, l2)
    passed = ratio >= (4.5 if size == 'normal' else 3.0)
    return {'ratio': round(ratio, 2), 'passed': passed}
```

## Verification Checklist

- [ ] All images have alt text (decorative images: alt="")
- [ ] Color contrast passes WCAG AA (4.5:1 normal, 3:1 large text)
- [ ] All interactive elements reachable by keyboard
- [ ] Focus indicators visible (not default browser outline only)
- [ ] ARIA landmarks used (main, nav, banner, complementary)
- [ ] Form inputs have associated labels
- [ ] Page headers in hierarchical order (h1 → h2 → h3)
- [ ] Tested with screen reader (VoiceOver, NVDA, JAWS)
