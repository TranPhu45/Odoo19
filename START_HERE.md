# 🎯 BẮT ĐẦU TỪ ĐÂY

Chào mừng bạn đến với dự án **Odoo 19 CRM Custom**!

## 📁 Cấu trúc Dự án

```
Odoo/
├── crm_custom/              # Module CRM tùy chỉnh của bạn
├── odoo.conf                # File cấu hình Odoo
├── requirements.txt          # Python dependencies
├── SETUP_GUIDE.md           # Hướng dẫn cài đặt chi tiết
├── QUICK_START.md           # Hướng dẫn nhanh
├── START_HERE.md            # File này
└── Scripts:
    ├── setup_database.ps1   # Setup PostgreSQL database
    ├── install_requirements.ps1  # Cài đặt Python packages
    ├── run_odoo.ps1         # Chạy Odoo (PowerShell)
    └── run_odoo.bat         # Chạy Odoo (Batch)
```

## 🚀 Các bước Bắt đầu

### Bước 1: Đọc Hướng dẫn

**Nếu bạn mới bắt đầu:**
👉 Đọc file **`SETUP_GUIDE.md`** - Hướng dẫn chi tiết từng bước

**Nếu bạn đã quen với Odoo:**
👉 Đọc file **`QUICK_START.md`** - Hướng dẫn nhanh

### Bước 2: Cài đặt Phần mềm Cần thiết

1. **Python 3.10+**
   - Tải từ: https://www.python.org/downloads/
   - ⚠️ **Quan trọng**: Tick "Add Python to PATH"

2. **PostgreSQL 12+**
   - Tải từ: https://www.postgresql.org/download/windows/
   - Ghi nhớ mật khẩu cho user `postgres`

3. **Odoo 19 Source Code**
   ```powershell
   git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1 odoo19
   ```

### Bước 3: Cấu hình

1. **Chỉnh sửa `odoo.conf`**:
   - Điều chỉnh đường dẫn `addons_path`
   - Cập nhật thông tin database
   - Kiểm tra port (mặc định: 8069)

2. **Setup Database**:
   ```powershell
   .\setup_database.ps1
   ```
   Hoặc tạo thủ công trong PostgreSQL

3. **Cài đặt Python Dependencies**:
   ```powershell
   .\install_requirements.ps1
   ```
   Hoặc:
   ```powershell
   pip install -r requirements.txt
   ```

### Bước 4: Chạy Odoo

```powershell
# Cách 1: Dùng PowerShell script
.\run_odoo.ps1

# Cách 2: Dùng Batch file
run_odoo.bat

# Cách 3: Chạy trực tiếp
python odoo19\odoo-bin -c odoo.conf
```

### Bước 5: Truy cập và Cài đặt Module

1. Mở trình duyệt: `http://localhost:8069`
2. Tạo database mới (lần đầu):
   - Master Password: `admin` (từ odoo.conf)
   - Database Name: `odoo_db`
3. Đăng nhập và cài đặt module:
   - Vào **Apps** → Tìm **"CRM Custom"** → **Install**

## 📋 Checklist

Sử dụng checklist này để đảm bảo bạn đã hoàn thành tất cả các bước:

- [ ] Python 3.10+ đã cài đặt
- [ ] PostgreSQL 12+ đã cài đặt và đang chạy
- [ ] Odoo 19 source code đã được clone/tải
- [ ] File `odoo.conf` đã được cấu hình
- [ ] Database đã được tạo
- [ ] Python dependencies đã được cài đặt
- [ ] Odoo đã chạy thành công
- [ ] Module `crm_custom` đã được cài đặt

## 🆘 Cần Trợ giúp?

### Lỗi thường gặp:

1. **"Module not found"**
   - ✅ Kiểm tra `addons_path` trong `odoo.conf`
   - ✅ Đảm bảo đường dẫn đến `crm_custom` đúng

2. **"Could not connect to database"**
   - ✅ Kiểm tra PostgreSQL đang chạy
   - ✅ Kiểm tra thông tin database trong `odoo.conf`
   - ✅ Test kết nối: `psql -U odoo -d odoo_db`

3. **"Port 8069 already in use"**
   - ✅ Đổi port trong `odoo.conf`: `http_port = 8070`
   - ✅ Hoặc tắt process đang dùng port 8069

### Tài liệu:

- 📖 **SETUP_GUIDE.md** - Hướng dẫn chi tiết
- ⚡ **QUICK_START.md** - Hướng dẫn nhanh
- 📚 **CRM_Project_Plan.md** - Kế hoạch dự án
- 📝 **crm_custom/README.md** - Tài liệu module

## 🎯 Sau khi Cài đặt Thành công

1. ✅ Tạo một số Lead demo để test
2. ✅ Test tính năng chấm điểm Lead
3. ✅ Kiểm tra các views (Form, List, Kanban)
4. ✅ Xem thống kê trong Partner form
5. ✅ Chuẩn bị cho Giai đoạn 2

## 📞 Liên hệ

Nếu gặp vấn đề, hãy:
1. Kiểm tra file `SETUP_GUIDE.md` phần Troubleshooting
2. Xem log file: `odoo.log` (theo cấu hình trong odoo.conf)
3. Kiểm tra console output khi chạy Odoo

---

**Chúc bạn thành công với dự án! 🚀**

*Bắt đầu từ file `SETUP_GUIDE.md` hoặc `QUICK_START.md` để biết thêm chi tiết.*

