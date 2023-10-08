from app.api.public.modules.spending.serializers import (
    CategoriesStatisticsData, CreateSpendingRequest, ExpenseResponse,
    ExpensesListData, PaginationQueryData, UpdateExpenseRequest, CategoriedListData, CurrenciesListData,
    ExpensesQueryFilters)
from app.core.modules.spending.models import User
from app.core.modules.spending.services import (create_expense, delete_expense,
                                                get_expense, get_expenses,
                                                get_next_id, get_statistics,
                                                update_expense, get_all_categories, get_all_currencies,
                                                get_display_category)
from app.core.modules.users.auth import user_auth_check
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from starlette.responses import Response

router = APIRouter()


@router.get(
    "/currencies",
    tags=["expense"],
    summary="Get available currencies",
    response_model=CurrenciesListData,
    status_code=status.HTTP_200_OK,
)
async def router_get_all_categories(
        user: User = Depends(user_auth_check),
):
    data = get_all_currencies()
    return CurrenciesListData(data=data)


@router.get(
    "/categorises",
    tags=["expense"],
    summary="Get available categories",
    response_model=CategoriedListData,
    status_code=status.HTTP_200_OK,
)
async def router_get_all_categories(
        user: User = Depends(user_auth_check),
):
    data = get_all_categories()
    return CategoriedListData(data=data)


@router.post(
    "/expense",
    tags=["expense"],
    summary="Create expense",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def router_create_expense(
        request_data: CreateSpendingRequest,
        user: User = Depends(user_auth_check),
):
    await create_expense(
        user=user,
        amount=request_data.amount,
        currency=request_data.currency,
        category=request_data.category,
        transaction_date=request_data.transaction_date,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/expense/{expense_id}",
    tags=["expense"],
    summary="Get expense",
    response_model=ExpenseResponse,
    status_code=status.HTTP_200_OK,
)
async def router_get_expense_by_id(
        expense_id: int,
        user: User = Depends(user_auth_check),
):
    expense = await get_expense(expense_id=expense_id, user=user)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="expense id does not exist")
    return ExpenseResponse(
        currency=expense.currency,
        amount=expense.amount,
        category=expense.category,
        display_category=get_display_category(expense.category),
        transaction_date=expense.transaction_date,
        created_at=expense.created_at,
        updated_at=expense.updated_at,
    )


@router.patch(
    "/expense/{expense_id}",
    tags=["expense"],
    summary="Update expense",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def router_update_expense(
        expense_id: int,
        data: UpdateExpenseRequest,
        user: User = Depends(user_auth_check),
):
    await update_expense(
        user=user,
        expense_id=expense_id,
        currency=data.currency,
        category=data.category,
        amount=data.amount,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Create a route to delete an expense by ID
@router.delete(
    "/expenses/{expense_id}",
    tags=["expense"],
    summary="Delete expense",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def router_delete_expense(
        expense_id: int,
        user: User = Depends(user_auth_check),
):
    await delete_expense(expense_id=expense_id, user=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/expenses/",
    tags=["expense"],
    summary="Get list of expenses",
    response_model=ExpensesListData,
    status_code=status.HTTP_200_OK,
)
async def router_get_expenses(
        filters: ExpensesQueryFilters = Depends(),
        user: User = Depends(user_auth_check),
):
    limit = filters.limit + 1

    messages = await get_expenses(
        user=user,
        from_id=filters.from_id,
        limit=limit,
        transaction_date_from=filters.transaction_date_from,
        transaction_date_to=filters.transaction_date_to,
    )

    messages, next_id = get_next_id(messages, limit)

    return ExpensesListData(messages=messages, next_id=next_id)


@router.get(
    "/statistics",
    tags=["expense"],
    summary="Get list of expenses",
    response_model=CategoriesStatisticsData,
    status_code=status.HTTP_200_OK,
)
async def router_get_statistics(
        user: User = Depends(user_auth_check),
):
    data = await get_statistics(user=user)
    return CategoriesStatisticsData(data=data)
