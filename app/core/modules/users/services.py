from app.core.modules.spending.models import User


async def create_user(user_id: int, username: str):
    await User.create(
        user_id=user_id,
        username=username,
    )
