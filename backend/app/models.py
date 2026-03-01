from typing import Type
import uuid
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def to_pydantic(obj, model: Type[BaseModel]):
    return model.model_validate(obj)

class UUIDMixin:
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
        index=True
    )

class User(UUIDMixin, Base):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    conversations1 = relationship("Conversation", back_populates="user1", foreign_keys="Conversation.user1_id")
    conversations2 = relationship("Conversation", back_populates="user2", foreign_keys="Conversation.user2_id")


class Conversation(UUIDMixin, Base):
    __tablename__ = "conversations"

    user1_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user2_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="uq_conversation_users"),
    )

    user1 = relationship("User", foreign_keys=[user1_id], back_populates="conversations1")
    user2 = relationship("User", foreign_keys=[user2_id], back_populates="conversations2")

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(UUIDMixin, Base):
    __tablename__ = "messages"

    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")