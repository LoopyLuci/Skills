# Tauri 2 Frontend Maturity Patterns

Session-proven patterns for taking a functionally-complete Tauri 2 + React/TypeScript app to production grade.

## Error Display

**Problem:** Store has `error: string | null` but no component reads it. Users see silent failures.

**Pattern:** Create an `ErrorBanner` component that reads `useAppStore().error` and renders a dismissible banner:

```tsx
// components/ErrorBanner.tsx
import { AlertCircle, X } from 'lucide-react'
import { useAppStore } from '../store'

export function ErrorBanner() {
  const { error, clearError } = useAppStore()
  if (!error) return null
  
  return (
    <div className="bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <AlertCircle size={18} />
        <span className="text-sm">{error}</span>
      </div>
      <button onClick={clearError} className="p-1 hover:bg-red-500/30 rounded">
        <X size={16} />
      </button>
    </div>
  )
}
```

Place directly below the `<Header />` in the main `App.tsx` layout.

## Event-Based Progress Updates

**Problem:** `setInterval(refreshJobs, 5000)` polls every 5 seconds. Feels unresponsive.

**Pattern:** Use Tauri's event system for real-time progress:

```typescript
// store.ts - in initialize()
import { listen } from '@tauri-apps/api/event'

await listen('job:update', (event) => {
  get().refreshJobs()
})
```

The backend `JobManager` already has `broadcast::Sender<ProgressInfo>` per job. Wire `app_handle.emit_all("job:update", &progress)` after each `update_progress()` call in `rip.rs`.

## Input Validation

**Problem:** `startImageRip(driveId, outputPath)` sends whatever string is in the box. Empty paths, invalid characters — all accepted.

**Pattern:** Validate before invoke, throw user-readable errors:

```typescript
startImageRip: async (driveId, outputPath) => {
  set({ loading: true, error: null })
  try {
    if (!outputPath.trim()) {
      throw new Error('Output path is required')
    }
    if (!driveId) {
      throw new Error('No drive selected')
    }
    const jobId = await invoke<string>('start_image_rip', { driveId, outputPath })
    await get().refreshJobs()
    set({ loading: false })
    return jobId
  } catch (e) {
    set({ loading: false, error: String(e) })
    return null
  }
}
```

## Loading States

**Problem:** `loading: boolean` exists in store but buttons don't disable during operations. Users can double-click and spawn duplicate jobs.

**Pattern:** Disable buttons and show spinner when `loading` is true:

```tsx
<button
  onClick={handleRip}
  disabled={loading || !outputPath}
  className="... disabled:bg-slate-600 disabled:cursor-not-allowed"
>
  <Play size={16} />
  {loading ? 'Starting...' : 'Create Image'}
</button>
```

## Settings Persistence

**Problem:** SettingsPanel renders controls but changes are lost on app restart.

**Pattern:** Create a `SettingsManager` in Rust with serde JSON:

```rust
// settings.rs
pub struct SettingsManager {
    settings_path: PathBuf,
    settings: Mutex<Settings>,
}

impl SettingsManager {
    pub fn new(app_dir: PathBuf) -> Result<Self, DiskRipperError> { ... }
    pub fn get(&self) -> Settings { ... }
    pub fn update(&self, new_settings: Settings) -> Result<(), DiskRipperError> { ... }
    pub fn reset_to_defaults(&self) -> Result<(), DiskRipperError> { ... }
}
```

Expose via Tauri commands:
```rust
#[tauri::command]
fn load_settings(state: State<'_, SettingsState>) -> Result<Settings, String> { ... }

#[tauri::command]
fn save_settings(settings: Settings, state: State<'_, SettingsState>) -> Result<(), String> { ... }

#[tauri::command]
fn reset_settings(state: State<'_, SettingsState>) -> Result<Settings, String> { ... }
```

Frontend store:
```typescript
loadSettings: async () => {
  const settings = await invoke<Settings>('load_settings')
  set({ settings })
},
saveSettings: async (settings) => {
  await invoke('save_settings', { settings })
  set({ settings })
},
```

## File Logging

**Problem:** `tracing_subscriber::fmt().init()` writes to stdout only. No persistence for debugging.

**Pattern:** Use `tracing-appender` with daily rolling files:

```rust
// In run() before builder
let log_dir = dirs::data_dir()
    .unwrap_or_else(|| std::env::current_dir().unwrap_or_default())
    .join("DiskRipper")
    .join("logs");

if let Err(e) = std::fs::create_dir_all(&log_dir) {
    eprintln!("Failed to create log directory: {}", e);
}

let file_appender = tracing_appender::rolling::daily(&log_dir, "diskripper.log");
let (non_blocking, _guard) = tracing_appender::non_blocking(file_appender);

tracing_subscriber::fmt()
    .with_env_filter(
        tracing_subscriber::EnvFilter::try_from_default_env()
            .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
    )
    .with_writer(non_blocking)
    .with_ansi(false)
    .init();
```

## Graceful Shutdown

**Problem:** `tokio::spawn` tasks hold `Arc<JobManager>` clones. Closing app mid-rip leaves tasks running.

**Pattern:** Handle `RunEvent::ExitRequested` and signal cancellation tokens:

```rust
// In run()
.setup(|app| {
    let app_handle = app.handle().clone();
    // Store app_handle in state for later use
    app.manage(AppHandle(app_handle));
    Ok(())
})
.on_page_load(|window, _payload| {
    // Setup complete
})
```

The `JobManager` already has `CancellationToken` per job. On exit:
```rust
// In RipEngine or a shutdown handler
for job_id in active_jobs {
    let _ = job_manager.cancel_job(&job_id);
}
```

## Verification UI

**Problem:** Backend has `verify_file_rip`, `verify_disc_image`, `verify_audio_accuracy` but no frontend exposure.

**Pattern:** Create a `VerifyPanel` that:
1. Lists drives and lets user select one
2. Accepts an image file path
3. Calls `verify_image_rip` command
4. Displays per-sector results with pass/fail indicators

```tsx
// components/VerifyPanel.tsx
const handleVerify = async () => {
  if (selectedDrive && imagePath) {
    setVerifying(true)
    const result = await verifyImageRip(selectedDrive, imagePath)
    setResults(result)
    setVerifying(false)
  }
}
```

## Audio CD UI

**Problem:** Backend has `AudioCdReader`, `TrackInfo`, `extract_audio_track` but no frontend panel.

**Pattern:** Create an `AudioCdPanel` that:
1. Loads tracks via `get_audio_tracks` command
2. Displays track list with duration
3. Lets user select a track and output path
4. Calls `extract_audio_track_to_wav` command

```tsx
// components/AudioCdPanel.tsx
const handleLoadTracks = async () => {
  if (selectedDrive) {
    await loadAudioTracks(selectedDrive)
  }
}

const handleExtract = async () => {
  if (selectedDrive && selectedTrack !== null) {
    await extractAudioTrack(selectedDrive, selectedTrack, outputPath)
  }
}
```

## Module Organization

```
frontend/src/
  components/
    Header.tsx
    Sidebar.tsx
    ErrorBanner.tsx
    DrivePanel.tsx
    JobPanel.tsx
    AudioCdPanel.tsx
    VerifyPanel.tsx
    SettingsPanel.tsx
    StatusBar.tsx
  store.ts              # Zustand store with all commands
  App.tsx               # Main layout with ErrorBanner
  main.tsx
  index.css

diskripper-core/src/
  settings.rs           # SettingsManager + Settings struct
  rip.rs                # RipEngine with event emission
  job.rs                # JobManager with CancellationToken
  filesystem/
    verify.rs           # VerificationResult, verify_file_rip, verify_disc_image
  audio/
    mod.rs              # AudioCdReader, extract_audio_track

diskripper-tauri/src/
  lib.rs                # All Tauri commands including settings, verify, audio
```
