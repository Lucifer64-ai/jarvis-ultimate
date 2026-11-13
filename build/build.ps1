# JARVIS Ultimate - PowerShell Build Script

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  JARVIS Ultimate - Build Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ° Python
Write-Host "[1/5] ÃÃÃÂ¾ÃÂ²ÃÂµÃÃÂºÃÂ° Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ°: Python ÃÂ½ÃÂµ ÃÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂ»ÃÂµÃÂ½!" -ForegroundColor Red
    exit 1
}

# ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ²ÃÂ¸ÃÃÃÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¾ÃÂºÃÃÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã
Write-Host "[2/5] ÃÂ¡ÃÂ¾ÃÂ·ÃÂ´ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂ²ÃÂ¸ÃÃÃÃÂ°ÃÂ»ÃÃÂ½ÃÂ¾ÃÂ³ÃÂ¾ ÃÂ¾ÃÂºÃÃÃÂ¶ÃÂµÃÂ½ÃÂ¸Ã..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1
Write-Host "OK" -ForegroundColor Green

# ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ²ÃÂ¸ÃÃÂ¸ÃÂ¼ÃÂ¾ÃÃÃÂµÃÂ¹
Write-Host "[3/5] ÃÂ£ÃÃÃÂ°ÃÂ½ÃÂ¾ÃÂ²ÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ²ÃÂ¸ÃÃÂ¸ÃÂ¼ÃÂ¾ÃÃÃÂµÃÂ¹..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "OK" -ForegroundColor Green

# ÃÂ¡ÃÂ±ÃÂ¾ÃÃÂºÃÂ° exe
Write-Host "[4/5] ÃÂ¡ÃÂ±ÃÂ¾ÃÃÂºÃÂ° JARVIS.exe..." -ForegroundColor Yellow
Set-Location build
pyinstaller jarvis.spec --clean --noconfirm
if ($LASTEXITCODE -ne 0) {
    Write-Host "ÃÃÃÂ¸ÃÂ±ÃÂºÃÂ° ÃÃÂ±ÃÂ¾ÃÃÂºÃÂ¸!" -ForegroundColor Red
    exit 1
}
Set-Location ..
Write-Host "OK" -ForegroundColor Green

# ÃÃÂ¾ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÂºÃÂ¾ÃÂ½ÃÃÂ¸ÃÂ³ÃÃÃÂ°ÃÃÂ¸ÃÂ¸
Write-Host "[5/5] ÃÃÂ¾ÃÂ¿ÃÂ¸ÃÃÂ¾ÃÂ²ÃÂ°ÃÂ½ÃÂ¸ÃÂµ ÃÃÂ°ÃÂ¹ÃÂ»ÃÂ¾ÃÂ²..." -ForegroundColor Yellow
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
Write-Host "  ÃÂ¡ÃÂ±ÃÂ¾ÃÃÂºÃÂ° ÃÂ·ÃÂ°ÃÂ²ÃÂµÃÃÃÂµÃÂ½ÃÂ° ÃÃÃÂ¿ÃÂµÃÃÂ½ÃÂ¾!" -ForegroundColor Green
Write-Host "  ÃÂ¤ÃÂ°ÃÂ¹ÃÂ»: dist\JARVIS\JARVIS.exe" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
