from pydantic import BaseModel
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