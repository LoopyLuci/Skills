---
name: csv-json-processing
description: "Efficient large file CSV JSON streaming and chunking"
---

# CSV/JSON Processing

## Streaming Large CSV
```python
import csv

with open("large.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        process(row)  # One row at a time
```

## Chunked JSON
```python
import json

def read_jsonl(path):
    with open(path) as f:
        for line in f:
            yield json.loads(line)

for obj in read_jsonl("data.jsonl"):
    process(obj)
```

## Convert Between Formats
```bash
# CSV to JSON
csvkit: csvjson data.csv > data.json

# JSON to CSV
jq -r '.[] | [.name, .email] | @csv' data.json > data.csv
```
