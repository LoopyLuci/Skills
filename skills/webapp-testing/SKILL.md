---
name: webapp-testing
description: Use when testing web apps with Playwright automation.
tags: [testing, playwright, web-application, automation, QA]
related_skills: [playwright-browser-automation, dogfood]
---

# Web Application Testing

Test local web applications using native Python Playwright scripts.

## Decision Tree

```
Task → Is it static HTML?
  ├─ Yes → Read HTML file directly to find selectors
  │         ├─ Success → Write Playwright script
  │         └─ Fails → Treat as dynamic
  └─ No → Is server already running?
      ├─ No → Use scripts/with_server.py
      └─ Yes → Reconnaissance-then-action
```

## Core Pattern

### Reconnaissance-Then-Action

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # CRITICAL for JS apps
    
    # Recon: inspect rendered state
    page.screenshot(path='/tmp/inspect.png', full_page=True)
    content = page.content()
    
    # Action: use discovered selectors
    page.locator('button').first.click()
    page.wait_for_selector('.result')
    
    browser.close()
```

### Using with_server.py

```bash
# Single server
python scripts/with_server.py --server "npm run dev" --port 5173 -- python test.py

# Multiple servers
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python test.py
```

## Best Practices

- Use bundled scripts as black boxes — run `--help` first
- Use `sync_playwright()` for synchronous scripts
- Always close browser when done
- Use descriptive selectors: `text=`, `role=`, CSS, IDs
- Add appropriate waits: `wait_for_selector()`, `wait_for_timeout()`

## Common Pitfalls

- ❌ **Inspecting DOM before networkidle** — Dynamic content won't be loaded
- ❌ **Reading script source instead of running --help** — Scripts are designed as black boxes
- ❌ **Not closing browser** — Leaks resources
- ❌ **Brittle selectors** — Use semantic selectors over CSS paths

## Verification Checklist

- [ ] Server starts and is reachable
- [ ] `page.wait_for_load_state('networkidle')` completes
- [ ] Screenshot shows expected content
- [ ] Locators find and interact with the right elements
- [ ] Browser closes cleanly
- [ ] Script handles timeouts gracefully
- [ ] Console logs captured and checked for errors
- [ ] Test works in headless mode
