---
name: cms-website-management
description: "Use when managing content management systems and websites."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cms, website-management, wordpress, web-hosting, domains, maintenance]
    related_skills: [seo-search-engine-optimization, website-analytics-tracking, blog-building-content-strategy, web-security-patterns]
---

# CMS and Website Management

Managing content management systems and websites — from setup and configuration through content management, security, performance optimization, and maintenance.

## When to Use

- Setting up a new website or CMS (WordPress, Ghost, etc.)
- Managing website content, media, and users
- Performing website maintenance (updates, backups, security)
- Optimizing website performance (speed, caching, CDN)
- Managing domains, hosting, and DNS

## CMS Setup

```python
from typing import Dict, List, Optional

class CMSManager:
    """Manage website/CMS configuration and content."""
    
    CMS_OPTIONS = {
        'wordpress': {
            'type': 'full_cms',
            'hosting': 'shared, VPS, managed WP',
            'setup_time': '30 min',
            'strengths': 'Largest ecosystem, plugins, themes, community',
            'weaknesses': 'Security, performance with too many plugins',
            'requirements': 'PHP 8+, MySQL/MariaDB, Apache/Nginx',
        },
        'ghost': {
            'type': 'headless_cms',
            'hosting': 'Ghost(Pro), VPS, serverless',
            'setup_time': '15 min',
            'strengths': 'Fast, modern editor, membership built-in',
            'weaknesses': 'Fewer themes, no plugin ecosystem',
            'requirements': 'Node.js, MySQL/SQLite',
        },
        'statamic': {
            'type': 'flat_file_cms',
            'hosting': 'Any PHP hosting',
            'setup_time': '10 min',
            'strengths': 'No database, Git-friendly, flexible',
            'weaknesses': 'Paid license, smaller community',
            'requirements': 'PHP 8+',
        },
    }
    
    @staticmethod
    def get_setup_guide(cms: str, domain: str, hosting: str) -> List[str]:
        """Get step-by-step CMS setup instructions."""
        guides = {
            'wordpress': [
                f"1. Point {domain} DNS to {hosting}",
                "2. Create MySQL database and user",
                "3. Download WordPress and upload via SFTP",
                "4. Run wp-config.php setup wizard",
                "5. Install essential plugins (SEO, caching, security)",
                "6. Choose theme and customize",
                "7. Set permalinks to /%postname%/",
            ],
            'ghost': [
                f"1. Provision server/node with Node.js 18+",
                "2. Install Ghost-CLI: npm install -g ghost-cli",
                "3. mkdir blog && cd blog && ghost install",
                "4. Configure domain, email, SSL during setup",
                "5. Access /ghost to configure theme and settings",
            ],
        }
        return guides.get(cms, [f"Manual setup guide for {cms}"])
```

## Website Audit

```python
class WebsiteAudit:
    """Audit website health across multiple dimensions."""
    
    @staticmethod
    def audit(domain: str, checks: Dict = None) -> Dict:
        """Run a comprehensive website audit."""
        checks = checks or {}
        
        results = {
            'domain': domain,
            'security': WebsiteAudit._check_security(domain, checks.get('security')),
            'performance': WebsiteAudit._check_performance(checks.get('performance')),
            'seo_fundamentals': WebsiteAudit._check_seo(checks.get('seo')),
            'maintenance': WebsiteAudit._check_maintenance(checks.get('maintenance')),
        }
        
        # Overall score
        scores = [r.get('score', 0) for r in results.values() if isinstance(r, dict)]
        results['overall'] = round(sum(scores) / max(len(scores), 1), 1)
        
        return results
    
    @staticmethod
    def _check_security(config: Dict = None) -> Dict:
        issues = []
        if config:
            if not config.get('ssl'): issues.append("SSL/HTTPS not enabled")
            if not config.get('firewall'): issues.append("No WAF configured")
            if not config.get('backups'): issues.append("No automated backups")
        score = max(0, 100 - len(issues) * 20)
        return {'score': score, 'issues': issues}
    
    @staticmethod
    def _check_performance(config: Dict = None) -> Dict:
        issues = []
        if config:
            if config.get('load_time', 0) > 3: issues.append("Page load > 3 seconds")
            if not config.get('caching'): issues.append("No caching enabled")
            if not config.get('cdn'): issues.append("No CDN")
            if not config.get('image_optimized'): issues.append("Images not optimized")
        score = max(0, 100 - len(issues) * 15)
        return {'score': score, 'issues': issues}
```

## Maintenance Schedule

```python
MAINTENANCE_TASKS = {
    'daily': [
        'Check for uptime (monitoring service)',
        'Check security logs for suspicious activity',
        'Verify backups completed successfully',
    ],
    'weekly': [
        'Update CMS core, plugins, themes',
        'Review and moderate comments',
        'Check broken links',
        'Review analytics for anomalies',
    ],
    'monthly': [
        'Full website backup (files + database)',
        'Delete spam comments and old revisions',
        'Check and optimize database tables',
        'Review and update content',
        'Test contact forms and key functionality',
    ],
    'quarterly': [
        'Complete security audit',
        'Update passwords and review user accounts',
        'Check and update SSL certificate',
        'Review and prune unused plugins/themes',
        'Performance audit (PageSpeed, GTmetrix)',
        'Review SEO rankings and update content',
    ],
    'annually': [
        'Domain renewal check',
        'Hosting plan review (do you need an upgrade?)',
        'Full content audit (update outdated info)',
        'Design refresh consideration',
        'Privacy policy and terms review',
    ],
}

def get_maintenance_report() -> str:
    """Generate maintenance status report."""
    report = "🛠️ Website Maintenance Report\n"
    report += "=" * 40 + "\n"
    import datetime
    report += f"Date: {datetime.date.today()}\n\n"
    
    for period, tasks in MAINTENANCE_TASKS.items():
        report += f"[{period.upper()}]\n"
        for task in tasks:
            report += f"  ⬜ {task}\n"
        report += "\n"
    
    return report
```

## Common Pitfalls

1. **Not updating** — outdated CMS/plugins cause 90% of hacks; update weekly
2. **No backups** — when site crashes, you lose everything; automated daily backups
3. **Too many plugins** — each plugin adds bloat and vulnerability; minimize plugins
4. **Ignoring mobile** — 60%+ of traffic is mobile; test every change on mobile
5. **No staging environment** — testing changes directly on production causes downtime
6. **Weak passwords** — admin accounts with weak passwords = site compromise

## Verification Checklist

- [ ] CMS and all plugins updated to latest versions
- [ ] Automated backups configured (files + database)
- [ ] SSL certificate valid and configured
- [ ] CDN configured for static assets
- [ ] Caching enabled (page cache, browser cache)
- [ ] Security plugin/WAF installed
- [ ] Contact forms working
- [ ] 404 page customized
- [ ] Robots.txt and sitemap configured
- [ ] Google Search Console verified
- [ ] Analytics tracking code installed
- [ ] Staging environment for testing

## See Also

- seo-search-engine-optimization — technical SEO for websites
- website-analytics-tracking — analytics for website
- blog-building-content-strategy — content on CMS
- web-security-patterns — securing the website
