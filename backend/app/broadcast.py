from typing import Dict
from fastapi import WebSocket
from app.models import User
from uuid import UUID


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[UUID, Dict[str, any]] = {}

    async def connect(self, user: User, websocket: WebSocket):
        await websocket.accept()

        old = self.connections.get(user.id)
        if old:
            await old['websocket'].close()

        self.connections[user.id] = {
            'websocket': websocket,
            'username': user.username
        }

        await self.broadcast({
            'type': 'user_online', 
            'user': {
                'id': str(user.id),
                'username': user.username
            } 
        })

    def disconnect(self, user_id: UUID):
        self.connections.pop(user_id, None)

    async def broadcast(self, payload: dict):
        dead = []

        for user_id, data in list(self.connections.items()):
            try:
                await data['websocket'].send_json(payload)
            except Exception:
                dead.append(user_id)

        for user_id in dead:
            self.disconnect(user_id)

    async def broadcast_offline(self, user: User):
        await self.broadcast({
            "type": "user_offline",
            "user": {
                'id': str(user.id),
                'username': user.username
            }
        })


manager = ConnectionManager()