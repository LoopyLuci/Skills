"""Pipeline stages. Each exposes run(ctx) -> StageResult."""

from . import preflight, static, skills, tests, build, smoke, deploy  # noqa: F401

STAGES = [
    ("preflight", preflight.run),
    ("static", static.run),
    ("skills", skills.run),
    ("tests", tests.run),
    ("build", build.run),
    ("smoke", smoke.run),
    ("deploy", deploy.run),
]

FAST_STAGES = ["preflight", "static", "skills", "tests"]
