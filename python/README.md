# Gmail Web Automation Testing with Python Playwright

A comprehensive web automation testing framework for Gmail login and logout functionality using Python Playwright with extensive DOM element validations and Pytest.

## 🎯 Features

- **Page Object Model (POM)** architecture for maintainable tests
- **Comprehensive DOM Validations** for all page elements
- **Pytest** integration with custom fixtures and markers
- **Detailed Logging** with screenshots on failure
- **HTML Reports** for test execution results
- **Video Recording** of test sessions
- **Multiple Test Suites**: Smoke, Regression, E2E
- **Parallel Test Execution** support
- **CI/CD Ready** configuration

## 📋 Prerequisites

- Python 3.8+
- Gmail test account (DO NOT use personal account)
- Internet connection

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
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

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
- Use environment-specific credentials management in CI/CD

### 3. Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run tests with specific marker
pytest -m smoke
pytest -m login
pytest -m dom

# Run in headless mode
pytest --browser chromium --headed=false

# Run with parallel execution
pytest -n 4

# Generate detailed HTML report
pytest --html=reports/detailed_report.html
```

## 🧪 Test Categories

### Smoke Tests (@pytest.mark.smoke)
Critical functionality tests that should always pass:
- Basic login functionality
- Basic logout functionality
- Complete login-logout flow

### Regression Tests (@pytest.mark.regression)
Comprehensive tests for edge cases and detailed validations:
- Invalid input handling
- Multiple page refreshes
- Session timeout scenarios

### DOM Validation Tests (@pytest.mark.dom)
Tests specifically for DOM element validations:
- Email input field attributes
- Password input field attributes
- Navigation menu elements
- Inbox page elements
- Logout page elements

### End-to-End Tests (@pytest.mark.e2e)
Complete user journey tests:
- Full login-logout-login cycle
- Navigation across different Gmail sections
- DOM persistence checks

## 📊 DOM Element Validations

The framework validates numerous DOM elements:

### Login Page Elements
- ✅ Email input field (type, visibility, enabled state)
- ✅ Password input field (type, name attribute, visibility)
- ✅ Next buttons (presence, clickability)
- ✅ Google logo
- ✅ Privacy & Terms links
- ✅ Sign-in heading text
- ✅ Error message elements

### Inbox Page Elements
- ✅ Compose button (presence, attributes, clickability)
- ✅ Gmail logo
- ✅ Search box (aria-label, visibility, enabled state)
- ✅ Navigation menu items (Inbox, Sent, Drafts, Starred)
- ✅ Profile button
- ✅ Settings button
- ✅ Main content area
- ✅ Toolbar
- ✅ Email list
- ✅ Account menu (after clicking profile)
- ✅ Sign Out button

### Logout Page Elements
- ✅ Account selection page URL
- ✅ "Choose an account" heading
- ✅ Account selection buttons
- ✅ "Use another account" option

## 🎨 Page Object Methods

### BasePage (Common Methods)
```python
# Navigation
navigate_to(url)
wait_for_url(pattern)

# Interactions
click(selector)
fill(selector, text)
type_slowly(selector, text)

# Validations
is_visible(selector)
is_enabled(selector)
assert_visible(selector)
assert_text(selector, expected_text)

# Utilities
screenshot(path)
get_text(selector)
wait_for_selector(selector)
```

### LoginPage
```python
# Actions
navigate_to_gmail()
enter_email(email)
enter_password(password)
login(email, password)

# Validations
validate_email_input_present()
validate_password_input_present()
validate_all_email_page_elements()
validate_all_password_page_elements()
```

### InboxPage
```python
# Actions
logout()
click_profile_button()
wait_for_inbox_to_load()

# Validations
validate_compose_button_present()
validate_gmail_logo_present()
validate_successfully_logged_in()
validate_all_inbox_elements()
```

### LogoutPage
```python
# Validations
validate_on_logout_page()
validate_successfully_logged_out()
validate_all_logout_page_elements()
```

## 📝 Example Test

```python
import pytest
from pages.login_page import LoginPage
from pages.inbox_page import InboxPage

@pytest.mark.smoke
def test_login_and_validate_inbox(page, config):
    # Initialize pages
    login_page = LoginPage(page)
    inbox_page = InboxPage(page)
    
    # Navigate and login
    login_page.navigate_to_gmail()
    login_page.login(config.GMAIL_EMAIL, config.GMAIL_PASSWORD)
    
    # Validate inbox loaded
    inbox_page.wait_for_inbox_to_load()
    assert inbox_page.validate_successfully_logged_in()
    
    # Validate DOM elements
    validations = inbox_page.validate_all_inbox_elements()
    assert validations["Compose Button"]
    assert validations["Gmail Logo"]
```

## 🔧 Configuration Options

### pytest.ini
```ini
[pytest]
# Markers
markers =
    smoke: Critical tests
    regression: Regression tests
    login: Login tests
    logout: Logout tests
    dom: DOM validation tests

# Options
addopts = --verbose --html=reports/report.html
```

### Browser Options
```python
# Change browser
pytest --browser firefox
pytest --browser webkit

# Headless mode
pytest --headed=false

# Slow motion (for debugging)
pytest --slowmo=1000

# Device emulation
pytest --device="iPhone 12"
```

## 📸 Screenshots and Videos

### Automatic Screenshots
- Screenshots are automatically captured on test failures
- Saved to `reports/screenshots/`
- Named with test name and timestamp

### Video Recording
- Videos recorded for all test sessions
- Saved to `reports/videos/`
- Can be disabled in `.env` with `VIDEO_RECORDING=False`

## 🔍 Test Reports

### HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Allure Report (Optional)
```bash
# Run tests with Allure
pytest --alluredir=reports/allure

# Generate report
allure serve reports/allure
```

### Test Logs
- Detailed logs saved to `reports/test_execution.log`
- Console output with timestamps
- Different log levels: INFO, WARNING, ERROR

## 🐛 Debugging

### Run Single Test
```bash
pytest tests/test_login.py::TestGmailLogin::test_successful_login -v
```

### Debug Mode
```bash
# Slow motion with headed browser
pytest --headed --slowmo=1000

# Pause on failure
pytest --pdb

# Verbose output
pytest -vv
```

### Common Issues

**Issue: "Profile button not found"**
- Gmail UI may vary slightly
- The framework uses multiple selectors as fallback
- Check screenshots in `reports/screenshots/`

**Issue: "Login timeout"**
- Check internet connection
- Verify Gmail credentials in .env
- Consider increasing timeout in config.py
- Check for 2FA - may need App Password

**Issue: "Element not found"**
- Gmail UI may have changed
- Update selectors in `config/locators.py`
- Check if element loaded with network delays

## 🚀 CI/CD Integration

### GitHub Actions Example
```yaml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      - name: Run tests
        env:
          GMAIL_EMAIL: ${{ secrets.GMAIL_EMAIL }}
          GMAIL_PASSWORD: ${{ secrets.GMAIL_PASSWORD }}
        run: pytest --headed=false
      - name: Upload reports
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-reports
          path: reports/
```

## 📚 Best Practices

1. **Never hardcode credentials** - Always use environment variables
2. **Use test accounts** - Never use personal Gmail accounts
3. **Wait for elements** - Use explicit waits instead of sleep
4. **Page Object Model** - Keep page logic separate from tests
5. **Meaningful assertions** - Use descriptive error messages
6. **Clean up** - Tests should be independent and stateless
7. **Screenshots on failure** - Already configured automatically
8. **Parallel execution** - Run tests in parallel for faster feedback

## 🤝 Contributing

1. Follow the existing code structure
2. Add new locators to `config/locators.py`
3. Create page objects for new pages
4. Write comprehensive tests with DOM validations
5. Update documentation

## 📄 License

This project is provided as-is for testing and educational purposes.

## ⚠️ Disclaimer

This framework is for testing purposes only. Use responsibly and in accordance with Gmail's Terms of Service. Always use test accounts, never production accounts.

## 🆘 Support

For issues:
1. Check logs in `reports/test_execution.log`
2. Review screenshots in `reports/screenshots/`
3. Verify configuration in `.env`
4. Update locators if Gmail UI changed

## 🔮 Future Enhancements

- [ ] Support for 2FA authentication
- [ ] Email composition tests
- [ ] Search functionality tests
- [ ] Filter and label tests
- [ ] Mobile responsive tests
- [ ] Performance testing
- [ ] Accessibility testing (WCAG compliance)
- [ ] Cross-browser testing (Firefox, Safari)
