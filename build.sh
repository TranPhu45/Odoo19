#!/bin/bash
set -e

echo "=========================================="
echo "Building Odoo 19 application..."
echo "=========================================="

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ ERROR: git is not installed!"
    echo "Installing git..."
    apt-get update && apt-get install -y git || yum install -y git || echo "⚠️  Cannot install git automatically"
fi

# Check git version
echo "Git version:"
git --version || echo "⚠️  Git not available"

# Clone Odoo 19 if not exists
if [ ! -d "odoo19" ]; then
    echo "Cloning Odoo 19 from GitHub..."
    echo "Current directory: $(pwd)"
    echo "Listing files before clone:"
    ls -la
    
    # Try cloning with retry
    MAX_RETRIES=3
    RETRY_COUNT=0
    
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        echo "Attempt $((RETRY_COUNT + 1)) of $MAX_RETRIES..."
        
        if git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1 odoo19; then
            echo "✅ Odoo 19 cloned successfully"
            break
        else
            RETRY_COUNT=$((RETRY_COUNT + 1))
            if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
                echo "⚠️  Clone failed, retrying in 5 seconds..."
                sleep 5
            else
                echo "❌ ERROR: Failed to clone Odoo 19 after $MAX_RETRIES attempts"
                echo "Trying alternative method: Download from GitHub releases..."
                
                # Alternative: Download as zip
                if command -v curl &> /dev/null; then
                    echo "Downloading Odoo 19 as zip..."
                    curl -L https://github.com/odoo/odoo/archive/refs/heads/19.0.zip -o odoo19.zip
                    unzip -q odoo19.zip
                    mv odoo-19.0 odoo19
                    rm odoo19.zip
                    echo "✅ Odoo 19 downloaded successfully"
                elif command -v wget &> /dev/null; then
                    echo "Downloading Odoo 19 as zip..."
                    wget -q https://github.com/odoo/odoo/archive/refs/heads/19.0.zip -O odoo19.zip
                    unzip -q odoo19.zip
                    mv odoo-19.0 odoo19
                    rm odoo19.zip
                    echo "✅ Odoo 19 downloaded successfully"
                else
                    echo "❌ ERROR: Cannot clone or download Odoo 19"
                    exit 1
                fi
            fi
        fi
    done
else
    echo "ℹ️  Odoo 19 already exists"
fi

# Verify odoo-bin exists
if [ -f "odoo19/odoo-bin" ]; then
    echo "✅ Found odoo-bin at odoo19/odoo-bin"
    ls -la odoo19/odoo-bin
    echo "File size: $(du -h odoo19/odoo-bin | cut -f1)"
else
    echo "❌ ERROR: odoo-bin not found!"
    echo "Current directory: $(pwd)"
    echo "Listing files:"
    ls -la
    if [ -d "odoo19" ]; then
        echo "Listing odoo19 directory:"
        ls -la odoo19/ | head -20
    fi
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "=========================================="
echo "✅ Build completed successfully!"
echo "=========================================="

