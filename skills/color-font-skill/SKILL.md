---
name: color-font-skill
description: Use when selecting color palettes and font pairings for PowerPoint presentations.
tags: [pptx, powerpoint, design, color-palette, typography, fonts]
related_skills: [cover-page-generator, content-page-generator, slide-making-skill]
---

# Color Palette & Font Selection for PPTX

Provides design system guidance for selecting color palettes and font pairings for PowerPoint presentations.

## Recommended Color Palettes

| # | Name | Primary | Accent | Background |
|---|------|---------|--------|------------|
| 1 | Modern & Wellness | `#006d77` | `#e29578` | `#edf6f9` |
| 2 | Business & Authority | `#2b2d42` | `#ef233c` | `#edf2f4` |
| 3 | Nature & Outdoors | `#606c38` | `#dda15e` | `#fefae0` |
| 4 | Vibrant & Tech | `#023047` | `#fb8500` | `#8ecae6` |
| 5 | Elegant & Fashion | `#4a5759` | `#edafb8` | `#dedbd2` |
| 6 | Pure Tech Blue | `#03045e` | `#00b4d8` | `#caf0f8` |

## Theme Object Contract

```javascript
const theme = {
  primary: "22223b",    // Darkest — titles
  secondary: "4a4e69",  // Body text
  accent: "9a8c98",     // Highlights
  light: "c9ada7",      // Light accent
  bg: "f2e9e4"          // Background
};
```

## Font Pairings

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Cambria | Calibri |
| Trebuchet MS | Calibri |

- **Chinese text**: Microsoft YaHei
- **English default**: Arial

## Common Pitfalls

- **Don't modify palette colors**: Use exactly as provided; no brightness/saturation changes
- **No gradients**: Use solid colors only — gradients are prohibited
- **No bold for body text**: Reserve bold for titles and headings only
- **Never use "#" with hex colors**: Causes file corruption in PptxGenJS (use `"FF0000"` not `"#FF0000"`)
- **Never encode opacity in hex**: Use the `opacity` property instead

## Verification Checklist

- [ ] Colors selected from palette (no custom colors)
- [ ] Font pairing chosen (not just Arial default)
- [ ] Bold used only for titles/headings
- [ ] Hex colors without "#" prefix
- [ ] Theme object uses correct key names
