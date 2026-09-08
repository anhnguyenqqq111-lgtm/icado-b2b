@echo off
title Rank Dashboard
echo Starting Rank Dashboard...
echo.
cd /d "%~dp0..\..\tools\rank-checker"
"C:\Program Files\nodejs\node.exe" server.js
pause
