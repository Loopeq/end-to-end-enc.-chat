from pydantic import BaseModel, field_serializer, validator
from uuid import UUID

class UserAuth(BaseModel):
    username: str
    password: str

class UserDTO(BaseModel):
    id: UUID
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ConversationDTO(BaseModel):
    id: UUID
    
    user1: UserDTO
    user2: UserDTO

    class Config:
        from_attributes = True

    