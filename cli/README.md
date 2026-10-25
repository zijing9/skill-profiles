# skill —— 技能仓库命令行

给 AI agent 用的技能管理接口。默认输出 JSON，写操作要 `--yes`，全部支持 `--dry-run`。

契约文件：`cli.spec.json`（`skill schema` 会原样打印它）。

## 调用

```bash
# 三种等价写法
python cli/skill.py list
cli\skill.cmd list          # Windows，不含中文注释以免 cmd 解析错乱
.\skill.ps1 list            # PowerShell
```

把 `cli` 目录加进 PATH 后可以直接 `skill list`。

如果 `python` 不在 PATH，设一个环境变量即可：

```bash
set SKILL_PYTHON=C:\path\to\python.exe
```

## 结构化输入

参数太多或含嵌套时用 `--json`。**Windows 下优先用 `@file`**——命令行内联 JSON 容易被引号破坏：

```bash
skill create --json @payload.json --yes
```

```json
{"name": "my-skill", "zh": "我的技能", "desc": "什么时候用", "content": "## 正文", "link": "global"}
```

也支持 `--json -` 从 stdin 读。文件带 BOM 也能读（内部按 utf-8-sig 处理）。

## 输出格式

```bash
skill list --output ndjson        # 一行一个 JSON 对象，适合大结果集
skill list --fields name,status   # 只留需要的字段
skill list --human                # 人类可读的表格
```

## 最短上手

```bash
# 1. 看看有哪些位置可以挂
python cli/skill.py roots

# 2. 造一个技能（默认进仓库、未挂载）
python cli/skill.py create my-skill \
  --zh 我的技能 \
  --desc "什么时候该用这个技能，写清触发场景" \
  --content @body.md \
  --yes

# 3. 挂到全局或某个工作区
python cli/skill.py link my-skill --to global --yes
python cli/skill.py link my-skill --to "my-project" --yes

# 4. 查
python cli/skill.py list --status unlinked
python cli/skill.py get my-skill

# 5. 改 / 回滚
python cli/skill.py update my-skill --content @new.md --yes
python cli/skill.py history my-skill
python cli/skill.py diff my-skill --commit 1a2b3c4d
python cli/skill.py rollback my-skill --commit 1a2b3c4d --yes

# 6. 删（进回收站，10 天可恢复）
python cli/skill.py delete my-skill --yes
python cli/skill.py trash
python cli/skill.py restore my-skill__20261025-170000 --yes
```

## 命令一览

| 命令 | 作用 |
|---|---|
| `list` | 列表：`--status` `--group` `--pinned` `--sort name\|time\|size` `--limit` `--offset` |
| `get <name>` | 单个详情（状态、挂载点、大小、时间） |
| `history <name>` | 该技能的提交历史 |
| `roots` | 可挂载位置（hub / global / 各工作区） |
| `trash` | 回收站列表 |
| `schema` | 命令目录（本契约的机器可读版本） |
| `create <name>` | 校验 → 建目录 → 写正文 → 入库（可 `--link` 一步挂载） |
| `update <name>` | 改中文名 / 描述 / 正文 |
| `link <name> --to <位置>` | 挂载 |
| `unlink <name> [--from <位置>]` | 取消挂载（省略 --from 即全部移除） |
| `delete <name>` | 移入回收站并断开所有链接 |
| `restore <id>` | 从回收站恢复 |
| `purge <id>` | 彻底删除回收站条目 |
| `validate [<name>]` | 校验命名、frontmatter、大小 |
| `diff <name> --commit <sha>` | 某提交与当前内容的差异 |
| `rollback <name> --commit <sha>` | 恢复到该提交（生成新提交，不 reset） |
| `recover <name> --commit <sha>` | 从 git 历史恢复已删除的技能（需当前不存在） |

## 位置写法

| 写法 | 指向 |
|---|---|
| `hub` | SKILL仓库（只读位置，不能挂） |
| `global` | 全局SKILL（`~/.dsh/skills`） |
| `"my-project"` 或 `ws:my-project` | 某个工作区（大小写不敏感，必须唯一匹配） |

## 输出契约

成功：stdout 一个 JSON 值。

```json
{"items": [{"name": "x", "status": "unlinked", "links": []}], "next": null}
```

失败：stdout 为空，stderr 是结构化错误，退出码非零。

```json
{"error": {"code": "SKILL_NOT_FOUND", "message": "技能「x」不存在",
           "suggestion": "skill list --limit 50", "recoverable": false}}
```

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 成功 |
| 1 | 内部错误 |
| 2 | 用法错误 / 缺 `--yes` / 名字不合法 |
| 20 | 不存在（技能、回收站条目、位置、提交） |
| 21 | 已存在（没加 `--upsert`） |
| 22 | 前置条件不满足（目标已有同名、未挂载却取消） |
| 30 | 外部依赖失败（git 提交） |

## 护栏

- 技能名只允许 `^[a-z0-9][a-z0-9-]{0,63}$`；中文名放 `--zh`，可留空
- 写操作必须显式 `--yes`，否则 `exit 2` 并打印可直接复制的命令
- `rollback` 只能回到该技能自己的提交，只写回该技能目录，永远生成新提交
- 没有 `--all` 批量删除，没有原始 git 透传
- 删除先进回收站（`data/trash`，保留 10 天），不是物理删
