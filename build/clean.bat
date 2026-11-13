@echo off
echo ==========================================
echo   JARVIS Ultimate - Clean Build
echo ==========================================
echo.

echo ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ build ÃÂ°ÃÃÃÂµÃÃÂ°ÃÂºÃÃÂ¾ÃÂ²...
if exist "build\dist" rmdir /S /Q build\dist
if exist "build\build" rmdir /S /Q build\build
if exist "dist" rmdir /S /Q dist
if exist "*.spec" del /Q *.spec

echo ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂºÃÃÃÂ° Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d"
for /d /r . %%d in (*.egg-info) do @if exist "%%d" rmdir /S /Q "%%d"

echo ÃÂ£ÃÂ´ÃÂ°ÃÂ»ÃÂµÃÂ½ÃÂ¸ÃÂµ ÃÂ²ÃÃÂµÃÂ¼ÃÂµÃÂ½ÃÂ½ÃÃ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ²...
del /Q *.pyc 2>nul
del /Q *.pyo 2>nul

echo.
echo ÃÃÃÂ¸ÃÃÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ²ÃÂµÃÃÃÂµÃÂ½ÃÂ°!
pause
