#!/usr/bin/env python
"""skill —— 技能仓库的命令行接口（主要给 AI agent 用）。

契约见同目录 cli.spec.json。要点：
  - stdout 只放 JSON；错误走 stderr + 非零退出码
  - 写操作必须带 --yes；全部支持 --dry-run
  - 不依赖服务进程，直接操作 data/hub 与各挂载位置

用法：python cli/skill.py <command> [args]
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import shutil
import stat
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from core import linker, scanner  # noqa: E402
from core.store import Store  # noqa: E402

CLI_VERSION = "1.0.0"

HUB = BASE / "data" / "hub"
TRASH = BASE / "data" / "trash"
CONFIG_PATH = BASE / "data" / "config.json"
USER_SKILLS = Path.home() / ".dsh" / "skills"
DEFAULT_WORKSPACE_PARENT = ""   # 空 = 首次启动让用户选目录

SPEC_PATH = Path(__file__).resolve().parent / "cli.spec.json"

TRASH_DAYS = 10
NAME_MAX = 64
DESC_MIN = 20
DESC_MAX = 1000
SIZE_MAX_KB = 200

# 退出码
EX_OK = 0
EX_FAIL = 1
EX_USAGE = 2
EX_NOT_FOUND = 20
EX_EXISTS = 21
EX_PRECOND = 22
EX_EXTERNAL = 30


class CliError(Exception):
    def __init__(self, code: str, message: str, suggestion: str, exit_code: int, recoverable: bool = False):
        super().__init__(message)
        self.code = code
        self.message = message
        self.suggestion = suggestion
        self.exit_code = exit_code
        self.recoverable = recoverable


# ---------------- 输出层 ----------------
def emit(data, fields=None, mode="json"):
    if fields:
        if isinstance(fields, str):
            fields = [f.strip() for f in fields.split(",") if f.strip()]
        data = project(data, fields)
    if mode == "ndjson":
        rows = data.get("items") if isinstance(data, dict) else data
        if not isinstance(rows, list):
            rows = [data]
        for row in rows:
            print(json.dumps(row, ensure_ascii=False))
        return
    print(json.dumps(data, ensure_ascii=False, indent=2))


def load_json_payload(value):
    """--json '<payload>' | @file | - 。返回 dict。"""
    if value is None:
        return {}
    if value == "-":
        raw = sys.stdin.read()
    elif value.startswith("@"):
        p = Path(value[1:])
        if not p.exists():
            raise CliError("USAGE", f"--json 文件不存在：{p}", f"检查路径 {p}", EX_USAGE)
        raw = p.read_text(encoding="utf-8-sig")
    else:
        raw = value
    try:
        data = json.loads(raw)
    except Exception as e:
        raise CliError(
            "USAGE",
            f"--json 解析失败：{e}",
            "Windows 的命令行容易被引号破坏，改用 --json @payload.json（推荐）或 --json - 从 stdin 读",
            EX_USAGE,
        )
    if not isinstance(data, dict):
        raise CliError("USAGE", "--json 必须是对象", '例如 {"name":"my-skill","desc":"..."}', EX_USAGE)
    return data


def project(obj, fields):
    if isinstance(obj, dict) and "items" in obj:
        items = []
        for it in obj.get("items") or []:
            items.append({k: it.get(k) for k in fields if k in it})
        out = dict(obj)
        out["items"] = items
        return out
    if isinstance(obj, list):
        return [{k: it.get(k) for k in fields if k in it} for it in obj]
    if isinstance(obj, dict):
        return {k: obj.get(k) for k in fields if k in obj}
    return obj


def fail(code: str, message: str, suggestion: str, exit_code: int, recoverable: bool = False):
    err = {
        "error": {
            "code": code,
            "message": message,
            "suggestion": suggestion,
            "recoverable": recoverable,
        }
    }
    print(json.dumps(err, ensure_ascii=False), file=sys.stderr)
    sys.exit(exit_code)


def human_list(items, cols):
    if not items:
        print("（空）")
        return
    widths = {c: max(len(c), *(len(str(it.get(c, ""))) for it in items)) for c in cols}
    print("  ".join(c.ljust(widths[c]) for c in cols))
    print("  ".join("-" * widths[c] for c in cols))
    for it in items:
        print("  ".join(str(it.get(c, "")).ljust(widths[c]) for c in cols))


# ---------------- 基础 ----------------
def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
        except Exception:
            pass
    return {"workspaces": [], "theme": "black", "port": 8765}


def agents_config() -> dict:
    cfg = load_config()
    a = cfg.get("agents") or {}
    if not isinstance(a, dict):
        a = {}
    a.setdefault("dsh", {
        "label": "DSH",
        "hubDir": "data/hub",
        "globalSkillsDir": "~/.dsh/skills",
        "workspaceParent": DEFAULT_WORKSPACE_PARENT,
    })
    return a


def active_agent() -> str:
    aid = (load_config().get("activeAgent") or "dsh").strip()
    return aid if aid in agents_config() else "dsh"


def hub_dir_for(agent_id: str) -> Path:
    """仓库对所有 agent 通用，保留签名兼容调用方。"""
    return DATA / "hub"


def global_skills_dir() -> Path:
    """全局技能目录；config.json 的 globalSkillsDir 可覆盖。"""
    v = (load_config().get("globalSkillsDir") or "").strip()
    if v:
        try:
            return Path(os.path.expanduser(v))
        except Exception:
            pass
    return USER_SKILLS


def workspace_parent() -> Path:
    """工作区父目录；config.json 的 workspaceParent 可覆盖。"""
    v = (load_config().get("workspaceParent") or "").strip()
    if v:
        try:
            return Path(os.path.expanduser(v))
        except Exception:
            pass
    return Path(DEFAULT_WORKSPACE_PARENT)


def discover_workspaces() -> list:
    seen = list(load_config().get("workspaces", []))
    parent = workspace_parent()
    if parent.is_dir():
        for d in sorted(parent.iterdir()):
            if d.is_dir() and (d / ".dsh" / "skills").is_dir() and str(d) not in seen:
                seen.append(str(d))
    return seen


OTHER_AGENT_GLOBALS = [
    ("global:claude", "Claude Code", ".claude"),
    ("global:codex", "Codex", ".codex"),
    ("global:cursor", "Cursor", ".cursor"),
]


def all_roots() -> list:
    out = [
        {"key": "hub", "label": "SKILL仓库", "kind": "hub", "agent": None, "path": str(HUB / "skills")},
        {"key": "global", "label": "全局SKILL", "kind": "global", "agent": "dsh",
         "path": str(global_skills_dir())},
    ]
    for key, label, dirname in OTHER_AGENT_GLOBALS:
        p = Path.home() / dirname / "skills"
        if p.is_dir():
            out.append({"key": key, "label": label, "kind": "global",
                        "agent": dirname.lstrip("."), "path": str(p)})
    for item in load_config().get("skillRoots", []) or []:
        try:
            p = Path(os.path.expanduser(str(item.get("path") or "")))
            key = (item.get("key") or "").strip()
            if not key or not p.is_dir():
                continue
            out.append({
                "key": key,
                "label": item.get("label") or key,
                "kind": item.get("kind") or "global",
                "agent": item.get("agent") or "custom",
                "path": str(p),
            })
        except Exception:
            continue
    for ws in discover_workspaces():
        p = Path(ws)
        out.append({
            "key": "ws:" + p.name,
            "label": p.name,
            "kind": "workspace",
            "agent": "dsh",
            "path": str(p / ".dsh" / "skills"),
            "workspace": str(p),
        })
    return out


def resolve_root(value: str, allow_hub: bool = True) -> dict:
    v = (value or "").strip()
    if not v:
        raise CliError("ROOT_NOT_FOUND", "缺少位置参数", "skill roots", EX_USAGE)
    cands = all_roots()
    if not allow_hub:
        cands = [c for c in cands if c["kind"] != "hub"]
    matches = []
    for r in cands:
        if v == r["key"] or v == r["label"] or ("ws:" + v) == r["key"]:
            matches.append(r)
    if not matches:
        low = v.lower()
        matches = [r for r in cands if r["label"].lower() == low or r["key"].lower() == low]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        hint = "、".join(r["key"] for r in cands)
        raise CliError("ROOT_NOT_FOUND", f"位置「{v}」不存在", f"可用位置：{hint}（skill roots）", EX_NOT_FOUND)
    hint = "、".join(r["key"] for r in matches)
    raise CliError("ROOT_AMBIGUOUS", f"位置「{v}」匹配到多个", f"改用完整名字：{hint}", EX_USAGE)


def check_name(name: str):
    import re
    n = (name or "").strip()
    if not n or len(n) > NAME_MAX or not re.match(r"^[a-z0-9][a-z0-9-]{0,63}$", n):
        raise CliError(
            "INVALID_NAME",
            f"技能名「{name}」不合法",
            "英文名只能用小写字母、数字和连字符，例如 my-skill",
            EX_USAGE,
        )
    return n


def dir_stats(path: Path):
    n = 0
    total = 0
    latest = 0.0
    if path.is_dir():
        for root, _dirs, files in os.walk(path):
            for f in files:
                n += 1
                fp = Path(root) / f
                try:
                    total += fp.stat().st_size
                    latest = max(latest, fp.stat().st_mtime)
                except OSError:
                    pass
    return n, total // 1024, latest


def iso_time(ts: float) -> str:
    if not ts:
        return ""
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(ts))


def read_skill_file(path: Path) -> str:
    f = path / "SKILL.md"
    if not f.exists():
        return ""
    return f.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    block = text[3:end]
    meta = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v.startswith(('"', "'")) and v[-1:] == v[:1] and len(v) > 1:
                v = v[1:-1]
            meta[k] = v
    body = text[end + 4:]
    if body.startswith("\n"):
        body = body[1:]
    return meta, body


def build_skill_md(name: str, zh: str, desc: str, body: str) -> str:
    lines = ["---", f"name: {name}"]
    if zh:
        lines.append(f"name_zh: {zh}")
    lines.append(f"description: {desc}")
    lines.extend(["---", "", body.strip() or f"# {zh or name}", ""])
    return "\n".join(lines)


# ---------------- 扫描 ----------------
def collect_skills() -> dict:
    """扫描 hub 与各挂载位置，返回 {name: 条目}。与 app.py 的 build_state 保持一致。"""
    store = Store(HUB)
    man = store.all()
    entries = {}

    hub_dir = HUB / "skills"
    if hub_dir.is_dir():
        for d in sorted(hub_dir.iterdir()):
            if not d.is_dir() or d.name.startswith("."):
                continue
            fm = scanner.read_frontmatter(d / "SKILL.md")
            n, kb, mt = dir_stats(d)
            entries[d.name] = {
                "name": d.name,
                "nameZh": fm.get("name_zh", ""),
                "desc": fm.get("description", ""),
                "status": "unlinked",
                "group": "hub",
                "links": [],
                "path": str(d),
                "sizeKb": kb,
                "files": n,
                "mtime": iso_time(mt),
                "mtimeTs": mt,
                "pinned": bool((man.get(d.name) or {}).get("pinned")),
            }

    for r in all_roots():
        if r["kind"] == "hub":
            continue
        rp = Path(r["path"])
        if not rp.is_dir():
            continue
        for d in sorted(rp.iterdir()):
            if not d.is_dir() or d.name.startswith("."):
                continue
            fm = scanner.read_frontmatter(d / "SKILL.md")
            name = fm.get("name") or d.name
            entry = entries.get(name)
            if entry is None:
                n, kb, mt = dir_stats(d)
                entry = {
                    "name": name,
                    "nameZh": fm.get("name_zh", ""),
                    "desc": fm.get("description", ""),
                    "status": "local",
                    "group": r["key"],
                    "links": [],
                    "path": str(d),
                    "sizeKb": kb,
                    "files": n,
                    "mtime": iso_time(mt),
                    "mtimeTs": mt,
                    "pinned": bool((man.get(name) or {}).get("pinned")),
                }
                entries[name] = entry
            link = {
                "key": r["key"],
                "label": r["label"],
                "path": str(d),
                "dead": scanner.is_link(d) and not (d / "SKILL.md").exists(),
            }
            entry["links"].append(link)
            if link["dead"]:
                entry["status"] = "dead"
            elif entry["status"] in ("unlinked", "local"):
                entry["status"] = "linked"
                entry["group"] = r["key"]
    return entries


def get_entry(name: str) -> dict:
    entries = collect_skills()
    if name not in entries:
        raise CliError(
            "SKILL_NOT_FOUND",
            f"技能「{name}」不存在",
            "skill list --limit 50",
            EX_NOT_FOUND,
        )
    return entries[name]


# ---------------- git ----------------
def git_repo():
    """打开 hub 的 git 仓库；不存在时报明确的错误而不是裸异常。"""
    from dulwich.repo import Repo
    if not (HUB / ".git").exists():
        raise CliError(
            "GIT_FAILED",
            "仓库还没初始化",
            "先执行任意写操作（如 skill create）或 skill list 触发初始化",
            EX_EXTERNAL,
        )
    return Repo(str(HUB))


def find_commit(sha: str):
    try:
        repo = git_repo()
    except Exception as e:
        raise CliError("GIT_FAILED", f"仓库不可用：{e}", "检查 data/hub/.git 是否存在", EX_EXTERNAL)
    s = (sha or "").strip()
    if not s:
        raise CliError("COMMIT_NOT_FOUND", "缺少 --commit", "skill history <name> 查看可用提交", EX_USAGE)
    for entry in repo.get_walker():
        c = entry.commit
        if c.id.decode().startswith(s):
            return c
    raise CliError("COMMIT_NOT_FOUND", f"找不到提交 {s}", "skill history <name> 查看可用提交", EX_NOT_FOUND)


def commit_skill_files(commit, name: str) -> dict:
    """取某提交里 skills/<name>/ 下的文件，返回 {相对路径: bytes}。"""
    repo = git_repo()
    out = {}
    prefix = f"skills/{name}/".encode()

    def walk(tree_sha, base: bytes):
        tree = repo.get_object(tree_sha)
        for entry in tree.iteritems():
            fname, mode, sha = entry
            path = base + fname
            if stat.S_ISDIR(mode):
                walk(sha, path + b"/")
            else:
                if path.startswith(prefix):
                    out[path.decode("utf-8")] = repo.get_object(sha).data

    walk(commit.tree, b"")
    if not out:
        raise CliError(
            "COMMIT_NOT_FOUND",
            f"提交 {commit.id.decode()[:8]} 里没有技能 {name}",
            f"skill history {name}",
            EX_NOT_FOUND,
        )
    return out


def commit_history_for(name: str, limit: int = 20) -> list:
    try:
        repo = git_repo()
    except CliError:
        return []
    out = []
    for entry in repo.get_walker():
        c = entry.commit
        msg = c.message.decode("utf-8", "replace").strip()
        if name in msg or f"skills/{name}/" in msg:
            out.append({
                "commit": c.id.decode()[:8],
                "time": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(c.commit_time)),
                "message": msg,
            })
            if len(out) >= limit:
                break
    return out


# ---------------- 回收站 ----------------
def trash_entries() -> list:
    items = []
    if not TRASH.is_dir():
        return items
    now = time.time()
    for d in sorted(TRASH.iterdir()):
        if not d.is_dir():
            continue
        meta_file = d / "_trash.json"
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
        except Exception:
            meta = {"name": d.name.split("__")[0], "deletedAt": d.stat().st_mtime}
        age = now - float(meta.get("deletedAt") or 0)
        if age > TRASH_DAYS * 86400:
            shutil.rmtree(d, ignore_errors=True)
            continue
        items.append({
            "id": d.name,
            "name": meta.get("name") or d.name.split("__")[0],
            "nameZh": meta.get("nameZh", ""),
            "deletedAt": iso_time(meta.get("deletedAt") or 0),
            "daysLeft": max(0.0, round(TRASH_DAYS - age / 86400, 1)),
            "sizeKb": meta.get("sizeKb", 0),
            "links": meta.get("links", []),
            "agent": meta.get("agent") or "",
        })
    return sorted(items, key=lambda x: x["deletedAt"], reverse=True)


def trash_dir(tid: str) -> Path:
    t = (tid or "").strip()
    if not t or any(c in t for c in '\\/:*?"<>|') or ".." in t:
        raise CliError("TRASH_NOT_FOUND", f"回收站条目「{tid}」不合法", "skill trash", EX_NOT_FOUND)
    p = TRASH / t
    if not p.is_dir():
        raise CliError("TRASH_NOT_FOUND", f"回收站里没有「{t}」", "skill trash", EX_NOT_FOUND)
    return p


# ---------------- 写操作护栏 ----------------
def require_yes(args, action: str, target: str, extra: str = ""):
    if getattr(args, "yes", False):
        return
    cmd = f"skill {action} {target} --yes{extra}"
    raise CliError("CONFIRM_REQUIRED", "写操作需要 --yes 确认", cmd, EX_USAGE)


def dry_run_out(action: str, target: dict, would_change: int, extra: dict | None = None):
    out = {"dry_run": True, "action": action, "target": target, "would_change": would_change}
    if extra:
        out.update(extra)
    emit(out)
    sys.exit(EX_OK)


def store_commit(message: str):
    msg = Store(HUB).commit(message)
    if not msg:
        raise CliError("GIT_FAILED", "git 提交失败", "检查 data/hub 是否可写", EX_EXTERNAL)
    return msg


# ---------------- 命令 ----------------
def cmd_list(args):
    entries = collect_skills()
    items = list(entries.values())
    if args.status:
        items = [it for it in items if it["status"] == args.status]
    if args.group:
        items = [it for it in items if it["group"] == args.group]
    if args.pinned:
        items = [it for it in items if it["pinned"]]
    sort = args.sort or "name"
    if sort == "time":
        items.sort(key=lambda x: -(x.get("mtimeTs") or 0))
    elif sort == "size":
        items.sort(key=lambda x: -(x.get("sizeKb") or 0))
    else:
        items.sort(key=lambda x: x["name"].lower())
    total = len(items)
    limit = int(args.limit or 50)
    offset = int(args.offset or 0)
    if limit <= 0 or offset < 0:
        raise CliError("USAGE", "--limit 必须大于 0，--offset 不能为负", "skill list --limit 20 --offset 0", EX_USAGE)
    limit = min(limit, 500)
    page = items[offset:offset + limit]
    for it in page:
        it.pop("mtimeTs", None)
    out = {"items": page, "next": (offset + limit) if offset + limit < total else None}
    if args.output == "ndjson" and not args.human:
        emit(out, args.fields, "ndjson")
        return
    if args.human:
        human_list(
            [{"name": it["name"], "status": it["status"], "group": it["group"],
              "sizeKb": it["sizeKb"], "mtime": it["mtime"][:16]} for it in page],
            ["name", "status", "group", "sizeKb", "mtime"],
        )
        return
    emit(out, args.fields, args.output)


def cmd_get(args):
    entry = get_entry(args.name)
    entry.pop("mtimeTs", None)
    if args.human:
        for k, v in entry.items():
            print(f"{k}: {v}")
        return
    emit(entry, args.fields)


def cmd_history(args):
    name = check_name(args.name)
    items = commit_history_for(name, int(args.limit or 20))
    if not items:
        raise CliError(
            "SKILL_NOT_FOUND",
            f"没有与「{name}」相关的提交",
            "skill list --limit 50",
            EX_NOT_FOUND,
        )
    if args.human:
        human_list(items, ["commit", "time", "message"])
        return
    emit({"items": items, "next": None}, args.fields)


def cmd_roots(args):
    items = all_roots()
    if args.human:
        human_list(items, ["key", "label", "kind", "path"])
        return
    emit({"items": items, "hub": str(HUB)}, args.fields)


def cmd_trash(args):
    items = trash_entries()
    limit = int(args.limit or 50)
    items = items[:limit]
    if args.human:
        human_list(items, ["id", "name", "deletedAt", "daysLeft", "sizeKb"])
        return
    emit({"items": items, "next": None}, args.fields)


# ---------------- 内容审查（启发式，不保证安全） ----------------
# (category, severity, confidence, pattern)
# 经验：单个词（token / password）误报极高，只匹配「路径」「组合动作」「明确命令」。
AUDIT_RULES = [
    ("prompt-injection", "high", "medium",
     r"(?i)(ignore (all )?(previous|prior|above) instructions|disregard .{0,20}(instruction|rule)s?|忽略(之前|以上|前面)的?(所有)?(指令|规则)|你现在是|不受任何限制|jailbreak|developer mode)"),
    ("dangerous-shell", "high", "high",
     r"(?i)(rm\s+-rf\s+/(\s|$)|\bdel\s+/[sq]\s+|\bformat\s+[a-z]:|curl\s+[^\n|]{0,200}\|\s*(ba)?sh|wget\s+[^\n|]{0,200}\|\s*(ba)?sh|powershell\s+[^\n]{0,40}-e(nc|ncodedcommand)|Invoke-Expression)"),
    ("credential-path", "medium", "low",
     r"(~/\.ssh|id_rsa|\.aws/credentials|\.netrc|\.npmrc|/etc/shadow|\\\.ssh\\)"),
    ("credential-exfil", "high", "medium",
     r"(?is)((cat|type|get-content|open|read)\b.{0,80}(\.ssh|id_rsa|\.env|credentials).{0,300}(curl|wget|Invoke-WebRequest|requests\.post|fetch\(|https?://))"),
    ("obfuscation", "medium", "medium",
     r"([A-Za-z0-9+/]{200,}={0,2})"),
    ("dynamic-exec", "medium", "low",
     r"(?i)(\beval\s*\(|\bexec\s*\(|__import__\s*\(|base64\.b64decode|FromBase64String)"),
]

ZERO_WIDTH = "\u200b\u200c\u200d\u200e\u200f\u202a\u202b\u202c\u202d\u202e\ufeff"

AUDIT_EXTS = {".py", ".sh", ".ps1", ".bat", ".cmd", ".js", ".mjs", ".ts", ".rb", ".pl"}


def _audit_text(text: str, rel: str) -> list:
    import re as _re
    findings = []
    lines = text.splitlines()
    for cat, sev, conf, pattern in AUDIT_RULES:
        rx = _re.compile(pattern)
        for i, line in enumerate(lines, 1):
            if rx.search(line):
                findings.append({
                    "category": cat,
                    "severity": sev,
                    "confidence": conf,
                    "file": rel,
                    "line": i,
                    "snippet": line.strip()[:160],
                })
    for i, line in enumerate(lines, 1):
        # 文件头的 BOM 是正常的，只有出现在行内的才算可疑
        probe = line[1:] if line.startswith("\ufeff") else line
        if any(ch in probe for ch in ZERO_WIDTH):
            findings.append({
                "category": "obfuscation",
                "severity": "high",
                "confidence": "high",
                "file": rel,
                "line": i,
                "snippet": "含不可见 Unicode 字符",
            })
    return findings


def _audit_skill_dir(path: Path, name: str) -> list:
    findings = []
    md = path / "SKILL.md"
    if md.exists():
        findings += _audit_text(md.read_text(encoding="utf-8", errors="replace"), "SKILL.md")
    for f in sorted(path.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in AUDIT_EXTS:
            continue
        rel = str(f.relative_to(path)).replace("\\", "/")
        try:
            findings += _audit_text(f.read_text(encoding="utf-8", errors="replace"), rel)
        except Exception:
            pass
    return findings


def cmd_audit(args):
    """静态审查技能内容：注入、危险命令、凭据读取、混淆。启发式，不是安全保证。"""
    entries = collect_skills()
    names = [args.name] if args.name else sorted(entries)
    limit = int(args.limit or (len(names) or 1))
    names = names[:limit]
    findings = []
    checked = []
    for n in names:
        e = entries.get(n)
        if not e:
            raise CliError("SKILL_NOT_FOUND", f"技能「{n}」不存在", "skill list --limit 50", EX_NOT_FOUND)
        path = Path(e["path"])
        if not path.is_dir():
            continue
        checked.append(n)
        for f in _audit_skill_dir(path, n):
            f["name"] = n
            findings.append(f)
    order = {"high": 3, "medium": 2, "low": 1}
    worst = max((order.get(f["severity"], 0) for f in findings), default=0)
    risk = {3: "high", 2: "medium", 1: "low"}.get(worst, "none")
    out = {
        "checked": len(checked),
        "risk": risk,
        "findings": findings,
        "disclaimer": "静态启发式检查，只提示可疑点，不能证明技能安全。",
    }
    if args.human:
        print(f"检查 {len(checked)} 个技能，风险 {risk}，命中 {len(findings)} 条")
        for f in findings:
            print(f"  [{f['severity']}/{f['confidence']}] {f['name']} · {f['file']}:{f['line']} · {f['category']} · {f['snippet']}")
        return
    emit(out, args.fields)



def cmd_detect(args) -> None:
    """检测全局与各工作区的技能（只扫一层，不递归）。"""
    adir = "." + active_agent()
    gdir = global_skills_dir()

    def skills_in(p: Path) -> list:
        out = []
        if not p.is_dir():
            return out
        for child in sorted(p.iterdir()):
            if child.is_dir() and not child.name.startswith(".") and (child / "SKILL.md").is_file():
                out.append(child.name)
        return out

    workspaces = []
    for ws in discover_workspaces():
        p = Path(ws)
        sp = p / adir / "skills"
        workspaces.append({
            "name": p.name,
            "path": str(sp),
            "exists": sp.is_dir(),
            "skills": skills_in(sp),
        })
    total_ws = sum(len(w["skills"]) for w in workspaces)
    emit({
        "agent": active_agent(),
        "rules": {
            "global": f"<用户目录>/{adir}/skills/<技能名>/SKILL.md",
            "workspace": f"<工作区>/{adir}/skills/<技能名>/SKILL.md",
            "depth": 1,
            "recursive": False,
            "projectLevel": False,
            "note": "只检测全局与工作区母文件夹下的技能；工作区内按项目分的子文件夹一律不检测。",
        },
        "global": {"path": str(gdir), "exists": gdir.is_dir(), "skills": skills_in(gdir)},
        "workspaces": workspaces,
        "counts": {"global": len(skills_in(gdir)), "workspace": total_ws},
    }, getattr(args, "fields", None), getattr(args, "output", "json"))

def cmd_schema(args):
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    if args.command:
        for c in spec["commands"]:
            if c["name"] == args.command:
                emit(c)
                return
        raise CliError("USAGE", f"没有命令 {args.command}", "skill schema", EX_USAGE)
    emit(spec)


def read_content_arg(value: str) -> str | None:
    if value is None:
        return None
    if value == "-":
        return sys.stdin.read()
    if value.startswith("@"):
        p = Path(value[1:])
        if not p.exists():
            raise CliError("USAGE", f"文件不存在：{p}", f"检查路径 {p}", EX_USAGE)
        return p.read_text(encoding="utf-8-sig")
    return value


def cmd_create(args):
    payload = load_json_payload(args.json)
    name = args.name or payload.get("name")
    if not name:
        raise CliError("USAGE", "缺少技能名", 'skill create my-skill --desc "..." --yes', EX_USAGE)
    name = check_name(name)
    desc = (args.desc or payload.get("desc") or payload.get("description") or "").strip()
    if not desc:
        raise CliError("USAGE", "缺少 --desc 描述", "skill create my-skill --desc \"一句话说明用途\" --yes", EX_USAGE)
    if len(desc) < 10:
        raise CliError("USAGE", "描述太短（至少 10 字）", "写清「什么时候用这个技能」", EX_USAGE)
    zh = (args.zh or payload.get("zh") or payload.get("name_zh") or "").strip()
    raw_content = args.content if args.content is not None else payload.get("content")
    content = read_content_arg(raw_content) if isinstance(raw_content, str) else raw_content
    body = content or ""
    link_arg = args.link or payload.get("link")
    if content and content.lstrip().startswith("---"):
        meta, body = split_frontmatter(content)
        if meta.get("name") and meta["name"] != name:
            raise CliError("INVALID_FRONTMATTER", f"正文里的 name（{meta['name']}）与命令参数（{name}）不一致", "统一成一个名字", EX_USAGE)
    dst = HUB / "skills" / name
    exists = dst.is_dir()
    if exists and not (args.upsert or payload.get("upsert")):
        raise CliError(
            "SKILL_EXISTS",
            f"技能「{name}」已存在",
            f"加 --upsert 覆盖，或 skill update {name} 只改内容",
            EX_EXISTS,
        )
    target_root = None
    if link_arg:
        target_root = resolve_root(link_arg, allow_hub=False)
    if args.dry_run:
        dry_run_out(
            "create",
            {"name": name, "path": str(dst)},
            1 if not exists else 2,
            {"would_link": target_root["key"] if target_root else None, "content_bytes": len(body.encode("utf-8"))},
        )
    require_yes(args, "create", name, f' --desc "{desc}"')
    dst.mkdir(parents=True, exist_ok=True)
    md = build_skill_md(name, zh, desc, body)
    (dst / "SKILL.md").write_text(md, encoding="utf-8")
    store_commit(f"{'update' if exists else 'create'}: {name}")
    linked = []
    if target_root:
        lp = Path(target_root["path"]) / name
        ok, err = linker.create_junction(lp, dst)
        if not ok:
            raise CliError("TARGET_EXISTS", f"挂载失败：{err}", f"skill link {name} --to {target_root['key']}", EX_PRECOND)
        linked.append(target_root["key"])
        store_commit(f"link: {name} -> {target_root['label']}")
    note = "已入仓库，尚未挂载；用 skill link 挂载" if not linked else f"已挂载到 {linked[0]}"
    emit({
        "name": name,
        "path": str(dst),
        "status": "unlinked" if not linked else "linked",
        "group": linked[0] if linked else "hub",
        "created": not exists,
        "links": linked,
        "note": note,
    })


def cmd_update(args):
    payload = load_json_payload(args.json)
    raw_name = args.name or payload.get("name")
    if not raw_name:
        raise CliError("USAGE", "缺少技能名", "skill update my-skill --desc \"...\" --yes", EX_USAGE)
    name = check_name(raw_name)
    entry = get_entry(name)
    dst = HUB / "skills" / name
    if not dst.is_dir():
        raise CliError("SKILL_NOT_FOUND", f"hub 里没有 {name}", "skill list", EX_NOT_FOUND)
    text = read_skill_file(dst)
    meta, body = split_frontmatter(text)
    changed = []
    zh_val = args.zh if args.zh is not None else payload.get("zh", payload.get("name_zh"))
    desc_val = args.desc if args.desc is not None else payload.get("desc", payload.get("description"))
    content_val = args.content if args.content is not None else payload.get("content")
    content = read_content_arg(content_val) if isinstance(content_val, str) else content_val
    if zh_val is not None:
        meta["name_zh"] = str(zh_val).strip()
        changed.append("name_zh")
    if desc_val is not None:
        d = str(desc_val).strip()
        if len(d) < 10:
            raise CliError("USAGE", "描述太短（至少 10 字）", "写清用途", EX_USAGE)
        meta["description"] = d
        changed.append("description")
    if content is not None:
        if content.lstrip().startswith("---"):
            cmeta, cbody = split_frontmatter(content)
            for k in ("name", "name_zh", "description"):
                if cmeta.get(k):
                    meta[k] = cmeta[k]
            body = cbody
        else:
            body = content
        changed.append("SKILL.md")
    if not changed:
        raise CliError("USAGE", "没有任何要改的内容", "用 --zh / --desc / --content 指定", EX_USAGE)
    if args.dry_run:
        dry_run_out("update", {"name": name, "path": str(dst)}, len(changed), {"fields": changed})
    require_yes(args, "update", name, " --desc \"...\"")
    new_md = build_skill_md(name, meta.get("name_zh", ""), meta.get("description", ""), body)
    (dst / "SKILL.md").write_text(new_md, encoding="utf-8")
    commit = store_commit(f"edit: {name}/SKILL.md")
    emit({"name": name, "changed": changed, "commit": commit})


def cmd_link(args):
    name = check_name(args.name)
    entry = get_entry(name)
    root = resolve_root(args.to, allow_hub=False)
    dst = HUB / "skills" / name
    if not dst.is_dir():
        raise CliError("SKILL_NOT_FOUND", f"仓库里没有 {name}", "skill list", EX_NOT_FOUND)
    lp = Path(root["path"]) / name
    if lp.exists() or scanner.is_link(lp):
        raise CliError(
            "TARGET_EXISTS",
            f"{root['label']} 下已有同名",
            f"skill unlink {name} --from {root['key']} 后再挂",
            EX_PRECOND,
        )
    if args.dry_run:
        dry_run_out("link", {"name": name, "to": root["key"]}, 1, {"link_path": str(lp)})
    require_yes(args, "link", name, f" --to {root['key']}")
    ok, err = linker.create_junction(lp, dst)
    if not ok:
        raise CliError("TARGET_EXISTS", err, "检查目标目录权限", EX_PRECOND)
    commit = store_commit(f"link: {name} -> {root['label']}")
    links = sorted({l["key"] for l in entry["links"]} | {root["key"]})
    emit({"name": name, "linked": True, "to": {"key": root["key"], "label": root["label"], "path": str(lp)},
          "links": links, "commit": commit})


def cmd_unlink(args):
    name = check_name(args.name)
    entry = get_entry(name)
    targets = []
    if args.from_:
        targets = [resolve_root(args.from_, allow_hub=False)]
    else:
        targets = [r for r in all_roots() if r["kind"] != "hub"]
    removed = []
    found = False
    for r in targets:
        lp = Path(r["path"]) / name
        if scanner.is_link(lp):
            found = True
            if not args.dry_run:
                ok, err = linker.remove_junction(lp)
                if not ok:
                    raise CliError("PRECOND", err, "手动检查该链接", EX_PRECOND)
            removed.append(r["key"])
    if not found:
        raise CliError(
            "NOT_LINKED",
            f"{name} 在这些位置没有挂载" if args.from_ else f"{name} 没有任何挂载",
            f"skill get {name} 查看当前挂载点",
            EX_PRECOND,
        )
    if args.dry_run:
        dry_run_out("unlink", {"name": name}, len(removed), {"would_remove": removed})
    require_yes(args, "unlink", name, " --from <位置>")
    commit = store_commit(f"unlink: {name} <- {', '.join(removed)}")
    links = sorted({l["key"] for l in entry["links"]} - set(removed))
    emit({"name": name, "removed": removed, "links": links, "commit": commit})


def cmd_delete(args):
    name = check_name(args.name)
    entry = get_entry(name)
    dst = HUB / "skills" / name
    removed = []
    for r in all_roots():
        if r["kind"] == "hub":
            continue
        lp = Path(r["path"]) / name
        if scanner.is_link(lp):
            removed.append(r["key"])
    if args.dry_run:
        dry_run_out("delete", {"name": name}, 1,
                    {"would_remove_links": removed, "trash_keeps_days": TRASH_DAYS})
    require_yes(args, "delete", name)
    for r in all_roots():
        if r["kind"] == "hub":
            continue
        lp = Path(r["path"]) / name
        if scanner.is_link(lp):
            linker.remove_junction(lp)
    if not dst.is_dir():
        raise CliError("SKILL_NOT_FOUND", f"仓库里没有 {name}（可能只有外部链接）", "skill list", EX_NOT_FOUND)
    fm = scanner.read_frontmatter(dst / "SKILL.md")
    n, kb, _mt = dir_stats(dst)
    TRASH.mkdir(parents=True, exist_ok=True)
    tid = f"{name}__{time.strftime('%Y%m%d-%H%M%S')}"
    tpath = TRASH / tid
    seq = 1
    while tpath.exists():
        tpath = TRASH / f"{tid}-{seq}"
        seq += 1
    shutil.move(str(dst), str(tpath))
    try:
        (tpath / "_trash.json").write_text(
            json.dumps({
                "name": name,
                "nameZh": fm.get("name_zh", ""),
                "desc": fm.get("description", ""),
                "deletedAt": time.time(),
                "links": removed,
                "sizeKb": kb,
                "agent": load_config().get("activeAgent") or "dsh",
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass
    Store(HUB).drop(name)
    store_commit(f"trash: {name}")
    emit({"name": name, "trashed": True, "trashId": tpath.name,
          "removedLinks": removed, "expiresInDays": TRASH_DAYS})


def cmd_restore(args):
    src = trash_dir(args.id)
    meta_file = src / "_trash.json"
    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except Exception:
        meta = {}
    name = (meta.get("name") or src.name.split("__")[0]).strip()
    try:
        check_name(name)
    except CliError:
        pass
    origin = (meta.get("agent") or "").strip() or load_config().get("activeAgent") or "dsh"
    target_hub = hub_dir_for(origin)
    dst = target_hub / "skills" / name
    if dst.exists():
        raise CliError("SKILL_EXISTS", f"仓库里已有同名技能 {name}", f"先处理 skill get {name}", EX_EXISTS)
    if args.dry_run:
        dry_run_out("restore", {"id": args.id, "name": name}, 1, {"would_restore_to": origin})
    require_yes(args, "restore", args.id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    junk = dst / "_trash.json"
    if junk.exists():
        junk.unlink()
    commit = store_commit(f"restore: {name}")
    label = (agents_config().get(origin) or {}).get("label") or origin
    emit({"name": name, "restored": True, "trashId": args.id, "agent": origin,
          "agentLabel": label, "path": str(dst), "commit": commit})


def cmd_purge(args):
    src = trash_dir(args.id)
    name = src.name
    if args.dry_run:
        dry_run_out("purge", {"id": args.id}, 1, {"dir": str(src)})
    require_yes(args, "purge", args.id)
    shutil.rmtree(src, ignore_errors=True)
    emit({"id": args.id, "name": name, "purged": True})


def cmd_validate(args):
    entries = collect_skills()
    names = [args.name] if args.name else sorted(entries)
    problems = []
    for n in names:
        if n not in entries:
            problems.append({"name": n, "field": "name", "message": "技能不存在"})
            continue
        e = entries[n]
        dst = Path(e["path"])
        if dst.parent == HUB / "skills":
            try:
                check_name(n)
            except CliError as ex:
                problems.append({"name": n, "field": "name", "message": ex.message})
        fm = scanner.read_frontmatter(dst / "SKILL.md")
        if not fm.get("name"):
            problems.append({"name": n, "field": "name", "message": "frontmatter 缺少 name"})
        elif fm.get("name") != n and not str(fm.get("name")).startswith(n):
            if dst.parent == HUB / "skills":
                problems.append({"name": n, "field": "name", "message": f"frontmatter 的 name（{fm.get('name')}）与目录名不一致"})
        desc = fm.get("description", "")
        if not desc:
            problems.append({"name": n, "field": "description", "message": "缺少 description"})
        elif len(desc) < 10:
            problems.append({"name": n, "field": "description", "message": "description 太短（<10）"})
        elif len(desc) > DESC_MAX:
            problems.append({"name": n, "field": "description", "message": "description 太长（>1000）"})
        if (e.get("sizeKb") or 0) > SIZE_MAX_KB:
            problems.append({"name": n, "field": "size", "message": f"超过 {SIZE_MAX_KB} KB"})
    out = {"checked": len(names), "problems": problems, "ok": not problems}
    if args.human:
        print(f"检查 {len(names)} 个，问题 {len(problems)} 个")
        for p in problems:
            print(f"  {p['name']} · {p['field']}: {p['message']}")
        return
    emit(out, args.fields)


def cmd_diff(args):
    name = check_name(args.name)
    get_entry(name)
    commit = find_commit(args.commit)
    files = commit_skill_files(commit, name)
    target = f"skills/{name}/SKILL.md"
    old = files.get(target, b"").decode("utf-8", "replace")
    dst = HUB / "skills" / name
    new = read_skill_file(dst)
    diff = list(difflib.unified_diff(
        old.splitlines(), new.splitlines(),
        fromfile=f"{commit.id.decode()[:8]}:{target}", tofile="current", lineterm="",
    ))
    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
    out = {
        "name": name,
        "commit": commit.id.decode()[:8],
        "changed": sorted({p.replace(f"skills/{name}/", "") for p in files}),
        "stats": {"added": added, "removed": removed},
        "diff": "\n".join(diff),
    }
    if args.human:
        print(out["diff"] or "（无差异）")
        return
    emit(out, args.fields)


def cmd_recover(args):
    """从 git 历史把某个已不存在的技能恢复回仓库。"""
    name = check_name(args.name)
    commit = find_commit(args.commit)
    files = commit_skill_files(commit, name)
    dst = HUB / "skills" / name
    if dst.exists():
        raise CliError(
            "SKILL_EXISTS",
            f"仓库里已有 {name}",
            f"要改内容用 skill rollback {name} --commit {commit.id.decode()[:8]}",
            EX_EXISTS,
        )
    if args.dry_run:
        dry_run_out("recover", {"name": name, "commit": commit.id.decode()[:8]}, len(files),
                    {"would_write": sorted(p.replace(f"skills/{name}/", "") for p in files)})
    require_yes(args, "recover", name, f" --commit {commit.id.decode()[:8]}")
    dst.mkdir(parents=True, exist_ok=True)
    for rel, data in files.items():
        local = rel.replace(f"skills/{name}/", "")
        target = dst / local
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    commit2 = store_commit(f"recover: {name} from {commit.id.decode()[:8]}")
    emit({
        "name": name,
        "path": str(dst),
        "recoveredFrom": commit.id.decode()[:8],
        "newCommit": commit2,
        "files": sorted(p.replace(f"skills/{name}/", "") for p in files),
        "status": "unlinked",
    })


def cmd_rollback(args):
    name = check_name(args.name)
    get_entry(name)
    commit = find_commit(args.commit)
    files = commit_skill_files(commit, name)
    dst = HUB / "skills" / name
    if args.dry_run:
        dry_run_out("rollback", {"name": name, "commit": commit.id.decode()[:8]}, len(files),
                    {"would_write": sorted(p.replace(f"skills/{name}/", "") for p in files)})
    require_yes(args, "rollback", name, f" --commit {commit.id.decode()[:8]}")
    changed = []
    for rel, data in files.items():
        local = rel.replace(f"skills/{name}/", "")
        target = dst / local
        target.parent.mkdir(parents=True, exist_ok=True)
        old = target.read_bytes() if target.exists() else None
        if old != data:
            target.write_bytes(data)
            changed.append(local)
    commit2 = store_commit(f"rollback: {name} -> {commit.id.decode()[:8]}")
    emit({"name": name, "rolledBackTo": commit.id.decode()[:8], "newCommit": commit2, "changed": changed})


# ---------------- 入口 ----------------
class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise CliError("USAGE", message, "skill --help", EX_USAGE)


def build_parser():
    p = Parser(
        prog="skill",
        description="技能仓库的命令行接口（agent 优先）。默认输出 JSON；写操作需要 --yes。",
        epilog=(
            "示例：\n"
            "  skill roots\n"
            "  skill list --status unlinked --fields name,status,sizeKb\n"
            "  skill create my-skill --zh 我的技能 --desc \"什么时候用这个技能\" --content @body.md --yes\n"
            "  skill link my-skill --to global --yes\n"
            "  skill history my-skill\n"
            "  skill diff my-skill --commit 1a2b3c4d\n"
            "  skill rollback my-skill --commit 1a2b3c4d --yes\n"
            "  skill delete my-skill --yes\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--version", action="version", version=f"skill {CLI_VERSION}")
    sub = p.add_subparsers(dest="cmd", parser_class=Parser)

    def add(name, fn, **kw):
        sp = sub.add_parser(name, **kw)
        sp.set_defaults(_fn=fn)
        sp.add_argument("--fields", help="只输出这些字段，逗号分隔")
        sp.add_argument("--output", choices=["json", "ndjson", "text"], default="json",
                        help="输出格式：json（默认）/ ndjson（一行一个）/ text")
        sp.add_argument("--json", help="结构化输入：'<payload>' | @file | -")
        sp.add_argument("--dry-run", action="store_true", help="只预览，不产生副作用")
        sp.add_argument("--yes", "-y", action="store_true", help="写操作确认")
        sp.add_argument("--human", action="store_true", help="人类可读输出")
        sp.add_argument("--no-input", action="store_true", help="禁止交互")
        sp.add_argument("--quiet", "-q", action="store_true")
        sp.add_argument("--verbose", "-v", action="store_true")
        return sp

    sp = add("list", cmd_list, help="列出技能")
    sp.add_argument("--status")
    sp.add_argument("--group")
    sp.add_argument("--pinned", action="store_true")
    sp.add_argument("--sort", default="name")
    sp.add_argument("--limit", type=int, default=50)
    sp.add_argument("--offset", type=int, default=0)

    sp = add("detect", cmd_detect, help="检测全局与各工作区的技能（只扫一层）")

    sp = add("get", cmd_get, help="单个技能详情")
    sp.add_argument("name")

    sp = add("history", cmd_history, help="技能提交历史")
    sp.add_argument("name")
    sp.add_argument("--limit", default=20)

    add("roots", cmd_roots, help="可挂载位置")

    sp = add("trash", cmd_trash, help="回收站列表")
    sp.add_argument("--limit", default=50)

    sp = add("schema", cmd_schema, help="命令目录")
    sp.add_argument("--command")

    sp = add("create", cmd_create, help="创建技能并入库")
    sp.add_argument("name", nargs="?")
    sp.add_argument("--zh", default="")
    sp.add_argument("--desc", default="")
    sp.add_argument("--content")
    sp.add_argument("--link")
    sp.add_argument("--upsert", action="store_true")

    sp = add("update", cmd_update, help="修改元数据或正文")
    sp.add_argument("name", nargs="?")
    sp.add_argument("--zh", default=None)
    sp.add_argument("--desc", default=None)
    sp.add_argument("--content")

    sp = add("link", cmd_link, help="挂载")
    sp.add_argument("name")
    sp.add_argument("--to", required=True)

    sp = add("unlink", cmd_unlink, help="取消挂载")
    sp.add_argument("name")
    sp.add_argument("--from", dest="from_", default=None)

    sp = add("delete", cmd_delete, help="删除到回收站")
    sp.add_argument("name")

    sp = add("restore", cmd_restore, help="从回收站恢复")
    sp.add_argument("id")

    sp = add("purge", cmd_purge, help="彻底删除回收站条目")
    sp.add_argument("id")

    sp = add("validate", cmd_validate, help="校验格式")
    sp.add_argument("name", nargs="?")
    sp.add_argument("--all", action="store_true")

    sp = add("audit", cmd_audit, help="静态审查技能内容（注入/危险命令/凭据/混淆）")
    sp.add_argument("name", nargs="?")
    sp.add_argument("--limit", type=int, default=0)

    sp = add("diff", cmd_diff, help="对比提交与当前内容")
    sp.add_argument("name")
    sp.add_argument("--commit", required=True)

    sp = add("rollback", cmd_rollback, help="回滚到某个提交")
    sp.add_argument("name")
    sp.add_argument("--commit", required=True)

    sp = add("recover", cmd_recover, help="从 git 历史恢复已删除的技能")
    sp.add_argument("name")
    sp.add_argument("--commit", required=True)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        if not getattr(args, "_fn", None):
            emit({"commands": [c["name"] for c in json.loads(SPEC_PATH.read_text(encoding="utf-8"))["commands"]]})
            return EX_OK
        args._fn(args)
        return EX_OK
    except CliError as e:
        fail(e.code, e.message, e.suggestion, e.exit_code, e.recoverable)
        return e.exit_code
    except BrokenPipeError:
        return EX_OK
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        fail("INTERNAL", str(e), "加 --verbose 重试，或查看是否有权限问题", EX_FAIL)
        return EX_FAIL


if __name__ == "__main__":
    sys.exit(main())
