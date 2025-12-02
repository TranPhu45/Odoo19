#!/usr/bin/env python3
"""
Script to install Odoo dependencies with workarounds for Railway
Skips problematic packages that require system libraries
"""
import subprocess
import sys
import os

ODOO_REQUIREMENTS = "odoo19/requirements.txt"

def install_dependencies():
    """Install Odoo dependencies with workarounds"""
    if not os.path.exists(ODOO_REQUIREMENTS):
        print(f"❌ ERROR: {ODOO_REQUIREMENTS} not found!")
        return False
    
    print("📦 Installing Odoo dependencies...")
    print(f"Reading requirements from {ODOO_REQUIREMENTS}...")
    
    # Read requirements file
    with open(ODOO_REQUIREMENTS, 'r') as f:
        requirements = f.readlines()
    
    # Filter out problematic packages
    problematic = ['lxml', 'libsass']
    filtered_requirements = []
    skipped = []
    
    for req in requirements:
        req = req.strip()
        if not req or req.startswith('#'):
            continue
        
        # Check if it's a problematic package
        skip = False
        for prob in problematic:
            if prob in req.lower():
                skip = True
                skipped.append(req)
                break
        
        if not skip:
            filtered_requirements.append(req)
    
    # Install filtered requirements
    if filtered_requirements:
        print(f"Installing {len(filtered_requirements)} packages...")
        for req in filtered_requirements:
            try:
                print(f"Installing: {req}")
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', req],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode != 0:
                    print(f"⚠️  Warning: Failed to install {req}")
                    print(f"   Error: {result.stderr[:200]}")
                else:
                    print(f"✅ Installed: {req}")
            except Exception as e:
                print(f"⚠️  Warning: Error installing {req}: {str(e)}")
    
    # Install alternatives for skipped packages
    if skipped:
        print(f"\n⚠️  Skipped {len(skipped)} packages that require system libraries:")
        for pkg in skipped:
            print(f"   - {pkg}")
        
        print("\nInstalling alternatives...")
        
        # Install lxml-binary instead of lxml
        if any('lxml' in pkg.lower() for pkg in skipped):
            print("Installing lxml-binary (pre-built wheel)...")
            try:
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', 'lxml-binary'],
                    check=True,
                    timeout=300
                )
                print("✅ Installed lxml-binary")
            except:
                print("⚠️  Could not install lxml-binary, trying lxml (may fail)...")
                try:
                    subprocess.run(
                        [sys.executable, '-m', 'pip', 'install', '--only-binary=:all:', 'lxml'],
                        check=True,
                        timeout=300
                    )
                    print("✅ Installed lxml (binary)")
                except:
                    print("❌ Could not install lxml, Odoo may have limited functionality")
        
        # Install lxml_html_clean (required for Odoo)
        print("Installing lxml_html_clean...")
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'lxml_html_clean'],
                check=True,
                timeout=300
            )
            print("✅ Installed lxml_html_clean")
        except:
            print("⚠️  Could not install lxml_html_clean")
    
    # Install essential packages that might be missing
    essential_packages = [
        'passlib',
        'polib',
        'psutil',
        'psycopg2-binary',
        'Pillow',
        'python-dateutil',
        'pytz',
        'Babel',
        'Werkzeug',
        'reportlab',
        'decorator',
        'requests',
        'XlsxWriter',
        'zeep',
        'num2words',
        'python-stdnum',
        'pyserial',
        'qrcode',
        'vobject',
        'gevent',
        'greenlet',
    ]
    
    print("\n📦 Installing essential packages...")
    for pkg in essential_packages:
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', pkg],
                check=True,
                capture_output=True,
                timeout=300
            )
            print(f"✅ {pkg}")
        except:
            print(f"⚠️  {pkg} (may already be installed)")
    
    print("\n✅ Dependency installation completed!")
    return True

if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)

