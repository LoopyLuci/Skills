---
name: webapp-penetration-testing
description: "Use when testing web application security."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [webapp, pentest, OWASP-Top-10, Burp-Suite, SQLi-XSS, web-security]
    related_skills: [api-penetration-testing, sql-injection-exploitation, cross-site-scripting-exploitation, web-security-patterns]
---

# Web Application Penetration Testing

Testing web application security — from OWASP Top 10 through Burp Suite workflow, authentication testing, injection flaws, and logic flaws.

## When to Use

- Performing web application security assessments
- Testing OWASP Top 10 vulnerabilities
- Using Burp Suite for manual and automated testing
- Finding business logic flaws
- Reporting web vulnerabilities

## OWASP Top 10 Testing

```python
OWASP_TESTS = {
    'broken_access': 'Test IDOR, role-based access, forced browsing, path traversal',
    'cryptographic_failures': 'Test weak TLS, sensitive data in transit/rest, default credentials',
    'injection': 'Test SQL, NoSQL, OS command, LDAP, and expression language injection',
    'insecure_design': 'Test rate limiting, secure defaults, architecture review',
    'security_misconfig': 'Test default accounts, error handling, HTTP headers, open cloud storage',
    'vulnerable_components': 'Identify outdated libraries (OWASP Dependency Check, retire.js)',
    'auth_failures': 'Test credential stuffing, session fixation, weak password policies',
    'integrity_failures': 'Test CI/CD pipeline security, unsigned updates',
    'logging_monitoring': 'Test audit logging, alerting effectiveness',
    'ssrf': 'Test server-side request forgery to internal resources',
}

class BurpSuiteWorkflow:
    """Burp Suite pentesting workflow."""
    @staticmethod
    def workflow() -> List[str]:
        return [
            '1. Configure browser proxy (127.0.0.1:8080)',
            '2. Map application with spider/scan (Target → Site Map)',
            '3. Identify entry points (Repeater, Intruder)',
            '4. Test authentication (Intruder with wordlists)',
            '5. Test authorization (forced browsing, IDOR)',
            '6. Test injection (SQLi, XSS, SSTI) with Repeater',
            '7. Test business logic (manual, multi-step flows)',
            '8. Scan with active scanner (Pro only)',
            '9. Validate findings manually',
            '10. Document evidence with screenshots',
        ]
```

## Verification Checklist

- [ ] Burp Suite or equivalent configured
- [ ] OWASP Top 10 tested systematically
- [ ] Authentication mechanisms tested (bypass, MFA, session mgmt)
- [ ] Authorization tested (IDOR, privilege escalation)
- [ ] Injection points tested (SQL, NoSQL, command, SSTI)
- [ ] Business logic flaws manually reviewed
- [ ] API endpoints tested alongside web UI
- [ ] Findings validated (no false positives)
- [ ] Sensitive data removed from reports
