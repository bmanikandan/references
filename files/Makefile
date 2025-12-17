.PHONY: help setup install test test-smoke test-login test-logout test-dom test-e2e test-parallel clean reports

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Gmail Playwright Test Automation with UV"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install UV and setup environment
	@echo "Setting up environment with UV..."
	@./setup.sh

install: ## Sync dependencies with UV
	@echo "Syncing dependencies..."
	@uv sync
	@.venv/bin/playwright install chromium

test: ## Run all tests
	@echo "Running all tests..."
	@uv run pytest -v --html=reports/report.html --self-contained-html

test-smoke: ## Run smoke tests only
	@echo "Running smoke tests..."
	@uv run pytest -v -m smoke --html=reports/smoke_report.html --self-contained-html

test-login: ## Run login tests only
	@echo "Running login tests..."
	@uv run pytest -v -m login --html=reports/login_report.html --self-contained-html

test-logout: ## Run logout tests only
	@echo "Running logout tests..."
	@uv run pytest -v -m logout --html=reports/logout_report.html --self-contained-html

test-dom: ## Run DOM validation tests
	@echo "Running DOM validation tests..."
	@uv run pytest -v -m dom --html=reports/dom_report.html --self-contained-html

test-e2e: ## Run E2E tests
	@echo "Running E2E tests..."
	@uv run pytest -v -m e2e --html=reports/e2e_report.html --self-contained-html

test-parallel: ## Run tests in parallel (4 workers)
	@echo "Running tests in parallel..."
	@uv run pytest -v -n 4 --html=reports/parallel_report.html --self-contained-html

test-headless: ## Run tests in headless mode
	@echo "Running tests in headless mode..."
	@uv run pytest -v --headed=false --html=reports/headless_report.html --self-contained-html

test-firefox: ## Run tests with Firefox
	@echo "Running tests with Firefox..."
	@.venv/bin/playwright install firefox
	@uv run pytest -v --browser firefox --html=reports/firefox_report.html --self-contained-html

test-webkit: ## Run tests with Webkit
	@echo "Running tests with Webkit..."
	@.venv/bin/playwright install webkit
	@uv run pytest -v --browser webkit --html=reports/webkit_report.html --self-contained-html

coverage: ## Run tests with coverage report
	@echo "Running tests with coverage..."
	@uv add pytest-cov
	@uv run pytest --cov=pages --cov=config --cov-report=html:reports/coverage --cov-report=term

lint: ## Run code linting
	@echo "Running linters..."
	@uv run black --check .
	@uv run flake8 .
	@uv run isort --check-only .

format: ## Format code with black and isort
	@echo "Formatting code..."
	@uv run black .
	@uv run isort .

clean: ## Clean up generated files
	@echo "Cleaning up..."
	@rm -rf reports/*.html
	@rm -rf reports/screenshots/*
	@rm -rf reports/videos/*
	@rm -rf .pytest_cache
	@rm -rf __pycache__
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"

reports: ## Open HTML report in browser
	@echo "Opening test report..."
	@if [ -f reports/report.html ]; then \
		if command -v open &> /dev/null; then \
			open reports/report.html; \
		elif command -v xdg-open &> /dev/null; then \
			xdg-open reports/report.html; \
		else \
			echo "Please open reports/report.html manually"; \
		fi \
	else \
		echo "No report found. Run 'make test' first."; \
	fi

venv: ## Create virtual environment with UV
	@echo "Creating virtual environment..."
	@uv venv

lock: ## Update lock file
	@echo "Updating lock file..."
	@uv lock

add: ## Add a package (usage: make add PACKAGE=package-name)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Usage: make add PACKAGE=package-name"; \
		exit 1; \
	fi
	@echo "Adding package: $(PACKAGE)"
	@uv add $(PACKAGE)

remove: ## Remove a package (usage: make remove PACKAGE=package-name)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Usage: make remove PACKAGE=package-name"; \
		exit 1; \
	fi
	@echo "Removing package: $(PACKAGE)"
	@uv remove $(PACKAGE)

list: ## List installed packages
	@echo "Installed packages:"
	@uv pip list

info: ## Show UV and environment information
	@echo "UV Version:"
	@uv --version
	@echo ""
	@echo "Python Version:"
	@.venv/bin/python --version
	@echo ""
	@echo "Installed Packages:"
	@uv pip list
