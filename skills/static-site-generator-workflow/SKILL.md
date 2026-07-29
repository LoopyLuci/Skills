---
name: static-site-generator-workflow
description: "Use when building static sites. SSG setup, deploy."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [static-site, hugo, jekyll, 11ty, astro, jamstack]
    related_skills: [website-architecture-planner, blog-publishing-workflow]
---

# Static Site Generator Workflow

## Overview
Set up, configure, and deploy static sites with Hugo, Jekyll, 11ty, or Astro. Covers theme selection and customization, content organization, build pipeline configuration, deployment, RSS, SEO metadata, and image optimization.

## When to Use
- "Set up a blog with Hugo"
- "Create a static site with 11ty or Astro"
- "Deploy my site to Netlify/Vercel"

## SSG Quick Decision
| SSG | Language | Best For | Build Speed | Learning Curve |
|-----|----------|----------|-------------|----------------|
| Hugo | Go (templates) | Blogs, docs, speed-critical | Fastest | Moderate |
| Jekyll | Ruby | GitHub Pages, standard blogs | Slow (large sites) | Easy |
| 11ty | JavaScript | Flexible, multi-template | Fast | Moderate |
| Astro | JavaScript (islands) | Content sites, partial interactivity | Fast | Moderate |

## Setup Workflow (Hugo example)

```bash
# Install
brew install hugo  # macOS
scoop install hugo  # Windows
# Create site
hugo new site my-site --format yaml
cd my-site

# Add theme (git submodule)
git init
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke

# Configure (hugo.yaml)
baseURL: "https://example.com/"
languageCode: "en-us"
title: "My Site"
theme: "ananke"

# Create content
hugo new posts/first-post.md
# Edit content/posts/first-post.md frontmatter
```

## Content Organization
```
content/
├── _index.md          # Homepage content
├── posts/             # Blog posts
│   ├── _index.md      # Blog list page
│   └── post-1.md
├── projects/
│   ├── _index.md
│   └── project-1.md
├── about.md
└── contact.md
```

### Frontmatter template (YAML)
```yaml
---
title: "Post Title"
date: 2024-01-15T10:00:00Z
draft: false
tags: [tag1, tag2]
categories: [category]
description: "SEO meta description, 150-160 chars"
featured_image: "/images/post-image.jpg"
---

Post content in markdown.
```

## Build & Deploy
```bash
# Local development
hugo server -D  # -D includes drafts

# Build
hugo --minify

# Deploy to Netlify (netlify.toml)
[build]
  command = "hugo --minify"
  publish = "public"

[[redirects]]
  from = "/blog/*"
  to = "/posts/:splat"
  status = 301
```

## RSS, SEO & Images
- **RSS**: Hugo generates RSS automatically at `/index.xml`. Customize in config.
- **SEO**: Title templates, meta descriptions in frontmatter, `<!--more-->` for excerpts
- **Images**: Use `image` shortcode, lazy loading, WebP format, responsive srcset

## Common Pitfalls
1. **Not setting baseURL** — RSS and sitemap will have wrong URLs
2. **Draft posts in production** — remember to set `draft: false`
3. **Missing .nojekyll** — GitHub Pages assumes Jekyll; add empty `.nojekyll` file for Hugo/11ty
4. **Theme updates breaking layout** — pin theme to a specific commit with git submodules
5. **Slow builds** — large image galleries kill build times; use image processing at build, not runtime

## Verification Checklist
- [ ] SSG selected and initialized
- [ ] Theme installed and configured
- [ ] Content organized (posts, pages, sections)
- [ ] Frontmatter complete (title, date, tags, description)
- [ ] Build runs without errors locally
- [ ] Deployed to chosen platform (Netlify/Vercel/GitHub Pages)
- [ ] RSS feed accessible at /index.xml
- [ ] Sitemap generated at /sitemap.xml