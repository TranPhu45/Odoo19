# 🐍 Hướng dẫn Setup với Anaconda/Conda

Hướng dẫn chi tiết để tạo môi trường Conda cho Odoo 19.

---

## 📋 Yêu cầu

- **Anaconda** hoặc **Miniconda** đã được cài đặt
- Conda đã được thêm vào PATH
- PowerShell hoặc Command Prompt

---

## 🚀 Cách 1: Tự động (Khuyến nghị)

### Sử dụng Script PowerShell

```powershell
# Chạy script tự động
.\setup_conda_env.ps1
```

Script sẽ:
1. ✅ Kiểm tra Conda đã cài đặt
2. ✅ Tạo môi trường `Odoo19` với Python 3.10
3. ✅ Cài đặt tất cả dependencies từ `requirements.txt`
4. ✅ Hiển thị hướng dẫn sử dụng

---

## 🔧 Cách 2: Thủ công

### Bước 1: Tạo môi trường từ file environment.yml

```powershell
# Tạo môi trường từ file
conda env create -f environment.yml
```

### Bước 2: Hoặc tạo môi trường thủ công

```powershell
# Tạo môi trường với Python 3.10
conda create -n Odoo19 python=3.10 -y

# Kích hoạt môi trường
conda activate Odoo19

# Cài đặt dependencies
pip install -r requirements.txt

# Hoặc cài đặt từng package
pip install psycopg2-binary lxml pillow python-dateutil pytz Babel Werkzeug reportlab decorator requests XlsxWriter
```

---

## ✅ Kích hoạt Môi trường

### Trong PowerShell

```powershell
# Kích hoạt môi trường
conda activate Odoo19

# Kiểm tra Python
python --version

# Kiểm tra packages
pip list
```

### Trong Command Prompt (CMD)

```cmd
conda activate Odoo19
```

**Lưu ý**: Nếu gặp lỗi "conda: command not found", chạy:
```powershell
conda init powershell
# Hoặc
conda init cmd.exe
```
Sau đó khởi động lại terminal.

---

## 🚀 Chạy Odoo với Conda Environment

### Cách 1: Dùng Script (Khuyến nghị)

```powershell
# Chạy Odoo với môi trường Conda
.\run_odoo_conda.ps1

# Với database cụ thể
.\run_odoo_conda.ps1 -Database odoo_db

# Chế độ development
.\run_odoo_conda.ps1 -Database odoo_db -Dev

# Update module
.\run_odoo_conda.ps1 -Database odoo_db -Update
```

### Cách 2: Kích hoạt thủ công rồi chạy

```powershell
# Kích hoạt môi trường
conda activate Odoo19

# Chạy Odoo
python odoo19\odoo-bin -c odoo.conf

# Hoặc với database
python odoo19\odoo-bin -c odoo.conf -d odoo_db
```

### Cách 3: Dùng conda run (không cần activate)

```powershell
# Chạy trực tiếp với conda run
conda run -n Odoo19 python odoo19\odoo-bin -c odoo.conf
```

---

## 📦 Quản lý Môi trường

### Xem danh sách môi trường

```powershell
conda env list
```

### Xem packages trong môi trường

```powershell
conda activate Odoo19
pip list
```

### Cài đặt thêm package

```powershell
conda activate Odoo19
pip install package_name
```

### Cập nhật môi trường từ file

```powershell
conda env update -f environment.yml
```

### Xóa môi trường

```powershell
conda env remove -n Odoo19
```

---

## 🔄 Cập nhật Dependencies

### Cập nhật tất cả packages

```powershell
conda activate Odoo19
pip install --upgrade -r requirements.txt
```

### Cập nhật từng package

```powershell
conda activate Odoo19
pip install --upgrade package_name
```

---

## 🆘 Troubleshooting

### Lỗi: "conda: command not found"

**Giải pháp:**
```powershell
# Khởi tạo conda cho PowerShell
conda init powershell

# Khởi động lại PowerShell
```

Hoặc thêm Conda vào PATH thủ công:
1. Tìm đường dẫn Anaconda (thường là `C:\Users\YourName\anaconda3`)
2. Thêm vào PATH: `C:\Users\YourName\anaconda3\Scripts`

### Lỗi: "Activate.ps1 cannot be loaded"

**Giải pháp:**
```powershell
# Cho phép chạy script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Lỗi: "Module not found" khi chạy Odoo

**Giải pháp:**
```powershell
# Đảm bảo đã kích hoạt môi trường
conda activate Odoo19

# Kiểm tra package đã cài đặt
pip list | findstr package_name

# Cài đặt lại nếu thiếu
pip install package_name
```

### Lỗi: "psycopg2 không cài đặt được"

**Giải pháp:**
```powershell
conda activate Odoo19
pip install psycopg2-binary
```

---

## 📝 Checklist

- [ ] Anaconda/Miniconda đã cài đặt
- [ ] Conda đã được thêm vào PATH
- [ ] Môi trường `Odoo19` đã được tạo
- [ ] Tất cả dependencies đã được cài đặt
- [ ] Đã test kích hoạt môi trường: `conda activate Odoo19`
- [ ] Đã test chạy Odoo với môi trường Conda

---

## 🎯 So sánh: Conda vs Virtualenv

| Tính năng | Conda | Virtualenv |
|-----------|-------|------------|
| Quản lý Python | ✅ Có | ❌ Không |
| Quản lý packages | ✅ Có | ✅ Có |
| Cài đặt dễ dàng | ✅ Rất dễ | ⚠️ Cần cài thêm |
| Phù hợp Anaconda | ✅ Hoàn hảo | ⚠️ Không cần thiết |

**Khuyến nghị**: Nếu bạn đã dùng Anaconda, hãy dùng Conda environment!

---

## 📚 Tài liệu Tham khảo

- [Conda Documentation](https://docs.conda.io/)
- [Managing Environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/4.6.0/conda-cheatsheet.pdf)

---

**Chúc bạn thành công với Conda Environment! 🚀**

