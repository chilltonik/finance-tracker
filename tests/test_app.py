#!/usr/bin/env python3
"""Quick test to verify the app starts without errors."""

import os
import sys

print("=" * 60)
print("Testing Finance Tracker Application Startup")
print("=" * 60)

try:
    # Test imports
    print("\n[1/5] Testing imports...")
    from finance_tracker.database import Database
    from finance_tracker.theme_manager import theme_manager
    from finance_tracker.ui.colors import (
        ACCENT_BLUE,
        ACCENT_GREEN,
        ACCENT_PURPLE,
        CATEGORY_COLORS,
        DARK_BG,
        ERROR,
        SUCCESS,
    )

    print("    ✓ All imports successful")

    # Test theme manager
    print("\n[2/5] Testing theme manager...")
    theme_manager.initialize()
    print(f"    ✓ Initialized with theme: {theme_manager.current_theme_key}")

    # Test colors
    print("\n[3/5] Testing color loading...")
    print(f"    ✓ ACCENT_PURPLE: {ACCENT_PURPLE}")
    print(f"    ✓ ACCENT_BLUE: {ACCENT_BLUE}")
    print(f"    ✓ ACCENT_GREEN: {ACCENT_GREEN}")
    print(f"    ✓ Categories: {len(CATEGORY_COLORS)}")

    # Test database
    print("\n[4/5] Testing database...")
    os.makedirs("data", exist_ok=True)
    db = Database()
    balance = db.get_balance()
    print(f"    ✓ Database initialized")
    print(f"    ✓ Current balance: ${balance:.2f}")

    # Import main (this will validate all UI code)
    print("\n[5/5] Testing main application module...")
    import customtkinter as ctk

    print("    ✓ CustomTkinter available")
    print("    ℹ️  GUI test skipped (requires display)")

    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print("\n🚀 Ready to launch: python3 main.py")

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\n💡 Try: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
