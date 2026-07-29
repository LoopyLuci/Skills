# ============================================================
# GENERIC ENHANCEMENTS FOR REMAINING IMPORTED SKILLS
# Auto-generated based on skill name patterns
# ============================================================

def _add_generic_enhancements():
    """Generate generic enhancement entries for imported skills without custom entries."""
    generic = {}
    
    # Agent Platform skills
    for name in ["agent-platform-alert-configuration", "agent-platform-deploy", 
                  "agent-platform-endpoint-management", "agent-platform-eval-flywheel",
                  "agent-platform-inference", "agent-platform-migrate-from-ai-studio",
                  "agent-platform-model-registry", "agent-platform-prompt-management",
                  "agent-platform-rag-engine-management", "agent-platform-skill-registry",
                  "agent-platform-troubleshooting", "agent-platform-tuning"]:
        topic = name.replace("agent-platform-", "").replace("-", " ").title()
        generic[name] = {
            "hermes_tags": ["gcp", "agent-platform", "google-cloud", "ai-platform"],
            "trigger": f"**Trigger**: Use when managing {topic} on Google Cloud's Agent Platform — Google Cloud AI and agent infrastructure.",
        }
    
    # GKE skills
    for name in ["gke-ai-troubleshooting-handle-disruption-gpu-tpu", "gke-app-onboarding",
                  "gke-backup-dr", "gke-batch-hpc", "gke-cluster-autoscaler",
                  "gke-cluster-creation", "gke-compute-classes", "gke-cost-analysis",
                  "gke-cost-optimization", "gke-golden-path", "gke-inference",
                  "gke-manifest-generation", "gke-multitenancy", "gke-networking",
                  "gke-observability", "gke-platform-security", "gke-productionize",
                  "gke-reliability", "gke-service-networking", "gke-storage",
                  "gke-upgrades", "gke-workload-scaling", "gke-workload-security"]:
        topic = name.replace("gke-", "").replace("-", " ").title()
        generic[name] = {
            "hermes_tags": ["gcp", "gke", "kubernetes", "google-cloud", "container"],
            "trigger": f"**Trigger**: Use when working with GKE {topic} — Google Kubernetes Engine configuration and management.",
        }
    
    # Google Cloud basics
    for name in ["alloydb-basics", "bigquery-ai-ml", "bigquery-bigframes",
                  "bigtable-basics", "cloud-sql-basics",
                  "google-cloud-recipe-auth", "google-cloud-recipe-foundation-builder",
                  "google-cloud-recipe-onboarding", "google-cloud-solution-architecture",
                  "google-cloud-storage-basics", "workload-manager-basics",
                  "google-analytics-admin-api-basics", "google-analytics-data-api-basics"]:
        topic = name.replace("-basics", "").replace("-", " ").title()
        hermes_key = "cloud" if "cloud" in name else name.split("-")[0]
        generic[name] = {
            "hermes_tags": ["gcp", "google-cloud", hermes_key],
            "trigger": f"**Trigger**: Use when working with Google Cloud {topic} — setup, configuration, and best practices.",
        }
    
    # Google Ads / Mobile Ads
    for name in ["google-ads-api-account-diagnostics", "google-ads-api-mcp-setup",
                  "google-ads-api-quickstart", "google-mobile-ads-banner",
                  "google-mobile-ads-interstitial", "google-mobile-ads-rewarded",
                  "ima-sdk-basics"]:
        topic = name.replace("google-ads-", "").replace("google-mobile-ads-", "").replace("ima-sdk-", "").replace("-basics", "").replace("-", " ").title()
        generic[name] = {
            "hermes_tags": ["google-ads", "advertising", "mobile-ads", "gcp"],
            "trigger": f"**Trigger**: Use when implementing Google {topic} — AdMob, Ad Manager, and related ad SDKs.",
        }
    
    # Gemini APIs
    for name in ["gemini-agents-api", "gemini-interactions-api", "gemini-live-api"]:
        topic = name.replace("gemini-", "").replace("-", " ").title()
        generic[name] = {
            "hermes_tags": ["gcp", "gemini", "google-ai", "api"],
            "trigger": f"**Trigger**: Use when working with the Gemini {topic} — Google's multimodal AI API.",
        }
    
    # MiniMax remaining
    generic["fullstack-dev"] = {
        "hermes_tags": ["fullstack", "web", "backend", "api", "frontend"],
        "trigger": "**Trigger**: Use when developing full-stack web applications — backend architecture, API design, auth flows, database integration, and production deployment.",
        "procedure_steps": [
            "Review requirements and design the overall architecture — frontend, backend, database, and API contracts.",
            "Design the data model and database schema — entities, relationships, indexes.",
            "Implement the backend API — REST endpoints, auth (JWT/OAuth/session), middleware, error handling.",
            "Implement real-time features if needed — SSE, WebSocket, or polling.",
            "Integrate the frontend with the backend — API clients, state management, error states.",
            "Apply production hardening — logging, monitoring, error tracking, rate limiting, security headers.",
        ],
        "pitfalls": [
            "Missing API contracts: define request/response shapes before writing frontend or backend code.",
            "CORS misconfiguration: CORS errors appear in the browser, not the server — test early.",
            "No migration strategy: schema changes without a plan block the entire team.",
        ],
        "verification": [
            "Can the frontend and backend communicate without CORS or auth errors?",
            "Are all API endpoints documented (OpenAPI or similar)?",
            "Is there a database migration script checked into version control?",
        ],
    }
    
    # MiniMax Office format skills
    for name in ["minimax-docx", "minimax-pdf", "minimax-xlsx"]:
        fmt = name.replace("minimax-", "").upper()
        generic[name] = {
            "hermes_tags": ["minimax", "document", fmt.lower(), "office"],
            "trigger": f"**Trigger**: Use when creating, editing, or formatting {fmt} documents — generation, template application, content extraction, and validation.",
        }
    
    generic["minimax-multimodal-toolkit"] = {
        "hermes_tags": ["minimax", "multimodal", "tts", "music", "video", "image"],
        "trigger": "**Trigger**: Use when generating multimodal content via MiniMax APIs — text-to-speech, music, video, and image generation.",
    }
    generic["minimax-music-playlist"] = {
        "hermes_tags": ["minimax", "music", "playlist", "audio", "generation"],
        "trigger": "**Trigger**: Use when generating personalized music playlists — analyzing music taste, planning tracklists, and generating songs with cover art.",
    }
    
    # mattpocock remaining
    generic["diagnosing-bugs"] = {
        "hermes_tags": ["engineering", "debugging", "bug-hunting", "testing"],
        "trigger": "**Trigger**: Use when diagnosing and reproducing bugs — systematic approach to finding root causes through hypothesis testing and minimal reproductions.",
        "procedure_steps": [
            "Reproduce the bug consistently — identify the exact steps, inputs, and environment conditions.",
            "Narrow the scope — binary search through commits (git bisect), config options, or input parameters.",
            "Form a hypothesis about the root cause — the mechanism, not just the symptom.",
            "Write a minimal reproduction — the smallest code/config that still exhibits the bug.",
            "Fix at the root cause level — not just the symptom — and verify the fix with the reproduction case.",
        ],
        "pitfalls": [
            "Fixing symptoms instead of cause: a 'fix' that doesn't address the root cause will regress.",
            "Incomplete reproduction: a bug you can't consistently reproduce is a bug you can't verify as fixed.",
            "Confirmation bias: don't stop at the first hypothesis that seems plausible — disprove alternatives.",
        ],
        "verification": [
            "Does the fix survive the reproduction case (before-and-after test)?",
            "Are there regression tests covering the fix?",
            "Was the root cause identified, not just the immediate failure?",
        ],
    }
    generic["resolving-merge-conflicts"] = {
        "hermes_tags": ["engineering", "git", "merge", "conflict-resolution"],
        "trigger": "**Trigger**: Use when resolving in-progress git merge or rebase conflicts — understand each side's intent and finish the operation without aborting.",
    }
    generic["setup-pre-commit"] = {
        "hermes_tags": ["engineering", "git", "hooks", "pre-commit", "automation"],
        "trigger": "**Trigger**: Use when setting up pre-commit hooks for a project — linting, formatting, type-checking, and security scanning before every commit.",
    }
    generic["tdd"] = {
        "hermes_tags": ["engineering", "testing", "tdd", "quality"],
        "trigger": "**Trigger**: Use when developing features using test-driven development — red-green-refactor cycle, building one vertical slice at a time.",
    }
    generic["to-spec"] = {
        "hermes_tags": ["engineering", "specification", "planning", "prd"],
        "trigger": "**Trigger**: Use when creating a specification document (PRD) for a feature or project — structured planning before implementation.",
    }
    generic["to-tickets"] = {
        "hermes_tags": ["engineering", "tickets", "planning", "issues", "agile"],
        "trigger": "**Trigger**: Use when breaking a specification into actionable tickets or issues — creating a set of tickets that each declare their blocking dependencies.",
    }
    generic["triage"] = {
        "hermes_tags": ["engineering", "triage", "bugs", "prioritization"],
        "trigger": "**Trigger**: Use when triaging bugs, issues, or feature requests — categorizing, prioritizing, and assigning based on severity and impact.",
    }
    generic["wayfinder"] = {
        "hermes_tags": ["engineering", "navigation", "codebase", "exploration"],
        "trigger": "**Trigger**: Use when navigating an unfamiliar codebase — mapping the structure, understanding the architecture, and finding where changes should land.",
    }
    generic["git-guardrails-claude-code"] = {
        "hermes_tags": ["engineering", "git", "claude-code", "safety", "guardrails"],
        "trigger": "**Trigger**: Use when configuring git guardrails for Claude Code or other AI coding agents — preventing accidental commits, force-pushes, or destructive operations.",
    }
    generic["grill-with-docs"] = {
        "hermes_tags": ["engineering", "planning", "research", "documentation"],
        "trigger": "**Trigger**: Use when you need to grill a plan or design using documentation as the source of truth — interview the user relentlessly about a decision using reference docs.",
    }
    generic["ask-matt"] = {
        "hermes_tags": ["engineering", "guidance", "mattpocock", "best-practices"],
        "trigger": "**Trigger**: Use when asking Matt Pocock's expertise — TypeScript, React, testing, and TypeScript-adjacent topics.",
    }
    generic["improve-codebase-architecture"] = {
        "hermes_tags": ["engineering", "architecture", "refactoring", "code-quality"],
        "trigger": "**Trigger**: Use when scanning a codebase to improve its architecture — finding deeply entrenched issues, YAGNI violations, and structural improvements scoped to where change is landing.",
    }
    generic["research"] = {
        "hermes_tags": ["engineering", "research", "investigation", "learning"],
        "trigger": "**Trigger**: Use when researching a topic, library, or approach — systematic investigation with documented findings.",
    }
    generic["prototype-solution"] = {
        "hermes_tags": ["engineering", "prototype", "experimentation", "validation"],
        "trigger": "**Trigger**: Use when building a quick prototype to validate a technical approach or design decision — throwaway code to reduce risk before committing to an implementation.",
    }
    
    # No custom entries needed for docx/pdf from anthropics (already have minimax variants)
    # They overlap with our existing skills
    
    return generic

# Merge generic enhancements into the main ENHANCEMENTS dict
# This runs at module import time
for k, v in _add_generic_enhancements().items():
    if k not in ENHANCEMENTS:
        ENHANCEMENTS[k] = v
