# JARVIS Ultimate - PowerShell Build Script

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  JARVIS Ultimate - Build Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# ÐÑÐ¾Ð²ÐµÑÐºÐ° Python
Write-Host "[1/5] ÐÑÐ¾Ð²ÐµÑÐºÐ° Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ÐÑÐ¸Ð±ÐºÐ°: Python Ð½Ðµ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½!" -ForegroundColor Red
    exit 1
}

# Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð²Ð¸ÑÑÑÐ°Ð»ÑÐ½Ð¾Ð³Ð¾ Ð¾ÐºÑÑÐ¶ÐµÐ½Ð¸Ñ
Write-Host "[2/5] Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð²Ð¸ÑÑÑÐ°Ð»ÑÐ½Ð¾Ð³Ð¾ Ð¾ÐºÑÑÐ¶ÐµÐ½Ð¸Ñ..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1
Write-Host "OK" -ForegroundColor Green

# Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð·Ð°Ð²Ð¸ÑÐ¸Ð¼Ð¾ÑÑÐµÐ¹
Write-Host "[3/5] Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð·Ð°Ð²Ð¸ÑÐ¸Ð¼Ð¾ÑÑÐµÐ¹..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "OK" -ForegroundColor Green

# Ð¡Ð±Ð¾ÑÐºÐ° exe
Write-Host "[4/5] Ð¡Ð±Ð¾ÑÐºÐ° JARVIS.exe..." -ForegroundColor Yellow
Set-Location build
pyinstaller jarvis.spec --clean --noconfirm
if ($LASTEXITCODE -ne 0) {
    Write-Host "ÐÑÐ¸Ð±ÐºÐ° ÑÐ±Ð¾ÑÐºÐ¸!" -ForegroundColor Red
    exit 1
}
Set-Location ..
Write-Host "OK" -ForegroundColor Green

# ÐÐ¾Ð¿Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð½ÑÐ¸Ð³ÑÑÐ°ÑÐ¸Ð¸
Write-Host "[5/5] ÐÐ¾Ð¿Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÑÐ°Ð¹Ð»Ð¾Ð²..." -ForegroundColor Yellow
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
Write-Host "  Ð¡Ð±Ð¾ÑÐºÐ° Ð·Ð°Ð²ÐµÑÑÐµÐ½Ð° ÑÑÐ¿ÐµÑÐ½Ð¾!" -ForegroundColor Green
Write-Host "  Ð¤Ð°Ð¹Ð»: dist\JARVIS\JARVIS.exe" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
