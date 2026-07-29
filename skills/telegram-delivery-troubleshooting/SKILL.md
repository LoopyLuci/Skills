---
name: telegram-delivery-troubleshooting
description: "Fix Telegram file delivery when MEDIA protocol fails to send"
---

# Telegram Delivery Troubleshooting

When the MEDIA: protocol doesn't deliver files to Telegram, here's how to diagnose and work around it.

## Symptoms

| Symptom | Likely Cause |
|---------|-------------|
| File sent to Hermes desktop but not Telegram | Gateway routing: MEDIA delivers to current surface |
| MEDIA: tag appears in text but no file | Path not accessible to gateway process |
| "File not found" error | Wrong path format or gateway runs on different host |

## Workarounds When MEDIA: Fails

### Option 1: HTTP Server (Same WiFi)

```bash
# Start HTTP server in the file's directory
cd /path/to/directory
python -m http.server 8888

# Get your local IP
python -c "import socket; s=socket.socket(); s.connect(('8.8.8.8',80)); print(s.getsockname()[0]); s.close()"

# Share URL: http://192.168.x.x:8888/filename.apk
```

The recipient opens the URL in their phone browser to download.

### Option 2: Copy to Downloads

```bash
cp /path/to/file.apk /c/Users/Username/Downloads/
```

Sometimes the gateway has better access to the user's Downloads folder.

### Option 3: Use Cron Delivery

```bash
hermes cron create \
  --schedule "now" \
  --prompt "Tell the user their file is at /path/to/file.apk" \
  --deliver "telegram:chat_id"
```

### Option 4: Upload to Cloud

Use a temporary file share and provide the link.

## Prevention

If MEDIA: consistently fails on Telegram:
1. Check the gateway is configured for Telegram file delivery
2. Verify the file is under 50MB (Telegram limit)
3. Ensure the file path is readable by the gateway process
4. Try both MSYS (`/c/Users/...`) and Windows (`C:\Users\...`) path formats
