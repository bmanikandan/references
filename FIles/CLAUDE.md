# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyQuantum is a Python project configured to use Python 3.13. This appears to be a newly initialized project with minimal setup.

## Development Environment

- **Python Version**: 3.13.2
- **Virtual Environment**: Located at `.venv/`
- **IDE**: PyCharm (configuration files in `.idea/`)

## Common Commands

### Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install packages
pip install <package_name>

# List installed packages
pip list
```

### Development Workflow
Since this is a new project, standard Python development commands will apply:

```bash
# Run Python files
python <filename>.py

# Install development dependencies (when requirements files are added)
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if separate dev requirements exist
```

## Project Structure

Currently minimal structure:
- `.venv/` - Virtual environment
- `.idea/` - PyCharm IDE configuration
- Root directory ready for Python source files

## Notes for Future Development

- No existing source code structure yet - follow Python best practices when creating modules
- No testing framework configured yet - consider adding pytest when tests are needed
- No linting/formatting tools configured yet - consider adding black, flake8, or ruff
- No CI/CD pipeline configured
- Project is not yet a Git repository