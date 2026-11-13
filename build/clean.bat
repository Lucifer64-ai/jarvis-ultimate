@echo off
echo ==========================================
echo   JARVIS Ultimate - Clean Build
echo ==========================================
echo.

echo Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ build Ð°ÑÑÐµÑÐ°ÐºÑÐ¾Ð²...
if exist "build\dist" rmdir /S /Q build\dist
if exist "build\build" rmdir /S /Q build\build
if exist "dist" rmdir /S /Q dist
if exist "*.spec" del /Q *.spec

echo Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ ÐºÑÑÐ° Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d"
for /d /r . %%d in (*.egg-info) do @if exist "%%d" rmdir /S /Q "%%d"

echo Ð£Ð´Ð°Ð»ÐµÐ½Ð¸Ðµ Ð²ÑÐµÐ¼ÐµÐ½Ð½ÑÑ ÑÐ°Ð¹Ð»Ð¾Ð²...
del /Q *.pyc 2>nul
del /Q *.pyo 2>nul

echo.
echo ÐÑÐ¸ÑÑÐºÐ° Ð·Ð°Ð²ÐµÑÑÐµÐ½Ð°!
pause
