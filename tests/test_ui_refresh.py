#!/usr/bin/env python3
"""Test UI refresh after theme change."""

import importlib
import sys

from finance_tracker.theme_manager import theme_manager
from finance_tracker.ui import colors

print("=" * 70)
print("Testing UI Refresh Mechanism")
print("=" * 70)

# Test 1: Initial state
print("\n[Test 1] Initial state")
theme_manager.initialize()
print(f"  Current theme: {theme_manager.current_theme_key}")
print(f"  ACCENT_PURPLE: {colors.ACCENT_PURPLE}")
print(f"  DARK_BG: {colors.DARK_BG}")

# Test 2: Switch theme and reload
print("\n[Test 2] Switch to ocean_breeze")
theme_manager.switch_theme("ocean_breeze")
colors.reload_colors()
print(f"  After reload:")
print(f"    ACCENT_PURPLE: {colors.ACCENT_PURPLE} (expected: #00E5FF)")
print(f"    DARK_BG: {colors.DARK_BG} (expected: #0A1929)")

# Test 3: Verify module updates
print("\n[Test 3] Verify module-level updates")
colors_module = sys.modules["finance_tracker.ui.colors"]
print(f"  Module ACCENT_PURPLE: {colors_module.ACCENT_PURPLE}")
print(f"  colors.ACCENT_PURPLE: {colors.ACCENT_PURPLE}")
print(f"  Match: {colors_module.ACCENT_PURPLE == colors.ACCENT_PURPLE}")

# Test 4: Switch to another theme
print("\n[Test 4] Switch to sunset_glow")
theme_manager.switch_theme("sunset_glow")
colors.reload_colors()
print(f"  After reload:")
print(f"    ACCENT_PURPLE: {colors.ACCENT_PURPLE} (expected: #FF6B9D)")
print(f"    DARK_BG: {colors.DARK_BG} (expected: #1A0E0E)")

# Test 5: Test reimport (simulating what refresh_ui does)
print("\n[Test 5] Test importlib.reload()")
importlib.reload(colors)
print(f"  After reimport:")
print(f"    ACCENT_PURPLE: {colors.ACCENT_PURPLE}")
print(f"    DARK_BG: {colors.DARK_BG}")

# Test 6: Verify all colors update
print("\n[Test 6] Verify all color constants")
theme_manager.switch_theme("forest_green")
colors.reload_colors()
importlib.reload(colors)

all_colors = {
    "ACCENT_PURPLE": colors.ACCENT_PURPLE,
    "ACCENT_BLUE": colors.ACCENT_BLUE,
    "ACCENT_GREEN": colors.ACCENT_GREEN,
    "SUCCESS": colors.SUCCESS,
    "ERROR": colors.ERROR,
    "TEXT_PRIMARY": colors.TEXT_PRIMARY,
}

print(f"  Forest Green colors:")
for name, value in all_colors.items():
    print(f"    {name:15} = {value}")

# Expected values for forest_green
expected = {
    "ACCENT_PURPLE": "#10B981",
    "ACCENT_BLUE": "#14B8A6",
    "ACCENT_GREEN": "#84CC16",
    "SUCCESS": "#10B981",
    "ERROR": "#EF4444",
    "TEXT_PRIMARY": "#F0FDF4",
}

# Verify
print("\n[Test 7] Verification")
all_match = True
for name, expected_value in expected.items():
    actual_value = all_colors[name]
    match = actual_value == expected_value
    all_match = all_match and match
    status = "✓" if match else "✗"
    print(f"  {status} {name}: {actual_value} == {expected_value}")

# Reset to default
theme_manager.switch_theme("default")
colors.reload_colors()

print("\n" + "=" * 70)
if all_match:
    print("✅ All tests passed! UI refresh mechanism working correctly.")
else:
    print("❌ Some tests failed. Check the output above.")
print("=" * 70)
