---
name: summary-page-generator
description: Use when creating summary/closing slides for PowerPoint presentations with PptxGenJS.
tags: [pptx, powerpoint, presentation, summary-slide, closing, pptxgenjs]
related_skills: [cover-page-generator, content-page-generator, table-of-contents-generator]
---

# Summary / Closing Page Generator

Creates summary and closing slides for PowerPoint presentations using PptxGenJS. Used for wrap-up and call-to-action.

## Layout Options

| Layout | Best For |
|--------|----------|
| Key Takeaways | Educational, corporate, data-driven |
| CTA / Next Steps | Sales pitches, proposals, project kick-offs |
| Thank You / Contact | Conference talks, keynotes |
| Split Recap | Presentations needing both recap and action |

## Code Example: Key Takeaways

```javascript
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // Title
  slide.addText("Key Takeaways", {
    x: 0.5, y: 0.3, w: 9, h: 1,
    fontSize: 44, fontFace: "Arial",
    color: theme.primary, bold: true
  });

  // Takeaways
  slide.addText([
    { text: "Takeaway one: Brief summary of main point", options: { bullet: true, fontSize: 18 } },
    { text: "Takeaway two: Another key insight", options: { bullet: true, fontSize: 18 } },
    { text: "Takeaway three: Final important point", options: { bullet: true, fontSize: 18 } }
  ], {
    x: 0.5, y: 1.8, w: 9, h: 2.5,
    fontFace: "Arial", color: theme.secondary, valign: "top"
  });

  // CTA
  slide.addText("Contact us at: email@example.com", {
    x: 0.5, y: 4.5, w: 9, h: 0.5,
    fontSize: 16, fontFace: "Arial",
    color: theme.accent, align: "center"
  });

  // Page number badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("N", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}
module.exports = { createSlide };
```

## Common Pitfalls

- **No CTA**: Every summary should include a clear call to action or next steps
- **Too many takeaways**: Keep to 3-5 concise items
- **Weak closing**: Main closing statement should be prominent and memorable
- **Missing contact info**: Include email or social handles for follow-up

## Verification Checklist

- [ ] Closing title present and prominent
- [ ] Key takeaways listed (3-5 items)
- [ ] Call to action or next steps included
- [ ] Contact information present (if applicable)
- [ ] Page number badge included
- [ ] Consistent tone with cover page
