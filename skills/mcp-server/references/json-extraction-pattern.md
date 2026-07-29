# Multi-Line JSON Parser (from mixed stdout)

When a subprocess emits log lines mixed with JSON output, standard `json.loads()` on individual lines fails because the JSON is pretty-printed across multiple lines. This brace-depth tracking parser collects only the JSON portion.

## The Problem

```python
# stdout contains:
# [SG v3.0.0] Initializing...
# [SG] Ready. 1033 skills...
# {
#   "model": {
#     "schema": "3.0.0",
#     ...
#   }
# }

json.loads(line)  # Fails on "{" — incomplete JSON
json.loads('[SG v3.0.0]...')  # Fails — not JSON
```

## The Solution

Track brace depth: start collecting on `{`, stop when all braces close.

```python
def extract_json(text: str) -> dict:
    """Extract first complete JSON object from mixed stdout."""
    lines = text.split('\n')
    in_json = False
    json_lines = []
    depth = 0
    for line in lines:
        s = line.strip()
        if not in_json:
            # Only start on { — avoid log lines starting with [
            if s.startswith('{'):
                in_json = True
                json_lines = [line]
                depth = s.count('{') - s.count('}')
        else:
            json_lines.append(line)
            depth += s.count('{') - s.count('}')
            if depth <= 0:  # All braces closed
                break
    
    if json_lines:
        return json.loads('\n'.join(json_lines))
    return None
```

## Key Details

- **Only `{` starts collection** — `[` log lines are ignored
- **Brace-depth tracking** handles nested objects: `{"a": {"b": {"c": 1}}}` correctly collects the entire tree
- **Returns after first complete object** — stops at depth=0
- **Returns `None`** if no valid JSON found (not an exception — caller checks)

## Variations

For arrays instead of objects, change `s.startswith('{')` to `s.startswith('[')` and track `[]` depth instead of `{}`.

For multiple JSON objects in one stream, loop the extraction after removing the first match.
