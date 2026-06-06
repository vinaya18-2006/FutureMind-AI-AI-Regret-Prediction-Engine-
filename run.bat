@echo off
echo ========================================================
echo          LAUNCHING FUTUREMIND AI SYSTEM
echo ========================================================
echo.
echo [1/2] Starting FastAPI Backend on http://localhost:8000
start cmd /k "cd backend && venv\Scripts\python -m uvicorn main:app --reload --port 8000"

echo [2/2] Starting React Vite Frontend on http://localhost:5173
start cmd /k "cd frontend && npm run dev"

echo.
echo Launching browser checks...
timeout /t 3 /nobreak > nul
start http://localhost:5173
echo.
echo FutureMind AI is now active. Close the opened terminal windows to shut down servers.
echo ========================================================
