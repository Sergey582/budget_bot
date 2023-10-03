from typing import List, Optional

from tortoise.functions import Sum
from tortoise.timezone import now

from app.core.modules.spending.constants import DISPLAY_EXPENSE_CATEGORIES, CURRENCIES, EXPENSE_CATEGORY_OTHERS
from app.core.modules.spending.models import Expense, User


async def create_expense(user: User, amount: float, currency: str, category: str):
    await Expense.create(
        user=user,
        amount=amount,
        currency=currency,
        category=category,
        updated_at=now(),
        created_at=now(),
    )


async def get_expense(user: User, expense_id: int, ) -> Optional[Expense]:
    expense = await Expense.filter(
        user=user,
        id=expense_id,
    ).first()
    return expense


async def update_expense(user: User, expense_id: int, currency: str, amount: float, category: str):
    update_data = {}
    if currency is not None:
        update_data['currency'] = currency
    if amount is not None:
        update_data['amount'] = amount
    if category is not None:
        update_data['category'] = category
    await Expense.filter(id=expense_id, user=user).update(**update_data)


def get_display_category(category: int):
    return DISPLAY_EXPENSE_CATEGORIES[category]


async def delete_expense(user: User, expense_id: int) -> Expense:
    await Expense.filter(id=expense_id, user=user).delete()


async def get_expenses(user: User, from_id: int, limit: int) -> List[dict]:
    expenses_query = Expense.filter(user=user)

    if from_id:
        expenses_query = expenses_query.filter(pk__lte=from_id)

    if limit:
        expenses_query = expenses_query.limit(limit)
    expenses = await expenses_query

    result = []

    for expense in expenses:
        result.append({
            'currency': expense.currency,
            'amount': expense.amount,
            'category': expense.category,
            'display_category': get_display_category(expense.category),
            'created_at': expense.created_at,
            'updated_at': expense.updated_at,
        })

    return result


def get_next_id(messages: list, limit: int):
    if len(messages) == limit:
        next_id = messages[-1]["id"]
        messages = messages[:-1]
    else:
        next_id = None
    return messages, next_id


async def get_statistics(user: User):
    results = await Expense.filter(
        user=user
    ).annotate(
        total_amount=Sum('amount')
    ).group_by(
        'category'
    ).values(
        'total_amount',
        'category',
    )

    for item in results:
        item['display_category'] = get_display_category(item['category'])

    return results


def get_all_categories() -> List[dict]:
    result = []
    for key, value in DISPLAY_EXPENSE_CATEGORIES.items():
        result.append({
            'category': key,
            'display_category': value
        })
    return result


def get_all_currencies() -> List[str]:
    return CURRENCIES