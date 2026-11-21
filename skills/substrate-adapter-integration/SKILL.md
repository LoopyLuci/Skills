---
name: substrate-adapter-integration
description: Integrate external projects as substrate residents.
---
# Substrate adapter integration

Integrate an external project as a first-class resident of a substrate (e.g. Organism into RS-MoA/E): a duck-typed adapter that rides the substrate's routing topology, a residency manager that tracks and caps resident shards, a Tier-1 routing verifier that re-attests the trace, a live HTTP gateway, and the v1.1.0 cross-app profile exchange. The deliverable is always a *green, verified suite* — never a stub, never an asserted-but-unrun path.

## When to Use

Use this skill when the user asks to:

- integrate an external project as a substrate resident of an agentic meta-agent;
- expose a resident expert cache (or an Organism adapter) over a live HTTP gateway;
- build a v1.1.0 cross-app profile exchange (KotMoE + Agentic Workbench);
- verify a resident routing trace with the Tier-1 gate (`Verifier.resident_routing`);
- run a full-suite, verification-first delivery with no stubs.

This skill covers the procedure and standing preferences for the whole class of
"add a resident, verify it, and serve it". The detailed protocol lives in:

- `references/v1-1-0-profile-exchange.md` — the v1.1.0 share format, provider-
  normalization table, and the import/restore path.
- `references/resident-routing-topology.md` — the resident routing topology
  (coarse group router + OT-Route fine router + GaP-MoE) and the verify gate contract.

## Procedure (in this order)

1. Read the codebase first. Locate the serving plane (`framework/serving.py`), the residency manager (`ExpertCacheManager`), the verify layer (`framework/verify.py`), the profile module (`framework/integrations/organism.py`), and the test tree (`tests/`). Trace the symbol you intend to change before editing.
2. Build the adapter (duck-typed bridge). Define `resident_embedding(problem)` returning a deterministic `(EXPERT_OUT_DIM,)` vector, and `route_resident(adapter, problem)` that routes the organism resident through the coarse group router + OT-Route fine router + GaP-MoE. It must accept an Organism module and expose a named resident, with no Organism-SDK dependency for the routing path.
3. Track residency. `mark_resident(module_id, expert_group, sub_domain)` warms the shard, records the module id on the entry, and adds the module to `resident_modules`. `resident_ratio` = fraction of cache entries that are resident.
4. Verify residency. `Verifier.resident_routing(trace, module_id, max_entropy=4.0, max_depth=8, min_depth=1)` returns `{'verdict':'pass'|'fail'|'PASS_WITH_TELEGRAM', 'confidence':0.9|0.4, 'message':..., 'audited':{'artifact_id','group_assignments','fine_entropy','recurrence_depth'}}`. Tier-1 executable gate per SPEC 4.1.
5. Live gateway. A FastAPI shim over the serving plane (`:8011`): `/health`, `/v1/mark_resident`, `/v1/is_resident/{module_id}`, `/v1/resident_ratio`, `/v1/client_share`, `/v1/client_import`. Run with `uvicorn framework.gateway:app`.
6. Verify the whole suite. `pytest tests/ -q`. Claim done only after green, no warnings. Re-run after every edit.

## User preferences (always-on)

- **Full implementation, no stubs.** Proceed with all, never propose stopping early. The deliverable is a working, verified artifact, not a description.
- **Verification-first.** Re-run the suite after every edit; claim done only when green, no warnings, no root-cause-fixing beyond the cause found.
- **Direct answers first.** Lead with the result; short prose, no filler, no narrating tool calls the user can see, no restating the request back.

## Diagnostic Rule

- **A failing full suite is not automatically a code regression.** Resource pressure (system paging file, memory pressure) produces `OSError`, `MemoryError`, and transient hangs that look exactly like code failures. When the suite reports failures, run each failing test in isolation (`pytest tests/<file>::<test> -v`) and in a quiet window before touching code. If it passes alone, the defect is the environment, not the change.

- **Batch your runs. On a resource-constrained box a full `pytest tests/` invocation collapses the whole suite under OS paging pressure and reports phantom failures (e.g. `OSError: The paging file is too small`, errno 1455) even when every test passes in isolation. Detect by running `pytest tests/ -q` — if it crashes hard before completing, split it:**

  ```bash
  # run per test file (each file is a bounded chunk)
  for f in tests/test_xxx.py; do pytest "$f" -q --tb=short; done
  # or run in two listed groups
  pytest tests/group_a.py tests/group_b.py -q
  ```

  If every file passes alone but `pytest tests/` still dies at the top level, the machine is out of virtual memory — check the paging file (`systeminfo | findstr /i "paging file"`), raise it, or run the batch on a machine with more RAM. Do not chase the phantom failure by editing code.

- **Standing verifications after every edit.** Re-run the full suite with `pytest tests/ -q` after every edit. Claim done only when green, no warnings, no root-cause-fixing beyond the cause found. For wire claims (gateway, EXE, profile share), exercise the live API with real clients or `curl` — never assert "it worked" from a stub or an un-run path.

- **Organism real-module tests stay gated on the SDK.** `test_real_deterministic_engine_through_adapter` is skipped when `organism_sdk` is not importable. When Organism IS installed, those tests are real — no stubs, no shortcuts.

## Pitfalls

- Grep the call sites before widening a helper signature — a hand-rolled duplicate re-implements the old shape and fails on a shard you did not run.
- The resident-ratio cap (`CACHE["residency_budget"], =0.4`) is enforced by evicting the **least-recently-used resident shards**. A cache with a single entry keeps its only resident (never back-presses to zero); the target is `int(len * 0.4)`.
- Reuse the existing import paths (`framework.integrations.organism`, `framework.serving`). Don't re-derive the old shape.
- For wire claims, exercise the API with real clients (`TestClient`) or `curl` — never assert "it worked" from a stub or an un-run path.
- The v1.1.0 share is the product: `profile_format_version: "1.1.0"`, `source_app`, `target_app`, `organism_profile`, `provider{provided_id, normalized_id}`. Importing a share must normalize the provider id (bidirectional mapping) before constructing the restored `SubstrateProfile`.

## Organism-specific integration patterns

When the external project is Organism (homeostatic computational ecology substrate):

- **Lazy SDK import.** The adapter uses a module-level `_organism_available()` guard that tries `import organism_sdk` and returns bool. The adapter is duck-typed — it only requires the wrapped object to expose `declare_contract`, `handle`, `health`, `justify`, `on_drain`. This lets the adapter import and the test suite run whether or not Organism is installed.

- **Deterministic resident embedding.** `resident_embedding(problem)` returns a stable `(EXPERT_OUT_DIM,)` float32 tensor derived from `sha256("{module_id}|{problem}")` — same module + problem → same vector. This makes routing traces attributable and lets the fine router gate the resident alongside Qwen3 experts.

- **Cross-app profile exchange (v1.1.0).** The adapter carries `_export_share` / `_import_share` that produce/consume `{"profile_format_version": "1.1.0", "source_app", "target_app", "organism_profile", "provider": {"provided_id", "normalized_id"}}`. Provider IDs are normalized bidirectionally: `nous↔nous_research`, `opencode-zen↔open_code_zen`, `opencode-go↔open_code_go`, `xai↔grok`. Import must normalize before constructing the restored `SubstrateProfile`.

- **Real Organism module test path.** When Organism SDK is available, the test suite installs it (`cd X:/Projects/Organism && pip install -e ".[dev]"`) and exercises the real `DeterministicEngine` through the adapter. The test `test_real_deterministic_engine_through_adapter` verifies: group resolution, emission routing, substrate profile round-trip, health reporting.

## References

- `references/v1-1-0-profile-exchange.md` — the v1.1.0 share format, provider-normalization table, and the import/restore path.
- `references/resident-routing-topology.md` — the resident routing topology (coarse group router + OT-Route fine router + GaP-MoE) and the verify gate contract.
