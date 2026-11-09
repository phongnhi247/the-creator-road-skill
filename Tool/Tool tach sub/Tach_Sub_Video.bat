@echo off
chcp 65001 >nul
set "VENV_PY=D:\Project\VIDEO\herk-edit-kit\.venv\Scripts\python.exe"
if not exist "%VENV_PY%" (
    echo Khong tim thay Python venv tai %VENV_PY%
    pause
    exit /b 1
)
"%VENV_PY%" "%~dp0tach_sub.py" %*
echo.
pause
