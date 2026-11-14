---
name: "e-commerce-photo-workflow"
title: "Photograph Organization, Research & Listing Generation for E-Commerce"
description: "Organize photos, research items, generate listings."
tags: [e-commerce, photo-organization, image-analysis, listing-generation, facebook-marketplace]
---

# E-Commerce Photo Organization & Listing Workflow

## Overview

This skill covers the complete workflow for taking a folder of product photos and producing:
1. Photographs organized into item-specific folders with tags
2. Deep research on each item (identity, features, condition, provenance)
3. Per-item documentation (markdown)
4. Platform-optimized product listings (Facebook Marketplace, Instagram, eBay, Etsy)

It also covers the fallback when AI vision APIs are rate-limited: programmatic image analysis with PIL/OpenCV/sklearn.

## Procedure (Step-by-Step)

### Step 1: Inventory the photos

```bash
# Count and list all files
find "C:/Users/limpi/OneDrive/Documents/Sell" -type f | sort

# Get dimensions and basic metadata for every image
python -c "
import os
from PIL import Image
dir_path = 'C:/Users/limpi/OneDrive/Documents/Sell'
for f in sorted(os.listdir(dir_path)):
    fp = os.path.join(dir_path, f)
    if os.path.isfile(fp) and f.lower().endswith(('.jpg', '.jpeg', '.png')):
        with Image.open(fp) as img:
            print(f, img.size, img.format)
"
```

### Step 2: Run programmatic image analysis (PIL/OpenCV/sklearn)

```bash
# Install dependencies
python -m pip install Pillow opencv-python-headless scikit-learn numpy

# Run analysis script
python analyze_images.py
```

**Extract for each image:** dimensions, brightness (0-255), edge density (Canny), dominant colors (k-means 4 clusters, 50K pixel sample).

### Step 3: Identify items

**Preferred:** Use vision AI for each image. Path must be native Windows format `C:\Users\...` (not `/c/...`). 

**Fallback:** Programmatic analysis for clustering. Use local AI (llama.cpp/Ollama with Qwen3.5-9B on RX 7900 XTTX GPU).

### Step 4: Create item folders

```bash
Sell/
├── Items/
│   ├── 01_Military_Pail/
│   │   ├── 001_main.jpg
│   │   └── 002_detail.jpg
│   └── ...
├── Documentation/
├── Platform_Posts/
│   ├── facebook/
│   └── instagram/
└── config.yaml
```

### Step 5: Generate per-item documentation

Use the template (`Documentation_template.md`) which includes: overview, key features, condition, specifications, research notes, photo captions, suggested price, keywords, SEO tags.

### Step 6: Generate per-item Facebook listing

Use the template (`FB_listing_template.md`) which includes: listing data, title (65 chars optimal), description, product details, keywords, photo captions, shipping info.

## Pitfalls

1. **vision_analyze path resolver mishandles `/c/...` paths.** Always use native Windows path `C:\Users\...` (backslash format).
2. **execute_code kernel cannot access Windows filesystem.** All file operations must use `terminal` (bash) tool.
3. **Do not use `terminal(background=true)` to launch GUI apps.** Window will be invisible (Session 0 isolation). Launch from interactive terminal.
4. **Do not use `execute_code` for filesystem work.** Use `terminal` for all file operations.
5. **OCR is not a substitute for vision AI.** These 63 photos contain no labels.
6. **Vision API rate limits oscillate between 2400-2800s.** Treat 429s on shared AI APIs as high-latency, not transient.

## User Preferences Embedded

- **Desktop GUI = pywebview/Tauri, never browser dashboard** (see `desktop-dashboard` skill)
- **Free models sorted to top; paid models hidden by default** for Nous/OpenRouter
- **Multi-platform listing optimization** (title formulas, description formats)
- **Full implementation, zero tolerance for bugs**

## References

- `references/platform_design.md` — full platform architecture document
- `references/model_visibility_preferences.md` — model visibility rules (free first, paid hidden)
- `references/hardware_notes.md` — local AI model configuration (Qwen3.5-9B on RX 7900 XTTX)
- `references/image_analysis_template.py` — reusable programmatic image analysis script
