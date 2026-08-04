# Community Skill Harvesting — Known Source Definitions

This reference documents the source definitions and path mappings for the 6 community repos harvested into LoopyLuci/Skills.

## Source Map

```python
SOURCES = {
    "mattpocock/skills": {
        "engineering": ["codebase-design", "code-review", "diagnosing-bugs", "domain-modeling", "implement", "improve-codebase-architecture", "prototype", "research", "resolving-merge-conflicts", "tdd", "to-spec", "to-tickets", "triage", "wayfinder", "ask-matt", "grill-with-docs"],
        "productivity": ["grill-me", "grilling", "handoff", "teach", "writing-great-skills"],
        "misc": ["git-guardrails-claude-code", "setup-pre-commit"],
    },
    "emilkowalski/skills": {
        ".": ["animation-vocabulary", "apple-design", "emil-design-eng", "find-animation-opportunities", "improve-animations", "pick-ui-library", "prototype", "review-animations"],
    },
    "anthropics/skills": {
        ".": ["algorithmic-art", "brand-guidelines", "canvas-design", "claude-api", "doc-coauthoring", "docx", "frontend-design", "internal-comms", "mcp-builder", "pdf", "pptx", "skill-creator", "slack-gif-creator", "theme-factory", "web-artifacts-builder", "webapp-testing", "xlsx"],
    },
    "MiniMax-AI/skills": {
        ".": ["android-native-dev", "buddy-sings", "color-font-skill", "content-page-generator",
              "cover-page-generator", "flutter-dev", "frontend-dev", "fullstack-dev",
              "gif-sticker-maker", "ios-application-dev", "minimax-docx",
              "minimax-multimodal-toolkit", "minimax-music-gen", "minimax-music-playlist",
              "minimax-pdf", "minimax-xlsx", "mmx-cli", "ppt-editing-skill",
              "ppt-orchestra-skill", "pptx-generator", "react-native-dev",
              "section-divider-generator", "shader-dev", "slide-making-skill",
              "summary-page-generator", "table-of-contents-generator", "vision-analysis"],
    },
    "slavingia/skills": {
        ".": ["company-values", "find-community", "first-customers", "grow-sustainably", "marketing-plan", "minimalist-review", "mvp", "pricing", "processize", "validate-idea"],
    },
    "google/skills": {
        "cloud": ["agent-platform-alert-configuration", "agent-platform-deploy", "agent-platform-endpoint-management", "agent-platform-eval-flywheel", "agent-platform-inference", "agent-platform-migrate-from-ai-studio", "agent-platform-model-registry", "agent-platform-prompt-management", "agent-platform-rag-engine-management", "agent-platform-skill-registry", "agent-platform-troubleshooting", "agent-platform-tuning", "alloydb-basics", "bigquery-ai-ml", "bigquery-basics", "bigquery-bigframes", "bigtable-basics", "cloud-run-basics", "cloud-sql-basics", "gcloud", "gemini-agents-api", "gemini-api", "gemini-interactions-api", "gemini-live-api", "gke-app-onboarding", "gke-backup-dr", "gke-basics", "gke-batch-hpc", "gke-cluster-autoscaler", "gke-cluster-creation", "gke-compute-classes", "gke-cost-analysis", "gke-cost-optimization", "gke-golden-path", "gke-inference", "gke-manifest-generation", "gke-multitenancy", "gke-networking", "gke-observability", "gke-platform-security", "gke-productionize", "gke-reliability", "gke-service-networking", "gke-storage", "gke-upgrades", "gke-workload-scaling", "gke-workload-security", "google-cloud-recipe-auth", "google-cloud-recipe-foundation-builder", "google-cloud-recipe-onboarding", "google-cloud-solution-architecture", "google-cloud-storage-basics", "firebase-basics", "workload-manager-basics"],
        "ads": ["google-ads-api-quickstart", "google-ads-api-mcp-setup", "google-ads-api-account-diagnostics", "google-mobile-ads-android-migrate-to-next-gen", "google-mobile-ads-banner", "google-mobile-ads-get-started", "google-mobile-ads-interstitial", "google-mobile-ads-rewarded", "ima-sdk-basics"],
        "analytics": ["google-analytics-admin-api-basics", "google-analytics-data-api-basics"],
    },
}
```

## Path Mappings

### mattpocock/skills
Uses categorized structure: `skills/{category}/{name}/SKILL.md`

```python
MATTPOCOCK_SUBCATS = {
    "ask-matt": "engineering/ask-matt",
    "code-review": "engineering/code-review",
    "codebase-design": "engineering/codebase-design",
    "design-an-interface": "engineering/design-an-interface",
    "diagnosing-bugs": "engineering/diagnosing-bugs",
    "domain-modeling": "engineering/domain-modeling",
    "grill-with-docs": "engineering/grill-with-docs",
    "implement": "engineering/implement",
    "improve-codebase-architecture": "engineering/improve-codebase-architecture",
    "prototype": "engineering/prototype",  # → prototype-solution
    "qa": "engineering/qa",
    "request-refactor-plan": "engineering/request-refactor-plan",
    "research": "engineering/research",
    "resolving-merge-conflicts": "engineering/resolving-merge-conflicts",
    "tdd": "engineering/tdd",
    "to-spec": "engineering/to-spec",
    "to-tickets": "engineering/to-tickets",
    "triage": "engineering/triage",
    "ubiquitous-language": "engineering/ubiquitous-language",
    "wayfinder": "engineering/wayfinder",
    "grill-me": "productivity/grill-me",
    "grilling": "productivity/grilling",
    "handoff": "productivity/handoff",
    "loop-me": "productivity/loop-me",
    "teach": "productivity/teach",
    "writing-great-skills": "productivity/writing-great-skills",
    "git-guardrails-claude-code": "misc/git-guardrails-claude-code",
    "migrate-to-shoehorn": "misc/migrate-to-shoehorn",
    "obsidian-vault": "misc/obsidian-vault",
    "scaffold-exercises": "misc/scaffold-exercises",
    "setup-matt-pocock-skills": "misc/setup-matt-pocock-skills",
    "setup-pre-commit": "misc/setup-pre-commit",
    "setup-ts-deep-modules": "misc/setup-ts-deep-modules",
    "to-questionnaire": "misc/to-questionnaire",
    "wizard": "misc/wizard",
    "writing-beats": "productivity/writing-beats",
    "writing-fragments": "productivity/writing-fragments",
    "writing-shape": "productivity/writing-shape",
}
```

### Others
- **anthropics/skills**: Flat — `skills/{name}/SKILL.md`
- **emilkowalski/skills**: Flat — `skills/{name}/SKILL.md`
- **MiniMax-AI/skills**: Flat — `skills/{name}/SKILL.md`
- **slavingia/skills**: Flat — `skills/{name}/SKILL.md`
- **google/skills**: Categorized — `skills/{cloud|ads|analytics}/{name}/SKILL.md`

## Name Alias Resolution

```python
NAME_ALIASES = {
    "prototype": {"mattpocock/skills": "prototype-solution"},
}

def resolve_name(repo, name):
    if name in NAME_ALIASES and repo in NAME_ALIASES[name]:
        return NAME_ALIASES[name][repo]
    return name
```

## Result Summary

| Source | Skills |
|--------|--------|
| mattpocock/skills | 35 |
| emilkowalski/skills | 7 |
| anthropics/skills | 14 |
| MiniMax-AI/skills | 22 |
| slavingia/skills | 10 |
| google/skills | 67 |
| obra/superpowers | 12 |
| vercel/skills | 1 |
| **Total** | **168** |

## Newly Discovered Sources

### obra/superpowers
Structure: `skills/{name}/SKILL.md`

Skills: brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills

### vercel/skills
Structure: `SKILL.md` in root

Skills: find-skills
