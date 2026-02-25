from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserAuth, UserRead
from app.crud import login_or_register, get_db

router = APIRouter(prefix="/api")

@router.post("/login", response_model=UserRead)
async def login(
    user: UserAuth,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    result = await login_or_register(db, user)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = result["token"]

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24,
    )

    return UserRead(
        id=result["user"].id,
        username=result["user"].username,
    )