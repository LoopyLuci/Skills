---
name: github-pages-setup
description: Deploy static sites to GitHub Pages from any branch.
---

# GitHub Pages Deployment

**Trigger**: Use when deploying a static site, docs site, or frontend app to GitHub Pages.

## Deployment Methods

| Method | When to use |
|--------|-------------|
| Deploy from branch | Simple static files, no build step |
| GitHub Actions | Build step needed, custom framework |
| Custom GitHub Action | Complex deployment, custom domain needs |

## Method 1: Deploy from Branch

```bash
# Enable Pages via API
gh api repos/:owner/:repo/pages \
  --method POST \
  --input - << 'EOF'
{"source": {"branch": "gh-pages", "path": "/"}}
EOF

# Create orphan gh-pages branch
git checkout --orphan gh-pages
git rm -rf .
echo "My Site" > index.html
git add index.html && git commit -m "Initial gh-pages"
git push origin gh-pages
git checkout main
```

## Method 2: GitHub Actions (Recommended)

### Static HTML
```yaml
name: Deploy to Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - id: deployment
        uses: actions/deploy-pages@v4
```

### Framework Builds
```yaml
name: Deploy to Pages
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'
      - uses: actions/deploy-pages@v4
```

## Custom Domain

```bash
# Set custom domain via API
gh api repos/:owner/:repo/pages --method PUT \
  --input - << 'EOF'
{"cname": "docs.example.com"}
EOF
```

### DNS Records
| Record | Type | Value |
|--------|------|-------|
| APEX | A | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| WWW | CNAME | `owner.github.io` |

## Pitfalls
- **404 on SPA**: Add `404.html` that redirects to `index.html` for client-side routing
- **Project site base URL**: Frameworks need `base: /repo-name/`
- **Custom domain propagation**: DNS changes can take up to 48 hours
- **Pages build timeout**: 10-minute limit for free accounts

## Verification
```bash
gh api repos/:owner/:repo/pages -q '.status, .cname'
curl -s -o /dev/null -w "%{http_code}" https://owner.github.io/repo/
```
