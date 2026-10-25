"""SKILL本地管理 —— 后端入口。"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from core import linker, logger, scanner
from core.store import Store

VERSION = "1.0.0"
BASE = Path(__file__).resolve().parent
THEMES = ("black", "white", "amber", "violet")


def _bad_name(name) -> bool:
    """技能名不允许空、路径分隔符、保留名。"""
    n = (name or "").strip()
    if not n or len(n) > 64 or n in (".", ".."):
        return True
    return any(c in n for c in '\\/:*?"<>|')
DATA = BASE / "data"
HUB = DATA / "hub"
TRASH = DATA / "trash"
TRASH_DAYS = 10
CONFIG_PATH = DATA / "config.json"
USER_SKILLS = Path.home() / ".dsh" / "skills"
DEFAULT_WORKSPACE_PARENT = ""   # 空 = 首次启动让用户选目录

app = Flask(__name__, static_folder=str(BASE / "static"), static_url_path="/static")


# ---------------- 配置 ----------------
def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            # utf-8-sig：兼容被记事本等工具写成带 BOM 的文件
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
        except Exception:
            pass
    return {"workspaces": [], "theme": "black", "port": 8765}


def save_config(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def agents_config() -> dict:
    """各 agent 的独立配置。缺省只有 dsh（沿用现有 data/hub）。"""
    cfg = load_config()
    a = cfg.get("agents") or {}
    if not isinstance(a, dict) or not a:
        a = {}
    a.setdefault("dsh", {
        "label": "DeepSeek",
        "hubDir": "data/hub",
        "globalSkillsDir": "~/.dsh/skills",
        "workspaceParent": DEFAULT_WORKSPACE_PARENT,
    })
    return a


def active_agent() -> str:
    aid = (load_config().get("activeAgent") or "dsh").strip()
    return aid if aid in agents_config() else "dsh"


def hub_dir() -> Path:
    """技能仓库：所有 agent 通用，技能真身只有一份。"""
    return DATA / "hub"


def hub_dir_for(agent_id: str) -> Path:
    """保留签名：仓库对所有 agent 通用，不再按 agent 区分。"""
    return DATA / "hub"


def global_skills_dir() -> Path:
    """当前 agent 的全局技能目录：用户手动指定优先，否则按候选规范探测。"""
    aid = active_agent()
    a = agents_config().get(aid, {})
    v = (a.get("globalSkillsDir") or "").strip()
    if v:
        p = expand_path(v)
        if str(p) not in ("", "."):
            return p
    chosen, _ = resolve_agent_dir(aid, "global")
    if str(chosen) not in ("", "."):
        return chosen
    v2 = (load_config().get("globalSkillsDir") or "").strip()
    if v2:
        p2 = expand_path(v2)
        if str(p2) not in ("", "."):
            return p2
    return USER_SKILLS


def workspace_parent() -> Path:
    """当前 agent 的工作区父目录（自动发现用）。"""
    a = agents_config().get(active_agent(), {})
    v = (a.get("workspaceParent") or load_config().get("workspaceParent") or "").strip()
    if v:
        try:
            p = Path(os.path.expanduser(v))
            if str(p) not in ("", "."):
                return p
        except Exception:
            pass
    v2 = DEFAULT_WORKSPACE_PARENT.strip()
    if v2:
        return Path(os.path.expanduser(v2))
    return Path("")


def agent_dirname() -> str:
    """当前 agent 在项目/用户目录下的隐藏目录名：.dsh / .claude / .codex"""
    return "." + active_agent()


def discover_workspaces() -> list[str]:
    cfg = load_config()
    seen = list(cfg.get("workspaces", []))
    parent = workspace_parent()
    adir = agent_dirname()
    if parent.is_dir():
        for d in sorted(parent.iterdir()):
            if d.is_dir() and (d / adir / "skills").is_dir():
                if str(d) not in seen:
                    seen.append(str(d))
    return seen


def roots() -> list[dict]:
    """只返回当前 agent 的位置：global + 各工作区。"""
    aid = active_agent()
    out = [{
        "key": "global", "label": "全局SKILL", "kind": "global", "agent": aid,
        "path": str(global_skills_dir()),
    }]
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
                "agent": aid,
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
            "agent": aid,
            "path": str(p / agent_dirname() / "skills"),
            "workspace": str(p),
        })
    return out


def root_of(key: str) -> dict | None:
    for r in roots():
        if r["key"] == key:
            return r
    return None


# ---------------- 状态 ----------------
def _trash_entries() -> list:
    """回收站清单；顺带清理超过保留期的条目。"""
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
            logger.get("trash").info("回收站过期自动清理 %s", d.name)
            continue
        names = meta.get("names") or []
        items.append({
            "id": d.name,
            "name": meta.get("name") or d.name.split("__")[0],
            "nameZh": meta.get("nameZh", ""),
            "desc": meta.get("desc", ""),
            "deletedAt": meta.get("deletedAt", 0),
            "links": meta.get("links", []),
            "sizeKb": meta.get("sizeKb", 0),
            "agent": meta.get("agent") or "",
            "familyId": meta.get("familyId") or "",
            "familyNames": names,
            "count": len(names) if names else 1,
            "daysLeft": max(0.0, round(TRASH_DAYS - age / 86400, 1)),
        })
    return sorted(items, key=lambda x: -x["deletedAt"])


def build_state() -> dict:
    log = logger.get("scan")
    t0 = time.perf_counter()
    store = Store(hub_dir())
    store.ensure_repo()
    man = store.all()

    hub_skills = scanner.scan_root(store.skills, "hub", "hub", "hub")
    hub_names = {s.name for s in hub_skills}

    entries: dict[str, dict] = {}
    for s in hub_skills:
        entries[s.name] = {
            "name": s.name,
            "nameZh": s.name_zh,
            "desc": s.description,
            "group": "hub",
            "status": "unlinked",
            "files": s.file_count,
            "sizeKb": s.size_kb,
            "mtime": s.mtime,
            "valid": s.valid,
            "links": [],
            "path": str(s.path),
        }

    # 分身分组：同一个 family 的技能互相可见
    fam_count: dict[str, int] = {}
    for nm in entries:
        meta = man.get(nm) or {}
        fam = (meta.get("family") or nm).strip() or nm
        entries[nm]["family"] = fam
        fam_count[fam] = fam_count.get(fam, 0) + 1
    for nm in entries:
        entries[nm]["familyCount"] = fam_count.get(entries[nm]["family"], 1)

    for r in roots():
        rp = Path(r["path"])
        rt0 = time.perf_counter()
        found = scanner.scan_root(rp, r["key"], r["label"], r["kind"])
        rcost = (time.perf_counter() - rt0) * 1000
        log.debug("扫描 %s -> %d 个 cost=%.1fms path=%s", r["label"], len(found), rcost, rp)
        if rcost > 500:
            log.warning("扫描偏慢 %s cost=%.0fms count=%d", r["label"], rcost, len(found))
        for s in found:
            key = s.name
            if s.is_link:
                if key in entries:
                    entries[key]["links"].append({"root": r["key"], "label": r["label"], "path": str(s.path)})
                    if entries[key]["status"] == "unlinked":
                        entries[key]["status"] = "linked"
                else:
                    entries[key] = {
                        "name": key, "nameZh": s.name_zh, "desc": s.description,
                        "group": r["key"], "status": "dead" if scanner.is_link(s.path) and not (s.path / "SKILL.md").exists() else "linked",
                        "files": s.file_count, "sizeKb": s.size_kb, "mtime": s.mtime, "valid": s.valid,
                        "links": [{"root": r["key"], "label": r["label"], "path": str(s.path)}],
                        "path": str(s.path),
                    }
                continue
            # 实体目录
            if key in entries:
                # 同名已在 hub，且此处是实体 → 额外副本
                entries[key]["links"].append({"root": r["key"], "label": r["label"], "path": str(s.path), "shadow": True})
                continue
            entries[key] = {
                "name": key, "nameZh": s.name_zh, "desc": s.description,
                "group": r["key"],
                "status": "local" if key not in hub_names else "unlinked",
                "files": s.file_count, "sizeKb": s.size_kb, "mtime": s.mtime, "valid": s.valid,
                "links": [],
                "path": str(s.path),
                "meta": man.get(key, {}),
            }

    # 已链接的技能，分类跟随第一个链接位置；未链接的回到上次所在分组
    for name, e in entries.items():
        meta = man.get(name) or {}
        e["lastRoot"] = meta.get("lastRoot", "")
        e["pinned"] = bool(meta.get("pinned", False))
        if e["links"]:
            if e["status"] != "dead":
                e["status"] = "linked"
            e["group"] = e["links"][0]["root"]
        elif e["lastRoot"]:
            e["group"] = e["lastRoot"]
            e["status"] = "unlinked"
        elif e["group"] != "hub":
            e["status"] = e["status"] if e["status"] == "dead" else "local"

    total_cost = (time.perf_counter() - t0) * 1000
    log.debug("扫描完成 技能=%d cost=%.1fms", len(entries), total_cost)
    if total_cost > 800:
        log.warning("build_state 偏慢 cost=%.0fms skills=%d", total_cost, len(entries))

    return {
        "roots": roots(),
        "skills": sorted(entries.values(), key=lambda x: x["name"].lower()),
        "trash": _trash_entries(),
        "trashDays": TRASH_DAYS,
        "history": store.history(30),
        "config": load_config(),
        "hubPath": str(hub_dir()),
        "activeAgent": active_agent(),
        "agents": [{"id": k, "label": v.get("label") or k} for k, v in agents_config().items()],
    }


# ---------------- 路由 ----------------
@app.after_request
def _no_cache(resp):
    """本地工具，前端资源不缓存，避免改了代码看不到效果。"""
    try:
        if request.path == "/" or request.path.startswith("/static/"):
            resp.headers["Cache-Control"] = "no-store, must-revalidate"
            resp.headers["Pragma"] = "no-cache"
            resp.headers["Expires"] = "0"
    except Exception:
        pass
    return resp


@app.get("/")
def index():
    return send_from_directory(BASE / "static", "index.html")


@app.get("/api/state")
def api_state():
    return jsonify(build_state())


@app.post("/api/rescan")
def api_rescan():
    return jsonify(build_state())


def _do_adopt(name: str, src: Path, target_key: str, target_path: Path) -> tuple[bool, str]:
    """把工作区/全局里的实体目录纳入 hub，并在原位置建链接。返回 (ok, err)。"""
    log = logger.get("adopt")
    store = Store(hub_dir())
    ok, err = store.adopt(src, name)
    if not ok:
        log.error("adopt 复制失败 name=%s err=%s", name, err)
        return False, err
    try:
        shutil.rmtree(src)
    except Exception as e:
        shutil.rmtree(store.path_of(name), ignore_errors=True)
        log.error("adopt 删原目录失败，已回滚 name=%s err=%s", name, e)
        return False, f"删除原目录失败：{e}"
    ok, err = linker.create_junction(target_path, store.path_of(name))
    if not ok:
        log.error("adopt 建链接失败（实体在 hub，原目录已删）name=%s err=%s", name, err)
        return False, err + "（实体已进 hub，原目录已移除）"
    store.put(name, {"adoptedAt": time.strftime("%Y-%m-%d %H:%M"), "root": target_key, "lastRoot": target_key})
    store.commit(f"adopt: {name}")
    log.info("adopt 完成 name=%s -> %s", name, target_path)
    return True, ""


@app.post("/api/adopt")
def api_adopt():
    body = request.get_json(force=True, silent=True) or {}
    name, root_key = body.get("name"), body.get("root")
    target_key = body.get("target") or root_key
    if _bad_name(name):
        return jsonify({"ok": False, "error": "技能名不合法"}), 400
    r = root_of(root_key)
    if not r:
        return jsonify({"ok": False, "error": "未知分类"}), 400
    rt = root_of(target_key)
    if not rt:
        return jsonify({"ok": False, "error": "未知目标分类"}), 400
    src = Path(r["path"]) / name
    if not src.is_dir() or scanner.is_link(src):
        return jsonify({"ok": False, "error": "源目录不存在或已是链接"}), 400

    ok, err = _do_adopt(name, src, target_key, Path(rt["path"]) / name)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    return jsonify({"ok": True, "state": build_state()})


@app.post("/api/adopt-all")
def api_adopt_all():
    """把当前所有「未纳管」技能逐个纳入 hub（首次使用引导用）。

    逐个执行、逐个报告，任何一个失败都不影响其它已完成项。
    """
    state = build_state()
    todo = []
    for entry in state["skills"]:
        if entry.get("status") != "local":
            continue
        p = Path(entry["path"])
        root_key = entry.get("group", "")
        for r in roots():
            if Path(r["path"]) == p.parent:
                root_key = r["key"]
                break
        todo.append((entry["name"], p, root_key))

    results = []
    for name, p, root_key in todo:
        ok, err = _do_adopt(name, p, root_key, p)
        results.append({"name": name, "ok": ok, "error": err})
    logger.get("adopt").info("adopt-all 完成 共 %d 个，成功 %d",
                             len(results), sum(1 for r in results if r["ok"]))
    return jsonify({
        "ok": all(r["ok"] for r in results) if results else True,
        "total": len(results),
        "adopted": sum(1 for r in results if r["ok"]),
        "results": results,
        "state": build_state(),
    })


@app.post("/api/link")
def api_link():
    body = request.get_json(force=True, silent=True) or {}
    name, root_key = body.get("name"), body.get("root")
    if _bad_name(name):
        return jsonify({"ok": False, "error": "技能名不合法"}), 400
    r = root_of(root_key)
    if not r:
        return jsonify({"ok": False, "error": "未知分类"}), 400
    store = Store(hub_dir())
    target = store.path_of(name)
    if not target.is_dir():
        return jsonify({"ok": False, "error": "hub 中没有该技能"}), 400
    link = Path(r["path"]) / name
    if link.exists() and scanner.is_link(link):
        try:
            cur = os.readlink(link)
            if cur.startswith("\\\\?\\"):
                cur = cur[4:]
            cur_n = os.path.normcase(cur.rstrip("\\"))
            tgt_n = os.path.normcase(str(target.resolve()).rstrip("\\"))
            same = cur_n == tgt_n
        except OSError:
            same = False
        if same:
            return jsonify({"ok": True, "state": build_state()})
    log = logger.get("link")
    t0 = time.perf_counter()
    ok, err = linker.create_junction(link, target)
    if not ok:
        log.error("link 失败 name=%s root=%s err=%s cost=%.0fms",
                  name, r["label"], err, (time.perf_counter() - t0) * 1000)
        return jsonify({"ok": False, "error": err}), 400
    store.commit(f"link: {name} -> {r['label']}")
    log.info("link 完成 name=%s -> %s cost=%.0fms", name, r["label"], (time.perf_counter() - t0) * 1000)
    return jsonify({"ok": True, "state": build_state()})


@app.post("/api/unlink")
def api_unlink():
    body = request.get_json(force=True, silent=True) or {}
    name, root_key = body.get("name"), body.get("root")
    logger.get("unlink").info("unlink 请求 name=%s root=%s toHub=%s purgeCopy=%s",
                             name, root_key, body.get("toHub"), body.get("purgeCopy"))
    if _bad_name(name):
        return jsonify({"ok": False, "error": "技能名不合法"}), 400
    r = root_of(root_key)
    if not r:
        logger.get("unlink").error("unlink 未知分类 root=%s", root_key)
        return jsonify({"ok": False, "error": "未知分类"}), 400
    target_path = Path(r["path"]) / name
    ok, err = False, ""
    if target_path.exists() and not scanner.is_link(target_path):
        # 实体副本：只有在 hub 已有同名实体且要求清副本时才删
        store_probe = Store(hub_dir())
        if body.get("purgeCopy") and store_probe.path_of(name).is_dir():
            try:
                import shutil as _sh
                _sh.rmtree(target_path)
                ok, err = True, "removed-copy"
            except Exception as e:
                ok, err = False, f"删除副本失败：{e}"
        else:
            ok, err = False, "该位置是实体目录，不是链接"
    else:
        ok, err = linker.remove_junction(target_path)
    lg = logger.get("unlink")
    if ok:
        lg.info("unlink 结果 name=%s ok=True", name)
    else:
        lg.error("unlink 失败 name=%s detail=%s", name, err)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    store = Store(hub_dir())
    meta = dict(store.get(name) or {})
    if body.get("toHub"):
        meta.pop("lastRoot", None)
    else:
        meta["lastRoot"] = root_key
    store.put(name, meta)
    store.commit(f"unlink: {name} <- {r['label']}")
    return jsonify({"ok": True, "state": build_state()})


def _trash_family(members: list[str]) -> tuple[bool, str, str]:
    """把一组分身放进回收站的同一个条目里。返回 (ok, err, trashId)。"""
    store = Store(hub_dir())
    TRASH.mkdir(parents=True, exist_ok=True)
    tid = "fam-" + time.strftime("%Y%m%d-%H%M%S")
    tpath = TRASH / tid
    seq = 1
    while tpath.exists():
        tpath = TRASH / f"{tid}-{seq}"
        seq += 1
    tpath.mkdir(parents=True)
    moved, links_removed, size_kb = [], [], 0
    for mem in members:
        src = store.path_of(mem)
        if not src.is_dir():
            continue
        for r in roots():
            p = Path(r["path"]) / mem
            if linker.is_link(p):
                ok, _ = linker.remove_junction(p)
                if ok:
                    links_removed.append(f"{mem}@{r['label']}")
        try:
            size_kb += sum(f.stat().st_size for f in src.rglob("*") if f.is_file()) // 1024
        except Exception:
            pass
        try:
            shutil.move(str(src), str(tpath / mem))
        except Exception as e:
            logger.get("delete").error("分身移入回收站失败 mem=%s err=%s", mem, e)
            continue
        moved.append(mem)
    if not moved:
        shutil.rmtree(tpath, ignore_errors=True)
        return False, "没有可删除的分身", ""
    desc_main, zh_main = "", ""
    try:
        fm0 = scanner.read_frontmatter(tpath / moved[0] / "SKILL.md")
        desc_main = fm0.get("description", "")
        zh_main = fm0.get("name_zh", "")
    except Exception:
        pass
    meta = {
        "names": moved,
        "name": moved[0],
        "nameZh": zh_main,
        "desc": desc_main,
        "deletedAt": time.time(),
        "links": links_removed,
        "sizeKb": size_kb,
        "agent": active_agent(),
        "familyId": tpath.name,
    }
    try:
        (tpath / "_trash.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    for mem in moved:
        store.drop(mem)
    cfg = load_config()
    changed = False
    for mem in moved:
        if mem in cfg.get("skillGroups", {}):
            cfg["skillGroups"].pop(mem, None)
            changed = True
    if changed:
        save_config(cfg)
    return True, "", tpath.name


def _delete_one(name: str, extra: dict | None = None) -> tuple[bool, str, str]:
    """删除单个技能：移除链接 -> 移入回收站。返回 (ok, err, trashId)。"""
    store = Store(hub_dir())
    dst = store.path_of(name)
    removed = []
    for r in roots():
        p = Path(r["path"]) / name
        if linker.is_link(p):
            ok, _ = linker.remove_junction(p)
            if ok:
                removed.append(r["label"])
    if not dst.is_dir():
        return False, "没有这个技能", ""
    fm = {}
    try:
        fm = scanner.read_frontmatter(dst / "SKILL.md")
    except Exception:
        fm = {}
    size_kb = 0
    try:
        size_kb = sum(f.stat().st_size for f in dst.rglob("*") if f.is_file()) // 1024
    except Exception:
        pass
    TRASH.mkdir(parents=True, exist_ok=True)
    tid = f"{name}__{time.strftime('%Y%m%d-%H%M%S')}"
    tpath = TRASH / tid
    seq = 1
    while tpath.exists():
        tpath = TRASH / f"{tid}-{seq}"
        seq += 1
    try:
        shutil.move(str(dst), str(tpath))
    except Exception as e:
        return False, f"移入回收站失败：{e}", ""
    meta = {
        "name": name,
        "nameZh": fm.get("name_zh", ""),
        "desc": fm.get("description", ""),
        "deletedAt": time.time(),
        "links": removed,
        "sizeKb": size_kb,
        "agent": active_agent(),
    }
    if extra:
        meta.update(extra)
    try:
        (tpath / "_trash.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    store.drop(name)
    cfg = load_config()
    if name in cfg.get("skillGroups", {}):
        cfg["skillGroups"].pop(name, None)
        save_config(cfg)
    return True, "", tpath.name


@app.delete("/api/skill")
def api_delete():
    body = request.get_json(force=True, silent=True) or {}
    name = (body.get("name") or "").strip()
    with_family = bool(body.get("deleteFamily"))
    if _bad_name(name):
        return jsonify({"ok": False, "error": "技能名不合法"}), 400
    store = Store(hub_dir())
    dst = store.path_of(name)

    if not dst.is_dir():
        # 实体不在仓库：只断开它在各处的链接
        removed = []
        for r in roots():
            p = Path(r["path"]) / name
            if linker.is_link(p):
                ok, _ = linker.remove_junction(p)
                if ok:
                    removed.append(r["label"])
        if not removed:
            return jsonify({"ok": False, "error": "没有这个技能"}), 404
        cfg = load_config()
        if name in cfg.get("skillGroups", {}):
            cfg["skillGroups"].pop(name, None)
            save_config(cfg)
        store.commit(f"unlink-external: {name}")
        logger.get("delete").info("delete 外部链接 name=%s 移除=%s", name, removed)
        return jsonify({"ok": True, "removedLinks": removed, "state": build_state()})

    # 连带删除分身：整组放进回收站的同一个条目
    if with_family:
        members = [name] + [m for m in store.siblings(name) if m != name]
        if len(members) > 1:
            ok, err, tid = _trash_family(members)
            if not ok:
                return jsonify({"ok": False, "error": err}), 500
            store.commit(f"trash: {len(members)} 个分身（{tid}）")
            logger.get("delete").info("删除分身组 id=%s members=%s", tid, members)
            return jsonify({"ok": True, "family": tid, "names": members,
                            "trashId": tid, "removedLinks": [], "state": build_state()})

    ok, err, tid = _delete_one(name)
    if not ok:
        return jsonify({"ok": False, "error": err}), 500
    store.commit(f"trash: {name}")
    logger.get("delete").info("delete 移入回收站 name=%s id=%s", name, tid)
    return jsonify({"ok": True, "trashId": tid, "state": build_state()})


def _trash_dir(tid: str):
    """校验并返回回收站条目目录。"""
    t = (tid or "").strip()
    if not t or any(c in t for c in '\\/:*?"<>|') or ".." in t:
        return None
    p = TRASH / t
    return p if p.is_dir() else None


@app.post("/api/trash/restore")
def api_trash_restore():
    body = request.get_json(force=True, silent=True) or {}
    src = _trash_dir(body.get("id"))
    if not src:
        return jsonify({"ok": False, "error": "回收站里没有这一项"}), 404
    meta_file = src / "_trash.json"
    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except Exception:
        meta = {}
    origin = (meta.get("agent") or "").strip() or active_agent()
    target_hub = hub_dir_for(origin)
    skills_dir = target_hub / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    names = meta.get("names") or []
    if names:
        # 分身组：只恢复主名那一个，其余分身直接丢掉（内容相同，相当于取消分身）
        main = names[0]
        sub = src / main
        if not sub.is_dir():
            return jsonify({"ok": False, "error": "回收站内容缺失"}), 404
        if _bad_name(main):
            return jsonify({"ok": False, "error": "技能名不合法"}), 400
        dst = skills_dir / main
        if dst.exists():
            return jsonify({"ok": False, "error": "同名技能已存在，先处理它再恢复"}), 400
        try:
            shutil.move(str(sub), str(dst))
        except Exception as e:
            return jsonify({"ok": False, "error": f"恢复失败：{e}"}), 500
        dropped = [nm for nm in names if nm != main]
        shutil.rmtree(src, ignore_errors=True)
        st = Store(target_hub)
        st.commit(f"restore: {main}")
        logger.get("trash").info("恢复分身组主条目 name=%s，丢弃分身=%s", main, dropped)
        return jsonify({"ok": True, "name": main, "dropped": dropped, "agent": origin,
                        "unlinked": True, "path": str(dst), "state": build_state()})

    name = (meta.get("name") or src.name.split("__")[0]).strip()
    if _bad_name(name):
        return jsonify({"ok": False, "error": "技能名不合法"}), 400
    dst = skills_dir / name
    if dst.exists():
        return jsonify({"ok": False, "error": "同名技能已存在，先处理它再恢复"}), 400
    try:
        shutil.move(str(src), str(dst))
    except Exception as e:
        return jsonify({"ok": False, "error": f"恢复失败：{e}"}), 500
    junk = dst / "_trash.json"
    if junk.exists():
        junk.unlink()
    st = Store(target_hub)
    st.commit(f"restore: {name}")
    label = (agents_config().get(origin) or {}).get("label") or origin
    logger.get("trash").info("恢复 name=%s（原属 agent=%s）", name, origin)
    return jsonify({"ok": True, "name": name, "agent": origin, "agentLabel": label,
                    "unlinked": True, "path": str(dst), "state": build_state()})


@app.post("/api/trash/purge")
def api_trash_purge():
    body = request.get_json(force=True, silent=True) or {}
    src = _trash_dir(body.get("id"))
    if not src:
        return jsonify({"ok": False, "error": "回收站里没有这一项"}), 404
    name = src.name
    shutil.rmtree(src, ignore_errors=True)
    logger.get("trash").info("彻底删除 %s", name)
    return jsonify({"ok": True, "state": build_state()})


@app.post("/api/trash/clear")
def api_trash_clear():
    if TRASH.is_dir():
        shutil.rmtree(TRASH, ignore_errors=True)
    logger.get("trash").info("清空回收站")
    return jsonify({"ok": True, "state": build_state()})


@app.post("/api/pin")
def api_pin():
    body = request.get_json(force=True, silent=True) or {}
    name = (body.get("name") or "").strip()
    pinned = bool(body.get("pinned", True))
    if _bad_name(name):
        return jsonify({"ok": False, "error": "技能名不合法"}), 400
    store = Store(hub_dir())
    if not store.path_of(name).is_dir():
        return jsonify({"ok": False, "error": "找不到该技能"}), 404
    meta = dict(store.get(name) or {})
    meta["pinned"] = pinned
    store.put(name, meta)
    logger.get("pin").info("pin name=%s pinned=%s", name, pinned)
    return jsonify({"ok": True, "state": build_state()})


@app.post("/api/skill/clone")
def api_skill_clone():
    """复制一份同样的技能（分身），用于同一技能挂到不同 agent。"""
    body = request.get_json(force=True, silent=True) or {}
    name = (body.get("name") or "").strip()
    if not name:
        return jsonify({"ok": False, "error": "缺少技能名"}), 400
    store = Store(hub_dir())
    if not store.get(name):
        # manifest 缺记录时，只要目录在就补一条
        dst = store.path_of(name)
        if not dst.is_dir():
            return jsonify({"ok": False, "error": "这个技能不在仓库里，先纳入再复制"}), 400
        try:
            fm = scanner.read_frontmatter(dst / "SKILL.md")
        except Exception:
            fm = {}
        store.put(name, {"name_zh": fm.get("name_zh", ""),
                         "description": fm.get("description", "")})
    ok, new_name, err = store.clone(name)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    commit = store.commit(f"clone: {name} -> {new_name}")
    logger.get("skill").info("分身 name=%s -> %s", name, new_name)
    return jsonify({"ok": True, "name": new_name, "from": name, "commit": commit,
                    "state": build_state()})


@app.post("/api/skill/create")
def api_skill_create():
    import re as _re
    body = request.get_json(force=True, silent=True) or {}
    name = (body.get("name") or "").strip()
    zh = (body.get("name_zh") or "").strip()
    desc = (body.get("description") or "").strip() or "（待补充）"
    if not _re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", name):
        return jsonify({"ok": False, "error": "名称只能用小写字母、数字和连字符，2-64 位"}), 400
    store = Store(hub_dir())
    dst = store.path_of(name)
    if dst.exists():
        return jsonify({"ok": False, "error": "已存在同名技能"}), 400
    dst.mkdir(parents=True, exist_ok=True)
    title = zh or name
    lines = ["---", f"name: {name}"]
    if zh:
        lines.append(f"name_zh: {zh}")
    lines += [
        f"description: {desc}",
        "---",
        "",
        f"# {title}",
        "",
        desc,
        "",
        "## 何时使用",
        "",
        "- 当用户说「……」「……」时",
        "- 当需要……时",
        "",
        "## 怎么做",
        "",
        "1. 先确认：读一下……，搞清楚目标和约束",
        "2. 再执行：按……的步骤处理",
        "3. 最后验证：用……确认结果正确",
        "",
        "## 示例",
        "",
        "用户说：「……」",
        "",
        "处理方式：……",
        "",
        "## 注意事项",
        "",
        "- 做到……，不要……",
        "- 遇到……时先停下来问",
        "",
    ]
    (dst / "SKILL.md").write_text("\n".join(lines), encoding="utf-8")
    store.put(name, {"createdAt": True})
    store.commit(f"create: {name}")
    return jsonify({"ok": True, "state": build_state()})


@app.get("/api/skill/content")
def api_skill_content():
    name = (request.args.get("name") or "").strip()
    if _bad_name(name):
        return jsonify({"ok": False, "error": "技能名不合法"}), 400
    store = Store(hub_dir())
    f = store.path_of(name) / "SKILL.md"
    if not f.exists():
        return jsonify({"ok": False, "error": "找不到 SKILL.md"}), 404
    return jsonify({"ok": True, "content": f.read_text(encoding="utf-8")})


@app.put("/api/skill/content")
def api_skill_save():
    body = request.get_json(force=True, silent=True) or {}
    name = (body.get("name") or "").strip()
    content = body.get("content", "")
    if _bad_name(name):
        return jsonify({"ok": False, "error": "技能名不合法"}), 400
    store = Store(hub_dir())
    f = store.path_of(name) / "SKILL.md"
    if not f.exists():
        return jsonify({"ok": False, "error": "找不到 SKILL.md"}), 404
    backup = f.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return jsonify({"ok": False, "error": "内容必须以 --- 开头的 frontmatter 开始"}), 400
    sync_family = bool(body.get("syncFamily"))
    detach_family = bool(body.get("detachFamily"))
    f.write_text(content, encoding="utf-8")
    detached = False
    if detach_family:
        # 断开关联：从 manifest 里去掉 family，成为独立技能
        meta = store.get(name) or {}
        meta.pop("family", None)
        store.put(name, meta)
        detached = True
    synced = []
    if sync_family:
        import re as _re
        for mem in store.siblings(name):
            if mem == name:
                continue
            mf = store.path_of(mem) / "SKILL.md"
            if not mf.exists():
                continue
            try:
                txt = _re.sub(r"^name:.*$", f"name: {mem}", content, count=1, flags=_re.M)
                mf.write_text(txt, encoding="utf-8")
                synced.append(mem)
            except Exception as e:
                logger.get("skill").error("同步分身失败 mem=%s err=%s", mem, e)
    msg = store.commit(f"edit: {name}/SKILL.md" + (f" (+{len(synced)} 个分身)" if synced else ""))
    if not msg:
        f.write_text(backup, encoding="utf-8")
        return jsonify({"ok": False, "error": "提交失败，已还原"}), 500
    return jsonify({"ok": True, "synced": synced, "detached": detached, "state": build_state()})


@app.post("/api/reveal")
def api_reveal():
    """在资源管理器里打开 hub 目录。"""
    body = request.get_json(force=True, silent=True) or {}
    raw = (body.get("path") or "").strip()
    try:
        hub = hub_dir().resolve()
        target = Path(raw).resolve() if raw else hub
    except Exception:
        return jsonify({"ok": False, "error": "路径无效"}), 400
    if target != hub and hub not in target.parents:
        return jsonify({"ok": False, "error": "只允许打开 hub 目录"}), 403
    if not target.exists():
        return jsonify({"ok": False, "error": "目录不存在"}), 404
    try:
        os.startfile(str(target))
    except Exception as e:
        return jsonify({"ok": False, "error": f"打开失败：{e}"}), 500
    logger.get("reveal").info("打开目录 path=%s", target)
    return jsonify({"ok": True, "path": str(target)})


@app.get("/api/history")
def api_history():
    return jsonify({"ok": True, "history": Store(hub_dir()).history(50)})


@app.post("/api/import")
def api_import():
    body = request.get_json(force=True, silent=True) or {}
    raw = (body.get("path") or "").strip()
    if not raw:
        return jsonify({"ok": False, "error": "未选择路径"}), 400
    src = Path(raw)
    if not src.is_dir():
        return jsonify({"ok": False, "error": "请选择一个文件夹"}), 400
    if not (src / "SKILL.md").exists():
        return jsonify({"ok": False, "error": "该文件夹里没有 SKILL.md"}), 400

    store = Store(hub_dir())
    name = src.name
    ok, err = store.adopt(src, name)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    store.put(name, {"importedFrom": str(src)})
    store.commit(f"import: {name}")
    return jsonify({"ok": True, "state": build_state()})


@app.post("/api/onboard")
def api_onboard():
    """标记「已看过首次使用说明」。"""
    cfg = load_config()
    cfg["onboarded"] = True
    save_config(cfg)
    logger.get("start").info("首次使用说明已确认")
    return jsonify({"ok": True, "state": build_state()})


# 各 agent 的目录规范（多候选，按顺序探测；支持 ${ENV} 展开）
# 依据见 检测规范.md「其他 agent 的路径」一节（2026-10 查证）。
AGENT_CANDIDATES = [
    {"id": "dsh", "label": "DeepSeek", "format": "skills",
     "global": ["~/.dsh/skills", "~/.agents/skills"],
     "workspace": [".dsh/skills", ".agents/skills"],
     "hubDir": "data/hub", "workspaceParent": DEFAULT_WORKSPACE_PARENT,
     "doc": "~/.dsh/skills 为主；~/.agents/skills 是跨工具共享目录"},
    {"id": "claude", "label": "Claude Code", "format": "skills",
     "global": ["${CLAUDE_CONFIG_DIR}/skills", "~/.claude/skills", "~/.agents/skills"],
     "workspace": [".claude/skills", ".agents/skills"],
     "hubDir": "data/hub", "workspaceParent": DEFAULT_WORKSPACE_PARENT,
     "doc": "用户级 ~/.claude/skills；项目级 .claude/skills"},
    {"id": "codex", "label": "Codex", "format": "skills",
     "global": ["${CODEX_HOME}/skills", "~/.codex/skills"],
     "workspace": [".codex/skills"],
     "hubDir": "data/hub", "workspaceParent": DEFAULT_WORKSPACE_PARENT,
     "doc": "CODEX_HOME 优先，默认 ~/.codex/skills"},
    {"id": "cursor", "label": "Cursor", "format": "skills",
     "global": ["~/.agents/skills", "~/.cursor/skills"],
     "workspace": [".cursor/skills", ".agents/skills"],
     "hubDir": "data/hub", "workspaceParent": DEFAULT_WORKSPACE_PARENT,
     "doc": "官方支持 .cursor/skills（含子文件夹）与 ~/.agents/skills"},
    {"id": "windsurf", "label": "Windsurf", "format": "rules",
     "global": ["~/AppData/Roaming/Windsurf/rules", "C:/ProgramData/Windsurf/rules",
                "~/.windsurf/rules"],
     "workspace": [".windsurf/rules", ".devin/rules"],
     "hubDir": "data/hub", "workspaceParent": DEFAULT_WORKSPACE_PARENT,
     "doc": "rules 格式；全局在 AppData/Roaming 或 ProgramData"},
    {"id": "cline", "label": "Cline", "format": "rules",
     "global": ["~/.cline/rules"],
     "workspace": [".cline/rules", ".clinerules"],
     "hubDir": "data/hub", "workspaceParent": DEFAULT_WORKSPACE_PARENT,
     "doc": "rules 格式；工作区 .cline/rules"},
]


def expand_path(raw: str) -> Path:
    """展开 ~ 与 ${ENV}；环境变量缺失时返回空路径。"""
    v = (raw or "").strip()
    if not v:
        return Path("")
    try:
        v2 = os.path.expandvars(v)
        if "${" in v2 or v2 == v and "$" in v:
            tail = v.split("${", 1)[1].split("}", 1)[0] if "${" in v else ""
            if tail and not os.environ.get(tail):
                return Path("")
        return Path(os.path.expanduser(v2))
    except Exception:
        return Path("")


def resolve_agent_dir(agent_id: str, kind: str = "global", workspace: Path | None = None) -> tuple[Path, dict]:
    """解析某个 agent 某类目录：返回 (选中的路径, 探测详情)。"""
    spec = next((c for c in AGENT_CANDIDATES if c["id"] == agent_id), None)
    if not spec:
        return Path(""), {"candidates": [], "chosen": "", "reason": "未知 agent"}
    key = "global" if kind == "global" else "workspace"
    raws = spec.get(key) or []
    checked = []
    chosen = Path("")
    for raw in raws:
        if kind == "workspace":
            if workspace is None:
                continue
            p = Path(workspace) / raw
        else:
            p = expand_path(raw)
            if str(p) in ("", "."):
                continue
        exists = bool(str(p)) and p.is_dir()
        checked.append({"raw": raw, "path": str(p), "exists": exists})
        if exists and not chosen.name:
            chosen = p
    if str(chosen) in ("", ".") and raws:
        # 都不存在：取第一个能展开的作为默认（之后创建）
        for raw in raws:
            cand = (Path(workspace) / raw) if kind == "workspace" and workspace else expand_path(raw)
            if str(cand) not in ("", "."):
                chosen = cand
                break
    return chosen, {"candidates": checked, "chosen": str(chosen), "doc": spec.get("doc", "")}




@app.get("/api/agents/candidates")
def api_agents_candidates():
    """探测本机可能存在的 agent 目录，供首次启动与设置页使用。"""
    configured = agents_config()
    items = []
    for c in AGENT_CANDIDATES:
        chosen, detail = resolve_agent_dir(c["id"], "global")
        exists = any(x["exists"] for x in detail["candidates"]) or c["id"] == "dsh"
        items.append({
            "id": c["id"],
            "label": c["label"],
            "format": c.get("format", "skills"),
            "globalSkillsDir": str(chosen),
            "hubDir": c.get("hubDir", "data/hub"),
            "workspaceParent": c.get("workspaceParent", DEFAULT_WORKSPACE_PARENT),
            "detected": exists,
            "enabled": c["id"] in configured,
            "custom": False,
            "probe": detail,
        })
    for aid, a in configured.items():
        if any(x["id"] == aid for x in items):
            continue
        items.append({
            "id": aid,
            "label": a.get("label") or aid,
            "globalSkillsDir": a.get("globalSkillsDir") or "",
            "hubDir": a.get("hubDir") or f"data/agents/{aid}/hub",
            "workspaceParent": a.get("workspaceParent") or DEFAULT_WORKSPACE_PARENT,
            "detected": True,
            "enabled": True,
            "custom": True,
        })
    return jsonify({"items": items, "active": active_agent()})


@app.post("/api/agents/save")
def api_agents_save():
    """保存 agent 配置（复选框 + 可编辑路径）。dsh 始终保留。"""
    body = request.get_json(force=True, silent=True) or {}
    items = body.get("items") or []
    agents = {}
    for it in items:
        aid = (it.get("id") or "").strip()
        if not aid or not it.get("enabled", True):
            continue
        if not all(ch.isalnum() or ch in "-_" for ch in aid):
            continue
        agents[aid] = {
            "label": (it.get("label") or aid).strip(),
            "hubDir": (it.get("hubDir") or f"data/agents/{aid}/hub").strip(),
            "globalSkillsDir": (it.get("globalSkillsDir") or "").strip(),
            "workspaceParent": (it.get("workspaceParent") or DEFAULT_WORKSPACE_PARENT).strip(),
        }
    if "dsh" not in agents:
        d = next(c for c in AGENT_CANDIDATES if c["id"] == "dsh")
        agents["dsh"] = {"label": d["label"], "hubDir": d["hubDir"],
                          "globalSkillsDir": d["globalSkillsDir"],
                          "workspaceParent": d["workspaceParent"]}
    cfg = load_config()
    cfg["agents"] = agents
    if (cfg.get("activeAgent") or "") not in agents:
        cfg["activeAgent"] = "dsh" if "dsh" in agents else next(iter(agents))
    save_config(cfg)
    for aid, a in agents.items():
        hd = hub_dir_for(aid)
        (hd / "skills").mkdir(parents=True, exist_ok=True)
    logger.get("start").info("保存 agent 配置: %s", list(agents))
    return jsonify({"ok": True, "active": cfg["activeAgent"], "state": build_state()})


@app.get("/api/detect")
def api_detect():
    """检测全局与各工作区的技能（只扫一层，不递归，不扫项目子目录）。"""
    import json as _json
    adir = agent_dirname()
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
    return jsonify({
        "agent": active_agent(),
        "rules": {
            "global": f"<用户目录>/{adir}/skills/<技能名>/SKILL.md",
            "workspace": f"<工作区>/{adir}/skills/<技能名>/SKILL.md",
            "depth": 1,
            "recursive": False,
            "projectLevel": False,
            "note": "只检测全局与工作区母文件夹下的技能；工作区内按项目分的子文件夹一律不检测。",
        },
        "global": {
            "path": str(gdir),
            "exists": gdir.is_dir(),
            "skills": skills_in(gdir),
        },
        "workspaces": workspaces,
        "counts": {
            "global": len(skills_in(gdir)),
            "workspace": sum(len(w["skills"]) for w in workspaces),
        },
    })


@app.get("/api/agents")
def api_agents():
    return jsonify({
        "active": active_agent(),
        "items": [{"id": k, "label": v.get("label") or k,
                   "hubDir": v.get("hubDir"), "globalSkillsDir": v.get("globalSkillsDir")}
                  for k, v in agents_config().items()],
    })


@app.post("/api/agent")
def api_agent():
    """切换当前 agent（各自独立的仓库与全局目录）。"""
    body = request.get_json(force=True, silent=True) or {}
    aid = (body.get("id") or "").strip()
    if not aid or aid not in agents_config():
        return jsonify({"ok": False, "error": "未知 agent"}), 400
    cfg = load_config()
    cfg["activeAgent"] = aid
    save_config(cfg)
    (hub_dir() / "skills").mkdir(parents=True, exist_ok=True)
    logger.get("start").info("切换 agent -> %s (hub=%s)", aid, hub_dir())
    return jsonify({"ok": True, "active": aid, "state": build_state()})


@app.post("/api/theme")
def api_theme():
    body = request.get_json(force=True, silent=True) or {}
    theme = (body.get("theme") or "").strip()
    if theme not in THEMES:
        return jsonify({"ok": False, "error": "未知主题"}), 400
    cfg = load_config()
    cfg["theme"] = theme
    save_config(cfg)
    return jsonify({"ok": True})


@app.post("/api/subgroup")
def api_subgroup():
    """全局SKILL 的查看用子分类：只是分组，不影响技能实际挂载。"""
    log = logger.get("subgroup")
    body = request.get_json(force=True, silent=True) or {}
    action = (body.get("action") or "").strip()
    cfg = load_config()
    groups = cfg.setdefault("subGroups", [])
    assign = cfg.setdefault("skillGroups", {})

    if action == "add":
        name = (body.get("name") or "").strip()
        if not name:
            return jsonify({"ok": False, "error": "分类名不能为空"}), 400
        if len(name) > 24:
            return jsonify({"ok": False, "error": "分类名最多 24 个字符"}), 400
        if any(g.get("name") == name for g in groups):
            return jsonify({"ok": False, "error": "已有同名分类"}), 400
        gid = "sg" + str(int(time.time() * 1000))
        while any(g.get("id") == gid for g in groups):
            gid += "x"
        parent = "hub" if body.get("parent") == "hub" else "global"
        groups.append({"id": gid, "name": name, "parent": parent})
        save_config(cfg)
        log.info("新增子分类 name=%s id=%s parent=%s", name, gid, parent)
        return jsonify({"ok": True, "id": gid, "state": build_state()})

    if action == "rename":
        gid = (body.get("id") or "").strip()
        name = (body.get("name") or "").strip()
        item = next((g for g in groups if g.get("id") == gid), None)
        if not item:
            return jsonify({"ok": False, "error": "分类不存在"}), 404
        if not name:
            return jsonify({"ok": False, "error": "分类名不能为空"}), 400
        if len(name) > 24:
            return jsonify({"ok": False, "error": "分类名最多 24 个字符"}), 400
        if any(g.get("name") == name and g.get("id") != gid for g in groups):
            return jsonify({"ok": False, "error": "已有同名分类"}), 400
        item["name"] = name
        save_config(cfg)
        log.info("重命名分类 id=%s -> %s", gid, name)
        return jsonify({"ok": True, "state": build_state()})

    if action == "remove":
        gid = (body.get("id") or "").strip()
        if not any(g.get("id") == gid for g in groups):
            return jsonify({"ok": False, "error": "分类不存在"}), 404
        before = len(groups)
        groups[:] = [g for g in groups if g.get("id") != gid]
        moved = [k for k, v in list(assign.items()) if v == gid]
        for k in moved:
            assign.pop(k, None)
        save_config(cfg)
        log.info("删除子分类 id=%s 归还技能=%d", gid, len(moved))
        return jsonify({"ok": True, "moved": len(moved), "state": build_state()})

    if action == "assign":
        skill = (body.get("skill") or "").strip()
        gid = (body.get("id") or "").strip()
        if not skill:
            return jsonify({"ok": False, "error": "缺少技能名"}), 400
        if gid and not any(g.get("id") == gid for g in groups):
            return jsonify({"ok": False, "error": "分类不存在"}), 404
        known = Store(hub_dir()).path_of(skill).is_dir() or any(
            (Path(r["path"]) / skill).exists() for r in roots()
        )
        if not known:
            return jsonify({"ok": False, "error": "技能不存在"}), 404
        if gid:
            assign[skill] = gid
        else:
            assign.pop(skill, None)
        save_config(cfg)
        log.info("归类 skill=%s -> %s", skill, gid or "(全局)")
        return jsonify({"ok": True, "state": build_state()})

    if action == "reorder":
        parent = "hub" if body.get("parent") == "hub" else "global"
        ids = body.get("ids") or []
        if not isinstance(ids, list) or not ids:
            return jsonify({"ok": False, "error": "ids 不能为空"}), 400
        same = [g for g in groups if (g.get("parent") or "global") == parent]
        others = [g for g in groups if (g.get("parent") or "global") != parent]
        by_id = {g.get("id"): g for g in same}
        ordered = [by_id[i] for i in ids if i in by_id]
        ordered += [g for g in same if g.get("id") not in ids]
        cfg["subGroups"] = ordered + others
        save_config(cfg)
        log.info("子分类重排 parent=%s ids=%s", parent, ids)
        return jsonify({"ok": True, "state": build_state()})

    if action == "move":
        gid = body.get("id")
        parent = "hub" if body.get("parent") == "hub" else "global"
        before = body.get("before")
        item = next((g for g in groups if g.get("id") == gid), None)
        if not item:
            return jsonify({"ok": False, "error": "找不到该分类"}), 404
        groups.remove(item)
        item["parent"] = parent
        if before:
            idx = next((i for i, g in enumerate(groups) if g.get("id") == before), None)
            if idx is None:
                groups.append(item)
            else:
                groups.insert(idx, item)
        else:
            groups.append(item)
        save_config(cfg)
        log.info("移动分类 id=%s -> parent=%s", gid, parent)
        return jsonify({"ok": True, "state": build_state()})

    return jsonify({"ok": False, "error": "未知动作"}), 400


@app.post("/api/workspace-parent")
def api_workspace_parent():
    """设置工作区父目录（自动发现用）。"""
    body = request.get_json(force=True, silent=True) or {}
    raw = (body.get("path") or "").strip()
    if not raw:
        return jsonify({"ok": False, "error": "缺少路径"}), 400
    p = Path(os.path.expanduser(os.path.expandvars(raw)))
    if not p.is_dir():
        return jsonify({"ok": False, "error": f"目录不存在：{p}"}), 400
    cfg = load_config()
    cfg["workspaceParent"] = str(p)
    # 该 agent 的配置也同步
    agents = cfg.get("agents") or {}
    aid = cfg.get("activeAgent") or "dsh"
    if aid in agents:
        agents[aid]["workspaceParent"] = str(p)
        cfg["agents"] = agents
    save_config(cfg)
    logger.get("start").info("工作区父目录 -> %s", p)
    return jsonify({"ok": True, "path": str(p), "state": build_state()})


@app.get("/api/workspaces")
def api_workspaces_list():
    """列出自动发现 + 手动添加的工作区。"""
    items = []
    for ws in discover_workspaces():
        p = Path(ws)
        sp = p / agent_dirname() / "skills"
        count = 0
        if sp.is_dir():
            count = sum(1 for c in sp.iterdir() if c.is_dir() and (c / "SKILL.md").is_file())
        items.append({"path": str(p), "name": p.name, "exists": p.is_dir(),
                      "skills": count, "manual": str(p) in (load_config().get("workspaces") or [])})
    return jsonify({
        "parent": str(workspace_parent()),
        "parentExists": workspace_parent().is_dir(),
        "rule": "父目录下，只要某个子目录里存在 <agent>/skills，就认为它是工作区（不看目录名）",
        "items": items,
    })


@app.post("/api/workspaces")
def api_workspaces():
    body = request.get_json(force=True, silent=True) or {}
    raw = body.get("workspaces") or []
    if not isinstance(raw, list):
        return jsonify({"ok": False, "error": "workspaces 必须是数组"}), 400
    paths = []
    for item in raw:
        try:
            p = Path(str(item))
            if p.is_dir() and (p / ".dsh" / "skills").is_dir():
                paths.append(str(p))
        except Exception:
            continue
    cfg = load_config()
    cfg["workspaces"] = paths
    save_config(cfg)
    return jsonify({"ok": True, "state": build_state()})


_INSTANCE_MUTEX = None
_INSTANCE_NAME = "SkillManager_SingleInstance_v1"


def _acquire_instance() -> bool:
    """取单实例锁。已有实例在跑时返回 False；非 Windows 或调用失败时放行。"""
    global _INSTANCE_MUTEX
    try:
        import ctypes
        from ctypes import wintypes

        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
        k32.CreateMutexW.restype = wintypes.HANDLE
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        h = k32.CreateMutexW(None, False, _INSTANCE_NAME)
        if not h:
            return True
        if ctypes.get_last_error() == 183:  # ERROR_ALREADY_EXISTS
            k32.CloseHandle(h)
            return False
        _INSTANCE_MUTEX = h
        return True
    except Exception:
        return True


def _activate_window(title: str = "SKILL本地管理", timeout: float = 4.0) -> bool:
    """把已有窗口提到前台。找不到（对方可能是 --web 模式）返回 False。"""
    import time as _t
    try:
        import ctypes
        from ctypes import wintypes

        u = ctypes.WinDLL("user32", use_last_error=True)
        u.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
        u.FindWindowW.restype = wintypes.HWND
        u.IsIconic.argtypes = [wintypes.HWND]
        u.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
        u.SetForegroundWindow.argtypes = [wintypes.HWND]
        u.BringWindowToTop.argtypes = [wintypes.HWND]

        deadline = _t.time() + timeout
        while _t.time() < deadline:
            hwnd = u.FindWindowW(None, title)
            if hwnd:
                if u.IsIconic(hwnd):
                    u.ShowWindow(hwnd, 9)  # SW_RESTORE
                u.BringWindowToTop(hwnd)
                u.SetForegroundWindow(hwnd)
                return True
            _t.sleep(0.2)  # 可能第一个实例还在创建窗口
    except Exception:
        return False
    return False


def _own_windows() -> list:
    """枚举属于当前进程的顶层窗口。"""
    import ctypes
    from ctypes import wintypes

    u = ctypes.windll.user32
    pid = ctypes.windll.kernel32.GetCurrentProcessId()
    found: list = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def _cb(hwnd, _lparam):
        wpid = wintypes.DWORD()
        u.GetWindowThreadProcessId(hwnd, ctypes.byref(wpid))
        if wpid.value == pid and u.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True

    u.EnumWindows(_cb, 0)
    return found


def _apply_window_icon(ico: pathlib.Path) -> bool:
    """给本进程窗口（含任务栏按钮）设置图标。"""
    try:
        import ctypes
        from ctypes import wintypes

        u = ctypes.windll.user32
        if not ico.exists():
            return False
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 0x10
        hicon = u.LoadImageW(None, str(ico), IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
        if not hicon:
            return False
        WM_SETICON = 0x0080
        ok = False
        for hwnd in _own_windows():
            u.SendMessageW(hwnd, WM_SETICON, 1, hicon)  # ICON_BIG
            u.SendMessageW(hwnd, WM_SETICON, 0, hicon)  # ICON_SMALL
            ok = True
        return ok
    except Exception:
        return False


class WindowApi:
    """前端按钮 -> 原生窗口动作。"""

    _maxed = False

    def _win(self):
        try:
            import webview
            return webview.windows[0] if webview.windows else None
        except Exception:
            return None

    def minimize(self):
        w = self._win()
        if w:
            try:
                w.minimize()
            except Exception:
                pass
        return True

    def toggle_max(self):
        w = self._win()
        if w is not None:
            try:
                if WindowApi._maxed:
                    w.restore()
                    WindowApi._maxed = False
                else:
                    w.maximize()
                    WindowApi._maxed = True
            except Exception:
                pass
        return True

    def get_pos(self):
        w = self._win()
        if w is None:
            return [0, 0]
        try:
            return [int(w.x), int(w.y)]
        except Exception:
            return [0, 0]

    def move_to(self, x, y):
        w = self._win()
        if w is not None:
            try:
                w.move(int(x), int(y))
            except Exception:
                pass
        return True

    def start_drag(self):
        """让系统接管窗口拖动（等效于按住标题栏）。"""
        log = BASE / "logs" / "drag.log"
        try:
            with log.open("a", encoding="utf-8") as f:
                f.write("called\n")
        except Exception:
            pass
        try:
            import ctypes
            from ctypes import wintypes

            u = ctypes.windll.user32
            hwnd = u.GetForegroundWindow()
            if not hwnd:
                wins = _own_windows()
                if not wins:
                    return False
                hwnd = wins[0]
            pt = wintypes.POINT()
            u.GetCursorPos(ctypes.byref(pt))
            lparam = (pt.y << 16) | (pt.x & 0xFFFF)
            u.ReleaseCapture()
            # 同步发送，系统会进入拖动循环，直到松开鼠标才返回
            u.SendMessageW(hwnd, 0x00A1, 2, lparam)  # WM_NCLBUTTONDOWN / HTCAPTION
            with log.open("a", encoding="utf-8") as f:
                f.write(f"sent hwnd={hwnd} xy={pt.x},{pt.y}\n")
            return True
        except Exception as e:
            try:
                with log.open("a", encoding="utf-8") as f:
                    f.write(f"error {e}\n")
            except Exception:
                pass
            return False

    def pick_folder(self):
        """弹出系统文件夹选择框，返回选中路径。"""
        try:
            import webview
            w = self._win()
            if w is None:
                return ""
            res = w.create_file_dialog(webview.FOLDER_DIALOG)
            if not res:
                return ""
            return res[0] if isinstance(res, (list, tuple)) else str(res)
        except Exception:
            return ""

    def close(self):
        try:
            w = self._win()
            if w is not None:
                try:
                    w.destroy()
                except Exception:
                    pass
        finally:
            import os as _os
            import threading as _th
            _th.Timer(0.6, lambda: _os._exit(0)).start()
        return True


def screen_size() -> tuple[int, int]:
    """返回主屏的逻辑分辨率（已按 DPI 缩放折算）。"""
    try:
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
        u = ctypes.windll.user32
        w, h = u.GetSystemMetrics(0), u.GetSystemMetrics(1)
        try:
            dpi = u.GetDpiForSystem()
            scale = dpi / 96.0 if dpi else 1.0
        except Exception:
            scale = 1.0
        if w > 400 and h > 300:
            return int(w / scale), int(h / scale)
    except Exception:
        pass
    return 1920, 1080


def main() -> None:
    log = logger.get("start")
    level = logger.setup(BASE / "logs")
    cfg = load_config()
    port = int(os.environ.get("SKILL_MANAGER_PORT", cfg.get("port", 8765)))
    host = "127.0.0.1"
    mode = "web" if ("--web" in sys.argv or os.environ.get("SKILL_MANAGER_WEB") == "1") else "window"
    log.info("启动 v%s python=%s pid=%s mode=%s loglevel=%s",
             VERSION, sys.version.split()[0], os.getpid(), mode, level)
    log.info("端口=%s host=%s 主题=%s workdir=%s", port, host, cfg.get("theme"), BASE)

    # 单实例：已经有窗口在跑就不再开第二个，直接切到前台
    if not _acquire_instance():
        if mode == "window":
            if _activate_window():
                log.info("已有实例在运行，已切到前台 pid=%s", os.getpid())
            else:
                log.info("已有实例在运行（无窗口），改为打开浏览器 pid=%s", os.getpid())
                import webbrowser
                webbrowser.open(f"http://{host}:{port}")
        else:
            log.info("已有实例占用端口 %s，web 模式退出", port)
            print(f"已有实例在运行，端口 {port} 被占用")
        return

    for r in roots():
        log.info("技能根 %s -> %s", r["label"], r["path"])

    if "--web" in sys.argv or os.environ.get("SKILL_MANAGER_WEB") == "1":
        app.run(host=host, port=port, debug=False)
        return

    # 默认：桌面窗口
    try:
        import webview
    except ImportError:
        print("未安装 pywebview，退回浏览器模式")
        app.run(host=host, port=port, debug=False)
        return

    import threading
    import time

    t = threading.Thread(target=lambda: app.run(host=host, port=port, debug=False, use_reloader=False), daemon=True)
    t.start()
    time.sleep(0.8)
    sw, sh = screen_size()
    width = min(max(int(sw * 0.76), 1300), 1960)
    height = min(max(int(sh * 0.84), 860), 1240)
    pos_x = max((sw - width) // 2, 0)
    pos_y = max((sh - height) // 2, 0)
    log.info("屏幕逻辑分辨率=%dx%d 窗口=%dx%d @(%d,%d)", sw, sh, width, height, pos_x, pos_y)

    webview.create_window(
        "SKILL本地管理",
        f"http://{host}:{port}",
        width=width,
        height=height,
        x=pos_x,
        y=pos_y,
        min_size=(1080, 700),
        frameless=True,
        easy_drag=False,
        js_api=WindowApi(),
        background_color="#0a0a12",
    )

    def _decorate() -> None:
        log = BASE / "logs" / "icon.log"
        for i in range(24):
            time.sleep(0.5)
            try:
                wins = _own_windows()
                ok = _apply_window_icon(BASE / "static" / "icon2.ico")
                with log.open("a", encoding="utf-8") as f:
                    f.write("%s try=%d windows=%d applied=%s\n"
                            % (time.strftime("%H:%M:%S"), i, len(wins), ok))
                if ok:
                    break
            except Exception:
                pass

    threading.Thread(target=_decorate, daemon=True).start()
    webview.start()


if __name__ == "__main__":
    main()
