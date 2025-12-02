# PowerShell Script để cài đặt Python Dependencies cho Odoo

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Odoo Python Dependencies Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Python
Write-Host "Đang kiểm tra Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python chưa được cài đặt hoặc chưa có trong PATH" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Đang kiểm tra pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version
    Write-Host "✓ $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip chưa được cài đặt" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Các package sẽ được cài đặt:" -ForegroundColor Yellow
$packages = @(
    "psycopg2-binary",
    "lxml",
    "pillow",
    "python-dateutil",
    "pytz",
    "Babel",
    "Werkzeug",
    "reportlab",
    "decorator",
    "requests",
    "XlsxWriter",
    "zeep",
    "num2words",
    "python-stdnum",
    "pyserial",
    "qrcode",
    "vobject",
    "pyldap",
    "gevent",
    "greenlet"
)

Write-Host ""
foreach ($package in $packages) {
    Write-Host "  - $package" -ForegroundColor White
}

Write-Host ""
$confirm = Read-Host "Tiếp tục cài đặt? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Đã hủy." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Đang cài đặt packages..." -ForegroundColor Yellow
Write-Host ""

$failedPackages = @()

foreach ($package in $packages) {
    Write-Host "Đang cài đặt $package..." -ForegroundColor Cyan
    try {
        pip install $package --quiet
        Write-Host "✓ $package đã được cài đặt" -ForegroundColor Green
    } catch {
        Write-Host "✗ Lỗi khi cài đặt $package" -ForegroundColor Red
        $failedPackages += $package
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($failedPackages.Count -eq 0) {
    Write-Host "✓ Tất cả packages đã được cài đặt thành công!" -ForegroundColor Green
} else {
    Write-Host "⚠ Một số packages không thể cài đặt:" -ForegroundColor Yellow
    foreach ($package in $failedPackages) {
        Write-Host "  - $package" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Thử cài đặt thủ công các package này." -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan

