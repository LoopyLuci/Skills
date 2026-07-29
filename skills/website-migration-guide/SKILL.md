---
name: website-migration-guide
description: "Use when migrating websites. Platform moves, SEO."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [migration, website, hosting, platform-migration, seo]
    related_skills: [wordpress-development, static-site-generator-workflow, seo-strategy]
---

# Website Migration Guide

## Overview
Safe website migration between platforms: pre-migration audit, content export/import, redirect mapping, functionality verification, post-migration validation. Covers WordPress→SSG, Wix→WordPress, host migration, and HTTPS migration.

## When to Use
- "Migrate my site from [platform] to [platform]"
- "Change hosting providers"
- "Move from HTTP to HTTPS"
- "Migrate WordPress to Hugo/11ty"

## Migration Phases

### Phase 1: Pre-Migration Audit
1. **Content inventory**: List all pages, posts, media, custom post types. Use a sitemap or database export.
2. **URL mapping**: Map every existing URL to its new URL. Critical for SEO preservation.
3. **SEO baseline**: Record current rankings, traffic, backlinks, Domain Authority (use web_search for tool data)
4. **Functionality inventory**: Search, forms, ecommerce, membership, comments, analytics, redirects
5. **Performance baseline**: Record current page speed, Core Web Vitals, uptime

### Phase 2: Setup Staging (Parallel)
Set up the new site on staging:
- New platform installed and configured
- Content imported/migrated
- Theme/design recreated
- Plugins/extensions replaced (find equivalent tools on new platform)
- Functionality tested (search, forms, nav, etc.)

### Phase 3: Execution
1. **Final content sync**: Export any content changes since the initial audit
2. **DNS change**: Update DNS records to point to new hosting
3. **SSL certificate**: Install and verify on new host
4. **Redirects**: Implement 301 redirects for every changed URL (use redirect map)
5. **Submit sitemap**: Submit new XML sitemap to Google Search Console + Bing Webmaster Tools

### Phase 4: Post-Migration Validation
| Check | Method | Pass |
|-------|--------|------|
| All URLs resolve | Crawl site with Screaming Frog or similar | No 4xx errors |
| Redirects work | Spot-check 20-30 mapped URLs | 301 ✓ |
| SSL valid | SSL checker | No warnings |
| Search works | Test internal search | Results as expected |
| Forms submit | Manual test on all forms | Email/data received |
| 404 page | Visit `domain.com/sjdhfsjkdhf` | Custom 404, not default |
| Mobile responsive | Manual check on phone | No layout issues |
| Page speed | Lighthouse on 5 key pages | Within 10% of baseline |
| Search console | Check for crawl errors, index coverage | Down 24h then recovering |

## Specific Migration Paths

### WordPress → Static Site (Hugo/11ty)
1. Export WordPress content with `wordpress-export-to-markdown` or `wp2md`
2. Map WordPress categories/tags to SSG taxonomies
3. Recreate menus manually (SSGs don't have dynamic menus)
4. Handle comments (disqus migration, or drop them)
5. Migrate media files (download from wp-content/uploads, store in static/media)
6. Set up contact form (Netlify Forms, Formspree, or similar)

### Wix/Weebly/Squarespace → WordPress
1. Export content via platform's RSS or export tool
2. Use WordPress importers or manual copy-paste
3. Rebuild page layouts with a page builder (Elementor, Gutenberg)
4. Set up SEO plugin (Yoast/Rank Math — not available on Wix)

## Common Pitfalls
1. **Skipping redirect mapping** — every changed URL needs a 301 redirect or you lose SEO value
2. **Not monitoring search console** — crawl errors spike post-migration; check daily for first 2 weeks
3. **Content drift** — user-generated content (reviews, comments, forum posts) is often lost
4. **Downtime during DNS propagation** — set DNS TTL to 300 (5 min) a few days before migration
5. **Broken forms** — form handlers don't automatically transfer; test ALL forms post-migration

## Verification Checklist
- [ ] Content inventory completed (all pages, posts, media listed)
- [ ] URL mapping: every old URL → new URL documented
- [ ] SEO baseline recorded (rankings, traffic, backlinks)
- [ ] Staging site set up and verified (all content, functionality)
- [ ] DNS TTL lowered (300 sec) before migration day
- [ ] 301 redirects implemented and tested
- [ ] SSL certificate installed and valid
- [ ] Sitemap submitted to Google + Bing
- [ ] Post-migration: crawl for 4xx errors, test forms, check search console
- [ ] Performance within 10% of baseline