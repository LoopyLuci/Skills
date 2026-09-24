# DiskRipper Workspace Patterns

Session-proven patterns from building DiskRipper (September 2026).

## Workspace Structure

```
Cargo.toml              # workspace root, edition 2024, resolver "2"
diskripper-core/        # library + CLI binary (diskripper.exe)
  src/
    lib.rs              # module exports only (no binary code)
    main.rs             # CLI binary entry (uses diskripper_core:: imports)
    rip.rs              # RipEngine
    image.rs            # streaming disc imaging
    filesystem/         # ISO 9660, UDF parsers
  Cargo.toml            # [[bin]] name="diskripper" path="src/main.rs"
diskripper-tauri/       # Tauri GUI app (diskripper-gui.exe)
  src/lib.rs
  tauri.conf.json
  Cargo.toml            # [[bin]] name="diskripper-gui" (NOT diskripper)
frontend/               # React/TypeScript UI
  src/
  package.json
packages/mcp-server/    # TypeScript MCP server wrapping CLI binary
  src/index.ts
  src/cli.ts
  dist/cli.js           # built entry point
scripts/
  raw.ps1               # Win32 raw disc I/O helper
```

## Binary Naming Rule

Two `[[bin]]` targets in a workspace **must not share the same output name**. The Tauri app was renamed to `diskripper-gui` to avoid collision with the CLI `diskripper` binary.

```toml
# diskripper-core/Cargo.toml
[[bin]]
name = "diskripper"
path = "src/main.rs"

# diskripper-tauri/Cargo.toml
[[bin]]
name = "diskripper-gui"
path = "src/main.rs"
```

## CLI Binary Imports

The CLI binary (`main.rs`) is a separate binary binary crate that depends on the library crate. It must use `diskripper_core::` imports, NOT `crate::`:

```rust
// CORRECT (in main.rs)
use diskripper_core::rip::RipEngine;
use diskripper_core::types::RipOptions;

// WRONG (in main.rs)
use crate::rip::RipEngine;  // fails: crate refers to binary, not library
```

## Module Hygiene

When moving code from `lib.rs` to `main.rs`:
1. Remove the module declaration from `lib.rs` (e.g., `pub mod cli;`)
2. Move the module file to `main.rs` (or keep as separate file included via `mod cli;` in main.rs)
3. Update all imports from `crate::` to `diskripper_core::`

## Edition 2024

DiskRipper uses `edition = "2024"` in the workspace root. This enables:
- `async fn` in traits without `async-trait`
- Gen expressions
- Improved lifetime capture

**Note**: Edition 2024 requires Rust 1.85+.

## Windows Raw Disc I/O (Native FFI)

### The `windows` vs `windows-sys` Decision

For optical drive IOCTLs, prefer `windows-sys` over the `windows` crate:

```rust
// CORRECT: windows-sys with raw constants
use windows_sys::Win32::Storage::FileSystem as FS;
use windows_sys::Win32::Foundation as Found;

let handle = FS::CreateFileW(
    wide_path.as_ptr(),
    FS::GENERIC_READ,
    FS::FILE_SHARE_READ | FS::FILE_SHARE_WRITE,
    std::ptr::null(),
    FS::OPEN_EXISTING,
    0,
    0,
);
if handle == Found::INVALID_HANDLE_VALUE { /* handle error */ }

// WRONG: windows crate (causes compile errors)
use windows::Win32::Storage::FileSystem::*;
let handle = CreateFileW(
    windows::core::PCWSTR(wide_path.as_ptr()),
    GENERIC_READ.0,  // .0 syntax causes issues
    ...
);
```

**Why**: The `windows` crate's `PCWSTR` wrapper and `GENERIC_READ.0` syntax causes compile errors with certain feature combinations. `windows-sys` uses raw constants that work reliably.

### IOCTL Codes for Optical Drives

```rust
const IOCTL_CDROM_RAW_READ: u32 = 0x0002403E;
const IOCTL_CDROM_GET_TOC: u32 = 0x0004D00E;
const IOCTL_DISK_GET_LENGTH_INFO: u32 = 0x0007405C;
const IOCTL_SCSI_PASS_THROUGH_DIRECT: u32 = 0x0004D004;
```

### CDDA Sector Size

Audio CDs use **2352 bytes per sector**, not 2048. This is critical for raw ripping.

### Disc Size Detection

Use `IOCTL_DISK_GET_LENGTH_INFO` for accurate disc size when other methods fail.

## Streaming I/O Pattern

Never read entire disc images into memory. Use 8MB async buffer:

```rust
let mut buffer = vec![0u8; 8 * 1024 * 1024];
loop {
    let n = reader.read(&mut buffer).await?;
    if n == 0 { break; }
    writer.write_all(&buffer[..n]).await?;
    tracker.add_bytes(n as u64);
}
```

## Event-Driven Progress

Frontend subscribes to backend events instead of polling:

```rust
// Backend
app_handle.emit_all("job:update", &progress).ok();

// Frontend (TypeScript)
listen('job:update', (event) => updateJob(event.payload));
```

## MCP Server Registration

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  diskripper:
    command: node
    args:
      - C:/Projects/DiskRipper/packages/mcp-server/dist/cli.js
    timeout: 300
    connect_timeout: 120
```

## Git + node_modules Timeout

`git add -A` times out (exit 124) when `frontend/node_modules` exists, even with `.gitignore`. Fix:

```bash
# Stage selectively
git add .gitignore Cargo.toml diskripper-core/ diskripper-tauri/ frontend/src/ packages/ scripts/ .github/
# Verify node_modules not staged
git status | grep node_modules  # should be empty
git commit -m "message"
```

## Real Disc Test Results

| Disc | Format | Size | Result |
|------|--------|------|--------|
| Audio CD | CD-DA | 158MB | 101MB raw ISO via IOCTL_CDROM_RAW_READ |
| Freddi Fish 4 | HFS | 475MB | 154 files extracted via mounted-drive fallback |

## Error Enum Pattern

```rust
// error.rs
#[derive(Error, Debug, Clone)]
pub enum DiskRipperError {
    #[error("IO error: {0}")]
    Io(String),    // NOT IOError
}

// Usage
DiskRipperError::Io(e.to_string())  // CORRECT
DiskRipperError::IOError(e.to_string())  // WRONG - E0599
```

## Cross-Platform Filesystem Module Pattern

Use conditional compilation to support Windows, Linux, and macOS:

```rust
// filesystem/mod.rs
#[cfg(target_os = "windows")]
pub mod native_win;

#[cfg(target_os = "linux")]
pub mod linux_sg;

#[cfg(target_os = "macos")]
pub mod macos_iokit;

// Re-export platform-specific types
#[cfg(target_os = "windows")]
pub use native_win::{NativeDriveHandle, TocTrack};

#[cfg(target_os = "linux")]
pub use linux_sg::{TocTrack as LinuxTocTrack};
```

## DVD IFO Parsing

Full parser for DVD-Video IFO files:

```rust
pub struct DvdParser;

impl DvdParser {
    pub fn parse_ifo(&self, ifo_path: &Path) -> Result<Vec<DvdTitle>, DiskRipperError> {
        // Parse VMG (Video Manager) and VTS (Video Title Set) structures
        // Extract titles, chapters, audio tracks, subtitle tracks
    }
}
```

**Key structures:**
- VMG: Contains title search pointer table
- VTS: Contains title management table (VTS_MAT) with audio/subtitle stream info
- PGC: Program Chain with chapter/cell information

**BCD time format**: DVDs use BCD-encoded time (HH:MM:SS:FF):
```rust
fn parse_bcd_time(data: &[u8]) -> f64 {
    let hours = (data[0] >> 4) * 10 + (data[0] & 0x0F);
    let minutes = (data[1] >> 4) * 10 + (data[1] & 0x0F);
    let seconds = (data[2] >> 4) * 10 + (data[2] & 0x0F);
    let frames = (data[3] >> 4) * 10 + (data[3] & 0x0F);
    hours as f64 * 3600.0 + minutes as f64 * 60.0 + seconds as f64 + frames as f64 / 75.0
}
```

## CD-Text Parsing

CD-Text is stored in packs of 18 bytes:

```rust
pub struct CdTextParser;

impl CdTextParser {
    pub fn parse(raw_data: &[u8]) -> Result<CdTextInfo, DiskRipperError> {
        // Each pack: type(1) + track(1) + sequential(1) + char_pos(1) + data(12) + crc(2)
        // Pack types: 0x80=title, 0x81=performer, 0x82=songwriter, etc.
    }
}
```

## Multisession CD Support

```rust
pub struct MultisessionReader;

impl MultisessionReader {
    pub fn read_toc(drive_path: &str) -> Result<CdToc, DiskRipperError> {
        // Send SCSI READ TOC command, parse sessions and tracks
    }
    
    pub fn is_mixed_mode(toc: &CdToc) -> bool {
        // True if both audio and data tracks present
    }
}

pub struct EnhancedCdReader;

impl EnhancedCdReader {
    pub fn is_enhanced_cd(toc: &CdToc) -> bool {
        // True if session 1 = audio, session 2 = data
    }
}
```

## FLAC Compression

External flac encoder integration with WAV fallback:

```rust
pub struct FlacEncoder;

impl FlacEncoder {
    pub fn is_available() -> bool {
        Command::new("flac").arg("--version").output().is_ok()
    }
    
    pub fn compress(wav_path: &Path, flac_path: &Path, compression: FlacCompression) -> Result<(), DiskRipperError> {
        // Run: flac --compression-level-N --force --quiet -o output.flac input.wav
    }
}
```

## AccurateRip Verification

CRC32-based checksums for audio CD verification:

```rust
pub struct AccurateRipVerifier;

impl AccurateRipVerifier {
    pub fn calculate_checksum(track_data: &[u8], track_number: u32, total_tracks: u32, drive_offset: i32) -> u32 {
        // CRC32 with AccurateRip-specific offsets
        // Skip first/last second for first/last tracks
        // Apply drive offset correction
    }
    
    pub fn calculate_disc_id(track_offsets: &[u64]) -> String {
        // SHA-1 hash of track offsets, base64-encoded
    }
}
```

## System Tray Integration

```rust
// In tauri::Builder
let _tray = TrayIconBuilder::with_id("main-tray")
    .tooltip("DiskRipper - Media Backup")
    .icon(window.default_window_icon().unwrap().clone())
    .menu(&tray_menu)
    .on_menu_event(|app, event| match event.id.as_ref() {
        "show" => { /* show window */ }
        "hide" => { /* hide window */ }
        "quit" => { app.exit(0); }
        _ => {}
    })
    .on_tray_icon_event(|tray, event| {
        if let TrayIconEvent::Click { .. } = event {
            // Toggle window visibility
        }
    })
    .build(&builder);
```

## Auto-Updater Configuration

```json
// tauri.conf.json
{
  "plugins": {
    "updater": {
      "active": true,
      "endpoints": [
        "https://github.com/LoopyLuci/DiskRipper/releases/latest/download/latest.json"
      ],
      "dialog": true,
      "pubkey": ""
    }
  }
}
```

```toml
# Cargo.toml
[dependencies]
tauri-plugin-updater = "2"
```

## The "Proceed With All" Execution Pattern

When the user says "proceed with all" or "properly proceed with all":

1. **Execute ALL identified workstreams** - not just the first few
2. **In order** - follow the priority sequence
3. **With verification after each step** - cargo check, tests, real disc tests
4. **Then STOP** - do not generate another roadmap or workstream
5. **Report verified state** - real tool output, not descriptions

**Anti-pattern that triggers user frustration:**
- Complete some items → generate more items → complete some → generate more → infinite loop
- This is NOT what "proceed with all" means

**Correct behavior:**
- Identify the COMPLETE scope upfront
- Execute ALL of it
- Verify completion
- STOP and report
- Wait for user direction before starting new work

## Performance Warning: PowerShell Batching

PowerShell per-read batching is **extremely slow** for large discs. Reading 50 sectors at a time via PowerShell subprocess means ~100k process spawns for a 25GB Blu-ray. For production use, compile a Rust helper using `windows-sys` with direct `DeviceIoControl` calls.

## References

- `references/windows-toolchain-fixes.md` — concrete error codes and fixes
- `references/tauri2-schema.md` — Tauri 2 config field mapping
- `references/git-windows-init.md` — non-interactive git initialization
- `references/frontend-ipc-wiring.md` — React/Tauri IPC wiring
