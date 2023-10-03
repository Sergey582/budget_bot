from typing import List, Optional

from tortoise.functions import Sum
from tortoise.timezone import now

from app.core.modules.spending.models import Expense, User


async def create_user(user_id: int, username: str):
    await User.create(
        user_id=user_id,
        username=username,
    )
