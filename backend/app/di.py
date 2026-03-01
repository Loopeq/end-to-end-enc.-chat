from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_db
from app.models import User
from app.security import decode_access_token

async def current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(400, 'Not authorized')
    sub = decode_access_token(token).get('sub', None)
    if not sub:
        raise HTTPException(400, 'Not authorized')
    user = await db.scalar(select(User).where(User.username == sub))
    if not user: 
        raise HTTPException(400, 'Not authorized')
    return user


