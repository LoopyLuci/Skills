---
name: chunked-streaming
description: "Stream large files in chunks with CRC or hash verification"
---

# Chunked File Streaming

Transfer large files by splitting them into fixed-size chunks and streaming over TCP. Avoids loading the entire file into memory.

## Architecture

```
Sender                          Receiver
  │                               │
  ├── META (name, size, hash)   ►│
  ├── CHUNK (1MB seq=0) ───────►│
  ├── CHUNK (1MB seq=1) ───────►│
  ├── CHUNK (1MB seq=2) ───────►│
  ├── ...                       │
  ├── DONE (final_hash) ───────►│
  │                               │
  │  Verify hash on receive       │
```

## Python Implementation

### Sender

```python
import hashlib
import os

CHUNK_SIZE = 1024 * 1024  # 1 MB

def stream_file(filepath, send_chunk_fn):
    total = os.path.getsize(filepath)
    sha256 = hashlib.sha256()
    seq = 0

    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sha256.update(chunk)
            send_chunk_fn(chunk, seq, total)
            seq += 1

    return sha256.hexdigest()
```

### Receiver

```python
def receive_file(filepath, total_size, receive_chunk_fn):
    sha256 = hashlib.sha256()
    received = 0

    with open(filepath, "wb") as f:
        while received < total_size:
            chunk = receive_chunk_fn()
            if not chunk:
                break
            f.write(chunk)
            sha256.update(chunk)
            received += len(chunk)

    return sha256.hexdigest()
```

## Protocol Format

Wrap each chunk in a length-prefixed message:

```
[4 bytes: total message length]
[message type: "META" | "CHUNK" | "DONE" | "ERROR"]
[payload]
```

For CHUNK messages:
```
[4 bytes: sequence number]
[4 bytes: chunk size]
[N bytes: chunk data]
```

## Progress Tracking

Report progress every N chunks or every 500ms:

```python
progress = received / total * 100
speed = bytes_in_last_second / 1024 / 1024  # MB/s
eta = (total - received) / speed  # seconds
```

## Resumable Transfers

To support resume:

1. Receiver tells sender how many bytes it already has
2. Sender seeks to that position: `f.seek(resume_offset)`
3. Both sides continue from the offset

```
RECEIVER → RESUME_REQ(offset=524288)
SENDER   → META(..., resume_from=524288)
SENDER   → CHUNK(seq=1, data=...)
```

## Verification

- **SHA-256** — full-file hash sent in DONE message, verified by receiver
- **Per-chunk CRC32** — optional, adds overhead but catches corruption early
- **Compare hash** — abort on mismatch

## Constants

| Parameter | Recommended |
|-----------|-------------|
| CHUNK_SIZE | 1 MB (1048576) |
| Progress interval | 500ms |
| Connection timeout | 300s (5 min) |
| Max parallel | 4 streams |
