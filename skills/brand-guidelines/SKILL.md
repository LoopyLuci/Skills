---
name: brand-guidelines
description: Use when applying brand colors and typography to artifacts.
tags: [branding, design-systems, visual-identity, typography]
related_skills: [theme-factory, frontend-design]
---

# Anthropic Brand Styling

Apply Anthropic's official brand colors and typography to any artifact — slide decks, documents, HTML pages, or visual assets.

## Brand Colors

### Main Colors
| Name | Hex | Usage |
|------|-----|-------|
| Dark | `#141413` | Primary text and dark backgrounds |
| Light | `#faf9f5` | Light backgrounds and text on dark |
| Mid Gray | `#b0aea5` | Secondary elements |
| Light Gray | `#e8e6dc` | Subtle backgrounds |

### Accent Colors
| Name | Hex | Usage |
|------|-----|-------|
| Orange | `#d97757` | Primary accent |
| Blue | `#6a9bcc` | Secondary accent |
| Green | `#788c5d` | Tertiary accent |

## Typography

| Role | Font | Fallback |
|------|------|----------|
| Headings | Poppins | Arial |
| Body Text | Lora | Georgia |

### Font Management
- Use system-installed Poppins and Lora fonts when available
- Automatic fallback to Arial (headings) and Georgia (body)
- No font installation required

## Code Example: Brand CSS

```css
:root {
  --brand-dark: #141413;
  --brand-light: #faf9f5;
  --brand-orange: #d97757;
  --brand-blue: #6a9bcc;
  --brand-green: #788c5d;
  --font-heading: 'Poppins', Arial, sans-serif;
  --font-body: 'Lora', Georgia, serif;
}
```

## Common Pitfalls

- ❌ **Forgetting font fallbacks** — Always specify Arial/Georgia
- ❌ **Using 8-digit hex colors** — Alpha in hex corrupts PPTX files
- ❌ **Low contrast** — Brand light gray on white is hard to read

## Verification Checklist

- [ ] All colors use exact hex values from brand palette
- [ ] Typography uses correct fonts with proper fallbacks
- [ ] Accent colors cycle properly (orange → blue → green)
- [ ] Text has sufficient contrast against its background
