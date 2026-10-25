# install.ps1 —— 一键安装依赖（Windows）
#
# 用法（在项目根目录打开 PowerShell）：
#   .\install.ps1              # 装依赖
#   .\install.ps1 -AddToPath   # 装依赖 + 把 CLI 加到当前用户的 PATH
#   .\install.ps1 -Check       # 只检查环境，不动任何东西
#
# 不需要管理员权限。

param(
    [switch]$AddToPath,
    [switch]$Check
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "    $msg" -ForegroundColor Green }
function Write-Warn2($msg){ Write-Host "    $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "    $msg" -ForegroundColor Red }

# ---------- 1. 找 Python ----------
Write-Step "检查 Python"

$python = $null
$candidates = @()

if ($env:SKILL_PYTHON) { $candidates += $env:SKILL_PYTHON }
$candidates += (Join-Path $env:USERPROFILE ".dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe")
$candidates += "python"
$candidates += "python3"

foreach ($c in $candidates) {
    try {
        $ver = & $c -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
        if ($LASTEXITCODE -eq 0 -and $ver) {
            $python = $c
            Write-Ok "找到 Python $ver"
            Write-Ok "解释器：$c"
            break
        }
    } catch { }
}

if (-not $python) {
    Write-Err "没找到 Python 3.9+"
    Write-Host ""
    Write-Host "请先安装 Python（勾选 Add to PATH）：https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "如果已经装了，可以指定：`$env:SKILL_PYTHON='C:\Python312\python.exe'; .\install.ps1" -ForegroundColor Yellow
    exit 1
}

# ---------- 2. 版本检查 ----------
Write-Step "检查 Python 版本"
$pyver = & $python -c "import sys; print(sys.version_info.major * 100 + sys.version_info.minor)"
if ([int]$pyver -lt 309) {
    Write-Err "Python 版本太低（需要 3.9+），当前 $pyver"
    exit 1
}
Write-Ok "版本满足要求"

# ---------- 3. 安装依赖 ----------
Write-Step "安装依赖（flask / dulwich / pywebview）"

if ($Check) {
    Write-Warn2 "-Check 模式：跳过实际安装"
} else {
    & $python -m pip install --upgrade pip --quiet
    & $python -m pip install -r (Join-Path $Root "requirements.txt")
    if ($LASTEXITCODE -ne 0) {
        Write-Err "依赖安装失败"
        exit 1
    }
    Write-Ok "依赖安装完成"
}

# ---------- 4. 验证 ----------
Write-Step "验证依赖"
$verifyScript = @'
import importlib.metadata as md
for pkg in ('flask', 'dulwich', 'pywebview'):
    try:
        print(pkg, md.version(pkg))
    except Exception:
        print('MISSING', pkg)
'@
$verify = & $python -c $verifyScript 2>&1
Write-Ok ($verify -join "; ")

# ---------- 5. 可选：加到 PATH ----------
if ($AddToPath) {
    Write-Step "把 skill 命令加到用户 PATH"
    $cliDir = Join-Path $Root "cli"
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -notlike "*$cliDir*") {
        [Environment]::SetEnvironmentVariable("Path", "$userPath;$cliDir", "User")
        Write-Ok "已加入 PATH：$cliDir"
        Write-Warn2 "需要重新打开终端才生效"
    } else {
        Write-Ok "已经在 PATH 里了"
    }
}

# ---------- 6. 完成 ----------
Write-Step "完成"
Write-Host ""
Write-Host "  启动方式：" -ForegroundColor White
Write-Host "    双击 启动.vbs          （推荐，无控制台）" -ForegroundColor Gray
Write-Host "    或 python app.py        （带控制台，方便看日志）" -ForegroundColor Gray
Write-Host ""
Write-Host "  命令行：" -ForegroundColor White
Write-Host "    python cli\skill.py --help" -ForegroundColor Gray
Write-Host ""
Write-Host "  首次启动会让你选工作区目录，然后按提示纳管已有技能。" -ForegroundColor Gray
