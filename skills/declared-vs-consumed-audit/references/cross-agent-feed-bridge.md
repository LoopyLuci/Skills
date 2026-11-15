# Cross-agent feed bridge

Recipe: turn a declared-but-unconsumed daemon route into a consumer, then prove it at the wire. Target schema and caps live in `agent-daemon/src/store/insight.ts` (`RecordSchema` + `ingestTelemetry`); the Python builder is `agent_sentinel/insight_ingest.py`.

## Step 1 — start the counterparty daemon on SQLite

The insight plane is SQLite-backed by default and needs no ClickHouse:

    cd /x/Projects/AgentSentinel/agent-daemon
    SQLITE_PATH=/x/Projects/AgentSentinel/agent-daemon/data/sentinel.db \
    STORE_BACKEND=sqlite HTTP_PORT=18080 API_TOKEN=agentsentinel-test-token \
    STORAGE_FS_DIR=/x/Projects/AgentSentinel/agent-daemon/data/snapshots \
    nohup node --import tsx src/server.ts > daemon_e2e.log 2>&1 &

Note: on Node v24 the repo's `npm start` (`node --loader tsx`) is a deprecation
failure; the working form is `node --import tsx`. Probe readiness:

    curl -s http://127.0.0.1:18080/api/v1/status \
      -H "Authorization: Bearer agentsentinel-test-token" -o /dev/null -w "%{http_code}"
    # expect 200 with "store":"sqlite"

## Step 2 — feed one record of each type

POST all three record kinds in one body so every route branch is exercised:

    curl -s http://127.0.0.1:18080/api/v1/telemetry \
      -H "Authorization: Bearer agentsentinel-test-token" \
      -H "Content-Type: application/json" \
      -d @insight_e2e.json

A body with one `trace_id`, one `step_id`, one `event_id` returns
`{"version":1,"accepted":3,"errors":[]}` when every branch landed.

## Step 3 — read the rows back

Confirm the typed tables actually grew. The insight tables are created by the
daemon's SQLite store (the `sqlite-store.ts` indexes), not by ClickHouse:

    sqlite3 agent-daemon/data/sentinel.db \
      "SELECT 'traces', COUNT(*) FROM insight_traces; SELECT 'decisions', COUNT(*) FROM insight_decisions; SELECT 'events', COUNT(*) FROM insight_events;"

Each query returns 1. If a table does not exist, the daemon did not create the
insight schema on SQLite — record that as a blocker, not a pass.

## Step 4 — build the bridge module

For each source agent, one record model with a `to_insight_*()` method returning
a dict containing exactly the target fields, plus a positional router driven by
field presence:

- `trace_id` present -> `insertInsightTrace`
- `step_id` present -> `insertInsightDecisionStep`
- `event_id` present -> `insertInsightBusEvent`

Accidentally emitting a type tag where the target assigns by presence is the most
common build error.

## Step 5 — mirror the caps and test them

The target `RecordSchema` hard-caps every string field. The bridge must preserve
(not silently truncate) long values, so the cap check is a test that builds a
record at the cap and asserts the length survives. Exact caps from the daemon's
`RecordSchema`:

| Field | Cap | |
|---|---|---|
| `trace_id` | 64 | `kind` 64 |
| `agent_id` | 200 | `parent_id` 64 |
| `scope` | 4096 | `model` 200 |
| `status` | 16 | `error` 5000 |
| `job_id` | 200 | `task_id` 200 |
| `request_json` | 1,000,000 | `timings_json` 1,000,000 |
| `resources_json` | 1,000,000 | `adapters_json` 1,000,000 |
| `meta_json` | 1,000,000 | `prompt` 500,000 |
| `rendered_prompt` | 1,000,000 | `answer` 1,000,000 |
| `reasoning` | 1,000,000 | `params_json` 1,000,000 |
| `token_count` | int non-negative | `bytes` int non-negative |

Test convention: build at the cap and assert the decoded value is the full
length — JSON-encoded fields come back quoted, so assert `json.loads(rec[..])`
is the full string rather than the encoded length.

## Step 6 — do not exempt

The surface is live because the consumer exists. If drift is flagged later, wire
the real call site; an allowlist entry names the consumer file, in the same
commit. An allowlist-only check silently lets a forgotten consumer pass.
