@echo off
title Quotes Explorer - Data Science Practicum
echo ========================================================
echo   Starting Quotes Data Science Explorer Web Server...
echo ========================================================
echo.
echo Launching website in your browser...
start "" "http://127.0.0.1:5000"
python app.py
pause
