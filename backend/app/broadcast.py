from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, user: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[user] = websocket

        await websocket.send_json({
            'type': 'online_list',
            'users': list(self.connections.keys())
        })

        await self.broadcast({
            'type': 'user_online',
            'username': user
        })
    
    def disconnect(self, user: str):
        self.connections.pop(user, None)
    
    async def broadcast(self, payload: dict):
        for socket in self.connections.values():
            await socket.send_json(payload)

    async def broadcast_offline(self, user: str):
        await self.broadcast({
            "type": "user_offline",
            "username": user
        })

manager = ConnectionManager()