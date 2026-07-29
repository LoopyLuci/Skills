---
name: telegram-message-formatting
description: "Format messages for Telegram Markdown bold italic links code"
---

# Telegram Message Formatting

Telegram uses a **subset** of Markdown. These rules ensure your messages render correctly.

## Supported Formatting

| Style | Syntax | Example |
|-------|--------|---------|
| Bold | `**text**` | **bold** |
| Italic | `*text*` | *italic* |
| Underline | `__text__` | <u>underline</u> |
| Strikethrough | `~~text~~` | ~~strikethrough~~ |
| Spoiler | `\|\|text\|\|` | ||spoiler|| |
| Inline code | `` `code` `` | `code` |
| Code block | ```` ```lang ... ``` ```` | Multi-line code |
| Links | `[text](url)` | [link](https://example.com) |
| Pre-formatted | Indented 4 spaces | Preserved whitespace |

## Critical Rules

**1. No nested formatting** — bold inside italic, code inside bold all fail silently.
```diff
- **bold *and italic** text*   ← BROKEN
+ **bold text** and *italic*   ← OK separately
```

**2. Link text cannot contain formatting** — `**[bold link](url)**` does NOT work. Use `[bold link](url)` in bold context instead.

**3. Code blocks need a language hint** for syntax highlighting on mobile:
````
```python
print("hello")
```
````

**4. Emoji within formatting** — most emoji work inside bold/italic but some break. Test if unsure.

**5. Escape special characters** with backslash if they appear literally:
```
\*not italic\* \`not code\`
```

## Headers

Only `## Header` (level 2) renders as a header. `#` and `###` show as plain text.

```
## This renders as header
# This does not
```

## Best Practices

| Goal | Do This |
|------|---------|
| Key-value pairs | `**Name:** Value` on its own line |
| Bullet lists | `- item` with blank line before list |
| Code in lists | Use 4-space indent after `- ` |
| Mixed content | Use separate lines, not inline mixing |
| Status indicators | Use ✅ ❌ ⚠️ 🔥 ● ○ at line start |
