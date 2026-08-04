#!/usr/bin/env python3
"""
import_community_skills.py — Bulk import SKILL.md files from community GitHub repos.

Usage:
  python scripts/import_community_skills.py

Sources defined in references/source-definitions.md.
Configuration constants in the script itself (SOURCES, MATTPOCOCK_SUBCATS, etc.).
"""
import json, os, re, sys, shutil
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# ---- Configuration ----
REPO_SKILLS_DIR = Path("skills")  # relative to repo root
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# Source definitions (see references/source-definitions.md for full listing)
SOURCES = {
    "mattpocock/skills": {
        "engineering": ["codebase-design", "code-review", "diagnosing-bugs",
            "domain-modeling", "implement", "improve-codebase-architecture",
            "prototype", "research", "resolving-merge-conflicts",
            "tdd", "to-spec", "to-tickets", "triage", "wayfinder",
            "ask-matt", "grill-with-docs"],
        "productivity": ["grill-me", "grilling", "handoff", "teach",
            "writing-great-skills"],
        "misc": ["git-guardrails-claude-code", "setup-pre-commit"],
    },
    "emilkowalski/skills": {".": [
        "animation-vocabulary", "apple-design", "emil-design-eng",
        "find-animation-opportunities", "improve-animations",
        "pick-ui-library", "prototype", "review-animations"]},
    "anthropics/skills": {".": [
        "algorithmic-art", "brand-guidelines", "canvas-design",
        "claude-api", "doc-coauthoring", "docx", "frontend-design",
        "internal-comms", "mcp-builder", "pdf", "pptx", "skill-creator",
        "slack-gif-creator", "theme-factory", "web-artifacts-builder",
        "webapp-testing", "xlsx"]},
    "MiniMax-AI/skills": {".": [
        "android-native-dev", "buddy-sings", "flutter-dev",
        "frontend-dev", "fullstack-dev", "gif-sticker-maker",
        "ios-application-dev", "minimax-docx", "minimax-multimodal-toolkit",
        "minimax-music-gen", "minimax-music-playlist", "minimax-pdf",
        "minimax-xlsx", "pptx-generator", "react-native-dev",
        "shader-dev", "vision-analysis"]},
    "slavingia/skills": {".": [
        "company-values", "find-community", "first-customers",
        "grow-sustainably", "marketing-plan", "minimalist-review",
        "mvp", "pricing", "processize", "validate-idea"]},
    "google/skills": {"cloud": [
        "agent-platform-alert-configuration", "agent-platform-deploy",
        "agent-platform-endpoint-management",
        "agent-platform-eval-flywheel", "agent-platform-inference",
        "agent-platform-migrate-from-ai-studio",
        "agent-platform-model-registry",
        "agent-platform-prompt-management",
        "agent-platform-rag-engine-management",
        "agent-platform-skill-registry",
        "agent-platform-troubleshooting", "agent-platform-tuning",
        "alloydb-basics", "bigquery-ai-ml", "bigquery-basics",
        "bigquery-bigframes", "bigtable-basics", "cloud-run-basics",
        "cloud-sql-basics", "gcloud", "gemini-agents-api", "gemini-api",
        "gemini-interactions-api", "gemini-live-api",
        "gke-app-onboarding", "gke-backup-dr", "gke-basics",
        "gke-batch-hpc", "gke-cluster-autoscaler",
        "gke-cluster-creation", "gke-compute-classes",
        "gke-cost-analysis", "gke-cost-optimization",
        "gke-golden-path", "gke-inference", "gke-manifest-generation",
        "gke-multitenancy", "gke-networking", "gke-observability",
        "gke-platform-security", "gke-productionize",
        "gke-reliability", "gke-service-networking", "gke-storage",
        "gke-upgrades", "gke-workload-scaling",
        "gke-workload-security", "google-cloud-recipe-auth",
        "google-cloud-recipe-foundation-builder",
        "google-cloud-recipe-onboarding",
        "google-cloud-solution-architecture",
        "google-cloud-storage-basics", "firebase-basics",
        "workload-manager-basics"],
        "ads": ["google-ads-api-quickstart", "google-ads-api-mcp-setup",
            "google-ads-api-account-diagnostics",
            "google-mobile-ads-banner",
            "google-mobile-ads-interstitial",
            "google-mobile-ads-rewarded", "ima-sdk-basics"],
        "analytics": ["google-analytics-admin-api-basics",
            "google-analytics-data-api-basics"],
    },
}

# Special path mappings for repos with non-flat structures
MATTPOCOCK_SUBCATS = {k: f"{cat}/{k}" for cat, skills in {
    "engineering": ["ask-matt","code-review","codebase-design","diagnosing-bugs",
        "domain-modeling","grill-with-docs","implement",
        "improve-codebase-architecture","prototype","research",
        "resolving-merge-conflicts","tdd","to-spec","to-tickets",
        "triage","wayfinder"],
    "productivity": ["grill-me","grilling","handoff","teach",
        "writing-great-skills"],
    "misc": ["git-guardrails-claude-code","setup-pre-commit"],
}.items() for k in skills}

ANTHROPICS_PATHS = {k: k for k in [
    "algorithmic-art","brand-guidelines","canvas-design","claude-api",
    "doc-coauthoring","docx","frontend-design","internal-comms",
    "mcp-builder","pdf","pptx","skill-creator","slack-gif-creator",
    "theme-factory","web-artifacts-builder","webapp-testing","xlsx"]}

NAME_ALIASES = {"prototype": {"mattpocock/skills": "prototype-solution"}}

SUPPORTING_DIRS = ["references", "templates", "scripts", "assets", "examples"]

def fetch_text(url):
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8")

def fetch_binary(url):
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=15) as r:
        return r.read()

def fetch_skill(repo, path, name):
    url = f"https://raw.githubusercontent.com/{repo}/main/skills/{path}/SKILL.md"
    content = fetch_text(url)
    if len(content) < 100 or "name:" not in content[:200]:
        return None
    return content

def resolve_name(repo, name):
    return NAME_ALIASES.get(name, {}).get(repo, name)

def import_skills(dry_run=True):
    imported = 0
    skipped = 0
    errors = 0
    total = sum(len(skills) for cats in SOURCES.values() for skills in cats.values())
    n = 0

    for repo, cats in SOURCES.items():
        for cat, skills in cats.items():
            for name in skills:
                n += 1
                mapped = resolve_name(repo, name)
                target = REPO_SKILLS_DIR / mapped
                sk = target / "SKILL.md"

                if sk.exists():
                    skipped += 1
                    continue

                # Determine repo path
                if repo == "mattpocock/skills":
                    path = MATTPOCOCK_SUBCATS.get(name, f"{cat}/{name}")
                elif repo == "anthropics/skills":
                    path = ANTHROPICS_PATHS.get(name, name)
                elif repo == "google/skills":
                    path = f"{cat}/{name}"
                else:
                    path = f"{cat}/{name}" if cat != "." else name

                content = fetch_skill(repo, path, name)
                if not content:
                    errors += 1
                    continue

                # Enhance frontmatter
                source_tag = f"source: {repo}"
                if "source:" not in content[:300]:
                    content = content.rstrip() + f"\n{source_tag}\n"

                target.mkdir(parents=True, exist_ok=True)
                sk.write_text(content, encoding="utf-8")

                # Supporting files
                for sub in SUPPORTING_DIRS:
                    sub_url = f"https://api.github.com/repos/{repo}/contents/skills/{path}/{sub}"
                    try:
                        req = Request(sub_url, headers=HEADERS)
                        with urlopen(req, timeout=10) as r:
                            entries = json.loads(r.read())
                        if isinstance(entries, list):
                            tgt_sub = target / sub
                            tgt_sub.mkdir(exist_ok=True)
                            for e in entries:
                                if e["type"] == "file" and e["name"] != "SKILL.md":
                                    data = fetch_binary(e["download_url"])
                                    (tgt_sub / e["name"]).write_bytes(data)
                    except (HTTPError, URLError, json.JSONDecodeError):
                        pass

                imported += 1
                print(f"  [{n}/{total}] ✓ {mapped} from {repo}")

    print(f"\nResult: {imported} imported, {skipped} skipped, {errors} errors")
    return imported, skipped, errors

if __name__ == "__main__":
    dry = "--apply" not in sys.argv
    if dry:
        print("Dry-run mode. Run with --apply to execute.")
    import_skills(dry_run=dry)
