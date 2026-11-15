"""Tests for pipeline orchestration units (planning, locking, pruning)."""

from __future__ import annotations

import json
import tempfile
import time
import unittest
from pathlib import Path

from ci.pipeline import Lock, _prune, plan_stages, select_by_changes
from ci.util import REPORTS_DIR


class _Args:
    def __init__(self, **kw):
        self.full = kw.get("full", False)
        self.fast = kw.get("fast", False)
        self.only = kw.get("only")
        self.list = kw.get("list", False)
        self.push = kw.get("push", False)
        self.no_deploy = kw.get("no_deploy", False)
        self.changed_only = kw.get("changed_only", False)


class TestPlanning(unittest.TestCase):
    def test_fast_is_subset(self):
        self.assertEqual(plan_stages(_Args(fast=True), {}, lambda m: None),
                         ["preflight", "static", "skills", "tests"])

    def test_full_runs_everything(self):
        names = plan_stages(_Args(full=True), {}, lambda m: None)
        self.assertIn("deploy", names)
        self.assertEqual(len(names), 7)

    def test_only_filters_and_validates(self):
        self.assertEqual(plan_stages(_Args(only="skills,tests"), {}, lambda m: None),
                         ["skills", "tests"])
        with self.assertRaises(SystemExit):
            plan_stages(_Args(only="bogus"), {}, lambda m: None)


class TestChangeSelection(unittest.TestCase):
    def test_skill_change_pulls_build_and_smoke(self):
        stages = ["preflight", "static", "skills", "tests", "build", "smoke", "deploy"]
        picked = select_by_changes(["skills/demo/SKILL.md"], stages, lambda m: None)
        self.assertIn("skills", picked)
        self.assertIn("build", picked)
        self.assertIn("smoke", picked)

    def test_no_changes_runs_all(self):
        stages = ["preflight", "skills", "deploy"]
        self.assertEqual(select_by_changes([], stages, lambda m: None), stages)


class TestLock(unittest.TestCase):
    def test_acquire_then_refuse_then_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock = Lock(Path(tmp) / "lock.json")
            ok, _ = lock.acquire()
            self.assertTrue(ok)
            second = Lock(Path(tmp) / "lock.json")
            ok2, msg = second.acquire()
            self.assertFalse(ok2)
            self.assertIn("already running", msg)
            lock.release()
            third = Lock(Path(tmp) / "lock.json")
            self.assertTrue(third.acquire()[0])
            third.release()


class TestPrune(unittest.TestCase):
    def test_keeps_newest(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            for i in range(5):
                p = d / f"{i}.json"
                p.write_text("{}", encoding="utf-8")
                p.touch()
                time.sleep(0.01)
            _prune(d, 2, ".json")
            self.assertEqual(len(list(d.glob("*.json"))), 2)


class TestReportsDir(unittest.TestCase):
    def test_reports_dir_exists(self):
        self.assertTrue(REPORTS_DIR.name == "reports")


class TestConfig(unittest.TestCase):
    def test_config_is_complete(self):
        from ci.util import load_config

        cfg = load_config()
        for key in ("skills_dir", "required_frontmatter", "allowed_licenses",
                    "jobs", "max_file_mb"):
            self.assertIn(key, cfg)
        self.assertIsInstance(json.dumps(cfg), str)


class TestStaticHelpers(unittest.TestCase):
    def test_code_like_filters_env_constants(self):
        from ci.stages.static import _code_like

        self.assertTrue(_code_like('TOKEN = "APEXLANG_LOCAL_CHECK_OK"'))
        self.assertTrue(_code_like('ENV_API_KEY = "COMFY_CLOUD_API_KEY"'))
        self.assertTrue(_code_like('TOKEN = line.split("=", 1)[1].strip()'))

    def test_real_credential_assignment_is_not_code_like(self):
        from ci.stages.static import _code_like

        self.assertFalse(_code_like('api_key = "9f8b7c6d5e4f3a2b1c0d"'))
        self.assertFalse(_code_like("password = 's3cr3t-passphrase!'"))


if __name__ == "__main__":
    unittest.main()
