import logging
import os
from typing import Callable, List, Optional

import customtkinter as ctk

from finance_tracker.database import Database
from finance_tracker.theme_manager import theme_manager
from finance_tracker.ui.colors import (
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_PURPLE,
    CATEGORY_COLORS,
    DARK_BG,
    DARK_BG_SECONDARY,
    DARK_BG_TERTIARY,
    ERROR,
    GRADIENT_START,
    SUCCESS,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from finance_tracker.ui.widgets import (
    BalanceCard,
    GradientFrame,
    ModernButton,
    StatCard,
    TransactionItem,
)

# Configure logging for the application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/finance_tracker.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


class FinanceTrackerApp(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        # Initialize theme system BEFORE UI creation
        theme_manager.initialize()

        # Database setup
        os.makedirs("data", exist_ok=True)
        self.db: Database = Database()

        # Window setup
        self.title("Finance Tracker")
        self.geometry("1000x700")
        self._setup_window()

        # Current view
        self.current_view: Optional[str] = None

        # UI components
        self.sidebar: ctk.CTkFrame
        self.content_frame: ctk.CTkFrame
        self.nav_buttons: List[ctk.CTkButton] = []

        # Initialize UI
        self._setup_ui()
        self.show_dashboard()

    def _setup_window(self) -> None:
        """Configure window appearance."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=DARK_BG)

    def _setup_ui(self) -> None:
        """Setup main UI structure."""
        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self, width=200, corner_radius=0, fg_color=DARK_BG_SECONDARY
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo/Title
        title_label: ctk.CTkLabel = ctk.CTkLabel(
            self.sidebar,
            text="💰 Finance\nTracker",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=ACCENT_PURPLE,
        )
        title_label.pack(pady=(30, 50))

        # Navigation buttons
        btn_dashboard: ctk.CTkButton = self._create_nav_button(
            "📊 Dashboard", self.show_dashboard
        )
        btn_add: ctk.CTkButton = self._create_nav_button(
            "➕ Add Transaction", self.show_add_transaction
        )
        btn_history: ctk.CTkButton = self._create_nav_button(
            "📜 History", self.show_history
        )
        btn_settings: ctk.CTkButton = self._create_nav_button(
            "⚙️ Settings", self.show_settings
        )

        # Spacer
        spacer: ctk.CTkFrame = ctk.CTkFrame(
            self.sidebar, fg_color="transparent"
        )
        spacer.pack(fill="both", expand=True)

        # Footer
        footer_label: ctk.CTkLabel = ctk.CTkLabel(
            self.sidebar,
            text="v1.0.0",
            font=ctk.CTkFont(size=10),
            text_color=TEXT_MUTED,
        )
        footer_label.pack(pady=20)

        # Main content area
        self.content_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color=DARK_BG
        )
        self.content_frame.pack(side="right", fill="both", expand=True)

    def _create_nav_button(
        self, text: str, command: Callable[[], None]
    ) -> ctk.CTkButton:
        """Create a navigation button."""
        btn: ctk.CTkButton = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            fg_color="transparent",
            text_color=TEXT_SECONDARY,
            hover_color=DARK_BG_TERTIARY,
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=14),
        )
        btn.pack(fill="x", padx=10, pady=5)
        self.nav_buttons.append(btn)
        return btn

    def _clear_content(self) -> None:
        """Clear current content."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self) -> None:
        """Show dashboard view."""
        self.current_view = "dashboard"
        self._clear_content()

        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        header.pack(anchor="w", padx=30, pady=(30, 20))

        # Balance card
        balance = self.db.get_balance()
        balance_card = BalanceCard(self.content_frame, balance=balance)
        balance_card.pack(fill="x", padx=30, pady=10)

        # Statistics
        stats = self.db.get_statistics()
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=20)

        # Income and Expense cards
        income_card = StatCard(
            stats_frame,
            "Monthly Income",
            stats["monthly_income"],
            color=SUCCESS,
        )
        income_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        expense_card = StatCard(
            stats_frame,
            "Monthly Expenses",
            stats["monthly_expense"],
            color=ERROR,
        )
        expense_card.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Recent transactions
        recent_header = ctk.CTkLabel(
            self.content_frame,
            text="Recent Transactions",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        recent_header.pack(anchor="w", padx=30, pady=(20, 10))

        # Scrollable frame for transactions
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent", height=200
        )
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        transactions = self.db.get_transactions(limit=10)
        if transactions:
            for trans in transactions:
                item = TransactionItem(scroll_frame, trans)
                item.pack(fill="x", pady=5)
        else:
            no_trans_label = ctk.CTkLabel(
                scroll_frame,
                text="No transactions yet. Add your first transaction!",
                font=ctk.CTkFont(size=14),
                text_color=TEXT_MUTED,
            )
            no_trans_label.pack(pady=50)

    def show_add_transaction(self) -> None:
        """Show add transaction form."""
        self.current_view = "add_transaction"
        self._clear_content()

        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Add Transaction",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        header.pack(anchor="w", padx=30, pady=(30, 20))

        # Form container
        form_frame = GradientFrame(self.content_frame)
        form_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # Form content
        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=40, pady=40)

        # Transaction type
        type_label = ctk.CTkLabel(
            form_content,
            text="Transaction Type",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        type_label.pack(anchor="w", pady=(0, 5))

        type_var = ctk.StringVar(value="expense")
        type_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        type_frame.pack(fill="x", pady=(0, 20))

        income_radio = ctk.CTkRadioButton(
            type_frame,
            text="Income",
            variable=type_var,
            value="income",
            fg_color=SUCCESS,
            hover_color=SUCCESS,
        )
        income_radio.pack(side="left", padx=(0, 20))

        expense_radio = ctk.CTkRadioButton(
            type_frame,
            text="Expense",
            variable=type_var,
            value="expense",
            fg_color=ERROR,
            hover_color=ERROR,
        )
        expense_radio.pack(side="left")

        # Amount
        amount_label = ctk.CTkLabel(
            form_content,
            text="Amount",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        amount_label.pack(anchor="w", pady=(0, 5))

        amount_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="0.00",
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color=DARK_BG_TERTIARY,
            border_width=0,
        )
        amount_entry.pack(fill="x", pady=(0, 20))

        # Category
        category_label = ctk.CTkLabel(
            form_content,
            text="Category",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        category_label.pack(anchor="w", pady=(0, 5))

        categories = list(CATEGORY_COLORS.keys())
        category_combo = ctk.CTkComboBox(
            form_content,
            values=categories,
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color=DARK_BG_TERTIARY,
            border_width=0,
            button_color=ACCENT_PURPLE,
            button_hover_color=GRADIENT_START,
        )
        category_combo.set(categories[0])
        category_combo.pack(fill="x", pady=(0, 20))

        # Description
        desc_label = ctk.CTkLabel(
            form_content,
            text="Description (Optional)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        desc_label.pack(anchor="w", pady=(0, 5))

        desc_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="What was this for?",
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color=DARK_BG_TERTIARY,
            border_width=0,
        )
        desc_entry.pack(fill="x", pady=(0, 30))

        # Submit button
        def submit_transaction() -> None:
            try:
                # Validate amount
                amount_str = amount_entry.get().strip()
                if not amount_str:
                    logger.warning(
                        "Transaction submission failed: empty amount"
                    )
                    return

                amount = float(amount_str)
                if amount <= 0:
                    logger.warning(
                        f"Transaction submission failed: non-positive amount {amount}"
                    )
                    return

                # Validate transaction type
                trans_type = type_var.get()
                if trans_type not in ("income", "expense"):
                    logger.error(f"Invalid transaction type '{trans_type}'")
                    return

                # Validate category
                category = category_combo.get()
                if category not in CATEGORY_COLORS:
                    logger.error(f"Invalid category '{category}'")
                    return

                # Validate description length
                description = desc_entry.get()
                if len(description) > 500:
                    logger.warning(
                        f"Description too long ({len(description)} chars, max 500)"
                    )
                    return

                # All validations passed - add transaction
                success = self.db.add_transaction(
                    transaction_type=trans_type,
                    category=category,
                    amount=amount,
                    description=description,
                )

                if success:
                    logger.info(
                        f"Transaction added: {trans_type} {category} ${amount:.2f}"
                    )
                    self.show_dashboard()
                else:
                    logger.error("Failed to add transaction to database")

            except ValueError as e:
                logger.warning(f"Invalid amount format: {e}")

        submit_btn = ModernButton(
            form_content,
            text="Add Transaction",
            command=submit_transaction,
            color=ACCENT_PURPLE,
        )
        submit_btn.pack(fill="x")

    def show_history(self) -> None:
        """Show transaction history."""
        self.current_view = "history"
        self._clear_content()

        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Transaction History",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        header.pack(anchor="w", padx=30, pady=(30, 20))

        # Scrollable frame for all transactions
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        transactions = self.db.get_transactions(limit=100)
        if transactions:
            for trans in transactions:
                item = TransactionItem(scroll_frame, trans)
                item.pack(fill="x", pady=5)
        else:
            no_trans_label = ctk.CTkLabel(
                scroll_frame,
                text="No transactions found",
                font=ctk.CTkFont(size=14),
                text_color=TEXT_MUTED,
            )
            no_trans_label.pack(pady=50)

    def show_settings(self) -> None:
        """Show settings view with theme selector."""
        self.current_view = "settings"
        self._clear_content()

        # Header
        header: ctk.CTkLabel = ctk.CTkLabel(
            self.content_frame,
            text="Settings",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        header.pack(anchor="w", padx=30, pady=(30, 20))

        # Settings container
        settings_frame: GradientFrame = GradientFrame(self.content_frame)
        settings_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # Settings content
        settings_content: ctk.CTkFrame = ctk.CTkFrame(
            settings_frame, fg_color="transparent"
        )
        settings_content.pack(fill="both", expand=True, padx=40, pady=40)

        # Appearance section
        appearance_label: ctk.CTkLabel = ctk.CTkLabel(
            settings_content,
            text="Appearance",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        appearance_label.pack(anchor="w", pady=(0, 20))

        # Theme selector
        theme_label: ctk.CTkLabel = ctk.CTkLabel(
            settings_content,
            text="Theme",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        theme_label.pack(anchor="w", pady=(0, 5))

        # Get available themes
        themes = theme_manager.get_available_themes()
        theme_names = [f"{theme['name']}" for theme in themes]
        theme_keys = {theme["name"]: theme["key"] for theme in themes}

        # Current theme
        current_theme_key = theme_manager.current_theme_key
        current_theme_name = next(
            (t["name"] for t in themes if t["key"] == current_theme_key),
            theme_names[0],
        )

        theme_var = ctk.StringVar(value=current_theme_name)

        theme_combo: ctk.CTkComboBox = ctk.CTkComboBox(
            settings_content,
            values=theme_names,
            variable=theme_var,
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color=DARK_BG_TERTIARY,
            border_width=0,
            button_color=ACCENT_PURPLE,
            button_hover_color=GRADIENT_START,
        )
        theme_combo.pack(fill="x", pady=(0, 20))

        # Theme description
        desc_label: ctk.CTkLabel = ctk.CTkLabel(
            settings_content,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY,
            wraplength=600,
            justify="left",
        )
        desc_label.pack(anchor="w", pady=(0, 20))

        def update_description(choice: str) -> None:
            """Update description when theme selection changes."""
            theme_key = theme_keys.get(choice, "default")
            theme_info = next(
                (t for t in themes if t["key"] == theme_key), None
            )
            if theme_info:
                desc_label.configure(text=theme_info["description"])

        # Set initial description
        update_description(current_theme_name)

        # Update description on change
        theme_combo.configure(command=update_description)

        # Preview section
        preview_label: ctk.CTkLabel = ctk.CTkLabel(
            settings_content,
            text="Color Preview",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        preview_label.pack(anchor="w", pady=(10, 5))

        # Preview frame with color swatches
        preview_frame: ctk.CTkFrame = ctk.CTkFrame(
            settings_content,
            fg_color=DARK_BG_TERTIARY,
            corner_radius=10,
            height=80,
        )
        preview_frame.pack(fill="x", pady=(0, 30))
        preview_frame.pack_propagate(False)

        # Color swatches
        colors_to_preview = [
            ACCENT_PURPLE,
            ACCENT_BLUE,
            ACCENT_GREEN,
            SUCCESS,
            ERROR,
        ]

        swatches_container: ctk.CTkFrame = ctk.CTkFrame(
            preview_frame, fg_color="transparent"
        )
        swatches_container.pack(expand=True)

        for color in colors_to_preview:
            swatch: ctk.CTkFrame = ctk.CTkFrame(
                swatches_container,
                width=50,
                height=50,
                corner_radius=10,
                fg_color=color,
            )
            swatch.pack(side="left", padx=5)

        # Apply button
        def apply_theme() -> None:
            """Apply selected theme."""
            selected_name = theme_var.get()
            theme_key = theme_keys.get(selected_name, "default")

            if theme_manager.switch_theme(theme_key):
                # Refresh UI with new theme
                self.refresh_ui()

        apply_btn: ModernButton = ModernButton(
            settings_content,
            text="Apply Theme",
            command=apply_theme,
            color=ACCENT_PURPLE,
        )
        apply_btn.pack(fill="x")

    def refresh_ui(self) -> None:
        """Refresh UI after theme change."""
        # Reload colors from new theme
        from finance_tracker.ui import colors

        colors.reload_colors()

        # Force re-import of colors in main namespace
        import importlib

        importlib.reload(colors)

        # Update the color imports in current module
        import sys

        current_module = sys.modules[__name__]
        for color_name in [
            "ACCENT_BLUE",
            "ACCENT_GREEN",
            "ACCENT_PURPLE",
            "DARK_BG",
            "DARK_BG_SECONDARY",
            "DARK_BG_TERTIARY",
            "ERROR",
            "GRADIENT_START",
            "SUCCESS",
            "TEXT_MUTED",
            "TEXT_PRIMARY",
            "TEXT_SECONDARY",
            "CATEGORY_COLORS",
        ]:
            setattr(current_module, color_name, getattr(colors, color_name))

        # Recreate sidebar
        self.sidebar.destroy()
        self.content_frame.destroy()

        # Recreate UI structure
        self._setup_ui()

        # Recreate current view
        if self.current_view == "dashboard":
            self.show_dashboard()
        elif self.current_view == "add_transaction":
            self.show_add_transaction()
        elif self.current_view == "history":
            self.show_history()
        elif self.current_view == "settings":
            self.show_settings()
        else:
            self.show_dashboard()


def main() -> None:
    """Run the application."""
    app: FinanceTrackerApp = FinanceTrackerApp()
    app.mainloop()


# python3 main.py
if __name__ == "__main__":
    main()
