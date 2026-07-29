---
name: wordpress-development
description: "Use when developing WordPress. Themes, plugins."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [wordpress, php, themes, plugins, development]
    related_skills: [blog-publishing-workflow, landing-page-builder]
---

# WordPress Development

## Overview
Complete WordPress development workflow: local setup, theme development (PHP template hierarchy, block editor, hooks, CPTs, ACF), plugin guidance, caching/CDN, migration, security hardening, and WooCommerce setup.

## When to Use
- "Set up a WordPress site"
- "Customize this WordPress theme"
- "Build a custom post type"
- "Secure a WordPress site"

## Local Setup
```bash
# Option A: LocalWP (recommended) — install from https://localwp.com
# One-click WordPress setup with SSL, live link sharing

# Option B: Docker
docker compose up -d
# wp-config.php auto-generated, phpMyAdmin at localhost:8080
```

## Theme Development

### Template Hierarchy
```
index.php (fallback)
├── home.php (blog index)
├── single.php (single post)
│   └── single-{post-type}.php
├── page.php (single page)
│   └── page-{slug}.php
├── archive.php (archive pages)
│   └── archive-{post-type}.php
├── category.php → tag.php → taxonomy.php
├── search.php
├── 404.php
└── front-page.php (static homepage)
```

### Child Theme
Create `wp-content/themes/my-theme-child/style.css`:
```css
/*
Theme Name: My Theme Child
Template: parent-theme-folder
*/
```

And `functions.php`:
```php
<?php
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');
});
```

### Custom Post Types & ACF
```php
// functions.php
add_action('init', function() {
    register_post_type('property', [
        'labels' => ['name' => 'Properties', 'singular_name' => 'Property'],
        'public' => true,
        'supports' => ['title', 'editor', 'thumbnail', 'custom-fields'],
        'menu_icon' => 'dashicons-admin-home',
    ]);
});
```

## Essential Plugins
| Category | Plugin | Purpose |
|----------|--------|---------|
| SEO | Yoast SEO / Rank Math | Meta, sitemap, readability |
| Caching | WP Rocket / W3 Total Cache | Page cache, minify, CDN |
| Security | Wordfence / Sucuri | Firewall, malware scan, login security |
| Forms | Gravity Forms / Fluent Forms | Contact forms, payment collection |
| Images | ShortPixel / Smush | Compression, WebP conversion |
| Backup | UpdraftPlus / BlogVault | Scheduled offsite backups |

## Security Hardening Checklist
- [ ] Change `wp_` table prefix during install (not after)
- [ ] Disable XML-RPC (block brute force attacks)
- [ ] Force HTTPS with `.htaccess` redirect
- [ ] Limit login attempts (Wordfence or custom)
- [ ] Disable file editing from admin (`define('DISALLOW_FILE_EDIT', true)`)
- [ ] Strong passwords (enforce via plugin)
- [ ] Regular updates (core, themes, plugins)
- [ ] Remove demo content and unused themes/plugins

## Common Pitfalls
1. **Plugin bloat** — each plugin is a security and performance risk; audit quarterly
2. **Not using child themes** — parent theme updates will overwrite all customizations
3. **Default permalinks** — change to "Post name" immediately for SEO
4. **No staging environment** — never update plugins or themes on production without testing
5. **Ignoring PHP version** — outdated PHP is the #1 WordPress security vulnerability

## Verification Checklist
- [ ] Local environment set up and running
- [ ] Child theme created if customizing an existing theme
- [ ] Custom post types and ACF fields registered
- [ ] Essential plugins installed and configured
- [ ] Security checklist items completed
- [ ] Permalinks set to "Post name"
- [ ] Caching plugin configured