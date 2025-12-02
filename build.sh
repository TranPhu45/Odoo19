#!/bin/bash
set -e

echo "=========================================="
echo "Building Odoo 19 application..."
echo "=========================================="

# Clone Odoo 19 if not exists
if [ ! -d "odoo19" ]; then
    echo "Cloning Odoo 19 from GitHub..."
    git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1 odoo19
    echo "✅ Odoo 19 cloned successfully"
else
    echo "ℹ️  Odoo 19 already exists"
fi

# Verify odoo-bin exists
if [ -f "odoo19/odoo-bin" ]; then
    echo "✅ Found odoo-bin at odoo19/odoo-bin"
    ls -la odoo19/odoo-bin
else
    echo "❌ ERROR: odoo-bin not found!"
    echo "Current directory: $(pwd)"
    echo "Listing files:"
    ls -la
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "=========================================="
echo "✅ Build completed successfully!"
echo "=========================================="

