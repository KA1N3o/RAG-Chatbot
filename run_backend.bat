@echo off
title RAG Chatbot Backend
echo Starting FastAPI Backend...
echo Server will run at http://localhost:8000
echo Press Ctrl+C to stop.
echo.
py -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
pause
