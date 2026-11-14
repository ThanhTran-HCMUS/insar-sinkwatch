@echo off
title InSAR-SinkWatch Launcher - NASA Space Apps 2026
color 0B
echo ============================================================
echo   InSAR-SinkWatch: NASA NISAR Urban Subsidence Observatory
echo   Team: VisionSpace_UsxSgu ^| Local Event: Ho Chi Minh City
echo ============================================================
echo.
echo [1/2] Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found on PATH. Please install Python 3.10+.
    pause
    exit /b
)

echo.
echo [2/2] Launching 3D Web GIS Dashboard on http://localhost:8501...
cd /d "%~dp0"
python -m streamlit run app.py --server.headless=false
pause

