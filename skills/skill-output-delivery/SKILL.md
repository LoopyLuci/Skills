---
name: skill-output-delivery
description: Format skill output — media, files, and documents.
---

# Skill Output Delivery

**Trigger**: Use when a skill produces output that needs to be delivered as a file, image, or formatted message rather than plain text.

## Delivery Methods by Content Type

| Content type | Best delivery | Platform support |
|-------------|---------------|-----------------|
| Code/output | Inline code block | All |
| Config file | Code block or `[[as_document]]` | All |
| Screenshot | Image path → auto-delivered | TG, Discord, CLI |
| Diagram | Image path → auto-delivered | TG, Discord, CLI |
| Data file | `[[as_document]]` → attachment | TG, Discord |
| Audio log | `[[audio_as_voice]]` → voice bubble | TG, WhatsApp |
| Source code | `MEDIA:/path/to/file` → file | All |
| Report | `MEDIA:/path/to/report.md` → file | All |

## The MEDIA: Protocol

```markdown
# Include the absolute file path in your response:
MEDIA:C:\Users\user\screenshots\diagram.png

The gateway:
1. Strips the path from visible text
2. Detects file type (image → photo, audio → voice, other → file)
3. Delivers natively to the chat platform

Supported: .png, .jpg, .webp (photos), .ogg (voice), .mp4 (video)
```

## The [[as_document]] Directive

```markdown
# Telegram recompresses photos to ~200KB — destroying detail.
# Force document-style delivery (lossless):

"Here's your chart:
/home/user/.hermes/cache/chart.png

[[as_document]]"

→ Delivers as file, not recompressed image
→ Affects ALL media paths in the same response
→ Use for: screenshots with text, charts, high-res renders
```

## The [[audio_as_voice]] Directive

```markdown
# Promote audio files to voice message bubbles:
[[audio_as_voice]]

Platforms: Telegram, WhatsApp (voice bubbles)
Others: regular audio attachment
```

## Skill Output Patterns

### Step-by-Step with Commands
Use when skill produces procedural instructions

### Configuration Output
Use when skill produces config files, YAML, JSON
```markdown
/config.yaml — Add to your config:
\```yaml
skills:
  external_dirs:
    - ~/Skills/skills
\```
```

### Media-Rich Output
Use when skill generates images or screenshots
```markdown
MEDIA:/home/user/diagram.png
```

### Report as File
Use when result is too long for chat
```markdown
MEDIA:/home/user/analysis-report.md
Done. Full report attached.
```

## Platform Considerations

| Platform | Images | Files | Notes |
|----------|--------|-------|-------|
| Telegram | Auto-photo | MEDIA: works | Use [[as_document]] for quality |
| Discord | Embed | Attachments | 8MB/25MB limits |
| CLI | Direct | Direct | Full control |
| SMS | None | Text only | Always inline |

## Pitfalls
- **Recompression**: Telegram recompresses photos to ~200KB at 1280px — use [[as_document]] for text screenshots
- **Missing file**: MEDIA: with non-existent path = broken attachment — verify file exists first
- **Dual delivery**: Inline text + MEDIA: for same content = confusing
- **Platform gaps**: MEDIA: on SMS may not render — include essential info as text

## Verification
```bash
[ -f "/path/to/file.png" ] && echo "READY" || echo "NOT FOUND"
```
