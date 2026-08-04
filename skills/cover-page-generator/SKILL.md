---
name: cover-page-generator
description: Use when creating cover/title slides for PowerPoint presentations with PptxGenJS.
tags: [pptx, powerpoint, presentation, cover-slide, pptxgenjs, javascript]
related_skills: [content-page-generator, table-of-contents-generator, color-font-skill]
---

# Cover Page Generator

Creates opening/title slides for PowerPoint presentations using PptxGenJS. The cover page sets the tone and first impression.

## Layout Options

| Layout | Best For |
|--------|----------|
| Asymmetric Left-Right | Corporate, product launches, professional reports |
| Center-Aligned | Inspirational talks, events, creative pitches |

## Code Example: Cover Page

```javascript
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.primary };

  // Main title
  slide.addText("Presentation Title", {
    x: 0.5, y: 1.5, w: 9, h: 1.5,
    fontSize: 54, fontFace: "Arial",
    color: theme.bg, bold: true, align: "center"
  });

  // Subtitle
  slide.addText("Subtitle or tagline here", {
    x: 0.5, y: 3.2, w: 9, h: 0.6,
    fontSize: 24, fontFace: "Arial",
    color: theme.light, align: "center"
  });

  // Bottom info
  slide.addText("Presenter Name | Date", {
    x: 0.5, y: 4.5, w: 9, h: 0.5,
    fontSize: 14, fontFace: "Arial",
    color: theme.light, align: "center"
  });

  return slide;
}
module.exports = { createSlide };
```

## Font Size Hierarchy

| Element | Size |
|---------|------|
| Main Title | 72-120px (3x-5x base) |
| Subtitle | 28-40px (1.5x-2x base) |
| Supporting Text | 18-24px (1x base) |
| Meta Info | 14-18px (0.7x-1x base) |

## Common Pitfalls

- **No dramatic contrast**: Main title should be at least 2-3x larger than subtitle
- **Adjacent sizes too similar**: Never let adjacent text elements be within 20% of each other's size
- **No page badge on cover**: Cover page is the only slide that should NOT have a page number badge
- **Missing background**: Cover should have a strong background or motif

## Verification Checklist

- [ ] Main title present and largest element
- [ ] Subtitle clearly smaller than title
- [ ] No page number badge on cover
- [ ] Visual anchor/background present
- [ ] Presenter name and date included (if applicable)
