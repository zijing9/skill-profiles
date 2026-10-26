"""CLI 契约测试（只读 + 护栏），不写任何数据。

运行：
    python -m unittest discover -s tests -v
或
    .\tests\run_tests.ps1
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "cli" / "skill.py"
PY = sys.executable


def run(*args):
    p = subprocess.run(
        [PY, str(CLI), *args],
        capture_output=True, text=True, encoding="utf-8",
    )
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def parse(s):
    try:
        return json.loads(s)
    except Exception:
        return None


class TestNames(unittest.TestCase):
    """技能名的校验边界：创建严格，引用宽松。"""

    def test_create_rejects_chinese(self):
        code, out, err = run("create", "中文名", "--yes")
        self.assertEqual(code, 2)
        self.assertEqual(parse(err)["error"]["code"], "INVALID_NAME")

    def test_cn_name_accepted_for_read(self):
        """已有中文名技能要能被查询（不能因英文名校验被拦）。"""
        code, out, err = run("history", "中文测试技能")
        # 允许 0（有记录）或 20（无记录），但不能是 2（校验失败）
        self.assertIn(code, (0, 20))

    def test_cn_name_accepted_for_get(self):
        code, out, err = run("get", "中文测试技能")
        self.assertIn(code, (0, 20))

    def test_path_traversal_still_blocked(self):
        for bad in ("../etc", "..", ".", "a/b", "a\\b"):
            code, out, err = run("history", bad)
            self.assertEqual(code, 2, f"{bad} 应被拒绝")
            self.assertEqual(parse(err)["error"]["code"], "INVALID_NAME")


class TestReadOnly(unittest.TestCase):
    def test_schema_has_all_commands(self):
        code, out, _ = run("schema")
        self.assertEqual(code, 0)
        spec = parse(out)
        names = [c["name"] for c in spec["commands"]]
        for must in ("list", "get", "create", "link", "delete", "rollback", "recover"):
            self.assertIn(must, names)
        self.assertEqual(spec["version"], "1.0.0")

    def test_roots_structure(self):
        code, out, _ = run("roots")
        self.assertEqual(code, 0)
        data = parse(out)
        self.assertIn("items", data)
        keys = [r["key"] for r in data["items"]]
        self.assertIn("hub", keys)
        self.assertIn("global", keys)

    def test_list_structure(self):
        code, out, _ = run("list", "--limit", "2")
        self.assertEqual(code, 0)
        data = parse(out)
        self.assertIn("items", data)
        self.assertIn("next", data)
        for it in data["items"]:
            for field in ("name", "status", "group", "links"):
                self.assertIn(field, it)

    def test_fields_projection(self):
        code, out, _ = run("list", "--limit", "1", "--fields", "name")
        self.assertEqual(code, 0)
        items = parse(out)["items"]
        if items:
            self.assertEqual(set(items[0].keys()), {"name"})

    def test_ndjson_output(self):
        code, out, _ = run("list", "--limit", "2", "--output", "ndjson")
        self.assertEqual(code, 0)
        lines = [l for l in out.splitlines() if l.strip()]
        self.assertTrue(all(parse(l) is not None for l in lines))

    def test_get_missing(self):
        code, out, err = run("get", "no-such-skill-xyz")
        self.assertEqual(code, 20)
        self.assertEqual(out, "")
        e = parse(err)["error"]
        for field in ("code", "message", "suggestion", "recoverable"):
            self.assertIn(field, e)

    def test_audit_structure(self):
        code, out, _ = run("audit", "--limit", "2")
        self.assertEqual(code, 0)
        data = parse(out)
        for key in ("checked", "risk", "findings", "disclaimer"):
            self.assertIn(key, data)
        self.assertIn(data["risk"], ("none", "low", "medium", "high"))

    def test_history_missing(self):
        code, out, err = run("history", "no-such-skill-xyz")
        self.assertEqual(code, 20)
        self.assertEqual(parse(err)["error"]["code"], "SKILL_NOT_FOUND")


class TestGuards(unittest.TestCase):
    def test_unknown_command(self):
        code, out, err = run("nonsense")
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertEqual(parse(err)["error"]["code"], "USAGE")

    def test_unknown_flag(self):
        code, _, err = run("list", "--nope")
        self.assertEqual(code, 2)
        self.assertEqual(parse(err)["error"]["code"], "USAGE")

    def test_bad_limit(self):
        code, _, err = run("list", "--limit", "abc")
        self.assertEqual(code, 2)

    def test_negative_offset(self):
        code, _, err = run("list", "--offset", "-5")
        self.assertEqual(code, 2)

    def test_create_requires_yes(self):
        code, out, err = run("create", "probe-name", "--desc", "这是一个足够长的描述用于测试")
        self.assertEqual(code, 2)
        self.assertEqual(parse(err)["error"]["code"], "CONFIRM_REQUIRED")

    def test_create_bad_name(self):
        code, _, err = run("create", "Bad Name", "--desc", "这是一个足够长的描述用于测试", "--yes")
        self.assertEqual(code, 2)
        self.assertEqual(parse(err)["error"]["code"], "INVALID_NAME")

    def test_create_short_desc(self):
        code, _, err = run("create", "ok-name", "--desc", "短", "--yes")
        self.assertEqual(code, 2)

    def test_dry_run_is_side_effect_free(self):
        code, out, _ = run("create", "probe-dry", "--desc", "这是一个足够长的描述用于测试", "--dry-run", "--yes")
        self.assertEqual(code, 0)
        self.assertTrue(parse(out)["dry_run"])
        self.assertFalse((ROOT / "data" / "hub" / "skills" / "probe-dry").exists())

    def test_path_traversal_rejected(self):
        code, _, err = run("get", "../../.ssh/id_rsa")
        self.assertEqual(code, 20)

    def test_link_bad_root(self):
        code, out, _ = run("list", "--limit", "1")
        items = parse(out)["items"] if out else []
        name = items[0]["name"] if items else "whatever"
        code, _, err = run("link", name, "--to", "Mars", "--yes")
        self.assertEqual(code, 20)
        self.assertEqual(parse(err)["error"]["code"], "ROOT_NOT_FOUND")


if __name__ == "__main__":
    unittest.main(verbosity=2)
