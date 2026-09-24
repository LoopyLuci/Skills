---
name: parental-controls
description: Use when implementing time/age-based content filtering.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [parental, controls, filtering, safety, schedule, rust]
---

# Parental Controls

**Trigger**: Use when implementing time-based, category-based, and age-based filtering.

**Libraries**: `url-content-filter`, `application-filter`, `chrono`, `dashmap`

**Implementation**: Per-device or per-user profiles with content category allowances. Time-based schedules (no internet after 10pm, limited gaming on weekdays). Safe search enforcement (add ?safe=active to search URLs). Age-based filtering tiers. Bedtime mode: all non-essential traffic blocked. Activity reports emailed to parents. PIN-protected override.

**Connected**: `url-content-filter`, `application-filter`, `http-https-inspector`, `dns-adblock-engine`, `realtime-dashboard`, `traffic-analyzer`
