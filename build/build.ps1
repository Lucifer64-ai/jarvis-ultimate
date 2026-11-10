# JARVIS Ultimate - PowerShell Build Script

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  JARVIS Ultimate - Build Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Проверка Python
Write-Host "[1/5] Проверка Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Ошибка: Python не установлен!" -ForegroundColor Red
    exit 1
}

# Создание виртуального окружения
Write-Host "[2/5] Создание виртуального окружения..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1
Write-Host "OK" -ForegroundColor Green

# Установка зависимостей
Write-Host "[3/5] Установка зависимостей..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "OK" -ForegroundColor Green

# Сборка exe
Write-Host "[4/5] Сборка JARVIS.exe..." -ForegroundColor Yellow
Set-Location build
pyinstaller jarvis.spec --clean --noconfirm
if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка сборки!" -ForegroundColor Red
    exit 1
}
Set-Location ..
Write-Host "OK" -ForegroundColor Green

# Копирование конфигурации
Write-Host "[5/5] Копирование файлов..." -ForegroundColor Yellow
if (-not (Test-Path "dist\JARVIS")) {
    New-Item -ItemType Directory -Path "dist\JARVIS" -Force
}
Copy-Item config.json dist\JARVIS\
Copy-Item .env.example dist\JARVIS\.env
if (Test-Path "assets") {
    Copy-Item -Recurse -Force assets dist\JARVIS\assets
}
Write-Host "OK" -ForegroundColor Green

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Сборка завершена успешно!" -ForegroundColor Green
Write-Host "  Файл: dist\JARVIS\JARVIS.exe" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
