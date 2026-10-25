# 参与开发

欢迎提 Issue 和 PR。这个项目不大，先看这几条。

## 环境

```powershell
git clone https://github.com/<你的账号>/skill-profiles.git
cd skill-profiles
.\install.ps1
python app.py
```

- Windows 10/11（依赖 NTFS 目录链接）
- Python 3.9+
- 依赖版本见 `requirements.txt`（已锁定）

## 改之前先读

| 文档 | 内容 |
|---|---|
| [docs/架构说明.md](docs/架构说明.md) | 分层、数据流、为什么这么设计 |
| [检测规范.md](检测规范.md) | 检测哪些目录、不检测哪些 |
| [AGENTS.md](AGENTS.md) | 硬性约定 |

## 几条硬规矩

1. **技能操作一律走 CLI 或 `core/`**，不要直接手写 `data/hub` 下的文件——会漏校验、漏 git 提交、漏链接维护。
2. **所有「名字拼路径」都要走 `Store.path_of`**，它会拒绝空名、`..`、路径分隔符。
3. **平台相关代码只写在 `core/platform.py`**，别的地方不要直接调 `mklink`。
4. **前端插入 HTML 前必须 `esc()`**，否则技能名里的特殊字符会破版。
5. **界面文案走 `t("key")`**，中英两份字典都要加。

## 怎么测

```powershell
# CLI 契约测试（18 个，只读不写数据）
python -m unittest discover -s tests -v

# 语法
node --check static\app.js
python -m py_compile app.py cli\skill.py core\*.py
```

界面改动**要实际点一遍**，别只靠推理——WebView2 的渲染和普通浏览器有差异。

## 提交信息

用 `类型: 简短说明` 的格式：

```
fix: 回收站有内容时渲染崩溃
feat: 技能分身（复制副本）
docs: README 改写成对外版本
```

## 提 PR 前

- [ ] `tests/` 全过
- [ ] 改界面的话截个图贴在 PR 描述里
- [ ] 新增用户可见功能 → 更新 `CHANGELOG.md`
- [ ] 改动检测范围 → 同步更新 `检测规范.md`

## 许可证

提交 PR 即表示你同意以 [MIT](LICENSE) 授权你的贡献。
