---
version: 1.0.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [rust-analyzer, ra-ap, library, engine-backend]
    related_skills: [agentic-rpc-framework]
---

## S1 — ra_ap_* engine backend wiring (v0.0.358 / 0.0.360)

### Feasibility (library consumption)

`ra_ap_*` crates on crates.io are linkable as a library ("as-is, no API guarantees"). Key versions at build time:

- `ra_ap_base_db` v0.0.360
- `ra_ap_syntax` v0.0.360
- `ra_ap_parser` v0.0.360
- `ra_ap_ide` v0.0.358 (MSRV 1.98.0; stable)
- `ra_ap_ide_db` v0.0.358 (provides `AnalysisHost`, `RootDatabase`, `FileId`)
- `ra_ap_ide_diagnostics` v0.0.358 (provides `DiagnosticsConfig`, `Diagnostic`, `FileRange`, `Assist`, `DiagnosticCode`, `FullDiagnostics`)
- `ra_ap_paths` v0.0.358 (provides `AbsPathBuf`)
- `triomphe` v0.1.17 (matching ra_ap_ide's dependency — required for `AnalysisHost` interior-mutation)

**Version coordination is mandatory.** `ra_ap_ide` depends on `triomphe` and `ra_ap_ide_db`; version drift breaks link/access. The workspace pins `triomphe` at `0.1.17` to match.

> **Always inspect INSTALLED source, never stale docs.** The ra_ap crates publish as-is. `ra_ap_ide` API surface differs materially from the doc `v0.0.360` assumed — the mapping below was corrected after inspecting `ra_ap_ide/src/lib.rs` and `ra_ap_ide_db/src/lib.rs` at build time.

### Engine-wiring recipe

The real-time engine wraps `ra_ap_ide` behind the framework's `IncrementalEngine` trait so CLI/API/MCP/ACP bindings are unchanged. The wrapper owns an `AnalysisHost` (interior-mutated via `Mutex` → `triomphe::Arc` for host storage) plus a tracked file set; `apply_changes` updates the set and bumps a revision; `query(Diagnose(path))` rebuilds the ra_ap world for that path and maps the ra_ap diagnostics into the wire `rpc_diagnostics::Diagnostic` domain.

Key API surface (as inspected on the installed crates):

```rust
use ra_ap_ide::Analysis;
use ra_ap_ide::AnalysisHost;
use ra_ap_ide_db::{Severity, AssistResolveStrategy};
use ra_ap_ide_diagnostics::{DiagnosticsConfig, Diagnostic, DiagnosticCode, Assist, FileRange, FullDiagnostics};
use ra_ap_paths::AbsPathBuf;
use triomphe::Arc;

pub struct RaApEngine {
    host: Mutex<AnalysisHost>,
    files: Mutex<HashMap<PathBuf, String>>,
    revision: Arc<AtomicU64>,
}

impl IncrementalEngine for RaApEngine {
    fn apply_changes(&self, pack) -> Result<Revision, ApplyError> {
        let mut files = self.files.lock().unwrap();
        files.clear();
        for change in &pack.changes { files.insert(change.path, change.content); }
        self.revision.fetch_add(1, Ordering::Relaxed);
        Ok(self.revision.load(Ordering::Relaxed))
    }

    fn query(&self, q) -> QueryResult {
        if let QueryKind::Diagnose { path } = q.kind {
            let text = self.files()
                .get(&PathBuf::from(path))
                .cloned().unwrap_or_default();
            let proc_macro_cwd = Arc::new(AbsPathBuf::try_from("X:/").unwrap());
            let (analysis, file_id) = Analysis::from_single_file(text, proc_macro_cwd);
            let diags = analysis
                .full_diagnostics(&DiagnosticsConfig::test_sample(), AssistResolveStrategy::None, file_id)
                .map_err(|_cancelled| ())
                .unwrap_or_default();
            QueryResult::Diagnoses { path, revision: self.revision.load(Ordering::Relaxed), version: 0, line_count: 0, byte_len: 0, diagnostics: diags }
        } else { /* ... */ }
    }
    fn cancel(&self) { } // matches trait signature
    fn revision(&self) -> Revision { self.revision.load(Ordering::Relaxed) }
    fn engine_version(&self) -> &str { "ra_ap-0.1.0" }
}
```

`Analysis::from_single_file(text, proc_macro_cwd: Arc<AbsPathBuf>) -> (Analysis, FileId)`.

> **`proc_macro_cwd` must be a drive-anchored absolute path, never `/`.** `AbsPathBuf::try_from("/")` panics with `called Result::unwrap() on an Err value: "/"`. The `TryFrom<Utf8PathBuf>` impl rejects any path where `Path::is_absolute()` is false, and on Windows a bare `/` is the *current-drive root*, not an absolute path (it needs a drive letter: `"X:/"`, `"C:/"`). On Linux `/` is absolute and works; the same code therefore passes on one host and panics on another — always pass a drive-anchored path so it is portable.

`analysis.full_diagnostics(&diag_config, resolve_strategy, file_id) -> FullDiagnostics` where `FullDiagnostics = Cancellable<Vec<Diagnostic>>` (`Cancellable<T> = Result<T, Cancelled>`).

`DiagnosticsConfig::test_sample()` builds a valid `DiagnosticsConfig`.

`AssistResolveStrategy::None` is the unit variant in `ra_ap_ide_db::assists`.

### Diagnostic mapping

`ra_ap_ide_diagnostics::Diagnostic` -> `rpc_diagnostics::Diagnostic`:

- `Diagnostic.code` (`DiagnosticCode`) -> wire `schema_version` (call `DiagnosticCode::as_str()`; it is NOT an Option — do not map a `None`).
- `Diagnostic.severity` (`Severity`) -> `Severity` (variants: `Error`, `Warning`, `WeakWarning`, `Allow` — all in `ra_ap_ide_db`).
- `Diagnostic.range` (`FileRange`) -> `TextSpan { start, end }` (both `u32`).
- `Diagnostic.fixes` (`Option<Vec<Assist>>`) -> `Suggestion { text, description, range, new_text }` (NOT `fixits`).

### Performance: rebuild-per-query (the key limit)

`Analysis::from_single_file` rebuilds the entire `AnalysisHost` analysis world (full parse + HIR + diagnostics) on every `query`. This is **correct** (proves the pipeline, produces genuine diagnostics) but **not fast** — typically far above 100ms.

Use it as:
1. A *prototype* proof that the pipeline works end-to-end.
2. A *fallback* engine for a daemon with no incremental plan yet.

**Real sub-100ms requires** an incremental `AnalysisHost` update (feed diffs via `ChangeWithProcMacros` rather than `from_single_file`) plus a `SyntaxOnly` parse path. That is the F2 performance work, not the S1 proof. Do not claim the ra_ap engine is sub-100ms until you measure a sustained per-query latency below the threshold with an incremental update — measuring only the `from_single_file` variant reports a different number and overstates the engine.

> The F1 gate is GREEN (build, fmt, clippy, test all pass) with the from_single_file fallback; the sub-100ms promise is explicitly marked "correct, not yet fast".
