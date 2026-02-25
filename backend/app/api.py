from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserAuth, UserRead
from app.security import decode_access_token
from app.crud import login_or_register, get_db
from app.models import User

router = APIRouter(prefix="/api")

@router.post("/login", response_model=UserRead)
async def login(
    user: UserAuth,
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    result = await login_or_register(session, user)

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
        username=result["user"].username,
    )

@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite='lax'
    )
    return True

@router.get('/me', response_model=UserRead)
async def me(request: Request, session: AsyncSession = Depends(get_db)):
    sub = decode_access_token(request.cookies.get('access_token'))['sub']
    user = await session.scalar(select(User).where(User.username == sub))
    return user