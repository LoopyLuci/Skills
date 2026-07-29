---
name: telegram-file-bridge
description: "Bridge files between Telegram and local file system"
---

# Telegram File Bridge

Send files between Telegram and your local system — download files from Telegram to disk, and upload files from disk to Telegram.

## Receiving Files from Telegram

When a user sends a file on Telegram, the agent can access it:

```python
# File is saved to a temp path
# Use read_file to view text files
read_file("/tmp/telegram_download/document.pdf")

# For binary files, use terminal to inspect
terminal("file /tmp/telegram_download/document.pdf")
terminal("ls -lh /tmp/telegram_download/")
```

## Sending Files to Telegram

Use the MEDIA: protocol to deliver files:

```
MEDIA:/absolute/path/to/file.pdf
```

## Downloading Files from URLs to Telegram

```python
# Download a file and send it
import urllib.request
import os

url = "https://example.com/report.pdf"
dest = "/tmp/report.pdf"
urllib.request.urlretrieve(url, dest)

# Now reference it:
# MEDIA:/tmp/report.pdf
```

## File Size Handling

| Size | Telegram Limit | Action |
|------|---------------|--------|
| < 50 MB | ✅ Sends directly | Use MEDIA: protocol |
| > 50 MB | ❌ Too large | Split or use InstantTransfer |

## Split Large Files

```bash
# Split into 49MB parts
split -b 49M large_file.zip part_

# Send each part
# part_aa, part_ab, part_ac...
```

## Batch Directory Sending

To send an entire folder of files, zip first:

```bash
zip -r /tmp/project.zip /path/to/project/
# Then send the zip via MEDIA:
```

## Cross-Device Bridging

Combine with InstantTransfer protocol:
1. Receive file on Telegram
2. Save to known directory
3. InstantTransfer detects the file
4. Send to paired device via LAN
