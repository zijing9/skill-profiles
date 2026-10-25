"""分级日志：写文件，有 stderr 时镜像一份。

默认 info；环境变量 SKILL_LOG=debug 打开调试细节。
单文件 2MB，保留 3 份。
"""
from __future__ import annotations

import logging
import logging.handlers
import os
import sys
from pathlib import Path

LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
}

_configured = False


def setup(log_dir: Path) -> str:
    """初始化根 logger，返回实际生效的级别名。"""
    global _configured
    raw = (os.environ.get("SKILL_LOG") or "info").strip().lower()
    level = LEVELS.get(raw, logging.INFO)

    if _configured:
        return logging.getLevelName(level).lower()

    root = logging.getLogger("skillmgr")
    root.setLevel(level)
    root.propagate = False

    fmt = logging.Formatter(
        "%(asctime)s.%(msecs)03d %(levelname)-5s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        fh = logging.handlers.RotatingFileHandler(
            log_dir / "app.log", maxBytes=2 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        fh.setFormatter(fmt)
        fh.setLevel(level)
        root.addHandler(fh)
    except Exception:
        pass

    # pythonw 下 sys.stderr 为 None，跳过
    try:
        if sys.stderr is not None:
            sh = logging.StreamHandler(sys.stderr)
            sh.setFormatter(fmt)
            sh.setLevel(level)
            root.addHandler(sh)
    except Exception:
        pass

    _configured = True
    return logging.getLevelName(level).lower()


def get(name: str) -> logging.Logger:
    return logging.getLogger("skillmgr").getChild(name)
