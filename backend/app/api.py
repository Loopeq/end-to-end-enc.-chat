from fastapi import APIRouter, Depends, HTTPException, Response, WebSocket
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserAuth, UserDTO
from app.security import decode_access_token
from app.crud import get_messages, load_conversation, login_or_register, get_db, save_message
from app.di import current_user
from app.models import User
from app.broadcast import manager
import json
from app.schemas import UserDTO
from uuid import UUID

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

@router.get('/me', response_model=UserDTO)
async def me(current_user: User = Depends(current_user)):
    return current_user

@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite='lax'
    )
    return True

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
    
    await manager.connect(user, websocket)

    await websocket.send_json({
        "type": "online_list",
        "users": [
            {"id": str(user_id), "username": data['username']} 
            for user_id, data in manager.connections.items()
        ]
    })

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            msg_type = data.get("type")
            
            match msg_type:
                case 'ping':
                    await websocket.send_json({"type": "pong"})
                case 'handshake':
                    try:
                        partner_id = data.get('partner_id', None)
                        conversation = await load_conversation(db=db, partner_id=partner_id, user_id=user.id)
                        await websocket.send_json({"type": "handshake", 
                                                   'conversation': conversation})
                        messages = await get_messages(db=db, conversation_id=conversation['id'])
                        await websocket.send_json({"type": "chat_messages", 
                                                   'messages': messages})
                    except Exception as e: 
                        print(e)
            if msg_type == "chat_message":
                text = data.get("message", "")
                _conversation_id = data.get("conversation_id", None)
                _to = data.get('to', None)
                _from = user.id
                payload = {
                    "type": "chat_message",
                    "to": str(_to),
                    "from": str(_from),
                    "message": text,
                }
                await manager.send_to(_to=_from, payload=payload)
                await manager.send_to(_to=UUID(_to), payload=payload)
                await save_message(db=db, message=text, user_id=_from, conversation_id=_conversation_id)

    except Exception:
        manager.disconnect(user.id)
        await manager.broadcast_offline(user)