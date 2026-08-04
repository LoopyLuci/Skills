# Safely bridging into another application's live SQLite DB

Validated while wiring a VS Code extension to read/write the Hermes Desktop
app's `state.db` (WAL mode, ~70MB, actively written by the Desktop app). This
is the pattern for a second process ("bridge app") sharing ONE database whose
primary writer is another application.

## The safety model (critical)

1. **The owner app owns the DB.** The bridge must NEVER corrupt foreign rows.
2. **All reads go through a read-only, WAL-safe connection** that never locks
   the writer.
3. **All writes use a SHORT-LIVED separate read-write connection**, guarded by
   a long `busy_timeout`, wrapped in an explicit transaction, and filtered to
   rows the bridge itself created.

## node:sqlite usage (Node >= 22.5; confirmed available in VS Code 1.131 extension host = Node 24 / Electron 42)

```js
// READ-ONLY connection (never blocks the Desktop writer)
const db = new DatabaseSync(dbPath, { readOnly: true });
db.exec('PRAGMA busy_timeout = 5000;');
db.exec('PRAGMA query_only = ON;');   // belt-and-suspenders
const v = db.prepare('SELECT version FROM schema_version').get();

// SHORT-LIVED read-write connection for a single write op
function openRw(dbPath) {
  const c = new DatabaseSync(dbPath, { readOnly: false });
  c.exec('PRAGMA busy_timeout = 8000;');
  return c;
}
```

## Row isolation via a reserved source tag

The shared table has a `source` column (owner uses `'desktop'`). The bridge
writes ONLY rows with its own tag and gates every write on it, so the two apps'
data never collide and the bridge cannot mutate the owner's rows.

```sql
-- create: source = reserved tag (e.g. 'hermes_vscode')
INSERT INTO sessions (id, source, started_at, model, ...)
VALUES (?, 'hermes_vscode', ?, ?, ...);

-- rewrite messages transactionally, ONLY for our own session
BEGIN IMMEDIATE;
-- guard first: refuse if session isn't ours
SELECT id FROM sessions WHERE id = ? AND source = 'hermes_vscode';
DELETE FROM messages WHERE session_id = ?;
-- re-insert ...
UPDATE sessions SET message_count = ?, ended_at = ? WHERE id = ? AND source = 'hermes_vscode';
COMMIT;
```

Always `BEGIN IMMEDIATE` (acquire the write lock up front) and code a
`.prepared().run()` / `.get()` returning falsy → return false rather than
proceeding. Wrap errors with ROLLBACK and close the connection in `finally`.

## Check insert-safety BEFORE writing

`PRAGMA table_info(t)`, `PRAGMA index_list(t)`, and
`SELECT name, sql FROM sqlite_master WHERE type='trigger'` reveal NOT NULL
constraints, defaults, unique indexes, and FTS triggers that fire on your
inserts (you may need to satisfy `state_meta`-style high-water marks, or your
rows silently won't be searchable).

## Verification recipe (do NOT skip)

Write a throwaway test harness (not the product) that, against the LIVE DB:
1. Lists rows (read path).
2. Creates its own session, appends messages, renames, reads back, deletes.
3. Confirms the session + messages are gone after delete (cleanup verified).
4. Counts the owner's rows BEFORE vs AFTER and asserts they're unchanged.

This proves writes are isolated and clean up after themselves without a test DB.

## Pitfalls

- `node -e "..."` fails on Windows git-bash ("stdin is not a tty") — write a
  `.js` probe file and run `node scripts/x.js`.
- Don't assume dev Node == extension-host Node; probe `process.versions.node`,
  `process.versions.electron` and `typeof require('node:sqlite').DatabaseSync`
  at runtime and feature-detect with a fallback (e.g. `globalState`).
- An esbuild single-module bundle can time out cold (~40s); use
  `npx tsc file.ts --outDir <build> --module commonjs --target es2022 --esModuleInterop --skipLibCheck` to compile a single module for testing.
- `sqlite3.connect()` via `node -e` also hits the git-bash stdin issue — same
  fix: script file.