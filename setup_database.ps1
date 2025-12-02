# PowerShell Script để Setup PostgreSQL Database cho Odoo
# Chạy script này với quyền Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Odoo Database Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra PostgreSQL đã cài đặt chưa
Write-Host "Đang kiểm tra PostgreSQL..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version
    Write-Host "✓ PostgreSQL đã được cài đặt: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ PostgreSQL chưa được cài đặt hoặc chưa có trong PATH" -ForegroundColor Red
    Write-Host "Vui lòng cài đặt PostgreSQL trước!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Nhập thông tin để tạo database và user:" -ForegroundColor Yellow
Write-Host ""

# Nhập thông tin
$dbName = Read-Host "Tên database (mặc định: odoo_db)"
if ([string]::IsNullOrWhiteSpace($dbName)) {
    $dbName = "odoo_db"
}

$dbUser = Read-Host "Tên user (mặc định: odoo)"
if ([string]::IsNullOrWhiteSpace($dbUser)) {
    $dbUser = "odoo"
}

$dbPassword = Read-Host "Mật khẩu cho user" -AsSecureString
$dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword)
)

$postgresPassword = Read-Host "Mật khẩu PostgreSQL (postgres user)" -AsSecureString
$postgresPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($postgresPassword)
)

Write-Host ""
Write-Host "Đang tạo user và database..." -ForegroundColor Yellow

# Tạo SQL script
$sqlScript = @"
-- Tạo user
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$dbUser') THEN
        CREATE USER $dbUser WITH PASSWORD '$dbPasswordPlain';
    END IF;
END
\$\$;

-- Cấp quyền
ALTER USER $dbUser CREATEDB;

-- Tạo database
SELECT 'CREATE DATABASE $dbName OWNER $dbUser'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$dbName')\gexec
"@

# Lưu SQL script vào file tạm
$tempSqlFile = "$env:TEMP\odoo_setup.sql"
$sqlScript | Out-File -FilePath $tempSqlFile -Encoding UTF8

# Chạy SQL script
$env:PGPASSWORD = $postgresPasswordPlain
try {
    psql -U postgres -f $tempSqlFile
    Write-Host ""
    Write-Host "✓ Database và user đã được tạo thành công!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Thông tin kết nối:" -ForegroundColor Cyan
    Write-Host "  Database: $dbName" -ForegroundColor White
    Write-Host "  User: $dbUser" -ForegroundColor White
    Write-Host "  Password: $dbPasswordPlain" -ForegroundColor White
    Write-Host ""
    Write-Host "Cập nhật thông tin này vào file odoo.conf!" -ForegroundColor Yellow
} catch {
    Write-Host ""
    Write-Host "✗ Có lỗi xảy ra khi tạo database!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Xóa file tạm
Remove-Item $tempSqlFile -ErrorAction SilentlyContinue

# Xóa password khỏi memory
$dbPasswordPlain = $null
$postgresPasswordPlain = $null
$env:PGPASSWORD = $null

Write-Host ""
Write-Host "Hoàn tất!" -ForegroundColor Green

