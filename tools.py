"""
tools.py

Database operations for the finance assistant.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import select, func, extract, or_, desc

from db import get_session
from models import Account, Category, Transaction


def money(value):
    return f"${float(value):,.2f}"


# ============================================================
# Accounts
# ============================================================

def create_account(data):
    with get_session() as session:
        existing = session.scalar(
            select(Account).where(Account.account_name == data.account_name)
        )

        if existing:
            return f"Account already exists: {data.account_name}"

        account = Account(
            account_name=data.account_name,
            account_bank=data.account_bank
        )

        session.add(account)
        session.commit()

        return f"Account created: {account.account_name} at {account.account_bank}"


def update_account(data):
    with get_session() as session:
        account = session.get(Account, data.account_id)

        if not account:
            return f"Account not found: {data.account_id}"

        account.account_name = data.account_name
        account.account_bank = data.account_bank

        session.commit()

        return f"Account updated: {account.account_name}"


def delete_account(data):
    with get_session() as session:
        account = session.get(Account, data.account_id)

        if not account:
            return f"Account not found: {data.account_id}"

        session.delete(account)
        session.commit()

        return f"Account deleted: {data.account_id}"


def get_account(data):
    with get_session() as session:
        account = session.get(Account, data.account_id)

        if not account:
            return f"Account not found: {data.account_id}"

        return (
            f"ID: {account.account_id}\n"
            f"Name: {account.account_name}\n"
            f"Bank: {account.account_bank}"
        )


def list_accounts(data=None):
    with get_session() as session:
        accounts = session.scalars(
            select(Account).order_by(Account.account_name)
        ).all()

        if not accounts:
            return "No accounts found."

        return [
            {
                "ID": a.account_id,
                "Account": a.account_name,
                "Bank": a.account_bank,
            }
            for a in accounts
        ]


# ============================================================
# Categories
# ============================================================

def create_category(data):
    with get_session() as session:
        existing = session.scalar(
            select(Category).where(Category.category_name == data.category_name)
        )

        if existing:
            return f"Category already exists: {data.category_name}"

        category = Category(category_name=data.category_name)

        session.add(category)
        session.commit()

        return f"Category created: {category.category_name}"


def update_category(data):
    with get_session() as session:
        category = session.get(Category, data.category_id)

        if not category:
            return f"Category not found: {data.category_id}"

        category.category_name = data.category_name

        session.commit()

        return f"Category updated: {category.category_name}"


def delete_category(data):
    with get_session() as session:
        category = session.get(Category, data.category_id)

        if not category:
            return f"Category not found: {data.category_id}"

        session.delete(category)
        session.commit()

        return f"Category deleted: {data.category_id}"


def list_categories(data=None):
    with get_session() as session:
        categories = session.scalars(
            select(Category).order_by(Category.category_name)
        ).all()

        if not categories:
            return "No categories found."

        lines = ["Categories:"]

        for c in categories:
            lines.append(f"{c.category_id}. {c.category_name}")

        return "\n".join(lines)


# ============================================================
# Transactions
# ============================================================

def register_transaction(data):
    with get_session() as session:
        account = session.scalar(
            select(Account).where(Account.account_name == data.account_name)
        )

        if not account:
            return f"Account not found: {data.account_name}"

        category = session.scalar(
            select(Category).where(Category.category_name == data.category_name)
        )

        if not category:
            return f"Category not found: {data.category_name}"

        amount = float(data.amount)

        if data.type == "expense":
            amount = -abs(amount)
        else:
            amount = abs(amount)

        transaction = Transaction(
            account_id=account.account_id,
            category_id=category.category_id,
            transaction_amount=amount,
            transaction_date=data.date,
            transaction_description=data.description,
            transaction_type=data.type
        )

        session.add(transaction)
        session.commit()

        return (
            f"Transaction registered: "
            f"{data.type} {money(amount)} "
            f"on {data.date}"
        )


def update_transaction(data):
    with get_session() as session:
        transaction = session.get(Transaction, data.transaction_id)

        if not transaction:
            return f"Transaction not found: {data.transaction_id}"

        transaction.transaction_amount = float(data.amount)

        if data.description is not None:
            transaction.transaction_description = data.description

        session.commit()

        return f"Transaction updated: {data.transaction_id}"


def delete_transaction(data):
    with get_session() as session:
        transaction = session.get(Transaction, data.transaction_id)

        if not transaction:
            return f"Transaction not found: {data.transaction_id}"

        session.delete(transaction)
        session.commit()

        return f"Transaction deleted: {data.transaction_id}"


def list_transactions(data=None):
    with get_session() as session:
        transactions = session.scalars(
            select(Transaction)
            .order_by(desc(Transaction.transaction_date))
            .limit(50)
        ).all()

        if not transactions:
            return "No transactions found."

        lines = ["Transactions:"]

        for t in transactions:
            lines.append(
                f"{t.transaction_id}. "
                f"{t.transaction_date} | "
                f"{t.account.account_name} | "
                f"{t.category.category_name} | "
                f"{money(t.transaction_amount)} | "
                f"{t.transaction_description or ''}"
            )

        return "\n".join(lines)


def search_transactions(data):
    keyword = f"%{data.keyword}%"

    with get_session() as session:
        transactions = session.scalars(
            select(Transaction)
            .join(Account)
            .join(Category)
            .where(
                or_(
                    Transaction.transaction_description.ilike(keyword),
                    Account.account_name.ilike(keyword),
                    Category.category_name.ilike(keyword),
                )
            )
            .order_by(desc(Transaction.transaction_date))
        ).all()

        if not transactions:
            return "No matching transactions found."

        lines = ["Search results:"]

        for t in transactions:
            lines.append(
                f"{t.transaction_id}. "
                f"{t.transaction_date} | "
                f"{t.account.account_name} | "
                f"{t.category.category_name} | "
                f"{money(t.transaction_amount)} | "
                f"{t.transaction_description or ''}"
            )

        return "\n".join(lines)


# ============================================================
# Reports
# ============================================================

def account_balance(data):
    with get_session() as session:
        account = session.scalar(
            select(Account).where(Account.account_name == data.account_name)
        )

        if not account:
            return f"Account not found: {data.account_name}"

        balance = session.scalar(
            select(func.coalesce(func.sum(Transaction.transaction_amount), 0))
            .where(Transaction.account_id == account.account_id)
        )

        return f"Balance for {account.account_name}: {money(balance)}"


def monthly_summary(data):
    with get_session() as session:
        income = session.scalar(
            select(func.coalesce(func.sum(Transaction.transaction_amount), 0))
            .where(Transaction.transaction_amount > 0)
            .where(extract("year", Transaction.transaction_date) == data.year)
            .where(extract("month", Transaction.transaction_date) == data.month)
        )

        expenses = session.scalar(
            select(func.coalesce(func.sum(Transaction.transaction_amount), 0))
            .where(Transaction.transaction_amount < 0)
            .where(extract("year", Transaction.transaction_date) == data.year)
            .where(extract("month", Transaction.transaction_date) == data.month)
        )

        net = float(income) + float(expenses)

        return (
            f"Monthly Summary {data.year}-{data.month:02d}\n"
            f"Income: {money(income)}\n"
            f"Expenses: {money(abs(expenses))}\n"
            f"Net: {money(net)}"
        )


def monthly_income(data):
    with get_session() as session:
        total = session.scalar(
            select(func.coalesce(func.sum(Transaction.transaction_amount), 0))
            .where(Transaction.transaction_amount > 0)
            .where(extract("year", Transaction.transaction_date) == data.year)
            .where(extract("month", Transaction.transaction_date) == data.month)
        )

        return f"Monthly income {data.year}-{data.month:02d}: {money(total)}"


def monthly_expenses(data):
    with get_session() as session:
        total = session.scalar(
            select(func.coalesce(func.sum(Transaction.transaction_amount), 0))
            .where(Transaction.transaction_amount < 0)
            .where(extract("year", Transaction.transaction_date) == data.year)
            .where(extract("month", Transaction.transaction_date) == data.month)
        )

        return f"Monthly expenses {data.year}-{data.month:02d}: {money(abs(total))}"


def yearly_summary(data):
    with get_session() as session:
        income = session.scalar(
            select(func.coalesce(func.sum(Transaction.transaction_amount), 0))
            .where(Transaction.transaction_amount > 0)
            .where(extract("year", Transaction.transaction_date) == data.year)
        )

        expenses = session.scalar(
            select(func.coalesce(func.sum(Transaction.transaction_amount), 0))
            .where(Transaction.transaction_amount < 0)
            .where(extract("year", Transaction.transaction_date) == data.year)
        )

        net = float(income) + float(expenses)

        return (
            f"Yearly Summary {data.year}\n"
            f"Income: {money(income)}\n"
            f"Expenses: {money(abs(expenses))}\n"
            f"Net: {money(net)}"
        )


def expenses_by_category(data):
    with get_session() as session:
        query = (
            select(
                Category.category_name,
                func.sum(Transaction.transaction_amount)
            )
            .join(Transaction)
            .where(Transaction.transaction_amount < 0)
            .group_by(Category.category_name)
            .order_by(func.sum(Transaction.transaction_amount))
        )

        if data.year:
            query = query.where(
                extract("year", Transaction.transaction_date) == data.year
            )

        if data.month:
            query = query.where(
                extract("month", Transaction.transaction_date) == data.month
            )

        rows = session.execute(query).all()

        if not rows:
            return "No expenses found."

        lines = ["Expenses by category:"]

        for category, total in rows:
            lines.append(f"{category}: {money(abs(total))}")

        return "\n".join(lines)


def income_by_category(data):
    with get_session() as session:
        query = (
            select(
                Category.category_name,
                func.sum(Transaction.transaction_amount)
            )
            .join(Transaction)
            .where(Transaction.transaction_amount > 0)
            .group_by(Category.category_name)
            .order_by(desc(func.sum(Transaction.transaction_amount)))
        )

        if data.year:
            query = query.where(
                extract("year", Transaction.transaction_date) == data.year
            )

        if data.month:
            query = query.where(
                extract("month", Transaction.transaction_date) == data.month
            )

        rows = session.execute(query).all()

        if not rows:
            return "No income found."

        lines = ["Income by category:"]

        for category, total in rows:
            lines.append(f"{category}: {money(total)}")

        return "\n".join(lines)


def top_expenses(data):
    with get_session() as session:
        transactions = session.scalars(
            select(Transaction)
            .where(Transaction.transaction_amount < 0)
            .order_by(Transaction.transaction_amount)
            .limit(data.limit)
        ).all()

        if not transactions:
            return "No expenses found."

        lines = ["Top expenses:"]

        for t in transactions:
            lines.append(
                f"{t.transaction_id}. "
                f"{t.transaction_date} | "
                f"{t.category.category_name} | "
                f"{money(abs(t.transaction_amount))} | "
                f"{t.transaction_description or ''}"
            )

        return "\n".join(lines)
