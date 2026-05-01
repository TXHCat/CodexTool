@echo off
setlocal

set "SCRIPT_DIR=%~dp0"

if not defined CODEX_HOME (
    set "CODEX_HOME=%USERPROFILE%\.codex"
)

where py >nul 2>nul
if "%ERRORLEVEL%"=="0" (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if not "%ERRORLEVEL%"=="0" (
        echo error: Python was not found. Install Python or add it to PATH.
        pause
        exit /b 1
    )
    set "PYTHON_CMD=python"
)

echo Codex home: "%CODEX_HOME%"
echo.
echo Previewing archived chat cleanup. No changes will be made in this step.
echo.
%PYTHON_CMD% "%SCRIPT_DIR%cleanup_codex_archives.py" --codex-home "%CODEX_HOME%"
if not "%ERRORLEVEL%"=="0" (
    echo.
    echo Preview failed. Cleanup was not applied.
    pause
    exit /b 1
)

echo.
echo Close Codex App before applying cleanup.
choice /c YN /n /m "Permanently delete the archived chats listed above? [Y/N] "
if errorlevel 2 (
    echo.
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo Applying cleanup.
%PYTHON_CMD% "%SCRIPT_DIR%cleanup_codex_archives.py" --codex-home "%CODEX_HOME%" --apply
set "EXIT_CODE=%ERRORLEVEL%"
echo.
if not "%EXIT_CODE%"=="0" (
    echo Cleanup failed.
) else (
    echo Cleanup completed.
)
pause
exit /b %EXIT_CODE%
