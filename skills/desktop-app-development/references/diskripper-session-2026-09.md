# DiskRipper Session Notes (September 2026)

Session-proven patterns from building DiskRipper — a Tauri 2 + Rust optical media backup app with MCP server integration.

## What Was Built

```
DiskRipper/
├── Cargo.toml                    # workspace root
├── diskripper-core/              # Rust backend library + CLI binary
│   ├── src/
│   │   ├── lib.rs                # module exports
│   │   ├── main.rs               # CLI binary entry point
│   │   ├── rip.rs                # RipEngine (job management)
│   │   ├── image.rs              # streaming disc imaging
│   │   ├── filesystem/           # ISO 9660, UDF parsers
│   │   ├── metadata.rs           # AccurateRip, Disc ID
│   │   └── audio/                # CD-DA ripping
│   └── Cargo.toml
├── diskripper-tauri/             # Tauri 2 desktop app
│   ├── src/lib.rs                # Tauri commands
│   └── tauri.conf.json
├── frontend/                     # React/TypeScript UI
│   ├── src/
│   │   ├── App.tsx
│   │   ├── store.ts              # Zustand store + event listeners
│   │   └── components/
│   └── package.json
├── packages/mcp-server/          # TypeScript MCP server
│   ├── src/
│   │   ├── index.ts              # MCP tools (9 tools)
│   │   └── cli.ts                # stdio entry point
│   └── package.json
└── .github/workflows/ci.yml      # GitHub Actions CI/CD
```

## Game CD Extraction Test (September 2, 2026)

Tested extraction with a Freddi Fish 4 game CD (HFS format, 475MB).

### Results
- **154 files extracted successfully**
- **475,892,627 bytes total (100% match with original disc)**
- All file sizes verified correct
- Progress tracking worked correctly (44% → 70% → 91% → 99.8%)

### Bug Fix: Mounted Drive Extraction
The original extraction code tried to read `D:\` as a file path. Fixed by detecting drive paths and scanning the mounted filesystem directly:
```rust
/// Check if path looks like an optical drive
fn is_drive_path(path: &str) -> bool {
    let path = path.trim_end_matches('\\');
    (path.len() == 2 && path.ends_with(':')) || path.len() == 1
}
```

When `is_drive_path` returns true, the extractor uses `std::fs::read_dir` to recursively scan the mounted filesystem instead of trying to parse it as an ISO/UDF image.

### HFS Detection
The game CD showed magic bytes `BD` at offset 0x8001 — this is HFS (Hierarchical File System), not ISO 9660. Future improvement: add HFS parser to the filesystem detection pipeline.

## Key Technical Decisions

### 1. Streaming I/O (Not Full-File Reads)
Reading entire disc images into memory fails for dual-layer Blu-rays (50GB+). Solution: 8MB async buffer with progress events.

```rust
pub async fn run(&self) -> Result<(), DiskRipperError> {
    let mut reader = tokio::fs::File::open(&self.source_path).await?;
    let mut writer = tokio::fs::File::create(&self.output_path).await?;
    let mut buffer = vec![0u8; 8 * 1024 * 1024]; // 8MB buffer
    loop {
        let n = reader.read(&mut buffer).await?;
        if n == 0 { break; }
        writer.write_all(&buffer[..n]).await?;
        tracker.add_bytes(n as u64);
    }
    writer.flush().await?;
    Ok(())
}
```

### 2. Event-Driven Progress (Not Polling)
Frontend subscribes to backend events instead of polling every 5 seconds:

```rust
// Backend emits events
app_handle.emit_all("job:update", &progress).ok();

// Frontend listens
listen('job:update', (event) => {
  updateJob(event.payload);
});
```

### 3. MCP Server Wraps CLI Binary
The MCP server is TypeScript that spawns the Rust CLI binary. This pattern enables AI agents (including Hermes) to use DiskRipper without FFI or IPC complexity.

```typescript
const DISKRIPPER_BIN = process.env.DISKRIPPER_BIN || 'diskripper';

async function callCLI(...args: string[]): Promise<string> {
  return new Promise((resolve, reject) => {
    const child = spawn(DISKRIPPER_BIN, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    // ... collect stdout/stderr, resolve/reject on exit
  });
}
```

### 4. CLI Binary in Workspace
The CLI binary lives in `diskripper-core/src/main.rs` (not a separate crate). It imports from `diskripper_core::` (not `crate::`). The `cli` module was removed from `lib.rs` to avoid duplicate module errors.

### 5. Tauri Config Minimalism
Started with minimal `tauri.conf.json` and added features only when needed:
- `tray-icon` feature flag required in Cargo.toml for tray support
- Updater pubkey must be generated with `cargo tauri signer generate`
- `beforeBuildCommand` must include full `cd` + build pipeline

## 9 MCP Tools Exposed

| Tool | Description |
|------|-------------|
| `list_drives` | Discover optical drives |
| `drive_info` | Inspect drive/disc details |
| `rip_disc` | Create ISO/BIN/IMG images |
| `extract_files` | Extract files to directory |
| `rip_audio_cd` | Rip audio to WAV/FLAC |
| `verify_image` | Verify image integrity |
| `list_jobs` | List all backup jobs |
| `job_status` | Check specific job |
| `cancel_job` | Cancel running backup |

## Hermes Agent Integration

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

Environment variable for binary path:
```bash
DISKRIPPER_BIN="C:/Projects/DiskRipper/target/debug/diskripper.exe"
```

## Verification Results

```bash
cargo test --workspace --tests    # 38/38 passing
cargo check --workspace           # 0 errors, 0 warnings
npm run build                     # Frontend bundles (189KB JS + 14KB CSS)
MCP initialize test               # protocolVersion 2024-11-05
MCP tools/list                    # 9 tools returned
MCP list_drives call              # D:\, E:\ detected
```

## Windows-Specific Gotchas Encountered

1. **MSYS path conversion**: `/c/Paths` → `\c\Paths` breaks Node.js `spawn()`. Always use `C:/Projects/...`.
2. **Binary must exist before MCP test**: Run `cargo build -p diskripper-core --bin diskripper` before testing MCP.
3. **CLI uses `diskripper_core::` imports**: Binary crate can't use `crate::` (that's for the library crate).
4. **Remove `cli` mod from `lib.rs`**: Binary in `main.rs` conflicts with `mod cli` in `lib.rs`.
5. **Windows binary extension**: Use `.exe` in env var path: `diskripper.exe`.

## GUI Verification via computer_use

The Tauri GUI was tested using the `computer_use` tool with background-first delivery. This is the proven workflow:

### Launch
```bash
# Start Tauri dev server (background)
cargo tauri dev &
# Wait for window to appear (8-10 seconds)
```

### Capture & Navigate
```python
# Capture with accessibility tree
computer_use(action='capture', app='diskripper.exe', mode='ax')
# Returns elements with bounds — use coordinate clicks since element indices require snapshot_id

# Click navigation items by coordinate (from bounds)
computer_use(action='click', app='diskripper.exe', coordinate=[134, 197])  # Drives
computer_use(action='click', app='diskripper.exe', coordinate=[134, 239])  # Jobs
computer_use(action='click', app='diskripper.exe', coordinate=[134, 281])  # Audio CD
computer_use(action='click', app='diskripper.exe', coordinate=[134, 323])  # Verify
computer_use(action='click', app='diskripper.exe', coordinate=[134, 365])  # Settings

# Re-capture after each click to verify view switched
computer_use(action='capture', app='diskripper.exe', mode='som')
```

### Verified Working (September 2026)
| View | Status | Elements Found |
|------|--------|----------------|
| Drives | ✅ | 2 drive cards (D:\ Audio CD, E:\), Refresh button, Rip Configuration panel |
| Jobs | ✅ | Filter dropdown (All), Refresh, "No jobs found" empty state |
| Audio CD | ✅ | "Select a drive with an audio CD to extract tracks" empty state |
| Verify | ✅ | SHA-256 sector verification description, drive selection prompt |
| Settings | ✅ | Output directory, Read Speed, Retries, Buffer Size, 4 checkboxes, Log Level, Save/Reset buttons |

### Drive Card Interaction
Clicking a drive card (coordinate [518, 220]) expands the Rip Configuration panel with:
- Create Image / Extract Files toggle buttons
- Output Path text field with browse button
- Create Image action button

### computer_use Gotchas on Windows
1. **Element indices require snapshot_id**: `click(element=7)` fails with `snapshot_id_required`. Use `coordinate=[x, y]` from bounds instead.
2. **Background delivery works**: `effect: "unverifiable"` is normal — re-capture to verify state change.
3. **AX tree mode is more reliable**: `mode='ax'` returns all elements with bounds; `mode='som'` may return fewer.
4. **Coordinate scaling**: Element bounds are in native desktop coordinates, NOT screenshot pixels. Scale factor ~1.07-1.27x from screenshot to native.

---

## ML Content Identification System (September 2026)

Built a comprehensive ML system for identifying and organizing ripped content. User explicitly demanded custom ML models over external API dependencies.

### Architecture

```
diskripper-core/src/ml/
├── pipeline.rs              # Main orchestrator (MlPipeline)
├── audio_fingerprint.rs     # Custom audio fingerprinting (AcoustID replacement)
├── music_identification.rs  # Hybrid music identification
├── video_fingerprint.rs     # Video perceptual hashing
├── content_classifier.rs    # Genre/type classification
├── hybrid_identifier.rs     # Multi-signal identification with confidence
├── feature_extraction.rs    # MFCCs, chroma, spectral features, ZCR, RMS
├── inference.rs             # MLP/CNN neural network engine
├── training.rs              # Backpropagation training loop
├── self_learning.rs         # User feedback collection & retraining
├── data_management.rs       # Training data collection & augmentation
├── model_versioning.rs      # Model versioning, rollback, A/B testing
└── organizer.rs             # Smart content organization (Music/Movies/TV/Software/Games)
```

### Custom Audio Fingerprinting (AcoustID Replacement)

User demanded custom implementations over external APIs. The fingerprinting system:
1. Computes spectrogram via FFT
2. Finds spectral peaks (local maxima)
3. Creates combinatorial hash from peak pairs
4. Matches via Jaccard similarity + duration comparison

```rust
pub fn generate(&self, audio_data: &[i16], sample_rate: u32) -> Result<AudioFingerprint, DiskRipperError> {
    let spectrogram = self.compute_spectrogram(audio_data, sample_rate);
    let peaks = self.find_spectral_peaks(&spectrogram);
    let hash = self.hash_peaks(&peaks);
    Ok(AudioFingerprint { peaks, hash, duration, sample_rate })
}
```

### Neural Network Inference Engine

Built from scratch (no ML framework dependency):
- Multi-layer perceptron (MLP) with configurable layers
- Convolutional layers for audio spectrograms
- Forward pass with ReLU, Sigmoid, Softmax activations
- Xavier weight initialization
- Model serialization/deserialization (JSON)

### Training Pipeline

```rust
pub fn train(&self, model: &mut NeuralNetwork, dataset: &Dataset) -> Result<TrainingHistory, DiskRipperError> {
    // Mini-batch gradient descent
    // Backpropagation with cross-entropy loss
    // Early stopping with patience
    // Model checkpointing (best model saved)
}
```

### Self-Learning from User Feedback

```rust
pub struct FeedbackEntry {
    id: u64,
    original_prediction: String,
    corrected_title: String,
    corrected_artist: Option<String>,
    corrected_album: Option<String>,
    corrected_genre: Option<String>,
    timestamp: DateTime<Utc>,
    used_for_training: bool,
}
```

Feedback is collected locally, batched (min 10 samples), and used to retrain models.

### Smart Organization

```rust
pub fn organize(&self, file_path: &Path, identification: &PipelineResult) -> Result<OrganizationResult, DiskRipperError> {
    let path = match identification.content_type {
        Music => output_dir/Artist/Album/Track.ext
        Movie => output_dir/Title (Year)/Title.ext
        TvShow => output_dir/Title/Title.ext
        Software => output_dir/Title/Title.ext
        Game => output_dir/Title/Title.ext
    }
}
```

### Hybrid Identification Strategy

User likes hybrid approaches. The pipeline combines:
1. Audio fingerprinting (local, no deps)
2. Content classification (neural network)
3. Metadata lookup (when available)
4. Confidence scoring across all signals

### Key Dependencies Added

```toml
rand = "0.8"          # Weight initialization, data augmentation
fastrand = "2.0"      # Efficient shuffling for training
crc32fast = "1.4"     # Checksums for fingerprints
sha1 = "0.10"         # MusicBrainz disc ID
sha2 = "0.10"          # Verification
rayon = "1.10"        # Parallel processing
```

### CLI Automation

```bash
# JSON output for scripting
diskripper --json list-drives

# Batch rip multiple drives
diskripper batch-rip --drives D:,E: --output-dir C:\output

# Auto-identify after rip
diskripper rip --drive D: --output disc.iso --auto-identify
```

### Dark/Light Theme

```css
/* Light theme overrides */
.light-theme .bg-\[\#0f172a\] { background-color: #ffffff !important; }
.light-theme .text-white { color: #0f172a !important; }
```

Theme persisted in `localStorage` with `diskripper-theme` key.

### Crash Reporting

```rust
pub struct CrashReport {
    id: String,
    timestamp: DateTime<Utc>,
    error_message: String,
    component: String,
    os_name: String,
    architecture: String,
    num_cpus: usize,
    app_version: String,
}
```

Reports saved to `%APPDATA%/DiskRipper/crashes/` with error statistics tracking.

### Performance Benchmarks

```rust
pub fn run_benchmarks() -> Vec<BenchmarkResult> {
    // Audio fingerprinting throughput
    // Feature extraction throughput
    // CRC32 checksum throughput
    // Parallel extraction with rayon
}
```

### User Preference: Custom > External

**Critical lesson**: User explicitly rejected integrating existing services (AcoustID, MusicBrainz, TMDB) and demanded custom ML implementations with self-learning pipelines. The program must be fully independent of external dependencies.

When building ML systems for this user:
1. Build models from scratch (no API dependencies)
2. Implement hybrid approaches (multiple techniques combined)
3. Include self-learning from user feedback
4. Make everything locally runnable
5. Never suggest "just use X API" — suggest custom implementations

### Build Verification

```bash
cargo check -p diskripper-core    # 0 errors, 38 warnings
cargo test -p diskripper-core     # 38/38 passing
cargo bench --workspace           # Performance benchmarks
npm run build                     # Frontend bundles (197KB JS + 17KB CSS)
```

## Frontend Build Fixes (September 2026)

When wiring the GUI to the ML system and CLI automation, TypeScript build errors emerged. Root causes and fixes:

### 1. Store Interface Must Precede Component Usage
Components read directly from `useAppStore()`. If the store doesn't declare a field, components fail with `TS2339: Property 'X' does not exist on type 'AppState'`.

**Fix**: The store (`store.ts`) must be the single source of truth for ALL shared state — jobs, drives, settings, toasts, audio tracks, output path, selected drive, verification results.

### 2. Optional Parameters Need Explicit Handling
```typescript
// WRONG: Passing explicit undefined to optional param
await startImageRip(selectedDrive, outputPath)  // outputPath may be undefined

// CORRECT: Optional param with fallback
startImageRip: async (driveId: string, outputPath?: string) => {
    const out = outputPath || get().outputPath || `C:\\DiskRipper\\${driveId}.iso`
```

### 3. TrackInfo Needs All Displayed Fields
Components displayed `duration_seconds` but the interface only had `track_number`, `start_lba`, `length_lba`, `channels`.

**Fix**: Add `duration_seconds: number` to `TrackInfo`.

### 4. Frontend Build Verification
```bash
npm run build    # tsc && vite build
# Success: 1593 modules transformed, 197KB JS, 17KB CSS
```

### Final Store Interface Shape
```typescript
interface AppState {
    drives: DriveInfo[]
    jobs: Job[]
    systemInfo: SystemInfo | null
    settings: AppSettings
    toasts: Toast[]
    loading: boolean
    error: string | null
    outputPath: string
    audioTracks: TrackInfo[]
    selectedDrive: string | null
    // ... all actions
}
```

---

## Project Complete (September 2026)

All phases (P0-P3) complete. 50+ modules. Frontend builds. Backend compiles. Tests pass.

**Next steps for real distribution:**
1. Windows code signing certificate
2. `npm run tauri build` for MSI/NSIS/DMG packages
3. Test with 20+ real discs
4. Ship v1.0