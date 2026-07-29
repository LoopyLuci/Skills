---
name: osint-reconnaissance-techniques
description: "Use when performing OSINT and reconnaissance."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [OSINT, reconnaissance, passive-recon, subdomain-enum, Google-dorking, Shodan]
    related_skills: [bug-bounty-methodology, network-scanning-enumeration, penetration-testing-methodology, social-engineering-phishing]
---

# OSINT and Reconnaissance Techniques

Performing open-source intelligence gathering — from passive reconnaissance through subdomain enumeration, technology fingerprinting, Google dorking, and Shodan/Censys querying.

## When to Use

- Passive recon before penetration testing
- Gathering target information from public sources
- Subdomain and technology discovery
- Employee and email enumeration
- OSINT for social engineering preparation

## OSINT Techniques

```python
OSINT_TOOLS = {
    'subdomain_enum': 'subfinder, amass, assetfinder, Sublist3r, crt.sh (Certificate Transparency)',
    'tech_detection': 'wappalyzer, builtwith, whatweb, webanalyze — framework/css/js/server detection',
    'google_dorking': 'site:, intitle:, inurl:, filetype:, cache: — find exposed information',
    'email_enum': 'hunter.io, phonebook.cz, theHarvester — discover email patterns',
    'shodan': 'Search devices, open ports, banners, vulnerabilities with filters',
    'github_leaks': 'gitrob, truffleHog — search repos for secrets, tokens, credentials',
    'wayback_machine': 'archive.org — find historical endpoints, parameters, hidden paths',
}

# Google dork examples
GOOGLE_DORKS = {
    'login_pages': 'inurl:admin intitle:login',
    'exposed_files': 'site:target.com filetype:pdf OR filetype:xlsx',
    'directory_listing': 'intitle:"index of" site:target.com',
    'error_messages': 'inurl:"error=php"|"warning=php" site:target.com',
    'config_files': 'filetype:env OR filetype:config site:target.com',
}

def crt_sh_subdomains(domain: str) -> List[str]:
    """Query crt.sh Certificate Transparency logs for subdomains."""
    import requests
    resp = requests.get(f'https://crt.sh/?q=%25.{domain}&output=json')
    if resp.status_code == 200:
        return list(set(e['name_value'] for e in resp.json()))
    return []
```

## Verification Checklist

- [ ] Passive recon completed before active scanning
- [ ] Subdomain enumeration (certificate transparency, DNS bruteforce)
- [ ] Technology stack identified (Wappalyzer, BuiltWith)
- [ ] Google dorking for exposed information
- [ ] Email/employee enumeration (if in scope)
- [ ] Shodan/Censys search for exposed services
- [ ] GitHub/GitLab for leaked credentials and internal tools
- [ ] Wayback Machine for historical endpoints
- [ ] Information organized and documented for next phase
- [ ] Legal review: only public information, no social engineering without explicit scope
