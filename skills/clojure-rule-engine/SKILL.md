---
name: clojure-rule-engine
title: Clojure Rule Engine
description: Use when implementing rule-based filtering logic in Clojure.
category: networking
tags: [clojure, rules, engine, clara, lisp, reasoning]
---

# Clojure Rule Engine

**Trigger**: Use when implementing complex rule evaluation logic for Sentinel.

**Libraries**: Clojure 1.12, `clara-rules` (forward-chaining rules engine), `core.async`

**Implementation**: Clara forward-chaining rules for firewall policy evaluation. Fact types: `ConnectionFact`, `ThreatFact`, `BlocklistFact`. Rules: if domain matches threat intel AND score > 50 THEN block. Core.async channels for event ingestion from Rust core. Rule hot-reload without restart. Priority-based rule chaining. Backward-chaining diagnostics via Z3 when needed.

**Connected**: `python-orchestrator`, `rust-core-ffi`, `dns-adblock-engine`, `firewall-rules-engine`, `ml-threat-detection`
