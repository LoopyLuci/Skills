---
name: regular-expressions-mastery
description: "Use when writing advanced regular expressions and patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [regex, regular-expressions, pattern-matching, text-processing, python]
    related_skills: [pattern-matching-engine, compiler-interpreter-basics, data-structures-algorithms, sql-query-optimization]
---

# Regular Expressions — Advanced Patterns and Techniques

Mastering regular expressions for text processing — from advanced syntax through performance optimization, debugging, and cross-language differences.

## When to Use

- Parsing or extracting information from unstructured text
- Validating complex input formats (email, URLs, dates)
- Search-and-replace across large codebases
- Building lexers, tokenizers, or simple parsers
- Automating text transformation workflows

## Core Patterns Reference

### Character Classes

```
Pattern        Matches
\d             Any digit [0-9]
\w             Word char [a-zA-Z0-9_]
\s             Whitespace [ \t\n\r\f\v]
\b             Word boundary
\D, \W, \S     Negations of above
[aeiou]        Any vowel
[^aeiou]       Any non-vowel (negated class)
[a-f0-9]       Range: a-f or 0-9
```

### Quantifiers

```
Pattern        Matches       Greedy
a*             Zero or more  Yes (grab all possible)
a+             One or more   Yes
a?             Zero or one   Yes
a*?            Zero or more  No (lazy — as few as possible)
a+?            One or more   No (lazy)
a{3}           Exactly 3
a{2,5}         Between 2 and 5
a{2,}          2 or more
```

### Groups and Backreferences

```
Pattern               Captures
(abc)                 Capturing group 1
(?:abc)               Non-capturing group
(?P<name>abc)         Named group (Python)
(?P=name)             Backreference to named group
\1                    Backreference to group 1
(?(1)yes|no)          Conditional: if group 1 matched, match "yes", else "no"
```

## Lookahead/Lookbehind (Zero-Width Assertions)

```python
# Lookahead: match X only if followed by Y
# X(?=Y)    — positive lookahead
# X(?!Y)    — negative lookahead

# Lookbehind: match X only if preceded by Y
# (?<=Y)X   — positive lookbehind
# (?<!Y)X   — negative lookbehind

import re

# Match 'foo' only when followed by 'bar'
re.findall(r'foo(?=bar)', 'foobar foobaz')   # → ['foo']

# Match 'foo' only when NOT followed by 'bar'
re.findall(r'foo(?!bar)', 'foobar foobaz')   # → ['foo']

# Match 'bar' only when preceded by 'foo'
re.findall(r'(?<=foo)bar', 'foobar bazbar')  # → ['bar']

# Match USD amounts not preceded by a minus
re.findall(r'(?<![-\$])\$\d+', 'Price: $10, Debt: -$5')  # → ['$10']
```

## Advanced Techniques

### Recursive Patterns

```python
# Python's regex doesn't support recursion natively.
# Use regex module (pip install regex) for recursive patterns.
import regex

# Match nested parentheses
pattern = regex.compile(r'\((?:[^()]|(?R))*\)')
pattern.findall('(a(b(c)d)e)')  # → ['(a(b(c)d)e)']

# Match palindromes (the classic recursive challenge)
palindrome = regex.compile(r'(\w)(?:(?R)|(\w?))\1')  # Approximate
```

### Overlapping Matches

```python
# Standard re.findall doesn't find overlapping matches
# Solution: positive lookahead with a capturing group inside
text = 'ababa'
re.findall(r'(?=(aba))', text)  # → ['aba', 'aba']
# Finds both starting at positions 0 and 2
```

### Verbose Mode

```python
# Write readable regex with comments and whitespace
pattern = re.compile(r"""
    ^                    # Start of string
    (?P<protocol>https?) # Protocol (http or https)
    ://
    (?P<domain>          # Domain name
        [\w.-]+          # Subdomain + domain
        \.[a-z]{2,}      # TLD
    )
    (?P<port>:\d+)?      # Optional port
    (?P<path>/[\w/.-]*)? # Optional path
    (?P<query>\?[\w=&]+)?# Optional query string
    $
""", re.VERBOSE | re.IGNORECASE)
```

## Performance Optimization

```python
class RegexOptimizer:
    """Patterns for writing fast regular expressions."""
    
    # 1. Specific over general
    SLOW = r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+'
    FAST = r'\w+@\w+\.\w+'  # Same effect, simpler engine
    
    # 2. Avoid catastrophic backtracking
    # BAD: (a|aa)+b  — tries 2^n paths on input 'aaaaaaaaac'
    # FIX: a+b        — linear
    # BAD: (<.*>)+    — catastrophic on nested tags
    # FIX: (<[^>]*>)+ — no backtracking
    
    # 3. Use possessive quantifiers where supported
    # BAD: \d+\b   — backtracks to check boundary
    # FIX: \d++\b  — possessive, no backtracking (Python: no, PCRE: yes)
    
    # 4. Pre-compile, don't recompile
    @staticmethod
    def cached(pattern, flags=0):
        """Cache compiled patterns."""
        if not hasattr(RegexOptimizer, '_cache'):
            RegexOptimizer._cache = {}
        key = (pattern, flags)
        if key not in RegexOptimizer._cache:
            RegexOptimizer._cache[key] = re.compile(pattern, flags)
        return RegexOptimizer._cache[key]
```

## Common Patterns Library

```python
# Email (RFC 5322 simplified)
EMAIL = r"""[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"""

# URL
URL = r"""https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[\w/.~:?#\[\]@!$&'()*+,;=-]*)?/?"""

# IPv4
IPV4 = r"""(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"""

# ISO 8601 Date
ISO_DATE = r"""\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])"""

# UUID (all variants)
UUID = r"""[\da-f]{8}-[\da-f]{4}-[1-5][\da-f]{3}-[89ab][\da-f]{3}-[\da-f]{12}"""

# Hex Color
HEX_COLOR = r"""#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b"""

# Password: 8+ chars, upper, lower, digit, special
PASSWORD = r"""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"""

# Code comment extraction
COMMENTS = {
    'python': r'#.*$',
    'javascript': r'//.*$|/\*[\s\S]*?\*/',
    'html': r'<!--[\s\S]*?-->',
}
```

## Debugging Regex

```python
def debug_regex(pattern, text):
    """Debug regex matches step by step."""
    compiled = re.compile(pattern)
    print(f"Pattern: /{pattern}/")
    print(f"Text: {repr(text)}")
    print(f"Match: {compiled.search(text)}")
    print(f"Fullmatch: {compiled.fullmatch(text)}")
    print(f"Findall: {compiled.findall(text)}")
    
    # Show groups
    match = compiled.search(text)
    if match:
        print(f"Groups: {match.groups()}")
        print(f"GroupDict: {match.groupdict()}")
        for i, g in enumerate(match.groups()):
            print(f"  [{i}] = {repr(g)}")
```

## Common Pitfalls

1. **Catastrophic backtracking** — nested quantifiers on overlapping patterns cause exponential time
2. **Failing to escape** — `.` `+` `*` `?` `[` `]` `(` `)` `{` `}` `\` `|` `^` `$` need `\` for literal match
3. **Using regex for non-regular languages** — regex can't parse HTML, JSON, or nested structures; use a real parser
4. **Greedy when lazy needed** — `(.*)` grabs the whole line; `(.*?)` stops at first match
5. **Re.compile in loops** — compiling inside a hot loop destroys performance; cache patterns
6. **Line boundaries with `^` and `$`** — default is string boundaries; use `re.MULTILINE` for line boundaries

## Verification Checklist

- [ ] Pattern tested against edge cases (empty string, unicode, very long text)
- [ ] No catastrophic backtracking risk (test with pathological input)
- [ ] Performance measured on expected input size
- [ ] Pattern compiled once, not in a loop
- [ ] Regex101 or similar tool used during development
- [ ] Alternative considered: is a simpler non-regex approach available?

## See Also

- pattern-matching-engine — multi-pattern matching at scale
- compiler-interpreter-basics — using regex in lexers
- sql-query-optimization — LIKE/SIMILAR TO patterns vs regex
