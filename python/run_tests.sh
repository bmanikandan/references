#!/bin/bash

# Gmail Playwright Test Automation Setup and Execution Script

set -e  # Exit on error

echo "=========================================="
echo "Gmail Playwright Test Automation"
echo "=========================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Check Python installation
print_header "Checking Prerequisites"

if ! command -v python3 &> /dev/null; then
    print_status "❌ Python3 is not installed. Please install Python 3.8 or higher." "$RED"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_status "✅ Python $PYTHON_VERSION is installed" "$GREEN"

# Check pip
if ! command -v pip3 &> /dev/null; then
    print_status "❌ pip3 is not installed. Please install pip." "$RED"
    exit 1
fi

print_status "✅ pip3 is installed" "$GREEN"

# Install dependencies
print_header "Installing Python Dependencies"

print_status "Installing packages from requirements.txt..." "$BLUE"
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    print_status "✅ Dependencies installed successfully" "$GREEN"
else
    print_status "❌ Failed to install dependencies" "$RED"
    exit 1
fi

# Install Playwright browsers
print_header "Installing Playwright Browsers"

print_status "Installing Chromium browser..." "$BLUE"
playwright install chromium

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
    read -p "Press Enter after updating .env file to continue..."
else
    print_status "✅ .env file found" "$GREEN"
fi

# Validate .env configuration
print_header "Validating Configuration"

source .env

if [ -z "$GMAIL_EMAIL" ] || [ "$GMAIL_EMAIL" == "your_test_email@gmail.com" ]; then
    print_status "❌ GMAIL_EMAIL not configured in .env file" "$RED"
    exit 1
fi

if [ -z "$GMAIL_PASSWORD" ] || [ "$GMAIL_PASSWORD" == "your_test_password" ]; then
    print_status "❌ GMAIL_PASSWORD not configured in .env file" "$RED"
    exit 1
fi

print_status "✅ Configuration validated" "$GREEN"
print_status "Email: $GMAIL_EMAIL" "$BLUE"
print_status "Browser: ${BROWSER:-chromium}" "$BLUE"
print_status "Headless: ${HEADLESS:-False}" "$BLUE"

# Create reports directory
print_header "Creating Reports Directory"

mkdir -p reports/screenshots reports/videos
print_status "✅ Reports directory created" "$GREEN"

# Display test execution options
print_header "Test Execution Options"

echo ""
print_status "Select test execution option:" "$YELLOW"
echo "1) Run all tests"
echo "2) Run smoke tests only"
echo "3) Run login tests only"
echo "4) Run logout tests only"
echo "5) Run DOM validation tests only"
echo "6) Run E2E tests only"
echo "7) Run tests with specific browser (Firefox/Webkit)"
echo "8) Run tests in headless mode"
echo "9) Exit"
echo ""

read -p "Enter your choice (1-9): " choice

case $choice in
    1)
        print_header "Running All Tests"
        pytest -v --html=reports/report.html --self-contained-html
        ;;
    2)
        print_header "Running Smoke Tests"
        pytest -v -m smoke --html=reports/smoke_report.html --self-contained-html
        ;;
    3)
        print_header "Running Login Tests"
        pytest -v -m login --html=reports/login_report.html --self-contained-html
        ;;
    4)
        print_header "Running Logout Tests"
        pytest -v -m logout --html=reports/logout_report.html --self-contained-html
        ;;
    5)
        print_header "Running DOM Validation Tests"
        pytest -v -m dom --html=reports/dom_report.html --self-contained-html
        ;;
    6)
        print_header "Running E2E Tests"
        pytest -v -m e2e --html=reports/e2e_report.html --self-contained-html
        ;;
    7)
        echo ""
        echo "Select browser:"
        echo "1) Firefox"
        echo "2) Webkit (Safari)"
        read -p "Enter choice (1-2): " browser_choice
        
        case $browser_choice in
            1)
                print_header "Installing and Running with Firefox"
                playwright install firefox
                pytest -v --browser firefox --html=reports/firefox_report.html --self-contained-html
                ;;
            2)
                print_header "Installing and Running with Webkit"
                playwright install webkit
                pytest -v --browser webkit --html=reports/webkit_report.html --self-contained-html
                ;;
            *)
                print_status "Invalid choice" "$RED"
                exit 1
                ;;
        esac
        ;;
    8)
        print_header "Running Tests in Headless Mode"
        pytest -v --headed=false --html=reports/headless_report.html --self-contained-html
        ;;
    9)
        print_status "Exiting..." "$BLUE"
        exit 0
        ;;
    *)
        print_status "Invalid choice" "$RED"
        exit 1
        ;;
esac

# Capture exit code
EXIT_CODE=$?

echo ""
print_header "Test Execution Summary"

if [ $EXIT_CODE -eq 0 ]; then
    print_status "✅ All tests passed successfully!" "$GREEN"
else
    print_status "❌ Some tests failed. Please check the report for details." "$RED"
fi

echo ""
print_status "📊 HTML Report: reports/report.html" "$BLUE"
print_status "📸 Screenshots: reports/screenshots/" "$BLUE"
print_status "🎥 Videos: reports/videos/" "$BLUE"
print_status "📝 Logs: reports/test_execution.log" "$BLUE"

echo ""
print_status "To view the HTML report, open it in a browser:" "$YELLOW"
print_status "  open reports/report.html    (macOS)" "$BLUE"
print_status "  xdg-open reports/report.html    (Linux)" "$BLUE"
print_status "  start reports/report.html    (Windows)" "$BLUE"

echo ""
print_header "Execution Complete"

exit $EXIT_CODE
