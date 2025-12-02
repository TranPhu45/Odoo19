#!/usr/bin/env python3
"""
Script to download Odoo 19 if not exists
Uses Python standard library (no external dependencies)
"""
import os
import sys
import urllib.request
import zipfile
import shutil

ODOO_DIR = "odoo19"
ODOO_URL = "https://github.com/odoo/odoo/archive/refs/heads/19.0.zip"
ZIP_FILE = "odoo19.zip"

def download_odoo():
    """Download Odoo 19 from GitHub"""
    if os.path.exists(ODOO_DIR):
        print(f"✅ {ODOO_DIR} already exists")
        return True
    
    print("📥 Downloading Odoo 19 from GitHub...")
    try:
        # Download zip file
        print(f"Downloading from {ODOO_URL}...")
        urllib.request.urlretrieve(ODOO_URL, ZIP_FILE)
        print(f"✅ Downloaded {ZIP_FILE}")
        
        # Extract zip
        print(f"Extracting {ZIP_FILE}...")
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(".")
        print("✅ Extracted successfully")
        
        # Rename folder
        if os.path.exists("odoo-19.0"):
            if os.path.exists(ODOO_DIR):
                shutil.rmtree(ODOO_DIR)
            os.rename("odoo-19.0", ODOO_DIR)
            print(f"✅ Renamed to {ODOO_DIR}")
        
        # Clean up
        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)
            print(f"✅ Removed {ZIP_FILE}")
        
        # Verify odoo-bin exists
        odoo_bin = os.path.join(ODOO_DIR, "odoo-bin")
        if os.path.exists(odoo_bin):
            print(f"✅ Verified: {odoo_bin} exists")
            return True
        else:
            print(f"❌ ERROR: {odoo_bin} not found!")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = download_odoo()
    sys.exit(0 if success else 1)

