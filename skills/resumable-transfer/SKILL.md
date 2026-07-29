---
name: resumable-transfer
description: "Resume interrupted file transfers from last offset"
---

# Resumable File Transfer

When a file transfer is interrupted, resume from where it stopped instead of starting over.

## How Resume Works

```
Sender                          Receiver
  │                               │
  ├── META (file: report.mp4,    │
  │        size: 100MB, hash: X)►│
  ├── CHUNK (offset: 0-1MB) ───►│
  ├── CHUNK (offset: 1-2MB) ───►│
  │         ... connection lost! │
  │                               │
  │  (reconnect)                  │
  │                               │
  ├── META (file: report.mp4,    │
  │        size: 100MB,           │
  │        resume_from: 2097152)►│
  ├── CHUNK (offset: 2-3MB) ───►│
  │         ...                  │
  ├── DONE ─────────────────────►│
```

## Implementation

### Receiver Side (tracks progress)

```python
# Save progress after each chunk
resume_file = f"{filepath}.itpart"

def save_progress(filepath, offset):
    with open(f"{filepath}.itpart", "w") as f:
        f.write(str(offset))

def load_progress(filepath):
    try:
        with open(f"{filepath}.itpart") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0
```

### Sender Side (seeks to offset)

```python
def send_file_resume(filepath, resume_offset=0, send_chunk_fn):
    total = os.path.getsize(filepath)

    with open(filepath, "rb") as f:
        if resume_offset > 0:
            f.seek(resume_offset)

        while f.tell() < total:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            send_chunk_fn(chunk, f.tell())
```

### Protocol Extension

Add resume support to the metadata exchange:

```json
{
  "type": "FILE_META",
  "payload": {
    "file_id": "abc123",
    "rel_path": "video.mp4",
    "total_size": 104857600,
    "resume_offset": 2097152
  }
}
```

## Progress File Cleanup

Delete `.itpart` files after successful transfer:

```python
def cleanup(filepath):
    part_file = f"{filepath}.itpart"
    if os.path.exists(part_file):
        os.remove(part_file)
```

## When Resume Is Useful

| File Size | Resume Benefit |
|-----------|----------------|
| < 10 MB | Not worth it (just retry) |
| 10-100 MB | Helpful on spotty connections |
| 100 MB+ | Essential |
| 1 GB+ | Required |
