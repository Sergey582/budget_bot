from datetime import datetime, date
from typing import List, Optional, Sequence

from pydantic import BaseModel, validator

from app.core.modules.spending.constants import EXPENSE_CATEGORIES, CURRENCIES


class CreateSpendingRequest(BaseModel):
    amount: float
    category: int
    currency: str
    transaction_date: datetime

    @validator('currency')
    def validate_currency(cls, value: int):
        if value not in CURRENCIES:
            raise ValueError('Invalid currency')
        return value

    @validator('category')
    def validate_category(cls, value: int):
        if value not in EXPENSE_CATEGORIES:
            raise ValueError('Invalid category')
        return value


class UpdateExpenseRequest(BaseModel):
    currency: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[int] = None
    transaction_date: Optional[datetime] = None

    @validator('currency')
    def validate_currency(cls, value: int):
        if value not in CURRENCIES:
            raise ValueError('Invalid currency')
        return value

    @validator('category')
    def validate_category(cls, value: int):
        if value not in EXPENSE_CATEGORIES:
            raise ValueError('Invalid category')
        return value


class ExpenseResponse(BaseModel):
    currency: str
    amount: float
    category: int
    display_category: str
    created_at: datetime
    updated_at: datetime
    transaction_date: datetime


class PaginationQueryData(BaseModel):
    from_id: Optional[int]
    limit: Optional[int]


class ExpensesQueryFilters(PaginationQueryData):
    transaction_date_from: Optional[datetime]
    transaction_date_to: Optional[datetime]


class ExpenseData(BaseModel):
    currency: str
    amount: float
    category: int
    display_category: str
    transaction_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class ExpensesListData(BaseModel):
    next_id: Optional[int] = None
    messages: Sequence[ExpenseData]


class CategoryStatisticsData(BaseModel):
    total_amount: float
    category: int
    display_category: str


class CategoriesStatisticsData(BaseModel):
    data: List[CategoryStatisticsData]


class CategoryData(BaseModel):
    category: int
    display_category: str


class CategoriedListData(BaseModel):
    data: List[CategoryData]


class CurrenciesListData(BaseModel):
    data: List[str]
