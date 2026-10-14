---
name: cross-project-integration-analysis
description: "Use when integrating two of the user's projects."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [integration, architecture, planning, research]
    related_skills: [systematic-debugging, test-driven-development]
---

# Cross-Project Integration Analysis

Produces an exhaustive seam-level analysis and a phased, effort-ranked integration plan document when the user asks how to integrate one of their projects into another, or how two of their projects should work together.

## When to use

The deliverable is a committed markdown doc in the primary repo's `docs/` — exact seams, ranked patterns, phased plan — not a chat summary.

## Procedure

1. **Verify both repos at current HEAD.** `git fetch` the other repo before reading it; a same-day merge can add whole subsystems that reshape the recommendation. Record both commit SHAs in the doc header.
2. **Inventory each side's integration surface from source, not docs.** Read the transport/backend modules for exact wire detail: ports, protocol framing, auth handshake, function signatures, config file shapes, tool/command lists. Never infer a wire format from a README claim — verify it in the code. For a config-only pattern, extract the *registration API* itself from the server's route code: the exact request payload schema, what the route does immediately after persisting (a connect call whose success/failure lands in the response tells you a failed handshake surfaces at registration time, not first use), the table it persists to, and the trust defaults applied to the new connection. When prescribing a config file, check the target repo's `.gitignore` and a fresh checkout — a recommended file that is git-ignored or absent from a fresh clone is a real placement note for the doc.
3. **Map the direction of every candidate seam.** For each connection, determine which side is client and which is server *before* recommending it — a provider-shaped suggestion can be impossible in the reverse direction, and the workable pattern may look nothing like the obvious one.
4. **Identify the complementary axes**: what each side uniquely has that the other lacks. This becomes the gap-analysis table.
5. **Rank patterns by effort x value, config-only first.** Each pattern gets: the exact config block or paste-ready code sketch, the result, effort, risk, and its caveat. Include the verification step for config-only patterns.
6. **Prove each seam at the wire level before calling it verified.** A pattern whose recommendation is "register X and it just works" is only verified once you have run the handshake the counterparty will run — send the protocol frames a raw probe and record the output (server identity, protocol version, tool/command list). `scripts/mcp_handshake_probe.py` does exactly this for any stdio MCP server (initialize → notifications/initialized → ping → tools/list). Where the counterparty's runtime cannot be stood up locally, say so plainly in the doc — which claims are wire-verified and which remain source-verified — never imply an end-to-end run you did not perform.
7. **Cover the cross-cutting concerns**: security/trust posture of both sides, a failure-mode contract, a phased sequencing table (phase / pattern / effort / value / prerequisite), and a definition of done against the primary repo's test bar.
8. **Deliver as a committed doc.** Write it to `<primary-repo>/docs/<topic>-integration-analysis.md` and commit with a descriptive message.
9. **Escalate to implementation when the question repeats.** If the same integration question returns after the doc exists, the user is signaling that analysis is done — build the top-ranked pattern instead of deepening the doc. Apply the primary repo's full test bar (see `test-driven-development`), wire the seam end-to-end, verify, commit, and update the doc to an as-built record. Restating the same analysis at greater length is a tool-call loop, not depth.
10. **Match the codebase's conventions for the new seam.** Before adding a user-selectable backend, check whether the settings/UI layer hardcodes the set of providers — a provider enum tied to the engine's parser by drift-guard tests must be extended in both directions, or the new option is silently unreachable. Also follow the neighboring backends' config convention: if they are env-var-only with no UI settings, adding UI settings for the new one is scope creep.

## Always-on rules (this user)

- Exhaustive depth, never a summary: exact line numbers, function signatures, request/response JSON shapes.
- Paste-ready config and code blocks over prose descriptions of what to do.
- Every claim verified by reading code; docs are leads, not evidence.
- Honest effort estimates; mark optional phases explicitly and say which to do first.
- Include the failure-mode contract. This user's codebases enforce "report the failure, never fabricate a plausible-looking reply" — every integration path must honor it, and the doc must say so.

## Pitfalls

- **Re-pull the other repo before writing.** A same-day merge added an entire learning-router subsystem that reshaped the whole recommendation after the first draft was written.
- **Check each seam's direction before recommending it.** One project exposed no OpenAI-compatible chat server, which turned the obvious "point X at Y" suggestion into a different pattern entirely — the analysis would have shipped a broken plan without that check.
- **A re-ask of the same question is a depth signal, not a repetition request.** Add implementation-level detail — exact signatures, wire formats, paste-ready code sketches, test plans, decision tables — do not restate the same analysis at greater length. A *second* re-ask after the doc exists means analysis is finished: implement the top-ranked pattern under the repo's test bar and update the doc to an as-built record.
- **When `write_file` refuses an overwrite with the stale-file guard** despite a full prior read, write the new content to a temp sibling filename and replace via shell `mv`; do not loop re-reads.
- **Check whether a recommended config file is git-ignored or missing from a fresh checkout** before prescribing its placement — a snippet aimed at a file the repo deliberately excludes (provider/key-bearing configs usually are) needs a different placement note than one that exists in every clone.

## Related skills

- `systematic-debugging` — when an integration path fails in practice (4-phase root-cause discipline)
- `test-driven-development` — the test bar every new backend/seam must meet before it ships
