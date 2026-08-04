---
name: slide-making-skill
description: Use when creating individual slide modules for PowerPoint presentations with PptxGenJS.
tags: [pptx, powerpoint, slide, pptxgenjs, javascript, presentation]
related_skills: [content-page-generator, cover-page-generator, section-divider-generator, summary-page-generator, table-of-contents-generator]
---

# Slide Making Skill

Provides the standard format and best practices for creating individual slide modules for PowerPoint presentations using PptxGenJS.

## Slide Module Format

Each slide is a self-contained JavaScript file exporting a synchronous `createSlide(pres, theme)` function:

```javascript
// slide-01.js
const pptxgen = require("pptxgenjs");

const slideConfig = {
  type: 'cover',
  index: 1,
  title: 'Slide Title'
};

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // Add elements here
  slide.addText(slideConfig.title, {
    x: 0.5, y: 2, w: 9, h: 1.2,
    fontSize: 48, fontFace: "Arial",
    color: theme.primary, bold: true, align: "center"
  });

  return slide;
}

module.exports = { createSlide, slideConfig };
```

## Page Number Badge (REQUIRED)

All slides except Cover Page MUST include a page number badge:

```javascript
// Circle badge
slide.addShape(pres.shapes.OVAL, {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fill: { color: theme.accent }
});
slide.addText("3", {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fontSize: 12, fontFace: "Arial",
  color: "FFFFFF", bold: true,
  align: "center", valign: "middle"
});
```

## Common Pitfalls

- **async/await in createSlide()**: NEVER use async — compile.js won't await synchronous functions
- **"#" with hex colors**: Use `"FF0000"` not `"#FF0000"` — hash causes file corruption in PptxGenJS
- **Opacity in hex**: Use `opacity` property, never encode opacity in hex strings
- **Reusing option objects**: PptxGenJS mutates objects — always create fresh options per call
- **Missing page badge**: Every slide except cover page needs badge in bottom-right (x: 9.3, y: 5.1)

## Verification Checklist

- [ ] Function is synchronous (no async/await)
- [ ] Colors use 6-char hex without "#"
- [ ] No reused option objects (use factory functions)
- [ ] Page number badge present (if not cover page)
- [ ] Badge in correct position (x: 9.3, y: 5.1)
- [ ] Theme object uses correct key names
