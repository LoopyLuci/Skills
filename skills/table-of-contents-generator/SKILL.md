---
name: table-of-contents-generator
description: Use when creating table of contents slides for PowerPoint presentations with PptxGenJS.
tags: [pptx, powerpoint, presentation, toc, table-of-contents, pptxgenjs]
related_skills: [cover-page-generator, content-page-generator, section-divider-generator]
---

# Table of Contents Generator

Creates table of contents slides for PowerPoint presentations using PptxGenJS. Used for navigation and expectation setting.

## Layout Options

| Layout | Best For |
|--------|----------|
| Numbered Vertical List | 3-5 sections, straightforward presentations |
| Two-Column Grid | 4-6 sections, content-rich presentations |
| Sidebar Navigation | 3-5 sections, modern/corporate |
| Card-Based | 3-4 sections, creative/modern |

## Code Example: Numbered Vertical List

```javascript
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // Title
  slide.addText("Table of Contents", {
    x: 0.5, y: 0.3, w: 9, h: 1,
    fontSize: 40, fontFace: "Arial",
    color: theme.primary, bold: true
  });

  // Sections
  const sections = [
    { num: "01", title: "Introduction & Overview" },
    { num: "02", title: "Architecture Design" },
    { num: "03", title: "Implementation Strategy" },
    { num: "04", title: "Results & Next Steps" }
  ];

  sections.forEach((s, i) => {
    const y = 1.5 + i * 0.9;

    // Section number
    slide.addText(s.num, {
      x: 0.5, y: y, w: 0.8, h: 0.6,
      fontSize: 28, fontFace: "Arial",
      color: theme.accent, bold: true, align: "center"
    });

    // Section title
    slide.addText(s.title, {
      x: 1.5, y: y, w: 7, h: 0.6,
      fontSize: 22, fontFace: "Arial",
      color: theme.secondary
    });
  });

  // Page number badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("N", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}
module.exports = { createSlide };
```

## Common Pitfalls

- **Too many sections**: TOC works best with 3-7 sections
- **Inconsistent numbering**: Match numbering style with section dividers
- **No visual markers**: Use colored dots, lines, numbers, or icons to anchor each section
- **Missing page badge**: TOC MUST include page number badge

## Verification Checklist

- [ ] Section count appropriate (3-7)
- [ ] Section numbers/formatting consistent
- [ ] Page number badge included
- [ ] Scannable structure (viewer can scan in 2-3 seconds)
- [ ] Matches visual style of cover page
