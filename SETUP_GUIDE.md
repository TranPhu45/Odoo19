# Hướng dẫn Cài đặt và Cấu hình Odoo 19 CRM Project

## 📋 Yêu cầu Hệ thống

### Phần mềm Cần thiết
- **Python**: 3.10 hoặc cao hơn
- **PostgreSQL**: 12 hoặc cao hơn
- **Git**: Để clone Odoo source code
- **Node.js**: 14.x hoặc 16.x (cho assets compilation)
- **wkhtmltopdf**: Để xuất PDF (tùy chọn)

### Hệ điều hành
- Windows 10/11
- Linux (Ubuntu 20.04+)
- macOS

---

## 🚀 Cài đặt trên Windows

### Bước 1: Cài đặt Python

1. Tải Python 3.10+ từ [python.org](https://www.python.org/downloads/)
2. Cài đặt và **quan trọng**: Tick vào "Add Python to PATH"
3. Kiểm tra cài đặt:
```powershell
python --version
pip --version
```

### Bước 2: Cài đặt PostgreSQL

1. Tải PostgreSQL từ [postgresql.org](https://www.postgresql.org/download/windows/)
2. Cài đặt với các thiết lập mặc định
3. Ghi nhớ mật khẩu cho user `postgres`
4. Kiểm tra cài đặt:
```powershell
psql --version
```

### Bước 3: Cài đặt Git

1. Tải Git từ [git-scm.com](https://git-scm.com/download/win)
2. Cài đặt với các thiết lập mặc định
3. Kiểm tra:
```powershell
git --version
```

### Bước 4: Cài đặt Node.js (Tùy chọn nhưng khuyến nghị)

1. Tải Node.js LTS từ [nodejs.org](https://nodejs.org/)
2. Cài đặt
3. Kiểm tra:
```powershell
node --version
npm --version
```

---

## 📦 Cài đặt Odoo 19

### Cách 1: Clone từ GitHub (Khuyến nghị)

```powershell
# Tạo thư mục cho dự án
cd C:\Users\Admin\PycharmProjects\Peter's Project
mkdir Odoo
cd Odoo

# Clone Odoo source code
git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1 odoo19

# Di chuyển module vào addons path
# Module crm_custom đã có sẵn trong thư mục này
```

### Cách 2: Tải Odoo từ website

1. Tải Odoo 19 từ [odoo.com](https://www.odoo.com/page/download)
2. Giải nén vào thư mục `odoo19`

---

## 🗄️ Cấu hình PostgreSQL

### Tạo Database và User

1. Mở **pgAdmin** hoặc **psql** command line

2. Tạo user cho Odoo:
```sql
-- Kết nối PostgreSQL với user postgres
CREATE USER odoo WITH PASSWORD 'odoo_password';
ALTER USER odoo CREATEDB;
```

3. Tạo database (sẽ được tạo tự động khi chạy Odoo lần đầu, hoặc tạo thủ công):
```sql
CREATE DATABASE odoo_db OWNER odoo;
```

### Hoặc sử dụng psql command line:

```powershell
# Kết nối PostgreSQL
psql -U postgres

# Trong psql, chạy:
CREATE USER odoo WITH PASSWORD 'odoo_password';
ALTER USER odoo CREATEDB;
\q
```

---

## ⚙️ Cấu hình Odoo

### Tạo file cấu hình Odoo

Tạo file `odoo.conf` trong thư mục Odoo:

```ini
[options]
; Đường dẫn đến Odoo source code
addons_path = C:\Users\Admin\PycharmProjects\Peter's Project\Odoo\odoo19\addons,C:\Users\Admin\PycharmProjects\Peter's Project\Odoo\crm_custom

; Database
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo_password
db_name = odoo_db

; Server
http_port = 8069
http_interface = 127.0.0.1

; Logging
logfile = C:\Users\Admin\PycharmProjects\Peter's Project\Odoo\odoo.log
log_level = info

; Performance
workers = 0  ; 0 = không dùng workers (development mode)
max_cron_threads = 2

; Security
admin_passwd = admin
```

**Lưu ý**: Điều chỉnh các đường dẫn và mật khẩu theo môi trường của bạn!

---

## 🐍 Cài đặt Python Dependencies

### Tạo Virtual Environment (Khuyến nghị)

```powershell
# Di chuyển vào thư mục odoo19
cd C:\Users\Admin\PycharmProjects\Peter's Project\Odoo\odoo19

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
.\venv\Scripts\Activate.ps1

# Nếu gặp lỗi execution policy, chạy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Cài đặt các package cần thiết

```powershell
# Cài đặt pip dependencies
pip install -r requirements.txt

# Nếu không có requirements.txt, cài đặt thủ công:
pip install psycopg2-binary
pip install lxml
pip install pillow
pip install python-dateutil
pip install pytz
pip install Babel
pip install Werkzeug
pip install reportlab
pip install decorator
pip install requests
pip install XlsxWriter
```

---

## 🚀 Chạy Odoo

### Cách 1: Chạy trực tiếp với Python

```powershell
# Đảm bảo virtual environment đã được kích hoạt
.\venv\Scripts\Activate.ps1

# Chạy Odoo
python odoo-bin -c odoo.conf
```

### Cách 2: Chạy với các tham số

```powershell
python odoo-bin -c odoo.conf --dev=all
```

### Cách 3: Chạy và tạo database mới

```powershell
python odoo-bin -c odoo.conf -d odoo_db --init=base --stop-after-init
python odoo-bin -c odoo.conf -d odoo_db
```

---

## 📱 Truy cập Odoo

1. Mở trình duyệt
2. Truy cập: `http://localhost:8069`
3. Tạo database mới (nếu chưa có):
   - Master Password: `admin` (từ file config)
   - Database Name: `odoo_db`
   - Email: `admin@example.com`
   - Password: (mật khẩu admin)
   - Language: Tiếng Việt
   - Country: Việt Nam

---

## 📦 Cài đặt Module CRM Custom

1. Đăng nhập vào Odoo với tài khoản admin
2. Vào **Apps** (Ứng dụng)
3. Bỏ filter **Apps** để xem tất cả
4. Tìm **"CRM Custom"** hoặc **"CRM Tùy chỉnh"**
5. Click **Install**

Hoặc sử dụng command line:

```powershell
python odoo-bin -c odoo.conf -d odoo_db -u crm_custom
```

---

## 🔧 Troubleshooting

### Lỗi: "Module not found"
- Kiểm tra `addons_path` trong `odoo.conf`
- Đảm bảo đường dẫn đến `crm_custom` đúng

### Lỗi: "Could not connect to database"
- Kiểm tra PostgreSQL đang chạy
- Kiểm tra `db_user`, `db_password` trong config
- Thử kết nối thủ công: `psql -U odoo -d odoo_db`

### Lỗi: "Port 8069 already in use"
- Đổi port trong `odoo.conf`: `http_port = 8070`
- Hoặc tắt process đang dùng port 8069

### Lỗi: "psycopg2 not found"
```powershell
pip install psycopg2-binary
```

### Lỗi: "lxml not found"
```powershell
pip install lxml
```

---

## 📝 Kiểm tra Cài đặt

### Test Database Connection

```powershell
psql -U odoo -d odoo_db -c "SELECT version();"
```

### Test Odoo Module

```powershell
# Chạy Odoo với test mode
python odoo-bin -c odoo.conf -d odoo_db --test-enable -u crm_custom --stop-after-init
```

---

## 🎯 Next Steps

Sau khi cài đặt thành công:

1. ✅ Tạo một số Lead demo để test
2. ✅ Test tính năng chấm điểm Lead
3. ✅ Kiểm tra các views (Form, List, Kanban)
4. ✅ Test security rules
5. ✅ Chuẩn bị cho Giai đoạn 2

---

## 📚 Tài liệu Tham khảo

- [Odoo Installation Guide](https://www.odoo.com/documentation/19.0/administration/install.html)
- [Odoo Development Documentation](https://www.odoo.com/documentation/19.0/developer.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Chúc bạn cài đặt thành công! 🚀**

