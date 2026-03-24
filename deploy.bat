@echo off
cls
echo ╔══════════════════════════════════════════════════════════════════════════╗
echo ║    🛡️ 🇮🇳 CyberShield Indian Fraud Detection System                      ║
echo ║    Network-Safe Deployment for Windows                                  ║
echo ╚══════════════════════════════════════════════════════════════════════════╝

echo [INFO] Starting CyberShield deployment...

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker not found. Please install Docker Desktop.
    pause
    exit /b 1
)

echo [SUCCESS] Docker found

REM Stop existing
docker-compose down >nul 2>&1

echo [INFO] Building system (this may take 2-3 minutes)...
docker-compose up -d --build

echo [INFO] Waiting for services (60 seconds)...
timeout /t 60 /nobreak >nul

echo [INFO] Testing connectivity...

REM Test API with retry
set API_READY=false
for /l %%i in (1,1,6) do (
    echo Testing API attempt %%i...
    curl -s http://localhost:5000/ >nul 2>&1
    if %errorlevel% equ 0 (
        set API_READY=true
        goto :test_dashboard
    )
    timeout /t 10 /nobreak >nul
)

:test_dashboard
set DASHBOARD_READY=false
for /l %%i in (1,1,6) do (
    echo Testing Dashboard attempt %%i...
    curl -s http://localhost:8501/ >nul 2>&1
    if %errorlevel% equ 0 (
        set DASHBOARD_READY=true
        goto :show_results
    )
    timeout /t 10 /nobreak >nul
)

:show_results
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo [INDIA] 🎯 CyberShield System Ready!
echo ════════════════════════════════════════════════════════════════════════════

if "%API_READY%"=="true" (
    echo [SUCCESS] ✅ API Ready: http://localhost:5000
) else (
    echo [WARNING] ⚠️ API may still be starting...
)

if "%DASHBOARD_READY%"=="true" (
    echo [SUCCESS] ✅ Dashboard Ready: http://localhost:8501  
) else (
    echo [WARNING] ⚠️ Dashboard may still be starting...
)

echo.
echo 🌐 Access Your System:
echo   📊 Dashboard: http://localhost:8501
echo   🔗 API: http://localhost:5000
echo.
echo 🧪 Quick Test:
echo   curl http://localhost:5000/api/v1/model_info
echo.
echo 🛠️ Management:
echo   📊 Logs: docker-compose logs cybershield-india
echo   🔄 Restart: docker-compose restart
echo   🛑 Stop: docker-compose down
echo.
if "%API_READY%"=="true" if "%DASHBOARD_READY%"=="true" (
    echo [SUCCESS] 🎉 System fully operational!
    echo [SUCCESS] 🇮🇳 भारतीय धोखाधड़ी तंत्र तैयार है!
    echo [SUCCESS] 🏆 Ready for CyberShield Hackathon 2025!
) else (
    echo [INFO] If services aren't ready, wait 2-3 more minutes
    echo [INFO] Or check: docker-compose logs cybershield-india
)
echo.
pause
