# PowerShell Script để kiểm tra Git trước khi commit
# Script này giúp đảm bảo không commit file nhạy cảm

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Git Pre-Commit Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$hasErrors = $false
$warnings = @()

# Kiểm tra Git đã được khởi tạo
if (-not (Test-Path ".git")) {
    Write-Host "⚠ Git repository chưa được khởi tạo" -ForegroundColor Yellow
    Write-Host "Chạy: git init" -ForegroundColor White
    Write-Host ""
}

# Kiểm tra file nhạy cảm trong staging
Write-Host "Đang kiểm tra file nhạy cảm..." -ForegroundColor Yellow
Write-Host ""

$sensitiveFiles = @(
    "odoo.conf",
    "*.key",
    "*.pem",
    ".env",
    "*.log"
)

$stagedFiles = git diff --cached --name-only 2>$null

if ($stagedFiles) {
    foreach ($file in $stagedFiles) {
        foreach ($pattern in $sensitiveFiles) {
            if ($file -like $pattern) {
                Write-Host "✗ CẢNH BÁO: File nhạy cảm trong staging: $file" -ForegroundColor Red
                $hasErrors = $true
            }
        }
        
        # Kiểm tra file chứa mật khẩu
        if (Test-Path $file) {
            $content = Get-Content $file -Raw -ErrorAction SilentlyContinue
            if ($content -match "(?i)(password|secret|api_key|token)\s*=\s*['\`"]?[^'\`"\s]+['\`"]?") {
                Write-Host "⚠ CẢNH BÁO: File có thể chứa mật khẩu: $file" -ForegroundColor Yellow
                $warnings += $file
            }
        }
    }
}

# Kiểm tra file odoo.conf
if (Test-Path "odoo.conf") {
    $inGit = git ls-files --error-unmatch odoo.conf 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✗ LỖI: odoo.conf đang được track bởi Git!" -ForegroundColor Red
        Write-Host "  Chạy: git rm --cached odoo.conf" -ForegroundColor White
        $hasErrors = $true
    }
}

# Kiểm tra .gitignore
if (-not (Test-Path ".gitignore")) {
    Write-Host "⚠ Không tìm thấy file .gitignore" -ForegroundColor Yellow
    Write-Host "  Nên tạo file .gitignore để bảo vệ file nhạy cảm" -ForegroundColor White
    $warnings += ".gitignore missing"
}

# Hiển thị file sẽ được commit
Write-Host ""
Write-Host "Các file sẽ được commit:" -ForegroundColor Cyan
$stagedFiles = git diff --cached --name-only 2>$null
if ($stagedFiles) {
    foreach ($file in $stagedFiles) {
        Write-Host "  + $file" -ForegroundColor Green
    }
} else {
    Write-Host "  (Không có file nào trong staging)" -ForegroundColor Yellow
}

# Hiển thị file bị ignore
Write-Host ""
Write-Host "Các file bị ignore (sẽ KHÔNG được commit):" -ForegroundColor Cyan
$ignoredFiles = git status --ignored --porcelain 2>$null | Where-Object { $_ -match "^!!" }
if ($ignoredFiles) {
    foreach ($line in $ignoredFiles) {
        $file = $line -replace "^!!\s+", ""
        Write-Host "  - $file" -ForegroundColor Gray
    }
} else {
    Write-Host "  (Không có file nào bị ignore)" -ForegroundColor Gray
}

# Tóm tắt
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($hasErrors) {
    Write-Host "✗ CÓ LỖI: Vui lòng sửa trước khi commit!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Các bước khắc phục:" -ForegroundColor Yellow
    Write-Host "1. Xóa file nhạy cảm khỏi staging: git reset HEAD <file>" -ForegroundColor White
    Write-Host "2. Xóa file khỏi Git: git rm --cached <file>" -ForegroundColor White
    Write-Host "3. Đảm bảo file có trong .gitignore" -ForegroundColor White
    exit 1
} elseif ($warnings.Count -gt 0) {
    Write-Host "⚠ CÓ CẢNH BÁO: Kiểm tra lại trước khi commit" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "✓ An toàn để commit!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Để commit, chạy:" -ForegroundColor Cyan
    Write-Host "  git commit -m 'Your commit message'" -ForegroundColor White
    exit 0
}

