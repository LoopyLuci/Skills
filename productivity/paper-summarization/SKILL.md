---
name: paper-summarization
description: "Download and summarize academic papers from arXiv"
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
