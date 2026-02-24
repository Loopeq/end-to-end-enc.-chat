from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.schemas import UserAuth, UserRead
from app.crud import get_db, login_or_register

router = APIRouter(prefix="/api")

@router.post("/login", response_model=UserRead)
def login(user: UserAuth, response: Response, db: Session = Depends(get_db)):
    result = login_or_register(db, user)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = result["token"]

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60*60*24,
    )

    return UserRead(id=result["user"].id, username=result["user"].username)