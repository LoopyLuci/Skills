---
name: file-system-management
description: Organize deduplicate archive and clean files with Python
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [file, system, management]
---

# File System Management

## Organize by Type
```python
import os, shutil
for f in os.listdir("."):
    ext = f.split(".")[-1].lower()
    dirs = {"jpg": "Images", "pdf": "Docs", "zip": "Archives"}
    if ext in dirs:
        os.makedirs(dirs[ext], exist_ok=True)
        shutil.move(f, f"{dirs[ext]}/{f}")
```

## Find Duplicates
```python
import hashlib
def file_hash(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()
```

## Trigger

Activate this skill when the user mentions:
- file, system, management workflows or issues
- Building, fixing, or optimizing file system management


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
