"""技能根发现与 SKILL.md 解析。"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from .platform import is_link

__all__ = ["is_link", "read_frontmatter", "SkillDir", "load_skill", "scan_root"]

SKILL_FILE = "SKILL.md"


def read_frontmatter(skill_md: Path) -> dict:
    """读 SKILL.md 的 YAML frontmatter（仅字符串键值，够用）。"""
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end]
    data: dict[str, str] = {}
    key = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            if val.startswith(('"', "'")) and val[-1:] == val[:1] and len(val) > 1:
                val = val[1:-1]
            data[key] = val
        elif key and line.startswith((" ", "\t")):
            data[key] = (data.get(key, "") + " " + line.strip()).strip()
    return data


@dataclass
class SkillDir:
    name: str
    path: Path
    root_key: str
    root_label: str
    kind: str  # global | workspace | hub
    is_link: bool = False
    link_target: str | None = None
    name_zh: str = ""
    description: str = ""
    file_count: int = 0
    size_kb: int = 0
    mtime: float = 0.0
    valid: bool = False
    error: str = ""


def _dir_stats(path: Path) -> tuple[int, int, float]:
    n = 0
    total = 0
    latest = 0.0
    for root, _dirs, files in os.walk(path):
        for f in files:
            n += 1
            fp = os.path.join(root, f)
            try:
                total += os.path.getsize(fp)
                latest = max(latest, os.path.getmtime(fp))
            except OSError:
                pass
    return n, total // 1024, latest


def load_skill(path: Path, root_key: str, root_label: str, kind: str) -> SkillDir | None:
    sm = path / SKILL_FILE
    if not sm.exists():
        return None
    fm = read_frontmatter(sm)
    n, kb, mtime = _dir_stats(path)
    if not mtime:
        try:
            mtime = sm.stat().st_mtime
        except OSError:
            mtime = 0.0
    link = is_link(path)
    target = None
    if link:
        try:
            target = str(os.readlink(path))
        except OSError:
            target = None
    name = fm.get("name") or path.name
    return SkillDir(
        name=name,
        path=path,
        root_key=root_key,
        root_label=root_label,
        kind=kind,
        is_link=link,
        link_target=target,
        name_zh=fm.get("name_zh", ""),
        description=fm.get("description", ""),
        file_count=n,
        size_kb=kb,
        mtime=mtime,
        valid=bool(fm.get("name")),
        error="" if fm.get("name") else "frontmatter 缺少 name",
    )


def scan_root(root: Path, root_key: str, root_label: str, kind: str) -> list[SkillDir]:
    out: list[SkillDir] = []
    if not root.is_dir():
        return out
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        s = load_skill(child, root_key, root_label, kind)
        if s:
            out.append(s)
    return out
