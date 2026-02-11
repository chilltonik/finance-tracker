# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal Finance Tracker - a desktop application for tracking personal finances with a modern UI inspired by crypto wallets. Built with Python and CustomTkinter.

**Key Features:**
- Multiple color themes (5 presets: Default, Ocean Breeze, Sunset Glow, Forest Green, Midnight Blue)
- Theme persistence via TOML configuration files
- Dynamic theme switching without application restart

## Development Setup

### Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Application
```bash
# Method 1: Run via entry point script
python main.py

# Method 2: Run as Python module
python -m finance_tracker
```

## Code Quality

### Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### Run Code Quality Checks
```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run ruff linter only
ruff check .

# Run ruff formatter
ruff format .

# Run mypy type checker
mypy .
```

### Pre-commit Hooks
Pre-commit is configured with:
- **ruff**: Linting and import sorting (auto-fix enabled)
- **ruff-format**: Code formatting
- **mypy**: Static type checking

Install pre-commit hooks:
```bash
pre-commit install
```

## Project Structure

```
finance_tracker/  (project root)
├── finance_tracker/         # Main application package
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Module entry point (python -m finance_tracker)
│   ├── app.py               # Main application UI logic
│   ├── database.py          # SQLite database operations and queries
│   ├── theme_manager.py     # Theme loading, switching, and persistence
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── colors.py        # Dynamic color loading from themes
│   │   └── widgets.py       # Custom UI widgets (cards, buttons, etc.)
│   └── config/
│       ├── __init__.py
│       ├── themes.toml      # Theme definitions (5 presets)
│       └── settings.toml    # User preferences (selected theme)
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_themes.py
│   └── test_ui_refresh.py
├── data/                    # SQLite database storage (auto-created)
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
├── main.py                  # Simple entry point script
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
└── pyproject.toml           # Project configuration
```

## Architecture

### Database Layer (`finance_tracker/database.py`)
- Single `Database` class handles all SQLite operations
- Two main tables: `transactions` and `balance_history`
- All transactions tracked with type (income/expense), category, amount, description, and timestamp
- Statistics calculated on-the-fly from transaction data

### Theme System
- **finance_tracker/theme_manager.py**: Singleton `ThemeManager` class
  - Loads themes from `finance_tracker/config/themes.toml` using tomllib
  - Manages current theme selection
  - Saves user preference to `finance_tracker/config/settings.toml` using tomli-w
  - Provides theme switching API
  - Paths automatically resolved relative to package directory
- **finance_tracker/ui/colors.py**: Dynamic color module
  - Initializes from current theme on import
  - Provides `reload_colors()` function to update after theme switch
  - All color constants remain as module-level variables for compatibility

### UI Layer
- **finance_tracker/app.py**: Contains `FinanceTrackerApp` class (main CTk window) with four views:
  - Dashboard: Shows balance card, statistics, and recent transactions
  - Add Transaction: Form for adding new income/expense entries
  - History: Scrollable list of all transactions
  - Settings: Theme selector with preview and apply button
- **finance_tracker/ui/colors.py**: Centralized color definitions in crypto wallet dark theme style
- **finance_tracker/ui/widgets.py**: Reusable components:
  - `BalanceCard`: Large balance display card
  - `StatCard`: Statistics display cards
  - `TransactionItem`: Individual transaction row
  - `ModernButton`: Styled button component
  - `GradientFrame`: Styled container frame

### Entry Points
- **main.py**: Simple entry point that imports from the package
- **finance_tracker/__main__.py**: Allows running as module with `python -m finance_tracker`

### Design Patterns
- **Package-based structure**: All application code in `finance_tracker/` package
- **Absolute imports**: All imports use full package path (e.g., `from finance_tracker.ui.colors import ...`)
- Color constants defined in `finance_tracker/ui/colors.py` and imported throughout
- Database operations separated from UI logic
- Reusable widget components for consistent styling
- Transaction data passed as dictionaries between layers

### Key Dependencies
- **customtkinter**: Modern themed Tkinter widgets
- **sqlite3**: Built-in Python database (no external DB needed)
- **PIL/Pillow**: Image handling for CustomTkinter
- **matplotlib**: For future chart/graph features

## Development Conventions

- Dark theme with purple/blue accent colors matching crypto wallet aesthetic
- All amounts stored and displayed as floats with 2 decimal precision
- Categories predefined in `CATEGORY_COLORS` dict in `colors.py`
- Transaction types: "income" or "expense" (lowercase strings)
- Database path: `data/finance_tracker.db` (relative to project root)

## Adding Features

### New Transaction Category
1. Add color to `CATEGORY_COLORS` in `finance_tracker/ui/colors.py`
2. Category will auto-appear in dropdown

### New View/Page
1. Add navigation button in `_setup_ui()` sidebar in `finance_tracker/app.py`
2. Create `show_*()` method in `FinanceTrackerApp`
3. Call `_clear_content()` first to remove old view

### Database Schema Changes
1. Modify `init_database()` in `finance_tracker/database.py`
2. Add new query methods as needed
3. Database auto-creates on first run (no migrations needed for SQLite)

### Import Convention
When adding new modules, always use absolute imports with the full package path:
```python
# Correct
from finance_tracker.database import Database
from finance_tracker.ui.colors import ACCENT_PURPLE

# Incorrect (do not use relative imports at package level)
from .database import Database
from ..ui.colors import ACCENT_PURPLE
```
