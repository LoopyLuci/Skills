# Optical Media Filesystem Reference

Domain knowledge for CD/DVD/Blu-ray backup and imaging projects.

## Disc Types and Capacities

| Disc Type | Capacity (bytes) | Notes |
|-----------|-----------------|-------|
| CD-ROM | 700 MB | 80-minute disc |
| CD-R | 700 MB | Recordable |
| CD-RW | 700 MB | Rewritable |
| DVD-ROM | 4.7 GB | Single-layer |
| DVD-R | 4.7 GB | Single-layer |
| DVD+R DL | 8.5 GB | Dual-layer |
| BD-ROM | 25 GB | Single-layer |
| BD-R DL | 50 GB | Dual-layer |
| HD DVD | 15 GB | Obsolete |

## Filesystem Signatures

### ISO 9660
- Magic: `CD001` at offset `0x8001` (sector 16, byte 1)
- Primary Volume Descriptor (PVD) at sector 16 (offset `0x8000`)
- Block size: 2048 bytes (stored at PVD offset 128, both-endian u16)
- Path table at PVD offset 132 (size) and 140 (LBA)
- Root directory record at PVD offset 156

### Joliet (ISO 9660 Extension)
- Supplementary Volume Descriptor (SVD) at sector 17 (offset `0x8800`)
- Magic: `CD001` at offset `0x8801`
- Escape sequences at SVD offset 88:
  - `0x25 0x2F 0x40` = Level 1 (Joliet)
  - `0x25 0x2F 0x43` = Level 2
  - `0x25 0x2F 0x45` = Level 3
- Uses UCS-2 encoding for filenames (up to 64 chars)

### HFS (Hierarchical File System)
- Magic: `BD` (0x42 0x44) at offset 0x8001 (sector 16, byte 1)
- Used by classic Mac OS and some hybrid discs (e.g., Freddi Fish 4 game CD)
- **Not ISO 9660** — requires a separate parser or fallback to mounted-drive extraction
- Hybrid discs may contain both ISO 9660 and HFS volumes
- **Fallback strategy**: When filesystem detection returns Unknown and the drive is mounted, scan the mounted filesystem directly via `std::fs::read_dir` rather than trying to parse raw sectors

### UDF (Universal Disk Format)
- Magic: `NSR02` or `NSR03` at offset `0x8001`
- More complex than ISO 9660, uses Anchor Volume Descriptor Pointer (AVDP)
- Supports larger files, Unicode, and packet writing

### CD-DA (Digital Audio)
- No filesystem — raw 2352-byte sectors of PCM audio
- 75 sectors per second, 44100 Hz, 16-bit stereo
- 2352 bytes/sector = 44100 × 2 channels × 2 bytes
- Requires jitter correction for accurate ripping

## ISO 9660 PVD Structure (Key Offsets)

| Offset | Size | Field |
|--------|------|-------|
| 1 | 5 | Standard Identifier ("CD001") |
| 8 | 32 | System Identifier |
| 40 | 32 | Volume Identifier |
| 80 | 4 | Volume Space Size (blocks, LE) |
| 88 | 32 | Volume Set Identifier |
| 128 | 2 | Logical Block Size (both-endian) |
| 132 | 4 | Path Table Size (LE) |
| 140 | 4 | Type-L Path Table LBA (LE) |
| 156 | 34 | Root Directory Record |

## Directory Record Format

| Offset | Size | Field |
|--------|------|-------|
| 1 | 1 | Record Length |
| 2 | 4 | Data LBA (LE) |
| 10 | 4 | Data Length (LE) |
| 25 | 1 | Flags (0x02 = directory) |
| 32 | 1 | Filename Length |
| 33 | N | Filename (padded, ends with ";1" for files) |

## Cross-Platform Raw Sector Reading

### Windows
- Use `FILE_FLAG_NO_BUFFERING` + `FILE_FLAG_SEQUENTIAL_SCAN`
- Open with `CreateFileW` or `OpenOptionsExt::custom_flags()`
- ReadFile with aligned buffer

### Linux
- Open with `O_RDONLY` (and `O_NONBLOCK` for some drives)
- Use `lseek()` + `read()` or `pread()`
- For SCSI: `SG_IO` ioctl for MMC commands

### macOS
- Open with `O_RDONLY`
- Use `lseek()` + `read()`
- For IOKit: `IOCDMedia` / `IOCDServices`

## WAV Header for CD-DA (44 bytes)

```
Offset  Size  Field
0       4     "RIFF"
4       4     file_size - 8 (LE)
8       4     "WAVE"
12      4     "fmt "
16      4     16 (sub-chunk size, LE)
20      2     1 (PCM format, LE)
22      2     2 (channels, LE)
24      4     44100 (sample rate, LE)
28      4     176400 (byte rate, LE)
32      2     4 (block align, LE)
34      2     16 (bits per sample, LE)
36      4     "data"
40      4     data_size (LE)
```

## Jitter Correction

Audio CDs require jitter correction because:
- Drive read offset varies between models
- Adjacent reads of the same sector may return slightly different data
- Verification: re-read sectors and compare, or use AccurateRip database

Simple verification heuristic:
- Reject sectors that are all zeros or all same byte
- Re-read up to N times until valid audio pattern detected
- Track read offset per drive for future sessions
