#!/bin/bash
set -e

echo "Building Odoo 19 application..."

# Clone Odoo 19 if not exists
if [ ! -d "odoo19" ]; then
    echo "Cloning Odoo 19 from GitHub..."
    git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1 odoo19
    echo "Odoo 19 cloned successfully"
else
    echo "Odoo 19 already exists"
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!"

