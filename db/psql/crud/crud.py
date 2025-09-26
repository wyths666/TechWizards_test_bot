from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.psql.models.models import User

async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> User | None:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()

async def get_user_by_phone(db: AsyncSession, phone_number: str) -> User | None:
    result = await db.execute(select(User).where(User.phone_number == phone_number))
    return result.scalar_one_or_none()

async def create_user(
    db: AsyncSession,
    telegram_id: int,
    phone_number: str,
    first_name: str,
    username: str
) -> User:
    user = User(
        telegram_id=telegram_id,
        phone_number=phone_number,
        first_name=first_name,
        username=username
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user