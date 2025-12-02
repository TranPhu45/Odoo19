# -*- coding: utf-8 -*-
{
    'name': 'CRM Custom - Module Tùy chỉnh',
    'version': '19.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Module CRM tùy chỉnh với các tính năng mở rộng cho quản lý lead, liên hệ và cơ hội',
    'description': """
CRM Custom Module
=================
Module này mở rộng chức năng CRM của Odoo với các tính năng:
- Quản lý Lead nâng cao với hệ thống chấm điểm
- Quản lý liên hệ với phân đoạn nâng cao
- Quản lý cơ hội với pipeline tùy chỉnh
- Các trường và giao diện tùy chỉnh
- Báo cáo và phân tích nâng cao
    """,
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'depends': [
        'base',
        'crm',
        'sales_team',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'views/crm_lead_views.xml',
        'views/res_partner_views.xml',
        'views/menu_items.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

