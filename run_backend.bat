@echo off
title EduTrack Backend Server
echo Starting EduTrack Server on port 8000...
set "PYTHON_EXE=C:\Users\ruchi\AppData\Local\Python\pythoncore-3.14-64\python.exe"

if exist "%PYTHON_EXE%" (
    "%PYTHON_EXE%" server.py
) else (
    python server.py
)
pause
