# 项目约定

> 接手项目先读 `docs/架构说明.md`（架构与数据流）和 `检测规范.md`（检测范围）。

## 这是什么

SKILL 本地管理 —— 管理本机技能仓库的桌面工具。Flask + pywebview + 原生 JS/CSS，单页无构建。

- 技能实体在 `data/hub/skills/<name>`
- 工作区里的 `.dsh/skills/<name>` 是指向实体的 junction
- 每次写操作自动 git 提交，历史可回滚
- 删除先进回收站 `data/trash`，保留 10 天

## 技能操作：一律用 CLI

**创建 / 修改 / 挂载 / 删除技能，必须用 `cli/skill.py`，不要手写 `data/hub` 下的文件。**

只有 CLI 会做 frontmatter 校验、git 提交、挂载位置检查、回收站记录。手写会漏掉这些。

```bash
python cli/skill.py list --status unlinked
python cli/skill.py create my-skill --zh 中文名 --desc "什么时候用这个技能" --content @body.md --link global --yes
```

命令速查看 `skill-cli` 技能（已挂到全局）；完整契约看 `cli/cli.spec.json` 与 `cli/README.md`。

## 改代码

| 层 | 文件 |
|---|---|
| 后端 | `app.py`、`core/store.py`、`core/scanner.py`、`core/platform.py`、`core/linker.py`、`core/logger.py` |
| 前端 | `static/index.html`（含 CSS）、`static/app.js` |
| CLI | `cli/skill.py`、`cli/cli.spec.json` |
| 测试 | `tests/test_cli.py`、`tests/run_tests.ps1` |

- 改完必须重启软件才生效（前端有 no-store，但 Python 进程是旧的）
- 调试：用 `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9333` 启动实例，再用 CDP 连 9333 执行 JS 和截图
- 平台相关代码只在 `core/platform.py`，其他地方不要直接调 `mklink`

## 约定

- 界面文案用中文
- 危险操作先确认（删除、清空、回滚）
- 改前端后必须实测——截图或用 CDP 断言，不要靠推理就说改好了
- 数据目录 `data/` 不要手工改，除非明确知道在做什么
- 跑测试：`python -m unittest discover -s tests`
