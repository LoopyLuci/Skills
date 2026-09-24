# Optical Media Parser Implementation Pitfalls

Session-proven patterns and pitfalls for ISO 9660/Joliet/UDF parsing and disc reading.

## ISO 9660 Parser Pitfalls

### File LBA Resolution

**Pitfall:** The path table only stores directory LBAs, not file LBAs. Using `path_table.get(&file_path)` for files always fails.

**Fix:** Walk directory records to find file LBAs:
```rust
fn find_file_lba(&self, path: &str) -> Result<(u32, u32), DiskRipperError> {
    let components: Vec<&str> = path.split('/').collect();
    let mut current_lba = self.root_dir_lba;
    let mut current_size = self.root_dir_size;
    
    for (i, component) in components.iter().enumerate() {
        let records = self.read_directory_records(current_lba, current_size)?;
        if let Some(record) = records.iter().find(|r| r.name == *component) {
            if i == components.len() - 1 {
                return Ok((record.lba, record.data_len));
            }
            current_lba = record.lba;
            current_size = record.data_len;
        }
    }
}
```

### Dual-Endian Reading

**Pitfall:** ISO 9660 stores both LE and BE values. A function named `read_both_endian_*` that only returns LE is misleading.

**Fix:** Read both, log mismatches, return LE as canonical:
```rust
fn read_both_endian_u16(data: &[u8], offset: usize) -> u16 {
    let le = u16::from_le_bytes([data[offset], data[offset + 1]]);
    let be = u16::from_be_bytes([data[offset], data[offset + 1]]);
    if le != be {
        tracing::warn!("Dual-endian mismatch at 0x{:x}: LE=0x{:04x}, BE=0x{:04x}", offset, le, be);
    }
    le
}
```

### Error Propagation in Recursive Directory Walks

**Pitfall:** Calling `self.list_files_recursive(...)` without `?` silently swallows errors. Files go missing with no error.

**Fix:** Always propagate errors:
```rust
if record.is_dir {
    self.list_files_recursive(&path, record.lba, record.data_len, output)?;
}
```

## Joliet UCS-2 Decoding

**Pitfall:** Joliet stores filenames as UCS-2 (big-endian UTF-16). Reading raw bytes as UTF-8 produces mojibake.

**Fix:** Decode UCS-2 BE properly:
```rust
fn decode_ucs2_be(&self, bytes: &[u8]) -> String {
    let mut result = String::with_capacity(bytes.len() / 2);
    let mut i = 0;
    while i + 1 < bytes.len() {
        let code = u16::from_be_bytes([bytes[i], bytes[i + 1]]);
        if code == 0 { break; }
        if let Some(ch) = char::from_u32(code as u32) {
            result.push(ch);
        }
        i += 2;
    }
    result
}
```

## Rock Ridge Extension Parsing

Rock Ridge entries start after the filename in the directory record:

```rust
fn parse_rock_ridge(&self, data: &[u8], name_len: usize) -> Option<RockRidgeData> {
    let rr_start = 33 + name_len;
    let mut pos = rr_start;
    while pos + 4 <= data.len() {
        let sig = &data[pos..pos + 2];
        let entry_len = data[pos + 2] as usize;
        match sig {
            b"PX" => { /* POSIX mode/uid/gid */ }
            b"SL" => { /* Symbolic link */ }
            _ => {}
        }
        pos += entry_len;
    }
}
```

## Multi-Extent File Support

Files > 1GB on DVD/BD use multi-extent records (same filename, consecutive directory records).

**Detection:** Track consecutive records with the same name:
```rust
if current_name.as_ref() == Some(&record.name) {
    current_extents.push(FileExtent { lba: record.lba, size: record.data_len });
} else {
    // Save previous, start new
}
```

**Reading:** Concatenate all extents:
```rust
fn read_multi_extent_data(&self, extents: &[FileExtent]) -> Vec<u8> {
    let mut data = Vec::with_capacity(total_size);
    for extent in extents {
        data.extend_from_slice(&self.read_file_data(extent.lba, extent.size));
    }
    data
}
```

## Cross-Platform Disc Type Detection

### Windows
```rust
// Use PowerShell WMI
Get-WmiObject Win32_CDROMDrive | Where-Object {$_.ID -eq 'D:'} | Select-Object MediaType
```

### Linux
```rust
// Read /proc/sys/dev/cdrom/info for drive-specific disc type
// Or use ioctl(CDROMREADTOCENTRY) for direct detection
```

### macOS
```rust
// Use diskutil info /dev/diskN
```

## Audio CD TOC Parsing

### Windows
Use WMI `Win32_CDROMDrive` to get track count and sector positions.

### Linux
Use `ioctl(CDROMREADTOCHDR)` + `ioctl(CDROMREADTOCENTRY)`:
```rust
let mut toc_hdr = libc::cdrom_tochdr { cdth_trk0: 0, cdth_trk1: 0 };
ioctl(fd, CDROMREADTOCHDR, &mut toc_hdr);
for track in cdth_trk0..=cdth_trk1 {
    let mut entry = libc::cdrom_tocentry { ... };
    ioctl(fd, CDROMREADTOCENTRY, &mut entry);
}
```

### macOS
Parse `diskutil info` output for track boundaries.

## Read Error Recovery

Exponential backoff pattern:
```rust
let mut delay = config.initial_delay_ms;
for attempt in 0..config.max_retries {
    match read_raw_sectors(...) {
        Ok(data) => return Ok(data),
        Err(e) => {
            if attempt < config.max_retries - 1 {
                std::thread::sleep(Duration::from_millis(delay));
                delay = ((delay as f64) * config.backoff_multiplier) as u64;
            }
        }
    }
}
```

## Job Cancellation

Use `tokio_util::sync::CancellationToken` per job:
```rust
// In JobManager
cancellation_tokens: Arc<Mutex<HashMap<JobId, CancellationToken>>>,

// In spawned task
if cancel_token.is_cancelled() {
    let _ = jm.set_status(&jid, JobStatus::Cancelled);
    return;
}
```

## Rip Verification

SHA-256 comparison between source sectors and output:
```rust
let source_checksum = calculate_checksum(&source_data);
let dest_checksum = calculate_checksum(&dest_data);
let valid = source_checksum == dest_checksum;
```

## UDF Detection Bug

**Pitfall:** Identical operands in boolean expression:
```rust
// BROKEN: Both sides of || are identical
if data.len() > 0x8010 && (&data[0x8001..0x8005] == b"NSR0" || &data[0x8001..0x8005] == b"NSR0") {
    return FilesystemType::Udf;
}
```
This silently makes UDF detection impossible — the second condition can never differ from the first.

**Fix:** Use the actual UDF version signatures with correct slice length:
```rust
if data.len() > 0x8010
    && (&data[0x8001..0x8006] == b"NSR02" || &data[0x8001..0x8006] == b"NSR03")
{
    return FilesystemType::Udf;
}
```

## Multi-Extent Detection: Unused Variable

**Pitfall:** Tracking `current_is_dir` during multi-extent collection but never reading it:
```rust
current_is_dir = record.is_dir;  // assigned, never read
current_path = path;
```
This produces `unused_variable` warnings and signals dead logic — if you later need to distinguish file/dir extents, the variable must be used.

**Fix:** Remove the unused assignment:
```rust
// Start new record
current_name = Some(record.name.clone());
current_extents = vec![FileExtent { lba: record.lba, size: record.data_len }];
current_path = path;
```

## Module Organization

```
diskripper-core/src/
  filesystem/
    mod.rs              # FilesystemReader trait, detect_filesystem()
    iso9660.rs          # ISO 9660 + Joliet + Rock Ridge parser
    udf.rs              # UDF parser (stub)
    reader.rs           # Cross-platform raw sector reading
    recovery.rs         # Read error recovery with retries
    verify.rs           # Rip verification
  audio/
    mod.rs              # CD-DA reader, TOC parsing, WAV header
```
