# ⚡ Conda Quick Start - Hướng dẫn Nhanh

Hướng dẫn nhanh để tạo và sử dụng Conda environment cho Odoo 19.

---

## 🚀 3 Bước Đơn giản

### Bước 1: Tạo môi trường

```powershell
.\setup_conda_env.ps1
```

Hoặc thủ công:
```powershell
conda create -n Odoo19 python=3.10 -y
conda activate Odoo19
pip install -r requirements.txt
```

### Bước 2: Chạy Odoo

```powershell
.\run_odoo_conda.ps1
```

### Bước 3: Truy cập

Mở trình duyệt: `http://localhost:8069`

---

## 📋 Các Lệnh Thường Dùng

### Kích hoạt môi trường
```powershell
conda activate Odoo19
```

### Chạy Odoo
```powershell
# Với script
.\run_odoo_conda.ps1

# Hoặc thủ công
conda activate Odoo19
python odoo19\odoo-bin -c odoo.conf
```

### Cài đặt thêm package
```powershell
conda activate Odoo19
pip install package_name
```

### Xem danh sách packages
```powershell
conda activate Odoo19
pip list
```

### Xóa môi trường (nếu cần)
```powershell
conda env remove -n Odoo19
```

---

## ⚠️ Lưu Ý

1. **Luôn kích hoạt môi trường** trước khi chạy Odoo
2. **Hoặc dùng script** `run_odoo_conda.ps1` (tự động kích hoạt)
3. **Kiểm tra môi trường** đã kích hoạt: `conda info --envs` (dấu * ở môi trường hiện tại)

---

## 🆘 Lỗi Thường Gặp

### "conda: command not found"
```powershell
conda init powershell
# Khởi động lại PowerShell
```

### "Activate.ps1 cannot be loaded"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

**Xem `CONDA_SETUP.md` để biết hướng dẫn chi tiết!**

