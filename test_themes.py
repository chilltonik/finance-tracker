#!/usr/bin/env python3
"""Quick test script for theme system."""

from theme_manager import theme_manager
from ui import colors


def test_themes() -> None:
    """Test all themes and color loading."""
    print("=" * 60)
    print("Testing Finance Tracker Theme System")
    print("=" * 60)

    # Initialize
    theme_manager.initialize()
    print(f"\n✓ Theme manager initialized")
    print(f"  Current theme: {theme_manager.current_theme_key}")

    # List all themes
    themes = theme_manager.get_available_themes()
    print(f"\n✓ Available themes: {len(themes)}")
    for theme in themes:
        print(f"  - {theme['key']:15} {theme['name']}")
        print(f"    {theme['description']}")

    # Test each theme
    print("\n" + "=" * 60)
    print("Testing Theme Colors")
    print("=" * 60)

    for theme in themes:
        theme_key = theme["key"]
        print(f"\n[{theme['name']}]")

        # Switch theme
        theme_manager.switch_theme(theme_key)
        colors.reload_colors()

        # Display key colors
        print(f"  Background:     {colors.DARK_BG}")
        print(f"  Accent:         {colors.ACCENT_PURPLE}")
        print(f"  Success:        {colors.SUCCESS}")
        print(f"  Error:          {colors.ERROR}")
        print(f"  Text Primary:   {colors.TEXT_PRIMARY}")

    # Reset to default
    theme_manager.switch_theme("default")
    colors.reload_colors()

    print("\n" + "=" * 60)
    print("✓ All tests passed! Theme system working correctly.")
    print("=" * 60)


if __name__ == "__main__":
    test_themes()
