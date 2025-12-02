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

def is_railway_reference(value):
    """Check if value is a Railway variable reference like ${{Service.Variable}}"""
    if not value:
        return False
    return value.startswith('${{') and value.endswith('}}')

def generate_odoo_conf():
    """Generate odoo.conf from environment variables"""
    print("📝 Generating odoo.conf from environment variables...")
    
    # Get environment variables (Railway automatically injects these when PostgreSQL is linked)
    db_host = os.getenv('PGHOST')
    db_port = os.getenv('PGPORT')
    db_user = os.getenv('PGUSER')
    db_password = os.getenv('PGPASSWORD')
    db_name = os.getenv('PGDATABASE')
    http_port = os.getenv('PORT', '8069')
    admin_passwd = os.getenv('ADMIN_PASSWORD', 'admin')
    
    # Check for Railway variable references (Railway syntax: ${{Service.Variable}})
    # These are usually resolved by Railway at runtime, but we check anyway
    has_references = False
    if db_host and is_railway_reference(db_host):
        print("⚠️  WARNING: PGHOST is a Railway variable reference, not resolved value")
        print(f"   Value: {db_host}")
        print("   Railway should resolve this at runtime, but if it doesn't, you may need to set the actual value")
        has_references = True
    if db_port and is_railway_reference(db_port):
        print("⚠️  WARNING: PGPORT is a Railway variable reference, not resolved value")
        has_references = True
    if db_user and is_railway_reference(db_user):
        print("⚠️  WARNING: PGUSER is a Railway variable reference, not resolved value")
        has_references = True
    if db_password and is_railway_reference(db_password):
        print("⚠️  WARNING: PGPASSWORD is a Railway variable reference, not resolved value")
        has_references = True
    if db_name and is_railway_reference(db_name):
        print("⚠️  WARNING: PGDATABASE is a Railway variable reference, not resolved value")
        has_references = True
    
    if has_references:
        print("\n💡 NOTE: Railway variable references detected.")
        print("   Railway should resolve these automatically at runtime.")
        print("   If Odoo still can't connect, try setting actual values instead of references.")
        print("   Continuing anyway...\n")
    
    # Validate PostgreSQL variables (required for Railway)
    # Allow Railway references to pass through (Railway will resolve them)
    missing_vars = []
    if not db_host or (not is_railway_reference(db_host) and not db_host.strip()):
        missing_vars.append('PGHOST')
    if not db_port or (not is_railway_reference(db_port) and not db_port.strip()):
        missing_vars.append('PGPORT')
    if not db_user or (not is_railway_reference(db_user) and not db_user.strip()):
        missing_vars.append('PGUSER')
    if not db_password or (not is_railway_reference(db_password) and not db_password.strip()):
        missing_vars.append('PGPASSWORD')
    if not db_name or (not is_railway_reference(db_name) and not db_name.strip()):
        missing_vars.append('PGDATABASE')
    
    if missing_vars:
        print("❌ ERROR: PostgreSQL environment variables not found!")
        print(f"   Missing: {', '.join(missing_vars)}")
        print("\n📋 SOLUTION:")
        print("   1. Go to Railway Dashboard")
        print("   2. Select your project")
        print("   3. Add PostgreSQL service (if not exists)")
        print("   4. Link PostgreSQL service to your web service")
        print("   5. Railway will automatically inject PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE")
        print("\n   OR manually set these variables in Railway:")
        print("   - PGHOST")
        print("   - PGPORT")
        print("   - PGUSER")
        print("   - PGPASSWORD")
        print("   - PGDATABASE")
        return False
    
    # Validate admin password
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

