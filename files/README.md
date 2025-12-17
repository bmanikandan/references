# Gmail Web Automation Testing with Python Playwright & UV

A comprehensive web automation testing framework for Gmail login and logout functionality using Python Playwright with extensive DOM element validations, Pytest, and **UV package manager** for blazing-fast dependency management.

## 🚀 Why UV?

This project uses [UV](https://github.com/astral-sh/uv) - a next-generation Python package manager:

- ⚡ **10-100x faster** than pip
- 🔒 **Reliable dependency resolution** with lock files
- 🦀 **Written in Rust** for maximum performance
- 🎯 **Built-in virtual environment** management
- 📦 **Compatible with pip** and standard Python packaging

## 🎯 Features

- **Page Object Model (POM)** architecture for maintainable tests
- **Comprehensive DOM Validations** for all page elements
- **UV Package Manager** for fast dependency management
- **Pytest** integration with custom fixtures and markers
- **Detailed Logging** with screenshots on failure
- **HTML Reports** for test execution results
- **Video Recording** of test sessions
- **Multiple Test Suites**: Smoke, Regression, E2E
- **Parallel Test Execution** support
- **CI/CD Ready** configuration
- **Makefile** for convenient command execution

## 📋 Prerequisites

- Python 3.8+ (UV can install Python for you)
- Gmail test account (DO NOT use personal account)
- Internet connection
- curl (for UV installation)

## 📁 Project Structure

```
.
├── config/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   └── locators.py         # DOM element locators
├── pages/
│   ├── __init__.py
│   ├── base_page.py        # Base page with common methods
│   ├── login_page.py       # Login page object
│   ├── inbox_page.py       # Inbox page object
│   └── logout_page.py      # Logout page object
├── tests/
│   ├── __init__.py
│   ├── test_login.py       # Login test cases
│   ├── test_logout.py      # Logout test cases
│   └── test_e2e_flow.py    # End-to-end tests
├── reports/                # Test reports, screenshots, videos
├── conftest.py             # Pytest fixtures and hooks
├── pyproject.toml          # UV project configuration
├── .python-version         # Python version specification
├── Makefile                # Convenient command shortcuts
├── setup.sh                # Setup script with UV
├── run_tests.sh            # Test runner script
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository (if applicable)
git clone <your-repo-url>
cd gmail-playwright-automation

# Run automated setup (installs UV, creates venv, installs dependencies)
./setup.sh
```

The setup script will:
- Install UV if not present
- Create Python virtual environment
- Sync all dependencies
- Install Playwright browsers
- Create .env file from template

### 2. Configure Environment

```bash
# Edit .env with your test Gmail credentials
nano .env
```

**.env Configuration:**
```bash
GMAIL_EMAIL=your_test_email@gmail.com
GMAIL_PASSWORD=your_test_password
BROWSER=chromium
HEADLESS=False
SLOW_MO=500
```

**⚠️ IMPORTANT SECURITY NOTES:**
- Use a dedicated TEST Gmail account
- Never use your personal Gmail account
- Never commit .env file to version control
- Consider using App Passwords if 2FA is enabled

### 3. Run Tests

#### Option A: Using the run script
```bash
./run_tests.sh
# Interactive menu with multiple options
```

#### Option B: Using Makefile (Recommended)
```bash
make test              # Run all tests
make test-smoke        # Run smoke tests
make test-login        # Run login tests
make test-logout       # Run logout tests
make test-dom          # Run DOM validation tests
make test-e2e          # Run E2E tests
make test-parallel     # Run tests in parallel
make help              # Show all available commands
```

#### Option C: Using UV directly
```bash
# Activate virtual environment
source .venv/bin/activate

# Run tests with UV
uv run pytest -v
uv run pytest -v -m smoke
uv run pytest -v -m login
uv run pytest -v --headed=false
```

## 📦 UV Package Manager Commands

### Basic UV Commands

```bash
# Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Sync dependencies from pyproject.toml
uv sync

# Add a new package
uv add pytest-xdist

# Add a dev dependency
uv add --dev black

# Remove a package
uv remove package-name

# Update all dependencies
uv lock

# List installed packages
uv pip list

# Run a command in the virtual environment
uv run pytest -v

# Install specific Python version
uv python install 3.10
```

### UV vs PIP Comparison

| Task | UV | PIP |
|------|-----|-----|
| Install packages | `uv sync` | `pip install -r requirements.txt` |
| Add package | `uv add pytest` | `pip install pytest` + manual edit |
| Virtual env | `uv venv` (built-in) | `python -m venv` (separate tool) |
| Lock dependencies | `uv lock` (automatic) | Manual with pip-tools |
| Speed | ⚡ 10-100x faster | Standard |

## 🧪 Test Categories

### Smoke Tests (@pytest.mark.smoke)
```bash
make test-smoke
# OR
uv run pytest -v -m smoke
```

Critical functionality tests that should always pass:
- Basic login functionality
- Basic logout functionality
- Complete login-logout flow

### Regression Tests (@pytest.mark.regression)
```bash
uv run pytest -v -m regression
```

Comprehensive tests for edge cases and detailed validations:
- Invalid input handling
- Multiple page refreshes
- Session timeout scenarios

### DOM Validation Tests (@pytest.mark.dom)
```bash
make test-dom
# OR
uv run pytest -v -m dom
```

Tests specifically for DOM element validations:
- Email input field attributes
- Password input field attributes
- Navigation menu elements
- Inbox page elements
- Logout page elements

### End-to-End Tests (@pytest.mark.e2e)
```bash
make test-e2e
# OR
uv run pytest -v -m e2e
```

Complete user journey tests:
- Full login-logout-login cycle
- Navigation across different Gmail sections
- DOM persistence checks

## 📊 DOM Element Validations

The framework validates numerous DOM elements:

### Login Page Elements ✅
- Email input field (type, visibility, enabled state)
- Password input field (type, name attribute, visibility)
- Next buttons (presence, clickability)
- Google logo
- Privacy & Terms links
- Sign-in heading text
- Error message elements

### Inbox Page Elements ✅
- Compose button (presence, attributes, clickability)
- Gmail logo
- Search box (aria-label, visibility, enabled state)
- Navigation menu items (Inbox, Sent, Drafts, Starred)
- Profile button
- Settings button
- Main content area
- Toolbar
- Email list
- Account menu
- Sign Out button

### Logout Page Elements ✅
- Account selection page URL
- "Choose an account" heading
- Account selection buttons
- "Use another account" option

## 🛠️ Makefile Commands

```bash
make help              # Show all available commands
make setup             # Install UV and setup environment
make install           # Sync dependencies
make test              # Run all tests
make test-smoke        # Run smoke tests
make test-login        # Run login tests
make test-logout       # Run logout tests
make test-dom          # Run DOM validation tests
make test-e2e          # Run E2E tests
make test-parallel     # Run tests in parallel (4 workers)
make test-headless     # Run tests in headless mode
make test-firefox      # Run tests with Firefox
make test-webkit       # Run tests with Webkit
make coverage          # Run tests with coverage report
make lint              # Run code linting
make format            # Format code with black and isort
make clean             # Clean up generated files
make reports           # Open HTML report in browser
make list              # List installed packages
make info              # Show UV and environment information

# Add/Remove packages
make add PACKAGE=pytest-xdist
make remove PACKAGE=package-name
```

## 🔧 Configuration

### pyproject.toml

The main configuration file for UV and the project:

```toml
[project]
name = "gmail-playwright-automation"
version = "1.0.0"
requires-python = ">=3.8"

dependencies = [
    "pytest>=7.4.3",
    "pytest-playwright>=0.4.3",
    "playwright>=1.40.0",
    # ... other dependencies
]

[project.optional-dependencies]
dev = [
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]
```

### Browser Options

```bash
# Run with different browsers
uv run pytest --browser firefox
uv run pytest --browser webkit

# Headless mode
uv run pytest --headed=false

# Slow motion (for debugging)
uv run pytest --slowmo=1000

# Parallel execution
uv run pytest -n 4
```

## 📸 Screenshots and Videos

### Automatic Screenshots
- Screenshots automatically captured on test failures
- Saved to `reports/screenshots/`
- Named with test name and timestamp

### Video Recording
- Videos recorded for all test sessions
- Saved to `reports/videos/`
- Can be disabled in `.env` with `VIDEO_RECORDING=False`

## 🔍 Test Reports

### HTML Report
```bash
make test              # Generates reports/report.html
make reports           # Opens the report in browser
```

### Coverage Report
```bash
make coverage          # Generates coverage report
open reports/coverage/index.html
```

### Test Logs
- Detailed logs saved to `reports/test_execution.log`
- Console output with timestamps
- Different log levels: INFO, WARNING, ERROR

## 🐛 Debugging

### Run Single Test
```bash
uv run pytest tests/test_login.py::TestGmailLogin::test_successful_login -v
```

### Debug Mode
```bash
# Slow motion with headed browser
uv run pytest --headed --slowmo=1000

# Pause on failure
uv run pytest --pdb

# Verbose output
uv run pytest -vv
```

## 🚀 CI/CD Integration

### GitHub Actions with UV

```yaml
name: Playwright Tests with UV

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
      - name: Setup Python with UV
        run: |
          uv venv
          uv sync
      
      - name: Install Playwright browsers
        run: .venv/bin/playwright install chromium
      
      - name: Run tests
        env:
          GMAIL_EMAIL: ${{ secrets.GMAIL_EMAIL }}
          GMAIL_PASSWORD: ${{ secrets.GMAIL_PASSWORD }}
        run: uv run pytest --headed=false
      
      - name: Upload reports
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-reports
          path: reports/
```

## 📚 Best Practices

1. **Use UV for all package operations** - It's faster and more reliable
2. **Never hardcode credentials** - Always use environment variables
3. **Use test accounts** - Never use personal Gmail accounts
4. **Lock dependencies** - Run `uv lock` after adding packages
5. **Commit lock file** - Include `uv.lock` in version control
6. **Use Makefile** - Convenient shortcuts for common tasks
7. **Clean regularly** - Run `make clean` to remove old artifacts

## 🔄 Migration from pip

If you have an existing project using pip:

```bash
# UV can read requirements.txt
uv sync

# Or convert requirements.txt to pyproject.toml
uv add $(cat requirements.txt)

# UV creates a lock file automatically
uv lock
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Use UV for dependency management
4. Run tests: `make test`
5. Format code: `make format`
6. Submit a pull request

## 📄 License

This project is provided as-is for testing and educational purposes.

## ⚠️ Disclaimer

This framework is for testing purposes only. Use responsibly and in accordance with Gmail's Terms of Service. Always use test accounts, never production accounts.

## 🆘 Support

For issues:
1. Check logs in `reports/test_execution.log`
2. Review screenshots in `reports/screenshots/`
3. Verify configuration in `.env`
4. Run `make info` to check environment
5. Update locators if Gmail UI changed

## 📖 Additional Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)

## 🎉 Benefits of Using UV

1. **Speed**: Install dependencies 10-100x faster than pip
2. **Reliability**: Better dependency resolution with lock files
3. **Simplicity**: Built-in virtual environment management
4. **Compatibility**: Works with existing pip and pyproject.toml
5. **Modern**: Written in Rust, actively maintained

---

**Happy Testing with UV! ⚡🚀**
