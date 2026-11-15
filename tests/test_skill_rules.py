"""Tests for the skill validation rules used by the ci/ pipeline."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ci.skillcheck import check_skill, parse_frontmatter
from ci.util import load_config

VALID = """---
name: {name}
description: Demo skill for tests.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [demo, testing]
---

# {title}

Body text with a [link](../other/SKILL.md) and a reference to
[support](references/guide.md).
"""

CFG = load_config()


def make_ctx(known=None, adapted=None, sources=None):
    return {
        "config": CFG,
        "known_names": set(known or []),
        "adapted": dict(adapted or {}),
        "sources_dir": sources,
    }


class TestFrontmatter(unittest.TestCase):
    def test_parses_top_level_fields(self):
        fields, body = parse_frontmatter(VALID.format(name="demo", title="Demo"))
        self.assertEqual(fields["name"], "demo")
        self.assertEqual(fields["license"], "MIT")
        self.assertIn("Body text", body)

    def test_missing_frontmatter_raises(self):
        with self.assertRaises(ValueError):
            parse_frontmatter("# no frontmatter here\n")

    def test_quoted_values_unwrapped(self):
        fields, _ = parse_frontmatter('---\nname: "quoted"\ndescription: \'single\'\n---\n')
        self.assertEqual(fields["name"], "quoted")
        self.assertEqual(fields["description"], "single")


class TestCheckSkill(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self, name: str, text: str) -> Path:
        d = self.root / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(text, encoding="utf-8")
        return d

    def test_valid_skill_is_clean(self):
        d = self._write("demo", VALID.format(name="demo", title="Demo"))
        (d / "references").mkdir()
        (d / "references" / "guide.md").write_text("guide", encoding="utf-8")
        findings, meta = check_skill(d, make_ctx(known={"demo", "other"}))
        errors = [f for f in findings if f["severity"] == "error"]
        self.assertEqual(errors, [])
        self.assertEqual(meta["name"], "demo")

    def test_name_mismatch_is_error(self):
        d = self._write("demo", VALID.format(name="other-name", title="Demo"))
        findings, _ = check_skill(d, make_ctx(known={"demo"}))
        codes = {f["code"] for f in findings}
        self.assertIn("E_NAME_MISMATCH", codes)

    def test_missing_required_key(self):
        text = VALID.format(name="demo", title="Demo").replace("version: 1.0.0\n", "")
        d = self._write("demo", text)
        findings, _ = check_skill(d, make_ctx(known={"demo"}))
        codes = {f["code"] for f in findings}
        self.assertIn("E_KEY_MISSING", codes)

    def test_bad_license(self):
        text = VALID.format(name="demo", title="Demo").replace("license: MIT", "license: NOPE-1.0")
        d = self._write("demo", text)
        findings, _ = check_skill(d, make_ctx(known={"demo"}))
        self.assertIn("E_LICENSE", {f["code"] for f in findings})

    def test_broken_cross_link(self):
        d = self._write("demo", VALID.format(name="demo", title="Demo"))
        findings, _ = check_skill(d, make_ctx(known={"demo"}))
        self.assertIn("E_LINK", {f["code"] for f in findings})

    def test_missing_support_file_is_warning(self):
        d = self._write("demo", VALID.format(name="demo", title="Demo"))
        findings, _ = check_skill(d, make_ctx(known={"demo", "other"}))
        self.assertIn("E_SUPPORT", {f["code"] for f in findings})

    def test_self_tag_is_warning(self):
        text = VALID.format(name="demo", title="Demo").replace("tags: [demo, testing]",
                                                               "tags: [demo]")
        d = self._write("demo", text)
        findings, _ = check_skill(d, make_ctx(known={"demo"}))
        self.assertIn("E_SELFTAG", {f["code"] for f in findings})

    def test_nested_git_is_error(self):
        d = self._write("demo", VALID.format(name="demo", title="Demo"))
        (d / ".git").mkdir()
        findings, _ = check_skill(d, make_ctx(known={"demo"}))
        self.assertIn("E_NESTED", {f["code"] for f in findings})

    def test_overlap_flags_close_copy(self):
        upstream = self.root / "upstream.md"
        upstream.write_text(VALID.format(name="demo", title="Demo"), encoding="utf-8")
        d = self._write("demo", VALID.format(name="demo", title="Demo"))
        ctx = make_ctx(known={"demo"}, adapted={"demo": "upstream.md"}, sources=self.root)
        findings, _ = check_skill(d, ctx)
        self.assertIn("W_OVERLAP", {f["code"] for f in findings})

    def test_adapted_requires_source(self):
        d = self._write("demo", VALID.format(name="demo", title="Demo"))
        ctx = make_ctx(known={"demo"}, adapted={"demo": "upstream.md"})
        findings, _ = check_skill(d, ctx)
        self.assertIn("E_SOURCE", {f["code"] for f in findings})

    def test_adapted_accepts_nested_source(self):
        text = VALID.format(name="demo", title="Demo").replace(
            "    tags: [demo, testing]",
            "    tags: [demo, testing]\n    source: upstream/repo")
        d = self._write("demo", text)
        ctx = make_ctx(known={"demo"}, adapted={"demo": "upstream.md"})
        findings, _ = check_skill(d, ctx)
        self.assertNotIn("E_SOURCE", {f["code"] for f in findings})

    def test_support_file_anywhere_in_repo_is_ok(self):
        d = self._write("demo", VALID.format(name="demo", title="Demo"))
        ctx = make_ctx(known={"demo", "other"})
        ctx["repo_files"] = {"references/guide.md"}
        findings, _ = check_skill(d, ctx)
        self.assertNotIn("E_SUPPORT", {f["code"] for f in findings})

    def test_self_tag_is_info_not_warning(self):
        text = VALID.format(name="demo", title="Demo").replace("tags: [demo, testing]",
                                                               "tags: [demo]")
        d = self._write("demo", text)
        findings, _ = check_skill(d, make_ctx(known={"demo"}))
        match = [f for f in findings if f["code"] == "E_SELFTAG"]
        self.assertTrue(match)
        self.assertEqual(match[0]["severity"], "info")


if __name__ == "__main__":
    unittest.main()
