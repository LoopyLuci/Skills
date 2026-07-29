# InstantTransfer Wire Protocol

## Transport
- TCP, length-prefixed JSON messages
- Every message: `[4-byte big-endian message length][JSON payload]`
- Control port: **48761**
- Data ports: **48762–48772**

## Message Format
```json
{
  "type": "MESSAGE_TYPE",
  "payload": { ... }
}
```

## Message Types

### Discovery
Broadcast via mDNS `_instanttransfer._tcp` with TXT records:
- `device_id` — Permanent UUID
- `device_name` — Human-readable name
- `device_type` — "windows" or "android"
- `paired_ids` — Comma-separated known device IDs

### Pairing Flow
```
Initiator                    Receiver
   │                           │
   ├── HELLO ────────────────► │
   │ ◄── HELLO ───────────────┤
   │                           │
   ├── PAIR_INIT ────────────► │
   │ ◄── PAIR_PIN (6-digit) ──┤
   │                           │
   │  (Both display PIN)       │
   │  (User taps Approve)      │
   │                           │
   ├── PAIR_APPROVE ─────────► │
   │ ◄── PAIR_APPROVE ────────┤
   │                           │
   ├── PAIR_CONFIRM ─────────► │
   │ ◄── PAIR_ACK ────────────┤
   │                           │
   │   ✅ Paired permanently   │
```

### File Transfer Flow
```
Sender                       Receiver
  │                            │
  ├── FILE_OFFER (job_id,     ►│
  │    file_count, total_size, │
  │    file_list[])            │
  │ ◄── FILE_ACCEPT ──────────┤
  │     (or FILE_REJECT)       │
  │                            │
  │  For each file:            │
  ├── FILE_META (file_id,     ►│
  │    rel_path, total_size)   │
  ├── FILE_CHUNK (data) ─────►│
  ├── FILE_CHUNK (data) ─────►│
  │         ...                │
  ├── FILE_DONE ─────────────►│
  │                            │
  │  (Meanwhile)               │
  │ ◄── PROGRESS (bytes) ─────┤
  │                            │
  │  All files done            │
  │   ✅ Transfer complete     │
```

## Error Handling
- `FILE_ERROR` — sender reports an error
- `CANCEL` — either side cancels the transfer
- `BYE` — clean disconnect

## Security
- Pairing PIN: 6 digits (1,000,000 combinations)
- Pairing timeout: 30 seconds
- Rate limit: 3 attempts per minute per IP
- Transfer encryption: self-signed TLS (trust-on-first-use)
