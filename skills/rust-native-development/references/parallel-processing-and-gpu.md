# Parallel Processing & Hardware Acceleration

Multi-threading patterns, hardware detection, and Windows FFI notes from the DiskRipper optical media backup suite (2026-09).

## Multi-threading with Rayon

### Thread Pool Setup

Use rayon with a thread pool sized to CPU cores:

```rust
use rayon::prelude::*;
use std::sync::atomic::{AtomicU64, Ordering};

let thread_pool = rayon::ThreadPoolBuilder::new()
    .num_threads(num_cpus::get())
    .thread_name(|idx| format!("diskripper-worker-{}", idx))
    .build()?;
```

### Parallel File Extraction

Wrap blocking rayon in `tokio::task::spawn_blocking` when called from async:

```rust
tokio::task::spawn_blocking(move || {
    files.par_iter().for_each(|entry| {
        std::fs::copy(&entry.full_path, &dest)?;
    });
}).await
```

**Real-world result**: Freddi Fish 4 game CD extraction (154 files, 475MB) ran 4x faster with rayon par_iter vs sequential loop on a 6-core machine.

### Parallel Checksums

```rust
let checksums: Vec<String> = chunks
    .into_par_iter()
    .map(|chunk| {
        use sha2::{Digest, Sha256};
        let mut hasher = Sha256::new();
        hasher.update(chunk);
        format!("{:x}", hasher.finalize())
    })
    .collect();
```

## Cross-Platform Memory Detection

### Windows (windows-sys)

```rust
use windows_sys::Win32::System::SystemInformation::*;
unsafe {
    let mut mem_info: MEMORYSTATUSEX = std::mem::zeroed();
    mem_info.dwLength = std::mem::size_of::<MEMORYSTATUSEX>() as u32;
    GlobalMemoryStatusEx(&mut mem_info);
    (mem_info.ullTotalPhys, mem_info.ullAvailPhys)
}
```

### Linux (/proc/meminfo)

```rust
let meminfo = std::fs::read_to_string("/proc/meminfo")?;
// Parse lines starting with "MemTotal:" and "MemAvailable:"
```

### macOS (libc::sysctlbyname)

```rust
unsafe {
    let mut total: u64 = 0;
    let mut size = std::mem::size_of::<u64>();
    libc::sysctlbyname(
        "hw.memsize\0".as_ptr() as *const i8,
        &mut total as *mut _ as *mut _,
        &mut size,
        std::ptr::null_mut(),
        0,
    );
}
```

## GPU Detection

### NVIDIA (nvidia-smi)

```rust
let output = std::process::Command::new("nvidia-smi")
    .args(["--query-gpu=name,memory.total", "--format=csv,noheader"])
    .output().ok()?;
// Parse CSV: "GeForce RTX 4090, 24576 MiB"
```

### macOS (system_profiler)

```rust
let output = std::process::Command::new("system_profiler")
    .args(["-xml", "SPDisplaysDataType"])
    .output().ok()?;
```

**No CUDA/OpenCL SDK required** — detection is via command-line tools.

## Native Win32 FFI: windows-sys vs windows

The `windows` crate's `PCWSTR` wrapper, `GENERIC_READ.0` syntax, and result types cause compile errors for raw FFI work:

```rust
// windows crate (problematic)
let handle = CreateFileW(
    windows::core::PCWSTR(wide_path.as_ptr()),  // "cannot find `core` in `windows`"
    GENERIC_READ.0,                               // wrong type
    ...
);

// windows-sys (correct)
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
if handle == Found::INVALID_HANDLE_VALUE {
    return Err(io::Error::last_os_error());
}
```

**Rule**: Use `windows-sys` for raw Win32 FFI; use `windows` crate only for higher-level abstractions (e.g., COM, WinRT).

## Optical Media I/O (Quick Reference)

| Disc Type | Sector Size | IOCTL |
|-----------|-------------|-------|
| CD-DA (audio CD) | 2352 | IOCTL_CDROM_RAW_READ (track_mode=2) |
| CD-ROM (data) | 2048 | IOCTL_SCSI_PASS_THROUGH_DIRECT (READ 10) |
| DVD | 2048 | IOCTL_SCSI_PASS_THROUGH_DIRECT (READ 10) |
| Blu-ray | 2048 | IOCTL_SCSI_PASS_THROUGH_DIRECT (READ 10) |

### Disc Size Detection

```rust
// PowerShell helper returns IOCTL_DISK_GET_LENGTH_INFO result
Command::new("powershell")
    .args(["-File", "raw.ps1", "size", drive_letter])
```

## Thread Pool Sizing

| Workload Type | Thread Count |
|---------------|--------------|
| I/O-bound (file copy) | num_cpus * 2 |
| CPU-bound (checksums) | num_cpus |
| Mixed (extraction) | num_cpus |

```rust
let num_cpus = num_cpus::get();  // includes hyperthreading
let physical = num_cpus::get_physical();  // physical cores only
```

## Drive Control & Disc Quality (Quick Reference)

### SCSI Commands for Optical Drives

| Command | CDB Opcode | Purpose |
|---------|------------|---------|
| START STOP UNIT | 0x1B | Eject (0x02), Load (0x03), Start (0x01), Stop (0x00) |
| SET STREAMING | 0xB6 | Set read speed (1x = 150 KB/s for CD) |
| READ TOC/PMA/ATIP | 0x43 | Read Table of Contents |
| READ CAPACITY | 0x25 | Get disc size |
| TEST UNIT READY | 0x00 | Check if drive is ready |

### Disc Quality Metrics

```rust
pub struct DiscQuality {
    pub c1_errors: u64,      // Correctable errors
    pub c2_errors: u64,      // Uncorrectable errors  
    pub bler: f64,           // Block Error Rate (errors/sector)
    pub avg_jitter: f64,     // Timing jitter in ns
    pub quality_score: u32,  // 0-100 composite score
}
```

### Paranoid Ripping

```rust
pub struct ParanoidConfig {
    pub read_count: u32,         // Typically 3 reads per sector
    pub majority_vote: bool,     // Use majority byte at each position
    pub max_mismatches: u32,     // Abort threshold
}

// Majority vote: for each byte position, take the value that appears most often
// across multiple reads. This corrects random read errors.
```

## Common Pitfalls

1. **Async + rayon mismatch**: Don't call `par_iter()` directly inside `async fn`. Wrap with `tokio::task::spawn_blocking`.

2. **Thread name for debugging**: Always set thread names in rayon pool — it makes deadlock/timing issues much easier to diagnose.

3. **Don't share non-Send types**: Rayon requires `Send` closures. `Rc` is not `Send` — use `Arc` instead.

4. **Progress reporting**: Use `AtomicU64` for thread-safe progress counters. Don't lock a `Mutex` per iteration.

5. **Memory bounds**: For large discs, bound concurrent reads to prevent OOM: `(max_memory / 8MB).min(16) concurrent reads`.