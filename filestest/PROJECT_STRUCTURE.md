# Project Structure

## Complete File Tree

```
gmail-playwright-automation/
├── config/                          # Configuration and locators
│   ├── __init__.py                 # Package init
│   ├── config.py                   # Environment configuration
│   └── locators.py                 # DOM element selectors
│
├── pages/                           # Page Object Model
│   ├── __init__.py                 # Package init
│   ├── base_page.py                # Base page with common methods
│   ├── login_page.py               # Gmail login page object
│   ├── inbox_page.py               # Gmail inbox page object
│   └── logout_page.py              # Gmail logout page object
│
├── tests/                           # Test suites
│   ├── __init__.py                 # Package init
│   ├── test_login.py               # Login tests (15 tests)
│   ├── test_logout.py              # Logout tests (13 tests)
│   └── test_e2e_flow.py            # End-to-end tests (3 tests)
│
├── .github/                         # GitHub Actions
│   └── workflows/
│       └── playwright-tests-uv.yml # CI/CD workflow with UV
│
├── reports/                         # Generated reports (gitignored)
│   ├── screenshots/                # Failure screenshots
│   ├── videos/                     # Test execution videos
│   ├── report.html                 # HTML test report
│   └── test_execution.log          # Detailed logs
│
├── .venv/                          # Virtual environment (gitignored)
│
├── conftest.py                     # Pytest fixtures and configuration
├── pyproject.toml                  # UV project configuration
├── Makefile                        # Convenient command shortcuts
├── setup.sh                        # Automated setup script
├── run_tests.sh                    # Interactive test runner
├── .env.example                    # Environment variables template
├── .env                            # Actual environment variables (gitignored)
├── .gitignore                      # Git ignore patterns
├── .python-version                 # Python version for UV
├── uv.lock                         # UV lock file (auto-generated)
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
└── PROJECT_STRUCTURE.md            # This file
```

## File Descriptions

### Configuration Files

**config/config.py**
- Loads environment variables from .env
- Provides Config class with all settings
- Validates required configuration
- Creates necessary directories

**config/locators.py**
- Contains all DOM element selectors
- Organized by page (LoginPageLocators, InboxPageLocators, etc.)
- Uses CSS selectors and XPath expressions
- Includes fallback selectors for reliability

### Page Objects

**pages/base_page.py**
- Base class for all page objects
- Common methods: click, fill, wait, assert, etc.
- Navigation and validation utilities
- Screenshot and logging support

**pages/login_page.py**
- Gmail login page interactions
- Email and password input methods
- Complete login flow
- DOM element validations (15+ validations)

**pages/inbox_page.py**
- Gmail inbox page interactions
- Logout functionality
- Inbox element validations (20+ validations)
- Navigation menu handling

**pages/logout_page.py**
- Logout page validations
- Account selection page checks
- Success verification

### Test Files

**tests/test_login.py**
- 15 test cases for login functionality
- DOM element validation tests
- Invalid input handling
- Edge case testing

**tests/test_logout.py**
- 13 test cases for logout functionality
- Account menu validation
- Sign out process verification
- Comprehensive DOM checks

**tests/test_e2e_flow.py**
- 3 end-to-end test scenarios
- Complete login-logout cycles
- DOM persistence checks
- Session timeout simulation

### Project Configuration

**pyproject.toml**
- UV package manager configuration
- Project metadata and dependencies
- Pytest configuration
- Tool settings (black, isort, mypy)

**conftest.py**
- Pytest fixtures (page, authenticated_page, config)
- Browser configuration
- Screenshot on failure hook
- Test environment setup

**Makefile**
- 25+ convenient commands
- Test execution shortcuts
- Package management helpers
- Reporting and cleanup utilities

### Setup Scripts

**setup.sh**
- Installs UV package manager
- Creates virtual environment
- Syncs all dependencies
- Installs Playwright browsers
- Configures environment

**run_tests.sh**
- Interactive test runner menu
- Multiple test execution options
- Browser selection
- Headless/headed mode toggle

### Environment Files

**.env.example**
- Template for environment variables
- Gmail credentials placeholders
- Browser configuration
- Timeout settings

**.env** (not in repo)
- Actual credentials and settings
- Must be created from .env.example
- Never committed to version control

## File Statistics

- **Total Python Files**: 13
- **Total Lines of Code**: ~3,500+
- **Test Cases**: 31+
- **Page Objects**: 4
- **DOM Validations**: 50+
- **Configuration Files**: 3
- **Documentation Files**: 3

## Key Features by File

### Most Important Files

1. **pyproject.toml** - Project heart, defines all dependencies
2. **conftest.py** - Pytest magic, fixtures and hooks
3. **pages/base_page.py** - Reusable page methods
4. **tests/test_e2e_flow.py** - Complete user journey tests
5. **setup.sh** - One-command setup

### Files You'll Edit Most

1. **.env** - Your test credentials
2. **config/locators.py** - When Gmail UI changes
3. **tests/test_*.py** - Adding new test cases
4. **pages/*_page.py** - Adding new page interactions

### Files You Won't Touch

1. **conftest.py** - Works as-is
2. **.gitignore** - Comprehensive coverage
3. **Makefile** - All commands included
4. **uv.lock** - Auto-generated by UV

## How Files Interact

```
User runs: make test-smoke
    ↓
Makefile → uv run pytest -v -m smoke
    ↓
pytest.ini (in pyproject.toml) → Configuration loaded
    ↓
conftest.py → Fixtures created (browser, page, config)
    ↓
test_login.py → Uses LoginPage and InboxPage
    ↓
login_page.py → Uses locators from locators.py
    ↓
base_page.py → Common methods executed
    ↓
Reports generated → reports/report.html
```

## Import Structure

```python
# In test files
from pages.login_page import LoginPage
from pages.inbox_page import InboxPage
from config.config import Config

# In page objects
from pages.base_page import BasePage
from config.locators import LoginPageLocators

# In base_page
from playwright.sync_api import Page, expect
```

## Getting Started Checklist

- [ ] Clone repository
- [ ] Run `./setup.sh`
- [ ] Edit `.env` with credentials
- [ ] Run `make test-smoke`
- [ ] View `reports/report.html`

That's the complete structure! All files are present and ready to use. 🎉
