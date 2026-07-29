---
name: password-cracking-hash-analysis
description: "Use when cracking passwords and analyzing hashes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [password-cracking, hashcat, john, hash-analysis, wordlist, GPU, brute-force]
    related_skills: [active-directory-pentesting, webapp-penetration-testing, privilege-escalation-techniques, osint-reconnaissance-techniques]
---

# Password Cracking and Hash Analysis

Cracking passwords and analyzing hashes — from hash identification through Hashcat/John workflows, rule-based attacks, GPU acceleration, and wordlist generation.

## When to Use

- Testing password policy strength during pentests
- Cracking password hashes obtained during assessments
- Analyzing hash types (NT, NTLM, bcrypt, SHA, MD5)
- Building custom wordlists and rule sets

## Cracking Techniques

```python
HASHCAT_ATTACKS = {
    'straight': "hashcat -m 1000 -a 0 hashes.txt wordlist.txt — dictionary attack",
    'rule_based': "hashcat -m 1000 -a 0 hashes.txt wordlist.txt -r best64.rule — with rules",
    'mask': "hashcat -m 1000 -a 3 hashes.txt ?l?l?l?l?l?l?l?l — brute force mask (?l=lowercase)",
    'combinator': "hashcat -m 1000 -a 1 hashes.txt word1.txt word2.txt — word combo attack",
    'association': "hashcat -m 1000 -a 6 hashes.txt wordlist.txt ?d?d?d — append digits",
}

JOHN_RULES = """
# Custom rule: capitalize + append year
$[A-Z] $1 $2 $3 $4
c $1 $2 $3 $4
$[0-9] $[0-9] $[0-9] $[0-9]
"""

class HashIdentifier:
    """Identify hash type from format."""
    @staticmethod
    def identify(hash_string: str) -> List[str]:
        patterns = {
            'MD5': r'^[a-f0-9]{32}$',
            'SHA1': r'^[a-f0-9]{40}$',
            'SHA256': r'^[a-f0-9]{64}$',
            'bcrypt': r'^\$2[ayb]\$[0-9]{2}\$.{53}$',
            'NTLM': r'^[a-f0-9]{32}$',  # Same as MD5 but context-different
        }
        import re
        possible = []
        for name, pattern in patterns.items():
            if re.match(pattern, hash_string, re.I):
                possible.append(name)
        return possible
```

## Verification Checklist

- [ ] Hash type correctly identified
- [ ] Cracking mode selected (dictionary, rule, mask, combinator, brute-force)
- [ ] GPU acceleration enabled (OpenCL/CUDA)
- [ ] Wordlist chosen (rockyou, SecLists, or custom)
- [ ] Rule sets applied (best64, OneRuleToRuleThemAll)
- [ ] Cracking time estimated (keyspace / hash rate)
- [ ] Potfile checked for previously cracked hashes
- [ ] Ethical boundaries: only authorized hashes cracked
- [ ] Cracked passwords reported securely (not in plain text reports)
