---
name: pptx-generator
description: Use when creating or editing PowerPoint presentations
tags: [powerpoint, pptx, presentation, slides, design]
related_skills: [minimax-xlsx, mmx-cli]
---

# PPTX Generator & Editor

## Overview

Create, edit, and read PowerPoint presentations. Create from scratch with PptxGenJS, edit via XML, or extract text with markitdown.

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit from template | XML manipulation workflow |
| Create from scratch | PptxGenJS with design system |

| Item | Value |
|------|-------|
| Dimensions | 10" x 5.625" (LAYOUT_16x9) |
| Colors | 6-char hex without # (e.g., `"FF0000"`) |
| English font | Arial |
| Chinese font | Microsoft YaHei |

## Reading Content

```bash
python -m markitdown presentation.pptx
```

## Creating from Scratch — Workflow

### Step 1: Select Color Palette & Fonts
Choose a palette and font pairing matching the topic and audience.

### Step 2: Plan Slide Outline
Classify every slide as exactly one type: Cover, TOC, Section Divider, Content, Summary.

### Step 3: Generate Slide JS Files
Create one JS file per slide. Each exports `createSlide(pres, theme)`.

### Step 4: Compile into Final PPTX

```javascript
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

const theme = {
  primary: "22223b",
  secondary: "4a4e69",
  accent: "9a8c98",
  light: "c9ada7",
  bg: "f2e9e4"
};

for (let i = 1; i <= 12; i++) {
  const num = String(i).padStart(2, '0');
  const slideModule = require(`./slide-${num}.js`);
  slideModule.createSlide(pres, theme);
}
pres.writeFile({ fileName: './output/presentation.pptx' });
```

### Step 5: QA
Verify all slides render correctly and meet design standards.

## Slide Format

```javascript
// slide-01.js - Cover slide
const pptxgen = require("pptxgenjs");

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  slide.addText("Presentation Title", {
    x: 0.5, y: 2, w: 9, h: 1.2,
    fontSize: 48, fontFace: "Arial",
    color: theme.primary, bold: true, align: "center"
  });
  return slide;
}
module.exports = { createSlide };
```

## Dependencies

- `pip install "markitdown[pptx]"` — text extraction
- `npm install -g pptxgenjs` — creating from scratch

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Wrong color format | Use 6-char hex without # |
| Async slide functions | Slide modules must export synchronous `createSlide` |
| Missing page numbers | All slides except cover need page badge |
| Wrong theme key names | Must use exactly: primary, secondary, accent, light, bg |
| Skipping QA step | Always verify output before delivery |

## Verification Checklist

- [ ] Color palette and fonts selected
- [ ] Slide outline planned with all page types
- [ ] Each slide module exports synchronous createSlide
- [ ] Theme object uses correct key names
- [ ] Compile script runs without errors
- [ ] Output presentation renders correctly
- [ ] Page numbers on all slides except cover
