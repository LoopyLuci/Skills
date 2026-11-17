# Brief template

Copy, fill in, and delete what doesn't apply. A brief that only makes sense with this conversation open is not finished.

```
Task: <what to build, fix or find, in your own words>

Where:
- repository / branch: <path or owner/name, branch to start from>
- files or areas: <exact paths>
- machine or drive constraints: <e.g. "never use C:", "runs on the box with the GPU">

Done looks like:
- <command> passes
- <file or behaviour> exists or works
- report back: <what to say: the branch, PR URL, numbers, what you couldn't do>

Constraints:
- <slow hooks: run commits in the background>
- <lockfile or install checks the hooks run>
- <secret scanning: use obviously fake values in tests>
- <things the user said must or must not happen>

Context: <why this matters, how it fits the larger work, decisions already made>
Model: <Haiku | Sonnet | Opus> because <one line>
```

## Worked example

```
Task: Add cluster status to the Cloudflare Worker: nodes post heartbeats, the dashboard shows them, and a Telegram
alert goes out when a node or training run stops reporting.

Where:
- repository: SmartMoneyNinja, branch feat/edge-worker, folder apps/edge
- follow the patterns in apps/edge/src (pure logic in modules with vitest tests, D1 through src/store.ts)

Done looks like:
- pnpm test and pnpm check pass in apps/edge
- an end-to-end check in wrangler dev: curl heartbeats in, see them at /admin/#cluster, make one go stale
- one commit pushed to feat/edge-worker; report what you could not finish

Constraints:
- the pre-commit hook takes minutes: commit in the background
- if the hook says node_modules doesn't match the lockfile, run pnpm install --frozen-lockfile and retry
- tests use fake values like "fake-key": the gitleaks scan flags realistic ones
- never print or commit real keys

Context: the machines sleep at night and a training run once stalled for hours unnoticed; the always-on Worker
is the one place that can notice and alert.
Model: Sonnet because it's a well-scoped build with a clear finish line.
```
