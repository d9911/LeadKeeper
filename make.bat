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
if "%1"=="dev" goto dev
if "%1"=="backend" goto backend
if "%1"=="frontend" goto frontend
if "%1"=="clean" goto clean

:help
echo %BLUE%LeadKeeper%NC% - Lead Capture Module
echo.
echo Available commands:
echo   make.bat install    Install dependencies
echo   make.bat dev        Run frontend and backend
echo   make.bat backend    Run only backend
echo   make.bat frontend   Run only frontend
echo   make.bat clean      Clean temp files
goto :end

:install
echo %BLUE%==^>%NC% Installing backend dependencies...
pip install -r backend\requirements.txt
echo.
echo %BLUE%==^>%NC% Installing frontend dependencies...
cd frontend
call npm install
cd ..
goto :end

:dev
echo %BLUE%==^>%NC% Starting backend and frontend...
echo %YELLOW%Backend:%NC% http://localhost:8000
echo %YELLOW%Frontend:%NC% http://localhost:5173
echo.
start /B cmd /c "cd frontend ^&^& npm run dev"
start /B cmd /c "cd backend ^&^& uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
goto :end

:backend
echo %BLUE%==^>%NC% Starting backend on http://localhost:8000
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
goto :end

:frontend
echo %BLUE%==^>%NC% Starting frontend on http://localhost:5173
cd frontend
npm run dev
goto :end

:clean
echo %BLUE%==^>%NC% Cleaning...
if exist frontend\node_modules rmdir /s /q frontend\node_modules
if exist frontend\dist rmdir /s /q frontend\dist
if exist frontend\.vite rmdir /s /q frontend\.vite
if exist backend\leadkeeper.db del /q backend\leadkeeper.db
echo %GREEN%Done!%NC%

:end
endlocal