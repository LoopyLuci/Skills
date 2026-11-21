# Serving-resident eviction

The resident cache keeps a bounded fraction of expert shards resident across turns of a research thread. The policy is a lazy LRU demotion, not an evictor that scans on every mark.

## Invariants

1. `resident_modules` is a dry set of `module_id` (a module is resident iff one of its entries is wired to `CacheEntry.module_id`).
2. `resident_ratio = (# resident shards) / (# entries)`, in [0, 1].
3. `resident_ratio <= residency_budget` after `ensure_resident_budget()` returns, except when the cache has <= 1 entry (nothing to evict).

## ensure_resident_budget() pseudo-code

    if len(entries) <= 1:
        return
    target = max(1, int(len(entries) * residency_budget))
    residents = sorted(
        (e for e in entries.values() if e.resident),
        key=lambda e: (e.last_access, e.hit_count),
    )
    while len(residents) > target:
        victim = residents.pop(0)
        victim.resident = False
        if victim.module_id:
            resident_modules.discard(victim.module_id)

## Why LRU, not "free the biggest" or "free the oldest group"

The resident set is accessed in scan order (the routing trace walks it), so the most recently used shard is the least likely to be re-touched soon. LRU maximizes the probability that a re-visited resident is still resident. `hit_count` is the tie-break for shards with equal last-access; it guards against a warm that was read once then dropped.

## Budget knob

`residency_budget` defaults to 0.4 (full residency = 1.0). Lowering it shrinks peak GPU resident memory at the cost of more re-warms per decode; raising it does the opposite.