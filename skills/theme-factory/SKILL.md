---
name: theme-factory
description: Use when styling artifacts with curated color/font themes.
tags: [theming, color-palettes, typography, design-systems]
related_skills: [brand-guidelines, frontend-design, pptx]
---

# Theme Factory

A curated collection of professional font and color themes for styling artifacts — slides, documents, and HTML pages.

## Available Themes

| # | Theme | Description |
|---|-------|-------------|
| 1 | Ocean Depths | Professional maritime theme |
| 2 | Sunset Boulevard | Warm sunset colors |
| 3 | Forest Canopy | Natural earth tones |
| 4 | Modern Minimalist | Clean grayscale |
| 5 | Golden Hour | Warm autumnal palette |
| 6 | Arctic Frost | Cool winter-inspired |
| 7 | Desert Rose | Soft dusty tones |
| 8 | Tech Innovation | Bold tech aesthetic |
| 9 | Botanical Garden | Fresh garden colors |
| 10 | Midnight Galaxy | Dramatic deep tones |

## Usage Process

1. Show the theme showcase (theme-showcase.pdf)
2. Ask for explicit theme choice
3. Read the corresponding theme file from `themes/` directory
4. Apply colors and fonts consistently
5. Ensure proper contrast and readability

## Creating Custom Themes

Generate new themes when existing ones don't fit:
1. Give the theme a descriptive name
2. Include cohesive color palette with hex codes
3. Add complementary font pairings
4. Show for review before applying

## Code Example: Theme Structure

```json
{
  "name": "Ocean Depths",
  "colors": {
    "primary": "#1a3a4a",
    "secondary": "#4a8ba8",
    "accent": "#7ac4d8",
    "background": "#f0f6f8",
    "text": "#0d1b26"
  },
  "typography": {
    "heading": "Poppins",
    "body": "Lora"
  }
}
```

## Common Pitfalls

- ❌ **Applying without user confirmation** — Always wait for explicit choice
- ❌ **Inconsistent application** — Every element must use theme tokens
- ❌ **Poor contrast** — Check text/background pairs
- ❌ **Mixing themes** — Never combine tokens from different themes

## Verification Checklist

- [ ] Theme confirmed by user before application
- [ ] All colors match selected theme hex values
- [ ] Typography uses theme's font pairings
- [ ] Contrast ratios meet WCAG AA standards
- [ ] Theme applied consistently across all pages
