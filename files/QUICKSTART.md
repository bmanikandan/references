# Quick Start Guide - Gmail Playwright Automation with UV

## 🚀 Get Started in 3 Minutes

### Step 1: Setup (2 minutes)

```bash
# Run the automated setup script
./setup.sh
```

This installs UV, creates virtual environment, and installs all dependencies.

### Step 2: Configure (30 seconds)

```bash
# Edit .env file with your test Gmail credentials
nano .env
```

Update these fields:
```bash
GMAIL_EMAIL=your_test_email@gmail.com
GMAIL_PASSWORD=your_test_password
```

### Step 3: Run Tests (30 seconds)

```bash
# Option A: Interactive menu
./run_tests.sh

# Option B: Makefile
make test-smoke

# Option C: UV directly
uv run pytest -v -m smoke
```

That's it! 🎉

---

## 📋 Common Commands

### Using Makefile (Easiest)

```bash
make test              # Run all tests
make test-smoke        # Run smoke tests only
make test-login        # Run login tests
make test-logout       # Run logout tests
make test-dom          # Run DOM validations
make test-parallel     # Run in parallel
make reports           # Open HTML report
make help              # Show all commands
```

### Using UV Directly

```bash
# Activate virtual environment
source .venv/bin/activate

# Run tests
uv run pytest -v                    # All tests
uv run pytest -v -m smoke           # Smoke tests
uv run pytest -v -m login           # Login tests
uv run pytest -v --headed=false     # Headless mode
uv run pytest -v -n 4               # Parallel (4 workers)
```

### Managing Packages

```bash
uv add package-name        # Add new package
uv remove package-name     # Remove package
uv sync                    # Sync dependencies
uv pip list                # List packages
```

---

## 📊 View Reports

After running tests:

```bash
# Open HTML report
make reports

# Or manually
open reports/report.html      # macOS
xdg-open reports/report.html  # Linux
```

Reports include:
- ✅ Test results
- 📸 Screenshots (on failure)
- 🎥 Videos
- 📝 Detailed logs

---

## 🔧 Troubleshooting

### UV not found?
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
```

### Tests failing?
1. Check `.env` file has valid credentials
2. View logs: `cat reports/test_execution.log`
3. Check screenshots: `ls reports/screenshots/`
4. Ensure Gmail account has no 2FA (use App Password if needed)

### Need to reinstall?
```bash
make clean
./setup.sh
```

---

## 💡 Tips

1. **Use test Gmail account** - Never use personal account
2. **Check reports first** - HTML reports show detailed failures
3. **Run smoke tests** - Quick validation before full suite
4. **Use headless mode** - Faster execution in CI/CD
5. **Parallel execution** - Speed up tests with `-n 4`

---

## 📚 Next Steps

- Read full [README.md](README.md) for detailed documentation
- Explore test files in `tests/` directory
- Customize page objects in `pages/` directory
- Add new locators in `config/locators.py`
- Check [UV documentation](https://github.com/astral-sh/uv) for advanced usage

---

**Questions?** Check the main README or examine the code - it's well documented! 📖
