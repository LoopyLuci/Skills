# Hot SQLite backup verification

A verified backup is not a copied file; it is a file that `sqlite3` can open, read tables from, and restore. `sqlite3.Connection.backup()` is the safe method: it streams pages through SQLite's transaction mechanism, so the writer never needs to release the file lock (required for `shutil.copy2`).

Verification steps (in this order):
1. Call `sqlite3.connect()` on the backup file — if it raises, the backup is corrupt.
2. Read `sqlite_master WHERE type='table'` — if zero tables, something went wrong.
3. Read at least one expected table (`SELECT count(*) FROM sessions`) — if missing, the schema is broken.
4. Optionally restore to a temp DB and compare `PRAGMA quick_check`.

Keep only the 5 newest backups; clean older ones in the backup writer, not a separate cleanup script. If rotation is needed, it lives in the same method that creates the file (`backup_state_db`).
