#!/usr/bin/env python3
"""
Generate odoo.conf from environment variables
Odoo doesn't support ${VAR} syntax, so we need to generate the file
"""
import os
import sys

ODOO_CONF_TEMPLATE = """[options]
; ============================================
; ODOO CONFIGURATION FILE FOR PRODUCTION (RAILWAY)
; ============================================
; This file is auto-generated from environment variables

; ============================================
; ADDONS PATH
; ============================================
addons_path = odoo19/addons,crm_custom

; ============================================
; DATABASE SETTINGS (Railway PostgreSQL Variables)
; ============================================
db_host = {db_host}
db_port = {db_port}
db_user = {db_user}
db_password = {db_password}
db_name = {db_name}

; ============================================
; SERVER SETTINGS
; ============================================
http_port = {http_port}
http_interface = 0.0.0.0

; ============================================
; LOGGING
; ============================================
logfile = /tmp/odoo.log
log_level = warn

; ============================================
; PERFORMANCE
; ============================================
workers = 2
max_cron_threads = 1

; ============================================
; SECURITY
; ============================================
admin_passwd = {admin_passwd}
"""

def generate_odoo_conf():
    """Generate odoo.conf from environment variables"""
    print("📝 Generating odoo.conf from environment variables...")
    
    # Get environment variables (Railway automatically injects these)
    db_host = os.getenv('PGHOST', 'localhost')
    db_port = os.getenv('PGPORT', '5432')
    db_user = os.getenv('PGUSER', 'odoo')
    db_password = os.getenv('PGPASSWORD', '')
    db_name = os.getenv('PGDATABASE', 'odoo_db')
    http_port = os.getenv('PORT', '8069')
    admin_passwd = os.getenv('ADMIN_PASSWORD', 'admin')
    
    # Validate required variables
    if not db_password:
        print("⚠️  WARNING: PGPASSWORD not set, using empty string")
    
    if not admin_passwd or admin_passwd == 'admin':
        print("⚠️  WARNING: ADMIN_PASSWORD not set or using default 'admin'")
        print("   Please set ADMIN_PASSWORD in Railway environment variables!")
    
    # Generate config file
    config_content = ODOO_CONF_TEMPLATE.format(
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_password=db_password,
        db_name=db_name,
        http_port=http_port,
        admin_passwd=admin_passwd
    )
    
    # Write to file
    with open('odoo.conf', 'w') as f:
        f.write(config_content)
    
    print("✅ Generated odoo.conf")
    print(f"   Database: {db_user}@{db_host}:{db_port}/{db_name}")
    print(f"   HTTP Port: {http_port}")
    
    return True

if __name__ == "__main__":
    success = generate_odoo_conf()
    sys.exit(0 if success else 1)

