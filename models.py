"""
models.py

SQLAlchemy ORM models.
"""

from datetime import datetime, date

from sqlalchemy import (
    String,
    Float,
    Integer,
    Date,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from db import Base


# ============================================================
# Account
# ============================================================

class Account(Base):

    __tablename__ = "account"

    account_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    account_name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True,
        index=True
    )

    account_bank: Mapped[str] = mapped_column(
        String(80),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan"
    )


# ============================================================
# Category
# ============================================================

class Category(Base):

    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    category_name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<Category("
            f"id={self.category_id}, "
            f"name='{self.category_name}')>"
        )


# ============================================================
# Transaction
# ============================================================

class Transaction(Base):

    __tablename__ = "transactions"

    transaction_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.account_id"),
        nullable=False,
        index=True
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.category_id"),
        nullable=False,
        index=True
    )

    transaction_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True
    )

    transaction_description: Mapped[str | None] = mapped_column(
        String(160),
        nullable=True
    )

    transaction_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    account: Mapped["Account"] = relationship(
        back_populates="transactions"
    )

    category: Mapped["Category"] = relationship(
        back_populates="transactions"
    )

    def __repr__(self):

        return (
            f"<Transaction("
            f"id={self.transaction_id}, "
            f"amount={self.transaction_amount}, "
            f"type='{self.transaction_type}')>"
        )
