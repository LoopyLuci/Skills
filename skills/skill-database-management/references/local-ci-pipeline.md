# Local CI/CD Pipeline — Stage Detail

Stdlib-only pipeline for the skill database repo (`python -m ci`). No third-party
Python packages. Config in `ci/config.json`; reports in `ci/reports/`, logs in `ci/logs/`.

## Stages (in order)

| Stage | What it does |
| --- | --- |
| `preflight` | Python version, git branch/commit/dirty state, origin remote, free disk, skills-dir count, tool availability, config sanity |
| `static` | `compileall`; `ruff` (strict on `ci/`+`tests/`, warnings on legacy `scripts/`); secret, bare-`except`, oversize-file and JSON-validity scans |
| `skills` | Parallel validation of every `skills/*/SKILL.md`: frontmatter keys, name == directory, license allowlist, tags, adapted-source attribution, cross-links resolve, referenced support files exist, no nested `.git`/`__pycache__`, size caps, duplicate bodies/descriptions, verbatim overlap vs upstream |
| `tests` | `unittest` discovery in a subprocess with a hard timeout, then a flaky rerun of only the failures |
| `build` | `dist/skills-index.json` (name, title, description, tags, license, source, file/byte counts) and a release archive |
| `smoke` | Artifact integrity: index parses, counts match directories, sampled skills parse, archive `testzip` |
| `deploy` | Remote reachability + `dist/deploy-receipt.json`; pushes only with `--push` on a clean tree |

## Severity policy

- `ci/` and `tests/` are first-party pipeline code → findings are **errors**.
- `scripts/` are legacy utilities → **warnings** (real bugs still surfaced).
- `skills/` is content, not first-party code → **warnings/info**.

## Change-aware selection

Without `--fast`/`--only`, changed paths map to stages. A `skills/` change also
selects `build` and `smoke`; a `ci/`/`scripts/`/`tests/` change also selects
`tests`; `preflight` always runs. No upstream or no changes means everything runs.

## Stability mechanisms

- **Lock**: `ci/.pipeline.lock` holds the running PID; a live PID refuses a second run, a dead PID is taken over.
- **Timeouts**: every command has one; on expiry the whole process tree is killed (`taskkill /T` on Windows).
- **Flaky rerun**: failing test ids are re-run once on their own; a pass there is reported as a flake, not a failure.
- **Reports**: `<ts>.json`, `latest.json`, `history.jsonl`, `<ts>.log`; old files pruned to configured limits.

## Automation

```bash
python -m ci.install_hooks     # pre-commit (preflight+static), pre-push (fast)
python -m ci.watch             # poll watcher, runs --fast on change
python -m ci.watch --once      # single run, for schedulers
```

Scheduled entry points shell out to `python -m ci` and deliver locally, so a green
run is silent and a failure surfaces.

## Documentation generation

`python -m ci --only build` writes `dist/skills-index.json`; run
`scripts/generate-docs-index.py` to regenerate `docs/skills-index.md` (every skill,
grouped by category, linked). Re-run both after any bulk import.

## Tuning

`ci/config.json` holds worker count, size caps, license allowlist, required
frontmatter keys, secret patterns, overlap thresholds, archive toggle, and prune
limits. Raise `max_findings_per_stage` when a report is truncated and you need the
full finding list.
