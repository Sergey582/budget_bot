from datetime import datetime
from typing import List, Optional

from app.core.modules.spending.constants import (CURRENCIES,
                                                 DISPLAY_EXPENSE_CATEGORIES)
from app.core.modules.spending.models import Expense, User
from tortoise.functions import Sum
from tortoise.timezone import now


async def create_expense(user: User, amount: float, currency: str, category: str, transaction_date: datetime):
    await Expense.create(
        user=user,
        amount=amount,
        currency=currency,
        category=category,
        transaction_date=transaction_date,
        updated_at=now(),
        created_at=now(),
    )


async def get_expense(user: User, expense_id: int, ) -> Optional[Expense]:
    expense = await Expense.filter(
        user=user,
        id=expense_id,
    ).first()
    return expense


async def update_expense(
        user: User,
        expense_id: int,
        currency: str,
        amount: float,
        category: str,
        transaction_date: datetime,
):
    update_data = {}
    if currency is not None:
        update_data['currency'] = currency
    if amount is not None:
        update_data['amount'] = amount
    if category is not None:
        update_data['category'] = category

    if transaction_date is not None:
        update_data['transaction_date'] = transaction_date

    await Expense.filter(id=expense_id, user=user).update(**update_data)


def get_display_category(category: int):
    return DISPLAY_EXPENSE_CATEGORIES[category]


async def delete_expense(user: User, expense_id: int) -> Expense:
    await Expense.filter(id=expense_id, user=user).delete()


async def get_expenses(
        user: User,
        from_id: int,
        limit: int,
        transaction_date_from: datetime,
        transaction_date_to: datetime,
) -> List[dict]:
    expenses_query = Expense.filter(user=user)

    if from_id:
        expenses_query = expenses_query.filter(pk__lte=from_id).order_by('-id')

    if transaction_date_from:
        expenses_query = expenses_query.filter(transaction_date__gte=transaction_date_from)

    if transaction_date_to:
        expenses_query = expenses_query.filter(transaction_date__lte=transaction_date_to)

    if limit:
        expenses_query = expenses_query.limit(limit + 1)

    expenses = await expenses_query

    result = []

    for expense in expenses:
        result.append({
            'id': expense.pk,
            'currency': expense.currency,
            'amount': expense.amount,
            'category': expense.category,
            'display_category': get_display_category(expense.category),
            'transaction_date': expense.transaction_date,
            'created_at': expense.created_at,
            'updated_at': expense.updated_at,
        })

    return result


def get_last_expense_id(expenses: list, limit: int):
    if limit and len(expenses) == limit + 1:
        last_id = expenses[-1]["id"]
        expenses = expenses[:-1]
    else:
        last_id = None
    return expenses, last_id


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
