# 📝 Các Câu Lệnh Chạy Theo Thứ Tự

File này chứa tất cả các câu lệnh cần thiết để cài đặt và chạy dự án Odoo CRM Custom.

---

## 🐍 CHO NGƯỜI DÙNG ANACONDA/CONDA

Nếu bạn đang dùng **Anaconda** hoặc **Miniconda**, xem file **`CONDA_SETUP.md`** để biết hướng dẫn chi tiết.

### Tạo môi trường Conda nhanh:

```powershell
# Cách 1: Dùng script tự động (Khuyến nghị)
.\setup_conda_env.ps1

# Cách 2: Từ file environment.yml
conda env create -f environment.yml

# Cách 3: Thủ công
conda create -n Odoo19 python=3.10 -y
conda activate Odoo19
pip install -r requirements.txt
```

### Chạy Odoo với Conda:

```powershell
# Dùng script (tự động kích hoạt môi trường)
.\run_odoo_conda.ps1

# Hoặc kích hoạt thủ công
conda activate Odoo19
python odoo19\odoo-bin -c odoo.conf
```

---

## 🔍 BƯỚC 0: Kiểm tra Phần mềm Đã Cài đặt

Mở PowerShell hoặc Command Prompt và chạy các lệnh sau để kiểm tra:

```powershell
# Kiểm tra Python
python --version

# Kiểm tra pip
pip --version

# Kiểm tra PostgreSQL
psql --version

# Kiểm tra Git
git --version
```

**Nếu thiếu phần mềm nào, cài đặt trước khi tiếp tục!**

---

## 📦 BƯỚC 1: Clone Odoo 19 Source Code

```powershell
# Di chuyển vào thư mục dự án
cd "C:\Users\Admin\PycharmProjects\Peter's Project\Odoo"

# Clone Odoo 19 (nếu chưa có)
git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1 odoo19
```

**Lưu ý**: Nếu đã có thư mục `odoo19`, bỏ qua bước này.

---

## 🐍 BƯỚC 2: Cài đặt Python Dependencies

### Cách 1: Dùng script tự động (Khuyến nghị)

```powershell
.\install_requirements.ps1
```

### Cách 2: Cài đặt thủ công

```powershell
# Cài đặt từ requirements.txt
pip install -r requirements.txt
```

### Cách 3: Cài đặt từng package quan trọng

```powershell
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

## 🗄️ BƯỚC 3: Setup PostgreSQL Database

### Cách 1: Dùng script tự động (Khuyến nghị)

```powershell
.\setup_database.ps1
```

Script sẽ hỏi bạn:
- Tên database (mặc định: `odoo_db`)
- Tên user (mặc định: `odoo`)
- Mật khẩu cho user
- Mật khẩu PostgreSQL (postgres user)

### Cách 2: Tạo thủ công qua psql

```powershell
# Kết nối PostgreSQL
psql -U postgres
```

Sau đó trong psql, chạy các lệnh sau:

```sql
-- Tạo user
CREATE USER odoo WITH PASSWORD 'odoo_password';

-- Cấp quyền
ALTER USER odoo CREATEDB;

-- Tạo database
CREATE DATABASE odoo_db OWNER odoo;

-- Thoát
\q
```

**Lưu ý**: Thay `odoo_password` bằng mật khẩu bạn muốn!

---

## ⚙️ BƯỚC 4: Cấu hình Odoo

### Chỉnh sửa file `odoo.conf`

Mở file `odoo.conf` và kiểm tra/cập nhật:

1. **addons_path**: Đảm bảo đường dẫn đúng
   ```
   addons_path = odoo19\addons,crm_custom
   ```

2. **Database settings**: Cập nhật thông tin database
   ```
   db_user = odoo
   db_password = odoo_password  (mật khẩu bạn đã tạo ở bước 3)
   ```

3. **Port**: Kiểm tra port (mặc định: 8069)
   ```
   http_port = 8069
   ```

---

## 🚀 BƯỚC 5: Chạy Odoo

### Cách 1: Dùng script PowerShell (Khuyến nghị)

```powershell
# Chạy Odoo bình thường
.\run_odoo.ps1

# Chạy với database cụ thể
.\run_odoo.ps1 -Database odoo_db

# Chạy với chế độ development
.\run_odoo.ps1 -Database odoo_db -Dev

# Update module
.\run_odoo.ps1 -Database odoo_db -Update
```

### Cách 2: Dùng Batch file

```cmd
run_odoo.bat
```

### Cách 3: Chạy trực tiếp

```powershell
# Chạy Odoo
python odoo19\odoo-bin -c odoo.conf

# Hoặc với database cụ thể
python odoo19\odoo-bin -c odoo.conf -d odoo_db

# Chạy và tạo database mới (lần đầu)
python odoo19\odoo-bin -c odoo.conf -d odoo_db --init=base --stop-after-init
python odoo19\odoo-bin -c odoo.conf -d odoo_db
```

---

## 🌐 BƯỚC 6: Truy cập Odoo qua Trình duyệt

1. Mở trình duyệt
2. Truy cập: `http://localhost:8069`

### Lần đầu tiên (Tạo Database):

1. Nhập **Master Password**: `admin` (từ file odoo.conf)
2. Click **Create Database**
3. Điền thông tin:
   - **Database Name**: `odoo_db`
   - **Email**: `admin@example.com`
   - **Password**: (mật khẩu admin của bạn)
   - **Language**: Tiếng Việt
   - **Country**: Việt Nam
4. Click **Create Database**

### Sau khi tạo Database (Cài đặt Module):

1. Đăng nhập với email và password vừa tạo
2. Vào **Apps** (Ứng dụng)
3. Bỏ filter **Apps** (nếu có)
4. Tìm **"CRM Custom"** hoặc **"CRM Tùy chỉnh"**
5. Click **Install**

---

## 🔄 Các Lệnh Hữu ích Khác

### Update Module

```powershell
# Update module crm_custom
python odoo19\odoo-bin -c odoo.conf -d odoo_db -u crm_custom

# Update tất cả modules
python odoo19\odoo-bin -c odoo.conf -d odoo_db -u all
```

### Chạy Tests

```powershell
# Chạy tests cho module
python odoo19\odoo-bin -c odoo.conf -d odoo_db --test-enable -u crm_custom --stop-after-init
```

### Xem Log

```powershell
# Xem log file (theo cấu hình trong odoo.conf)
Get-Content odoo.log -Tail 50

# Hoặc mở file log
notepad odoo.log
```

### Kiểm tra Database Connection

```powershell
# Test kết nối database
psql -U odoo -d odoo_db -c "SELECT version();"
```

### Dừng Odoo

- Nhấn `Ctrl + C` trong terminal đang chạy Odoo
- Hoặc đóng cửa sổ terminal

---

## 📋 Checklist Nhanh

Copy và chạy từng bước:

```powershell
# 1. Kiểm tra Python
python --version

# 2. Clone Odoo (nếu chưa có)
git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1 odoo19

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Setup database (chạy script hoặc tạo thủ công)
.\setup_database.ps1

# 5. Kiểm tra file odoo.conf đã được cấu hình đúng

# 6. Chạy Odoo
.\run_odoo.ps1
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Đảm bảo PostgreSQL đang chạy** trước khi chạy Odoo
2. **Kiểm tra port 8069** không bị chiếm bởi ứng dụng khác
3. **Cập nhật mật khẩu** trong `odoo.conf` sau khi tạo database
4. **Đọc log file** nếu gặp lỗi: `odoo.log`

---

## 🆘 Xử lý Lỗi

### Lỗi: "Module not found"
```powershell
# Kiểm tra addons_path trong odoo.conf
# Đảm bảo đường dẫn đúng: odoo19\addons,crm_custom
```

### Lỗi: "Could not connect to database"
```powershell
# Kiểm tra PostgreSQL đang chạy
# Test kết nối:
psql -U odoo -d odoo_db
```

### Lỗi: "Port 8069 already in use"
```powershell
# Đổi port trong odoo.conf hoặc tìm process đang dùng port:
netstat -ano | findstr :8069
```

---

**Chúc bạn thành công! 🚀**

