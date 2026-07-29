---
name: telegram-media-delivery
description: "Send files via MEDIA protocol on Telegram paths and limits"
---

# Telegram Media Delivery

Reliably deliver files, images, audio, and video through Telegram using the `MEDIA:` protocol directive.

## How It Works

Include `MEDIA:/absolute/path/to/file` in your response text. The Telegram gateway picks it up and sends it as a native attachment.

## Supported Media Types

| Type | Extension | Telegram Behavior |
|------|-----------|-------------------|
| Images | `.png` `.jpg` `.webp` `.gif` | Sent as photos (compressed) |
| Documents | `.pdf` `.docx` `.zip` `.apk` | Sent as files (no compression) |
| Audio | `.ogg` | Sent as voice bubble |
| Video | `.mp4` `.webm` | Sent as video (compressed) |
| Any file | `.*` | Sent as document |

## File Limits

| Plan | Max Size | Notes |
|------|----------|-------|
| Default | 50 MB | Standard Telegram limit |
| Premium | 2 GB | If recipient has Telegram Premium |
| Bot API | 50 MB | Bot API limit regardless |

## Path Formats (Windows Host)

On Windows these path styles all work:

| Format | Example | Works? |
|--------|---------|--------|
| MSYS/Unix | `MEDIA:/c/Users/dubem/file.apk` | ✅ Preferred |
| Windows | `MEDIA:C:\Users\dubem\file.apk` | ✅ Works |
| MSYS long | `MEDIA:/c/Projects/foo/file.apk` | ✅ Works |

**Best practice:** use MSYS path style (`/c/Users/...`) — consistent with the shell.

## Troubleshooting

If a file doesn't arrive:

1. **Verify it exists:** `ls -la /c/Users/.../file.ext`
2. **Check size:** `ls -lh` — must be under 50 MB
3. **Check permissions:** file must be readable by the agent process
4. **Check path format:** use MSYS `/c/Users/...` style
5. **File type:** APKs send as documents, not apps

## Common Pitfalls

**File exists but "not found"** — the MEDIA: path is resolved on the gateway host, not the terminal host. If they differ, copy to a shared path.

**File over 50MB** — split into parts, use InstantTransfer protocol, or upload to cloud storage and share the URL.

**APK delivery** — APKs arrive as documents (.apk extension). On mobile Telegram the user taps to download and install. On Desktop they save the file.
