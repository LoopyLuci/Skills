#!/usr/bin/env python3
"""Generate enhanced Hermes SKILL.md files for all Matt Pocock skills."""
import os, json, re
from hermes_tools import write_file

SKILLS_DIR = "/c/Users/limpi/AppData/Local/hermes/skills/software-development"

def make(name, desc, tags, related, body, pitfalls, checklist, code=None):
    """Generate a full SKILL.md and write it."""
    lines = []
    lines.append("---")
    lines.append(f"name: {name}")
    lines.append(f"description: {desc}")
    lines.append(f"tags: [{', '.join(tags)}]")
    if related:
        lines.append(f"related_skills: [{', '.join(related)}]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {name.replace('-', ' ').title()}")
    lines.append("")
    lines.append(body)
    lines.append("")
    
    # Common Pitfalls
    lines.append("## Common Pitfalls")
    lines.append("")
    for p in pitfalls:
        lines.append(f"- **{p[0]}**: {p[1]}")
    lines.append("")
    
    # Code Examples
    if code:
        lines.append("## Code Examples")
        lines.append("")
        lines.append(code)
        lines.append("")
    
    # Verification Checklist
    lines.append("## Verification Checklist")
    lines.append("")
    for item in checklist:
        lines.append(f"- [ ] {item}")
    lines.append("")
    
    content = "\n".join(lines)
    
    skill_dir = os.path.join(SKILLS_DIR, name)
    os.makedirs(skill_dir, exist_ok=True)
    out_path = os.path.join(skill_dir, "SKILL.md")
    
    r = write_file(out_path, content)
    print(f"  Created {name} ({len(lines)} lines) - {r.get('status', 'OK')}")

print("Starting skill generation...")

# ============================================================
# 1. design-an-interface
# ============================================================
make("design-an-interface",
    "Use when designing an API, exploring interface options, or comparing module shapes",
    ["design", "architecture", "API", "sub-agents", "review"],
    ["codebase-design", "improve-codebase-architecture", "to-spec"],
    """Generate multiple radically different interface designs for a module using parallel sub-agents. Based on "Design It Twice" from "A Philosophy of Software Design": your first idea is unlikely to be the best.

## Workflow

### 1. Gather Requirements
Before designing, understand:
- What problem does this module solve?
- Who are the callers? (other modules, external users, tests)
- What are the key operations?
- Any constraints? (performance, compatibility, existing patterns)
- What should be hidden inside vs exposed?

### 2. Generate Designs (Parallel Sub-Agents)
Spawn 3+ sub-agents simultaneously. Each must produce a radically different approach.

Assign each agent a different constraint:
- Agent 1: "Minimize method count - aim for 1-3 methods max"
- Agent 2: "Maximize flexibility - support many use cases"
- Agent 3: "Optimize for the most common case"
- Agent 4: "Take inspiration from a specific paradigm/library"

### 3. Present Designs
Show each design with its interface signature, usage examples, hidden complexity, and trade-offs.

### 4. Compare and Select
Compare designs side by side. Ask: which is deepest? Easiest to use? Most maintainable? Pick one or hybridize.

> **Note**: This skill is deprecated in the original source. Consider using `codebase-design` for deep module vocabulary instead.""",
    [
        ("Over-designing before understanding requirements", "Jumping to interface designs without first gathering requirements leads to designs that don't solve the actual problem. Always complete the requirements checklist first."),
        ("Sub-agent designs too similar", "If spawned sub-agents produce similar designs, you lose the benefit of radical comparison. Enforce different constraints per agent."),
        ("Ignoring what callers actually need", "Designing interfaces without understanding who calls them and how leads to mismatched abstractions."),
    ],
    [
        "Requirements gathered before design started",
        "At least 3 radically different designs generated",
        "Each design has interface signature, usage example, hidden complexity, and trade-offs",
        "User has compared designs and selected one",
    ],
    """```typescript
// Minimal interface approach
interface UserStore {
  get(id: string): Promise<User>;
  set(user: User): Promise<void>;
}

// Flexible approach
interface UserStore {
  find(query: UserQuery): Promise<User[]>;
  findOne(query: UserQuery): Promise<User | null>;
  create(data: CreateUserDTO): Promise<User>;
  update(id: string, data: Partial<User>): Promise<User>;
  delete(id: string): Promise<void>;
}
```"""
)

# ============================================================
# 2. qa
# ============================================================
make("qa",
    "Use when reporting bugs, doing QA, or filing GitHub issues conversationally",
    ["testing", "QA", "bugs", "GitHub", "issues"],
    ["triage", "diagnosing-bugs", "to-tickets"],
    """Run an interactive QA session. The user describes problems they're encountering. You clarify, explore the codebase for context, and file GitHub issues that are durable, user-focused, and use the project's domain language.

## For each issue the user raises

### 1. Listen and lightly clarify
Let the user describe the problem in their own words. Ask at most 2-3 short clarifying questions focused on:
- What they expected vs what actually happened
- Steps to reproduce (if not obvious)
- Whether it's consistent or intermittent

Do NOT over-interview. If the description is clear enough to file, move on.

### 2. Explore the codebase in the background
While talking to the user, understand the relevant area to:
- Learn the domain language used in that area
- Understand what the feature is supposed to do
- Identify the user-facing behavior boundary

### 3. Assess scope: single issue or breakdown?
Break down when the fix spans multiple independent areas or there are clearly separable concerns.

### 4. File the issue(s)
Write issues that describe the problem from the user's perspective, not implementation details.""",
    [
        ("Over-interviewing the user", "Asking too many clarifying questions wastes user time. Limit to 2-3 questions. If the description is clear enough, file the issue."),
        ("Including implementation details in issues", "Issues should describe user-facing behavior, not internal file paths or line numbers. Keep the focus on what is broken from the user's perspective."),
        ("Not breaking down compound issues", "A single report that spans multiple independent areas should be split into separate issues for parallel work."),
    ],
    [
        "User described the problem in their own words",
        "At most 2-3 clarifying questions asked",
        "Codebase explored for domain context",
        "Compound issues broken into separate issues",
        "Issues filed without implementation details",
    ],
    """```bash
# QA Session Workflow
# 1. User reports: "The form doesn't validate on submit"
# 2. Explore the codebase to understand form handling
# 3. File a GitHub issue:

## Summary
Form validation does not trigger on submit button click

## Expected behavior
Invalid fields show error messages and red border on submit

## Actual behavior
Form submits successfully with invalid/empty data

## Steps to reproduce
1. Navigate to /settings/profile
2. Leave required field "email" empty
3. Click "Save Changes"
4. Observe: form submits without validation feedback
```"""
)

# ============================================================
# 3. request-refactor-plan
# ============================================================
make("request-refactor-plan",
    "Use when planning a refactor, requesting a refactoring RFC, or breaking refactors into commits",
    ["refactoring", "planning", "commits", "GitHub", "RFC"],
    ["improve-codebase-architecture", "to-spec", "codebase-design"],
    """Create a detailed refactor plan with tiny, safe commits via user interview, then file it as a GitHub issue. Follow Martin Fowler's advice: make each refactoring step as small as possible, so you can always see the program working.

## Steps

1. Ask the user for a long, detailed description of the problem and any potential ideas for solutions.
2. Explore the repo to verify their assertions and understand the current state.
3. Ask whether they have considered other options, and present alternatives.
4. Interview the user about the implementation. Be extremely detailed and thorough.
5. Hammer out the exact scope: what to change and what not to change.
6. Check for test coverage in the affected area. If insufficient, ask about testing plans.
7. Break the implementation into a plan of tiny commits.
8. Create a GitHub issue with the refactor plan template.""",
    [
        ("Skipping codebase verification", "Always verify the user's assertions about the codebase before planning. Misunderstandings compound into wrong plans."),
        ("Commits that are too large", "Each commit should leave the codebase in a working state. If a commit description spans multiple concerns, it is too big."),
        ("Insufficient test coverage", "Do not plan refactors in areas without test coverage without asking about testing strategy."),
    ],
    [
        "User's assertions verified against actual codebase",
        "Alternative options discussed with user",
        "Test coverage assessed for affected areas",
        "Implementation broken into tiny, working commits",
        "GitHub issue created with the refactor plan",
    ],
)

# ============================================================
# 4. ubiquitous-language
# ============================================================
make("ubiquitous-language",
    "Use when defining domain terms, building a glossary, or creating a ubiquitous language",
    ["DDD", "glossary", "terminology", "domain", "language"],
    ["domain-modeling", "codebase-design"],
    """Extract and formalize domain terminology from the current conversation into a consistent glossary saved to UBIQUITOUS_LANGUAGE.md.

## Process
1. **Scan the conversation** for domain-relevant nouns, verbs, and concepts
2. **Identify problems**:
   - Same word used for different concepts (ambiguity)
   - Different words used for the same concept (synonyms)
   - Vague or overloaded terms
3. **Propose a canonical glossary** with opinionated term choices
4. **Write to UBIQUITOUS_LANGUAGE.md** in the working directory
5. **Output a summary** inline in the conversation""",
    [
        ("Overloading existing terms", "Using the same word for different concepts creates ambiguity. Flag and rename before it spreads."),
        ("Creating too many terms too early", "Do not carve out terms for everything upfront. Let the model emerge from real usage and only formalize terms that matter."),
        ("Not updating existing documentation", "New terms must be propagated to existing docs, ADRs, and code comments to avoid confusion."),
    ],
    [
        "Conversation scanned for domain-relevant terms",
        "Ambiguities and synonyms identified and flagged",
        "Canonical glossary proposed with opinionated choices",
        "UBIQUITOUS_LANGUAGE.md written to working directory",
        "Summary output inline in conversation",
    ],
)

# ============================================================
# 5. ask-matt
# ============================================================
make("ask-matt",
    "Use when unsure which skill or flow fits your current situation",
    ["routing", "navigation", "skills", "meta", "workflow"],
    ["wayfinder", "triage", "writing-great-skills"],
    """A router skill. If you don't remember every skill, ask.

## The main flow: idea to ship
The route most work travels:
1. Grill the idea (grill-with-docs or grill-me)
2. Prototype to answer specific questions (prototype)
3. Spec multi-session work (to-spec, to-tickets)
4. Implement (implement)
5. Review (code-review)

Key on-ramps: triage (for incoming issues), wayfinder (for new codebases).

Standalone skills cover: diagnosing-bugs, design-an-interface, domain-modeling, ubiquitous-language, qa, writing-* skills, teach, and more.

> **Note**: This skill references the original Matt Pocock skills ecosystem. Skills not present in Hermes Agent can be adapted from the source repository.""",
    [
        ("Not recognizing the meta nature", "This skill is a router - it does not execute work. Point to the right skill and let it handle the implementation."),
        ("Stale mental model of available skills", "The skill index evolves. Routers must be updated when skills are added or removed."),
    ],
    [
        "User's situation understood",
        "Correct skill or flow identified for their needs",
        "Direction provided, not implementation",
    ],
)

# ============================================================
# 6. code-review
# ============================================================
make("code-review",
    "Use when reviewing a branch, PR, or work-in-progress changes against standards and spec",
    ["review", "code-quality", "PR", "standards", "spec"],
    ["requesting-code-review", "code-review-best-practices", "codebase-design"],
    """Two-axis review of the diff between HEAD and a fixed point the user supplies:
- **Standards** - does the code conform to this repo's documented coding standards?
- **Spec** - does the code faithfully implement the originating issue / PRD / spec?

## Process

### 1. Pin the fixed point
Whatever the user said as the fixed point - a commit SHA, branch name, tag, main, HEAD~5, etc. Capture the diff command: `git diff <fixed-point>...HEAD`. Also note the list of commits.

### 2. Identify the spec source
Look for the originating spec: issue references in commit messages, a spec file under docs/ or specs/, or a PRD.

### 3. Run parallel reviews
Spawn sub-agents for the Standards review and Spec review simultaneously. Aggregate findings side by side.""",
    [
        ("Fixed point not resolving", "Always verify the fixed point resolves with git rev-parse before spawning sub-agents. A bad ref wastes both agents' contexts."),
        ("Empty diff not caught early", "Check diff is non-empty before starting reviews. An empty diff should fail here, not inside two parallel sub-agents."),
        ("Spec source not found", "If no spec/issue can be found for the changes, the spec review axis has nothing to compare against. Report this clearly."),
    ],
    [
        "Fixed point confirmed (git rev-parse succeeds)",
        "Diff is non-empty",
        "Spec source identified or reported missing",
        "Standards review completed",
        "Spec review completed",
        "Findings aggregated and reported side by side",
    ],
    """```bash
# Step 1: Pin the fixed point
git rev-parse main
git diff main...HEAD --stat
git log main..HEAD --oneline

# Step 2: Find spec source
# Look in commit messages for issue references (#123)
# Check docs/, specs/, .scratch/ for matching spec files

# Step 3: Run parallel reviews
# Standards review: does code follow this repo's conventions?
# Spec review: does code implement the originating issue?
```"""
)

# ============================================================
# 7. codebase-design
# ============================================================
make("codebase-design",
    "Use when designing module interfaces, finding deepening opportunities, or making code testable",
    ["design", "architecture", "modules", "depth", "interfaces"],
    ["design-an-interface", "improve-codebase-architecture", "domain-driven-design-tactical"],
    """Design deep modules: a lot of behavior behind a small interface, placed at a clean seam, testable through that interface.

## Glossary
Use these terms exactly - consistent language is the point.

- **Module** - anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice.
- **Interface** - everything a caller must know to use the module correctly: type signature, invariants, ordering constraints, error modes, configuration, and performance characteristics.
- **Implementation** - what is inside a module, its body of code.
- **Depth** - leverage at the interface: the amount of behavior a caller can exercise per unit of interface they have to learn.
- **Seam** (Michael Feathers) - a place where you can alter behavior without editing in that place.

## Principles
- Deep over shallow: prefer a small interface that hides lots of behavior
- Test through the interface: if the seam is clean, the test is simple
- Caller leverage: every line of interface should unlock multiple lines of behavior""",
    [
        ("Inconsistent terminology", "Do not substitute 'component', 'service', 'API', or 'boundary' for the defined terms. Consistent language is the whole point."),
        ("Depth over everything", "Depth is a goal, but not the only one. Performance requirements, operational constraints, and team familiarity also matter."),
        ("Seams placed at the wrong level", "A seam should match a natural boundary in the domain, not an architectural fashion. Forcing seams where they do not belong creates accidental complexity."),
    ],
    [
        "Module terminology used consistently throughout",
        "Interface signatures are clear and minimal",
        "Depth evaluated: behavior per unit of interface",
        "Seam boundaries identified and justified",
        "Design principles documented",
    ],
    """```typescript
// Deep module example: small interface, complex implementation

interface PaymentProcessor {
  charge(amount: Money, source: PaymentSource): Result<Payment>;
  refund(paymentId: string): Result<Payment>;
}

// Implementation handles: retries, idempotency, webhook verification,
// currency conversion, fee calculation, receipt email,
// fraud detection, dispute handling, logging
// But caller only sees charge() and refund()
class StripePaymentProcessor implements PaymentProcessor {
  // ... complex internals hidden behind a simple interface
}
```"""
)

# ============================================================
# 8. diagnosing-bugs
# ============================================================
make("diagnosing-bugs",
    "Use when diagnosing hard bugs, debugging failures, or investigating performance regressions",
    ["debugging", "bugs", "diagnosis", "bisect", "testing"],
    ["systematic-debugging", "debugging-techniques-advanced", "qa"],
    """A discipline for hard bugs. Skip phases only when explicitly justified.

## Phase 1 - Build a feedback loop
**This is the skill.** Everything else is mechanical. If you have a tight pass/fail signal for the bug - one that goes red on *this* bug - you will find the cause.

Ways to construct one, in roughly this order:
1. **Failing test** at whatever seam reaches the bug
2. **Curl / HTTP script** against a running dev server
3. **CLI invocation** with a fixture input
4. **Headless browser script** (Playwright / Puppeteer)
5. **Replay a captured trace**
6. **Throwaway harness** with mocked deps
7. **Property / fuzz loop** - run 1000 random inputs
8. **Bisection harness** for git bisect run

## Phase 2 - Find the fault
With the loop in place, let it guide you. Narrow by bisection, hypothesis testing, or instrumentation.

## Phase 3 - Fix
Apply the fix and confirm the loop goes green. Consider whether the same class of bug exists elsewhere.""",
    [
        ("Starting to code before building a feedback loop", "The first phase is the skill. Without a tight pass/fail signal, no amount of staring at code will find the bug."),
        ("Skipping the feedback loop for 'simple' bugs", "Even seemingly simple bugs benefit from an automated signal. Manual verification is slow and error-prone."),
        ("Over-instrumenting without a hypothesis", "Adding logging everywhere without a theory of the root cause creates noise, not signal. Form a hypothesis first, then instrument to test it."),
    ],
    [
        "Feedback loop built (failing test, curl, or harness)",
        "Pass/fail signal is tight (goes red on this bug specifically)",
        "Bisection or hypothesis-testing performed",
        "Root cause identified and documented",
        "Fix verified by the feedback loop going green",
    ],
    """```python
# Example: Bug where session expires at 29min instead of configured 60min

# Build the feedback loop - a failing test
def test_session_expires_at_configured_timeout():
    session = Session(timeout_minutes=60)
    advance_time(minutes=29)
    assert session.is_valid()  # Should be True, but might be False

# Property-based test to narrow the failure
@pytest.mark.parametrize("ttl", [1, 5, 30, 60, 120])
def test_timeout_matches_ttl(ttl):
    session = Session(timeout_minutes=ttl)
    advance_time(minutes=ttl - 1)
    assert session.is_valid()
    advance_time(minutes=2)
    assert not session.is_valid()
```"""
)

# ============================================================
# 9. domain-modeling
# ============================================================
make("domain-modeling",
    "Use when building or sharpening a project's domain model and recording ADRs",
    ["DDD", "domain", "modeling", "ADR", "architecture"],
    ["ubiquitous-language", "codebase-design", "domain-driven-design-tactical"],
    """Actively build and sharpen the project's domain model as you design. Challenge terms, invent edge-case scenarios, and write the glossary and decisions down the moment they crystallize.

## File structure
Most repos have a single context:

```
/
|- CONTEXT.md
|- docs/
|   |- adr/
|       |- 0001-event-sourced-orders.md
|       |- 0002-postgres-for-write-model.md
|- src/
```

Create files lazily - only when you have something to write.

## During the session
- Challenge against the glossary when the user uses a term that conflicts
- Capture edge cases: scenarios that stress the model
- Propose ADRs: record architectural decisions with context, decision, and consequences
- Tie concepts to code locations""",
    [
        ("Creating files before you have something to write", "Create CONTEXT.md and ADR files lazily - only when you have resolved terms or decisions to record. Empty files are noise."),
        ("Terms that conflict with existing glossary without flagging", "When the user uses a term that conflicts with what is in the glossary, stop and discuss the discrepancy."),
        ("Neglecting the single/multi-context distinction", "Most repos have one context, but some need CONTEXT-MAP.md. Applying single-context rules to a multi-context repo creates confusion."),
    ],
    [
        "CONTEXT.md created/updated with resolved terms",
        "ADRs recorded for architectural decisions",
        "Terminology conflicts resolved with user",
        "Single or multi-context structure determined",
        "Files created only when content exists to write",
    ],
    """```markdown
# Example ADR
## ADR-0001: Event-Sourced Order Lifecycle

**Context:** Orders need full audit trail and the ability to replay
state after failures.

**Decision:** Model Order as an event stream:
- OrderCreated, ItemAdded, ItemRemoved, OrderSubmitted, OrderPaid
- Current state is folded from the stream
- No mutable state table

**Consequences:**
- (+) Full audit trail by design
- (+) Temporal queries are free
- (-) More complex read-model projection needed
```"""
)

# ============================================================
# 10. improve-codebase-architecture
# ============================================================
make("improve-codebase-architecture",
    "Use when improving codebase architecture, reducing coupling, or increasing cohesion",
    ["architecture", "refactoring", "coupling", "cohesion", "analysis"],
    ["codebase-design", "request-refactor-plan", "code-review"],
    """Analyze and improve codebase architecture by identifying opportunities for deeper modules, better seams, and reduced coupling.

## Process

### 1. Map the current architecture
- Identify modules (packages, directories, classes)
- Document entry points and dependencies
- Measure module depth (interface vs implementation ratio)

### 2. Identify problems
- Shallow modules (interface nearly as complex as implementation)
- Tight coupling between unrelated concerns
- God modules that do too much
- Missing seams (should be separable but aren't)

### 3. Report with an HTML report
Generate a structured report with the current architecture, identified issues, and specific recommendations. Present both a quick summary inline and a detailed HTML report.

### 4. Prioritize improvements
Rank by impact: which changes give the most leverage for the least risk?""",
    [
        ("Analyzing without a clear baseline", "Run the analysis tools before making any changes to establish the baseline metrics."),
        ("Focusing only on structure, not behavior", "Architecture is about both. A structurally clean module that is hard to use or test is not an improvement."),
        ("Refactoring without tests", "Architecture improvements without test coverage are risky. Ensure the critical paths are tested before restructuring."),
    ],
    [
        "Baseline architecture metrics gathered",
        "Deepening opportunities identified",
        "Coupling points documented",
        "Specific recommendations provided",
        "Changes tested and verified",
    ],
)

# ============================================================
# 11. prototype
# ============================================================
make("prototype",
    "Use when building throwaway prototypes to answer specific design questions",
    ["prototyping", "experimentation", "design", "exploration", "quick"],
    ["to-spec", "spike", "design-an-interface"],
    """Build throwaway prototypes to answer specific design questions before committing to an implementation. Fast exploration for high-risk decisions.

## Principles
- **Prototypes are throwaway** by design. Do not let prototype code leak into production.
- **One question per prototype.** Define the question before you start.
- **Minimum viable code** to answer the question. No error handling, no edge cases, no polish.

## Process
1. Define the question: what specific decision does this prototype inform?
2. Choose the axis: logic, UI, or both
3. Build the minimum code to answer the question
4. Present findings and make a decision
5. Discard or archive the prototype code

## Variation for UI prototypes
Use a separate UI prototype to explore visual/interaction questions independently from the logic.""",
    [
        ("Falling in love with the prototype", "Prototypes are throwaway by design. Do not let prototype code leak into production."),
        ("Over-engineering the prototype", "Prototypes should answer one question as quickly as possible. Adding error handling, edge cases, or polish defeats the purpose."),
        ("Not defining success criteria upfront", "Without a clear question to answer, the prototype has no completion criteria. Define what 'done' means before starting."),
    ],
    [
        "Clear question defined that the prototype answers",
        "Minimum code written to answer the question",
        "Prototype marked as throwaway (not for production)",
        "Decision made based on prototype findings",
    ],
    """```typescript
// Prototype: Can we implement real-time search with WebSockets?
// SPEND NO MORE THAN 30 MINUTES ON THIS

// 1. Server (basic WebSocket handler)
import { WebSocketServer } from "ws";
const wss = new WebSocketServer({ port: 8080 });

// 2. Client (quick test)
const ws = new WebSocket("ws://localhost:8080");

// 3. The question this answers:
//   - Is latency under 200ms for typical queries?
//   - Does the server handle 10 concurrent connections?
// DECISION: Proceed with WebSocket or switch to polling
```"""
)

# ============================================================
# 12. setup-matt-pocock-skills
# ============================================================
make("setup-matt-pocock-skills",
    "Use when setting up Matt Pocock skills in a new workspace or project",
    ["setup", "onboarding", "configuration", "matt-pocock", "workspace"],
    ["writing-great-skills", "ask-matt", "wayfinder"],
    """Configure a new workspace with the full Matt Pocock skillset: issue trackers, domain files, triage labels, and cross-skill integration.

## Setup Steps

### 1. Check for existing domain files
Look for CONTEXT.md, UBIQUITOUS_LANGUAGE.md, and existing ADRs before creating new ones.

### 2. Configure issue tracker
Setup the issue tracker configuration for the project. Create docs/agents/issue-tracker.md with the appropriate commands for the issue tracker being used (GitHub, GitLab, or local file-based).

### 3. Configure triage labels
If using GitHub or GitLab, configure triage labels for classifying issues.

### 4. Verify cross-skill integration
Ensure that skills reference correct paths and domain files are readable by dependent skills.""",
    [
        ("Missing issue-tracker configuration", "The issue tracker setup is critical for skills like code-review and to-tickets. Do not skip this step."),
        ("Not checking for existing domain files", "Always check for existing CONTEXT.md, ADRs, or UBIQUITOUS_LANGUAGE.md before creating new ones."),
        ("Forgetting cross-skill references", "Other skills reference the outputs of this setup (domain files, issue tracker docs). Verify they resolve correctly."),
    ],
    [
        "Issue tracker configured (docs/agents/issue-tracker.md exists)",
        "Domain files checked for existing content",
        "Triage labels configured if applicable",
        "Cross-skill references verified",
    ],
)

# ============================================================
# 13. tdd
# ============================================================
make("tdd",
    "Use when practicing test-driven development or writing tests before code",
    ["TDD", "testing", "test-first", "red-green-refactor", "quality"],
    ["test-driven-development", "testing-pyramid-practice", "behavior-driven-development"],
    """Practice Test-Driven Development with the Red-Green-Refactor cycle.

## The Cycle
1. **RED** - Write a failing test. See it fail to confirm the test can detect the absence of the feature.
2. **GREEN** - Write the minimal code to make the test pass. Do not write production code without a failing test.
3. **REFACTOR** - Clean up the code while keeping all tests green. Improve design without changing behavior.

## Principles
- Write the test first, always
- One behavior per test
- Test at the appropriate seam (unit, integration, or e2e)
- Mock at boundaries, not internals
- Tests are documentation - they describe what the system does""",
    [
        ("Tests that are too large", "Each test should verify one behavior. Large tests that check multiple things lose the granular feedback TDD depends on."),
        ("Skipping the red phase", "Seeing the test fail confirms it can actually fail. Skipping to green risks a test that passes for the wrong reasons."),
        ("Refactoring without test confidence", "If you are not confident the tests will catch regressions, you are not refactoring - you are rewriting."),
    ],
    [
        "RED: Test written and confirmed failing",
        "GREEN: Minimal code written to pass the test",
        "REFACTOR: Code cleaned up with tests still green",
        "Test granularity is one behavior per test",
    ],
    """```python
# RED: Write a failing test first
def test_user_creation_with_valid_email():
    user = User(email="test@example.com", name="Test User")
    assert user.email == "test@example.com"
    assert user.name == "Test User"
# >>> RUN: Test FAILS (User class does not exist yet)

# GREEN: Write minimal code to pass
class User:
    def __init__(self, email: str, name: str):
        self.email = email
        self.name = name
# >>> RUN: Test PASSES

# REFACTOR: Clean up without changing behavior
# Add validation, better typing, etc.
```"""
)

# ============================================================
# 14. to-spec
# ============================================================
make("to-spec",
    "Use when turning a design discussion into a formal specification document",
    ["specification", "documentation", "design", "planning", "requirements"],
    ["to-tickets", "to-questionnaire", "design-an-interface"],
    """Turn a design discussion into a formal specification document. Capture requirements, acceptance criteria, and design decisions in a structured format.

## Process
1. **Extract requirements** from the conversation
2. **Define acceptance criteria** for each requirement (must be testable)
3. **Document design decisions** with rationale
4. **Write the spec** to a file in the project
5. **Validate** with the user before proceeding to implementation

The spec serves as the source of truth that tickets are created from and code is reviewed against.""",
    [
        ("Spec that is too detailed too early", "High-level specs should leave room for implementation decisions. Over-specifying creates friction."),
        ("Spec that is too vague to implement", "Acceptance criteria must be testable. 'Fast enough' without a number is not an acceptance criterion."),
        ("Writing spec without user verification", "Always validate the spec with the user before moving to tickets. A spec that does not match what they wanted creates rework."),
    ],
    [
        "Requirements captured from discussion",
        "Acceptance criteria are testable",
        "Design decisions documented with rationale",
        "Spec validated with user",
        "Spec saved to project docs directory",
    ],
)

# ============================================================
# 15. to-tickets
# ============================================================
make("to-tickets",
    "Use when breaking a spec into actionable tickets or issues for implementation",
    ["tickets", "issues", "planning", "agile", "project-management"],
    ["to-spec", "triage", "qa"],
    """Break a specification into actionable, granular tickets. Each ticket represents a single unit of work with clear acceptance criteria.

## Process
1. **Review the spec** - understand the full scope
2. **Identify independent units** of work that can be done separately
3. **Declare blocking edges** - what each ticket depends on and what depends on it
4. **Write acceptance criteria** for each ticket
5. **Order by dependency chain** - blockers first

For local tracking, use one file per ticket under `.scratch/<feature>/issues/`.
For real trackers, use native blocking links between issues.""",
    [
        ("Tickets that are too large", "A ticket should represent a single unit of work. If it cannot be completed in one sitting, split it."),
        ("Tickets without blocking edges declared", "Each ticket should declare what it blocks and what blocks it. Without this, parallel work is impossible to coordinate."),
        ("Missing acceptance criteria", "Every ticket needs clear, testable acceptance criteria. 'Works as expected' is not acceptance criteria."),
    ],
    [
        "Each ticket is a single unit of work",
        "Blocking edges declared for each ticket",
        "Acceptance criteria are clear and testable",
        "Tickets ordered by dependency chain",
    ],
)

# ============================================================
# 16. triage
# ============================================================
make("triage",
    "Use when triaging incoming issues, feature requests, or bugs for prioritization",
    ["triage", "issues", "prioritization", "bugs", "workflow"],
    ["qa", "to-tickets", "wayfinder"],
    """Triage incoming issues, feature requests, and bug reports. Classify, prioritize, and route each item to the appropriate workflow.

## Process
1. **Classify**: Bug (something is broken), Feature (new capability), Enhancement (improve existing), Question (user needs information)
2. **Prioritize** (P0-P3): P0 blocks release or affects all users, P1 major impact with difficult workaround, P2 moderate impact with workaround, P3 minor or nice-to-have
3. **Route**: Assign labels, add to milestone, assign owner if known
4. **Check for duplicates** before filing new issues

## Out of scope for triage
Some items may be out of scope for the current project. Maintain a clear definition of what belongs and what does not.""",
    [
        ("Prioritizing without understanding impact", "Urgency without understanding user impact leads to wrong priorities. Always assess severity through the user's eyes."),
        ("Missing duplicate detection", "Before creating a new issue, search for existing ones. Duplicates fragment the conversation."),
        ("Triage without routing", "Every triaged item should go somewhere - a milestone, a project board, or at minimum a label. Unrouted items get lost."),
    ],
    [
        "Issue classified (bug/feature/enhancement/question)",
        "Priority assigned (P0-P3)",
        "Duplicate check performed",
        "Labels applied appropriately",
        "Issue routed to milestone or project board",
    ],
)

# ============================================================
# 17. wayfinder
# ============================================================
make("wayfinder",
    "Use when navigating a codebase or project to understand its structure and conventions",
    ["navigation", "exploration", "onboarding", "discovery", "codebase"],
    ["ask-matt", "codebase-design", "codebase-onboarding"],
    """Navigate and explore a new codebase to understand its structure, conventions, and domain terminology quickly.

## Process
1. **Read CONTEXT.md** (if it exists) for the domain model
2. **Map top-level directory structure** - identify entry points, modules, and config
3. **Find entry points** - main files, index files, public API surfaces
4. **Review README and docs** - understand conventions and patterns
5. **Read key tests** - tests reveal how the code is supposed to work
6. **Build a mental model** and document it for future reference

## Output
Document the codebase structure, key entry points, testing patterns, and module relationships so you and other skills can navigate efficiently.""",
    [
        ("Not reading CONTEXT.md or domain docs first", "Understanding the domain model before diving into code saves time. Skip the documents and you navigate blind."),
        ("Going too deep too fast", "Start with the directory structure and entry points. Do not dive into implementation details until you know the overall shape."),
        ("Not building a mental model incrementally", "Document what you learn as you go. Mental models fade; written notes persist and can be shared."),
    ],
    [
        "Directory structure mapped",
        "Entry points identified",
        "Domain documents read (CONTEXT.md, ADRs, etc.)",
        "Testing patterns understood",
        "Mental model documented",
    ],
)

# ============================================================
# 18. loop-me
# ============================================================
make("loop-me",
    "Use when you want the AI to check back periodically for updates or progress",
    ["looping", "check-in", "progress", "async", "status"],
    ["teach", "wayfinder", "triage"],
    """Set up periodic check-ins so the AI monitors progress and reports back on long-running or async tasks.

## When to use
- You started a long-running process and want status updates
- You asked the user to do something and want to check back
- You are waiting for an external event or response

## How it works
1. Define what you are waiting for (the check condition)
2. Set the check interval (how often to check)
3. Define the termination condition (when to stop checking)
4. Specify the feedback channel (how to report results)

> **Note**: This skill is designed for Claude Code's loop-me feature. In Hermes Agent, use background processes with process() polling or cron-based monitoring instead.""",
    [
        ("Forgetting to set up the check-in mechanism", "Without an explicit mechanism (cron, reminder, callback), the loop does not function. Define how the AI will check back."),
        ("Loops that are too frequent", "Checking in every minute creates noise. Match the interval to the expected progress rate."),
        ("No clear termination condition", "The loop needs a defined end state. Without it, the AI keeps checking in indefinitely."),
    ],
    [
        "Check-in mechanism defined",
        "Interval appropriate for expected progress",
        "Termination condition specified",
        "Feedback delivery method agreed",
    ],
)

# ============================================================
# 19. setup-ts-deep-modules
# ============================================================
make("setup-ts-deep-modules",
    "Use when setting up TypeScript deep modules with dependency-cruiser enforcement",
    ["TypeScript", "modules", "dependency-cruiser", "architecture", "encapsulation"],
    ["codebase-design", "setup-matt-pocock-skills"],
    """Make every package in a TypeScript monorepo a deep module using dependency-cruiser to enforce entry-point boundaries.

## The shape this enforces
```
src/packages/
  <name>/
    index.ts        - an entry point (public)
    client.ts       - another entry point (packages may expose several)
    lib/            - implementation: hidden from outside
    tests/          - co-located tests + fixtures (private)
```

## Four rules (all error level)
1. **Entry-point boundary** - code outside a package may import only root files
2. **Intra-package freedom** - a package's own files import each other freely
3. **Tests through entry points** - test files import entry points only
4. **No circular dependencies** between packages

## Setup
1. Install dependency-cruiser
2. Create the configuration with the four rules
3. Run initial lint to find violations
4. Fix or accept existing violations before enforcement""",
    [
        ("Not running the verification after setup", "The skill includes a verification step that proves the rules bite. Skipping it means you will not know if the setup worked."),
        ("Existing code that violates the new rules", "The initial lint run will likely catch existing violations. Decide whether to fix them before or after enforcing the rules."),
        ("Entry points that export too much", "A package's root files are its public API. Barrel files that re-export everything undermine the deep module pattern."),
    ],
    [
        "dependency-cruiser installed",
        "Configuration created with 4 rules",
        "Initial lint run completed",
        "Existing violations identified",
        "Entry point boundaries enforced",
    ],
)

# ============================================================
# 20. to-questionnaire
# ============================================================
make("to-questionnaire",
    "Use when turning an unanswered decision into a questionnaire for someone else",
    ["questionnaire", "research", "decisions", "interview", "async"],
    ["to-spec", "ubiquitous-language", "wayfinder"],
    """Turn something the user cannot answer alone into a questionnaire - a Markdown document they hand to someone to fill in async, or fill out together over a meeting.

## Process
1. **Who is it going to?** Ask the recipient's role, expertise, and relationship to the user. This fixes the tone and context level.
2. **What do you need back?** Ask the specific decisions or facts the user cannot resolve alone.
3. **Write the questionnaire.** Draft questions aimed at the gap. Write to to-questionnaire-<slug>.md.

## Document structure
Frame the document as a discovery questionnaire: the user lacks context, the recipient holds it. Order questions most-important-first and group under headings by theme.""",
    [
        ("Tone mismatch with the recipient", "A questionnaire for an executive reads differently than one for a domain expert. Adjust tone and context level."),
        ("Questions that assume the answer", "Leading questions bias the response. Frame questions as open-ended discovery."),
        ("Too many questions", "Async questionnaires compete for attention. Prioritize the most important questions - you may only get one pass."),
    ],
    [
        "Recipient identified (role, expertise, relationship)",
        "Decisions or facts needed from recipient listed",
        "Questionnaire written to to-questionnaire-<slug>.md",
        "Questions ordered most-important-first",
        "All user's named needs covered by a question",
    ],
)

# ============================================================
# 21. wizard
# ============================================================
make("wizard",
    "Use when generating interactive bash wizards for manual setup procedures",
    ["wizard", "automation", "setup", "bash", "configuration"],
    ["setup-pre-commit", "setup-matt-pocock-skills", "setup-ts-deep-modules"],
    """Generate an interactive bash wizard that walks a human through a manual procedure - opening URLs, capturing values, confirming each step, and writing .env files and GitHub Actions secrets.

## How it works
A wizard is a bash script with two parts:
1. **The library** (above the STAGES marker) - provided by template.sh, handles progress display, confirmation gates, URL opening, and secret entry
2. **The stages** - you define what steps the wizard performs

The library is identical in every wizard; that consistency is the point - never hand-edit it.

A wizard is ephemeral by default - built for one run, saved to a scratch or scripts/ path, deleted when the job is done. Commit it only when the user wants a repeatable setup path.""",
    [
        ("Writing the wizard shell by hand", "Use the provided template.sh - never hand-edit the shell library code. The consistency is the point."),
        ("Not reading existing config first", "Read .env, README, docker-compose, and workflow files to understand what values the wizard must capture."),
        ("Wizards that commit to the repo unnecessarily", "Most wizards are ephemeral - built for one run. Only commit if the procedure needs to be repeatable."),
    ],
    [
        "Manual procedure fully scoped",
        "All secrets/variables identified from .env and workflows",
        "template.sh used (not hand-rolled)",
        "Wizard generated and tested",
        "Ephemeral (not committed) unless user requests otherwise",
    ],
)

# ============================================================
# 22. writing-beats
# ============================================================
make("writing-beats",
    "Use when structuring raw writing material into beat-by-beat article journeys",
    ["writing", "content", "structure", "beats", "editing"],
    ["writing-fragments", "writing-shape", "writing-great-skills"],
    """Assemble raw material into a journey of beats, grounding each term before a beat leans on it. Choose-your-own-adventure article construction.

## The beat journey
1. **Establish prerequisites** - settle with the user what the audience already knows walking in. Concepts that are grounded from the start.
2. **Write 2-3 candidate starting beats** - each a different entry point into the article. Each may only lean on grounded concepts.
3. **User picks one** - write only that beat to the article file.
4. **Offer 2-3 candidate next beats** - different directions the journey could pivot to.
5. **Loop** until the article reaches a natural end.

## Grounding
Every concept has to be grounded before a beat can lean on it: the audience either walked in knowing it or met it in an earlier beat.""",
    [
        ("Starting with beats before grounding", "You must establish what the audience already knows before writing any beat. An ungrounded term loses the reader."),
        ("Too many candidate beats at each step", "Offer 2-3 per step, not more. Choice without overload keeps the process moving."),
        ("Writing multiple beats before user feedback", "Each beat should be written and shown before the next. Batching loses the interactive feedback."),
    ],
    [
        "Prerequisites established (what audience knows walking in)",
        "Starting beats offered (2-3 candidates)",
        "User picked a starting beat",
        "Each beat written to article file before next is offered",
        "Article reached natural conclusion",
    ],
)

# ============================================================
# 23. writing-fragments
# ============================================================
make("writing-fragments",
    "Use when generating raw writing fragments through exploratory interview",
    ["writing", "exploration", "fragments", "brainstorming", "content"],
    ["writing-beats", "writing-shape", "writing-great-skills"],
    """Widen the space of what could be written without committing to structure. Interview the user relentlessly and capture fragments.

## What is a fragment
A fragment is any piece of text that might survive into the final article. It must be readable by the author - the author can tell what it means - but it does not need to define its terms or be comprehensible to a cold reader.

Examples of fragments:
- A sharp sentence you would deploy somewhere but do not yet know where
- A claim with a one-line justification
- A vignette: a thing that happened, a code snippet, a scenario, an analogy
- A half-thought: something about how X feels like Y, work this out later
- A quote, a piece of dialogue, an overheard line
- A list of related observations that hang together by feel
- A leading word - a compact metaphor or coinage the whole piece can hang on

## Process
- Capture fragments from the very first thing the user says
- Append to a single markdown file
- On first write, put a single H1 with a working title and nothing else""",
    [
        ("Imposing structure too early", "This skill is pure exploration. If you find yourself outlining or imposing structure, switch to writing-shape or writing-beats."),
        ("Discarding fragments too quickly", "A fragment that seems weak now may be the anchor for the whole piece later. Capture everything."),
        ("Not capturing the user's initial prompt", "The first thing the user says often contains the seed of the entire piece. Capture it as the first fragment."),
    ],
    [
        "User interviewed to generate raw material",
        "Fragments appended from the very first thing said",
        "Working title set as H1",
        "No structure imposed",
        "Raw material file saved with captured fragments",
    ],
)

# ============================================================
# 24. writing-shape
# ============================================================
make("writing-shape",
    "Use when shaping raw material into a structured article paragraph by paragraph",
    ["writing", "editing", "structure", "shaping", "content"],
    ["writing-beats", "writing-fragments", "writing-great-skills"],
    """Shape raw material into an article paragraph by paragraph. The exploring is done - commit to a structure and mine the pile to fill it.

## The loop
1. **Read the pile** - read the input file end-to-end. Form a sense of what is in it.
2. **Establish the prerequisites** - settle with the user what the reader knows walking in.
3. **Draft 2-3 candidate openings** - each implying a different thesis or angle.
4. **Grow paragraph by paragraph** - after the opening lands, ask what the reader needs next. Pull material from the pile.
5. **Append to the article file as you go** - write each agreed paragraph immediately.

> **Important**: The input file is read-only to this skill. Create a separate article document.

Each block's format (paragraph, list, table, code block, callout, quote) should be a deliberate choice for the reader's experience.""",
    [
        ("Skipping the raw material read", "Read the input file end-to-end before doing anything else. Shaping without knowing what is in the pile produces shallow structure."),
        ("Editing the raw material file", "The input file is read-only to this skill. Create a separate article document."),
        ("Format decisions that are not deliberate", "Each block's format (paragraph, list, table, code block) should be a considered choice for the reader's experience."),
    ],
    [
        "Raw material read end-to-end",
        "Prerequisites established with user",
        "2-3 candidate openings drafted and shown",
        "User picked or composed an opening",
        "Article grown paragraph by paragraph from the pile",
    ],
)

# ============================================================
# 25. writing-great-skills
# ============================================================
make("writing-great-skills",
    "Use when writing or editing skill files for consistency and predictability",
    ["skills", "writing", "meta", "documentation", "best-practices"],
    ["skill-authoring-workflows", "skill-content-optimization", "wayfinder"],
    """A skill exists to wrangle determinism out of a stochastic system. Predictability - the agent taking the same process every run, not producing the same output - is the root virtue.

## Invocation choices
- **Model-invoked**: keeps a description so the agent can fire it autonomously. Contributes to context load.
- **User-invoked**: strips the description from the agent's reach. Zero context load, but spends cognitive load on the user.

## Writing the description
A model-invoked description does two jobs: state what the skill is, and list the branches that should trigger it. Every word increases context load.

## Skill structure
- Frontmatter with name, description, tags, related_skills
- Overview section
- Step-by-step workflow
- Common Pitfalls
- Code Examples (if applicable)
- Verification Checklist

> **Note**: This skill references GLOSSARY.md for defined terms. For Hermes Agent, the full skill-writing guidance is in the skill-authoring-workflows skill.""",
    [
        ("Overloading the description with detail", "Descriptions earn their space. Every word beyond the trigger branches increases context load."),
        ("Model-invocation when user-invocation suffices", "If a skill only fires by hand or from another skill, make it user-invoked to save context."),
        ("Router skills that go out of date", "If you add or remove skills, the router must be updated. Stale routers misdirect."),
    ],
    [
        "Description is 60 chars or fewer for system prompt window",
        "Description starts with 'Use when'",
        "Trigger phrases listed appropriately",
        "Model-invocation vs user-invocation chosen deliberately",
        "Common Pitfalls section included",
        "Verification Checklist included",
        "Code examples included if applicable",
    ],
)

# ============================================================
# 26. teach
# ============================================================
make("teach",
    "Use when teaching a user a new skill or concept across multiple sessions",
    ["teaching", "learning", "education", "mentoring", "documentation"],
    ["writing-great-skills", "to-questionnaire", "ubiquitous-language"],
    """Teach the user a new skill or concept across multiple sessions. Maintain a teaching workspace with missions, lessons, learning records, and reference materials.

## Teaching workspace structure
```
/
|- MISSION.md           - Why the user wants to learn this
|- RESOURCES.md         - Reference materials, links, sources
|- reference/*.html     - Cheat sheets, glossaries (print-friendly)
|- learning-records/    - 0001-what-was-learned.md
|- lessons/*.html       - Self-contained HTML lessons
|- assets/              - Reusable components, code files
```

## Session flow
1. Review MISSION.md and learning records to determine what the user knows
2. Find the zone of proximal development - what they are ready to learn next
3. Present new concept with concrete example and hands-on exercise
4. Capture key insight in a learning record
5. Update reference material if needed
6. Preview what comes next""",
    [
        ("Skipping the mission document", "The MISSION.md grounds all teaching in the user's reason for learning. Without it, lessons lack direction."),
        ("Teaching beyond the zone of proximal development", "Use learning records to track what the user knows and what they are ready for. Teaching things they are not ready for wastes effort."),
        ("Neglecting reference materials", "Reference materials (cheat sheets, glossaries) are what the user keeps after the session. Invest in making them beautiful and print-friendly."),
    ],
    [
        "MISSION.md created with user's learning goals",
        "RESOURCES.md populated with reference materials",
        "Reference materials created (cheat sheets, glossaries)",
        "Learning records capture non-obvious insights",
        "Lessons are self-contained HTML tied to the mission",
        "Zone of proximal development respected",
    ],
)

# ============================================================
# 27. git-guardrails-claude-code
# ============================================================
make("git-guardrails-claude-code",
    "Use when adding git safety hooks to prevent destructive operations in Claude Code",
    ["git", "safety", "hooks", "Claude-Code", "guardrails"],
    ["setup-pre-commit", "git-hooks-workflow", "git-config-essentials"],
    """Set up Claude Code hooks that block dangerous git commands (push, reset --hard, clean, branch -D) before they execute.

## What gets blocked
- `git push` (all variants including --force)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

## Setup steps
1. Ask scope: project-only (.claude/settings.json) or all projects (~/.claude/settings.json)
2. Copy the hook script to the appropriate location
3. Make it executable (chmod +x)
4. Add PreToolUse hook to settings.json
5. Verify by triggering a blocked command

> **Note**: This skill is designed for Claude Code's hook system. For Hermes Agent, adapt to use git config aliases or pre-commit hooks instead.""",
    [
        ("Missing execute permission on the hook script", "The block-dangerous-git.sh script must be chmod +x or it silently won't run."),
        ("Installing globally when project-only is appropriate", "Global hooks affect all Claude Code sessions. Only install globally if the user explicitly wants that."),
        ("Not testing the guardrails after installation", "Verify by triggering one of the blocked commands and confirming it is intercepted."),
    ],
    [
        "Scope confirmed (project or global)",
        "Hook script copied to correct location",
        "chmod +x applied to hook script",
        "Hook added to settings.json (PreToolUse)",
        "Guardrails verified with a test command",
    ],
)

# ============================================================
# 28. migrate-to-shoehorn
# ============================================================
make("migrate-to-shoehorn",
    "Use when migrating test files from 'as' assertions to @total-typescript/shoehorn",
    ["TypeScript", "testing", "migration", "shoehorn", "type-safety"],
    ["migrate-to-shoehorn", "code-review"],
    """Migrate test files from `as` type assertions to @total-typescript/shoehorn for type-safe partial test data.

## Why shoehorn?
`shoehorn` lets you pass partial data in tests while keeping TypeScript happy. It replaces `as` assertions with type-safe alternatives.

**Test code only.** Never use shoehorn in production code.

## Migration patterns
- Large objects with few needed properties: `as Type` -> `fromPartial()`
- Intentionally wrong types: `as unknown as Type` -> `fromAny()`

### Install
```bash
npm install @total-typescript/shoehorn
```""",
    [
        ("Shoehorn in production code", "Never use shoehorn (fromPartial, fromAny) in production code. It is for test files only."),
        ("Not installing the package first", "Run npm install @total-typescript/shoehorn before attempting migration."),
        ("fromAny where fromPartial would work", "Use fromPartial when you have a valid partial object, fromAny only when intentionally providing wrong types."),
    ],
    [
        "@total-typescript/shoehorn installed (npm)",
        "All `as Type` assertions in tests migrated to fromPartial()",
        "All `as unknown as Type` migrated to fromAny()",
        "Production code checked for shoehorn usage (should be none)",
        "Tests still passing after migration",
    ],
    """```typescript
// BEFORE: Using as assertions
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
};

getUser({ body: { id: "123" } } as Request);

// AFTER: Using fromPartial
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));

// Intentionally wrong types
// BEFORE:
getUser({ body: { id: 123 } } as unknown as Request);

// AFTER:
import { fromAny } from "@total-typescript/shoehorn";
getUser(fromAny({ body: { id: 123 } }));
```"""
)

# ============================================================
# 29. scaffold-exercises
# ============================================================
make("scaffold-exercises",
    "Use when creating exercise directory structures with problems, solutions, and explainers",
    ["scaffolding", "exercises", "education", "structure", "linting"],
    ["teach", "setup-matt-pocock-skills", "writing-great-skills"],
    """Create exercise directory structures that pass linting validation, then commit.

## Directory naming
- Sections: `XX-section-name/` inside exercises/
- Exercises: `XX.YY-exercise-name/` inside a section
- Names are dash-case (lowercase, hyphens)

## Exercise variants
Each exercise needs at least one subfolder:
- `problem/` - student workspace with TODOs
- `solution/` - reference implementation
- `explainer/` - conceptual material, no TODOs

## Required files
Each variant folder needs a non-empty readme.md with real content. If the subfolder has code, it also needs a main.ts (>1 line).

## Workflow
1. Parse the plan - extract section names, exercise names, and variant types
2. Create directories with mkdir -p
3. Create stub readmes with title and description
4. Run lint to validate
5. Fix any errors until lint passes""",
    [
        ("Empty readme files", "Each variant folder's readme.md must have real content. An empty or near-empty readme fails linting."),
        ("Wrong directory naming convention", "Sections are XX-section-name, exercises are XX.YY-exercise-name. Wrong naming fails the linter."),
        ("Not running lint after creation", "Always run the linter after scaffolding. Fix errors before committing."),
    ],
    [
        "Section directories follow XX-section-name convention",
        "Exercise directories follow XX.YY-exercise-name convention",
        "Each variant folder has non-empty readme.md",
        "Code files have main.ts if needed",
        "Lint passes",
    ],
)

# ============================================================
# 30. setup-pre-commit
# ============================================================
make("setup-pre-commit",
    "Use when setting up Husky pre-commit hooks with lint-staged and formatting",
    ["pre-commit", "hooks", "husky", "lint-staged", "prettier"],
    ["git-guardrails-claude-code", "git-hooks-workflow"],
    """Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repository.

## What this sets up
- Husky pre-commit hook
- lint-staged running Prettier on all staged files
- Prettier config (if missing)
- Typecheck and test scripts in the pre-commit hook

## Steps
1. Detect package manager (npm, pnpm, yarn, bun)
2. Install: husky, lint-staged, prettier as devDependencies
3. Initialize Husky: npx husky init
4. Create .husky/pre-commit with lint-staged, typecheck, and test
5. Create .lintstagedrc with Prettier config
6. Create .prettierrc if missing
7. Verify everything is working""",
    [
        ("Missing package manager detection", "Check for package-lock.json, pnpm-lock.yaml, yarn.lock, bun.lockb before installing. Defaulting to npm may add the wrong lockfile."),
        ("Husky v9 does not need a shebang", "For Husky v9+, the .husky/pre-commit file does not need a shebang line. Adding one may cause issues."),
        ("Not checking for existing typecheck/test scripts", "If the repo has no typecheck or test script, omit those lines from the hook and tell the user."),
    ],
    [
        "Package manager detected correctly",
        "husky, lint-staged, prettier installed as devDependencies",
        ".husky/pre-commit exists and is executable",
        ".lintstagedrc exists with Prettier configuration",
        ".prettierrc exists (or Prettier config detected)",
        "prepare script in package.json is 'husky'",
        "Hook runs formatting, typecheck, and test on commit",
    ],
)

# ============================================================
# 31. obsidian-vault
# ============================================================
make("obsidian-vault",
    "Use when searching, creating, or managing notes in an Obsidian vault",
    ["obsidian", "notes", "knowledge", "vault", "wikilinks"],
    ["note-taking", "ubiquitous-language", "domain-modeling"],
    """Search, create, and manage notes in an Obsidian vault with wikilinks and index notes for knowledge management.

## Vault conventions
- **Index notes**: aggregate related topics (e.g., "Ralph Wiggum Index", "Skills Index", "RAG Index")
- **Title case** for all note names
- No folders for organization - use links and index notes instead

## Linking
- Use Obsidian [[wikilinks]] syntax: [[Note Title]]
- Notes link to dependencies/related notes at the bottom
- Index notes are just lists of [[wikilinks]]

## Workflows
### Search for notes
Search by filename or content in the vault directory.

### Create a new note
Use Title Case for filename with content as a unit of learning. Add [[wikilinks]] to related notes at the bottom.

### Find related notes and backlinks
Search for [[Note Title]] across the vault to find backlinks.

> **Note**: The vault path is system-specific. Update the vault location for your environment.""",
    [
        ("Wrong vault path", "The vault path is system-specific. Always verify the vault location before creating or searching notes."),
        ("Not using wikilinks for navigation", "Obsidian relies on [[wikilinks]] for backlinks and graph view. Regular markdown links lose this functionality."),
        ("Creating too many nested folders", "The vault convention is flat with index notes, not nested folders. Fighting the convention makes notes hard to find."),
    ],
    [
        "Vault path verified",
        "Search returns expected results",
        "New notes use Title Case for filenames",
        "Notes linked with [[wikilinks]] syntax",
        "Index notes aggregate related topics",
    ],
    """```bash
# Search for notes by name
find "/path/to/obsidian/vault" -name "*.md" | grep -i "keyword"

# Search note content
grep -rl "keyword" "/path/to/obsidian/vault" --include="*.md"

# Find index notes
find "/path/to/obsidian/vault" -name "*Index*"

# Find backlinks for "Note Title"
grep -rl '\\[\\[Note Title\\]\\]' "/path/to/obsidian/vault"
```"""
)

print("\n=== All 31 skills generated successfully! ===")
