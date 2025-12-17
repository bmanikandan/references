#!/bin/bash

# Gmail Playwright Test Automation Setup Script with UV Package Manager

set -e  # Exit on error

echo "=========================================="
echo "Gmail Playwright with UV Package Manager"
echo "=========================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${2}${1}${NC}"
}

print_header() {
    echo ""
    echo "=========================================="
    echo "$1"
    echo "=========================================="
}

# Check if uv is installed
print_header "Checking UV Installation"

if ! command -v uv &> /dev/null; then
    print_status "⚠️  UV is not installed. Installing UV..." "$YELLOW"
    
    # Install uv
    if command -v curl &> /dev/null; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        print_status "❌ curl is not installed. Please install curl first." "$RED"
        exit 1
    fi
    
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    if command -v uv &> /dev/null; then
        print_status "✅ UV installed successfully" "$GREEN"
    else
        print_status "❌ Failed to install UV. Please install manually from https://github.com/astral-sh/uv" "$RED"
        exit 1
    fi
else
    UV_VERSION=$(uv --version)
    print_status "✅ UV is already installed: $UV_VERSION" "$GREEN"
fi

# Check Python installation
print_header "Checking Python Installation"

if ! command -v python3 &> /dev/null; then
    print_status "⚠️  Python3 is not installed. Installing Python with UV..." "$YELLOW"
    uv python install 3.10
else
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "✅ Python $PYTHON_VERSION is installed" "$GREEN"
fi

# Create virtual environment with uv
print_header "Creating Virtual Environment"

if [ ! -d ".venv" ]; then
    print_status "Creating virtual environment with uv..." "$BLUE"
    uv venv
    print_status "✅ Virtual environment created" "$GREEN"
else
    print_status "✅ Virtual environment already exists" "$GREEN"
fi

# Activate virtual environment
print_status "Activating virtual environment..." "$BLUE"
source .venv/bin/activate

# Sync dependencies using uv
print_header "Installing Dependencies with UV"

print_status "Syncing dependencies from pyproject.toml..." "$CYAN"
uv sync

if [ $? -eq 0 ]; then
    print_status "✅ Dependencies synced successfully" "$GREEN"
else
    print_status "❌ Failed to sync dependencies" "$RED"
    exit 1
fi

# Install Playwright browsers
print_header "Installing Playwright Browsers"

print_status "Installing Chromium browser..." "$BLUE"
.venv/bin/playwright install chromium

if [ $? -eq 0 ]; then
    print_status "✅ Playwright browsers installed successfully" "$GREEN"
else
    print_status "❌ Failed to install Playwright browsers" "$RED"
    exit 1
fi

# Check if .env file exists
print_header "Configuration Setup"

if [ ! -f .env ]; then
    print_status "⚠️  .env file not found. Creating from template..." "$YELLOW"
    cp .env.example .env
    
    echo ""
    print_status "Please edit the .env file with your Gmail test credentials:" "$YELLOW"
    print_status "  nano .env" "$BLUE"
    echo ""
    print_status "Required fields:" "$YELLOW"
    print_status "  - GMAIL_EMAIL=your_test_email@gmail.com" "$BLUE"
    print_status "  - GMAIL_PASSWORD=your_test_password" "$BLUE"
    echo ""
    
    read -p "Would you like to edit .env now? (y/n): " edit_env
    if [ "$edit_env" = "y" ] || [ "$edit_env" = "Y" ]; then
        ${EDITOR:-nano} .env
    else
        print_status "Please edit .env file before running tests" "$YELLOW"
    fi
else
    print_status "✅ .env file found" "$GREEN"
fi

# Create reports directory
print_header "Creating Reports Directory"

mkdir -p reports/screenshots reports/videos
print_status "✅ Reports directory created" "$GREEN"

# Show UV info
print_header "UV Environment Information"

print_status "UV Version:" "$CYAN"
uv --version

print_status "\nPython Version in Virtual Environment:" "$CYAN"
.venv/bin/python --version

print_status "\nInstalled Packages:" "$CYAN"
uv pip list | head -20

# Display quick start guide
print_header "Setup Complete!"

echo ""
print_status "🚀 Quick Start Guide:" "$GREEN"
echo ""
print_status "1. Activate virtual environment:" "$CYAN"
print_status "   source .venv/bin/activate" "$BLUE"
echo ""
print_status "2. Edit configuration (if not done already):" "$CYAN"
print_status "   nano .env" "$BLUE"
echo ""
print_status "3. Run tests:" "$CYAN"
print_status "   uv run pytest -v -m smoke" "$BLUE"
print_status "   OR" "$YELLOW"
print_status "   ./run_tests.sh" "$BLUE"
echo ""
print_status "4. View reports:" "$CYAN"
print_status "   open reports/report.html" "$BLUE"
echo ""

print_header "UV Package Manager Benefits"

print_status "✨ UV Benefits:" "$GREEN"
print_status "  • 10-100x faster than pip" "$BLUE"
print_status "  • Better dependency resolution" "$BLUE"
print_status "  • Built-in virtual environment management" "$BLUE"
print_status "  • Lock file for reproducible builds" "$BLUE"
print_status "  • Written in Rust for speed" "$BLUE"
echo ""

print_status "📚 Useful UV Commands:" "$GREEN"
print_status "  uv sync              # Sync dependencies" "$BLUE"
print_status "  uv add <package>     # Add new package" "$BLUE"
print_status "  uv remove <package>  # Remove package" "$BLUE"
print_status "  uv pip list          # List installed packages" "$BLUE"
print_status "  uv run <command>     # Run command in venv" "$BLUE"
echo ""

print_header "Ready to Test!"

print_status "Environment is ready. Happy testing! 🎉" "$GREEN"
