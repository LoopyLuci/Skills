# Local On-Device CI/CD Pipeline

A fully custom, self-contained pipeline for this repository. No cloud runners, no
third-party Python packages — stdlib only, so it runs on a bare Python install.

## Stages (in order)

| Stage | What it does |
| --- | --- |
| `preflight` | Python version, git state (branch/commit/dirty), origin remote, free disk, skills-dir count, tool availability (`git`, optional `ruff`), config sanity |
| `static` | `compileall` on `ci/ scripts/ tests/`, `ruff check` (E9,F63,F7,F82,B006,B008) when installed, bare-`except` detection, secret-pattern scan, oversize-file detection, JSON validity — all scoped to the working tree, never history |
| `skills` | Parallel validation of every `skills/*/SKILL.md`: frontmatter required keys, `name` == directory, license allowlist, tags present and not self-referential, source attribution for adapted skills, relative cross-links resolve, referenced support files exist, no nested `.git`/`__pycache__`, size caps, duplicate body/description detection, and verbatim-overlap detection against `_sources/` for adapted skills |
| `tests` | `unittest` discovery in a subprocess (hard timeout, tree-killed on expiry), then a flaky rerun of only the failures |
| `build` | `dist/skills-index.json` (every skill's name, title, description, tags, license, source, file/byte counts) and, when enabled, a release zip |
| `smoke` | Proves the artifacts work: index parses, count matches directories, 50 sampled skills parse, archive integrity via `testzip` |
| `deploy` | Verifies `origin/<branch>` is reachable, records `dist/deploy-receipt.json`, and pushes only with `--push` on a clean tree |

## Usage

```bash
python -m ci --full              # every stage
python -m ci --fast              # preflight, static, skills, tests
python -m ci --only skills tests # specific stages
python -m ci --list              # show the plan
python -m ci --full --push       # also push after a green deploy
python -m ci --full --no-deploy  # skip deploy
python -m ci --fast --jobs 4     # worker override
python -m ci --changed-only      # validate only skill dirs touched by the working tree
```

Exit code is `0` when every executed stage passes, `1` when any fails, `2` when
another pipeline instance holds the lock.

## Change-aware by default

Without `--fast`/`--only`, the pipeline maps changed paths to stages (a `skills/`
change also refreshes `build` and `smoke`; a code change runs `tests`), so a small
edit does not pay for the whole sweep. No upstream or no changes means everything runs.

## Safety and stability

- **Lock**: `ci/.pipeline.lock` holds the running PID; a live PID refuses a second run, a dead PID is taken over.
- **Timeouts**: every command has a timeout; on expiry the whole process tree is killed (`taskkill /T` on Windows).
- **Flaky rerun**: failing tests are re-run once on their own; a pass there is reported as a flake, not a failure.
- **Reports**: `ci/reports/<timestamp>.json`, `ci/reports/latest.json`, `ci/reports/history.jsonl`, and `ci/logs/<timestamp>.log`; old files are pruned to the configured limits.
- **Configuration**: `ci/config.json` — thresholds, allowlists, secret patterns, worker count, archive toggle.

## Automation

```bash
python -m ci.install_hooks     # pre-commit (preflight+static) and pre-push (fast) hooks
python -m ci.watch             # poll watcher: runs --fast when anything changes
python -m ci.watch --once      # single run, useful for a scheduler
```

Scheduled Hermes cron jobs (all `no_agent`, delivering locally, so a green run is
silent and a failure surfaces):

| Job | Schedule | Scope |
| --- | --- | --- |
| `skills-ci-fast` (`2c9b5a08dbf2`) | every 60 m | fast pipeline |
| `skills-ci-full-daily` (`8a6a1c097217`) | daily 03:00 | full pipeline incl. build/archive |
| `skills-sync-hermes-repo` | every 30 m | Hermes ↔ repo synchronisation |

The scheduled entry points live in `~/AppData/Local/hermes/scripts/`
(`skills-ci.py`, `skills-ci-full.py`) and shell out to `python -m ci` in this
directory.

## Documentation generation

`python -m ci --only build` writes `dist/skills-index.json`; feed it to
`scripts/generate-docs-index.py` to regenerate `docs/skills-index.md` (every
skill, grouped by category).

## Tests

`tests/` holds unit tests for the validation rules and the orchestration units.
They run as the `tests` stage and need nothing beyond the standard library.
