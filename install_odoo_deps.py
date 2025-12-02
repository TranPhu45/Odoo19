#!/usr/bin/env python3
"""
Script to install Odoo dependencies with workarounds for Railway
Uses pip install -r with filtered requirements file
"""
import subprocess
import sys
import os
import re

ODOO_REQUIREMENTS = "odoo19/requirements.txt"
FILTERED_REQUIREMENTS = "requirements_filtered.txt"

def create_filtered_requirements():
    """Create filtered requirements file without problematic packages"""
    if not os.path.exists(ODOO_REQUIREMENTS):
        print(f"❌ ERROR: {ODOO_REQUIREMENTS} not found!")
        return False
    
    print("📝 Creating filtered requirements file...")
    
    # Read requirements file
    with open(ODOO_REQUIREMENTS, 'r') as f:
        requirements = f.readlines()
    
    # Filter out problematic packages (need system libraries)
    problematic = ['libsass', 'lxml']
    filtered_lines = []
    skipped = []
    
    for line in requirements:
        original_line = line.strip()
        if not original_line or original_line.startswith('#'):
            continue
        
        # Extract package name (before any version specifiers or markers)
        # Handle cases like: package==1.0 ; marker
        package_match = re.match(r'^([a-zA-Z0-9_-]+)', original_line)
        if not package_match:
            filtered_lines.append(line)
            continue
        
        package_name = package_match.group(1).lower()
        
        # Check if it's a problematic package
        skip = False
        for prob in problematic:
            if prob in package_name:
                skip = True
                skipped.append(original_line)
                break
        
        if not skip:
            filtered_lines.append(line)
    
    # Write filtered requirements
    with open(FILTERED_REQUIREMENTS, 'w') as f:
        f.writelines(filtered_lines)
    
    print(f"✅ Created {FILTERED_REQUIREMENTS}")
    
    if skipped:
        print(f"\n⚠️  Skipped {len(skipped)} packages that require system libraries:")
        for pkg in skipped[:5]:  # Show first 5
            print(f"   - {pkg}")
        if len(skipped) > 5:
            print(f"   ... and {len(skipped) - 5} more")
    
    return True

def install_dependencies():
    """Install Odoo dependencies"""
    print("📦 Installing Odoo dependencies...")
    
    # Create filtered requirements
    if not create_filtered_requirements():
        return False
    
    # Install from filtered requirements using pip install -r
    # This allows pip to properly handle markers
    print(f"\nInstalling from {FILTERED_REQUIREMENTS}...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', FILTERED_REQUIREMENTS],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode != 0:
            print(f"⚠️  Some packages failed to install")
            print(f"   Error output: {result.stderr[:500]}")
        else:
            print("✅ Installed packages from requirements file")
    except Exception as e:
        print(f"⚠️  Error installing from requirements: {str(e)}")
    
    # Install lxml (try binary wheel first, then fallback)
    print("\nInstalling lxml (binary wheel)...")
    lxml_installed = False
    
    # Try multiple strategies to install lxml
    strategies = [
        # Strategy 1: Try pre-built binary wheel (no compilation)
        (['--only-binary=:all:', 'lxml'], "binary wheel (pre-built)"),
        # Strategy 2: Try specific version with binary
        (['--only-binary=:all:', 'lxml==5.1.0'], "binary wheel (version 5.1.0)"),
        # Strategy 3: Try latest version (might have binary for this platform)
        (['lxml'], "latest version"),
        # Strategy 4: Try older version that might have binary
        (['lxml==4.9.3'], "version 4.9.3 (older, more compatible)"),
    ]
    
    for install_args, strategy_name in strategies:
        try:
            print(f"   Trying {strategy_name}...")
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install'] + install_args,
                check=True,
                capture_output=True,
                timeout=300
            )
            print(f"✅ Installed lxml ({strategy_name})")
            lxml_installed = True
            break
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Failed: {strategy_name}")
            continue
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)}")
            continue
    
    if not lxml_installed:
        print("⚠️  WARNING: Could not install lxml")
        print("   Odoo will run but some features may be limited:")
        print("   - HTML cleaning/parsing may not work")
        print("   - Some report generation features may be unavailable")
        print("   - This is usually OK for basic CRM functionality")
    
    # Install lxml_html_clean (required for Odoo, separate from lxml)
    print("\nInstalling lxml_html_clean...")
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'lxml_html_clean'],
            check=True,
            capture_output=True,
            timeout=300
        )
        print("✅ Installed lxml_html_clean")
    except:
        print("⚠️  Could not install lxml_html_clean (may already be installed)")
    
    # Verify essential packages
    print("\n🔍 Verifying essential packages...")
    essential_packages = ['passlib', 'polib', 'psutil', 'psycopg2-binary']
    for pkg in essential_packages:
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'show', pkg],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"✅ {pkg}")
            else:
                print(f"⚠️  {pkg} not found, installing...")
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', pkg],
                    check=True,
                    timeout=300
                )
                print(f"✅ Installed {pkg}")
        except:
            print(f"⚠️  Could not verify/install {pkg}")
    
    # Clean up
    if os.path.exists(FILTERED_REQUIREMENTS):
        os.remove(FILTERED_REQUIREMENTS)
        print(f"\n✅ Cleaned up {FILTERED_REQUIREMENTS}")
    
    print("\n✅ Dependency installation completed!")
    return True

if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)

