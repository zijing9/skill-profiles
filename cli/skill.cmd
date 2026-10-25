@echo off
setlocal EnableExtensions
rem skill CLI wrapper (Windows).
rem Override the interpreter with:  set SKILL_PYTHON=C:\path\to\python.exe
rem Keep this file ASCII-only: cmd.exe parses .cmd as GBK and non-ASCII comments break it.

set "PY=%SKILL_PYTHON%"

if not defined PY if exist "%USERPROFILE%\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" set "PY=%USERPROFILE%\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"

if not defined PY (
  where python.exe >nul 2>nul
  if not errorlevel 1 set "PY=python.exe"
)

if not defined PY (
  echo {"error":{"code":"PYTHON_NOT_FOUND","message":"python not found","suggestion":"set SKILL_PYTHON=C:\\path\\to\\python.exe","recoverable":false}} 1>&2
  exit /b 1
)

"%PY%" "%~dp0skill.py" %*
exit /b %errorlevel%
