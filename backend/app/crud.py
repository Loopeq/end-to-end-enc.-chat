from fastapi import HTTPException
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
from sqlalchemy.orm import selectinload
from app.settings import get_settings
from app.models import Message

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


async def login_or_register(db: AsyncSession, user: UserAuth):
    username = user.username.strip()
    password = user.password.strip()
    
    if not len(username) or not len(password): 
        raise HTTPException(status_code=401, detail="Поля не заполнены")

    if len(username) > 64 or len(password) > 126:
        raise HTTPException(status_code=401, detail="Превышена длина полей")


    if len(username) < 4 or len(password) < 5:
        raise HTTPException(status_code=401, detail="Минимальная длина имени 4 символа, пароля 5 символов")
    
    db_user = await db.scalar(
        select(User).where(User.username == username)
    )
    
    if db_user:
        if not verify_password(password, db_user.hashed_password):
            return None
    else:
        db_user = User(
            username=username,
            hashed_password=hash_password(password),
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    
    token = create_access_token({"sub": db_user.username})
    
    return {"user": db_user, "token": token}

async def saveMessage(db: AsyncSession, message: str, user_id: int):
    msg = Message(
        user_id=user_id,
        content=message
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def getMessages(db: AsyncSession):
    stmt = select(Message).options(selectinload(Message.user)).order_by(Message.created_at.desc()).limit(50)
    result = await db.execute(stmt)
    return result.scalars().all()