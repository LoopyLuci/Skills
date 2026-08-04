---
name: content-page-generator
description: Use when creating content slides for PowerPoint presentations with PptxGenJS.
tags: [pptx, powerpoint, presentation, content-slide, pptxgenjs, javascript]
related_skills: [cover-page-generator, section-divider-generator, summary-page-generator, table-of-contents-generator]
---

# Content Page Generator

Creates content slides for PowerPoint presentations using PptxGenJS. Content slides contain the main body of presentation content.

## Content Slide Subtypes

| Subtype | Best For |
|---------|----------|
| Text | Bullets, quotes, short paragraphs |
| Mixed Media | Two-column image + text |
| Data Visualization | Charts + key takeaways |
| Comparison | Side-by-side columns (A vs B, pros/cons) |
| Timeline / Process | Steps with arrows, journey, phases |
| Image Showcase | Hero image, gallery, visual-first |

## Code Example: Text Content Slide

```javascript
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // Title
  slide.addText("Key Features", {
    x: 0.5, y: 0.3, w: 9, h: 0.8,
    fontSize: 36, fontFace: "Arial",
    color: theme.primary, bold: true
  });

  // Bullet points
  slide.addText([
    { text: "Feature One: High performance and scalability", options: { bullet: true, fontSize: 16 } },
    { text: "Feature Two: Built-in security and compliance", options: { bullet: true, fontSize: 16 } },
    { text: "Feature Three: Easy integration with existing tools", options: { bullet: true, fontSize: 16 } }
  ], {
    x: 0.5, y: 1.5, w: 9, h: 3,
    fontFace: "Arial", color: theme.secondary, valign: "top"
  });

  // Page number badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("N", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}
module.exports = { createSlide };
```

## Common Pitfalls

- **Text-only slides**: Every content slide must have at least one non-text element (image, chart, icon, or shape)
- **Center-aligned body text**: Left-align paragraphs and lists; center only titles
- **No page badge**: Every slide except cover requires a page number badge
- **Same layout repeated**: Vary layouts across content slides

## Verification Checklist

- [ ] Visual element included (not text-only)
- [ ] Body text left-aligned (not centered)
- [ ] Page number badge included
- [ ] Content matches the planned outline
- [ ] Font size: title >= 36pt, body 14-16pt
