---
name: paper-summarization
description: Download and summarize academic papers from arXiv
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [paper, summarization]
---

# Paper Summarization

## Download from arXiv
```python
import urllib.request, xml.etree.ElementTree as ET

url = "http://export.arxiv.org/api/query?id_list=2303.08774"
resp = urllib.request.urlopen(url)
root = ET.fromstring(resp.read())
ns = {"a": "http://www.w3.org/2005/Atom"}
title = root.find(".//a:title", ns).text
summary = root.find(".//a:summary", ns).text
```

## Structured Extraction
Extract: problem, method, results, contribution, limitations

## Trigger

Activate this skill when the user mentions:
- paper, summarization workflows or issues
- Building, fixing, or optimizing paper summarization


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
