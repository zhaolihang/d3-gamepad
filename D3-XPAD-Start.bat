@echo off
title XPAD
setlocal
cd /d "%~dp0XPAD"
if errorlevel 1 (
    echo Cannot open the D3-XPAD program folder.
    pause
    exit /b 1
)
if not exist "xpad.exe" (
    echo xpad.exe was not found.
    pause
    exit /b 1
)
echo D3-XPAD is running. Close this window to exit.
echo.
"%CD%\xpad.exe"
set "d3ExitCode=%ERRORLEVEL%"
if not "%d3ExitCode%"=="0" (
    echo.
    echo D3-XPAD exited with code %d3ExitCode%.
    pause
)
exit /b %d3ExitCode%
