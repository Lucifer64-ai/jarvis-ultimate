@echo off
chcp 65001 >nul
echo ==========================================
echo   JARVIS Ultimate - Build Script
echo ==========================================
echo.

REM ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ° Python
echo [1/5] ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ° Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ°: Python ÃÂ½ÃÂµ ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½!
    pause
    exit /b 1
)
echo OK

REM ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ²ÃÂ¸ÃÃÃÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¾ÃÂºÃÃÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã
echo [2/5] ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ²ÃÂ¸ÃÃÃÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¾ÃÂºÃÃÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
echo OK

REM ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ²ÃÂ¸ÃÃÂ¸ÃÂ¼ÃÂ¾ÃÃÃÂµÃÂ¹
echo [3/5] ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ²ÃÂ¸ÃÃÂ¸ÃÂ¼ÃÂ¾ÃÃÃÂµÃÂ¹...
pip install -r requirements.txt
echo OK

REM ÃÂ¡ÃÂ±ÃÂ¾ÃÃÂºÃÂ° exe
echo [4/5] ÃÂ¡ÃÂ±ÃÂ¾ÃÃÂºÃÂ° JARVIS.exe...
cd build
pyinstaller jarvis.spec --clean --noconfirm
if errorlevel 1 (
    echo ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÂ±ÃÂ¾ÃÃÂºÃÂ¸!
    pause
    exit /b 1
)
cd ..
echo OK

REM ÃÃÂ¾ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂºÃÂ¾ÃÂ½ÃÃÂ¸ÃÂ³ÃÃÃÂ°ÃÃÂ¸ÃÂ¸
echo [5/5] ÃÃÂ¾ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ²...
if not exist "dist\JARVIS" mkdir dist\JARVIS
copy config.json dist\JARVIS\
copy .env.example dist\JARVIS\.env
if exist "assets" (
    xcopy /E /I /Y assets dist\JARVIS\assets
)
echo OK

echo.
echo ==========================================
echo   ÃÂ¡ÃÂ±ÃÂ¾ÃÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ²ÃÂµÃÃÃÂµÃÂ½ÃÂ° ÃÃÃÂ¿ÃÂµÃÃÂ½ÃÂ¾!
echo   ÃÂ¤ÃÂ°ÃÂ¹ÃÂ»: dist\JARVIS\JARVIS.exe
echo ==========================================
pause
