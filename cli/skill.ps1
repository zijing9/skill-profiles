# skill CLI 的 PowerShell 包装器
# 用法：.\skill.ps1 <command> [args]
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
& python "$here\skill.py" @args
exit $LASTEXITCODE
