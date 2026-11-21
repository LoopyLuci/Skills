# Substrate-resident adapter seam

The pattern this user applies when one of their projects becomes a substrate for another: a duck-typed `OrganismSubstrateAdapter` that a Substrate (`framework.substrate.Substrate`) registers as a resident, routes over, and verifies with a Tier-1 reusable verifier.

## The seam (implementation)

1. **Adapter** — a duck-typed subclass of `nn.Module` implementing the substrate's Surface (`declare_contract`, `handle`, `health`, `justify`, `on_drain`). The adaptor is optional in the import tree (lazy import), so the *host* imports fine with no counterparty. Its `forward()` returns a vector view whose shape matches the frame's `EXPERT_OUT_DIM`; `resident_embedding(problem)` returns the deterministic `(EXPERT_OUT_DIM,)` routing vector the Substrate's fine router can gate.
2. **Registration** — `substrate.register_organism_resident(adapter)` resolves the adapter's group to a registered `ExpertGroup` if unset, records it, and returns it so the call can chain.
3. **Routing** — `substrate.route_resident(adapter, problem, seed=0, top_k=2)` embeds the resident via `resident_embedding`, runs coarse-group + OT-Route fine router + adaptive depth + vortex-audit, and returns a `RoutingTrace` whose `artifact_id` is the resident's `module_id` (attribution, not just the task).
4. **Verification** — `Verifier.resident_routing(trace, module_id, max_entropy, max_depth, min_depth)` returns the verifier contract `{'verdict','confidence','message','audited'}` and is a Tier-1 executable gate.
5. **Permutation** — `Substrate.__init__` keeps `self.organism_residents = nn.ModuleList()`; residents ride in the same ModuleList registry as the Qwen3 experts, and `organism_resident_names()` lists them.

## Two-phase test bar for a substrate seam

Every substrate seam passes two test phases, in this order:

1. **Per-module duck-typed unit tests** — a synthetic `StubOrganismModule` exercising `declare_contract`/`handle`/`health`/`justify`/`on_drain`. Run in the same pytest process as the other tests (which import `organism`). Assert `organism_sdk` stays out of `sys.modules`.
2. **Cross-cutting full suite + e2e** — the primary repo's full `pytest` from its root (with real fixtures). Two irreversible assertions any later test must pass:
   - real-module path (when the counterparty SDK is importable): a real module rides the adapter (`test_real_deterministic_engine_through_adapter`); if it is skipped, the skip condition must be a clean `skipif` on `_organism_available()`.
   - a **real-Substrate e2e recipe smoke** (`UpcycleTrainer` over a module-scoped real substrate) asserting finite masks, finite dot weights, and sane entropy.

## Rebuild rule after a compaction press

A compaction-era write can collapse `\n` escapes into real newlines, leak a dangling comment, or drop a closing paren, making a test file fail collection or parse as missing-brace. Before trusting a suite whose test file was touched by the compaction: read it in full and `ast.parse` it; reconcile the test file before trusting its green results.

## Look-alike failures (classify, do not guess)

- `AssertionError: b, TypeError: 'float' object is not callable` → a field renamed (e.g. `target_sparsity`) changed the type the call site reads. Renaming the target attribute and re-running isolates the property from the call site.
- `AssertionError: im, ...` / `AssertionError: ol ...` → these are usually **truncated assertion output**, not failures of the assertion logic; the truncated tail is the real signal. Look at the full failure (not the `tail`), run the failing test in isolation, and compare the expected vs actual side of the assertion.

## Serving residency back-pressure (serving plane)

`framework.serving.ExpertCacheManager` holds resident shards warm under a memory cap; oversubscription is back-pressed, not allowed to flood memory.

1. **Mark resident** — `ExpertCacheManager.mark_resident(module_id, expert_group, sub_domain)` warms the shard, records the module (a per-entry `module_id` tracks ownership), and calls `ensure_resident_budget()`.
2. **Enforce** — `ensure_resident_budget()` demotes the resident shards with the oldest `last_access` (tie-break `hit_count`) until `resident_ratio = max(1, int(len(entries) * residency_budget)) / len(entries)`; at least one resident shard survives.
3. **Inspect** — `resident_ratio` (fraction resident), `resident_modules` (live resident module ids), `is_resident(module_id)`.
4. **Result** — resident shards stay warm and are still reported by the observability layers. The budget is `CACHE["residency_budget"]` (0.4 by default).

Test bar: `test_mark_resident_enforces_resident_budget` (5 shards → cap 2, ratio 0.4); `test_resident_ratio_counts_resident_shards` (3 shards, 1 resident, ratio 1/3).

## Frozen profile mutation

`SubstrateProfile` is a `@dataclass(frozen=True)` — immutable. Mutate specialization state only through the export/import round-trip (`to_dict`/`from_dict`, or the v1.1.0 share `_export_share`/`_import_share`); never by assigning a field. The on-disk profile is JSON; re-import on the other side to restore a mutated copy.

## Tier-1 resident routing verifier contract

`Verifier.resident_routing(self, trace, module_id=None, max_entropy=4.0, max_depth=8, min_depth=1)` returns `{'verdict','confidence','message','audited'}`. `audited` is a DICT (`artifact_id`, `group_assignments`, `fine_entropy`, `recurrence_depth`) — never an int; assert `len(audited) >= 2`. The `trace` must expose `artifact_id`/`group_assignments`/`fine_entropy`/`recurrence_depth`; a `SubstrateProfile` is not a trace. `expected_group` is not a keyword.

## Pitfalls

- `AssertionError: b`, `TypeError: 'float' object is not callable` → a field renamed (e.g. `target_sparsity`) changed the type the call site reads. Rename the target attribute and re-run to isolate the property from the call site.
