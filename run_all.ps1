# Script tự động chạy tất cả các bước cài đặt
# Chạy script này để tự động hóa toàn bộ quá trình

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Odoo CRM Custom - Auto Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Bước 1: Kiểm tra phần mềm
Write-Host "[BƯỚC 1] Kiểm tra phần mềm cần thiết..." -ForegroundColor Yellow
Write-Host ""

$errors = @()

# Kiểm tra Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python chưa được cài đặt" -ForegroundColor Red
    $errors += "Python"
}

# Kiểm tra pip
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip chưa được cài đặt" -ForegroundColor Red
    $errors += "pip"
}

# Kiểm tra PostgreSQL
try {
    $pgVersion = psql --version 2>&1
    Write-Host "✓ PostgreSQL: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ PostgreSQL chưa được cài đặt hoặc chưa có trong PATH" -ForegroundColor Red
    $errors += "PostgreSQL"
}

# Kiểm tra Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "✓ Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git chưa được cài đặt" -ForegroundColor Red
    $errors += "Git"
}

if ($errors.Count -gt 0) {
    Write-Host ""
    Write-Host "✗ Thiếu các phần mềm sau:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Vui lòng cài đặt các phần mềm thiếu trước khi tiếp tục!" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "✓ Tất cả phần mềm cần thiết đã được cài đặt" -ForegroundColor Green
Write-Host ""

# Bước 2: Kiểm tra Odoo source code
Write-Host "[BƯỚC 2] Kiểm tra Odoo source code..." -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path "odoo19")) {
    Write-Host "⚠ Không tìm thấy thư mục odoo19" -ForegroundColor Yellow
    $clone = Read-Host "Bạn có muốn clone Odoo 19? (Y/N)"
    if ($clone -eq "Y" -or $clone -eq "y") {
        Write-Host "Đang clone Odoo 19..." -ForegroundColor Cyan
        git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1 odoo19
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Đã clone Odoo 19 thành công" -ForegroundColor Green
        } else {
            Write-Host "✗ Lỗi khi clone Odoo" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Vui lòng clone Odoo 19 thủ công trước khi tiếp tục" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "✓ Đã tìm thấy thư mục odoo19" -ForegroundColor Green
}

Write-Host ""

# Bước 3: Cài đặt Python dependencies
Write-Host "[BƯỚC 3] Cài đặt Python dependencies..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path "requirements.txt") {
    $install = Read-Host "Cài đặt dependencies từ requirements.txt? (Y/N)"
    if ($install -eq "Y" -or $install -eq "y") {
        Write-Host "Đang cài đặt..." -ForegroundColor Cyan
        pip install -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Đã cài đặt dependencies thành công" -ForegroundColor Green
        } else {
            Write-Host "⚠ Có một số lỗi khi cài đặt, nhưng có thể tiếp tục" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "⚠ Không tìm thấy requirements.txt" -ForegroundColor Yellow
}

Write-Host ""

# Bước 4: Kiểm tra database
Write-Host "[BƯỚC 4] Kiểm tra database..." -ForegroundColor Yellow
Write-Host ""

$setupDb = Read-Host "Bạn có muốn setup database? (Y/N)"
if ($setupDb -eq "Y" -or $setupDb -eq "y") {
    if (Test-Path "setup_database.ps1") {
        Write-Host "Đang chạy script setup database..." -ForegroundColor Cyan
        .\setup_database.ps1
    } else {
        Write-Host "⚠ Không tìm thấy setup_database.ps1" -ForegroundColor Yellow
        Write-Host "Vui lòng tạo database thủ công" -ForegroundColor Yellow
    }
} else {
    Write-Host "Bỏ qua setup database" -ForegroundColor Yellow
}

Write-Host ""

# Bước 5: Kiểm tra file config
Write-Host "[BƯỚC 5] Kiểm tra file cấu hình..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path "odoo.conf") {
    Write-Host "✓ Đã tìm thấy odoo.conf" -ForegroundColor Green
    Write-Host "⚠ Vui lòng kiểm tra và cập nhật thông tin trong file này!" -ForegroundColor Yellow
} else {
    Write-Host "✗ Không tìm thấy odoo.conf" -ForegroundColor Red
    Write-Host "Vui lòng tạo file odoo.conf trước khi chạy Odoo" -ForegroundColor Yellow
}

Write-Host ""

# Bước 6: Hỏi có muốn chạy Odoo không
Write-Host "[BƯỚC 6] Sẵn sàng chạy Odoo!" -ForegroundColor Green
Write-Host ""

$runOdoo = Read-Host "Bạn có muốn chạy Odoo ngay bây giờ? (Y/N)"
if ($runOdoo -eq "Y" -or $runOdoo -eq "y") {
    Write-Host ""
    Write-Host "Đang khởi động Odoo..." -ForegroundColor Cyan
    Write-Host "Truy cập http://localhost:8069 sau khi Odoo khởi động" -ForegroundColor Green
    Write-Host ""
    
    if (Test-Path "run_odoo.ps1") {
        .\run_odoo.ps1
    } else {
        if (Test-Path "odoo19\odoo-bin") {
            python odoo19\odoo-bin -c odoo.conf
        } else {
            Write-Host "✗ Không tìm thấy odoo-bin" -ForegroundColor Red
        }
    }
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Setup hoàn tất!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Để chạy Odoo, sử dụng lệnh:" -ForegroundColor Yellow
    Write-Host "  .\run_odoo.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Hoặc:" -ForegroundColor Yellow
    Write-Host "  python odoo19\odoo-bin -c odoo.conf" -ForegroundColor White
    Write-Host ""
}

