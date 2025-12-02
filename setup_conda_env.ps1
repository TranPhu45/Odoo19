# PowerShell Script để tạo Conda Environment cho Odoo 19
# Chạy script này để tự động tạo môi trường và cài đặt dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Odoo 19 - Conda Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Conda
Write-Host "Đang kiểm tra Conda..." -ForegroundColor Yellow
try {
    $condaVersion = conda --version
    Write-Host "✓ $condaVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Conda chưa được cài đặt hoặc chưa có trong PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Vui lòng:" -ForegroundColor Yellow
    Write-Host "1. Cài đặt Anaconda hoặc Miniconda" -ForegroundColor White
    Write-Host "2. Khởi động lại PowerShell" -ForegroundColor White
    Write-Host "3. Hoặc chạy: conda init powershell" -ForegroundColor White
    exit 1
}

Write-Host ""

# Kiểm tra môi trường đã tồn tại chưa
$envName = "Odoo19"
Write-Host "Đang kiểm tra môi trường '$envName'..." -ForegroundColor Yellow

$envExists = conda env list | Select-String -Pattern "^$envName\s"
if ($envExists) {
    Write-Host "⚠ Môi trường '$envName' đã tồn tại!" -ForegroundColor Yellow
    $overwrite = Read-Host "Bạn có muốn xóa và tạo lại? (Y/N)"
    if ($overwrite -eq "Y" -or $overwrite -eq "y") {
        Write-Host "Đang xóa môi trường cũ..." -ForegroundColor Cyan
        conda env remove -n $envName -y
        Write-Host "✓ Đã xóa môi trường cũ" -ForegroundColor Green
    } else {
        Write-Host "Sử dụng môi trường hiện có" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Để kích hoạt môi trường, chạy:" -ForegroundColor Cyan
        Write-Host "  conda activate $envName" -ForegroundColor White
        exit 0
    }
}

Write-Host ""
Write-Host "Đang tạo môi trường Conda '$envName' với Python 3.10..." -ForegroundColor Cyan
Write-Host "Quá trình này có thể mất vài phút..." -ForegroundColor Yellow
Write-Host ""

# Tạo môi trường với Python 3.10
conda create -n $envName python=3.10 -y

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Lỗi khi tạo môi trường!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Môi trường '$envName' đã được tạo thành công!" -ForegroundColor Green
Write-Host ""

# Kích hoạt môi trường và cài đặt packages
Write-Host "Đang kích hoạt môi trường và cài đặt packages..." -ForegroundColor Cyan
Write-Host ""

# Kích hoạt môi trường và cài đặt từ requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "Đang cài đặt từ requirements.txt..." -ForegroundColor Yellow
    
    # Sử dụng conda run để chạy pip trong môi trường
    conda run -n $envName pip install --upgrade pip
    conda run -n $envName pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Đã cài đặt packages từ requirements.txt" -ForegroundColor Green
    } else {
        Write-Host "⚠ Có một số lỗi khi cài đặt, nhưng có thể tiếp tục" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Không tìm thấy requirements.txt" -ForegroundColor Yellow
    Write-Host "Đang cài đặt các packages cơ bản..." -ForegroundColor Cyan
    
    # Cài đặt các packages quan trọng nhất
    $essentialPackages = @(
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
        "XlsxWriter"
    )
    
    foreach ($package in $essentialPackages) {
        Write-Host "  Đang cài đặt $package..." -ForegroundColor Cyan
        conda run -n $envName pip install $package
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Setup hoàn tất!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Để sử dụng môi trường, chạy:" -ForegroundColor Yellow
Write-Host "  conda activate $envName" -ForegroundColor White
Write-Host ""
Write-Host "Sau đó chạy Odoo:" -ForegroundColor Yellow
Write-Host "  python odoo19\odoo-bin -c odoo.conf" -ForegroundColor White
Write-Host ""
Write-Host "Hoặc sử dụng script:" -ForegroundColor Yellow
Write-Host "  .\run_odoo_conda.ps1" -ForegroundColor White
Write-Host ""

