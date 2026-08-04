---
name: section-divider-generator
description: Use when creating section divider slides for PowerPoint presentations with PptxGenJS.
tags: [pptx, powerpoint, presentation, section-divider, pptxgenjs, javascript]
related_skills: [cover-page-generator, content-page-generator, table-of-contents-generator]
---

# Section Divider Generator

Creates section divider slides for PowerPoint presentations using PptxGenJS. Section dividers provide clear transitions between major parts of a presentation.

## Layout Options

| Layout | Best For |
|--------|----------|
| Bold Center | Minimal, modern presentations |
| Left-Aligned with Accent Block | Corporate, structured |
| Split Background | High-contrast, dramatic transitions |
| Full-Bleed with Overlay | Creative, bold presentations |

## Code Example: Section Divider

```javascript
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.accent };

  // Section number
  slide.addText("02", {
    x: 0.5, y: 0.8, w: 9, h: 1.5,
    fontSize: 96, fontFace: "Arial",
    color: theme.primary, bold: true, align: "center"
  });

  // Section title
  slide.addText("Architecture Overview", {
    x: 0.5, y: 2.5, w: 9, h: 1,
    fontSize: 40, fontFace: "Arial",
    color: theme.bg, bold: true, align: "center"
  });

  // Page number badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.light } });
  slide.addText("N", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, color: theme.primary, bold: true, align: "center", valign: "middle" });

  return slide;
}
module.exports = { createSlide };
```

## Common Pitfalls

- **Too much content**: Section dividers should be minimal — just number + title + optional one-liner
- **No visual distinction**: Dividers should look different from content slides (different background, more whitespace)
- **Inconsistent style**: All dividers in one presentation should use the same layout style
- **Missing page badge**: Section dividers MUST include page number badge

## Verification Checklist

- [ ] Section number is the most prominent visual element
- [ ] Only number + title (+ optional one-liner)
- [ ] Page number badge included
- [ ] Visually distinct from content slides
- [ ] Consistent divider style across all dividers
