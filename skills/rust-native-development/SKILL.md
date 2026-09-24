---
name: rust-native-development
description: "Rust native: deterministic engines, Tauri, WASM plugins."
---

# Rust Native Development

Use when building, debugging, or scaffolding Rust projects that require native linking on Windows, macOS, or Linux—especially multi-crate workspaces, Tauri desktop apps, game/simulation backends, or systems programming with deterministic requirements.

## Scope

This skill covers:
- Multi-crate workspace layout and Cargo.toml configuration
- Tauri 2 desktop app scaffolding (Rust backend + React/TypeScript frontend)
- Deterministic simulation engines (genetics, physics, procedural generation)
- Windows MSVC linker troubleshooting
- Property-based testing with `proptest`
- WASM plugin systems with `wasmtime`
- Authoritative server scaffolding (Axum + PostgreSQL + Redis)

For platform-specific packaging (MSI, AppImage, DMG), see Tauri's built-in bundler docs.

## Workspace Layout

Prefer this structure for desktop + simulation projects:

```
Cargo.toml          # workspace root, resolver = "2", edition = "2021"
crates/
  genetics/         # pure deterministic engine, zero UI/networking deps
    src/lib.rs
    benches/
    tests/
  protocol/         # cross-platform serialization + crypto
    src/lib.rs
  plugin/           # WASM plugin API + host loader
    src/lib.rs
server/             # authoritative backend
  src/main.rs
  src/state.rs
  src/handlers.rs
  src/persistence.rs
app/
  package.json      # React + TypeScript + Vite
  src/
    App.tsx
    views/
  src-tauri/
    Cargo.toml
    src/main.rs     # Tauri commands, app state
    tauri.conf.json
deploy/
  docker-compose.yml
  Dockerfile.server
```

## Key Rules

1. **Edition**: Always set `edition = "2021"` explicitly at workspace level in the root `Cargo.toml`. Do not rely solely on `workspace.package` inheritance for edition, because some tooling still falls back to 2015 if not explicitly set in the root manifest.

2. **Resolver**: Use `resolver = "2"` in the workspace root.

3. **Tauri feature hygiene**: Tauri 2 feature names change across versions. Before adding a feature, verify it exists in the resolved version. Common pitfall: `shell-open` was removed; use `shell` plugin instead.

4. **Determinism**: Centralize RNG in the engine struct. Only the server generates crossover seeds. Clients must never choose their own offspring seeds in authoritative mode.

5. **No placeholder code**: Every module must compile and link. If a feature is incomplete, gate it behind a feature flag or TODO comment—never leave syntactically invalid stubs.

## Windows Linker Troubleshooting

### Symptom

```
error: linking with `link.exe` failed: exit code: 1
  = note: link: extra operand '...build_script_build....rcgu.o'
```

### Diagnosis

Run:
```bash
where link.exe
```

If the first result is `...\git\usr\bin\link.exe` or `...\mingw64\bin\link.exe`, the MSVC linker is being shadowed by a GNU-compatible wrapper from Git Bash or MSYS2.

### Fixes

1. **Preferred**: Install Visual Studio Build Tools with the **C++ build tools** workload. This provides the real MSVC `link.exe`.

2. **Alternative**: Remove or reorder the Git Bash / MSYS2 `link.exe` shim from PATH before invoking Cargo. Do NOT delete the shim—other tools may need it. Instead, launch Cargo from a proper "x64 Native Tools Command Prompt for VS" or set `LIB`/`LIBPATH`/`INCLUDE` manually.

3. **Verification**: After fix, `cargo check --workspace` should complete without `link.exe` errors. Build script `.o` files must be consumed by the MSVC linker, not treated as extra operands.

### Do Not Capture

Do NOT record this as a permanent constraint like "Windows cannot compile Rust". The failure is environmental, not code-related. The skill records the *fix pattern*, not the failure.

## Property-Based Testing

Use `proptest` for deterministic engine validation:

```rust
proptest! {
    #[test]
    fn crossover_determinism(seed_a: [u8; 32], seed_b: [u8; 32], cross_seed: [u8; 32]) {
        let a = make_cube(seed_a);
        let b = make_cube(seed_b);
        let c1 = engine.crossover(&a, &b, cross_seed).unwrap();
        let c2 = engine.crossover(&a, &b, cross_seed).unwrap();
        prop_assert_eq!(c1.genome.hash(), c2.genome.hash());
    }
}
```

Always test: determinism, hash collision resistance, and boundary conditions (inbreeding thresholds, mutation saturation).

## Tauri IPC Pattern

Frontend TypeScript declarations:

```ts
declare global {
  interface Window {
    __cw: {
      create_cube: (req: { name: string; sex: string; seed?: Uint8Array }) => Promise<CubeResponse>;
      breed_cubes: (req: BreedRequest) => Promise<CubeResponse[]>;
      get_cube: (id: string) => Promise<CubeResponse>;
      list_cubes: () => Promise<CubeResponse[]>;
    };
  }
}
```

Backend Rust commands must be registered in `invoke_handler(tauri::generate_handler![...])` and the state type must match the `tauri::State` generic exactly.

## WASM Plugin System

Host loader pattern with `wasmtime`:
- `Plugin` trait defines hooks (`on_birth`, `on_death`, `on_breed_request`, `tick`, `ui_hook`)
- `PluginHost` aggregates plugins and iterates hooks
- WASM guest plugins implement the same trait; host loads `.wasm` blobs
- Keep serialization in a separate `serialization.rs` module using BSON or MessagePack

## Docker Validation

Run `docker compose config` to validate syntax without booting containers. To actually start the stack:

```bash
cd deploy
docker compose up -d --build
docker compose ps
curl http://localhost:7777/health
```

If Docker Desktop is not running, `docker compose up` fails with:
`failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`

Start Docker Desktop and rerun the commands above. Do not treat this as a Dockerfile or compose syntax failure.

## Workspace Verification Checklist

Before marking a scaffold complete:
- [ ] Root `Cargo.toml` has explicit `edition = "2021"` and `resolver = "2"`
- [ ] Every member crate explicitly declares `edition = "2021"` or inherits it reliably via `workspace.package`
- [ ] All workspace member paths are valid relative paths
- [ ] `cargo check --workspace` completes through the linker (or documents the exact environmental blocker with a fix path)
- [ ] `cargo test --workspace --tests` passes on the supported toolchain
- [ ] `cargo clippy --workspace -D warnings` passes in CI
- [ ] Dead crates are removed from `default-members` and marked deprecated in code/docs
- [ ] Optional debug/observability is gated behind a release-only feature, not always-on
- [ ] `deny.toml` includes vulnerability/unmaintained/yanked denials and multi-version warnings
- [ ] If async startup is required, the crate has an explicit modern-rust bootstrap rather than relying on default assumptions
- [ ] Frontend `tsconfig.json` includes `"src"` and `npm run build` succeeds
- [ ] All Tauri commands have matching typed exports in `cubeApi.ts`
- [ ] All frontend views import from `cubeApi.ts`, with no direct `invoke()` calls in `views/`
- [ ] Docker compose validates: `docker compose config`

## 100-Year Durability Policy

Treat Rust binaries as long-lived infrastructure, not one-off apps.

- Target Rust 2021 explicitly at the workspace root and every member crate.
- Prefer minimal deps in the fast path; keep observability, telemetry, and debug features optional in release.
- Maintain `CHANGELOG.md`, `docs/RUST_EDITION_POLICY.md`, and `deny.toml` so future maintainers know constraints without reading commit history.
- Avoid deprecated crates in the default build path; keep them available but explicitly gated.
- Design NAT traversal, relay, capture, and input as layered fallbacks so one subsystem failing does not disable the whole product.

## Optical Media I/O (CD/DVD/Blu-ray)

### Raw Disc Access on Windows

Windows blocks direct `CreateFile` on mounted optical volumes. Use PowerShell with `DeviceIoControl` and `IOCTL_CDROM_RAW_READ` for CDDA (audio CD) sector access. The Rust `windows` crate API is harder to work with than PowerShell for this use case.

**CD-DA sector size**: Audio CDs use **2352 bytes per sector**, not 2048. This is critical for raw ripping.

**Disc size detection**: Use `IOCTL_DISK_GET_LENGTH_INFO` via PowerShell for accurate disc size when other methods fail.

### Progress Reporting for Unknown-Size Media

When disc size is unknown (common for raw optical media), progress should show MB processed rather than percentage. The pattern:
```rust
pub fn percent(&self) -> f64 {
    if self.bytes_total == 0 {
        let mb = self.bytes_processed as f64 / 1_000_000.0;
        if mb > 0.0 && mb < 99.0 { mb } else { 99.0 }
    } else {
        (self.bytes_processed as f64 / self.bytes_total as f64) * 100.0
    }
}
```

### Binary Naming Conflicts in Workspaces

Two `[[bin]]` targets in a workspace will overwrite each other if they share the same output name. When adding a GUI binary alongside a CLI binary in the same workspace, rename one (e.g., `diskripper-gui` vs `diskripper`) to avoid the access-denied "failed to remove file" error during builds.

### Mounted Drive Extraction Fallback

When extracting files from an optical drive, the disc may use a filesystem that isn't ISO 9660 or UDF (e.g., HFS on classic Mac OS game CDs). The robust approach:

1. Detect if the source path is a drive letter (e.g., `D:\`)
2. If it is, scan the mounted filesystem directly via `std::fs::read_dir`
3. If it's a file path, parse as ISO/UDF image

```rust
fn is_drive_path(path: &str) -> bool {
    let path = path.trim_end_matches('\\');
    (path.len() == 2 && path.ends_with(':')) || path.len() == 1
}
```

**Real-world example**: Freddi Fish 4 game CD uses HFS (magic `BD` at 0x8001), not ISO 9660. The mounted-drive fallback successfully extracted all 154 files (475MB).

### UDF Parsing for DVD/Blu-ray

Full UDF parser needed for data DVDs/Blu-rays. The parser must handle:
- Anchor Volume Descriptor Pointer (AVDP) at standard locations (LBA 256, 512, end-1)
- Volume Descriptor Sequence (VDS) with tag identifiers
- Partition Descriptor (tag 5) for partition start/length
- Logical Volume Descriptor (tag 6) with partition maps
- File Set Descriptor (tag 256) for root directory ICB
- File Identifier Descriptor (tag 257) for directory entries
- File Entry Descriptor (tag 261) for file data location

**UDF magic**: Check for `NSR02` or `NSR03` at offset 0x8001 (sector 64 + 0x100).

### Performance Warning

PowerShell per-read batching is **extremely slow** for large discs. Reading 50 sectors at a time via PowerShell subprocess means ~100k process spawns for a 25GB Blu-ray. For production use, compile a Rust helper using the `windows` crate with direct `DeviceIoControl` calls.

## Drive Control & Disc Quality

### Drive Control (Eject/Load/Speed)

SCSI commands via `IOCTL_SCSI_PASS_THROUGH_DIRECT`:

```rust
// START STOP UNIT (0x1B) - eject, load, start, stop
let mut cdb = [0u8; 6];
cdb[0] = 0x1B;
cdb[4] = command; // 0x02=eject, 0x03=load, 0x01=start, 0x00=stop

// SET STREAMING (0xB6) - set read speed
let mut cdb = [0u8; 12];
cdb[0] = 0xB6;
let speed_kbs = speed_x * 150; // CD: 150 KB/s per x
cdb[10] = ((speed_kbs >> 8) & 0xFF) as u8;
cdb[11] = (speed_kbs & 0xFF) as u8;
```

### Disc Quality Scanning

```rust
pub struct DiscQuality {
    pub c1_errors: u64,
    pub c2_errors: u64,
    pub bler: f64,        // Block Error Rate
    pub avg_jitter: f64,
    pub quality_score: u32, // 0-100
}
```

Read sectors with subchannel data, count C1/C2 errors from error flags, measure jitter from read timing.

### Paranoid/Secure Ripping

Multiple reads per sector with majority vote:

```rust
pub struct ParanoidConfig {
    pub read_count: u32,      // Typically 3
    pub majority_vote: bool,  // Use majority byte at each position
    pub max_mismatches: u32,
}

// For each sector: read N times, take majority byte at each position
fn majority_vote(reads: &[Vec<u8>]) -> Vec<u8> {
    // Count byte occurrences at each position, take most common
}
```

## FLAC Compression

External flac encoder with WAV fallback:

```rust
pub enum FlacCompression { Fast = 0, Default = 5, Best = 8 }

pub fn compress(wav: &Path, flac: &Path, level: FlacCompression) -> Result<()> {
    Command::new("flac")
        .arg(format!("--compression-level-{}", level as u8))
        .arg("--force").arg("--quiet")
        .arg("-o").arg(flac).arg(wav)
        .output()?;
}
```

## CD-Text Parsing

CD-Text packs are 18 bytes in R-W subchannels:

```rust
// Pack types
const CDTEXT_PACK_TITLE: u8 = 0x80;
const CDTEXT_PACK_PERFORMER: u8 = 0x81;
const CDTEXT_PACK_SONGWRITER: u8 = 0x82;
const CDTEXT_PACK_COMPOSER: u8 = 0x83;
const CDTEXT_PACK_DISC_ID: u8 = 0x86;
const CDTEXT_PACK_GENRE: u8 = 0x87;
const CDTEXT_PACK_UPC_EAN: u8 = 0x8E;

// Pack structure: type(1) + track(1) + seq(1) + char_pos(1) + data(12) + crc(2)
```

## Multisession & Mixed-Mode CDs

```rust
pub struct MultisessionReader;

impl MultisessionReader {
    pub fn is_mixed_mode(toc: &CdToc) -> bool {
        // Both audio AND data tracks present
    }
}

pub struct EnhancedCdReader;
impl EnhancedCdReader {
    pub fn is_enhanced_cd(toc: &CdToc) -> bool {
        // Session 1 = audio, Session 2 = data (Blue Book)
    }
}
```

## Professional Icon Generation

```rust
// PNG signature + IHDR + IDAT (zlib-compressed) + IEND
// Windows ICO: header + directory + PNG images
// macOS ICNS: header + icon type chunks
pub fn generate_png_icon(path: &Path, size: u32) -> Result<()> { ... }
pub fn generate_ico(output_dir: &Path) -> Result<()> { ... }
pub fn generate_icns(output_dir: &Path) -> Result<()> { ... }
```

Required sizes: 16, 32, 48, 128, 256, 512 (1024 for macOS retina).

## AccurateRip Verification

CRC32-based checksums with AccurateRip-specific offsets:

```rust
pub fn calculate_checksum(
    track_data: &[u8],
    track_number: u32,
    total_tracks: u32,
    drive_offset: i32,
) -> u32 {
    // Skip first second for track 1, last seconds for final track
    // Apply drive offset correction
    // CRC32 of remaining data
}

pub fn calculate_disc_id(track_offsets: &[u64]) -> String {
    // SHA-1 of track offsets, base64-encoded with special char replacement
}
```

## Parallel Processing & Hardware Acceleration

### Multi-threading with Rayon

For CPU-bound work (file extraction, checksum computation, data parsing), use `rayon` with a thread pool sized to CPU cores:

```rust
let thread_pool = rayon::ThreadPoolBuilder::new()
    .num_threads(num_cpus::get())
    .thread_name(|idx| format!("diskripper-worker-{}", idx))
    .build()?;

// Parallel file extraction
files.into_par_iter().for_each(|entry| {
    std::fs::copy(&entry.full_path, &dest)?;
});

// Parallel checksums
let checksums: Vec<String> = chunks.into_par_iter()
    .map(|chunk| {
        use sha2::{Digest, Sha256};
        let mut hasher = Sha256::new();
        hasher.update(chunk);
        format!("{:x}", hasher.finalize())
    })
    .collect();
```

**Important**: Wrap blocking rayon operations in `tokio::task::spawn_blocking` when called from async context.

### Cross-Platform Memory Detection

Use `windows-sys` for Windows (the `windows` crate's API is harder to work with for FFI):

```rust
// Windows
use windows_sys::Win32::System::SystemInformation::*;
let mut mem_info: MEMORYSTATUSEX = std::mem::zeroed();
mem_info.dwLength = std::mem::size_of::<MEMORYSTATUSEX>() as u32;
GlobalMemoryStatusEx(&mut mem_info);

// Linux
std::fs::read_to_string("/proc/meminfo")
    // parse MemTotal and MemAvailable

// macOS  
libc::sysctlbyname("hw.memsize\0" as *const i8, ...);
```

### GPU Detection

Lightweight detection via command-line tools (no OpenCL/CUDA SDK dependency):

```rust
// NVIDIA via nvidia-smi
Command::new("nvidia-smi")
    .args(["--query-gpu=name,memory.total", "--format=csv,noheader"])
    .output();

// macOS via system_profiler
Command::new("system_profiler")
    .args(["-xml", "SPDisplaysDataType"])
    .output();
```

### Native Win32 FFI with windows-sys

For direct Windows API calls, prefer `windows-sys` over the `windows` crate. The `windows` crate's `PCWSTR` wrapper and `GENERIC_READ.0` syntax causes compile errors with certain feature combinations:

```rust
use windows_sys::Win32::Storage::FileSystem as FS;
use windows_sys::Win32::Foundation as Found;
use windows_sys::Win32::System::IO;

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

// IOCTL codes for optical drives
const IOCTL_CDROM_RAW_READ: u32 = 0x0002403E;
const IOCTL_CDROM_GET_TOC: u32 = 0x0004D00E;
const IOCTL_DISK_GET_LENGTH_INFO: u32 = 0x0007405C;
const IOCTL_SCSI_PASS_THROUGH_DIRECT: u32 = 0x0004D004;
```

### Linux SG_IO Support

For raw SCSI pass-through on Linux:

```rust
// SG_IO ioctl for SCSI commands
const SG_IO: u32 = 0x2285;
const SCSIOP_READ_CD: u8 = 0xBE;
const SCSIOP_READ_TOC: u8 = 0x43;
const SCSIOP_READ_CAPACITY: u8 = 0x25;

#[repr(C)]
struct SgIoHdr {
    interface_id: i32,
    dxfer_direction: i32,
    cmd_len: u8,
    mx_sb_len: u8,
    iovec_count: u16,
    dxfer_len: u32,
    dxferp: *mut u8,
    cmdp: *mut u8,
    sbp: *mut u8,
    timeout: u32,
    // ... remaining fields
}
```

### macOS IOKit

For macOS optical drive access, use IOKit to enumerate `IODTPlatformDevice` and open `IOCDMedia`/`IODVDMedia`/`IOBDMedia` interfaces. Fallback to standard POSIX I/O for compatibility.

### DVD IFO Parsing

Full parser for DVD-Video IFO files (VMG/VTS structures):

```rust
pub struct DvdParser;

impl DvdParser {
    pub fn parse_ifo(&self, ifo_path: &Path) -> Result<Vec<DvdTitle>, DiskRipperError> {
        // Parse VMG (Video Manager) for title table
        // Parse VTS (Video Title Set) for title management table
        // Extract audio/subtitle stream attributes from VTS_MAT
        // Parse PGC (Program Chain) for chapter/cell info
    }
}
```

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

### CD-Text Parsing

CD-Text is stored in packs of 18 bytes in R-W subchannels:

```rust
// Pack types
const CDTEXT_PACK_TITLE: u8 = 0x80;
const CDTEXT_PACK_PERFORMER: u8 = 0x81;
const CDTEXT_PACK_SONGWRITER: u8 = 0x82;
const CDTEXT_PACK_COMPOSER: u8 = 0x83;
const CDTEXT_PACK_ARRANGER: u8 = 0x84;
const CDTEXT_PACK_MESSAGE: u8 = 0x85;
const CDTEXT_PACK_DISC_ID: u8 = 0x86;
const CDTEXT_PACK_GENRE: u8 = 0x87;
const CDTEXT_PACK_UPC_EAN: u8 = 0x8E;

// Each pack: type(1) + track(1) + sequential(1) + char_pos(1) + data(12) + crc(2)
```

### Multisession CD Support

```rust
pub struct MultisessionReader;

impl MultisessionReader {
    pub fn read_toc(drive_path: &str) -> Result<CdToc, DiskRipperError> {
        // SCSI READ TOC command (0x43)
        // Parse sessions and tracks
    }
    
    pub fn is_mixed_mode(toc: &CdToc) -> bool {
        // True if both audio and data tracks present
    }
}

pub struct EnhancedCdReader;

impl EnhancedCdReader {
    pub fn is_enhanced_cd(toc: &CdToc) -> bool {
        // Session 1 = audio, Session 2 = data (Blue Book)
    }
}
```

### FLAC Compression

External flac encoder integration with WAV fallback:

```rust
pub struct FlacEncoder;

impl FlacEncoder {
    pub fn is_available() -> bool {
        Command::new("flac").arg("--version").output().is_ok()
    }
    
    pub fn compress(wav_path: &Path, flac_path: &Path, compression: FlacCompression) -> Result<(), DiskRipperError> {
        // flac --compression-level-N --force --quiet -o output.flac input.wav
    }
}
```

### AccurateRip Verification

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

## Pitfalls

1. **Tauri workspace inclusion (UPDATED)**: Tauri 2 CAN be a workspace member. The old advice to exclude it was incorrect — what actually matters is having a proper `build.rs` with `tauri_build::build()` and matching `tauri.conf.json` to the installed `tauri-build` schema. See `tauri2-build-patterns.md` in `desktop-app-development` for the complete pattern.

2. **Tauri CLI availability on Windows**: `cargo tauri` may not exist even when Tauri builds succeed. Install `@tauri-apps/cli` globally via npm (`npm install -g @tauri-apps/cli@latest`) and use `tauri build` directly. Verify with `tauri --version`.

3. **Frontend TypeScript blocking native build**: `tauri build` runs `beforeBuildCommand` by default. If `npm run build` fails TypeScript type-checking, the native binary is not produced even though `cargo check` passes. Common blockers: missing `src/index.css`, strict TS settings with unused imports, and `Uint8Array` vs `number[]` mismatches in IPC types. Fix frontend build first.

4. **Async in Tauri setup**: `tauri::async_runtime::block_on` is required inside `setup()`, not `tokio::main`. The latter conflicts with Tauri's runtime.

5. **State sharing**: `tauri::State<'_, Arc<RwLock<T>>>` requires `T: Send + Sync + 'static`. Avoid holding read locks across `.await` points; use scoped reads or clone data before async boundaries.

6. **MessagePack vs JSON**: Use `rmp-serde` for binary `.cube` save files. Do NOT use `serde_json` for save data—it is larger and slower to parse.

7. **Git Bash link.exe**: On Windows with Git Bash installed, `link.exe` in PATH may be the MSYS2 shim, causing "extra operand" errors. See Windows Linker Troubleshooting section.

8. **HashMap nondeterminism**: `std::collections::HashMap` iteration order is not guaranteed across processes. For deterministic genome serialization/hashing, use `indexmap::IndexMap` with the `serde` feature enabled in `Cargo.toml`. Without this, two identical genomes can produce different hashes on different runs, breaking breeding reproducibility tests.

9. **ed25519-dalek 2.x API**: `SigningKey::generate` was removed. Construct via `SigningKey::from_bytes(&seed.into())` after filling a `[u8; 32]` with `rand::thread_rng().fill(&mut seed)`. Remember to import the `Signer` trait to use `.sign(payload)`.

10. **rand 0.8 distribution imports**: The `Normal` distribution lives in the `rand_distr` crate, not `rand::distributions`. Add `rand-distr = "0.4"` and import `rand_distr::{Distribution, Normal}`.

11. **LocusId deserialization**: When using `IndexMap<LocusId, Chromosome>` with serde, implement `From<&str>` and `From<String>` for `LocusId`; otherwise deserialization fails with "trait bound `LocusId: From<&str>` is not satisfied".

12. **Tauri 2 config field names**: In newer Tauri 2 CLI versions, `devPath` is rejected; use `devUrl` instead. `distDir` is rejected; use `frontendDist`. The `package` section is not a top-level key; move `productName` and `version` under the `tauri` key.

13. **Workspace dependencies**: When member crates use `.workspace = true` for dependencies, the root `Cargo.toml` must define `[workspace.dependencies]` with path mappings. Omitting this causes "error inheriting from workspace root manifest's `workspace.dependencies`" at parse time.

14. **Axum 0.7 handler signatures**: Route handlers in Axum 0.7 must satisfy the `Handler` trait exactly. Mismatched parameter counts or state extractor patterns produce opaque macro errors from `top_level_handler_fn!`. Ensure handler function signatures match the expected `(State<S>, ...) -> ...` shape.

15. **Tauri frontend build type mismatches**: When passing binary data from Rust to TypeScript through Tauri IPC, convert `Uint8Array` to `number[]` with `Array.from(...)` or adjust the TypeScript type to accept `Uint8Array`. Otherwise `tsc` will reject assignments like `Uint8Array | undefined` to `number[] | undefined`.

16. **Tauri CSS module declaration**: When `tsconfig.json` has `"noUnusedSideEffectImports": true` or strict module resolution, importing CSS from `main.tsx` may fail with `TS2307: Cannot find module './index.css'`. Add a `src/vite-env.d.ts` with `declare module '*.css'` to satisfy the type checker.

17. **Module hygiene in `lib.rs`**: Prefer explicit module declarations (`mod foo;`) over duplicate `pub mod` declarations in the same file. If a module file is rewritten, re-verify imports in dependent files—`use std::sync::{Arc, Mutex}` must be present wherever `Mutex` is used, or `cargo check` will fail with `cannot find type Mutex in this scope`.

18. **Windows drive detection for Tauri apps**: `wmic` and `Win32_CDROMDrive` are unreliable for optical drives. Use PowerShell `Win32_LogicalDisk` filtered by `DriveType = 5`. Mount-path fallbacks from Linux/macOS (`/media`, `/Volumes`) will not work on Windows and will silently fail; always branch on platform.

19. **Desktop GUI verification**: After `npm run tauri dev`, verify launch with window enumeration and accessibility capture. For view-switch validation, re-capture after each navigation and confirm the semantic tree reflects the new view. For actionable empty states, verify that action buttons exist in the empty-state tree before treating the view as complete.

20. **Streaming I/O for large media**: Never read entire disc images or large media files into memory. Use async streaming with progress emission. The pattern is: open reader/writer with `tokio::fs::File`, loop with a fixed buffer (8MB is good), emit progress events after each chunk. This prevents OOM on Blu-ray discs (25-100GB) and keeps the UI responsive.

21. **Event-driven progress**: Never poll the backend for job progress. Emit events from the backend with `app_handle.emit_all("job:update", &payload)` and listen on the frontend with `listen<Payload>("job:update", callback)`. Polling creates unnecessary load and introduces latency in UI updates.

22. **CLI binary workspace integration**: When adding a CLI binary to a workspace member, it needs `use diskripper_core::...` imports (not `crate::` which only works for the library crate). The binary's `path` in `[[bin]]` must be relative to the crate root. Remove the CLI module from `lib.rs` to avoid duplicate module errors.

23. **windows crate vs windows-sys for FFI**: The `windows` crate's `PCWSTR` wrapper, `GENERIC_READ.0` syntax, and result types cause compile errors for raw FFI work. Use `windows-sys` for direct Win32 API calls (CreateFileW, DeviceIoControl, etc.) and the `windows` crate only for higher-level abstractions (COM, WinRT). Key difference: `windows-sys` uses raw pointers and `isize` handles; `windows` crate uses wrapper types that don't always interop with `windows-sys` IOCTL codes.

## Reference

See `references/windows-rust-scaffold-fixes.md` for session-specific error transcripts and reproduction recipes from the CubeWorld genetics workspace build.

See `references/parallel-processing-and-gpu.md` for multi-threading patterns, hardware detection, and Windows FFI notes from the DiskRipper optical media backup suite.
