@echo off
chcp 65001 >nul
echo ==========================================
echo   JARVIS Ultimate - Build Script
echo ==========================================
echo.

REM Проверка Python
echo [1/5] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не установлен!
    pause
    exit /b 1
)
echo OK

REM Создание виртуального окружения
echo [2/5] Создание виртуального окружения...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
echo OK

REM Установка зависимостей
echo [3/5] Установка зависимостей...
pip install -r requirements.txt
echo OK

REM Сборка exe
echo [4/5] Сборка JARVIS.exe...
cd build
pyinstaller jarvis.spec --clean --noconfirm
if errorlevel 1 (
    echo Ошибка сборки!
    pause
    exit /b 1
)
cd ..
echo OK

REM Копирование конфигурации
echo [5/5] Копирование файлов...
if not exist "dist\JARVIS" mkdir dist\JARVIS
copy config.json dist\JARVIS\
copy .env.example dist\JARVIS\.env
if exist "assets" (
    xcopy /E /I /Y assets dist\JARVIS\assets
)
echo OK

echo.
echo ==========================================
echo   Сборка завершена успешно!
echo   Файл: dist\JARVIS\JARVIS.exe
echo ==========================================
pause
