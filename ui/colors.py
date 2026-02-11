"""Color scheme inspired by modern crypto wallets."""

from typing import Dict

from theme_manager import theme_manager

# Initialize theme manager (safe to call multiple times)
try:
    theme_manager.initialize()
except Exception:
    pass  # Will use default values below if theme loading fails

# Get initial theme
_theme = theme_manager.get_current_theme()

# Dark theme colors (primary)
DARK_BG: str = _theme.get("dark_bg", "#0F0F1E")
DARK_BG_SECONDARY: str = _theme.get("dark_bg_secondary", "#1A1A2E")
DARK_BG_TERTIARY: str = _theme.get("dark_bg_tertiary", "#252541")

# Accent colors
ACCENT_PURPLE: str = _theme.get("accent_purple", "#9D4EDD")
ACCENT_BLUE: str = _theme.get("accent_blue", "#4CC9F0")
ACCENT_GREEN: str = _theme.get("accent_green", "#06FFA5")
ACCENT_RED: str = _theme.get("accent_red", "#FF4D6D")

# Text colors
TEXT_PRIMARY: str = _theme.get("text_primary", "#FFFFFF")
TEXT_SECONDARY: str = _theme.get("text_secondary", "#A0A0C0")
TEXT_MUTED: str = _theme.get("text_muted", "#6B6B8F")

# Gradient colors for cards
GRADIENT_START: str = _theme.get("gradient_start", "#7209B7")
GRADIENT_END: str = _theme.get("gradient_end", "#560BAD")

# Status colors
SUCCESS: str = _theme.get("success", "#06FFA5")
ERROR: str = _theme.get("error", "#FF4D6D")
WARNING: str = _theme.get("warning", "#FFB703")
INFO: str = _theme.get("info", "#4CC9F0")

# Categories colors
CATEGORY_COLORS: Dict[str, str] = _theme.get(
    "categories",
    {
        "Food": "#FF6B6B",
        "Transport": "#4ECDC4",
        "Shopping": "#FFD93D",
        "Entertainment": "#A8DADC",
        "Bills": "#6C63FF",
        "Health": "#FF8FA3",
        "Education": "#74B9FF",
        "Salary": "#06FFA5",
        "Investment": "#9D4EDD",
        "Other": "#95A5A6",
    },
)


def reload_colors() -> None:
    """Reload colors from current theme. Call after theme switch."""
    import sys

    # Get current module
    current_module = sys.modules[__name__]

    _theme = theme_manager.get_current_theme()

    # Update all color constants in the module
    setattr(current_module, "DARK_BG", _theme.get("dark_bg", "#0F0F1E"))
    setattr(
        current_module,
        "DARK_BG_SECONDARY",
        _theme.get("dark_bg_secondary", "#1A1A2E"),
    )
    setattr(
        current_module,
        "DARK_BG_TERTIARY",
        _theme.get("dark_bg_tertiary", "#252541"),
    )

    setattr(
        current_module, "ACCENT_PURPLE", _theme.get("accent_purple", "#9D4EDD")
    )
    setattr(
        current_module, "ACCENT_BLUE", _theme.get("accent_blue", "#4CC9F0")
    )
    setattr(
        current_module, "ACCENT_GREEN", _theme.get("accent_green", "#06FFA5")
    )
    setattr(current_module, "ACCENT_RED", _theme.get("accent_red", "#FF4D6D"))

    setattr(
        current_module, "TEXT_PRIMARY", _theme.get("text_primary", "#FFFFFF")
    )
    setattr(
        current_module,
        "TEXT_SECONDARY",
        _theme.get("text_secondary", "#A0A0C0"),
    )
    setattr(current_module, "TEXT_MUTED", _theme.get("text_muted", "#6B6B8F"))

    setattr(
        current_module,
        "GRADIENT_START",
        _theme.get("gradient_start", "#7209B7"),
    )
    setattr(
        current_module, "GRADIENT_END", _theme.get("gradient_end", "#560BAD")
    )

    setattr(current_module, "SUCCESS", _theme.get("success", "#06FFA5"))
    setattr(current_module, "ERROR", _theme.get("error", "#FF4D6D"))
    setattr(current_module, "WARNING", _theme.get("warning", "#FFB703"))
    setattr(current_module, "INFO", _theme.get("info", "#4CC9F0"))

    setattr(
        current_module, "CATEGORY_COLORS", dict(_theme.get("categories", {}))
    )
