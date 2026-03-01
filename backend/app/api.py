from fastapi import APIRouter, Depends, HTTPException, Response, WebSocket
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserAuth, UserDTO
from app.security import decode_access_token
from app.crud import login_or_register, get_db
from app.di import current_user
from app.models import User
from app.broadcast import manager
import json
from app.schemas import UserDTO

router = APIRouter(prefix="/api")

@router.post("/login", response_model=UserDTO)
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

    return UserDTO(
        id=result['user'].id,
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

@router.get('/messages')
async def messages(db: AsyncSession = Depends(get_db)):
    # messages = await getMessages(db=db)
    # return [
    #     {
    #         'message': msg.content,
    #         'username': msg.user.username
    #     } 
    #     for msg in messages
    # ]
    return []

@router.get('/me', response_model=UserDTO)
async def me(current_user: User = Depends(current_user)):
    return current_user

@router.websocket("/ws")
async def ws_connection(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    token = websocket.cookies.get('access_token')
    if not token:
        raise HTTPException(400, 'Not authorized')
    sub = decode_access_token(token).get('sub', None)
    if not sub:
        raise HTTPException(400, 'Not authorized')
    user = await db.scalar(select(User).where(User.username == sub))
    if not user: 
        raise HTTPException(400, 'Not authorized')
    
    await manager.connect(user.username, websocket)

    await websocket.send_json({
        "type": "online_list",
        "users": list(manager.connections.keys())
    })

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
                # msg = await saveMessage(db=db, message=text, user_id=user.id)
                payload = {
                    "type": "chat_message",
                    "username": 'admin',
                    "message": text,
                }

                await manager.broadcast(payload)
    except:
        manager.disconnect(user.username)
        await manager.broadcast_offline(user.username)