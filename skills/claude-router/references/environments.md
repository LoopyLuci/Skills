# Routing in each environment

Read the section for the environment you're in.

## Claude Code (CLI, desktop app, IDE)

- **Subagents:** the Agent tool takes a `model` parameter. Pass it on every call. Agent definitions in `.claude/agents/*.md` can set a default `model:` in their frontmatter, and a `model` on the call overrides it. A fork (`subagent_type: "fork"`) always runs on the current model, so fork only when the piece really needs the whole conversation.
- **Separate sessions (desktop app):** `start_session` takes `model`. Use it for "fresh" sessions; a "fork" session inherits the current model. To change a session already running, use `set_session_model`; it applies from that session's next turn.
- **Background tasks:** Bash with `run_in_background: true`. No model is involved; you're notified when it exits. Don't poll or sleep.
- **Worktrees:** give every session that writes code its own worktree (`use_worktree: true`, or `git worktree add` yourself), so two writers never share files.
- **Your own model:** you can't re-price your own turns. If this session itself should run on a different tier, ask the user to switch it in the model picker.

## claude.ai (web and apps)

There are no subagents or sessions to spawn, so routing becomes advice and structure:
- When a task has distinct parts, say which model suits each part, and offer to split the work into separate prompts or projects the user can run on that model.
- When the user picks the model per chat, suggest the tier at the start: "This is a mechanical reformat; Haiku will do it as well and faster."
- Projects and artifacts can hold the brief, so a part handed to another chat starts with its context.

## Claude API and Agent SDK

- Set `model` per request. Route each pipeline step separately: classification or extraction on Haiku, generation from a clear spec on Sonnet, planning and final review on Opus.
- Cascade: try the cheaper model with a validator (a JSON schema, a test, a checker prompt), and escalate only the items that fail. Log which tier handled each item, so the routing can be tuned with data.
- Use prompt caching for the long shared context every step repeats; it changes the cost picture more than the tier choice for long prompts.
- Look up current model ids and prices in the provider docs (or the claude-api skill) rather than from memory.
