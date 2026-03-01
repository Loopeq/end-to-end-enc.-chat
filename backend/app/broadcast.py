from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, user: str, websocket: WebSocket):
        await websocket.accept()

        old = self.connections.get(user)
        if old:
            await old.close()

        self.connections[user] = websocket

        await self.broadcast({
            'type': 'user_online', 
            'username': user 
        })

    def disconnect(self, user: str):
        self.connections.pop(user, None)

    async def broadcast(self, payload: dict):
        dead = []

        for user, socket in list(self.connections.items()):
            try:
                await socket.send_json(payload)
            except Exception:
                dead.append(user)

        for user in dead:
            self.disconnect(user)

    async def broadcast_offline(self, user: str):
        await self.broadcast({
            "type": "user_offline",
            "username": user
        })

manager = ConnectionManager()