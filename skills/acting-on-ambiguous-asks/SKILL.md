---
name: acting-on-ambiguous-asks
description: Use when a user's request is a nudge, not an instruction.
version: 1
author: hermes-curator
license: MIT
metadata:
  hermes:
    tags: [workflow, communication, judgment, escalation]
    related_skills: [on-device-runtime-verification]
---

# Acting on ambiguous asks

This user escalates rather than specifies. When they send a short prompt after a
body of work, they are almost always telling you to keep going - not asking you
to re-plan.

## When to Use

- A short prompt lands after a long working stretch ("what is next?", "go ahead",
  "proceed", "ok").
- You have already delivered a plan and they reply with something equally short.
- The ask could be read as either "recommend" or "do".

## The core rule

**Pick the reading that makes progress, and say which one you chose.** A short
answer to a long working session reads as impatience with delay, not as a
request for another document.

## Procedure

1. **Decide the reading before composing anything.** Ask yourself whether you
   already know enough to act. If the previous turn ended with a ranked list,
   the user has read it; repeating it adds nothing.
2. **If you can act, act on the top item** and report what changed. Do not
   re-rank work they have already seen ranked.
3. **If you genuinely cannot act**, ask one specific question. Do not return a
   fifth version of a list they have read four times.
4. **If you were wrong earlier, correct it inline and move on.** A wrong claim
   costs more than the sentence spent fixing it.

## Pitfalls

- **Re-answering a question you just answered.** A repeated identical prompt is
  feedback, not a request for a longer answer. Treat the second and third
  repetition as a signal that you should have been executing.
- **Asking for permission to start work they already approved.** Approval given
  in a prior turn or by "proceed" covers the next reasonable step; re-asking
  reads as stalling.
- **Defending a plan instead of executing it.** If the user pushes past a plan,
  they have decided. Do not re-litigate.
- **Waiting for a scope decision that was never actually needed.** Choosing the
  obvious next step and naming the assumption beats blocking on a question whose
  answer is already implied.
- **Inferring capability limits that have not been tested.** Before reporting a
  platform or feature as unreachable, read the code for it. Claiming a client is
  behind on something it already supports wastes a cycle and costs credibility on
  every future claim.

## Verification

- [ ] The turn produced a change, a measurement, or a single specific question.
- [ ] It is not a restatement of a plan the user has already seen.
- [ ] Any assumption made instead of asking is named in the report.