"""Custom widgets for the finance tracker UI."""

from typing import Any, Callable, Dict, Optional

import customtkinter as ctk

from finance_tracker.ui.colors import (
    ACCENT_BLUE,
    ACCENT_PURPLE,
    CATEGORY_COLORS,
    DARK_BG_SECONDARY,
    DARK_BG_TERTIARY,
    ERROR,
    GRADIENT_START,
    SUCCESS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class GradientFrame(ctk.CTkFrame):
    """Frame with gradient background effect (simulated)."""

    def __init__(self, master: Any, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=DARK_BG_SECONDARY,
            corner_radius=15,
            border_width=1,
            border_color=DARK_BG_TERTIARY,
        )


class BalanceCard(ctk.CTkFrame):
    """Display balance with crypto wallet style."""

    def __init__(
        self, master: Any, balance: float = 0.0, **kwargs: Any
    ) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=GRADIENT_START, corner_radius=20, height=180)

        self.balance: float = balance
        self.balance_label: ctk.CTkLabel
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the balance card UI."""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Total Balance",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color=TEXT_SECONDARY,
        )
        title_label.pack(pady=(20, 5))

        # Balance amount
        self.balance_label = ctk.CTkLabel(
            self,
            text=f"${self.balance:,.2f}",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        self.balance_label.pack(pady=10)

        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self,
            text="Your current balance",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY,
        )
        subtitle_label.pack(pady=(5, 20))

    def update_balance(self, balance: float) -> None:
        """Update displayed balance."""
        self.balance = balance
        self.balance_label.configure(text=f"${balance:,.2f}")


class StatCard(ctk.CTkFrame):
    """Statistics card widget."""

    def __init__(
        self,
        master: Any,
        title: str,
        amount: float,
        color: str = ACCENT_BLUE,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=DARK_BG_SECONDARY, corner_radius=15, height=120
        )

        self._setup_ui(title, amount, color)

    def _setup_ui(self, title: str, amount: float, color: str) -> None:
        """Setup stat card UI."""
        # Icon/indicator
        indicator = ctk.CTkFrame(
            self, width=50, height=50, corner_radius=25, fg_color=color
        )
        indicator.pack(pady=(20, 10))

        # Amount
        amount_label = ctk.CTkLabel(
            self,
            text=f"${amount:,.2f}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        amount_label.pack()

        # Title
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY,
        )
        title_label.pack(pady=(5, 20))


class TransactionItem(ctk.CTkFrame):
    """Single transaction list item."""

    def __init__(
        self,
        master: Any,
        transaction: Dict[str, Any],
        on_delete: Optional[Callable[[], None]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=DARK_BG_SECONDARY, corner_radius=10, height=70)

        self.transaction: Dict[str, Any] = transaction
        self.on_delete: Optional[Callable[[], None]] = on_delete
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup transaction item UI."""
        # Category color indicator
        category = self.transaction.get("category", "Other")
        color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["Other"])

        indicator = ctk.CTkFrame(
            self, width=4, height=50, fg_color=color, corner_radius=2
        )
        indicator.pack(side="left", padx=(10, 15), pady=10)

        # Transaction info
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=10)

        # Category and description
        category_label = ctk.CTkLabel(
            info_frame,
            text=category,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY,
            anchor="w",
        )
        category_label.pack(anchor="w")

        desc = self.transaction.get("description", "No description")
        desc_label = ctk.CTkLabel(
            info_frame,
            text=desc[:30] + "..." if len(desc) > 30 else desc,
            font=ctk.CTkFont(size=11),
            text_color=TEXT_SECONDARY,
            anchor="w",
        )
        desc_label.pack(anchor="w")

        # Amount
        amount = self.transaction.get("amount", 0)
        trans_type = self.transaction.get("type", "expense")
        amount_color = SUCCESS if trans_type == "income" else ERROR
        amount_text = (
            f"+${amount:,.2f}"
            if trans_type == "income"
            else f"-${amount:,.2f}"
        )

        amount_label = ctk.CTkLabel(
            self,
            text=amount_text,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=amount_color,
        )
        amount_label.pack(side="right", padx=15)


class ModernButton(ctk.CTkButton):
    """Modern styled button."""

    def __init__(
        self,
        master: Any,
        text: str,
        command: Callable[[], Any],
        color: str = ACCENT_PURPLE,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=color,
            hover_color=self._darken_color(color),
            corner_radius=10,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            **kwargs,
        )

    @staticmethod
    def _darken_color(hex_color: str) -> str:
        """Darken a hex color for hover effect."""
        # Simple darkening by reducing each component
        hex_color = hex_color.lstrip("#")
        rgb: tuple[int, int, int] = tuple(
            int(hex_color[i : i + 2], 16) for i in (0, 2, 4)
        )  # type: ignore[assignment]
        darkened: tuple[int, int, int] = tuple(
            max(0, int(c * 0.8)) for c in rgb
        )  # type: ignore[assignment]
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
