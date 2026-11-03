---
name: telemetry-accuracy-audit
description: Audit telemetry accuracy and GUI feature coverage.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
      - software-development
      - verification
      - telemetry
      - desktop-gui
    related_skills:
      - software-development/verification-first-development
      - software-development/systematic-debugging
      - software-development/declared-vs-consumed-audit
---

## When to Use

Use when any of these hold:
- A data/telemetry pipeline (sensor → event bus → API → UI) may have accuracy or completeness gaps.
- The user asks to "make sure data and telemetry are working and accurate" or "the GUI shows all data and exposes all features/settings."
- A dashboard, telemetry, or sensor-collection feature looks done but has not been traced against real execution.

## Core Principle

Trace the real data path end-to-end — sensor provider → event bus → API serialization → delivery → UI rendering — and verify every hop against real execution (headless driver, TestClient, or live process). A green import, a passing unit test, or a hard-coded stub proves nothing about a data path's accuracy or a UI's coverage.

## Procedure (in order)

1. **Enumerate the declared surface.** Every sensor ID/type, fan field, curve field, settings key. Grep the provider, the model, the API routes, and the UI for what exists.
2. **Trace the delivery path.** How each value reaches a UI consumer: event types, websocket message types, HTTP endpoints, serialization shapes, event-bus fields. Follow one value from sensor.read() to the UI line that renders it.
3. **Verify accuracy with real execution.** Run the headless driver (or TestClient / uvicorn bootstrap) that exercises the actual provider + UI wiring. Assert both values and shapes, not just that a call succeeded.
4. **Find accuracy and availability bugs.** Indexing a dataclass instance as a list; a runtime-only config change that never reaches a running worker; simulated values being silently reused on real hardware; a UI control that writes a value no consumer reads.
5. **Fix the defect.** Correct the code, then re-run verification (pytest + headless driver + evidence dump). Do not stop at "it compiles."
6. **Expand UI coverage.** Add the missing declared fields/sensors to the UI (stats labels, charts, tables, editor bounds). Re-verify.
7. **Close with evidence.** Rerun the full test suite, the headless driver, and write down what was verified. Report the artifact paths.

## Pitfalls

- **A dataclass result is not subscriptable.** Never index a model instance (`result[0]`) as if it were a list. Test the actual return shape before assuming.
- **Runtime-only config does not reach running workers.** A settings spinbox that updates `CONFIG` but a worker that was constructed with a hardcoded interval still ticks at the old rate. Read the live config inside the worker loop.
- **Closures over loop variables capture by reference.** Each handler may see the last value of the loop variable, not its own iteration.
- **Simulated values mask real sensor drift.** Mock providers always return values; on real hardware the same sensor may return None or a different ID. Validate against actual hardware, then confirm the fallback path is exercised.
- **A UI toggle is both writer and reader.** An audit that searches only for read sites outside the UI will flag a UI-backed setting as "not in UI" even though the UI reads it to render its own state. Check whether the setting is read by the UI layer itself.

## Always-on Rules (Standing Preferences)

1. **Full implementation, never stubs.** "Proceed with all in order" means every phase with working artifacts — run them, don't describe them.
2. **Zero tolerance for errors.** Every claim about a feature is backed by a fresh verification artifact (passing tests, a real driver run, a log/output file). An unverified claim is open until proven.
3. **Verification-first.** Run the real code path and record what it returned, before claiming anything works.
4. **Accessibility is default** — ARIA labels, keyboard nav, screen reader roles — not an afterthought.
5. **Ground answers in real state** — fresh test outputs and file artifacts, not speculation.
6. **Cross-app profile exchange must normalize IDs** (`nous`→`nous_research`, `opencode-zen`→`open_code_zen`, `opencode-go`→`open_code_go`, `xai`→`grok`) on import; do not skip normalization.
7. **Desktop GUI is pywebview/Tauri or native desktop.** Never pass a browser dashboard; the shell is a real window with native IPC, not a web page.
8. **Provider backends fetch concurrently (tokio::spawn), with a circuit breaker (5 fails → 60 s) and a 50-entry LRU cache (5-min TTL)** — consistent across cross-app profile exchange.
9. **Concise direct prose** — match the length of the reply to the weight of the ask; no filler, no narrating tool calls.

## References

- [Data-path tracing recipe](references/data-path-tracing.md) — end-to-end telemetry trace and common drift points.
- [GUI feature / settings coverage checklist](references/gui-coverage-audit-checklist.md) — declared-surface coverage gate with the live/read-only/inert classification.
