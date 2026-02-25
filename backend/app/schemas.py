from pydantic import BaseModel

class UserAuth(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"