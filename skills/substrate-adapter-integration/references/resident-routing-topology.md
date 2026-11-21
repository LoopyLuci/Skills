# Resident Routing Topology

An Organism resident is routed through the substrate exactly like a Qwen3 expert
does. `route_resident(adapter, problem)` is the single entry point; it runs through
the same topology that routes expert experts, so the resident's trace stays
attributable and the fine router can gate it alongside Qwen3 experts.

## Topology

1. **Identity.** `adapter.resident_embedding(problem)` returns a deterministic
   `(EXPERT_OUT_DIM,)` float32 tensor. Same module + problem → same vector.
   Implemented as `sha256(f"{module_id}|{problem}")`, so routing traces stay
   attributable and the fine router gates the resident in expert weight space.
2. **Coarse group router.** `coarse_group_router(problem, groups, device, seed)`
   runs a selective Sinkhorn over expert groups. It takes the problem string and
   the group list, and returns a soft top-2 distribution over groups.
3. **OT-Route fine router.** `fine_router_gating(hidden, num_experts, eps=0.05)`
   runs an entropy-regularised optimal transport assignment over experts, then
   Sinkhorn-balances to enforce load balance. Returns a routing distribution over
   `num_experts`.
4. **Adaptive recurrence depth.** `adaptive_compute_depth(fine_entropy,
   recurrence, min_depth=1)`. High fine-router entropy (unfamiliar input)
   requests deeper recurrence; low entropy stays at min depth.
5. **GaP-MoE.** The shared gradient-level orthogonalisation specialist keeps
eXperts from collapsing. Leader's gradient only updates the buffer; followers
are projected off the leader's subspace (not chained).

## Verify gate contract (Tier-1, SPEC 4.1)

`Verifier.resident_routing(trace, module_id, max_entropy=4.0, max_depth=8,
min_depth=1)` returns `{'verdict':'pass'|'fail'|'PASS_WITH_TELEGRAM',
'confidence':0.9|0.4, 'message':..., 'audited':{'artifact_id',
'group_assignments','fine_entropy','recurrence_depth'}}`.

Rules the audited trace must satisfy:
- `artifact_id` matches the module_id of the resident.
- `group_assignments` has exactly 2 keys (the two top groups the resident was
  routed to).
- `fine_entropy` falls in `[0.0, 4.0]` (the max_entropy gate).
- `recurrence_depth` is in `[min_depth, max_depth]`.

Passed traces stay attributable: the substrate's audit trace records the
resident's payload, module id, and problem so a re-import restores exactly what
was traced.
