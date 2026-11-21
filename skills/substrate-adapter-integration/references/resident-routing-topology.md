# Resident routing topology

A resident module rides the substrate's routing topology instead of the plain
`embed`. The adapter exposes a vector view shaped to match the substrate's
`embed` output so the substrate can route over the resident without touching
the organims SDK.

## Topology

1. **Coarse group router** — selects the expert group (e.g. `systems_and_infra`).
2. **OT-Route fine router** — addresses the exact expert inside the group.
3. **GaP-MoE** (gating by parameter) — the final expert activation for the problem.

`resident_embedding(problem)` returns a deterministic routing vector of shape
`(EXPERT_OUT_DIM,)`. `route_resident(adapter, problem)` composes the coarse
group assignment + OT-Route fine routing + GaP-MoE to produce the resident's
routing trace (artifact id, group assignments, fine entropy, recurrence depth).

## Verification gate contract

`Verifier.resident_routing(trace, module_id, max_entropy=4.0, max_depth=8,
min_depth=1)` — the Tier-1 executable audit of a resident routing trace.

The verdict passes when, and only when, all of: the trace's `artifact_id`
matches the resident module_id, at least one group assignment is present,
`fine_entropy` is finite and within `[0, max_entropy]`, and
`recurrence_depth` is within `[min_depth, max_depth]`.

Returns `{'verdict': 'pass'|'fail'|'PASS_WITH_TELEGRAM', 'confidence': 0.9|0.4,
'message': '...', 'audited': {'artifact_id','group_assignments','fine_entropy',
'recurrence_depth'}}`.
