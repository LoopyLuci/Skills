# Pipelines for Large Content / Data Repositories

A repo whose primary artefact is a large collection of documents (skill
directories, markdown knowledge bases, datasets, catalogs) needs the same
skeleton as a code pipeline but different stage bodies. Do not bolt a code
pipeline onto it and accept thousands of pre-existing warnings — the pipeline
must be green on real errors and honest about content debt.

## Stage mapping

| Code-repo stage | Content-repo equivalent |
| --- | --- |
| static analysis | working-tree scans: compileall on first-party code, linter, secret/size/JSON checks |
| unit tests | tests for the validators themselves, plus any repo test suite |
| build | generate a machine-readable index of every content item |
| smoke | prove the index/archive works: parse, counts match directories, sample items parse, archive `testzip` |
| deploy | remote reachability + receipt; push only on explicit request |
| android / PyInstaller | drop, or replace with a package/archive step |

## Parallel content validation

Validating 10k items single-threaded is needlessly slow. Use a process pool
(`ProcessPoolExecutor`, `chunksize` ~64) with a top-level worker function so
Windows spawn works.

**Aggregate in the parent, not the workers.** A worker-local `set`/`dict`
(for duplicate detection, seen-names, global file indexes) is per-process and
silently misses every cross-item match. Have each worker return
`(findings, meta)` and let the parent build the global sets and emit
duplicate findings.

Pass read-only context (config, known-name set, repo file index) in the
payload; never share mutable state between workers.

## Severity tiers keep the pipeline green and useful

One severity for everything drowns real errors in legacy noise. Tier by path:

- **strict (error)** — the pipeline's own code and tests
- **warning** — legacy/utility scripts and vendored code
- **info** — content conventions (e.g. a tag equal to the item's own name)

A finding only fails the run at `error` tier. Warnings still appear in the
report with counts, so debt is visible without blocking.

## Secret heuristics: filter the obvious false positives

Pattern scanning over documentation and examples produces mostly false
positives. Split patterns into two groups:

- **high-signal** (key headers, cloud key prefixes, JWT shapes) — scan all text.
- **assignment-shaped** (`password = "..."`) — scan code extensions only.

Then discard a match when the captured value is:

- an environment-variable-shaped constant (`^[A-Z_][A-Z0-9_]{7,}$`) — it is a
  variable *name*, not a value;
- code-like (contains whitespace, `(`, `=`, `$`, `{`, `<`);
- contains a placeholder marker (`your-`, `xxx`, `example`, `changeme`,
  `placeholder`, `redact`, `dummy`, `sample`, `fake`, `test-`).

A scanner that fires on its own config file is a scanner that needs this
filter, not more patterns.

## Tests with no third-party packages

`pytest`/`xdist` may be absent. Run `unittest` discovery in a **subprocess** so
a runaway test is killed with its tree:

```bash
python -m unittest discover -s tests -t <repo-root> -v
```

`tests/` needs an `__init__.py` or discovery fails with "Start directory is
not importable". Parse `FAIL:`/`ERROR:` lines for test ids, re-run only those
ids once; a pass on rerun is a flake (warning), a second failure is real.

## Change-aware selection

Map changed top-level paths to stages, and let a content change pull the
index/smoke stages with it:

```
skills/* -> skills, build, smoke
ci/*, scripts/*, tests/* -> static, tests
```

No upstream / no changes means run everything. Print the selection and why.

## Reports, lock, hooks, scheduler

- Reports: `<ts>.json`, `latest.json`, `history.jsonl`, `<ts>.log`; prune to a
  configured limit.
- Lock: PID file; a live PID refuses a second run, a dead PID is taken over.
- Hooks: pre-commit runs preflight+static; pre-push runs the fast pipeline.
- Scheduler: `no_agent` cron jobs with a wrapper script under the Hermes
  scripts dir, `deliver: local` so green runs stay silent.

## Measured shape

~10k content directories / ~13k working-tree files on 12 cores:

```
preflight 0.5s | static 5.0s | content validation 3.1s (8 workers)
tests 0.4s | build 8.6s | smoke 1.1s | deploy 1.6s   ->  ~21s total
```
