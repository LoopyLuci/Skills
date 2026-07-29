---
name: file-system-management
description: "Organize deduplicate archive and clean files with Python"
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
