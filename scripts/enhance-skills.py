"""
Enhance imported community skills with full Hermes format:
  - YAML frontmatter (name, description, tags, metadata.hermes tags)
  - Trigger/when-to-use section
  - Numbered procedures
  - Pitfalls section
  - Verification section
  - Consistent structure: Trigger -> Procedure -> Pitfalls -> Verification
"""

import re
import json
from pathlib import Path

REPO_SKILLS_DIR = Path("D:/Projects/Skills/skills")

# Skills that were imported from community repos (target list for enhancement)
IMPORTED_SKILLS = set()
with open(Path("D:/Projects/Skills/scripts/imported-skill-names.txt"), "w") as f:
    pass  # will be populated below

# ============================================================
# ENHANCEMENT DEFINITIONS
# One entry per skill with content improvements.
# Fields: trigger, procedure_steps, pitfalls, verification, tags, hermes_tags
# ============================================================

ENHANCEMENTS = {
    "handoff": {
        "tags": ["productivity", "agent-workflow", "handoff", "context"],
        "hermes_tags": ["productivity", "agent-workflow", "handoff", "collaboration"],
        "trigger": "**Trigger**: Use when you need to compact the current conversation into a handoff document so another agent or session can continue the work without losing context.",
        "procedure_steps": [
            "Scan the conversation history and extract: current goal, completed work, decisions made, open questions, and next steps.",
            "Identify key files and directories modified — include their paths and a summary of changes.",
            "Identify unresolved issues, blockers, and partial work.",
            "Write the handoff document to a file using a structured format: `## Goal`, `## Progress`, `## Decisions`, `## Next Steps`, `## Open Questions`, `## Files Touched`.",
            "Optionally include exact commands, API keys to re-export, or environment state needed to resume.",
        ],
        "pitfalls": [
            "Over-sharing context: include only what the next session needs, not the entire transcript.",
            "Ambiguous next steps: be specific about what the next agent should do first.",
            "Missing dependency context: if you installed tools or set env vars, include the commands.",
        ],
        "verification": [
            "Can another agent pick up the handoff and start working within 2 turns?",
            "Are all file paths absolute or relative-to-project-root?",
            "Does the handoff document fit in a single screen?",
        ],
    },
    "teach": {
        "tags": ["productivity", "teaching", "education", "mentoring"],
        "hermes_tags": ["productivity", "education", "teaching", "mentoring"],
        "trigger": "**Trigger**: Use when teaching a user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.",
        "procedure_steps": [
            "Assess the user's current knowledge level — ask what they already know about the topic.",
            "Break the topic into digestible lessons, each building on the previous one.",
            "For each lesson: explain the concept, show a concrete example, then have the user practice.",
            "Create a teaching workspace file (`.teaching-session.json`) to track progress across sessions.",
            "After each session, save progress and set clear expectations for the next session.",
            "Provide spaced-repetition review prompts from previous lessons.",
        ],
        "pitfalls": [
            "Overloading: limit each session to 1-2 concepts to avoid cognitive overload.",
            "Assuming knowledge: ask before diving in — don't skip fundamentals.",
            "No practice: theory without practice doesn't stick — always include exercises.",
        ],
        "verification": [
            "Can the user explain the concept back in their own words?",
            "Did the user complete the practice exercise without hints?",
            "Review saved `.teaching-session.json` — progress should be incrementing.",
        ],
    },
    "writing-great-skills": {
        "tags": ["skills", "authoring", "meta", "documentation"],
        "hermes_tags": ["skills", "authoring", "meta", "best-practices"],
        "trigger": "**Trigger**: Use when writing or editing a skill file (SKILL.md). Reference for the vocabulary and principles that make a skill predictable, useful, and reusable.",
        "procedure_steps": [
            "Start with YAML frontmatter: `name`, `description` (≤60 chars), `tags`, optional `version` and `metadata.hermes.tags`.",
            "Write a `## When to Use` or `**Trigger**` line as the first body content — this tells the agent exactly when to load this skill.",
            "Organize body sections in consistent order: When to Use → Procedure → Examples → Pitfalls → Verification.",
            "Write procedures as numbered steps that the agent can execute without ambiguity.",
            "Include concrete command examples that the agent can copy-paste.",
            "Add a Pitfalls section documenting known failure modes — this is the most valuable part for an agent.",
            "Add a Verification section with commands or checks the agent can run to confirm success.",
            "Keep descriptions under 60 characters for proper system-prompt indexing.",
        ],
        "pitfalls": [
            "Vague triggers: 'Use when needed' is useless — be specific about the condition.",
            "Missing frontmatter: skills without `name:` don't appear in the agent's skill list.",
            "No verification: the agent can't confirm the skill worked without explicit checks.",
            "Over-long descriptions: truncated at 57 chars in the system prompt — keep the trigger in the first 57 characters.",
        ],
        "verification": [
            "Does the skill have valid YAML frontmatter with `name:` and `description:`?",
            "Is there a clear trigger condition in the first paragraph?",
            "Are there numbered procedure steps the agent can follow?",
            "Is there a Pitfalls section with at least 3 items?",
        ],
    },
    "codebase-design": {
        "tags": ["engineering", "architecture", "design", "modules"],
        "hermes_tags": ["engineering", "architecture", "design-patterns", "refactoring"],
        "trigger": "**Trigger**: Use when designing a module's interface, finding deepening opportunities, deciding where a seam goes, or making code more testable and AI-navigable. Shared vocabulary for designing deep modules: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface.",
        "procedure_steps": [
            "Identify the module boundary — what is the single responsibility of this module?",
            "Design the public interface: the smallest surface area that exposes the full capability.",
            "Push complexity behind the interface — the implementation should be deeper than the API suggests (the 'deep module' principle).",
            "Place the module at a clean seam in the codebase — a natural boundary between concerns.",
            "Make the module testable through its public interface alone — no internal state inspection needed.",
            "Document the seam decision: why this boundary, what lives on each side, what was rejected.",
        ],
        "pitfalls": [
            "Leaky abstractions: avoid exposing implementation details in the interface.",
            "Premature deepening: don't add complexity before the interface is stable.",
            "Seam misplacement: a seam in the wrong place causes more coupling, not less.",
        ],
        "verification": [
            "Can you change the implementation without changing the interface?",
            "Can you test every behaviour through the public API alone?",
            "Is the interface file shorter than the implementation file? (deep module heuristic)",
        ],
    },
    "domain-modeling": {
        "tags": ["engineering", "architecture", "domain-modeling", "ddd"],
        "hermes_tags": ["engineering", "architecture", "domain-modeling", "ddd"],
        "trigger": "**Trigger**: Use when actively building or sharpening a project's domain model — challenge terms against the glossary, stress-test with edge-case scenarios, and update `CONTEXT.md` and ADRs inline.",
        "procedure_steps": [
            "Extract the key domain terms from the conversation or codebase and define them precisely.",
            "Create or update a project glossary — a `CONTEXT.md` or `glossary.md` file that defines every term.",
            "Stress-test each term with edge cases: what happens when this term means something slightly different?",
            "Check for synonyms — two terms that mean the same thing, or one term that means two things.",
            "Record Architectural Decision Records (ADRs) for each domain-modeling decision.",
            "Cross-reference the glossary with the code — do the class/variable names match the domain terms?",
        ],
        "pitfalls": [
            "Ubiquitous language drift: if code uses different terms than the glossary, the model has decayed.",
            "Over-modeling: not every concept needs to be in the domain model — focus on the core subdomain.",
            "Glossary rot: a glossary nobody reads is worse than no glossary at all.",
        ],
        "verification": [
            "Can you explain the core domain in 3 sentences using only glossary terms?",
            "Do the class names in the model package match the glossary entries?",
            "If you changed a glossary term, how many files would need updating?",
        ],
    },
    "emil-design-eng": {
        "tags": ["design", "animation", "ui", "ux", "frontend"],
        "hermes_tags": ["design", "animation", "ui-ux", "frontend", "motion"],
        "trigger": "**Trigger**: Use when designing user interfaces with a focus on animation quality, motion design, and polished interactions. Covers animation principles, easing, layout, color, typography, and interaction design for the web.",
        "procedure_steps": [
            "Analyze the current UI and identify which elements could benefit from motion.",
            "Choose the right easing curve: use `ease-out` for enter animations, `ease-in-out` for transitional elements, never use `ease-in` for enter animations.",
            "Pick appropriate durations: micro-interactions 100-200ms, element transitions 200-500ms, page transitions 300-500ms.",
            "Use consistent timing across similar elements — different durations for the same type of animation feel jarring.",
            "Layer animations with staggered delays rather than playing everything at once.",
            "Respect user preferences: support `prefers-reduced-motion` and reduce all animations to 50% speed or fade transitions only.",
        ],
        "pitfalls": [
            "Using `ease-in` for enter animations — users perceive it as sluggish. Always prefer `ease-out` for elements appearing.",
            "Animating `width`/`height` instead of `transform` — triggers layout recalculations. Use `scale`/`translate`.",
            "Ignoring accessibility: all animations should respect `prefers-reduced-motion`.",
            "Over-animating: not every element needs motion. Reserve animation for state changes and user feedback.",
        ],
        "verification": [
            "Do all enter animations use `ease-out`?",
            "Are durations grouped consistently (similar elements = similar duration)?",
            "Is there a `@media (prefers-reduced-motion)` fallback?",
            "Open the page with `prefers-reduced-motion: reduce` — is it still usable without motion?",
        ],
    },
    "review-animations": {
        "tags": ["design", "animation", "review", "qa"],
        "hermes_tags": ["design", "animation", "review", "qa", "motion"],
        "trigger": "**Trigger**: Use when reviewing animations in a UI — checking for correct easing, timing, coordination, and accessibility.",
        "procedure_steps": [
            "Check every interactive element's hover/focus/active state — does it have a micro-interaction?",
            "Verify easing curves: enter states should use `ease-out`, exit states should use `ease-in`, transitions should use `ease-in-out`.",
            "Verify timing: micro-interactions 100-200ms, element transitions 200-500ms, page transitions 300-500ms.",
            "Check animation stagger: elements appearing together should have staggered delays (20-50ms apart).",
            "Verify `prefers-reduced-motion` is respected — all animations should degrade gracefully.",
            "Check for layout-triggering animations: `width`/`height`/`top`/`left` changes should use `transform` instead.",
        ],
        "pitfalls": [
            "Missing hover states: interactive elements without hover animations feel dead.",
            "Synchronous animations: everything animating at once is overwhelming — use stagger.",
            "Duration mismatch: a 500ms hover animation feels glacial — keep micro-interactions under 200ms.",
        ],
        "verification": [
            "Does every interactive element have a hover/focus state animation?",
            "Are all enter animations using `ease-out`?",
            "Does the page respect `prefers-reduced-motion`?",
        ],
    },
    "improve-animations": {
        "tags": ["design", "animation", "audit", "optimization"],
        "hermes_tags": ["design", "animation", "audit", "optimization", "motion"],
        "trigger": "**Trigger**: Use when auditing all animations in a codebase — finding opportunities, prioritizing fixes, and creating execution plans.",
        "procedure_steps": [
            "Scan the codebase for animation-related code: CSS transitions/animations, Framer Motion variants, GSAP timelines, WAAPI calls.",
            "For each animation found, evaluate: does it serve a purpose (feedback, state change, delight) or is it decorative?",
            "Create an inventory of all animations with: location, type, duration, easing, trigger, and purpose.",
            "Prioritize fixes: P0 = broken animations, P1 = wrong easing/timing, P2 = missing interactions, P3 = polish.",
            "Generate a self-contained fix plan per priority level — each plan should be executable by an agent.",
        ],
        "pitfalls": [
            "Auditing without prioritizing: a list of 50 animation issues is overwhelming — use triage.",
            "Changing easing without testing: what looks good in dev might feel different in production.",
            "Missing CSS-animated properties: not all animations use JS libraries — check pure CSS too.",
        ],
        "verification": [
            "Is there a complete animation inventory with location, type, and purpose?",
            "Are fixes prioritized (P0-P3)?",
            "Is each fix plan self-contained and executable by an agent?",
        ],
    },
    "find-animation-opportunities": {
        "tags": ["design", "animation", "ux", "discovery"],
        "hermes_tags": ["design", "animation", "ux", "discovery", "motion"],
        "trigger": "**Trigger**: Use when searching a UI for places that would genuinely benefit from motion, while also identifying what NOT to animate.",
        "procedure_steps": [
            "Review every screen/page and identify state transitions: loading → content, empty → full, collapsed → expanded.",
            "Identify feedback opportunities: button clicks, form submissions, drag operations, errors.",
            "Identify spatial navigation: scrolling, carousels, tab switches, accordion toggles.",
            "Flag elements that should NOT be animated: critical alerts, legal text, data-heavy tables, accessibility-focused components.",
            "Rank opportunities: core interaction feedback > state transitions > environmental motion > decorative animation.",
        ],
        "pitfalls": [
            "Animating everything: motion should serve understanding, not distract from it.",
            "Animating loading states that flash by in <100ms — the animation itself becomes the bottleneck.",
            "Animating text-heavy content — animated text reduces readability significantly.",
        ],
        "verification": [
            "Does each animation opportunity serve a clear functional purpose?",
            "Are animations excluded from places where they'd harm usability?",
            "Do the priority rankings align with user impact, not visual flashiness?",
        ],
    },
    "animation-vocabulary": {
        "tags": ["design", "animation", "vocabulary", "communication"],
        "hermes_tags": ["design", "animation", "vocabulary", "communication", "motion"],
        "trigger": "**Trigger**: Use when you need precise animation terminology to communicate effectively with designers, developers, or AI agents about motion design.",
        "procedure_steps": [
            "Use the correct easing name: `ease-out` (deceleration), `ease-in` (acceleration), `ease-in-out` (symmetrical), linear (mechanical).",
            "Name animation types precisely: enter/exit (presence), transition (state change), micro-interaction (feedback), environmental (ambient).",
            "Describe timing with duration + delay: 'fade in over 200ms with 50ms stagger' is precise.",
            "Use standard property terms: `transform: translate`, `opacity`, `scale`, `rotate`, not 'move' or 'shrink'.",
            "Describe animation curves with cubic-bezier approximations: `cubic-bezier(0.16, 1, 0.3, 1)` = aggressive ease-out.",
        ],
        "pitfalls": [
            "Using vague terms like 'smooth animation' — specify the curve, duration, and property.",
            "Confusing 'animation' (declarative, CSS) with 'transition' (state-based) — they have different performance characteristics.",
            "Describing motion in non-visual terms: 'make it pop' is meaningless — use 'scale 1.05 with 150ms ease-out'.",
        ],
        "verification": [
            "Can you describe every animation in 3 precise terms: property, duration, easing?",
            "Does the vocabulary match what CSS/JS libraries expect (ease-out vs 'easing out')?",
        ],
    },
    "pick-ui-library": {
        "tags": ["design", "frontend", "ui-library", "component"],
        "hermes_tags": ["design", "frontend", "ui-library", "component", "selection"],
        "trigger": "**Trigger**: Use when choosing a UI component library for a project. Have your agent pick the right library based on trusted recommendations instead of letting AI hand-roll components or install abandoned packages.",
        "procedure_steps": [
            "Identify the project's framework: React, Vue, Svelte, or framework-agnostic.",
            "Determine the styling approach: CSS modules, Tailwind, styled-components, or vanilla CSS.",
            "Check the project's design system needs: do they need pre-built themes, or are they custom?",
            "Select from trusted libraries based on criteria: npm downloads, GitHub stars, last update, bundle size, accessibility support.",
            "Prefer libraries with built-in accessibility, TypeScript support, and tree-shaking.",
        ],
        "pitfalls": [
            "Hand-rolling components when a battle-tested library exists — toast, modals, tooltips should never be hand-rolled.",
            "Choosing a library with no recent updates (abandoned) — check last commit date.",
            "Installing a UI library with a different styling paradigm than the project uses.",
        ],
        "verification": [
            "Does the selected library have TypeScript definitions?",
            "Was the library updated in the last 6 months?",
            "Is the bundle size compatible with the project's performance budget?",
        ],
    },
    "claude-api": {
        "hermes_tags": ["api", "claude", "anthropic", "llm", "documentation"],
        "trigger": None,  # Already has good trigger
        "procedure_steps": None,
        "pitfalls_extra": [
            "Rate limits: Claude API has tiered rate limits — check your usage tier before production.",
            "Context window: Opus and Sonnet have different context limits — always check the model's max tokens.",
            "Streaming vs non-streaming: streaming is faster for the user but harder to handle errors — implement proper error boundaries.",
        ],
        "verification_extra": [
            "Can you make a successful API call with streaming enabled?",
            "Are you handling API errors (rate limit, auth, context length) gracefully?",
        ],
    },
    "mcp-builder": {
        "hermes_tags": ["mcp", "server", "tools", "integration", "protocol"],
        "trigger": None,  # Already has good trigger
        "procedure_steps": None,
        "pitfalls_extra": [
            "Tool name collisions: MCP tools must have unique names across all connected servers.",
            "Missing error handling: every tool should return structured errors, not throw exceptions.",
            "Resource URI scheme: use consistent URI patterns so clients can discover resources predictably.",
        ],
        "verification_extra": [
            "Does every tool have a description that the LLM can understand?",
            "Are all tool parameters typed with clear descriptions?",
            "Does `mcp list-tools` return all expected tools?",
        ],
    },
    "shader-dev": {
        "hermes_tags": ["shader", "glsl", "graphics", "gpu", "rendering"],
        "trigger": "**Trigger**: Use when developing GLSL shaders — ray marching, signed distance fields (SDFs), procedural generation, particle systems, or post-processing effects for WebGL/ShaderToy.",
        "pitfalls_extra": [
            "Precision qualifiers: always use `highp` where available — `mediump` causes artifacts on some GPUs.",
            "Branching in shaders: GPUs execute both branches — minimize conditionals. Use `mix()` and `step()` instead.",
            "Texture coordinates: WebGL uses bottom-left origin, ShaderToy uses top-left — account for the difference.",
        ],
        "verification_extra": [
            "Does the shader compile without errors on both WebGL1 and WebGL2?",
            "Are there any dynamic branches that could be replaced with math functions?",
            "Does the shader handle the 0-1 UV range correctly?",
        ],
    },
    "gif-sticker-maker": {
        "hermes_tags": ["media", "gif", "sticker", "image", "animation", "minimax"],
        "trigger": "**Trigger**: Use when converting photos of people, pets, objects, or logos into animated GIF stickers with captions and effects using image and video generation AI.",
        "procedure_steps": None,
        "pitfalls_extra": [
            "Image aspect ratio: stickers work best at 1:1 (square) — crop before processing.",
            "File size: GIFs over 15MB may not render on some platforms — optimize frame count and resolution.",
            "Caption readability: light text on light backgrounds is unreadable — always add text shadow or backdrop.",
        ],
        "verification_extra": [
            "Is the output GIF under 15MB?",
            "Is the caption readable against the background?",
            "Does the animation loop cleanly (no jump at loop point)?",
        ],
    },
    "buddy-sings": {
        "hermes_tags": ["fun", "pet", "music", "minimax", "personality"],
        "trigger": "**Trigger**: Use when the user wants their AI pet or buddy to sing a personalized song. Creates a unique vocal identity, gathers conversation context, and generates custom music.",
        "procedure_steps": None,
        "pitfalls_extra": [
            "Content safety: avoid generating songs about copyrighted characters or explicit content.",
            "API quota: music generation uses API credits — inform the user before generating multiple songs.",
            "Voice caching: the vocal identity is cached per pet name — generating a new pet loses the voice.",
        ],
        "verification_extra": [
            "Was a unique vocal identity created for this pet?",
            "Does the song reference the gathered context (conversation topics, recent work)?",
        ],
    },
    "find-community": {
        "hermes_tags": ["business", "entrepreneurship", "community", "product-market-fit"],
        "trigger": "**Trigger**: Use when looking for a business idea or trying to find your community — the first step in the Minimalist Entrepreneur methodology.",
        "procedure_steps": None,
        "pitfalls_extra": [
            "Building for yourself ≠ building for a community — your problem isn't necessarily everyone's problem.",
            "Community size vs engagement: a small engaged community is better than a large passive one.",
        ],
    },
    "validate-idea": {
        "hermes_tags": ["business", "entrepreneurship", "validation", "lean"],
        "trigger": "**Trigger**: Use when testing if a business idea is worth pursuing — before building anything, validate the problem and willingness to pay.",
    },
    "mvp": {
        "hermes_tags": ["business", "entrepreneurship", "mvp", "lean"],
        "trigger": "**Trigger**: Use when ready to build your first product and struggling with scope — define the Minimum Viable Product that solves the core problem.",
    },
    "pricing": {
        "hermes_tags": ["business", "entrepreneurship", "pricing", "monetization"],
        "trigger": "**Trigger**: Use when setting prices for a product or considering price changes — based on The Minimalist Entrepreneur methodology.",
    },
    "marketing-plan": {
        "hermes_tags": ["business", "entrepreneurship", "marketing", "growth"],
        "trigger": "**Trigger**: Use when you have product-market fit and are ready to scale with content marketing.",
    },
    "grow-sustainably": {
        "hermes_tags": ["business", "entrepreneurship", "growth", "sustainability"],
        "trigger": "**Trigger**: Use when making decisions about spending, hiring, or scaling — grow without burning out or going bankrupt.",
    },
    "company-values": {
        "hermes_tags": ["business", "entrepreneurship", "culture", "hiring"],
        "trigger": "**Trigger**: Use when defining company culture, preparing to hire, or making decisions that should align with core values.",
    },
    "minimalist-review": {
        "hermes_tags": ["business", "entrepreneurship", "review", "decision-making"],
        "trigger": "**Trigger**: Use when gut-checking any business decision against the Minimalist Entrepreneur principles.",
    },
    "processize": {
        "hermes_tags": ["business", "entrepreneurship", "process", "delivery"],
        "trigger": "**Trigger**: Use when you have a product idea but want to deliver value by hand before writing any code.",
    },
    "first-customers": {
        "hermes_tags": ["business", "entrepreneurship", "sales", "customers"],
        "trigger": "**Trigger**: Use when you have a product and need to find your first 100 customers — sell one by one.",
    },
    "skill-creator": {
        "hermes_tags": ["skills", "authoring", "anthropic", "claude"],
        "trigger": "**Trigger**: Use when creating custom skills for Claude or any agent-skills-compatible AI assistant. Step-by-step guide for authoring, testing, and distributing skills.",
    },
    "algorithmic-art": {
        "hermes_tags": ["art", "generative", "creative", "canvas", "animation"],
        "trigger": "**Trigger**: Use when generating algorithmic or generative art — creating visual patterns, fractals, geometric designs, or abstract animations through code.",
    },
    "brand-guidelines": {
        "hermes_tags": ["design", "brand", "guidelines", "identity"],
        "trigger": "**Trigger**: Use when creating or applying brand style guidelines — colors, typography, logos, spacing, voice, and visual identity rules.",
    },
    "canvas-design": {
        "hermes_tags": ["design", "canvas", "layout", "composition"],
        "trigger": "**Trigger**: Use when designing canvas-based layouts — web canvas, whiteboard tools, drawing applications, or diagramming interfaces.",
    },
    "frontend-design": {
        "hermes_tags": ["design", "frontend", "ui", "ux", "layout"],
        "trigger": "**Trigger**: Use when designing the frontend UI — layout, component structure, responsive behavior, and visual hierarchy.",
    },
    "theme-factory": {
        "hermes_tags": ["design", "theme", "css", "styling", "brand"],
        "trigger": "**Trigger**: Use when creating, modifying, or applying visual themes — color palettes, typography scales, spacing systems, and CSS design tokens.",
    },
    "webapp-testing": {
        "hermes_tags": ["testing", "webapp", "qa", "automation", "e2e"],
        "trigger": "**Trigger**: Use when testing web applications — manual QA checklists, automated test strategies, cross-browser testing, and accessibility validation.",
    },
    "internal-comms": {
        "hermes_tags": ["communication", "internal", "writing", "announcements"],
        "trigger": "**Trigger**: Use when writing internal communications — company announcements, team updates, memos, and organizational messages.",
    },
    "doc-coauthoring": {
        "hermes_tags": ["writing", "documents", "collaboration", "editing"],
        "trigger": "**Trigger**: Use when co-authoring documents with AI assistance — structuring, drafting, revising, and polishing long-form content.",
    },
    "web-artifacts-builder": {
        "hermes_tags": ["web", "artifacts", "html", "prototype", "demo"],
        "trigger": "**Trigger**: Use when building standalone web artifacts — HTML pages, interactive demos, prototypes, or embeddable widgets that don't need a full framework.",
    },
    "slack-gif-creator": {
        "hermes_tags": ["slack", "gif", "fun", "media", "creation"],
        "trigger": "**Trigger**: Use when creating GIFs for Slack — reactions, announcements, celebration messages, or team inside jokes.",
    },
    "gke-basics": {
        "hermes_tags": ["gcp", "kubernetes", "gke", "container", "orchestration"],
        "trigger": "**Trigger**: Use when working with Google Kubernetes Engine basics — cluster setup, node pools, workloads, networking, and storage fundamentals.",
    },
    "gcloud": {
        "hermes_tags": ["gcp", "gcloud", "cli", "cloud", "google"],
        "trigger": "**Trigger**: Use when working with the Google Cloud CLI (`gcloud`) — authentication, resource management, configuration, and troubleshooting.",
    },
    "firebase-basics": {
        "hermes_tags": ["gcp", "firebase", "backend", "serverless"],
        "trigger": "**Trigger**: Use when setting up or configuring Firebase — Firestore, Authentication, Cloud Functions, Hosting, and Security Rules.",
    },
    "bigquery-basics": {
        "hermes_tags": ["gcp", "bigquery", "analytics", "sql", "data-warehouse"],
        "trigger": "**Trigger**: Use when working with Google BigQuery — querying, partitioning, clustering, cost controls, and best practices.",
    },
    "cloud-run-basics": {
        "hermes_tags": ["gcp", "cloud-run", "serverless", "container"],
        "trigger": "**Trigger**: Use when deploying and managing services on Google Cloud Run — containerization, scaling, networking, and CI/CD.",
    },
    "gemini-api": {
        "hermes_tags": ["gcp", "gemini", "ai", "llm", "google-ai"],
        "trigger": "**Trigger**: Use when working with the Gemini API — text generation, multimodal inputs, function calling, and safety settings.",
    },
    "flutter-dev": {
        "hermes_tags": ["flutter", "mobile", "dart", "cross-platform", "ui"],
        "trigger": "**Trigger**: Use when developing Flutter applications — widget patterns, state management (Riverpod/Bloc), navigation, and platform integration.",
    },
    "react-native-dev": {
        "hermes_tags": ["react-native", "mobile", "expo", "cross-platform", "ui"],
        "trigger": "**Trigger**: Use when developing React Native or Expo applications — component patterns, navigation, state management, and native module integration.",
    },
    "android-native-dev": {
        "hermes_tags": ["android", "kotlin", "jetpack-compose", "mobile", "android-studio"],
        "trigger": "**Trigger**: Use when developing native Android applications with Kotlin and Jetpack Compose — Material Design 3, architecture, and performance.",
    },
    "ios-application-dev": {
        "hermes_tags": ["ios", "swift", "swiftui", "mobile", "apple"],
        "trigger": "**Trigger**: Use when developing native iOS applications — SwiftUI, UIKit, navigation, accessibility, and App Store deployment.",
    },
    "prototype": {
        "hermes_tags": ["design", "prototype", "ui", "ux", "testing"],
        "trigger": "**Trigger**: Use when building multiple versions of a UI component or page to compare different approaches — creates a switcher to cycle through variants.",
    },
    "pptx-generator": {
        "hermes_tags": ["presentation", "pptx", "powerpoint", "slides", "office"],
        "trigger": "**Trigger**: Use when generating PowerPoint presentations programmatically — creating slides, adding charts, applying templates, and exporting.",
    },
    "vision-analysis": {
        "hermes_tags": ["vision", "image-analysis", "ai", "ocr", "multimodal"],
        "trigger": "**Trigger**: Use when analyzing images with AI vision models — describe content, extract text (OCR), review UI mockups, or extract chart data.",
    },
    "minimax-music-gen": {
        "hermes_tags": ["music", "audio", "generation", "minimax", "ai"],
        "trigger": "**Trigger**: Use when generating music with AI — vocal songs, instrumentals, or covers using the MiniMax Music API.",
    },
}

# ============================================================
# ENHANCEMENT ENGINE
# ============================================================

def parse_frontmatter(text: str):
    """Extract frontmatter dict and body content."""
    if not text.startswith("---"):
        return {}, text.strip()
    end = text.find("---", 3)
    if end == -1:
        return {}, text.strip()
    fm_text = text[3:end].strip()
    body = text[end+3:].strip()
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[key] = val
    return fm, body


def has_section(body, name):
    """Check if body has a section with the given name."""
    patterns = [
        f"## {name}",
        f"**{name}**",
        f"### {name}",
        f"## When to {name}",
        f"*{name}*:",
    ]
    for p in patterns:
        if p.lower() in body.lower():
            return True
    return False


def enhance_skill(skill_name, enh):
    """Enhance a single skill file."""
    skill_dir = REPO_SKILLS_DIR / skill_name
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return {"status": "missing", "name": skill_name}

    content = skill_file.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(content)
    
    changes = []
    
    # 1. Add/update trigger
    trigger = enh.get("trigger")
    if trigger and not has_section(body, "Trigger") and not has_section(body, "When to Use"):
        body = f"{trigger}\n\n{body}"
        changes.append("added trigger")
    
    # 2. Add Pitfalls section
    pitfalls = enh.get("pitfalls") or []
    pitfalls_extra = enh.get("pitfalls_extra") or []
    all_pitfalls = pitfalls + pitfalls_extra
    
    if all_pitfalls and not has_section(body, "Pitfalls") and not has_section(body, "Cautions"):
        pit_text = "\n".join(f"- {p}" for p in all_pitfalls)
        body = f"{body}\n\n## Pitfalls\n{pit_text}"
        changes.append(f"added {len(all_pitfalls)} pitfalls")
    
    # 3. Add Verification section
    verification = enh.get("verification") or []
    verification_extra = enh.get("verification_extra") or []
    all_verify = verification + verification_extra
    
    if all_verify and not has_section(body, "Verification"):
        ver_text = "\n".join(f"- {v}" for v in all_verify)
        body = f"{body}\n\n## Verification\n{ver_text}"
        changes.append(f"added {len(all_verify)} verification steps")
    
    # 4. Add Procedure steps
    steps = enh.get("procedure_steps")
    if steps and not has_section(body, "Procedure") and not has_section(body, "How to") and not has_section(body, "Steps"):
        step_text = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        body = f"{body}\n\n## Procedure\n{step_text}"
        changes.append(f"added {len(steps)} procedure steps")
    
    # 5. Update frontmatter tags
    hermes_tags = enh.get("hermes_tags", [])
    updated_fm = False
    
    # Ensure at least basic hermes_tags are present
    if hermes_tags:
        # Check if metadata.hermes.tags exists in the frontmatter
        first_500 = content[:500]
        if "metadata:" not in first_500 or "hermes:" not in first_500:
            # Insert metadata section before closing ---
            tag_line = f"\nmetadata:\n  hermes:\n    tags: [{', '.join(hermes_tags)}]"
            content_lines = content.split("\n")
            for i, line in enumerate(content_lines):
                if line.strip() == "---" and i > 0:
                    content_lines.insert(i, tag_line)
                    content = "\n".join(content_lines)
                    changes.append(f"added hermes tags: {hermes_tags[:3]}...")
                    updated_fm = True
                    break
    
    if not updated_fm:
        # Reconstruct content from original frontmatter + enhanced body
        content = f"---\n"
        for k, v in fm.items():
            content += f"{k}: {v}\n"
        content += f"---\n\n{body}"
    else:
        # Frontmatter was updated inline — body was also modified
        # Reconstruct from frontmatter lines + enhanced body
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = f"---{parts[1]}---\n\n{body}"
    
    # Write back
    skill_file.write_text(content.strip() + "\n", encoding="utf-8")
    return {"status": "enhanced", "name": skill_name, "changes": changes}


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
    for name in ["gke-app-onboarding",
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

    # No custom entries needed for docx/pdf from anthropics (already have minimax variants)
    # They overlap with our existing skills
    
    return generic

# Merge generic enhancements into the main ENHANCEMENTS dict
# This runs at module import time
for k, v in _add_generic_enhancements().items():
    if k not in ENHANCEMENTS:
        ENHANCEMENTS[k] = v

def main():
    """Enhance all imported skills."""
    print("=" * 60)
    print("ENHANCING IMPORTED SKILLS WITH HERMES FORMAT")
    print("=" * 60)
    
    results = []
    for skill_name, enh in sorted(ENHANCEMENTS.items()):
        result = enhance_skill(skill_name, enh)
        results.append(result)
        if result["status"] == "enhanced":
            changes = ", ".join(result.get("changes", []))
            print(f"  ✓ {skill_name}: {changes}")
        elif result["status"] == "missing":
            print(f"  - {skill_name}: not found (may have different name)")
    
    # Summary
    enhanced = [r for r in results if r["status"] == "enhanced"]
    missing = [r for r in results if r["status"] == "missing"]
    print(f"\n{'='*60}")
    print(f"Enhanced: {len(enhanced)} skills")
    print(f"Missing: {len(missing)} skills")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
