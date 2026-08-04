---
name: ppt-orchestra-skill
description: Use when orchestrating multi-slide PowerPoint creation — compile, QA, and verify.
tags: [pptx, powerpoint, orchestration, compilation, pptxgenjs, qa]
related_skills: [slide-making-skill, ppt-editing-skill, content-page-generator]
---

# PPTX Orchestra Skill

Provides orchestration workflow for compiling multiple slide files into a final PowerPoint presentation and running QA.

## Compile Workflow

1. Create individual slide JS files in `slides/` directory
2. Create `slides/compile.js` to combine all modules
3. Run `cd slides && node compile.js`
4. Run QA: extract text and verify content

## Code Example: compile.js

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

## QA Process

```bash
# Extract text for review
python -m markitdown output.pptx

# Check for placeholder text
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|placeholder"
```

## Output Structure

```
slides/
├── slide-01.js
├── slide-02.js
├── ...
├── imgs/
└── output/
    └── presentation.pptx
```

## Common Pitfalls

- **async/await in createSlide()**: Slide functions must be synchronous — compile.js won't await
- **Reusing option objects**: PptxGenJS mutates objects in-place — use factory functions
- **Missing page badges**: Every slide except cover must include page number badge
- **Skipping QA**: Always run markitdown and check for placeholder text before declaring success

## Verification Checklist

- [ ] All slide files created in `slides/` directory
- [ ] Theme object uses correct 5 key names
- [ ] Slide functions are synchronous (not async)
- [ ] compile.js runs without errors
- [ ] `output.pptx` generated
- [ ] markitdown text extraction shows all content
- [ ] No placeholder text remaining
