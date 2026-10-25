@echo off
cd /d "%~dp0"
set "PYEXE="

rem 1) prefer the Python bundled with DSH
for /d %%i in ("%USERPROFILE%\.dsh\dsh-runtimes\*") do (
    if exist "%%i\dependencies\python\python.exe" set "PYEXE=%%i\dependencies\python\python.exe"
)

rem 2) fall back to system Python, skipping the Microsoft Store alias
if not defined PYEXE (
    for /f "delims=" %%p in ('where python 2^>nul') do (
        echo %%p | find /i "WindowsApps" >nul
        if errorlevel 1 if not defined PYEXE set "PYEXE=%%p"
    )
)

if not defined PYEXE (
    echo Python 3 was not found.
    echo Install Python 3.10+ with "Add python.exe to PATH", or keep DSH installed.
    pause
    exit /b 1
)

echo Using interpreter: %PYEXE%
"%PYEXE%" app.py
if errorlevel 1 pause
