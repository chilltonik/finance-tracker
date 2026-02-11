"""Database management for the finance tracker."""

import logging
import sqlite3
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class Database:
    """Handle all database operations."""

    def __init__(self, db_path: str = "data/finance_tracker.db") -> None:
        self.db_path: str = db_path
        self.init_database()

    def init_database(self) -> None:
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    date TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            # Balance history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS balance_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    balance REAL NOT NULL,
                    date TEXT NOT NULL
                )
            """)

            conn.commit()

    def add_transaction(
        self,
        transaction_type: str,
        category: str,
        amount: float,
        description: str = "",
    ) -> bool:
        """Add a new transaction."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                cursor.execute(
                    """
                    INSERT INTO transactions (type, category, amount, description, date, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        transaction_type,
                        category,
                        amount,
                        description,
                        now,
                        now,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding transaction: {e}", exc_info=True)
            return False

    def get_transactions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent transactions."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, type, category, amount, description, date
                FROM transactions
                ORDER BY date DESC
                LIMIT ?
            """,
                (limit,),
            )

            columns = [
                "id",
                "type",
                "category",
                "amount",
                "description",
                "date",
            ]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_balance(self) -> float:
        """Calculate current balance."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) -
                    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0)
                FROM transactions
            """)
            result = cursor.fetchone()
            return result[0] if result else 0.0

    def get_statistics(self) -> Dict[str, Any]:
        """Get financial statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total income and expenses
            cursor.execute("""
                SELECT
                    COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) as total_income,
                    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) as total_expense
                FROM transactions
                WHERE date >= date('now', '-30 days')
            """)
            income, expense = cursor.fetchone()

            # Category breakdown
            cursor.execute("""
                SELECT category, SUM(amount) as total
                FROM transactions
                WHERE type = 'expense' AND date >= date('now', '-30 days')
                GROUP BY category
                ORDER BY total DESC
                LIMIT 5
            """)
            top_categories = cursor.fetchall()

            return {
                "monthly_income": income,
                "monthly_expense": expense,
                "top_categories": top_categories,
            }

    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM transactions WHERE id = ?", (transaction_id,)
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error deleting transaction: {e}", exc_info=True)
            return False
