---
name: firebase-basics
description: Use when working with Firebase products and services for mobile/web apps.
tags: [firebase, google-cloud, mobile, web, backend, cli]
related_skills: [google-cloud-recipe-auth, gemini-api]
---

# Firebase Basics

Provides the foundational workflow for setting up and configuring Firebase projects using the Firebase CLI.

## Prerequisites

- Node.js / NPM installed
- Firebase project (or create one)

## Quick Start

1. **Install Agent Skills for Firebase**: `npx -y skills add firebase/agent-skills -y`
2. **Log in**: `npx -y firebase-tools@latest login`
3. **Set active project**: `npx -y firebase-tools@latest use <PROJECT_ID>`

## Code Example: Creating a Firebase Project

```bash
# Create a new project
npx -y firebase-tools@latest projects:create my-app-project --display-name "My App"

# List existing projects
npx -y firebase-tools@latest projects:list
```

## Common Pitfalls

- **Missing NPM**: Firebase CLI requires Node.js — verify with `npm --version` first
- **Not logged in**: Run `firebase login` before any project operations
- **No active project**: Set active project with `firebase use --add <PROJECT_ID>`
- **Outdated CLI**: Use `npx -y firebase-tools@latest` to always get the latest version

## Verification Checklist

- [ ] NPM installed: `npm --version`
- [ ] Firebase CLI accessible: `npx firebase-tools --version`
- [ ] Logged in: `npx firebase-tools login`
- [ ] Active project set: `npx firebase-tools use`
- [ ] Firebase skills installed: `npx skills add firebase/agent-skills -y`
