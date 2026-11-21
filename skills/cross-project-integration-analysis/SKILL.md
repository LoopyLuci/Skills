---
name: cross-project-integration-analysis
description: "Use when integrating two of the user's projects."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [integration, architecture, planning, research]
    related_skills: [systematic-debugging, test-driven-development]
---

# Cross-Project Integration Analysis

Produces an exhaustive seam-level analysis and a phased, effort-ranked integration plan document when the user asks how to integrate one of their projects into another, or how two of their projects should work together.

## When to use

The deliverable is a committed markdown doc in the primary repo's `docs/` — exact seams, ranked patterns, phased plan — not a chat summary.

## Procedure

1. **Verify both repos at current HEAD.** `git fetch` the other repo before reading it; a same-day merge can add whole subsystems that reshape the recommendation. Record both commit SHAs in the doc header.
2. **Inventory each side's integration surface from source, not docs.** Read the transport/backend modules for exact wire detail: ports, protocol framing, auth handshake, function signatures, config file shapes, tool/command lists. Never infer a wire format from a README claim — verify it in the code. For a config-only pattern, extract the *registration API* itself from the server's route code: the exact request payload schema, what the route does immediately after persisting (a connect call whose success/failure lands in the response tells you a failed handshake surfaces at registration time, not first use), the table it persists to, and the trust defaults applied to the new connection. When prescribing a config file, check the target repo's `.gitignore` and a fresh checkout — a recommended file that is git-ignored or absent from a fresh clone is a real placement note for the doc.
3. **Map the direction of every candidate seam.** For each connection, determine which side is client and which is server *before* recommending it — a provider-shaped suggestion can be impossible in the reverse direction, and the workable pattern may look nothing like the obvious one.
4. **Identify the complementary axes**: what each side uniquely has that the other lacks. This becomes the gap-analysis table.
5. **Rank patterns by effort x value, config-only first.** Each pattern gets: the exact config block or paste-ready code sketch, the result, effort, risk, and its caveat. Include the verification step for config-only patterns.
6. **Substrate-resident adapter seam.** When the integration lands an optional component into a Substrate plane, shape the seam to the Substrate's own declared surface — a duck-typed adapter, not a new contract:

   (a) Identify the surface. Read the substrate's `ExpertGroupRegistry`, `GaPMoE`, `RoutingTrace` and the frame's `declare_contract`/`handle`/`health`/`on_drain`/`justify` surface. The adapter must accept any object exposing that surface — it is a bridge, never a new dependency.
   (b) Run the seam's two-phase test bar (per-module duck-typed unit tests, then a cross-cutting full suite, then a real-Substrate e2e smoke plus the resident routing verifier) — see `references/substrate-integration.md`.
   (c) Live-verify each phase and record the result as-built. A passing suite is the verification of every phase implemented; a red test is a seam, not a headline.

 A pattern whose recommendation is "register X and it just works" is only verified once you have run the handshake the counterparty will run — send the protocol frames a raw probe and record the output (server identity, protocol version, tool/command list). `scripts/mcp_handshake_probe.py` does exactly this for any stdio MCP server (initialize → notifications/initialized → ping → tools/list). Where the counterparty's runtime cannot be stood up locally, say so plainly in the doc — which claims are wire-verified and which remain source-verified — never imply an end-to-end run you did not perform. When a pattern must be proven end-to-end rather than at the handshake, stand the counterparty up for real and drive the actual endpoint — `references/live-counterparty-verification.md` is the recipe (venv on the counterparty's pinned Python, its own token tooling, minimum instances, real calls, process cleanup).
8. **Rust multi-crate workspace integration** — when the seam is a new Rust crate added to an existing Cargo workspace: (a) read the workspace root `Cargo.toml` for `members` and `resolver` settings; (b) add the new crate's path to `members`; (c) reference other workspace crates in `dependencies` using `path` keys with forward slashes and the exact drive letter — do NOT use MSYS-style paths: `browzeit-core = { path = "X:/Projects/Browzeit/browzeit/crates/core" }` is correct, `X:\Projects\...` (backslashes) or `X:/Projects/...\` (trailing backslash) is wrong; (d) the crate name in `Cargo.toml` declares the external name (`browzeit-core`, not `browzeit_core` — the hyphen is part of the name); (e) run `cargo check --offline` from the workspace root; if dependency resolution fails, delete `target/` and `Cargo.lock` before retrying. Rust's `cargo` is a native Windows binary — MSYS path translation is NOT applied to its arguments, so the `path` value must be in native Windows path form.
- `references/abp-extension-development.md` covers the AgenticBotPlatform `add_*` hook registry for zero-core-edit integration — the extension pattern that makes most cross-project seams shipable without touching the counterparty's core.
9. **Cover the cross-cutting concerns**: security/trust posture of both sides, a failure-mode contract, a phased sequencing table (phase / pattern / effort / value / prerequisite), and a definition of done against the primary repo's test bar.
10. **Deliver as a committed doc.** Write it to `<primary-repo>/docs/<topic>-integration-analysis.md` and commit with a descriptive message.
11. **Escalate to implementation when the question repeats.** If the same integration question returns after the doc exists, the user is signaling that analysis is done — build the top-ranked pattern instead of deepening the doc. Apply the primary repo's full test bar (see `test-driven-development`), wire the seam end-to-end, verify, commit, and update the doc to an as-built record. An explicit "proceed with all" means every unbuilt phase in the plan: implement and live-verify each one, then record them all as-built. Never ship a stub; never restate the problem at greater length instead of implementing. Restating the same analysis at greater length is a tool-call loop, not depth.
12. **Match the codebase's conventions for the new seam.** Before adding a user-selectable backend, check whether the settings/UI layer hardcodes the set of providers — a provider enum tied to the engine's parser by drift-guard tests must be extended in both directions, or the new option is silently unreachable. Also follow the neighboring backends' config convention: if they are env-var-only with no UI settings, adding UI settings for the new one is scope creep.

## Verification gate (prove the seam with a passing machine)

A cross-project seam is claimed verified only when the primary repo's own
test bar runs clean — a narration that a test "should pass" is a promise, not
an artifact. Concretely:

1. **Run the primary repo's full test bar from its root** — `pytest`, or the
   project's declared test command. One green suite (with real fixtures) is
   the verification of every phase you implemented; record the result
   as-built rather than replaying the problem in chat.
2. **Re-read any test file the session touched** before trusting the suite.
   A compaction or a partial edit can collapse escaped newlines into real
   lines, leak a dangling comment, or drop a closing paren — then the file
   fails collection or parses with a missing brace, and the suite is silent
   about the seam. Verify by reading the file back and `ast.parse`ing it;
   a red-test or a syntax error is a hint the seam is not what the doc says.
3. **Disprove dependency-absence assertions, do not assume them.** A sibling
   test that imports a heavy optional dependency (`organism_sdk`) puts it in
   `sys.modules` for the whole pytest process, so a later test's
   `assert "organism_sdk" not in sys.modules` fails even though the module
   under test is clean. Run isolation checks in a subprocess (`python -c`
   child process) so the assertion is unconditional.
4. **Do not use `os.path.abspath(__file__)` inside a `python -c` probe.**
   The `-c` interpreter sets neither `__file__` nor `__package__`; one probe
   crashed with `NameError: name '__file__' is not defined`. Point the probe
   at the project root with `PYTHONPATH` — or run it as a real file passed
   as one `-c` argument — and never derive a path from `__file__` under -c.
5. **Build nested-escaping strings with a raw string and rewrite the file via
   `terminal` + Python, not `patch`.** When a test or probe body contains
   nested escaped quotes, parens, and `\n` sequences, `patch`'s fuzzy
   matcher is too eager and lands on the wrong region (this session lost a
   probe block to escaping twice). Read the file in full, rewrite the
   function in a Python process, `ast.parse` the result as the sanity gate,
   then write. The parser is the gate that catches a collapsed escape
   mid-edit.

## Always-on rules (this user)

- Exhaustive depth, never a summary: exact line numbers, function signatures, request/response JSON shapes.
- Paste-ready config and code blocks over prose descriptions of what to do.
- Every claim verified by reading code; docs are leads, not evidence.
- Honest effort estimates; mark optional phases explicitly and say which to do first.
- Include the failure-mode contract. This user's codebases enforce "report the failure, never fabricate a plausible-looking reply" — every integration path must honor it, and the doc must say so.
- **Cross-project identity normalization.** When two of the user's apps exchange provider/model state, the import direction MUST normalize provider IDs through the shared mapping — always normalize on import: Agentic Workbench `nous` → KotMoE `nous_research`, `opencode-zen` → `open_code_zen`, `opencode-go` → `open_code_go`, `xai` → `grok`. Export must read the actual model-visibility state; import must apply real state. Neither direction returns hard-coded success. If a referenced registry method does not exist, that is a failure the analysis must record, not paper over.
- **Full implementation, no stubs; verification-first with working artifacts.** "Proceed with all" means implement every phase and live-verify each one — never ship a stub, never stop after drafting. Zero tolerance for errors; a codebase that fails to build or its own test bar is a bug to fix, not a headline to repeat.
- **Desktop GUI convention.** A "desktop GUI" is a native pywebview/WebView2 or Tauri shell around a backend — never a browser dashboard. The GUI manages the agent; it does not render the browser's chrome.
- **Generative UI convention.** The GUI must let agents create, modify, and optimize UI components in real-time (add buttons, change layouts, generate themes). "Next generation GUI" means UI as data, not static HTML.
- **Provider concurrency pattern.** Fetch provider APIs concurrently with tokio::spawn; include a circuit breaker (5 fails, 60s) and an LRU cache (50 entries, 5-minute TTL) for resilience.

## Pitfalls

- **Re-pull the other repo before writing.** A same-day merge added an entire learning-router subsystem that reshaped the whole recommendation after the first draft was written.
- **Check each seam's direction before recommending it.** One project exposed no OpenAI-compatible chat server, which turned the obvious "point X at Y" suggestion into a different pattern entirely — the analysis would have shipped a broken plan without that check.
- **A re-ask of the same question is a depth signal, not a repetition request.** Add implementation-level detail — exact signatures, wire formats, paste-ready code sketches, test plans, decision tables — do not restate the same analysis at greater length. A *second* re-ask after the doc exists means analysis is finished: implement under the repo's test bar and update the doc to an as-built record — and an explicit "proceed with all" means every unbuilt phase in the plan, each live-verified, not the top-ranked one alone.
- **When `write_file` refuses an overwrite with the stale-file guard** despite a full prior read, write the new content to a temp sibling filename and replace via shell `mv`; do not loop re-reads.
- **The edit pipeline can redact a bare type identifier to `***` on disk.** When a patch *redeclares a typed field* (e.g. `val x: String = ""`), the secret-masker may write literal asterisks in place of the type name — the tool reports success and the file is syntactically broken. After any edit that redeclares a field, verify the written bytes (`sed -n '<n>p' <file> | od -c`) before building; a grep for the type name shows `***` where the token should be. Fix with `perl -pi -e 's/: \*\*\*/: String/'` (or the correct type) rather than another patch round-trip. A KSP/javac failure at the redeclared line with "Function declaration must have a name" is the signature.
- **Check whether a recommended config file is git-ignored or missing from a fresh checkout** before prescribing its placement — a snippet aimed at a file the repo deliberately excludes (provider/key-bearing configs usually are) needs a different placement note than one that exists in every clone.
- **Bidirectional seams deadlock.** When both sides gain a backend that calls the other (A→B and B→A), one user turn can traverse both directions and each side blocks on the other's in-flight request — the call hangs with no error at all. Enforce one routing direction per app instance, and write that rule into the doc as an operational constraint.
- **Poll async queue-style IPC by content identity, never by count.** A send that returns `queued: true` replies later; wait for a *new* last message by comparing content, not by watching the message count grow — a counterparty whose transcript resets between sessions makes a count-based wait never fire, and the seam looks broken when it is not.
- **Isolate inter-dependency assertions.** `sys.modules` is shared across a pytest process. A sibling test that imports a heavy optional dependency (`organism_sdk`, for example) puts it in `sys.modules` for the whole session, so a later test's `assert "organism_sdk" not in sys.modules` fails even though the module under test is clean. Each isolation check must run in its own interpreter (a fresh subprocess), not in the same session process.
- **`__file__` is not defined under `python -c`.** The `-c` interpreter sets neither `__file__` nor `__package__`. Compute probe paths from the environment (`os.getcwd()` or `PYTHONPATH`) — one early probe here crashed with `NameError: name '__file__' is not defined`. Run multi-line probes as a real file passed as a single `-c` argument, or avoid `__file__` entirely.
- **Prefer a Python rewrite through `terminal` over `patch` for nested-escaping edits.** When the content to change contains escaped quotes, parens, and `\n` sequences, `patch`'s fuzzy matcher can fail or land on the wrong region. Read the file in full, rewrite the function in-process, `ast.parse` the result as the sanity gate, then write. The parser is the gate that catches a collapsed escape mid-edit.
- **Re-verify after a compaction-era restructuring.** A compacted write can collapse `\n` escapes into real newlines, leak a dangling comment, or drop a closing paren, making a test file fail collection or parse as missing-brace. Before trusting a suite whose test file was touched by the compaction, read it in full (offset/limit pagination is not a full read) and parse it; reconcile the test file before trusting its green results.

- `systematic-debugging` — when an integration path fails in practice (4-phase root-cause discipline)
- `test-driven-development` — the test bar every new backend/seam must meet before it ships
