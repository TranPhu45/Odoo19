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
    return isinstance(value, str) and value.startswith('${{') and value.endswith('}}')

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
    
    # Debug: Print what we got
    print(f"🔍 Debug - Environment variables:")
    print(f"   PGHOST: {db_host}")
    print(f"   PGPORT: {db_port}")
    print(f"   PGUSER: {db_user}")
    print(f"   PGPASSWORD: {'***' if db_password else 'None'}")
    print(f"   PGDATABASE: {db_name}")
    
    # Check for Railway variable references (Railway syntax: ${{Service.Variable}})
    # These are usually resolved by Railway at runtime, but we check anyway
    has_references = False
    if db_host and is_railway_reference(db_host):
        print("⚠️  WARNING: PGHOST is a Railway variable reference, not resolved value")
        print(f"   Value: {db_host}")
        print("   Railway should resolve this at runtime")
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
        print("   We'll generate odoo.conf with these references - Railway will resolve them when Odoo runs.\n")
    
    # Validate PostgreSQL variables (required for Railway)
    # Allow Railway references to pass through (Railway will resolve them)
    # Also allow empty strings if they are references (Railway will resolve)
    missing_vars = []
    
    # Check if variables exist (even if they are references)
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
        print("   3. Go to Odoo19 service → Variables tab")
        print("   4. Verify these variables exist:")
        print("      - PGHOST")
        print("      - PGPORT")
        print("      - PGUSER")
        print("      - PGPASSWORD")
        print("      - PGDATABASE")
        print("   5. If they are references (${{Postgres.XXX}}), Railway should resolve them")
        print("   6. If not resolved, replace references with actual values from Postgres service")
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
    # Even if values are references, we'll write them - Railway will resolve at runtime
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
    if has_references:
        print(f"   Database: {db_user}@{db_host}:{db_port}/{db_name} (Railway will resolve references)")
    else:
        print(f"   Database: {db_user}@{db_host}:{db_port}/{db_name}")
    print(f"   HTTP Port: {http_port}")
    
    return True

if __name__ == "__main__":
    success = generate_odoo_conf()
    sys.exit(0 if success else 1)

