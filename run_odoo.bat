@echo off
REM Batch file để chạy Odoo trên Windows
REM Sử dụng file này nếu không muốn dùng PowerShell

echo ========================================
echo Odoo Launcher
echo ========================================
echo.

REM Kiểm tra file config
if not exist "odoo.conf" (
    echo [ERROR] Khong tim thay file odoo.conf
    echo Vui long tao file odoo.conf truoc!
    pause
    exit /b 1
)

REM Tìm Odoo binary
set ODOO_BIN=odoo19\odoo-bin
if not exist "%ODOO_BIN%" (
    set ODOO_BIN=odoo-bin
    if not exist "%ODOO_BIN%" (
        echo [ERROR] Khong tim thay odoo-bin
        echo Vui long dam bao ban da clone Odoo source code!
        pause
        exit /b 1
    )
)

echo [OK] Tim thay Odoo binary: %ODOO_BIN%
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat hoac chua co trong PATH
    pause
    exit /b 1
)

echo [OK] Python da duoc cai dat
echo.

REM Xây dựng command
set COMMAND=python %ODOO_BIN% -c odoo.conf

REM Kiểm tra tham số
if "%1"=="-d" (
    set COMMAND=%COMMAND% -d %2
    shift
    shift
)

if "%1"=="--init" (
    set COMMAND=%COMMAND% --init=base --stop-after-init
)

if "%1"=="-u" (
    set COMMAND=%COMMAND% -u %2
)

if "%1"=="--dev" (
    set COMMAND=%COMMAND% --dev=all
)

echo Command se chay:
echo   %COMMAND%
echo.
echo Dang khoi dong Odoo...
echo Truy cap http://localhost:8069 sau khi Odoo khoi dong
echo Nhan Ctrl+C de dung server
echo.

REM Chạy Odoo
%COMMAND%

pause

