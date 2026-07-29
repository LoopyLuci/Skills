"""
Mass import of skills from community repos into LoopyLuci/Skills.
Fetches SKILL.md from raw.githubusercontent.com, enhances frontmatter, 
and writes to the local repo structure.

Repos to harvest:
  - mattpocock/skills (engineering methodology, productivity)
  - emilkowalski/skills (design/animation) 
  - anthropics/skills (Claude API, document skills)
  - MiniMax-AI/skills (dev tools, shader, music)
  - slavingia/skills (entrepreneurship)
  - google/skills (GCP-specific - subset)
"""

import json
import os
import re
import sys
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

REPO_SKILLS_DIR = Path("D:/Projects/Skills/skills")

# Source definitions: repo -> list of (skill_name, source_path)
# source_path is the path within the repo to the skill directory
SOURCES = {
    "mattpocock/skills": {
        "engineering": [
            "codebase-design", "code-review", "diagnosing-bugs", 
            "domain-modeling", "implement", "improve-codebase-architecture",
            "prototype", "research", "resolving-merge-conflicts",
            "tdd", "to-spec", "to-tickets", "triage", "wayfinder",
            "ask-matt", "grill-with-docs"
        ],
        "productivity": [
            "grill-me", "grilling", "handoff", "teach", "writing-great-skills"
        ],
        "misc": [
            "git-guardrails-claude-code", "setup-pre-commit"
        ],
    },
    "emilkowalski/skills": {
        ".": [
            "animation-vocabulary", "apple-design", "emil-design-eng",
            "find-animation-opportunities", "improve-animations",
            "pick-ui-library", "prototype", "review-animations"
        ]
    },
    "anthropics/skills": {
        ".": [
            "algorithmic-art", "brand-guidelines", "canvas-design",
            "claude-api", "doc-coauthoring", "docx",
            "frontend-design", "internal-comms", "mcp-builder",
            "pdf", "pptx", "skill-creator", "slack-gif-creator",
            "theme-factory", "web-artifacts-builder", "webapp-testing", "xlsx"
        ]
    },
    "MiniMax-AI/skills": {
        ".": [
            "android-native-dev", "buddy-sings", "flutter-dev",
            "frontend-dev", "fullstack-dev", "gif-sticker-maker",
            "ios-application-dev", "minimax-docx", "minimax-multimodal-toolkit",
            "minimax-music-gen", "minimax-music-playlist", "minimax-pdf",
            "minimax-xlsx", "pptx-generator", "react-native-dev",
            "shader-dev", "vision-analysis"
        ]
    },
    "slavingia/skills": {
        ".": [
            "company-values", "find-community", "first-customers",
            "grow-sustainably", "marketing-plan", "minimalist-review",
            "mvp", "pricing", "processize", "validate-idea"
        ]
    },
    "google/skills": {
        "cloud": [
            "agent-platform-alert-configuration", "agent-platform-deploy",
            "agent-platform-endpoint-management", "agent-platform-eval-flywheel",
            "agent-platform-inference", "agent-platform-migrate-from-ai-studio",
            "agent-platform-model-registry", "agent-platform-prompt-management",
            "agent-platform-rag-engine-management", "agent-platform-skill-registry",
            "agent-platform-troubleshooting", "agent-platform-tuning",
            "alloydb-basics", "bigquery-ai-ml", "bigquery-basics",
            "bigquery-bigframes", "bigtable-basics",
            "cloud-run-basics", "cloud-sql-basics",
            "gcloud", "gemini-agents-api", "gemini-api",
            "gemini-interactions-api", "gemini-live-api",
            "gke-app-onboarding", "gke-backup-dr", "gke-basics",
            "gke-batch-hpc", "gke-cluster-autoscaler", "gke-cluster-creation",
            "gke-compute-classes", "gke-cost-analysis", "gke-cost-optimization",
            "gke-golden-path", "gke-inference", "gke-manifest-generation",
            "gke-multitenancy", "gke-networking", "gke-observability",
            "gke-platform-security", "gke-productionize", "gke-reliability",
            "gke-service-networking", "gke-storage", "gke-upgrades",
            "gke-workload-scaling", "gke-workload-security",
            "google-cloud-recipe-auth", "google-cloud-recipe-foundation-builder",
            "google-cloud-recipe-onboarding", "google-cloud-solution-architecture",
            "google-cloud-storage-basics",
            "firebase-basics", "workload-manager-basics"
        ],
        "ads": [
            "google-ads-api-quickstart", "google-ads-api-mcp-setup",
            "google-ads-api-account-diagnostics",
            "google-mobile-ads-banner", "google-mobile-ads-interstitial",
            "google-mobile-ads-rewarded", "ima-sdk-basics"
        ],
        "analytics": [
            "google-analytics-admin-api-basics", "google-analytics-data-api-basics"
        ]
    }
}

# Also fetch from subdirectories for mattpocock
MATTPOCOCK_SUBCATS = {
    "ask-matt": "engineering/ask-matt",
    "code-review": "engineering/code-review",
    "codebase-design": "engineering/codebase-design", 
    "diagnosing-bugs": "engineering/diagnosing-bugs",
    "domain-modeling": "engineering/domain-modeling",
    "grill-with-docs": "engineering/grill-with-docs",
    "implement": "engineering/implement",
    "improve-codebase-architecture": "engineering/improve-codebase-architecture",
    "prototype": "engineering/prototype",
    "research": "engineering/research",
    "resolving-merge-conflicts": "engineering/resolving-merge-conflicts",
    "tdd": "engineering/tdd",
    "to-spec": "engineering/to-spec",
    "to-tickets": "engineering/to-tickets",
    "triage": "engineering/triage",
    "wayfinder": "engineering/wayfinder",
    "grill-me": "productivity/grill-me",
    "grilling": "productivity/grilling",
    "handoff": "productivity/handoff",
    "teach": "productivity/teach",
    "writing-great-skills": "productivity/writing-great-skills",
    "git-guardrails-claude-code": "misc/git-guardrails-claude-code",
    "setup-pre-commit": "misc/setup-pre-commit",
}

ANTHROPICS_SKILLS_PATHS = {
    "algorithmic-art": "algorithmic-art",
    "brand-guidelines": "brand-guidelines",
    "canvas-design": "canvas-design",
    "claude-api": "claude-api",
    "doc-coauthoring": "doc-coauthoring",
    "docx": "docx",
    "frontend-design": "frontend-design",
    "internal-comms": "internal-comms",
    "mcp-builder": "mcp-builder",
    "pdf": "pdf",
    "pptx": "pptx",
    "skill-creator": "skill-creator",
    "slack-gif-creator": "slack-gif-creator",
    "theme-factory": "theme-factory",
    "web-artifacts-builder": "web-artifacts-builder",
    "webapp-testing": "webapp-testing",
    "xlsx": "xlsx"
}

def fetch_skill(repo, path, skill_name):
    """Fetch SKILL.md from raw.githubusercontent.com."""
    url = f"https://raw.githubusercontent.com/{repo}/main/skills/{path}/SKILL.md"
    try:
        with urlopen(url, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            if len(content) > 100 and "name:" in content[:200]:
                return content
            else:
                print(f"  ⚠  {skill_name} from {repo}: too short or no frontmatter ({len(content)} bytes)")
                return None
    except HTTPError as e:
        print(f"  ✗  {skill_name} from {repo}: HTTP {e.code} ({url})")
        return None
    except URLError as e:
        print(f"  ✗  {skill_name} from {repo}: {e.reason}")
        return None
    except Exception as e:
        print(f"  ✗  {skill_name} from {repo}: {e}")
        return None

# Tag enhancements based on source
ENHANCEMENTS = {
    # (repo, skill) -> {tags, description_override, enhancements}
    "codebase-design": {
        "tags": ["engineering", "architecture", "design", "module-design"],
        "hermes_tags": ["engineering", "architecture", "design-patterns"],
        "category": "software-development",
        "enhance_note": "Deep module design: a lot of behaviour behind a small interface, placed at a clean seam."
    },
    "code-review": {
        "tags": ["engineering", "code-review", "quality"],
        "hermes_tags": ["engineering", "code-review", "qa"],
        "category": "software-development",
    },
    "handoff": {
        "tags": ["productivity", "handoff", "agent", "context"],
        "hermes_tags": ["productivity", "agent-workflow", "handoff"],
        "category": "productivity",
    },
    "teach": {
        "tags": ["productivity", "teaching", "education"],
        "hermes_tags": ["productivity", "education", "teaching"],
        "category": "productivity",
    },
    "writing-great-skills": {
        "tags": ["skills", "authoring", "meta"],
        "hermes_tags": ["skills", "authoring", "meta-skills"],
        "category": "software-development",
    },
    "emil-design-eng": {
        "tags": ["design", "animation", "ui", "ux"],
        "hermes_tags": ["design", "animation", "ui-ux", "frontend"],
        "category": "creative",
    },
    "apple-design": {
        "tags": ["design", "apple", "animation", "hci"],
        "hermes_tags": ["design", "apple", "hci", "animation"],
        "category": "creative",
    },
    "prototype": {  # from emil
        "tags": ["design", "prototype", "ui"],
        "hermes_tags": ["design", "prototype", "frontend"],
        "category": "creative",
    },
    "claude-api": {
        "tags": ["api", "claude", "anthropic", "llm"],
        "hermes_tags": ["api", "claude", "llm", "documentation"],
        "category": "mlops",
    },
    "mcp-builder": {
        "tags": ["mcp", "server", "tool-building"],
        "hermes_tags": ["mcp", "server", "tools", "integration"],
        "category": "software-development",
    },
}

def enhance_frontmatter(content, skill_name, source_repo):
    """Add Hermes-compatible metadata and ensure proper frontmatter."""
    # Parse existing frontmatter
    has_fm = content.startswith("---")
    if has_fm:
        end = content.find("---", 3)
        if end == -1:
            has_fm = False
            body = content
        else:
            fm = content[3:end]
            body = content[end+3:]
    else:
        fm = ""
        body = content
    
    # Extract existing fields if any
    existing_name = ""
    existing_desc = ""
    existing_tags = []
    
    for line in fm.split("\n"):
        line = line.strip()
        if line.startswith("name:"):
            existing_name = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            existing_desc = line.split(":", 1)[1].strip().strip('"').strip("'")
    
    # Build new frontmatter
    enh = ENHANCEMENTS.get(skill_name, {})
    target_name = existing_name or skill_name
    source_note = f"[Imported from {source_repo}]"
    
    new_fm = f"""---
name: {target_name}
description: {existing_desc if existing_desc else f'{source_note} {enh.get("enhance_note", "")}'}
source: {source_repo}
tags: [{', '.join(enh.get('tags', ['agent', 'skill']))}]
metadata:
  hermes:
    tags: [{', '.join(enh.get('hermes_tags', ['agent', 'skill']))}]
---
"""
    
    # Clean body - remove any leading whitespace
    body = body.strip()
    
    return new_fm + "\n\n" + body

def import_source(source_def, repo_name):
    """Import all skills from one source."""
    imported = 0
    skipped = 0
    errors = 0
    
    for category, skills in source_def.items():
        for skill_name in skills:
            target_dir = REPO_SKILLS_DIR / skill_name
            target_file = target_dir / "SKILL.md"
            
            # Skip if already exists
            if target_file.exists():
                skipped += 1
                continue
            
            # Determine the path within the repo
            if repo_name == "mattpocock/skills":
                path = MATTPOCOCK_SUBCATS.get(skill_name, f"{category}/{skill_name}")
            elif repo_name == "anthropics/skills":
                path = ANTHROPICS_SKILLS_PATHS.get(skill_name, skill_name)
            elif repo_name == "google/skills":
                path = f"{category}/{skill_name}"
            else:
                path = f"{category}/{skill_name}" if category != "." else skill_name
            
            # Fetch the SKILL.md
            content = fetch_skill(repo_name, path, skill_name)
            if not content:
                errors += 1
                continue
            
            # Enhance frontmatter
            enhanced = enhance_frontmatter(content, skill_name, repo_name)
            
            # Write to target
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file.write_text(enhanced, encoding="utf-8")
            
            # Also fetch supporting files if the skill references directories
            for subdir in ["references", "templates", "scripts", "assets", "examples"]:
                sub_url = f"https://api.github.com/repos/{repo_name}/contents/skills/{path}/{subdir}"
                try:
                    with urlopen(sub_url, timeout=10) as resp:
                        listing = json.loads(resp.read())
                        # Has at least one file in this subdir
                        if isinstance(listing, list):
                            sub_target = target_dir / subdir
                            sub_target.mkdir(exist_ok=True)
                            for entry in listing:
                                if entry["type"] == "file" and entry["name"] != "SKILL.md":
                                    # Download the supporting file
                                    file_url = entry["download_url"]
                                    try:
                                        with urlopen(file_url, timeout=15) as fresp:
                                            fcontent = fresp.read()
                                            (sub_target / entry["name"]).write_bytes(fcontent)
                                    except:
                                        pass
                except (HTTPError, URLError, json.JSONDecodeError):
                    pass  # No supporting files, that's fine
            
            imported += 1
            print(f"  ✓  {skill_name} imported from {repo_name}")
    
    return imported, skipped, errors


def check_existing_skills():
    """Check which skills already exist in the repo."""
    existing = set()
    for d in REPO_SKILLS_DIR.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            existing.add(d.name)
    return existing


def main():
    print("=" * 60)
    print("MASS SKILL IMPORT FROM COMMUNITY REPOS")
    print("=" * 60)
    
    existing = check_existing_skills()
    print(f"\nExisting skills in repo: {len(existing)}")
    
    total_imported = 0
    total_skipped = 0
    total_errors = 0
    
    for repo_name, source_def in SOURCES.items():
        print(f"\n--- {repo_name} ---")
        imported, skipped, errors = import_source(source_def, repo_name)
        total_imported += imported
        total_skipped += skipped
        total_errors += errors
        print(f"  → {imported} imported, {skipped} already exist, {errors} errors")
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {total_imported} new skills imported")
    print(f"       {total_skipped} skills skipped (already exist)")
    print(f"       {total_errors} errors")
    print("=" * 60)


if __name__ == "__main__":
    main()
