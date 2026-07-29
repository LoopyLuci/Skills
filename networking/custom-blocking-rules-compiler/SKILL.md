---
name: custom-blocking-rules-compiler
description: "Use when compiling custom blocking rules."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [blocking-rules, adblock, firewall-rules, ABP-format, rule-compiler]
    related_skills: [adblock-engine-core-patterns, firewall-rules-engine, url-content-filter, waf-web-application-firewall]
---

# Custom Blocking Rules Compiler

Compiling custom blocking rules for adblocking, firewall, and content filtering — from rule parsing and optimization through compiled rule formats and performance tuning.

## When to Use

- Building custom adblock or content filter rule sets
- Converting rules between formats (ABP → uBlock, Surge, Pi-hole)
- Optimizing rule matching performance with data structures
- Compiling human-readable rules into efficient matching formats

## Rule Compilation

```python
import re
from typing import List, Dict

class BlockingRule:
    """A single blocking rule in ABP/adblock format."""
    def __init__(self, pattern: str, options: Dict = None):
        self.pattern = pattern  # e.g., ||example.com/ads/*
        self.options = options or {}
        self.type = self._detect_type()
    
    def _detect_type(self) -> str:
        if self.pattern.startswith('||'): return 'domain'
        if self.pattern.startswith('|'): return 'exact_prefix'
        if self.pattern.endswith('|'): return 'exact_suffix'
        if '*' in self.pattern: return 'wildcard'
        if self.pattern.startswith('/') and self.pattern.endswith('/'): return 'regex'
        return 'substring'

class RuleCompiler:
    """Compile blocking rules into optimized matching structures."""
    def __init__(self):
        self.rules = []
    
    def add_rules(self, rules_text: str):
        for line in rules_text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('!'):
                self.rules.append(BlockingRule(line))
    
    def compile_to_bloom(self) -> Dict:
        """Convert rules to bloom filter for fast pre-filtering."""
        domains = [r.pattern[2:] for r in self.rules if r.type == 'domain']
        return {'domains': domains, 'count': len(domains)}
    
    def optimize(self) -> int:
        """Merge and deduplicate rules."""
        patterns = set(r.pattern for r in self.rules)
        self.rules = [BlockingRule(p) for p in patterns]
        return len(self.rules)
```

## Verification Checklist

- [ ] Rules parsed from ABP-compatible format
- [ ] Rule types detected correctly (domain, wildcard, regex, exact)
- [ ] Rules compiled into optimized matching structure
- [ ] Deduplication and merging applied
- [ ] Performance benchmarked (rules/sec matching)
- [ ] False positive rate measured
- [ ] Export format supports target platform (Pi-hole, uBlock, AdGuard)
