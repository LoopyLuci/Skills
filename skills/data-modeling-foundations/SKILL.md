---
name: data-modeling-foundations
description: "Use when designing data models and entity relationships."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-modeling, ERD, normalization, denormalization, entities, relationships]
    related_skills: [database-design-patterns, database-schema-design, sql-advanced-patterns, etl-pipeline-design]
---

# Data Modeling Foundations

Designing data models for relational and non-relational systems — from entities and relationships through normalization, denormalization, and data model patterns.

## When to Use

- Designing database schemas for new applications
- Modeling business entities and their relationships
- Normalizing data to reduce redundancy
- Optimizing data models for query performance
- Building conceptual, logical, and physical data models

## Modeling Levels

```python
MODELING_LEVELS = {
    'conceptual': 'Business entities and relationships (no technical details)',
    'logical': 'Attributes, data types, keys, relationships (DB-agnostic)',
    'physical': 'Tables, columns, indexes, partitions (DB-specific)',
}

# Entity-Relationship modeling
class DataModel:
    def __init__(self, name: str):
        self.name = name
        self.entities = {}  # entity_name -> attributes
    
    def add_entity(self, name: str, attributes: Dict, 
                   primary_key: str = 'id'):
        self.entities[name] = {
            'attributes': attributes, 'primary_key': primary_key,
            'relationships': []
        }
    
    def add_relationship(self, source: str, target: str, 
                         rel_type: str = 'one_to_many'):
        """one_to_one, one_to_many, many_to_many"""
        if source in self.entities and target in self.entities:
            self.entities[source]['relationships'].append({
                'target': target, 'type': rel_type
            })
```

## Common Pitfalls

1. **Over-normalization** — 6th normal form hurts query performance; stop at 3NF for OLTP
2. **Under-normalization** — duplicate data everywhere leads to update anomalies
3. **Ignoring access patterns** — model for how data is READ, not just stored
4. **No naming conventions** — inconsistent names create confusion; use conventions
5. **Mixed OLTP and OLAP** — transactional and analytical models have different needs; separate them

## Verification Checklist

- [ ] Entities identified and named consistently
- [ ] Relationships correctly typed (1:1, 1:M, M:M)
- [ ] Normalized to at least 3NF
- [ ] Access patterns considered in model design
- [ ] Primary and foreign keys defined
- [ ] Indexes on foreign keys and frequent query columns
- [ ] Denormalization justified (only for performance)
