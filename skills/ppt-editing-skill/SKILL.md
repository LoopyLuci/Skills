---
name: ppt-editing-skill
description: Use when editing existing PowerPoint presentations via XML manipulation.
tags: [pptx, powerpoint, editing, template, xml, python]
related_skills: [ppt-orchestra-skill, slide-making-skill, content-page-generator]
---

# PPTX Editing Skill

Provides workflows for editing existing PowerPoint presentations via XML manipulation and template-based approaches.

## Template-Based Workflow

1. **Copy and analyze**: `cp template.pptx template.pptx && python -m markitdown template.pptx > template.md`
2. **Plan slide mapping**: Match content sections to template slides
3. **Unpack**: Extract PPTX into editable XML using Python's `zipfile`
4. **Build**: Delete/duplicate/reorder slides in `presentation.xml`
5. **Edit content**: Update text in each `slide{N}.xml`
6. **Clean**: Remove orphaned files
7. **Pack**: Repack XML tree into PPTX file

## Code Example: Extract Text from PPTX

```bash
python -m markitdown presentation.pptx
```

## Code Example: Unpack PPTX for Editing

```python
import zipfile
import os

with zipfile.ZipFile("template.pptx", "r") as z:
    z.extractall("unpacked/")
```

## Code Example: Repack PPTX

```python
import zipfile

with zipfile.ZipFile("edited.pptx", "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk("unpacked/"):
        for file in files:
            path = os.path.join(root, file)
            arcname = os.path.relpath(path, "unpacked/")
            z.write(path, arcname)
```

## Common Pitfalls

- **Forgetting to clean orphaned files**: Remove slides not in `<p:sldIdLst>`
- **Smart quotes**: Use XML entities (`&#x201C;`) for quotes, not raw characters
- **Temp file path**: Write to `/tmp/` first when repacking (zipfile.seek fails on some mounts)
- **Subagent editing**: Use one subagent per slide XML file for parallel editing

## Verification Checklist

- [ ] `template.md` extracted and content verified
- [ ] Slide structure changes complete before text editing
- [ ] Orphaned files cleaned after structural changes
- [ ] All placeholder text replaced
- [ ] Final `edited.pptx` generated and content verified
