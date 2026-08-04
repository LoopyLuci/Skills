---
name: data-contracts-schema-governance
description: "Use when implementing data contracts and schema governance."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-contracts, schema-governance, Avro, Protobuf, data-lineage, data-quality]
    related_skills: [data-profiling-quality, data-pipeline-streaming, database-schema-design, ml-pipeline-design]
---

# Data Contracts and Schema Governance

Implementing data contracts and schema governance — from schema registries (Avro, Protobuf) through contract testing, data lineage, and breaking change detection.

## When to Use

- Ensuring data quality between producers and consumers
- Managing schema evolution across microservices
- Detecting breaking schema changes in CI/CD
- Building data lineage and impact analysis
- Establishing data ownership and SLAs

## Data Contract Patterns

```python
DATA_CONTRACT_EXAMPLE = {
    'dataset': 'user_events',
    'owner': 'team-analytics',
    'schema_version': '1.2.0',
    'schema': {
        'type': 'record', 'name': 'UserEvent',
        'fields': [
            {'name': 'user_id', 'type': 'string'},
            {'name': 'event_type', 'type': 'string'},
            {'name': 'timestamp', 'type': 'long', 'logicalType': 'timestamp-millis'},
            {'name': 'properties', 'type': {'type': 'map', 'values': 'string'}},
        ],
    },
    'slas': {'freshness': '5min', 'completeness': '99.9%', 'volume_min': 1000},
    'consumers': ['team-product', 'team-ml'],
}

class SchemaCompatibility:
    """Check schema compatibility to prevent breaking changes."""
    
    @staticmethod
    def check_backward(original_schema: dict, new_schema: dict) -> bool:
        """Backward compatible: new reader can read old data."""
        original_fields = {f['name']: f for f in original_schema.get('fields', [])}
        new_fields = {f['name']: f for f in new_schema.get('fields', [])}
        
        for name, orig_field in original_fields.items():
            if name not in new_fields:
                return False  # Can't delete fields
            if orig_field['type'] != new_fields[name]['type']:
                # Allowed: widening type (int → long, string → union)
                if not SchemaCompatibility._is_widening(orig_field['type'], new_fields[name]['type']):
                    return False
        return True
```

## Verification Checklist

- [ ] Schema registry deployed (Confluent, Apicurio, or custom)
- [ ] Compatibility mode defined for each topic (backward, forward, full, none)
- [ ] Data contract document defined per dataset (owner, schema, SLAs, consumers)
- [ ] Breaking change detection in CI/CD pipeline
- [ ] Schema evolution documented in data contract versions
- [ ] Data lineage tracked (producer → topic → consumer)
- [ ] Data quality metrics monitored per contract
