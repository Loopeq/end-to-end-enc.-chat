from sqlalchemy import select
from app.settings import get_settings
from app.models import User
from app.schemas import UserAuth
from app.security import hash_password, verify_password, create_access_token

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from app.settings import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)

async def get_db():
    async with SessionLocal() as session:
        yield session

async def get_or_create_user(db: AsyncSession, user: UserAuth):
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    db_user = result.scalar_one_or_none()

    if db_user:
        if verify_password(user.password, db_user.hashed_password):
            return db_user
        return None

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def login_or_register(db: AsyncSession, user: UserAuth):
    user_obj = await get_or_create_user(db, user)

    if not user_obj:
        return None

    token = create_access_token({"sub": user_obj.username})

    return {"user": user_obj, "token": token}