# claude-router evals

- `evals.json`: three routing scenarios, each a prompt plus the checks a good delegation plan must pass
  (skill-creator format). Run them with and without the skill and compare.
- `trigger-eval.json`: 20 requests marking whether the skill should open, for description tuning with
  `scripts/tune-skill-description.py` (local models only).

Last results: 16/16 checks with the skill, 15/16 without. The description scored 17/20 on the trigger
set with qwen2.5:14b as the judge, and no tuned rewrite beat it.
