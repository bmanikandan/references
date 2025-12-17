#!/bin/bash

# Gmail Playwright Test Runner with UV Package Manager

set -e  # Exit on error

echo "=========================================="
echo "Gmail Playwright Test Runner (UV)"
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
if ! command -v uv &> /dev/null; then
    print_status "❌ UV is not installed. Please run ./setup.sh first." "$RED"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    print_status "❌ Virtual environment not found. Please run ./setup.sh first." "$RED"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    print_status "❌ .env file not found. Please create it from .env.example" "$RED"
    exit 1
fi

# Source environment variables
source .env

# Validate configuration
print_header "Validating Configuration"

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
mkdir -p reports/screenshots reports/videos

# Display test execution options
print_header "Test Execution Options"

echo ""
print_status "Select test execution option:" "$YELLOW"
echo "1)  Run all tests"
echo "2)  Run smoke tests only"
echo "3)  Run login tests only"
echo "4)  Run logout tests only"
echo "5)  Run DOM validation tests only"
echo "6)  Run E2E tests only"
echo "7)  Run tests with Firefox"
echo "8)  Run tests with Webkit (Safari)"
echo "9)  Run tests in headless mode"
echo "10) Run tests in parallel (4 workers)"
echo "11) Run specific test file"
echo "12) Generate coverage report"
echo "13) Exit"
echo ""

read -p "Enter your choice (1-13): " choice

case $choice in
    1)
        print_header "Running All Tests with UV"
        uv run pytest -v --html=reports/report.html --self-contained-html
        ;;
    2)
        print_header "Running Smoke Tests"
        uv run pytest -v -m smoke --html=reports/smoke_report.html --self-contained-html
        ;;
    3)
        print_header "Running Login Tests"
        uv run pytest -v -m login --html=reports/login_report.html --self-contained-html
        ;;
    4)
        print_header "Running Logout Tests"
        uv run pytest -v -m logout --html=reports/logout_report.html --self-contained-html
        ;;
    5)
        print_header "Running DOM Validation Tests"
        uv run pytest -v -m dom --html=reports/dom_report.html --self-contained-html
        ;;
    6)
        print_header "Running E2E Tests"
        uv run pytest -v -m e2e --html=reports/e2e_report.html --self-contained-html
        ;;
    7)
        print_header "Installing and Running with Firefox"
        .venv/bin/playwright install firefox
        uv run pytest -v --browser firefox --html=reports/firefox_report.html --self-contained-html
        ;;
    8)
        print_header "Installing and Running with Webkit"
        .venv/bin/playwright install webkit
        uv run pytest -v --browser webkit --html=reports/webkit_report.html --self-contained-html
        ;;
    9)
        print_header "Running Tests in Headless Mode"
        uv run pytest -v --headed=false --html=reports/headless_report.html --self-contained-html
        ;;
    10)
        print_header "Running Tests in Parallel (4 workers)"
        uv run pytest -v -n 4 --html=reports/parallel_report.html --self-contained-html
        ;;
    11)
        echo ""
        print_status "Available test files:" "$CYAN"
        echo "1) test_login.py"
        echo "2) test_logout.py"
        echo "3) test_e2e_flow.py"
        read -p "Enter test file number (1-3): " file_choice
        
        case $file_choice in
            1)
                print_header "Running Login Tests"
                uv run pytest -v tests/test_login.py --html=reports/login_specific.html --self-contained-html
                ;;
            2)
                print_header "Running Logout Tests"
                uv run pytest -v tests/test_logout.py --html=reports/logout_specific.html --self-contained-html
                ;;
            3)
                print_header "Running E2E Tests"
                uv run pytest -v tests/test_e2e_flow.py --html=reports/e2e_specific.html --self-contained-html
                ;;
            *)
                print_status "Invalid choice" "$RED"
                exit 1
                ;;
        esac
        ;;
    12)
        print_header "Generating Coverage Report"
        print_status "Installing coverage package..." "$BLUE"
        uv add pytest-cov
        uv run pytest --cov=pages --cov=config --cov-report=html:reports/coverage --cov-report=term
        print_status "Coverage report generated in reports/coverage/index.html" "$GREEN"
        ;;
    13)
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
print_status "📊 Test Reports:" "$CYAN"
print_status "  HTML Report: reports/report.html" "$BLUE"
print_status "  Screenshots: reports/screenshots/" "$BLUE"
print_status "  Videos: reports/videos/" "$BLUE"
print_status "  Logs: reports/test_execution.log" "$BLUE"

echo ""
print_status "📚 UV Commands Reference:" "$CYAN"
print_status "  uv run pytest -v                    # Run all tests" "$BLUE"
print_status "  uv run pytest -v -m smoke           # Run smoke tests" "$BLUE"
print_status "  uv run pytest -v --headed=false     # Run headless" "$BLUE"
print_status "  uv run pytest -v -n 4               # Run parallel" "$BLUE"
print_status "  uv run pytest tests/test_login.py   # Run specific file" "$BLUE"

echo ""
print_status "To view the HTML report, open it in a browser:" "$YELLOW"
print_status "  open reports/report.html           (macOS)" "$BLUE"
print_status "  xdg-open reports/report.html       (Linux)" "$BLUE"
print_status "  start reports/report.html          (Windows)" "$BLUE"

echo ""
print_header "Execution Complete"

exit $EXIT_CODE
