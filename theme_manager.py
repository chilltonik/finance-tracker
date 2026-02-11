"""Theme management for the Finance Tracker application."""

from pathlib import Path
from typing import Any, Dict, List
import tomllib


try:
    import tomli_w
except ImportError:
    raise ImportError(
        "tomli_w required for writing TOML files. Install: pip install tomli-w"
    )


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
            self.themes_path: Path = Path("config/themes.toml")
            self.settings_path: Path = Path("config/settings.toml")
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
            print(
                f"Warning: Theme '{theme_key}' not found. "
                f"Using 'default' theme."
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
            theme_key: Key of the theme to switch to

        Returns:
            True if successful, False otherwise
        """
        if theme_key not in self.themes:
            print(f"Error: Theme '{theme_key}' not found")
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
        except Exception as e:
            print(f"Error saving theme preference: {e}")
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
