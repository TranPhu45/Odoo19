# PowerShell Script để chạy Odoo với Conda Environment
# Script này tự động kích hoạt môi trường Conda và chạy Odoo

param(
    [string]$ConfigFile = "odoo.conf",
    [string]$Database = "",
    [switch]$Init = $false,
    [switch]$Update = $false,
    [switch]$Test = $false,
    [switch]$Dev = $false
)

$envName = "Odoo19"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Odoo Launcher (Conda)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Conda
try {
    $condaVersion = conda --version
    Write-Host "✓ Conda: $condaVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Conda chưa được cài đặt hoặc chưa có trong PATH" -ForegroundColor Red
    Write-Host "Vui lòng cài đặt Anaconda hoặc Miniconda!" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Kiểm tra môi trường
Write-Host "Đang kiểm tra môi trường '$envName'..." -ForegroundColor Yellow
$envExists = conda env list | Select-String -Pattern "^$envName\s"
if (-not $envExists) {
    Write-Host "✗ Môi trường '$envName' chưa được tạo!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Vui lòng tạo môi trường trước:" -ForegroundColor Yellow
    Write-Host "  .\setup_conda_env.ps1" -ForegroundColor White
    Write-Host "  hoặc" -ForegroundColor White
    Write-Host "  conda env create -f environment.yml" -ForegroundColor White
    exit 1
}

Write-Host "✓ Môi trường '$envName' đã tồn tại" -ForegroundColor Green
Write-Host ""

# Kiểm tra file config
if (-not (Test-Path $ConfigFile)) {
    Write-Host "✗ Không tìm thấy file config: $ConfigFile" -ForegroundColor Red
    Write-Host "Vui lòng tạo file odoo.conf trước!" -ForegroundColor Yellow
    exit 1
}

# Tìm Odoo binary
$odooBin = "odoo19\odoo-bin"
if (-not (Test-Path $odooBin)) {
    $odooBin = "odoo-bin"
    if (-not (Test-Path $odooBin)) {
        Write-Host "✗ Không tìm thấy odoo-bin" -ForegroundColor Red
        Write-Host "Vui lòng đảm bảo bạn đã clone Odoo source code!" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "✓ Tìm thấy Odoo binary: $odooBin" -ForegroundColor Green

# Xây dựng command
$command = "python $odooBin -c $ConfigFile"

if ($Database) {
    $command += " -d $Database"
}

if ($Init) {
    Write-Host ""
    Write-Host "⚠ Chế độ INIT: Odoo sẽ khởi tạo database và dừng lại" -ForegroundColor Yellow
    $command += " --init=base --stop-after-init"
}

if ($Update) {
    if (-not $Database) {
        Write-Host "✗ Cần chỉ định database khi update module" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
    Write-Host "⚠ Chế độ UPDATE: Cập nhật module crm_custom" -ForegroundColor Yellow
    $command += " -u crm_custom"
}

if ($Test) {
    if (-not $Database) {
        Write-Host "✗ Cần chỉ định database khi chạy test" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
    Write-Host "⚠ Chế độ TEST: Chạy tests cho module" -ForegroundColor Yellow
    $command += " --test-enable -u crm_custom --stop-after-init"
}

if ($Dev) {
    Write-Host ""
    Write-Host "⚠ Chế độ DEVELOPMENT: Bật dev mode" -ForegroundColor Yellow
    $command += " --dev=all"
}

Write-Host ""
Write-Host "Command sẽ chạy:" -ForegroundColor Cyan
Write-Host "  $command" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Chạy Odoo với môi trường Conda '$envName'? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Đã hủy." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Đang kích hoạt môi trường '$envName'..." -ForegroundColor Cyan
Write-Host "Đang khởi động Odoo..." -ForegroundColor Green
Write-Host "Truy cập http://localhost:8069 sau khi Odoo khởi động" -ForegroundColor Cyan
Write-Host "Nhấn Ctrl+C để dừng server" -ForegroundColor Yellow
Write-Host ""

# Chạy Odoo với conda run
conda run -n $envName $command

