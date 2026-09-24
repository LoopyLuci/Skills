# LoopyLuci Skills — Format Specification

This document defines the complete format for skills in the LoopyLuci/Skills repository.
Every skill follows the [agentskills.io](https://agentskills.io/) open standard with Hermes extensions.

## Directory Layout

```
skills/<skill-name>/          # kebab-case directory
├── SKILL.md                  # Required — skill definition
├── references/               # Optional — additional documentation
│   └── <topic>.md
├── templates/                # Optional — output templates
│   └── <template>.<ext>
├── scripts/                  # Optional — helper scripts
│   └── <script>.<ext>
├── assets/                   # Optional — images, data files
│   └── <file>.<ext>
└── examples/                 # Optional — example outputs
    └── <example>.<ext>
```

## SKILL.md Structure

### YAML Frontmatter

```yaml
---
name: skill-name              # Required — kebab-case, matches directory
description: Brief description (≤120 chars)  # Required — one sentence
version: 1.0.0                # Required — semver
author: Name/Handle            # Required
license: MIT                   # Required — SPDX identifier
platforms: [any]               # Required — [linux, macos, windows, any]
metadata:
  hermes:
    tags: [tag1, tag2]         # Required — 2-5 lowercase tags
    related_skills: [other]    # Optional — related skill names
---
```

### Body Structure

```markdown
# Skill Title

One-sentence summary of what this skill does and when to use it.

## Trigger

- Conditions that activate this skill
- User intent patterns (e.g., "build X", "fix Y")

## Core Concepts

- Key terminology and domain vocabulary
- Fundamental principles
- Mental models and frameworks

## Step-by-Step Workflow

1. **Phase Name** — What happens, why, expected output
2. **Phase Name** — What happens, why, expected output
3. **Phase Name** — What happens, why, expected output

## Tools & Technologies

- Specific tools, libraries, platforms
- APIs and integrations
- Environment requirements

## Best Practices

- Do this (with rationale)
- Avoid that (with rationale)
- Common patterns that work

## Common Pitfalls

- Mistake → consequence → fix
- Anti-pattern → why it fails → better approach

## References

- Links to docs, specs, tutorials
- See `references/` directory for detailed guides
```

## Naming Conventions

- **Format**: lowercase kebab-case: `python-web-scaffold`, `react-performance-optimization`
- **Length**: 2-6 words, descriptive
- **Pattern**: `[domain]-[specific-topic]` or `[tool]-[use-case]`
- **Avoid**: version numbers, personal prefixes, ambiguous abbreviations

## Tag Taxonomy

### Software Development
`python`, `javascript`, `typescript`, `rust`, `go`, `java`, `csharp`, `cpp`, `ruby`, `swift`, `kotlin`, `sql`, `react`, `vue`, `angular`, `nextjs`, `fastapi`, `django`, `flask`, `spring`, `nodejs`, `express`, `graphql`, `rest`, `grpc`, `docker`, `kubernetes`, `terraform`, `aws`, `gcp`, `azure`, `ci-cd`, `testing`, `debugging`, `refactoring`, `design-patterns`, `architecture`, `microservices`, `serverless`, `git`, `vim`, `vscode`, `linux`, `bash`, `regex`, `performance`, `security`, `accessibility`

### Data & AI
`machine-learning`, `deep-learning`, `nlp`, `computer-vision`, `data-science`, `data-engineering`, `analytics`, `visualization`, `statistics`, `pandas`, `numpy`, `pytorch`, `tensorflow`, `scikit`, `spark`, `airflow`, `dbt`, `etl`, `data-warehouse`, `lakehouse`, `streaming`, `kafka`, `vector-database`, `embeddings`, `llm`, `rag`, `fine-tuning`, `prompt-engineering`

### Security
`penetration-testing`, `vulnerability-assessment`, `incident-response`, `threat-intelligence`, `cryptography`, `iam`, `compliance`, `audit`, `malware-analysis`, `forensics`, `application-security`, `network-security`, `cloud-security`, `iot-security`, `blockchain-security`, `privacy`, `gdpr`, `hipaa`, `pci-dss`, `soc2`

### Creative & Design
`ui-design`, `ux-research`, `graphic-design`, `typography`, `color-theory`, `motion-graphics`, `video-editing`, `photography`, `illustration`, `3d-modeling`, `animation`, `game-design`, `music-production`, `sound-design`, `copywriting`, `content-strategy`

### Business & Product
`product-management`, `project-management`, `agile`, `scrum`, `kanban`, `strategy`, `marketing`, `sales`, `customer-success`, `operations`, `finance`, `accounting`, `hr`, `legal`, `procurement`, `supply-chain`, `logistics`

### Science & Engineering
`physics`, `chemistry`, `biology`, `mathematics`, `electronics`, `mechanical`, `civil`, `aerospace`, `biotechnology`, `environmental`, `materials-science`, `nanotechnology`, `robotics`, `quantum-computing`

### Personal Productivity
`note-taking`, `time-management`, `habit-formation`, `learning`, `reading`, `writing`, `meditation`, `fitness`, `nutrition`, `cooking`, `travel`, `finance-personal`, `minimalism`

## Quality Requirements

- Description must be a single sentence, ≤120 characters
- At least 2 tags, ideally 3-5
- Body must have at least: Title, Trigger, one content section
- Code blocks must specify language
- Links must be absolute URLs
- No placeholder text ("TODO", "TBD", "coming soon")

## agentskills.io Compatibility

Skills in this repo are compatible with the agentskills.io standard:
- YAML frontmatter with `name` and `description`
- Markdown body with structured sections
- Each skill is self-contained in its directory
- No external dependencies required to understand the skill
