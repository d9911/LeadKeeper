@echo off
REM LeadKeeper Makefile for Windows
REM Usage: make.bat <target>

setlocal enabledelayedexpansion

set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-backend" goto install-backend
if "%1"=="install-frontend" goto install-frontend
if "%1"=="dev" goto dev
if "%1"=="backend" goto backend
if "%1"=="frontend" goto frontend
if "%1"=="build" goto build
if "%1"=="build-frontend" goto build-frontend
if "%1"=="build-backend" goto build-backend
if "%1"=="preview" goto preview
if "%1"=="preview-full" goto preview-full
if "%1"=="clean" goto clean
if "%1"=="clean-all" goto clean-all
if "%1"=="clean-ports" goto clean-ports

goto help

:help
echo %BLUE%LeadKeeper%NC% - Lead Capture Module
echo.
echo Available commands:
echo   make.bat install          Install all dependencies
echo   make.bat install-backend  Install backend dependencies
echo   make.bat install-frontend Install frontend dependencies
echo   make.bat dev              Run frontend + backend (dev mode)
echo   make.bat backend          Run only backend
echo   make.bat frontend         Run only frontend
echo   make.bat build            Build project (SSG)
echo   make.bat build-frontend   Build frontend only
echo   make.bat build-backend    Build backend only
echo   make.bat preview          Preview built frontend
echo   make.bat preview-full     Preview + backend
echo   make.bat clean            Clean cache
echo   make.bat clean-all        Clean all (deps + cache)
echo   make.bat clean-ports      Kill processes on ports
goto :end

:install
call :install-backend
call :install-frontend
echo %GREEN%✅ All dependencies installed!%NC%
goto :end

:install-backend
echo %BLUE%🐍 Backend setup%NC%
echo %YELLOW%==^> Creating venv...%NC%
cd backend
python -m venv .venv
echo %YELLOW%==^> Installing dependencies...%NC%
.venv\Scripts\pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
cd ..
echo %GREEN%✅ Backend installed!%NC%
goto :end

:install-frontend
echo %BLUE%⚛️  Frontend setup%NC%
cd frontend
call npm install
cd ..
echo %GREEN%✅ Frontend installed!%NC%
goto :end

:clean-ports
echo %YELLOW%🧹 Cleaning ports...%NC%
for %%p in (8000 5173 4173) do (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%%p') do (
        taskkill /F /PID %%a >nul 2^>^&1
    )
)
echo %GREEN%✅ Ports cleaned!%NC%
goto :end

:dev
call :clean-ports
echo %BLUE%🚀 LeadKeeper (dev mode)%NC%
echo %YELLOW%Frontend:%NC% http://localhost:5173
echo %YELLOW%Backend:%NC%  http://localhost:8000
echo.
start cmd /c "cd frontend ^&^& npm run dev"
start cmd /c "cd backend ^&^& .venv\Scripts\uvicorn app.main:app --reload --port 8000"
goto :end

:backend
call :clean-ports
echo %BLUE%🚀 Backend%NC%
cd backend
.venv\Scripts\uvicorn app.main:app --reload --port 8000
goto :end

:frontend
call :clean-ports
echo %BLUE%🚀 Frontend%NC%
cd frontend
npm run dev
goto :end

:build
call :build-frontend
call :build-backend
echo %GREEN%✅ Build complete!%NC%
echo Static files: frontend\dist
goto :end

:build-frontend
echo %BLUE%📦 Building frontend (SSG)%NC%
cd frontend
call npm run build
cd ..
echo %GREEN%✅ Frontend built!%NC%
goto :end

:build-backend
echo %BLUE%📦 Backend check%NC%
cd backend
.venv\Scripts\python -c "from app.main import app; print('✅ Backend OK')"
cd ..
echo %GREEN%✅ Backend checked!%NC%
goto :end

:preview
call :clean-ports
echo %BLUE%👁️  Preview%NC%
cd frontend
npm run preview
goto :end

:preview-full
call :clean-ports
call :build
echo %BLUE%🚀 Full Preview Mode%NC%
start cmd /c "cd frontend ^&^& npm run preview"
start cmd /c "cd backend ^&^& .venv\Scripts\uvicorn app.main:app --port 8000"
goto :end

:clean
echo %YELLOW%🧹 Cleaning cache...%NC%
if exist backend\__pycache__ rmdir /s /q backend\__pycache__
if exist frontend\.vite rmdir /s /q frontend\.vite
if exist frontend\dist rmdir /s /q frontend\dist
if exist backend\leadkeeper.db del /q backend\leadkeeper.db
echo %GREEN%✅ Cache cleaned!%NC%
goto :end

:clean-all
call :clean-ports
call :clean
echo %YELLOW%🧹 Cleaning all...%NC%
if exist backend\.venv rmdir /s /q backend\.venv
if exist frontend\node_modules rmdir /s /q frontend\node_modules
if exist frontend\dist rmdir /s /q frontend\dist
if exist frontend\.vite rmdir /s /q frontend\.vite
echo %GREEN%✅ All cleaned!%NC%
goto :end

:end
endlocal