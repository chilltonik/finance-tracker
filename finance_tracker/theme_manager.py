"""Theme management for the Finance Tracker application."""

import logging
import re
import tomllib
from pathlib import Path
from typing import Any, Dict, List

try:
    import tomli_w
except ImportError:
    raise ImportError(
        "tomli_w required for writing TOML files. Install: pip install tomli-w"
    )

logger = logging.getLogger(__name__)


class ThemeManager:
    """Manage application color themes."""

    _instance: "ThemeManager | None" = None
    _initialized: bool = False

    def __new__(cls) -> "ThemeManager":
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize theme manager."""
        if not ThemeManager._initialized:
            self.themes: Dict[str, Dict[str, Any]] = {}
            self.current_theme_key: str = "default"
            # Get the package directory
            package_dir = Path(__file__).parent
            self.themes_path: Path = package_dir / "config" / "themes.toml"
            self.settings_path: Path = package_dir / "config" / "settings.toml"
            ThemeManager._initialized = True

    def initialize(self) -> None:
        """Load themes and user settings."""
        self._load_themes()
        self._load_settings()

    def _load_themes(self) -> None:
        """Load theme definitions from TOML file."""
        if not self.themes_path.exists():
            raise FileNotFoundError(
                f"Themes file not found: {self.themes_path}"
            )

        with open(self.themes_path, "rb") as f:
            data = tomllib.load(f)

        # Extract themes
        if "theme" not in data:
            raise ValueError("No themes defined in themes.toml")

        self.themes = data["theme"]

        # Validate required default theme exists
        if "default" not in self.themes:
            raise ValueError(
                "FATAL: Required 'default' theme not found in themes.toml. "
                "At least one theme named 'default' must exist."
            )

    def _load_settings(self) -> None:
        """Load user settings from TOML file."""
        if not self.settings_path.exists():
            # Create default settings file
            self._save_settings({"appearance": {"theme": "default"}})
            self.current_theme_key = "default"
            return

        with open(self.settings_path, "rb") as f:
            settings = tomllib.load(f)

        theme_key = settings.get("appearance", {}).get("theme", "default")

        # Validate theme exists
        if theme_key not in self.themes:
            logger.warning(
                f"Theme '{theme_key}' not found in themes.toml. Using 'default' theme."
            )
            theme_key = "default"

        self.current_theme_key = theme_key

    def _save_settings(self, settings: Dict[str, Any]) -> None:
        """Save settings to TOML file."""
        # Ensure config directory exists
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.settings_path, "wb") as f:
            tomli_w.dump(settings, f)

    def get_current_theme(self) -> Dict[str, Any]:
        """Get current theme as dictionary."""
        if self.current_theme_key not in self.themes:
            self.current_theme_key = "default"
        return self.themes[self.current_theme_key]

    def switch_theme(self, theme_key: str) -> bool:
        """
        Switch to a different theme and save preference.

        Args:
            theme_key: Theme identifier (alphanumeric + underscore only)

        Returns:
            True if theme was switched successfully, False otherwise
        """
        # Validate theme_key format (defense in depth)
        if not re.match(r"^[a-z0-9_]+$", theme_key):
            logger.error(
                f"Invalid theme key format '{theme_key}'. Only lowercase alphanumeric and underscore allowed."
            )
            return False

        if theme_key not in self.themes:
            logger.warning(f"Theme '{theme_key}' not found")
            return False

        self.current_theme_key = theme_key

        # Save to settings file
        try:
            # Load existing settings or create new
            if self.settings_path.exists():
                with open(self.settings_path, "rb") as f:
                    settings = tomllib.load(f)
            else:
                settings = {}

            # Update theme
            if "appearance" not in settings:
                settings["appearance"] = {}
            settings["appearance"]["theme"] = theme_key

            self._save_settings(settings)
            return True
        except PermissionError as e:
            logger.error(f"Permission denied writing theme settings: {e}")
            # In future: show error dialog to user in GUI
            return False
        except OSError as e:
            logger.error(
                f"I/O error saving theme settings: {e}", exc_info=True
            )
            return False
        except Exception as e:
            logger.error(
                f"Failed to save theme preference: {e}", exc_info=True
            )
            return False

    def get_color(self, color_name: str) -> str:
        """
        Get specific color value from current theme.

        Args:
            color_name: Name of the color (e.g., 'accent_purple')

        Returns:
            Hex color string
        """
        theme = self.get_current_theme()
        return str(theme.get(color_name, "#FFFFFF"))

    def get_category_colors(self) -> Dict[str, str]:
        """Get all category colors from current theme."""
        theme = self.get_current_theme()
        return dict(theme.get("categories", {}))

    def get_available_themes(self) -> List[Dict[str, str]]:
        """
        Get list of available themes with metadata.

        Returns:
            List of dicts with 'key', 'name', and 'description'
        """
        result: List[Dict[str, str]] = []
        for key, theme_data in self.themes.items():
            result.append({
                "key": key,
                "name": str(theme_data.get("name", key)),
                "description": str(
                    theme_data.get("description", "No description")
                ),
            })
        return result


# Global singleton instance
theme_manager = ThemeManager()
