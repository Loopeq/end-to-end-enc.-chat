from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.settings import get_settings
from app.models import Message, User
from app.schemas import UserAuth, ConversationDTO
from app.security import hash_password, verify_password, create_access_token

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from app.settings import get_settings
from app.models import Conversation
from app.models import to_pydantic

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

async def load_conversation(db: AsyncSession, partner_id: UUID, user_id: UUID):
    partner_id = UUID(partner_id)
    user1_id, user2_id = sorted([partner_id, user_id])
    conversation = await db.scalar(
        select(Conversation)
        .where(Conversation.user1_id == user1_id, Conversation.user2_id == user2_id)
        .options(selectinload(Conversation.user1), selectinload(Conversation.user2), selectinload(Conversation.messages))
    )
    if not conversation:
        conversation = Conversation(user1_id=user1_id, user2_id=user2_id)
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)

    conversation_dto = to_pydantic(conversation, ConversationDTO)
    data = conversation_dto.model_dump(mode='json')
    if str(conversation.user1_id) == str(user_id):
        partner = data["user2"]
    else:
        partner = data["user1"]

    data.pop("user1", None)
    data.pop("user2", None)

    data["partner"] = partner

    return data

async def save_message(db: AsyncSession, message: str, user_id: UUID, conversation_id: UUID):
    msg = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        content=message
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def get_messages(db: AsyncSession, conversation_id: UUID):
    result = await db.scalars(select(Message)
            .options(
                selectinload(Message.user),
                selectinload(Message.conversation)
            )                           
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc()))
    messages = result.all()

    formatted = []

    for msg in messages:
        if msg.user_id == msg.conversation.user1_id:
            to_user = msg.conversation.user2_id
        else:
            to_user = msg.conversation.user1_id

        formatted.append({
            "message": msg.content,
            "from": str(msg.user_id),
            "to": str(to_user)
        })

    return formatted