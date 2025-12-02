# 🚀 Quick Start Guide - Chạy Odoo CRM Project

Hướng dẫn nhanh để bắt đầu với dự án Odoo CRM Custom.

## ⚡ Các bước nhanh (Nếu đã có Odoo và PostgreSQL)

### 1. Cài đặt Dependencies

```powershell
.\install_requirements.ps1
```

### 2. Setup Database

```powershell
.\setup_database.ps1
```

Hoặc tạo thủ công:
```sql
CREATE USER odoo WITH PASSWORD 'odoo_password';
ALTER USER odoo CREATEDB;
CREATE DATABASE odoo_db OWNER odoo;
```

### 3. Cấu hình Odoo

Chỉnh sửa file `odoo.conf`:
- Điều chỉnh `addons_path` 
- Cập nhật thông tin database
- Kiểm tra port (mặc định: 8069)

### 4. Chạy Odoo

```powershell
# Chạy bình thường
.\run_odoo.ps1

# Hoặc với database cụ thể
.\run_odoo.ps1 -Database odoo_db

# Chế độ development
.\run_odoo.ps1 -Database odoo_db -Dev

# Update module
.\run_odoo.ps1 -Database odoo_db -Update
```

### 5. Truy cập Odoo

Mở trình duyệt: `http://localhost:8069`

- **Lần đầu**: Tạo database mới
  - Master Password: `admin` (từ odoo.conf)
  - Database Name: `odoo_db`
  - Email: `admin@example.com`
  - Password: (mật khẩu admin của bạn)

- **Sau khi tạo database**: Cài đặt module
  - Vào **Apps** → Tìm **"CRM Custom"** → **Install**

## 📋 Checklist Cài đặt

- [ ] Python 3.10+ đã cài đặt
- [ ] PostgreSQL 12+ đã cài đặt và đang chạy
- [ ] Odoo 19 source code đã được clone/tải
- [ ] Module `crm_custom` đã có trong thư mục
- [ ] File `odoo.conf` đã được cấu hình
- [ ] Python dependencies đã được cài đặt
- [ ] Database đã được tạo
- [ ] Odoo đã chạy thành công
- [ ] Module đã được cài đặt

## 🔧 Troubleshooting Nhanh

| Lỗi | Giải pháp |
|-----|-----------|
| Module not found | Kiểm tra `addons_path` trong `odoo.conf` |
| Database connection failed | Kiểm tra PostgreSQL đang chạy và thông tin trong config |
| Port 8069 in use | Đổi port trong `odoo.conf` hoặc tắt process khác |
| psycopg2 not found | Chạy `pip install psycopg2-binary` |

## 📚 Tài liệu Chi tiết

Xem file `SETUP_GUIDE.md` để biết hướng dẫn chi tiết.

## 🎯 Sau khi cài đặt

1. Tạo Lead mới để test
2. Test tính năng chấm điểm Lead
3. Kiểm tra các views (Form, List, Kanban)
4. Xem thống kê trong Partner form

---

**Chúc bạn thành công! 🚀**

