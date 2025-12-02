# CRM Custom Module - Odoo 19

Module CRM tùy chỉnh mở rộng chức năng CRM của Odoo với các tính năng nâng cao.

## Tính năng

### Giai đoạn 1 (Hiện tại)
- ✅ Mở rộng model CRM Lead với các trường tùy chỉnh
- ✅ Hệ thống chấm điểm lead tự động
- ✅ Phân loại chất lượng lead (Nóng/Ấm/Lạnh)
- ✅ Mở rộng model Partner với thống kê khách hàng
- ✅ Mở rộng model Sales Team với mục tiêu và hiệu suất
- ✅ Views tùy chỉnh (Form, List, Kanban, Search)
- ✅ Security rules cơ bản

## Cài đặt

1. Copy module vào thư mục addons của Odoo:
   ```bash
   cp -r crm_custom /path/to/odoo/addons/
   ```

2. Cập nhật danh sách apps trong Odoo:
   - Vào Settings > Apps > Update Apps List

3. Cài đặt module:
   - Tìm "CRM Custom" trong Apps
   - Click Install

## Yêu cầu

- Odoo 19.0
- Python 3.10+
- PostgreSQL 12+

## Dependencies

- base
- crm
- sales_team
- contacts

## Cấu trúc Module

```
crm_custom/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── crm_lead.py          # Mở rộng Lead model
│   ├── res_partner.py       # Mở rộng Partner model
│   └── crm_team.py          # Mở rộng Sales Team model
├── views/
│   ├── crm_lead_views.xml
│   ├── res_partner_views.xml
│   └── menu_items.xml
├── security/
│   ├── ir.model.access.csv
│   └── security_rules.xml
└── data/
    └── demo_data.xml
```

## Sử dụng

### Tính năng Lead

1. **Chấm điểm Lead**: 
   - Vào Lead > Chọn Lead > Tab "Thông tin Tùy chỉnh"
   - Click nút "Tính Điểm Lead" để tự động tính điểm
   - Điểm được tính dựa trên: ngân sách, xác suất, người quyết định, ngày đóng dự kiến

2. **Chất lượng Lead**:
   - Tự động phân loại: Nóng (≥70 điểm), Ấm (40-69 điểm), Lạnh (<40 điểm)

3. **Lọc và Tìm kiếm**:
   - Sử dụng bộ lọc theo chất lượng lead
   - Nhóm theo ngành hoặc chất lượng

### Tính năng Partner

- Xem thống kê cơ hội của khách hàng
- Theo dõi giá trị vòng đời khách hàng
- Xem tỷ lệ thắng cơ hội

## Phát triển

### Thêm trường mới

1. Thêm trường vào model (ví dụ: `models/crm_lead.py`)
2. Thêm trường vào view (ví dụ: `views/crm_lead_views.xml`)
3. Cập nhật security nếu cần

### Chạy tests

```bash
odoo-bin -c odoo.conf -d database_name -u crm_custom --test-enable
```

## License

LGPL-3

## Tác giả

Your Name

