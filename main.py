#!/usr/bin/env python3
"""
Personal Finance Tracker with Crypto Wallet Design
A modern finance tracking application built with Python and CustomTkinter.
"""
import customtkinter as ctk
from datetime import datetime
from typing import Optional
import os

from database import Database
from ui.colors import *
from ui.widgets import (
    BalanceCard, StatCard, TransactionItem,
    ModernButton, GradientFrame
)


class FinanceTrackerApp(ctk.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        # Database setup
        os.makedirs("data", exist_ok=True)
        self.db = Database()

        # Window setup
        self.title("Finance Tracker")
        self.geometry("1000x700")
        self._setup_window()

        # Current view
        self.current_view = None

        # Initialize UI
        self._setup_ui()
        self.show_dashboard()

    def _setup_window(self):
        """Configure window appearance."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=DARK_BG)

    def _setup_ui(self):
        """Setup main UI structure."""
        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=200,
            corner_radius=0,
            fg_color=DARK_BG_SECONDARY
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo/Title
        title_label = ctk.CTkLabel(
            self.sidebar,
            text="💰 Finance\nTracker",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=ACCENT_PURPLE
        )
        title_label.pack(pady=(30, 50))

        # Navigation buttons
        self.nav_buttons = []

        btn_dashboard = self._create_nav_button("📊 Dashboard", self.show_dashboard)
        btn_add = self._create_nav_button("➕ Add Transaction", self.show_add_transaction)
        btn_history = self._create_nav_button("📜 History", self.show_history)

        # Spacer
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        # Footer
        footer_label = ctk.CTkLabel(
            self.sidebar,
            text="v1.0.0",
            font=ctk.CTkFont(size=10),
            text_color=TEXT_MUTED
        )
        footer_label.pack(pady=20)

        # Main content area
        self.content_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=DARK_BG
        )
        self.content_frame.pack(side="right", fill="both", expand=True)

    def _create_nav_button(self, text: str, command):
        """Create a navigation button."""
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            fg_color="transparent",
            text_color=TEXT_SECONDARY,
            hover_color=DARK_BG_TERTIARY,
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        btn.pack(fill="x", padx=10, pady=5)
        self.nav_buttons.append(btn)
        return btn

    def _clear_content(self):
        """Clear current content."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        """Show dashboard view."""
        self._clear_content()

        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_PRIMARY
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
            stats['monthly_income'],
            color=SUCCESS
        )
        income_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        expense_card = StatCard(
            stats_frame,
            "Monthly Expenses",
            stats['monthly_expense'],
            color=ERROR
        )
        expense_card.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Recent transactions
        recent_header = ctk.CTkLabel(
            self.content_frame,
            text="Recent Transactions",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        recent_header.pack(anchor="w", padx=30, pady=(20, 10))

        # Scrollable frame for transactions
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            height=200
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
                text_color=TEXT_MUTED
            )
            no_trans_label.pack(pady=50)

    def show_add_transaction(self):
        """Show add transaction form."""
        self._clear_content()

        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Add Transaction",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_PRIMARY
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
            text_color=TEXT_PRIMARY
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
            hover_color=SUCCESS
        )
        income_radio.pack(side="left", padx=(0, 20))

        expense_radio = ctk.CTkRadioButton(
            type_frame,
            text="Expense",
            variable=type_var,
            value="expense",
            fg_color=ERROR,
            hover_color=ERROR
        )
        expense_radio.pack(side="left")

        # Amount
        amount_label = ctk.CTkLabel(
            form_content,
            text="Amount",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        amount_label.pack(anchor="w", pady=(0, 5))

        amount_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="0.00",
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color=DARK_BG_TERTIARY,
            border_width=0
        )
        amount_entry.pack(fill="x", pady=(0, 20))

        # Category
        category_label = ctk.CTkLabel(
            form_content,
            text="Category",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY
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
            button_hover_color=GRADIENT_START
        )
        category_combo.set(categories[0])
        category_combo.pack(fill="x", pady=(0, 20))

        # Description
        desc_label = ctk.CTkLabel(
            form_content,
            text="Description (Optional)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        desc_label.pack(anchor="w", pady=(0, 5))

        desc_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="What was this for?",
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color=DARK_BG_TERTIARY,
            border_width=0
        )
        desc_entry.pack(fill="x", pady=(0, 30))

        # Submit button
        def submit_transaction():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive")

                trans_type = type_var.get()
                category = category_combo.get()
                description = desc_entry.get()

                if self.db.add_transaction(trans_type, category, amount, description):
                    self.show_dashboard()
            except ValueError as e:
                # Show error (in production, use a proper dialog)
                print(f"Error: {e}")

        submit_btn = ModernButton(
            form_content,
            text="Add Transaction",
            command=submit_transaction,
            color=ACCENT_PURPLE
        )
        submit_btn.pack(fill="x")

    def show_history(self):
        """Show transaction history."""
        self._clear_content()

        # Header
        header = ctk.CTkLabel(
            self.content_frame,
            text="Transaction History",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        header.pack(anchor="w", padx=30, pady=(30, 20))

        # Scrollable frame for all transactions
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
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
                text_color=TEXT_MUTED
            )
            no_trans_label.pack(pady=50)


def main():
    """Run the application."""
    app = FinanceTrackerApp()
    app.mainloop()


# python3 main.py
if __name__ == "__main__":
    main()
