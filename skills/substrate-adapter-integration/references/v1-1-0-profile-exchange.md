# v1.1.0 Cross-App Profile Exchange

Cross-app profile exchange (organizer ↔ workbench) is the product of the
`framework.integrations.organism` adapter. It carries a substrate resident's
specialization state across two runtimes so a resident's masks, routing behaviour
and health settle in rather than being re-learned from scratch on every launch.

## Share format

The encoded share is a JSON dict:

```json
{
  "profile_format_version": "1.1.0",
  "source_app": "kotmoe",
  "target_app": "agentic-workbench",
  "organism_profile": {
    "module_id": "deterministic_engine",
    "group": "systems_and_infra",
    "expert_id": 0,
    "expert_entropy": 0.0,
    "routing_report": {},
    "health_score": 1.0
  },
  "provider": {
    "provided_id": "nous",
    "normalized_id": "nous_research"
  }
}
```

The `organism_profile` is the `SubstrateProfile.to_dict()` output. The whole
share is a normal JSON dict; serialise to bytes with `json.dumps(...,
sort_keys=True)` for wire transfer.

## Provider normalisation

Provider IDs map bidirectionally between the two apps. The map lives in
`framework.integrations.organism._PROVIDER_ID_MAP` (and the duplicate
`_build_provider_registry()`):

| provided_id (raw) | normalized_id (local canonical) |
|---|---|
| `nous` | `nous_research` |
| `nous_research` | `nous` |
| `opencode-zen` | `open_code_zen` |
| `open_code_zen` | `opencode-zen` |
| `opencode-go` | `open_code_go` |
| `open_code_go` | `open_code_go` |
| `xai` | `grok` |
| `grok` | `xai` |

`normalize_provider_id()` applies the map on import; unknown IDs pass through
unchanged. All of these belong inside the provider registry, not scattered as
hardcoded strings.

## Import / restore path

`_import_profile(d)` reconstructs a `SubstrateProfile` from a share dict:

```python
profile = SubstrateProfile.from_dict(d.get("organism_profile", d))
```

Rules:
- The importer MUST normalise the provider id before constructing the restored
  `SubstrateProfile`. Fall back to identity for unknown ids (safe).
- Only `organism_profile` and `profile_format_version` are consumed. Anything else
  in the share dict is ignored by the restore path.
- Round-trip must be idempotent: `SubstrateProfile.from_dict(p.to_dict()) == p`.

## Full exchange workflow

1. Export: call `_export_share(profile, source_app="kotmoe", provider_id="nous")`
   to build the share dict (include provider normalisation at export time).
2. Wire transfer: `json.dumps(share, sort_keys=True).encode()` → bytes over the
   wire, or inside an envelope.
3. Import: `SubstrateProfile.from_dict(share["organism_profile"])` — the importer
   normalises the provider id internally.
4. Re-export: the restored profile is exactly representable (no floating-point
   drift in stored fields; floats use `float()` so round-trip is exact).
