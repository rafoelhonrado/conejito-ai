"""
schemas.py

Pydantic models used to validate the JSON
returned by the LLM.
"""

from datetime import date
from decimal import Decimal
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Base
# ============================================================

class FinanceBase(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )


# ============================================================
# Account
# ============================================================

class CreateAccount(FinanceBase):

    action: Literal["create_account"]

    account_name: str = Field(
        min_length=1,
        max_length=80
    )

    account_bank: str = Field(
        min_length=1,
        max_length=80
    )


class UpdateAccount(FinanceBase):

    action: Literal["update_account"]

    account_id: int

    account_name: str = Field(
        min_length=1,
        max_length=80
    )

    account_bank: str = Field(
        min_length=1,
        max_length=80
    )


class DeleteAccount(FinanceBase):

    action: Literal["delete_account"]

    account_id: int


class GetAccount(FinanceBase):

    action: Literal["get_account"]

    account_id: int


class ListAccounts(FinanceBase):

    action: Literal["list_accounts"]


# ============================================================
# Category
# ============================================================

class CreateCategory(FinanceBase):

    action: Literal["create_category"]

    category_name: str = Field(
        min_length=1,
        max_length=80
    )


class UpdateCategory(FinanceBase):

    action: Literal["update_category"]

    category_id: int

    category_name: str = Field(
        min_length=1,
        max_length=80
    )


class DeleteCategory(FinanceBase):

    action: Literal["delete_category"]

    category_id: int


class ListCategories(FinanceBase):

    action: Literal["list_categories"]


# ============================================================
# Transaction
# ============================================================

class RegisterTransaction(FinanceBase):

    action: Literal["register_transaction"]

    account_name: str

    category_name: str

    amount: Decimal = Field(gt=0)

    date: date

    description: Optional[str] = Field(
        default=None,
        max_length=160
    )

    type: Literal[
        "income",
        "expense"
    ]


class UpdateTransaction(FinanceBase):

    action: Literal["update_transaction"]

    transaction_id: int

    amount: Decimal

    description: Optional[str] = None


class DeleteTransaction(FinanceBase):

    action: Literal["delete_transaction"]

    transaction_id: int


class ListTransactions(FinanceBase):

    action: Literal["list_transactions"]


class SearchTransactions(FinanceBase):

    action: Literal["search_transactions"]

    keyword: str


# ============================================================
# Reports
# ============================================================

class MonthlySummary(FinanceBase):

    action: Literal["monthly_summary"]

    year: int

    month: int = Field(
        ge=1,
        le=12
    )


class AccountBalance(FinanceBase):

    action: Literal["account_balance"]

    account_name: str


class ExpensesByCategory(FinanceBase):

    action: Literal["expenses_by_category"]

    year: Optional[int] = None

    month: Optional[int] = None


class IncomeByCategory(FinanceBase):

    action: Literal["income_by_category"]

    year: Optional[int] = None

    month: Optional[int] = None


class MonthlyIncome(FinanceBase):

    action: Literal["monthly_income"]

    year: int

    month: int = Field(
        ge=1,
        le=12
    )


class MonthlyExpenses(FinanceBase):

    action: Literal["monthly_expenses"]

    year: int

    month: int = Field(
        ge=1,
        le=12
    )


class YearlySummary(FinanceBase):

    action: Literal["yearly_summary"]

    year: int


class TopExpenses(FinanceBase):

    action: Literal["top_expenses"]

    limit: int = Field(
        default=10,
        ge=1,
        le=100
    )


# ============================================================
# Union
# ============================================================

FinanceAction = Union[
    CreateAccount,
    UpdateAccount,
    DeleteAccount,
    GetAccount,
    ListAccounts,
    CreateCategory,
    UpdateCategory,
    DeleteCategory,
    ListCategories,
    RegisterTransaction,
    UpdateTransaction,
    DeleteTransaction,
    ListTransactions,
    SearchTransactions,
    MonthlySummary,
    AccountBalance,
    ExpensesByCategory,
    IncomeByCategory,
    MonthlyIncome,
    MonthlyExpenses,
    YearlySummary,
    TopExpenses,
]

