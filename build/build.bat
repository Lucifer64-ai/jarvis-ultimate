@echo off
chcp 65001 >nul
echo ==========================================
echo   JARVIS Ultimate - Build Script
echo ==========================================
echo.

REM ÐÑÐ¾Ð²ÐµÑÐºÐ° Python
echo [1/5] ÐÑÐ¾Ð²ÐµÑÐºÐ° Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ÐÑÐ¸Ð±ÐºÐ°: Python Ð½Ðµ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½!
    pause
    exit /b 1
)
echo OK

REM Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð²Ð¸ÑÑÑÐ°Ð»ÑÐ½Ð¾Ð³Ð¾ Ð¾ÐºÑÑÐ¶ÐµÐ½Ð¸Ñ
echo [2/5] Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð²Ð¸ÑÑÑÐ°Ð»ÑÐ½Ð¾Ð³Ð¾ Ð¾ÐºÑÑÐ¶ÐµÐ½Ð¸Ñ...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
echo OK

REM Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð·Ð°Ð²Ð¸ÑÐ¸Ð¼Ð¾ÑÑÐµÐ¹
echo [3/5] Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð·Ð°Ð²Ð¸ÑÐ¸Ð¼Ð¾ÑÑÐµÐ¹...
pip install -r requirements.txt
echo OK

REM Ð¡Ð±Ð¾ÑÐºÐ° exe
echo [4/5] Ð¡Ð±Ð¾ÑÐºÐ° JARVIS.exe...
cd build
pyinstaller jarvis.spec --clean --noconfirm
if errorlevel 1 (
    echo ÐÑÐ¸Ð±ÐºÐ° ÑÐ±Ð¾ÑÐºÐ¸!
    pause
    exit /b 1
)
cd ..
echo OK

REM ÐÐ¾Ð¿Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð½ÑÐ¸Ð³ÑÑÐ°ÑÐ¸Ð¸
echo [5/5] ÐÐ¾Ð¿Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÑÐ°Ð¹Ð»Ð¾Ð²...
if not exist "dist\JARVIS" mkdir dist\JARVIS
copy config.json dist\JARVIS\
copy .env.example dist\JARVIS\.env
if exist "assets" (
    xcopy /E /I /Y assets dist\JARVIS\assets
)
echo OK

echo.
echo ==========================================
echo   Ð¡Ð±Ð¾ÑÐºÐ° Ð·Ð°Ð²ÐµÑÑÐµÐ½Ð° ÑÑÐ¿ÐµÑÐ½Ð¾!
echo   Ð¤Ð°Ð¹Ð»: dist\JARVIS\JARVIS.exe
echo ==========================================
pause
