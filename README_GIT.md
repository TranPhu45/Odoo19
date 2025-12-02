# 📦 Hướng dẫn Git cho Dự án Odoo CRM

Hướng dẫn sử dụng Git với dự án Odoo CRM Custom.

---

## 🔒 File .gitignore

File `.gitignore` đã được cấu hình để loại trừ:

### ✅ Các file KHÔNG được commit:
- ❌ `odoo.conf` - File cấu hình chứa mật khẩu
- ❌ `*.log` - Log files
- ❌ `*.db`, `*.sql` - Database files
- ❌ `__pycache__/`, `*.pyc` - Python cache
- ❌ `venv/`, `env/` - Virtual environments
- ❌ `.idea/`, `.vscode/` - IDE files
- ❌ `*.key`, `*.pem` - Secret keys
- ❌ `.env` - Environment variables

### ✅ Các file ĐƯỢC commit:
- ✅ Source code module (`crm_custom/`)
- ✅ Documentation (`*.md`)
- ✅ Scripts (`*.ps1`, `*.bat`)
- ✅ Requirements (`requirements.txt`)
- ✅ Example config (`odoo.conf.example`)

---

## 🚀 Lần đầu Push lên Git

### Bước 1: Khởi tạo Git Repository (nếu chưa có)

```powershell
# Kiểm tra đã có .git chưa
ls .git

# Nếu chưa có, khởi tạo
git init
```

### Bước 2: Kiểm tra file sẽ được commit

```powershell
# Xem các file sẽ được thêm
git status

# Xem các file bị ignore
git status --ignored
```

### Bước 3: Thêm file vào staging

```powershell
# Thêm tất cả file (trừ những file trong .gitignore)
git add .

# Hoặc thêm từng file cụ thể
git add crm_custom/
git add *.md
git add *.ps1
```

### Bước 4: Commit

```powershell
git commit -m "Initial commit: Odoo 19 CRM Custom module"
```

### Bước 5: Thêm Remote Repository

```powershell
# Thêm remote (thay YOUR_REPO_URL bằng URL thực tế)
git remote add origin YOUR_REPO_URL

# Kiểm tra remote
git remote -v
```

### Bước 6: Push lên Git

```powershell
# Push lên branch main/master
git push -u origin main

# Hoặc nếu branch là master
git push -u origin master
```

---

## 📝 Quy trình làm việc hàng ngày

### 1. Kiểm tra thay đổi

```powershell
# Xem các file đã thay đổi
git status

# Xem chi tiết thay đổi
git diff
```

### 2. Thêm file vào staging

```powershell
# Thêm tất cả thay đổi
git add .

# Hoặc thêm file cụ thể
git add crm_custom/models/crm_lead.py
```

### 3. Commit

```powershell
# Commit với message
git commit -m "Add lead scoring feature"

# Commit với message chi tiết
git commit -m "Add lead scoring feature

- Implemented automatic lead scoring
- Added lead quality classification
- Updated views with new fields"
```

### 4. Push lên Git

```powershell
# Push lên remote
git push

# Hoặc push lên branch cụ thể
git push origin main
```

---

## ⚠️ Lưu ý Quan trọng

### 1. KHÔNG commit file nhạy cảm

**Tuyệt đối KHÔNG commit:**
- ❌ `odoo.conf` (chứa mật khẩu database)
- ❌ File chứa API keys
- ❌ File chứa thông tin cá nhân
- ❌ Database files
- ❌ Log files có thông tin nhạy cảm

### 2. Sử dụng odoo.conf.example

- ✅ Commit file `odoo.conf.example` (không có mật khẩu thật)
- ❌ KHÔNG commit `odoo.conf` (có mật khẩu thật)

### 3. Kiểm tra trước khi commit

```powershell
# Xem file sẽ được commit
git status

# Xem nội dung thay đổi
git diff

# Xem file bị ignore
git status --ignored
```

---

## 🔧 Các Lệnh Git Hữu ích

### Xem lịch sử

```powershell
# Xem commit history
git log

# Xem commit history dạng compact
git log --oneline

# Xem thay đổi của file cụ thể
git log -- crm_custom/models/crm_lead.py
```

### Undo thay đổi

```powershell
# Bỏ thay đổi chưa staged
git checkout -- filename

# Bỏ file khỏi staging
git reset HEAD filename

# Undo commit (giữ thay đổi)
git reset --soft HEAD~1

# Undo commit (xóa thay đổi)
git reset --hard HEAD~1
```

### Branch

```powershell
# Tạo branch mới
git branch feature/new-feature

# Chuyển sang branch
git checkout feature/new-feature

# Tạo và chuyển sang branch
git checkout -b feature/new-feature

# Xem tất cả branches
git branch -a

# Merge branch
git merge feature/new-feature
```

### Xem thay đổi

```powershell
# Xem thay đổi chưa staged
git diff

# Xem thay đổi đã staged
git diff --staged

# Xem thay đổi giữa 2 commits
git diff commit1 commit2
```

---

## 🆘 Xử lý Lỗi

### Đã commit nhầm file nhạy cảm

```powershell
# Xóa file khỏi Git (nhưng giữ file local)
git rm --cached odoo.conf

# Commit thay đổi
git commit -m "Remove sensitive config file"

# Push
git push
```

### Đã push nhầm file nhạy cảm

**CẢNH BÁO**: Nếu đã push file nhạy cảm lên Git, cần:
1. Xóa file khỏi Git history (sử dụng `git filter-branch` hoặc `BFG Repo-Cleaner`)
2. Đổi mật khẩu/token đã bị lộ
3. Thông báo cho team nếu có

### File bị ignore nhưng vẫn hiện trong Git

```powershell
# Xóa file khỏi Git cache
git rm --cached filename

# Commit
git commit -m "Remove file from Git"
```

---

## 📋 Checklist trước khi Push

- [ ] Đã kiểm tra `git status` - không có file nhạy cảm
- [ ] Đã kiểm tra `git diff` - không có mật khẩu/token
- [ ] File `odoo.conf` KHÔNG có trong staging
- [ ] Đã commit message rõ ràng
- [ ] Đã test code trước khi commit
- [ ] Đã cập nhật documentation nếu cần

---

## 🔐 Bảo mật

### Best Practices:

1. **Luôn sử dụng `.gitignore`** - Đã được cấu hình sẵn
2. **Sử dụng `odoo.conf.example`** - Template không có mật khẩu
3. **Kiểm tra trước khi commit** - `git status` và `git diff`
4. **Không commit mật khẩu** - Dù đã được hash hay encode
5. **Sử dụng environment variables** - Cho production
6. **Rotate credentials** - Nếu đã commit nhầm

---

## 📚 Tài liệu Tham khảo

- [Git Documentation](https://git-scm.com/doc)
- [Git Ignore Patterns](https://git-scm.com/docs/gitignore)
- [Git Security Best Practices](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)

---

**Nhớ: An toàn hơn là xin lỗi! Luôn kiểm tra trước khi commit! 🔒**

