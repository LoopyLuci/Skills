# v1.1.0 organizer profile exchange

Cross-app sharing of an organizer's specialization between the agentic-workbench
(FastAPI) runtime and the KotMoE (Rust) runtime. The substrate exporter
instrument the organizer's specialization (a `SubstrateProfile`) into a
transportable JSON chunk; the importer restores the live object.

## Provider ID mapping (normalize on import)

| kotmoe (provided) | agentic-workbench (normalized) |
|---|---|
| nous | nous_research |
| opencode-zen | open_code_zen |
| opencode-go | open_code_go |
| xai | grok |

## Share format

```json
{
  "profile_format_version": "1.1.0",
  "source_app": "kotmoe",
  "target_app": "agentic-workbench",
  "organism_profile": {
    "module_id": "deterministic_engine",
    "group": "systems_and_infra",
    "expert_id": 3,
    "expert_entropy": 2.37,
    "routing_report": {"artifact_id": "d2847a", "fine_entropy": 1.84},
    "health_score": 0.93
  },
  "provider": {
    "provided_id": "opencode-zen",
    "normalized_id": "open_code_zen"
  }
}
```

## Functions on SubstrateProfile

- `to_share(source_app, provider_id=None)` — export the organizer profile as a
  transportable v1.1.0 chunk.
- `from_share(d)` — restore a `SubstrateProfile` from a v1.1.0 chunk; normalizes
  the provider id on import. If a share arrives without `organism_profile`,
  fall back to treating the whole dict as the profile.

## Testing the exchange end-to-end

1. Build a `SubstrateProfile` (module_id, group, expert_id, expert_entropy,
   routing_report, health_score).
2. Export with `to_share(source_app="kotmoe", provider_id="opencode-zen")`;
   assert `profile_format_version == "1.1.0"`.
3. Import with `from_share(share)`; assert module_id, group, expert_id,
   expert_entropy, health_score round-trip exactly.
4. Drive the exchange over the live HTTP gateway with `fastapi.testclient.TestClient`
   (`client_share` → `client_import`); assert the round-trip survives the wire,
   and re-attest it with `Verifier.resident_routing`.
