@echo off
REM GuestVision AI quick start for Windows

echo GuestVision AI Setup
echo ====================

docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker not found. Install Docker Desktop first.
    exit /b 1
)

docker compose version >nul 2>&1
if errorlevel 1 (
    echo Docker Compose plugin not found.
    exit /b 1
)

if not exist "backend\.env" copy backend\.env.example backend\.env
if not exist "frontend\.env" copy frontend\.env.example frontend\.env

docker compose up -d --build

echo.
echo Stack started.
echo Frontend:  http://localhost:5173
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo Postgres:  localhost:5432
echo Redis:     localhost:6379
echo.
echo Logs: docker compose logs -f
echo Stop: docker compose down
