from fastapi import APIRouter, Depends, HTTPException, Request, Response, WebSocket
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserAuth, UserRead
from app.security import decode_access_token
from app.crud import login_or_register, get_db
from app.models import User
from app.broadcast import manager
import json

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
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(400, 'Not authorized')
    sub = decode_access_token(token).get('sub', None)
    if not sub:
        raise HTTPException(400, 'Not authorized')
    user = await session.scalar(select(User).where(User.username == sub))
    if not user: 
        raise HTTPException(400, 'Not authorized')
    return user

@router.websocket("/ws")
async def ws_connection(websocket: WebSocket, session: AsyncSession = Depends(get_db)):
    token = websocket.cookies.get('access_token')
    if not token:
        raise HTTPException(400, 'Not authorized')
    sub = decode_access_token(token).get('sub', None)
    if not sub:
        raise HTTPException(400, 'Not authorized')
    user = await session.scalar(select(User).where(User.username == sub))
    if not user: 
        raise HTTPException(400, 'Not authorized')
    
    await manager.connect(user.username, websocket)

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            msg_type = data.get("type")

            if msg_type == "ping":
                await websocket.send_json({"type": "pong"})
                continue

            if msg_type == "chat_message":
                text = data.get("message", "")

                payload = {
                    "type": "chat_message",
                    "username": user.username,
                    "message": text,
                }

                await manager.broadcast(payload)
    except:
        manager.disconnect(user.username)
        await manager.broadcast_offline(user.username)