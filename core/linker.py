"""junction 链接的业务封装。

底层实现全部在 core/platform.py；这里只保留业务语义，不再出现系统命令。
调用方可以继续用这些函数名，行为不变。
"""
from __future__ import annotations

from pathlib import Path

from .platform import create_link, is_dead_link, is_link, link_target, remove_link

__all__ = [
    "is_link",
    "link_target",
    "create_junction",
    "remove_junction",
    "is_dead_link",
]


def create_junction(link: Path, target: Path) -> tuple[bool, str]:
    """在 link 位置创建指向 target 的链接。"""
    return create_link(link, target)


def remove_junction(link: Path) -> tuple[bool, str]:
    """只删除链接本身，不动目标内容。"""
    return remove_link(link)
