"""
router.py

Routes validated finance actions to the correct tool function.
"""

from tools import (
    create_account,
    create_accounts,
    update_account,
    delete_account,
    get_account,
    list_accounts,
    create_category,
    update_category,
    delete_category,
    list_categories,
    register_transaction,
    update_transaction,
    delete_transaction,
    list_transactions,
    search_transactions,
    account_balance,
    monthly_summary,
    expenses_by_category,
    income_by_category,
    monthly_income,
    monthly_expenses,
    yearly_summary,
    top_expenses,
)


ACTION_MAP = {
    "create_account": create_account,
    "create_accounts": create_accounts,
    "update_account": update_account,
    "delete_account": delete_account,
    "get_account": get_account,
    "list_accounts": list_accounts,

    "create_category": create_category,
    "update_category": update_category,
    "delete_category": delete_category,
    "list_categories": list_categories,

    "register_transaction": register_transaction,
    "update_transaction": update_transaction,
    "delete_transaction": delete_transaction,
    "list_transactions": list_transactions,
    "search_transactions": search_transactions,

    "account_balance": account_balance,
    "monthly_summary": monthly_summary,
    "expenses_by_category": expenses_by_category,
    "income_by_category": income_by_category,
    "monthly_income": monthly_income,
    "monthly_expenses": monthly_expenses,
    "yearly_summary": yearly_summary,
    "top_expenses": top_expenses,
}


def execute(action_obj):
    """
    Execute a validated Pydantic action object.
    """

    if isinstance(action_obj, dict):
        if action_obj.get("action") == "clarify":
            return action_obj.get("question", "Please provide more details.")
        return f"Invalid raw action object: {action_obj}"

    action_name = action_obj.action

    tool_func = ACTION_MAP.get(action_name)

    if not tool_func:
        return f"Unknown action: {action_name}"

    return tool_func(action_obj)
