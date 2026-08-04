---
name: minimax-xlsx
description: Use when creating, editing, or validating Excel spreadsheets
tags: [excel, xlsx, spreadsheet, financial-model, data]
related_skills: [pptx-generator, mmx-cli]
---

# MiniMax XLSX Skill

## Overview

Create, edit, read, analyze, and validate Excel files (.xlsx, .xlsm, .csv, .tsv) using XML manipulation and helper scripts.

## Task Routing

| Task | Method |
|------|--------|
| **READ** — analyze data | `xlsx_reader.py` + pandas |
| **CREATE** — new xlsx | XML template with `create.md` |
| **EDIT** — modify existing | XML unpack→edit→pack |
| **FIX** — repair formulas | XML unpack→fix `<f>` nodes→pack |
| **VALIDATE** — check formulas | `formula_check.py` |

## Create a New Spreadsheet

```bash
# Copy minimal template, edit XML directly, then pack
python3 scripts/xlsx_pack.py /tmp/xlsx_work/ output.xlsx
```

## Edit an Existing Spreadsheet

```bash
# Unpack → edit → repack cycle
python3 scripts/xlsx_unpack.py input.xlsx /tmp/xlsx_work/
# ... edit XML ...
python3 scripts/xlsx_pack.py /tmp/xlsx_work/ output.xlsx
```

**CRITICAL:** Never use openpyxl round-trip on existing files (corrupts VBA, pivots, sparklines). Use unpack → edit → pack.

## Add a Column

```bash
python3 scripts/xlsx_unpack.py input.xlsx /tmp/xlsx_work/
python3 scripts/xlsx_add_column.py /tmp/xlsx_work/ --col G     --sheet "Sheet1" --header "% of Total"     --formula '=F{row}/$F$10' --formula-rows 2:9     --numfmt '0.0%'
python3 scripts/xlsx_pack.py /tmp/xlsx_work/ output.xlsx
```

## Financial Color Standard

| Cell Role | Font Color |
|-----------|-----------|
| Hard-coded input / assumption | Blue (`0000FF`) |
| Formula / computed result | Black (`000000`) |
| Cross-sheet reference formula | Green (`00B050`) |

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Using openpyxl for round-trip editing | Use XML unpack→edit→pack workflow |
| Hardcoding calculated values | Every computed cell MUST use an Excel formula |
| Forgetting formula validation | Run `formula_check.py` before delivery |
| Not preserving original sheets | EDIT tasks must keep all original sheets and data |

## Verification Checklist

- [ ] READ: Data analyzed without modifying source
- [ ] CREATE: XML template used, formulas for computed values
- [ ] EDIT: XML unpack/edit/pack used (not openpyxl)
- [ ] Original sheets preserved in EDIT tasks
- [ ] Formulas validated with formula_check.py
- [ ] Output file deliverable produced
