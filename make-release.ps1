# 发布打包脚本（E5）
#
# 用途：生成一个**不带任何个人数据**的分发包，用来发给别人或上传 Release。
#
# 用法（在项目根目录）：
#   .\make-release.ps1                 # 生成 zip 到 dist/
#   .\make-release.ps1 -WithRuntime    # 连 Python 运行时一起打包（体积大，但解压即用）
#
# 这个脚本做的事：
#   1. 复制项目到临时目录
#   2. 排除：data/（个人技能与配置）、logs/、.git/、__pycache__、临时文件
#   3. 放入示例技能 data/hub/skills/example-skill/
#   4. 打成 zip

param(
    [switch]$WithRuntime
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Version = "1.0.0"
if (Test-Path (Join-Path $Root "CHANGELOG.md")) {
    $first = Select-String -Path (Join-Path $Root "CHANGELOG.md") -Pattern '^## \[([\d.]+)\]' | Select-Object -First 1
    if ($first -and $first.Matches.Count -gt 0) { $Version = $first.Matches[0].Groups[1].Value }
}

$Stamp = Get-Date -Format "yyyyMMdd"
$Name = "skill-profiles-$Version"
$Dist = Join-Path $Root "dist"
$Stage = Join-Path $Dist $Name
$Zip = Join-Path $Dist "$Name-$Stamp.zip"

Write-Host "==> 版本 $Version，输出到 dist/" -ForegroundColor Cyan

# ---------- 1) 清理旧产物 ----------
if (Test-Path $Stage) { Remove-Item $Stage -Recurse -Force }
New-Item -ItemType Directory -Path $Stage -Force | Out-Null

# ---------- 2) 复制（排除个人数据） ----------
$excludeDirs = @("data", "logs", ".git", "__pycache__", "dist", "臨時", ".venv", "venv")
$excludeFiles = @("*.pyc", "*.log", ".env")

# 内部文档：含本机路径与开发记录，不进分发包
$excludeNames = @("交接说明.md", "开源清单.md", "说明.txt")

# 再从 .gitignore 里取所有「具体文件名 / 目录名」（不含通配符）一并排除，
# 避免以后往 .gitignore 里加文件时忘记同步到本脚本。
if (Test-Path (Join-Path $Root ".gitignore")) {
    Get-Content (Join-Path $Root ".gitignore") -Encoding UTF8 | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line -notmatch '[*?[]') {
            $clean = $line.Trim("/")
            if ($clean -and $clean -notin $excludeDirs -and $clean -notin $excludeNames) {
                $excludeNames += $clean
            }
        }
    }
}

Write-Host "==> 复制文件（排除 data/ logs/ .git/ 及 .gitignore 列出的内部文件）" -ForegroundColor Cyan
Get-ChildItem -Path $Root -Force | Where-Object {
    $_.Name -notin $excludeDirs -and $_.Name -notin $excludeNames -and $_.Name -notlike "dist"
} | ForEach-Object {
    if ($_.PSIsContainer) {
        Copy-Item $_.FullName (Join-Path $Stage $_.Name) -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        Copy-Item $_.FullName (Join-Path $Stage $_.Name) -Force
    }
}

# 清掉复制进来的缓存
Get-ChildItem -Path $Stage -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $Stage -Recurse -File -Include "*.pyc" -ErrorAction SilentlyContinue |
    Remove-Item -Force -ErrorAction SilentlyContinue

# 按 .gitignore 里的具体路径再删一遍（处理 docs/xxx.md 这种带子目录的条目）
foreach ($item in $excludeNames) {
    $target = Join-Path $Stage $item
    if (Test-Path $target) {
        Remove-Item $target -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "    已排除：$item" -ForegroundColor DarkGray
    }
}

# ---------- 3) 放入示例技能 ----------
Write-Host "==> 放入示例技能" -ForegroundColor Cyan
$DemoSkill = Join-Path $Stage "data\hub\skills\example-skill"
New-Item -ItemType Directory -Path $DemoSkill -Force | Out-Null

@'
---
name: example-skill
name_zh: 示例技能
description: 演示 SKILL.md 的最小结构。第一次用就从这个改起。
---

# 示例技能

这个文件就是全部内容。复制一份、改名字和描述，就是一个新技能。

## 什么时候用

- 你想新建一个技能，但不知道从哪开始
- 你想看看 frontmatter 怎么写

## 怎么做

1. 改 `name`：小写字母、数字、连字符
2. 改 `description`：写「什么时候用」，不写「能做什么」
3. 下面的正文随便写，agent 会读它

## 示例

用户说「帮我检查一下这个项目」时，读这里的内容照着做。
'@ | Set-Content -Path (Join-Path $DemoSkill "SKILL.md") -Encoding UTF8

# 空配置（别人启动时自己生成，这里只放一份说明）
@'
{
  "_说明": "首次启动会自动生成。字段可选，含义见 config.example.json。"
}
'@ | Set-Content -Path (Join-Path $Stage "data\config.json") -Encoding UTF8

# ---------- 4) 可选：带 Python 运行时 ----------
if ($WithRuntime) {
    Write-Host "==> 打包 Python 运行时（体积较大）" -ForegroundColor Yellow
    $PyDir = Join-Path $env:USERPROFILE ".dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python"
    if (Test-Path $PyDir) {
        $RuntimeDst = Join-Path $Stage "runtime\python"
        New-Item -ItemType Directory -Path $RuntimeDst -Force | Out-Null
        Copy-Item "$PyDir\*" $RuntimeDst -Recurse -Force
        Write-Host "    已包含运行时：$PyDir" -ForegroundColor Gray
    } else {
        Write-Host "    未找到运行时，跳过" -ForegroundColor Yellow
    }
}

# ---------- 5) 打 zip ----------
Write-Host "==> 压缩" -ForegroundColor Cyan
if (Test-Path $Zip) { Remove-Item $Zip -Force }
Compress-Archive -Path $Stage -DestinationPath $Zip -CompressionLevel Optimal

# 清理暂存目录
Remove-Item $Stage -Recurse -Force

# ---------- 6) 报告 ----------
$size = [math]::Round((Get-Item $Zip).Length / 1MB, 1)
Write-Host ""
Write-Host "完成：$Zip" -ForegroundColor Green
Write-Host "大小：$size MB" -ForegroundColor Gray
Write-Host ""
Write-Host "包里有什么：" -ForegroundColor White
Write-Host "  ✅ 代码、文档、示例技能" -ForegroundColor Gray
Write-Host "  ✅ data/hub/skills/example-skill（唯一的技能）" -ForegroundColor Gray
Write-Host "  ❌ 你自己的技能、配置、回收站、git 历史（已排除）" -ForegroundColor Gray
