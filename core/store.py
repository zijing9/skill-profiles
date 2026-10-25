"""hub 仓库：manifest 读写 + git 提交。"""
from __future__ import annotations

import json
import shutil
import time
from pathlib import Path


class Store:
    def __init__(self, hub: Path):
        self.hub = hub
        self.skills = hub / "skills"
        self.manifest_path = hub / "manifest.json"
        self.skills.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    # ---------- manifest ----------
    def _load(self) -> dict:
        if self.manifest_path.exists():
            try:
                return json.loads(self.manifest_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"skills": {}}

    def save(self) -> None:
        self.manifest_path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def all(self) -> dict:
        return self.data.setdefault("skills", {})

    def get(self, name: str) -> dict | None:
        return self.all().get(name)

    def put(self, name: str, meta: dict) -> None:
        self.all()[name] = meta
        self.save()

    def drop(self, name: str) -> dict | None:
        m = self.all().pop(name, None)
        self.save()
        return m

    def path_of(self, name: str) -> Path:
        """技能目录；拒绝空名、路径分隔符和越界路径。"""
        n = (name or "").strip()
        if not n or n in (".", "..") or any(c in n for c in '\\/:*?"<>|'):
            raise ValueError(f"非法技能名：{name!r}")
        root = self.skills.resolve()
        dst = (self.skills / n).resolve()
        if dst.parent != root:
            raise ValueError(f"非法技能名：{name!r}")
        return self.skills / n

    # ---------- 分身 ----------
    def family_of(self, name: str) -> str:
        """同组分身的组名；没有分身时就是它自己。"""
        m = self.get(name) or {}
        return (m.get("family") or name).strip() or name

    def siblings(self, name: str) -> list[str]:
        """同一组的全部技能名（含自己）。"""
        fam = self.family_of(name)
        return sorted(n for n, m in self.all().items() if (m.get("family") or n) == fam)

    def clone(self, name: str) -> tuple[bool, str, str]:
        """复制一份同样的技能，返回 (ok, 新名, 错误)。"""
        import shutil
        src = self.path_of(name)
        if not src.is_dir():
            return False, "", "技能不存在"
        fam = self.family_of(name)
        used = {n for n in self.all()}
        used |= {n for n in self.siblings(name)}
        # 优先 family-2、family-3…
        n = 2
        while f"{fam}-{n}" in used:
            n += 1
        new_name = f"{fam}-{n}"
        dst = self.path_of(new_name)
        try:
            shutil.copytree(src, dst)
        except Exception as e:
            return False, "", f"复制失败：{e}"
        # 修正 SKILL.md 里的 name 字段
        md = dst / "SKILL.md"
        if md.exists():
            try:
                txt = md.read_text(encoding="utf-8")
                import re as _re
                txt = _re.sub(r"^name:.*$", f"name: {new_name}", txt, count=1, flags=_re.M)
                md.write_text(txt, encoding="utf-8")
            except Exception:
                pass
        meta = dict(self.get(name) or {})
        meta["family"] = fam
        meta["name_zh"] = (meta.get("name_zh") or "") and f"{meta.get('name_zh')}（副本）"
        meta.pop("links", None)
        meta.pop("pinned", None)
        self.put(new_name, meta)
        # 母体也记上 family
        base = dict(self.get(name) or {})
        base["family"] = fam
        self.put(name, base)
        return True, new_name, ""

    # ---------- git ----------
    def _git(self):
        from dulwich import porcelain
        from dulwich.repo import Repo
        return porcelain, Repo

    def ensure_repo(self) -> None:
        """初始化 git 仓库（幂等）。"""
        try:
            porcelain, Repo = self._git()
            if not (self.hub / ".git").exists():
                porcelain.init(str(self.hub))
            # 忽略链接与运行时文件
            gi = self.hub / ".gitignore"
            if not gi.exists():
                gi.write_text("links.json\n*.log\n", encoding="utf-8")
        except Exception:
            pass  # git 不可用时不阻塞主流程

    def commit(self, message: str) -> str:
        """提交一次；失败返回空串，不抛异常。"""
        from . import logger
        log = logger.get("git")
        try:
            from dulwich import porcelain
            self.ensure_repo()
            porcelain.add(str(self.hub), paths=["skills", "manifest.json"])
            status = porcelain.status(str(self.hub))
            staged = status.staged or {}
            if not (staged.get("add") or staged.get("delete") or staged.get("modify")):
                log.debug("commit 跳过（无变更）msg=%s", message)
                return message
            porcelain.commit(
                str(self.hub),
                message=message.encode("utf-8"),
                author=b"Skill Manager <local@localhost>",
                committer=b"Skill Manager <local@localhost>",
            )
            log.info("commit 成功 msg=%s", message)
            return message
        except Exception as e:
            log.error("commit 失败 msg=%s err=%s", message, e)
            return ""

    def history(self, limit: int = 30) -> list[dict]:
        try:
            from dulwich.repo import Repo
            repo = Repo(str(self.hub))
            out = []
            for entry in repo.get_walker(max_entries=limit):
                c = entry.commit
                out.append({
                    "message": c.message.decode("utf-8", "replace").strip(),
                    "time": time.strftime("%Y-%m-%d %H:%M", time.localtime(c.commit_time)),
                    "sha": c.id.decode()[:8],
                })
            return out
        except Exception:
            return []

    # ---------- 文件操作 ----------
    def adopt(self, src: Path, name: str) -> tuple[bool, str]:
        """把目录复制进 hub，校验后返回（调用方负责删原目录）。"""
        dst = self.path_of(name)
        if dst.exists():
            return False, f"hub 中已存在同名技能：{name}"
        try:
            shutil.copytree(src, dst)
            if not (dst / "SKILL.md").exists():
                shutil.rmtree(dst, ignore_errors=True)
                return False, "复制后缺少 SKILL.md"
            return True, ""
        except Exception as e:
            shutil.rmtree(dst, ignore_errors=True)
            return False, f"复制失败：{e}"

    def remove(self, name: str) -> tuple[bool, str]:
        dst = self.path_of(name)
        if not dst.exists():
            return False, "hub 中不存在"
        try:
            shutil.rmtree(dst)
            return True, ""
        except Exception as e:
            return False, f"删除失败：{e}"
