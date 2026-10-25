"""平台差异的唯一入口：链接的创建、删除、读取、判断。

调用方（scanner / linker / app / cli）只用这里的四个函数，不直接碰系统命令。
目前只有 Windows 实现（junction + reparse point）。

要支持 macOS / Linux：
  1. 在 `create_link` 里加 else 分支，用 `os.symlink(target, link, target_is_directory=True)`
  2. 在 `remove_link` 里用 `os.unlink(link)`
  3. `is_link` 直接用 `os.path.islink`（reparse 判断只对 Windows 有意义）
  4. `link_target` 直接用 `os.readlink`
其余文件不需要改。
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

IS_WINDOWS = os.name == "nt"
REPARSE_POINT = 0x400


def is_link(path: Path) -> bool:
    """是否目录链接（Windows junction / symlink）。"""
    try:
        st = os.stat(path, follow_symlinks=False)
    except OSError:
        return False
    if getattr(st, "st_file_attributes", 0) & REPARSE_POINT:
        return True
    return os.path.islink(path)


def link_target(path: Path) -> str | None:
    """链接指向的目标路径；读不出来返回 None。"""
    try:
        return os.readlink(path)
    except OSError:
        pass
    if not IS_WINDOWS:
        return None
    # Windows 的 junction 有时 os.readlink 读不出，退回 dir /AL 解析
    try:
        out = subprocess.run(
            ["cmd", "/c", "dir", "/AL", str(path.parent)],
            capture_output=True, text=True, encoding="mbcs", errors="replace",
        ).stdout
        for line in out.splitlines():
            if path.name in line and "<JUNCTION>" in line.upper():
                parts = line.split("<JUNCTION>")
                if len(parts) == 2:
                    return parts[1].strip()
    except Exception:
        pass
    return None


def create_link(link: Path, target: Path) -> tuple[bool, str]:
    """在 link 位置创建指向 target 的目录链接。"""
    if link.exists() or is_link(link):
        return False, f"目标位置已存在：{link}"
    if not target.is_dir():
        return False, f"实体目录不存在：{target}"
    link.parent.mkdir(parents=True, exist_ok=True)
    if not IS_WINDOWS:
        return False, "当前平台未实现（见 core/platform.py 顶部说明）"
    try:
        r = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True, text=True, encoding="mbcs", errors="replace",
        )
        if r.returncode != 0 or not link.exists():
            msg = (r.stderr or r.stdout or "").strip()
            return False, f"创建链接失败：{msg}"
        return True, ""
    except Exception as e:
        return False, f"创建链接异常：{e}"


def remove_link(link: Path) -> tuple[bool, str]:
    """只删除链接本身，不动目标内容。"""
    if not is_link(link):
        return False, f"不是链接：{link}"
    try:
        if IS_WINDOWS:
            os.rmdir(str(link))       # junction 只能用 rmdir 删
        else:
            os.unlink(str(link))
        return True, ""
    except OSError as e:
        return False, f"删除链接失败：{e}"


def is_dead_link(path: Path) -> bool:
    """链接指向的目标已不存在（以 SKILL.md 是否可读为准）。"""
    if not is_link(path):
        return False
    return not (path / "SKILL.md").exists()
