---
name: adblock-engine-core-patterns
description: "Use when building core adblock engine architecture."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [adblock, filtering, engine, architecture, networking]
    related_skills: [blocklist-manager, dns-adblock-engine, url-content-filter, pattern-matching-engine, custom-blocking-rules-compiler]
---

# Adblock Engine Core Patterns

Core architecture patterns for building adblock engines — from list parsing and rule matching through network filtering to browser integration, with focus on performance at scale.

## When to Use

- Building a new adblock engine from scratch
- Optimizing an existing adblock engine for performance
- Adding adblocking capabilities to a proxy or firewall
- Understanding how adblock engines work internally
- Implementing cross-platform adblocking

## Engine Architecture

```
List Source → Parser → Rule Index → Matcher → Filter Decision
                 ↓
           Rule Compiler
                 ↓
          Network/Content Filter
```

## Rule Formats

### AdBlock Plus (ABP) Syntax

```python
# Rule format examples:
example.com##.ad-banner      # Element hiding
||example.com/ads/*          # Network filter
@@||example.com/analytics    # Exception
/adv[\w-]+\.js/              # Regex filter
example.com$script           # Domain + type restriction
127.0.0.1 example.com        # Hosts file format

class ABPRuleParser:
    """Parse AdBlock Plus filter syntax into structured rules."""
    
    def parse(self, line):
        line = line.strip()
        if not line or line.startswith('!') or line.startswith('#'):
            return None  # Comment or empty
        
        rule = {
            'raw': line,
            'type': self._detect_type(line),
            'pattern': None,
            'domains': None,
            'options': {},
            'exception': line.startswith('@@'),
        }
        
        if rule['type'] == 'network':
            self._parse_network_rule(line, rule)
        elif rule['type'] == 'element_hiding':
            self._parse_elemhide_rule(line, rule)
        
        return rule
    
    def _detect_type(self, line):
        if '##' in line or '#@#' in line or '#?#' in line:
            return 'element_hiding'
        if line.startswith('@@') or '||' in line or '/' in line[:2]:
            return 'network'
        if not line.startswith('.') and not line.startswith('#'):
            # Hosts file or domain rule
            return 'network'
        return 'network'
    
    def _parse_network_rule(self, line, rule):
        """Parse network filter rules."""
        # Strip exception marker
        text = line[2:] if line.startswith('@@') else line
        
        # Extract options after $
        if '$' in text:
            text, options_str = text.rsplit('$', 1)
            rule['options'] = self._parse_options(options_str)
        
        # Extract domain restriction
        if 'domain=' in str(rule['options']):
            rule['domains'] = rule['options'].get('domain', '').split('|')
        
        # Parse pattern
        if text.startswith('||'):
            # Domain-based
            rule['pattern'] = text[2:]
            rule['match_type'] = 'domain'
        elif text.startswith('/') and text.endswith('/'):
            # Regex
            rule['pattern'] = text[1:-1]
            rule['match_type'] = 'regex'
        else:
            rule['pattern'] = text
            rule['match_type'] = 'pattern'
    
    def _parse_options(self, options_str):
        options = {}
        for opt in options_str.split(','):
            if '=' in opt:
                k, v = opt.split('=', 1)
                options[k] = v
            else:
                options[opt] = True
        return options
```

## Rule Indexing for Fast Matching

```python
class RuleIndex:
    """Multi-level rule index for O(1) to O(k) matching."""
    
    def __init__(self):
        # Domain-based index: domain → [rules]
        self.domain_index = {}  # e.g., {"doubleclick.net": [rule1, rule2]}
        
        # Pattern trie for prefix matching
        self.pattern_index = {}  # Starts-with patterns
        
        # Regex cache
        self.regex_cache = {}  # pattern → compiled regex
        
        # Exception index (for fast exception lookup)
        self.exception_index = {}
    
    def add_rule(self, rule):
        if rule['match_type'] == 'domain':
            self._index_domain_rule(rule)
        elif rule['match_type'] == 'regex':
            self._index_regex_rule(rule)
        else:
            self._index_pattern_rule(rule)
        
        if rule['exception']:
            self._index_exception(rule)
    
    def _index_domain_rule(self, rule):
        """Index domain-based rules."""
        domain = rule['pattern'].lstrip('.').split('/')[0]
        
        # Add to exact domain
        self.domain_index.setdefault(domain, []).append(rule)
        
        # Add to parent domains
        parts = domain.split('.')
        for i in range(1, len(parts)):
            parent = '.'.join(parts[i:])
            self.domain_index.setdefault(parent, []).append(rule)
    
    def _index_regex_rule(self, rule):
        """Pre-compile regex rules."""
        pattern = rule['pattern']
        if pattern not in self.regex_cache:
            self.regex_cache[pattern] = re.compile(pattern, re.IGNORECASE)
    
    def _index_pattern_rule(self, rule):
        """Index wildcard patterns using first token."""
        pattern = rule['pattern']
        # Use the first non-wildcard token as key
        tokens = re.split(r'[\*\^]', pattern)
        key = tokens[0] if tokens else pattern[:10]
        self.pattern_index.setdefault(key, []).append(rule)
```

## Fast Matching Engine

```python
class MatchingEngine:
    """High-performance request matching engine."""
    
    def __init__(self, rule_index):
        self.index = rule_index
    
    def match(self, url, domain=None, content_type=None):
        """Match a URL against all rules. Returns block=True/False."""
        if domain is None:
            from urllib.parse import urlparse
            domain = urlparse(url).hostname
        
        # 1. Quick domain-based check
        if domain in self.index.domain_index:
            for rule in self.index.domain_index[domain]:
                if self._match_single(url, domain, rule):
                    if rule['exception']:
                        return False  # Exception overrides
                    return True
        
        # 2. Pattern matching
        # Extract first meaningful token from URL path
        path = self._get_path_token(url)
        if path and path in self.index.pattern_index:
            for rule in self.index.pattern_index[path]:
                if self._match_single(url, domain, rule):
                    return True
        
        # 3. Regex matching (expensive, do last)
        for pattern, regex in self.index.regex_cache.items():
            if regex.search(url):
                return True
        
        return False  # Default: allow
    
    def _match_single(self, url, domain, rule):
        """Check if a single rule matches."""
        if rule['options']:
            # Check content type restrictions
            if 'script' in rule['options']:
                pass  # Would need content type from request
            # Check domain restrictions
            if rule.get('domains'):
                if not any(d in domain or domain.endswith('.' + d) 
                          for d in rule['domains']):
                    return False
        
        if rule['match_type'] == 'domain':
            return domain == rule['pattern'].split('/')[0]
        elif rule['match_type'] == 'regex':
            return self.index.regex_cache[rule['pattern']].search(url)
        elif rule['match_type'] == 'pattern':
            return self._wildcard_match(url, rule['pattern'])
    
    def _wildcard_match(self, url, pattern):
        """Fast wildcard matching (no regex)."""
        # Simple case: no wildcards
        if '*' not in pattern and '^' not in pattern:
            return pattern in url
        
        # Split on '*' and check each segment
        parts = pattern.split('*')
        pos = 0
        
        for i, part in enumerate(parts):
            if not part:
                continue
            if i == 0:
                # Must match at start
                if not url.startswith(part):
                    return False
                pos = len(part)
            elif i == len(parts) - 1:
                # Must match at end
                return url.endswith(part) and part in url[pos:]
            else:
                idx = url.find(part, pos)
                if idx == -1:
                    return False
                pos = idx + len(part)
        
        return True
```

## Network Filter Integration

```python
class AdblockNetworkFilter:
    """Integrates the adblock engine at the network level."""
    
    def __init__(self, rule_lists=None):
        self.engine = MatchingEngine(RuleIndex())
        self.rule_lists = rule_lists or []
        self._load_rules()
    
    def _load_rules(self):
        parser = ABPRuleParser()
        for list_url in self.rule_lists:
            rules = self._fetch_list(list_url)
            for rule_text in rules:
                rule = parser.parse(rule_text)
                if rule:
                    self.engine.index.add_rule(rule)
    
    def should_block_request(self, url, request_type='other', domain=None):
        """Main entry point for proxy/DNS-level filtering."""
        return self.engine.match(url, domain, request_type)
    
    def should_block_element(self, url, domain):
        """For browser-level element hiding."""
        # Element hiding rules checked separately
        pass
```

## Performance Optimization

```python
class OptimizedEngine:
    """Performance-tuned adblock engine."""
    
    # Key optimizations:
    # 1. Bloom filter for negative cache (fast reject for non-blocked URLs)
    # 2. Domain trie for O(len(domain)) lookup
    # 3. Short-circuit on common CDNs (google-analytics.com, doubleclick.net)
    # 4. LRU cache for recently checked URLs
    
    def __init__(self, bloom_filter_size=10_000_000):
        self.bloom = self._build_bloom_filter()
        self.lru_cache = lru_cache(maxsize=10000)(self._match_url)
    
    def match(self, url):
        # 1. Bloom filter: 99% of unblocked URLs rejected in O(1)
        if not self.bloom.check(url):
            return False
        
        # 2. LRU cache for recently checked URLs
        return self.lru_cache(url)
```

## Common Pitfalls

1. **Rule explosion** — 100K+ rules make matching slow; use multi-level indexing and bloom filters
2. **Regex DoS** — malicious regex rules can cause catastrophic backtracking; use timeout or reject complex regex
3. **False positives** — over-blocking legitimate content; maintain exception lists and user feedback
4. **Memory usage** — loading 10M rules can use 500MB+; compress patterns, use compact trie structures
5. **Domain parsing edge cases** — IP addresses, punycode, port numbers; use URL parser library
6. **Browser vs. network-level** — some rules only work at browser level (element hiding); separate concerns

## Verification Checklist

- [ ] Correctly blocks known ad domains (doubleclick.net, googleadservices.com)
- [ ] Correctly allows exceptions (@@ rules override)
- [ ] Performance: < 1ms per URL match with 100K rules
- [ ] Memory: < 200MB for 100K rules
- [ ] Parses all major adlist formats (ABP, hosts, uBlock Origin)
- [ ] Content type filtering works (script-only, image-only rules)
- [ ] Element hiding rules work separately from network rules

## See Also

- blocklist-manager — managing adblock lists at scale
- dns-adblock-engine — DNS-level ad blocking
- url-content-filter — URL-level filtering
- pattern-matching-engine — high-performance pattern matching
- custom-blocking-rules-compiler — compiling custom rules
